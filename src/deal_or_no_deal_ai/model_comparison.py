"""GEN-COMPARE-1.0 offline preparation and local response checks; no dispatch."""

from dataclasses import asdict
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
import tomllib
from typing import Literal

from pydantic import ValidationError

from .context import InputError, canonical_decimal, canonical_json, fingerprint, load_instruction
from .contracts import DealTermsWire, StrictModel, parse_extraction, parse_synthesis
from .documents import verify_evidence
from .policy import PolicyConfig, aggregate_workflow, evaluate_policy
from .services import RegisteredFixtureCase, evaluate_panels, load_registered_case, validate_registered_case
from .synthesis import prepare_synthesis, synthesis_task


class Baseline(StrictModel):
    model_id: Literal["Qwen/Qwen3-30B-A3B-Instruct-2507"]
    input_usd_per_million_tokens: Literal["0.10"]
    output_usd_per_million_tokens: Literal["0.30"]


class Challenger(StrictModel):
    model_id: Literal["nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"]
    input_usd_per_million_tokens: Literal["0.06"]
    output_usd_per_million_tokens: Literal["0.24"]


class ComparisonProfile(StrictModel):
    version: Literal["GEN-COMPARE-1.0"]
    provider: Literal["NEBIUS"]
    paid_execution_enabled: Literal[False]
    allowance_status: Literal["NOT_APPROVED"]
    provider_contract_status: Literal["UNVERIFIED"]
    pricing_checked_on: Literal["2026-10-23"]
    baseline: Baseline
    challenger: Challenger


def load_comparison_profile(root: Path) -> ComparisonProfile:
    with (root / "config/generation_comparison.toml").open("rb") as stream:
        return ComparisonProfile.model_validate(tomllib.load(stream))


def estimate_generation_cost(model: Baseline | Challenger, *, input_tokens: int,
                             billed_output_tokens: int) -> str:
    """Dated list-rate estimate; billed output must include billed reasoning."""
    for value in (input_tokens, billed_output_tokens):
        if type(value) is not int or value < 0:
            raise InputError("NONNEGATIVE_INTEGER_TOKEN_COUNTS_REQUIRED")
    cost = (Decimal(model.input_usd_per_million_tokens) * input_tokens
            + Decimal(model.output_usd_per_million_tokens) * billed_output_tokens) / Decimal(1000000)
    return canonical_decimal(cost)


def prepare_extraction_task(root: Path, case: RegisteredFixtureCase) -> dict:
    """Full registered evidence, not a top-k subset or generic upload adapter."""
    validate_registered_case(case)
    coverage = verify_evidence(scope=case.scope, sources=tuple(dict.fromkeys(b.source for b in case.inventory)),
        inventory=case.inventory, roots=(), selected=tuple(b.block_id for b in case.inventory),
        max_context_bytes=262144, mode="BASELINE", purpose="FULL_EXTRACTION")
    if coverage.status != "COMPLETE":
        raise InputError("EXTRACTION_SOURCE_COVERAGE_UNVERIFIED")
    prompt = load_instruction(root, "extractor", case.registration.instruction_hashes["extractor"])
    return dict(task="extractor", instruction=prompt,
                  output_schema=DealTermsWire.model_json_schema(),
                  sources={block.block_id: dict(text=block.text, source_id=block.source.source_id,
                            source_version=block.source.version, source_sha256=block.source.content_digest,
                            page=block.page, start=block.start, end=block.start + len(block.text),
                            dependencies=list(block.dependencies)) for block in coverage.dispatch_blocks},
                  bases=case.case_data["bases"],
                  review_basis=dict(scope=asdict(case.scope), review_as_of=case.registration.review_as_of,
                                    cutoff=case.registration.evidence_cutoff_at,
                                    source_profile=case.registration.source_profile_version))


