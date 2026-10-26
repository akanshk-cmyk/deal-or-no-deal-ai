"""Bounded E-P01 condition preparation/support; no inference or policy waiver."""
from dataclasses import asdict
from datetime import datetime, timezone

from .context import InputError, fingerprint, primitive
from .contracts import parse_synthesis
from .review import (Actor, ConditionDraft, DraftTarget, Requirement, advance_handling,
                     prepare_review_conditions, support_draft)
from .storage import OperationConflict, RecordWrite, StaleRecord, Store

CONDITION = "Supply annual financial statements"
DOMAINS = {"FINANCIAL_RISK": "RiskManager", "POLICY_CONTROL": "ComplianceOfficer"}


def is_conditional(synthesis):
    wire = parse_synthesis(synthesis["wire_json"])
    return wire.panel_decision.decision == "Conditional Approve"


def supported_condition(synthesis):
    wire = parse_synthesis(synthesis["wire_json"])
    if (wire.panel_decision.decision != "Conditional Approve" or wire.panel_decision.conditions != [CONDITION]
        or [c.model_dump() for c in wire.condition_links] != [dict(index=0, refs=["E-P01:AGREEMENT-P1"]) ]
        or synthesis["routing"]["final_policy"]["exception_rule_ids"] != ["SYN-ESC-001"]):
        raise InputError("REGISTERED_CONDITION_REQUIRED")
    return CONDITION, ["E-P01:AGREEMENT-P1", "E-P01:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"]


def decode_draft(data):
    if data is None:
        return None
    return ConditionDraft(**{**data, "conditions": tuple(data["conditions"]), "targets": tuple(
        DraftTarget(**{**t, "refs": tuple(t["refs"]), "domains": frozenset(t["domains"])}) for t in data["targets"])})


def apply_condition_event(request, draft, event, scope, synthesis):
    text, refs = supported_condition(synthesis)
    if (event.get("scope") != scope or event.get("analytical_basis") != request.analytical_basis_digest
        or event.get("previous_gate_version") != request.gate_version or not event.get("comments", "").strip()
        or event.get("condition_text") != text or event.get("evidence_refs") != sorted(refs)
        or event.get("provenance") != "EXECUTED_FIXTURE_REVIEW"):
        raise InputError("CONDITION_EVENT_EVIDENCE_MISMATCH")
    if "analysis_snapshot" in event and (event["analysis_snapshot"].get("ai") != synthesis
            or event["analysis_snapshot"].get("source_dependency") != synthesis["case_dependency_digest"]):
        raise InputError("CONDITION_EVENT_SNAPSHOT_MISMATCH")
    actor = Actor(event["reviewer_role"], request.workspace_id, frozenset({request.deal_id}), frozenset({"NORMAL"}))
    if event["action"] == "CONDITION_DRAFT_PREPARED":
        if event.get("domain") is not None or event.get("draft_digest") is not None:
            raise InputError("UNPREPARED_CONDITION_DRAFT_REQUIRED")
        if draft is not None or any(not r.satisfied for r in request.requirements if r.key.startswith("exception:")):
            raise InputError("CONDITION_PREPARATION_ORDER_REQUIRED")
        request, draft = prepare_review_conditions(request, actor, event["operation_id"], (text,), (tuple(refs),),
            (frozenset(DOMAINS),), frozenset(refs), expected_basis=request.analytical_basis_digest,
            expected_gate_version=request.gate_version)
        request = advance_handling(request, Requirement("REGISTERED_CONDITION_REVIEW", True, event["operation_id"], 2),
                                   expected_gate_version=request.gate_version)
    elif event["action"] == "CONDITION_SUPPORTED":
        domain = event.get("domain")
        if draft is None or domain not in DOMAINS or event.get("draft_digest") != draft.content_digest:
            raise InputError("CURRENT_CONDITION_DRAFT_REQUIRED")
        key = "draft:" + draft.targets[0].target_id + ":" + domain
        if next(r for r in request.requirements if r.key == key).satisfied:
            raise InputError("CONDITION_ALREADY_SUPPORTED")
        request = support_draft(request, draft, actor, draft.targets[0].target_id, domain, tuple(refs),
                                event["operation_id"], expected_gate_version=request.gate_version)
    else:
        raise InputError("UNKNOWN_CONDITION_ACTION")
    return request, draft


def condition_record(scope, synthesis, draft=None):
    text, refs = supported_condition(synthesis)
    return dict(condition_id=fingerprint("REGISTERED_CONDITION", dict(scope=scope, synthesis=synthesis["wire_digest"], index=0)),
        text=text, origin="MODEL_PROPOSAL", source_origin="SOURCE_COVENANT", category="PROPOSED_REVIEW_CONDITION",
        refs=refs, source_covenant_status="EXTRACTED_NOT_EVALUATED", status="OUTSTANDING", owner="Unassigned",
        blocks_completion=False, source_covenant_record_state="RECORDED",
        parent_synthesis=synthesis["wire_digest"], condition_index=0,
        issue_id=next(r["issue_id"] for r in synthesis["routing"]["final_policy"]["rules"] if r["rule_id"] == "SYN-ESC-001"),
        draft_id=None if draft is None else draft.draft_id,
        limitation="Annual statements do not cure DSCR. Review completion does not authorize funding or fulfil this condition.")


