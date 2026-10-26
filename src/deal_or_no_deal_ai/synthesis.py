"""Source-bound E-N01 synthesis preparation and exact Fixture validation only."""

from dataclasses import asdict
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Literal

from .context import InputError, canonical_json, fingerprint, load_instruction, primitive, strict_json
from .contracts import Scope, StrictModel, SynthesisWire, hydrate_narrative, parse_synthesis, wire_json
from .policy import PolicyConfig, aggregate_workflow, evaluate_policy
from .services import RegisteredFixtureCase, evaluate_panels


class SynthesisRegistration(StrictModel):
    version: Literal["E-N01-SYNTHESIS-1.0"]
    scenario_id: Literal["E-N01", "E-F03", "E-P01"]
    variant: Literal["default", "review"]
    mode: Literal["FIXTURE"]
    case_dependency_digest: str
    package_digest: str
    input_digest: str
    wire_sha256: str
    rubric_sha256: str
    authoring_basis: str
    semantic_support: Literal["AI_AUTHORED_EDUCATIONAL_FIXTURE_NOT_HUMAN_VERIFIED"]


def prepare_synthesis(case: RegisteredFixtureCase, *, panels=None) -> dict:
    return _prepare_packet(case, panels=panels, inspection=False)


def prepare_source_inspection(case: RegisteredFixtureCase) -> dict:
    """Partial evidence read model; never a permission to dispatch synthesis."""
    return _prepare_packet(case, inspection=True)


def _prepare_packet(case: RegisteredFixtureCase, *, panels=None, inspection=False) -> dict:
    general=case.registration.version=='UPLOAD-PROFILE-1.0'
    inspection=inspection or general
    financial, compliance, risk = evaluate_panels(case) if panels is None else panels
    if (financial.dependency_digest != case.dependency_digest or compliance.dependency_digest != case.dependency_digest
            or risk.score.dependency_digest != case.dependency_digest or financial.scope != case.scope):
        raise InputError("SYNTHESIS_PANEL_SCOPE_MISMATCH")
    if not inspection and (financial.completeness != "COMPLETE" or risk.score.total is None or risk.score.missing):
        raise InputError("SYNTHESIS_PREREQUISITES_INCOMPLETE")
    supported_exception = (case.registration.scenario_id in ("E-F03", "E-P01") and compliance.completeness == "PRE_SYNTHESIS"
                           and compliance.exception_rule_ids == ("SYN-ESC-001",) and risk.score.band == "MODERATE"
                           and compliance.workflow == "ESCALATE" and risk.score.workflow == "REVIEW_REQUIRED")
    if not inspection and not supported_exception and aggregate_workflow((compliance.workflow, risk.score.workflow)) != "CONTINUE":
        raise InputError("E_N01_DEFAULT_PANEL_ROUTE_CHANGED")
    refs = {b.block_id: dict(kind="SOURCE", label=f"{b.source.source_id} {b.source.version}, page {b.page}",
                             source_id=b.source.source_id, source_version=b.source.version,
                             source_sha256=b.source.content_digest, page=b.page, text=b.text, refs=[])
            for b in case.inventory}
    metrics = []
    metric_handles = {}
    for metric in financial.metric_results:
        handle = "calc:DSCR" if metric.metric_id == "CALC-004" else "calc:" + metric.metric_id
        metric_handles[metric.metric_id] = handle
        value = primitive(asdict(metric))
        value["source_refs"] = list(dict(financial.metric_source_refs)[metric.metric_id])
        metrics.append(value)
        refs[handle] = dict(kind="CALCULATION", label=f"{metric.metric_id} ({metric.definition_version})",
                            value=value, refs=value["source_refs"])
    rule_rows = []
    for rule in compliance.rules:
        handle = f"policy:{rule.policy_version}:{rule.rule_id}"
        # The rule's self-reference is not a transitive dependency.
        source_refs = [ref for ref in rule.source_refs if ref != handle]
        refs[handle] = dict(kind="POLICY", label=f"{rule.rule_id} ({rule.policy_version})",
                            value=primitive(asdict(rule)), refs=source_refs)
        rule_rows.append(dict(ref=handle, result=rule.outcome, state=rule.evaluation_state,
                              applicability=rule.applicability, workflow=rule.workflow,
                              authority=rule.authority, observed=rule.observed,
                              threshold=rule.threshold, predicate=rule.predicate,
                              calculation_ref=metric_handles.get(rule.calculation_ref)))
    for factor in risk.score.factors:
        refs[factor["assessment_id"]] = dict(kind="ASSESSMENT", label=factor["factor_id"] + " authored assessment",
                                            value=primitive(factor), refs=list(factor["refs"]))
    refs["panel:FINANCIAL"] = dict(kind="PANEL", label="Annual financial analysis", refs=list(metric_handles.values()))
    refs["panel:COMPLIANCE"] = dict(kind="PANEL", label="Fictional policy checks",
                                    refs=[row["ref"] for row in rule_rows])
    refs["panel:RISK"] = dict(kind="PANEL", label="Educational risk assessment",
                              refs=[f["assessment_id"] for f in risk.score.factors])
    if general and not refs['panel:RISK']['refs']:
        refs['panel:RISK']['refs']=[b.block_id for b in case.inventory]
    request = dict(wire_version="SYN-WIRE-1.0", scope=asdict(case.scope),
                   review_basis=dict(review_as_of=case.registration.review_as_of,
                                     cutoff=case.registration.evidence_cutoff_at,
                                     source_profile=case.registration.source_profile_version,
                                     financial_assessment_basis=case.case_data["bases"]["FY-ASSESS"],
                                     transaction_basis=case.case_data["bases"]["TXN-1"]),
                   terms={name: item.model_dump() for name, item in case.wire.terms.__dict__.items()},
                   financial=dict(metrics=metrics, analysis_scope=financial.analysis_scope,
                                  ebitda_reconciliation=financial.reported_ebitda_reconciliation,
                                  covenant_status=financial.covenant_status),
                   compliance=dict(policy_version=compliance.policy_version, rules=rule_rows,
                                   exceptions=list(compliance.exception_rule_ids),
                                   completeness=compliance.completeness,
                                   pending_control="Confidence check awaits validated synthesis"),
                   risk=primitive(asdict(risk)), reference_dictionary=refs)
    packet = dict(version="E-N01-SYNTHESIS-1.0", package_digest=case.registration.package_digest,
                  case_dependency_digest=case.dependency_digest, request=primitive(request))
    packet["input_digest"] = fingerprint("E-N01-SYNTHESIS-INPUT-1.0", packet)
    return packet