def prepare_comparison(root: Path) -> dict:
    """Explicit read-only registered-source inspection; no inference or scoring."""
    profile = load_comparison_profile(root)
    case = load_registered_case(root)
    # Evaluator answers/response files are never put into either task packet.
    packet = prepare_extraction_task(root, case)
    task_digest = fingerprint("GEN-COMPARE-TASK-1.0", packet)
    synthesis_packet = prepare_synthesis(case)
    synthesis_input = synthesis_task(root, case, synthesis_packet)
    synthesis_digest = fingerprint("GEN-COMPARE-TASK-1.0", synthesis_input)
    readiness = [
        dict(scenario="E-N01", variant="default", stage="extractor",
             source_status="REGISTERED_SOURCE_VERIFIED", packet_status="PREPARED_OFFLINE",
             execution_status="BLOCKED_PROVIDER_TOKEN_PREFLIGHT_AND_ALLOWANCE"),
        dict(scenario="E-N01", variant="default", stage="synthesizer", source_status="REGISTERED_SOURCE_VERIFIED",
             packet_status="PREPARED_OFFLINE", execution_status="BLOCKED_PROVIDER_TOKEN_PREFLIGHT_AND_ALLOWANCE"),
    ]
    for scenario, variant in (("E-M01", "default"), ("E-C01", "default"), ("E-F03", "reject-supported")):
        readiness.append(dict(scenario=scenario, variant=variant, stage="workflow",
                              source_status="NOT_READY", packet_status="NOT_READY",
                              execution_status="SOURCE_PACK_REGISTRATION_AND_RUBRIC_PENDING"))
    arms = []
    for role in ("baseline", "challenger"):
        model = getattr(profile, role)
        arms.append(dict(role=role, model_id=model.model_id, shared_task_digest=task_digest,
                         shared_task_digests=dict(extractor=task_digest, synthesizer=synthesis_digest),
                         status="NOT_RUN", schema_valid=None, field_accuracy=None,
                         source_grounding=None, risk_recall=None, false_positive_risk_count=None,
                         billed_input_tokens=None, billed_output_tokens=None, billed_reasoning_tokens=None,
                         latency_ms=None, actual_cost_usd=None, requests=None, retries=None))
    report = dict(version=profile.version, evidence_type="OFFLINE_COMPARISON_PREPARATION_ONLY",
                  profile=profile.model_dump(), registration_dependency_digest=case.dependency_digest,
                  instruction_hashes=case.registration.instruction_hashes,
                  shared_task_digest=task_digest, shared_task_packet=packet,
                  task_packets=dict(extractor=packet, synthesizer=synthesis_input),
                  task_digests=dict(extractor=task_digest, synthesizer=synthesis_digest),
                  serialized_task_bytes=dict(extractor=len(canonical_json(packet).encode("utf-8")),
                                             synthesizer=len(canonical_json(synthesis_input).encode("utf-8"))),
                  serialized_packet_bytes=len(canonical_json(packet).encode("utf-8")),
                  token_count=None, token_measurement_status="NOT_VERIFIED",
                  readiness=readiness, arms=arms, preparation_provider_requests=0,
                  application_model_changed=False, winner=None,
                  limitation="Prepared packet and test-double checks are not an executed model comparison")
    report["plan_digest"] = fingerprint("GEN-COMPARE-PLAN-1.0", report)
    return report


def check_extraction_response(raw: str | bytes, case: RegisteredFixtureCase) -> dict:
    """Conservative reference check only; no semantic support or model attribution."""
    validate_registered_case(case)
    expected = case.wire.model_dump()
    fields = [(group, field) for group in ("terms", "financial_inputs") for field in expected[group]]
    available = sum(expected[group][field]["value"] is not None for group, field in fields)
    result = dict(evidence_type="LOCAL_RESPONSE_CHECK_ONLY", schema_valid=False,
                  fields_total=len(fields), fields_exact_value_basis_match=0,
                  available_slots=available, available_slots_exact_value_basis_match=0,
                  field_results=[], missing_fields=None, conflict_fields=None,
                  unresolved_source_refs=None, unresolved_basis_refs=None,
                  source_grounding="MANUAL_REVIEW_REQUIRED", model_quality_status="NOT_ESTABLISHED",
                  credit_disposition=None)
    try:
        wire = parse_extraction(raw)
    except (InputError, ValidationError):
        return result  # A failed response remains in the field denominator.
    supplied = wire.model_dump()
    result["schema_valid"] = True
    result["fields_exact_value_basis_match"] = sum(
        (supplied[group][field]["value"], supplied[group][field]["basis_id"])
        == (expected[group][field]["value"], expected[group][field]["basis_id"])
        for group, field in fields)
    for group, field in fields:
        actual, gold = supplied[group][field], expected[group][field]
        value_match = actual["value"] == gold["value"]
        basis_match = actual["basis_id"] == gold["basis_id"]
        result["field_results"].append(dict(field=f"{group}.{field}", expected=gold, supplied=actual,
            value_match=value_match, basis_match=basis_match,
            expected_reference_set_match=set(actual["refs"]) == set(gold["refs"]),
            semantic_support="MANUAL_REVIEW_REQUIRED"))
        result["available_slots_exact_value_basis_match"] += int(
            gold["value"] is not None and value_match and basis_match)
    result["missing_fields"] = [f"{g}.{f}" for g, f in fields if supplied[g][f]["value"] is None]
    result["conflict_fields"] = [item["field_name"] for item in supplied["conflicts"]]
    facts = [supplied[group][field] for group, field in fields]
    facts.extend(candidate for conflict in supplied["conflicts"] for candidate in conflict["candidates"])
    source_ids = {block.block_id for block in case.inventory}
    basis_ids = set(case.case_data["bases"])
    result["unresolved_source_refs"] = len({ref for fact in facts for ref in fact["refs"] if ref not in source_ids})
    result["unresolved_basis_refs"] = len({fact["basis_id"] for fact in facts
                                          if fact["basis_id"] is not None and fact["basis_id"] not in basis_ids})
    return result