def record_condition_action(root, actor, run_operation, command):
    from .financial_review import (ConditionActionCommand, event_deal_snapshot, get_financial_review, request_key)
    from .command_center import get_run, source_packet
    from .configuration import load_configuration
    command = ConditionActionCommand.model_validate(command.model_dump())
    config = load_configuration(root); store = Store(config.database)
    run = get_run(store, actor, run_operation)
    if run["context"]["scenario_id"] != "E-P01":
        raise InputError("REGISTERED_CONDITIONAL_CASE_REQUIRED")
    panel = get_financial_review(store, actor, run)
    if panel is None:
        raise InputError("CURRENT_CONDITION_REVIEW_REQUIRED")
    expected_role = "AuthorizedApprover" if command.action == "CONDITION_DRAFT_PREPARED" else DOMAINS.get(command.domain)
    if actor.persona != expected_role or expected_role == "AuthorizedApprover" and "NORMAL" not in actor.allowed_review_tiers:
        raise InputError("CONDITION_ROLE_REQUIRED")
    digest = fingerprint("CONDITION_COMMAND", dict(command=command.model_dump(), actor=asdict(actor), run=run_operation))
    key = "financial-review-event:" + command.operation_id
    prior = store.get_record(key)
    if prior:
        if prior[1]["command_digest"] != digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return dict(event=prior[1], duplicate=True)
    request, data = panel["request"], panel["data"]
    if (run["status"] != "WAITING_REVIEW" or request.state != "PENDING" or data["information_pending"]
        or command.request_id != request.request_id or command.expected_version != panel["version"]
        or command.expected_gate_version != request.gate_version or command.expected_basis != request.analytical_basis_digest):
        raise StaleRecord("STALE_OR_BLOCKED_CONDITION_ACTION")
    packet = source_packet(config.workspace, run)
    synthesis = run["artifacts"]["synthesizer"]["payload"]
    text, refs = supported_condition(synthesis)
    if text not in packet["request"]["terms"]["covenants"]["value"] or not set(refs) <= set(packet["request"]["reference_dictionary"]):
        raise InputError("SOURCE_COVENANT_REQUIRED")
    event = dict(operation_id=command.operation_id, command_digest=digest, scope=data["scope"], run_operation=run_operation,
        previous_status=data["status"], new_status=data["status"], action=command.action, decision=None,
        comments=command.comments, requested_items=[], reviewer_name="Simulated " + actor.persona, reviewer_role=actor.persona,
        timestamp_utc=datetime.now(timezone.utc).isoformat(), provenance="EXECUTED_FIXTURE_REVIEW",
        condition_text=command.condition_text, evidence_refs=sorted(command.evidence_refs), domain=command.domain,
        draft_digest=command.draft_digest, analytical_basis=request.analytical_basis_digest, previous_gate_version=request.gate_version,
        analysis_snapshot=dict(deal=event_deal_snapshot(run), ai=synthesis, risk=run["artifacts"]["risk_quantifier"]["payload"],
            compliance=synthesis["routing"]["final_policy"], source_dependency=run["context"]["case_dependency_digest"],
            sources={k: v for k, v in packet["request"]["reference_dictionary"].items() if v["kind"] == "SOURCE"}))
    updated_request, draft = apply_condition_event(request, decode_draft(data.get("condition_draft")), event, data["scope"], synthesis)
    updated = {**data, "request": primitive(asdict(updated_request)), "condition_draft": primitive(asdict(draft)),
               "event_ids": data["event_ids"] + [command.operation_id]}
    try:
        receipt = store.admit(command.operation_id, data["scope"], {"action": command.action, "digest": digest}, writes=(
            RecordWrite(request_key(data["scope"]["run_id"]), "FINANCIAL_REVIEW", updated, panel["version"]),
            RecordWrite(key, "FINANCIAL_REVIEW_EVENT", event)))
    except OperationConflict:
        prior = store.get_record(key)
        if prior is None or prior[1]["command_digest"] != digest:
            raise
        return dict(event=prior[1], duplicate=True)
    if receipt.duplicate:
        prior = store.get_record(key)
        if prior is None or prior[1]["command_digest"] != digest:
            raise InputError("CONDITION_ADMISSION_REQUIRES_RECONCILIATION")
        return dict(event=prior[1], duplicate=True)
    store.release(receipt, confirmed_idle=True)
    return dict(event=event, duplicate=False)