def synthesis_task(root: Path, case: RegisteredFixtureCase, packet: dict) -> dict:
    if packet != prepare_synthesis(case):
        raise InputError("SYNTHESIS_PREREQUISITES_REQUIRED")
    current = packet["request"]
    # Provenance bodies remain in the local dictionary. The model reads the
    # recorded panels once, rather than repeated source/policy/metric copies.
    context = dict(scope=current["scope"], review_basis=current["review_basis"], terms=current["terms"],
                   financial=current["financial"], compliance=current["compliance"], risk=current["risk"],
                   references={key: {name: value[name] for name in ("kind", "label", "refs")}
                               for key, value in current["reference_dictionary"].items()})
    return dict(task="synthesizer", instruction=load_instruction(
        root, "synthesizer", case.registration.instruction_hashes["synthesizer"]),
        output_schema=SynthesisWire.model_json_schema(), context=context)


def validate_fixture_synthesis(root: Path, case: RegisteredFixtureCase, packet: dict,
                               scope: Scope, operation_id: str, *, variant: str = "default") -> dict:
    if packet != prepare_synthesis(case) or scope.deal_id != case.scope.deal_id or scope.input_revision != case.scope.revision:
        raise InputError("SYNTHESIS_CURRENT_INPUT_MISMATCH")
    if variant not in ("default", "review"):
        raise InputError("UNREGISTERED_SYNTHESIS_VARIANT")
    suffix = ("-correction" if case.registration.source_profile_version == "E-N01-CORRECTION-1.0" else "-reassessment" if case.scope.revision == 2 else "") + ("" if variant == "default" else "-review")
    config = SynthesisRegistration.model_validate(strict_json(
        (root / ("config/registrations/" + case.registration.scenario_id.lower() + suffix + "-synthesis.json")).read_bytes()))
    if config.variant != variant or config.scenario_id != case.registration.scenario_id:
        raise InputError("SYNTHESIS_VARIANT_BINDING_MISMATCH")
    if (config.case_dependency_digest != case.dependency_digest or config.package_digest != packet["package_digest"]
            or config.input_digest != packet["input_digest"]):
        raise InputError("SYNTHESIS_FIXTURE_BINDING_MISMATCH")
    pack = root / "fixtures/development" / case.registration.scenario_id.lower()
    raw = (pack / ("synthesis." + variant + ".json")).read_bytes()
    rubric_raw = (pack / ("synthesis.rubric.json" if variant == "default" else "synthesis.review.rubric.json")).read_bytes()
    if sha256(raw).hexdigest() != config.wire_sha256 or sha256(rubric_raw).hexdigest() != config.rubric_sha256:
        raise InputError("SYNTHESIS_FIXTURE_OR_RUBRIC_CHANGED")
    wire = parse_synthesis(raw)
    rubric = strict_json(rubric_raw)
    if fingerprint("E-N01-SYNTHESIS-WIRE", wire.model_dump()) != rubric["wire_content_digest"]:
        raise InputError("SYNTHESIS_RUBRIC_WIRE_MISMATCH")
    refs = packet["request"]["reference_dictionary"]
    targets = hydrate_narrative(wire, scope, operation_id, {key: scope for key in refs},
                               dict(input_digest=packet["input_digest"], case=case.dependency_digest))
    if {t.field_path: t.text_digest for t in targets} != rubric["narrative_text_digests"]:
        raise InputError("SYNTHESIS_NARRATIVE_RUBRIC_MISMATCH")
    def resolve(handle, ancestors=()):
        if handle not in refs or handle in ancestors:
            raise InputError("SYNTHESIS_REFERENCE_MISSING_OR_CYCLIC")
        for child in refs[handle]["refs"]:
            resolve(child, ancestors + (handle,))
    for target in targets:
        for handle in target.refs:
            resolve(handle)
    financial, _, risk = evaluate_panels(case)
    cfg = case.case_data["policy_config"]
    final_policy = evaluate_policy({m.metric_id: m for m in financial.metric_results}, case.wire.terms,
        config=PolicyConfig(cfg["secured_equipment"], cfg["kyc_fixture_required"], cfg["sanctions_fixture_required"], cfg["basis"]),
        dependency_digest=case.dependency_digest, metric_source_refs=dict(financial.metric_source_refs),
        material_financial_ready=True, synthesis_complete=True, confidence=wire.panel_decision.confidence)
    workflow = aggregate_workflow((final_policy.workflow, risk.score.workflow))
    expected_workflow = "ESCALATE" if case.registration.scenario_id in ("E-F03", "E-P01") else "CONTINUE" if variant == "default" else "REVIEW_REQUIRED"
    if workflow != expected_workflow or final_policy.completeness != "COMPLETE":
        raise InputError("NORMAL_FIXTURE_REVIEW_BRANCH_UNAVAILABLE")
    # This fixture-only exact-text/rubric check does not prove arbitrary semantics.
    effective = wire.panel_decision.model_copy(update={"escalate_to_human": workflow != "CONTINUE"})
    return dict(wire_json=wire_json(wire), wire_digest=fingerprint("E-N01-SYNTHESIS-WIRE", wire.model_dump()),
                input_digest=packet["input_digest"], case_dependency_digest=case.dependency_digest,
                targets=[primitive(t.model_dump()) for t in targets],
                evidence_status="FIXTURE_EXPECTATION_CHECKED_NOT_HUMAN_SUPPORTED",
                raw_escalate_to_human=wire.panel_decision.escalate_to_human,
                effective_wire_json=wire_json(SynthesisWire(**{**wire.model_dump(), "panel_decision": effective})),
                routing=dict(workflow=workflow, human_credit_review="Not required by configured demo rules",
                             human_disposition=None, final_policy=primitive(asdict(final_policy))),
                rubric_version=rubric["version"])