def check_synthesis_response(raw: str | bytes, case: RegisteredFixtureCase, packet: dict) -> dict:
    """Check structure/lineage and prepare manual support review, never approve prose."""
    if packet != prepare_synthesis(case):
        raise InputError("SYNTHESIS_CURRENT_INPUT_MISMATCH")
    result = dict(evidence_type="LOCAL_RESPONSE_CHECK_ONLY", schema_valid=False,
        source_grounding="MANUAL_REVIEW_REQUIRED", model_quality_status="NOT_ESTABLISHED",
        credit_disposition=None, narrative_targets=[], reference_problems=[],
        routing=None, narrative_scores=None, risk_recall=None, false_positive_risk_count=None, ragas=None,
        limitations=dict(analysis_scope=packet["request"]["financial"]["analysis_scope"],
                         covenant_status=packet["request"]["financial"]["covenant_status"],
                         ebitda_reconciliation=packet["request"]["financial"]["ebitda_reconciliation"]))
    try:
        wire = parse_synthesis(raw)
    except (InputError, ValidationError):
        return result
    result["schema_valid"] = True
    result["proposed_panel_decision"] = wire.panel_decision.model_dump()
    result["reference_context_cutoff"] = "ORIGINAL_PRE_SYNTHESIS_PACKET"
    refs = packet["request"]["reference_dictionary"]
    fields = [(f"observations[{i}].text", item.text, item.refs) for i, item in enumerate(wire.observations)]
    fields.append(("panel_decision.rationale", wire.panel_decision.rationale, wire.rationale_refs))
    links = {item.index: item.refs for item in wire.condition_links}
    fields.extend((f"panel_decision.conditions[{i}]", text, links[i])
                  for i, text in enumerate(wire.panel_decision.conditions))
    if wire.proposed_action is not None:
        fields.append(("proposed_action.reason", wire.proposed_action.reason, wire.proposed_action.refs))
    for path, text, handles in fields:
        closure, problems = {}, set()
        def resolve(handle, ancestors=()):
            if handle in ancestors:
                problems.add("CYCLIC_REFERENCE:" + handle)
                return
            if handle not in refs:
                problems.add("UNRESOLVED_REFERENCE:" + handle)
                return
            if handle in closure:
                return
            closure[handle] = refs[handle]
            for child in refs[handle]["refs"]:
                resolve(child, ancestors + (handle,))
        for handle in handles:
            resolve(handle)
        result["narrative_targets"].append(dict(field_path=path, text=text,
            text_sha256=sha256(text.encode("utf-8")).hexdigest(), refs=handles,
            reference_closure=closure, reference_problems=sorted(problems),
            support="MANUAL_REVIEW_REQUIRED",
            review_questions=["Does every material assertion follow from the cited evidence?",
                              "Are period, subject, units and limitations preserved?",
                              "Are adverse findings omitted or clearance/fulfillment falsely claimed?"]))
        result["reference_problems"].extend(dict(field_path=path, reason=p) for p in sorted(problems))
    financial, _, risk = evaluate_panels(case)
    cfg = case.case_data["policy_config"]
    policy = evaluate_policy({m.metric_id: m for m in financial.metric_results}, case.wire.terms,
        config=PolicyConfig(cfg["secured_equipment"], cfg["kyc_fixture_required"], cfg["sanctions_fixture_required"], cfg["basis"]),
        dependency_digest=case.dependency_digest, metric_source_refs=dict(financial.metric_source_refs),
        material_financial_ready=True, synthesis_complete=True, confidence=wire.panel_decision.confidence)
    workflow = aggregate_workflow((policy.workflow, risk.score.workflow))
    required = workflow != "CONTINUE"
    result["routing"] = dict(workflow=workflow, mandatory_review_required=required,
        proposed_escalate_to_human=wire.panel_decision.escalate_to_human,
        escalation_proposal_matches_controls=required == wire.panel_decision.escalate_to_human,
        policy_results=[asdict(rule) for rule in policy.rules], application_action="NOT_AUTHORIZED_BY_REVIEW_TOOL")
    return result
