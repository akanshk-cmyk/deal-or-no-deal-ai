"""FIN-REVIEW-1.0 scoped financial commands; illustrative records never accepted."""

from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid5
from hashlib import sha256
from typing import Annotated, Literal
from pydantic import Field, field_validator

from .context import InputError, fingerprint, primitive, unicode_scalar
from .contracts import Identifier, Scope, StrictModel, Text
from .decision_history import HistoryFilters
from .review import AcceptedReview, Actor, PendingReview, Requirement, accept_review, advance_handling, consume_own_receipt, review_action_availability
from .review_actions import ReviewActionCommand
from .storage import OperationConflict, RecordWrite, StaleRecord, Store
from .conditional_review import (is_conditional, supported_condition, decode_draft, apply_condition_event, condition_record)


def event_deal_snapshot(run):
    """Capture new event metadata from this exact run, never enrich old events."""
    terms = run["artifacts"]["extractor"]["payload"]["wire"]["terms"]
    return dict(borrower=terms["borrower"]["value"], amount=terms["requested_amount"]["value"],
                currency=terms["currency"]["value"], deal_type="Registered synthetic term loan")


def request_key(run_id):
    return "financial-review:" + run_id


def decode_request(data):
    return PendingReview(**{**data, "requirements": tuple(Requirement(**r) for r in data["requirements"])})


def prepare_request(scope, synthesis, evidence_digest):
    exceptions = synthesis["routing"]["final_policy"]["exception_rule_ids"]
    if not set(exceptions) <= {"SYN-ESC-001", "SYN-ESC-002", "SYN-ESC-004", "SYN-ESC-005"}:
        raise InputError("UNSUPPORTED_EXCEPTION_REVIEW_GATE")
    request = PendingReview(str(uuid5(UUID(scope.run_id), "financial-review")), scope.workspace_id,
        scope.deal_id, scope.thread_id, scope.input_revision,
        fingerprint("FINANCIAL_REVIEW_BASIS", dict(scope=scope.model_dump(), synthesis=synthesis, evidence=evidence_digest)),
        1, "NORMAL", (Requirement("REGISTERED_FIXTURE_EVIDENCE", True, evidence_digest, 1),)
        + tuple(Requirement("exception:" + rule, False, None, 1) for rule in exceptions)
        + ((Requirement("REGISTERED_CONDITION_REVIEW", False, None, 1),) if is_conditional(synthesis) else ()))
    return dict(kind="FINANCIAL_REVIEW", request=primitive(asdict(request)), scope=scope.model_dump(),
                status="AWAITING_DECISION", information_pending=False, event_ids=[],
                provenance="EXECUTED_FIXTURE_REVIEW", original_ai=synthesis["wire_json"])


def handling_references(rule):
    metric = "calc:DSCR" if rule["calculation_ref"] == "CALC-004" else "calc:" + rule["calculation_ref"]
    return sorted(set(rule["source_refs"] + [metric]))


def exception_receipt(event):
    """Bounded checkpoint receipt; full original snapshot stays in history once."""
    return {**{k: v for k, v in event.items() if k != "analysis_snapshot"},
            "event_snapshot_digest": fingerprint("EXCEPTION_EVENT_SNAPSHOT", event)}


def check_exception_event(event, scope, synthesis, basis):
    rules = synthesis["routing"]["final_policy"]["rules"]
    rule = next((r for r in rules if r["rule_id"] == event.get("rule_id")), None)
    if (event.get("scope") != scope or event.get("action") != "EXCEPTION_DISPOSITION"
        or event.get("reviewer_role") != "RiskManager" or event.get("handling") != ("ACCEPT_FOR_CONDITIONAL_REVIEW" if is_conditional(synthesis) else "RECOMMEND_REJECT")
        or event.get("analytical_basis") != basis or not event.get("comments", "").strip()
        or rule is None or rule["rule_id"] not in ("SYN-ESC-001", "SYN-ESC-002", "SYN-ESC-004", "SYN-ESC-005")
        or rule["outcome"] != "Exception" or rule["authority"] != "INTERNAL_SAMPLE_POLICY"
        or rule["evaluation_state"] != "EVALUATED" or event.get("issue_id") != rule["issue_id"]
        or event.get("evidence_refs") != handling_references(rule)
        or event.get("provenance") != "EXECUTED_FIXTURE_REVIEW"):
        raise InputError("EXCEPTION_HANDLING_EVIDENCE_MISMATCH")
    if is_conditional(synthesis) and event.get("registered_condition") != supported_condition(synthesis)[0]:
        raise InputError("REGISTERED_CONDITION_BINDING_REQUIRED")
    if "analysis_snapshot" in event and (event["analysis_snapshot"].get("ai") != synthesis
            or event["analysis_snapshot"].get("source_dependency") != synthesis["case_dependency_digest"]):
        raise InputError("EXCEPTION_ORIGINAL_SNAPSHOT_MISMATCH")
    return rule


def get_financial_review(store, actor, run):
    from .command_center import _scope
    _scope(actor, run["context"]["scope"])
    saved = store.get_record(request_key(run["context"]["scope"]["run_id"]))
    if saved is None:
        return None
    version, data = saved
    if data.get("kind") != "FINANCIAL_REVIEW" or data["scope"] != run["context"]["scope"]:
        raise InputError("FINANCIAL_REVIEW_SCOPE_MISMATCH")
    request = decode_request(data["request"])
    expected = prepare_request(Scope.model_validate(data["scope"]), run["artifacts"]["synthesizer"]["payload"],
                               run["artifacts"]["evidence_review"]["content_digest"])
    reconstructed = decode_request(expected["request"])
    handling = data.get("exception_handling", {})
    seen = {}
    draft = None
    for event_id in data["event_ids"]:
        saved_event = store.get_record("financial-review-event:" + event_id)
        if saved_event is None or saved_event[1]["scope"] != data["scope"]:
            raise InputError("FINANCIAL_REVIEW_EVENT_MISMATCH")
        event = saved_event[1]
        if event["action"] == "EXCEPTION_DISPOSITION":
            rule = check_exception_event(event, data["scope"], run["artifacts"]["synthesizer"]["payload"], reconstructed.analytical_basis_digest)
            if event.get("previous_gate_version") != reconstructed.gate_version or rule["rule_id"] in seen:
                raise InputError("EXCEPTION_HANDLING_GATE_MISMATCH")
            reconstructed = advance_handling(reconstructed, Requirement("exception:" + rule["rule_id"], True, event_id, 2),
                                            expected_gate_version=reconstructed.gate_version)
            seen[rule["rule_id"]] = event_id
        elif event["action"] in ("CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED"):
            reconstructed, draft = apply_condition_event(reconstructed, draft, event, data["scope"], run["artifacts"]["synthesizer"]["payload"])
    if handling != seen:
        raise InputError("EXCEPTION_HANDLING_RECEIPT_MISMATCH")
    if data.get("condition_draft") != (None if draft is None else primitive(asdict(draft))):
        raise InputError("CONDITION_DRAFT_RECEIPT_MISMATCH")
    frozen = primitive(asdict(reconstructed))
    if (data["original_ai"] != expected["original_ai"]
            or any(data["request"][key] != value for key, value in frozen.items()
                   if key not in ("state", "recorded_operation_id"))):
        raise InputError("FINANCIAL_REVIEW_ANALYTICAL_BASIS_CHANGED")
    actions = review_action_availability(request, actor, information_pending=data["information_pending"])
    conditional = is_conditional(run["artifacts"]["synthesizer"]["payload"])
    if conditional:
        actions["APPROVE"] = "REGISTERED_CONDITIONAL_PATH_ONLY"
        for action, decision in (("CONDITIONAL_APPROVE", "Conditional Approve"), ("REJECT", "Reject")):
            try:
                accept_review(request, actor, request.request_id, decision, expected_basis=request.analytical_basis_digest,
                              expected_gate_version=request.gate_version, draft=draft)
                actions[action] = "INFORMATION_REQUEST_OUTSTANDING" if data["information_pending"] else None
            except InputError as error:
                actions[action] = str(error)
    elif handling:
        actions["APPROVE"] = "EXCEPTION_HANDLING_RECOMMENDS_REJECT"
    if run["status"] not in ("WAITING_REVIEW", "WAITING_INFORMATION"):
        actions = {key: reason if key == "ADD_COMMENT" and run["status"] == "COMPLETED" else "RUN_NOT_WAITING"
                   for key, reason in actions.items()}
    from .readiness_service import require_approval, assess_current
    try:
        a=assess_current(store,run["context"],run["artifacts"])
        require_approval(store,run,a.version,a.assessment_digest)
    except (InputError,ValueError):
        for action in ("APPROVE","CONDITIONAL_APPROVE"):
            if action in actions and actions[action] is None:
                actions[action]="APPROVAL_READINESS_BLOCKED"
    events = []
    for event_id in data["event_ids"]:
        saved_event = store.get_record("financial-review-event:" + event_id)
        if saved_event is None or saved_event[1]["scope"] != data["scope"]:
            raise InputError("FINANCIAL_REVIEW_EVENT_MISMATCH")
        events.append(saved_event[1])
    if "human_record" in data and data["human_record"].get("exception_events", []) != [exception_receipt(e) for e in events if e["action"] == "EXCEPTION_DISPOSITION"]:
        raise InputError("FINAL_EXCEPTION_SNAPSHOT_MISMATCH")
    if "human_record" in data and conditional and data["human_record"].get("condition_events") != [exception_receipt(e) for e in events if e["action"] in ("CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED")]:
        raise InputError("FINAL_CONDITION_SNAPSHOT_MISMATCH")
    return dict(version=version, data=data, request=request, actions=actions, events=events)


def validate_human_record(human, scope):
    request = decode_request(human["request"])
    accepted = AcceptedReview(**{**human["accepted"], "condition_target_refs": tuple(human["accepted"]["condition_target_refs"])})
    if (request.workspace_id != scope.workspace_id or request.deal_id != scope.deal_id
            or request.thread_id != scope.thread_id or request.input_revision != scope.input_revision
            or human["event"]["scope"] != scope.model_dump()
            or human["event"]["operation_id"] != accepted.operation_id
            or human["event"]["decision"] != accepted.decision):
        raise InputError("FINANCIAL_HUMAN_RECORD_MISMATCH")
    consume_own_receipt(request, accepted)
    events = human.get("exception_events", [])
    required = {r.key: r.receipt_ref for r in request.requirements if r.key.startswith("exception:")}
    if len(events) != len(required) or human["event"]["reviewer_role"] != "AuthorizedApprover":
        raise InputError("FINAL_EXCEPTION_RECEIPTS_REQUIRED")
    for event in events:
        check_exception_event(event, scope.model_dump(), human["event"]["analysis_snapshot"]["ai"], request.analytical_basis_digest)
        conditional = is_conditional(human["event"]["analysis_snapshot"]["ai"])
        if required.get("exception:" + event["rule_id"]) != event["operation_id"] or accepted.decision not in (("Conditional Approve", "Reject") if conditional else ("Reject",)):
            raise InputError("FINAL_EXCEPTION_RECEIPT_MISMATCH")
    synthesis = human["event"]["analysis_snapshot"]["ai"]
    if is_conditional(synthesis):
        evidence = next(r.receipt_ref for r in request.requirements if r.key == "REGISTERED_FIXTURE_EVIDENCE")
        rebuilt = decode_request(prepare_request(scope, synthesis, evidence)["request"])
        for event in events:
            if event.get("previous_gate_version") != rebuilt.gate_version:
                raise InputError("FINAL_EXCEPTION_GATE_MISMATCH")
            rebuilt = advance_handling(rebuilt, Requirement("exception:" + event["rule_id"], True, event["operation_id"], 2), expected_gate_version=rebuilt.gate_version)
        draft = None
        for event in human.get("condition_events", []):
            rebuilt, draft = apply_condition_event(rebuilt, draft, event, scope.model_dump(), synthesis)
        if (draft is None or human.get("condition_draft") != primitive(asdict(draft))
            or primitive(asdict(rebuilt)) != primitive(asdict(replace(request, state="PENDING", recorded_operation_id=None)))):
            raise InputError("FINAL_CONDITION_RECEIPTS_REQUIRED")
        reproduced = accept_review(rebuilt, Actor("AuthorizedApprover", scope.workspace_id, frozenset({scope.deal_id}), frozenset({"NORMAL"})),
            accepted.operation_id, accepted.decision, expected_basis=rebuilt.analytical_basis_digest, expected_gate_version=rebuilt.gate_version, draft=draft)
        if reproduced != accepted:
            raise InputError("FINAL_CONDITION_ACCEPTANCE_MISMATCH")
    return accepted


class ExceptionHandlingCommand(StrictModel):
    operation_id: Identifier
    request_id: Identifier
    expected_version: Annotated[int, Field(ge=1)]
    expected_gate_version: Annotated[int, Field(ge=1)]
    expected_basis: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    rule_id: Literal["SYN-ESC-001", "SYN-ESC-002", "SYN-ESC-004", "SYN-ESC-005"]
    handling: Literal["RECOMMEND_REJECT", "ACCEPT_FOR_CONDITIONAL_REVIEW"]
    comments: Annotated[str, Field(min_length=1, max_length=4096)]
    evidence_refs: list[Text] = Field(min_length=1, max_length=32)

    @field_validator("comments")
    @classmethod
    def reason(cls, value):
        if not unicode_scalar(value).strip():
            raise ValueError("EXCEPTION_REASON_REQUIRED")
        return value


class ConditionActionCommand(StrictModel):
    operation_id: Identifier
    request_id: Identifier
    expected_version: Annotated[int, Field(ge=1)]
    expected_gate_version: Annotated[int, Field(ge=1)]
    expected_basis: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    action: Literal["CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED"]
    condition_text: Text
    comments: Annotated[str, Field(min_length=1, max_length=4096)]
    evidence_refs: list[Text] = Field(min_length=1, max_length=32)
    domain: Literal["FINANCIAL_RISK", "POLICY_CONTROL"] | None = None
    draft_digest: str | None = None


class FinancialActionCommand(ReviewActionCommand):
    action: Literal["ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION", "CONDITIONAL_APPROVE"]
    expected_readiness_version: int | None = None
    expected_readiness_digest: str | None = None


def record_exception_handling(root, actor, run_operation, command: ExceptionHandlingCommand):
    """One role-scoped handling receipt; no inference, graph resume or policy edit."""
    from .command_center import get_run, source_packet
    from .configuration import load_configuration
    command = ExceptionHandlingCommand.model_validate(command.model_dump())
    config = load_configuration(root)
    store = Store(config.database)
    run = get_run(store, actor, run_operation)
    panel = get_financial_review(store, actor, run)
    if panel is None or actor.persona != "RiskManager":
        raise InputError("RISK_MANAGER_EXCEPTION_PERMISSION_REQUIRED")
    digest = fingerprint("EXCEPTION_HANDLING_COMMAND", dict(command=command.model_dump(), actor=asdict(actor), run=run_operation))
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
        raise StaleRecord("STALE_OR_BLOCKED_EXCEPTION_HANDLING")
    requirement = next((r for r in request.requirements if r.key == "exception:" + command.rule_id), None)
    if requirement is None or requirement.satisfied:
        raise InputError("CURRENT_UNHANDLED_EXCEPTION_REQUIRED")
    packet = source_packet(config.workspace, run)
    synthesis = run["artifacts"]["synthesizer"]["payload"]
    if len(set(command.evidence_refs)) != len(command.evidence_refs):
        raise InputError("DISTINCT_EXCEPTION_EVIDENCE_REQUIRED")
    if not set(command.evidence_refs) <= set(packet["request"]["reference_dictionary"]):
        raise InputError("EXCEPTION_REFERENCE_OUT_OF_SCOPE")
    rule = next(r for r in synthesis["routing"]["final_policy"]["rules"] if r["rule_id"] == command.rule_id)
    event = dict(operation_id=command.operation_id, command_digest=digest, scope=data["scope"], run_operation=run_operation,
        previous_status=data["status"], new_status=data["status"], action="EXCEPTION_DISPOSITION", decision=None,
        comments=command.comments, requested_items=[], reviewer_name="Simulated RiskManager", reviewer_role="RiskManager",
        timestamp_utc=datetime.now(timezone.utc).isoformat(), provenance="EXECUTED_FIXTURE_REVIEW",
        rule_id=command.rule_id, issue_id=rule["issue_id"], handling=command.handling,
        evidence_refs=sorted(command.evidence_refs), analytical_basis=request.analytical_basis_digest,
        previous_gate_version=request.gate_version,
        analysis_snapshot=dict(deal=event_deal_snapshot(run), ai=synthesis,
            risk=run["artifacts"]["risk_quantifier"]["payload"], compliance=synthesis["routing"]["final_policy"],
            sources={k: v for k, v in packet["request"]["reference_dictionary"].items() if v["kind"] == "SOURCE"},
            source_dependency=run["context"]["case_dependency_digest"]))
    if is_conditional(synthesis):
        if run["context"]["scenario_id"] != "E-P01":
            raise InputError("REGISTERED_CONDITIONAL_CASE_REQUIRED")
        event["registered_condition"] = supported_condition(synthesis)[0]
    check_exception_event(event, data["scope"], synthesis, request.analytical_basis_digest)
    updated_request = advance_handling(request, Requirement(requirement.key, True, command.operation_id, requirement.record_version + 1),
                                       expected_gate_version=request.gate_version)
    updated = {**data, "request": primitive(asdict(updated_request)), "event_ids": data["event_ids"] + [command.operation_id],
               "exception_handling": {**data.get("exception_handling", {}), command.rule_id: command.operation_id}}
    try:
        receipt = store.admit(command.operation_id, data["scope"], {"action": "EXCEPTION_DISPOSITION", "digest": digest}, writes=(
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
            raise InputError("EXCEPTION_ADMISSION_REQUIRES_RECONCILIATION")
        return dict(event=prior[1], duplicate=True, admission_status=receipt.state)
    store.release(receipt, confirmed_idle=True)
    return dict(event=event, duplicate=False)


def record_financial_action(root: Path, actor: Actor, run_operation: str, command: ReviewActionCommand):
    """Receipt-first atomic decision. Only a new accepted receipt may dispatch."""
    from .command_center import get_run, source_packet
    from .configuration import load_configuration
    from .worker import run_normal_fixture
    command = FinancialActionCommand.model_validate(command.model_dump())
    config = load_configuration(root)
    store = Store(config.database)
    run = get_run(store, actor, run_operation)
    panel = get_financial_review(store, actor, run)
    if panel is None:
        raise InputError("FINANCIAL_REVIEW_UNAVAILABLE")
    payload_digest = fingerprint("FINANCIAL_REVIEW_COMMAND", dict(command=command.model_dump(), actor=asdict(actor), run=run_operation))
    event_key = "financial-review-event:" + command.operation_id
    prior = store.get_record(event_key)
    if prior:
        if prior[1]["command_digest"] != payload_digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return dict(event=prior[1], duplicate=True, outcome=run["outcome"])
    if command.expected_version != panel["version"]:
        raise StaleRecord("STALE_FINANCIAL_REVIEW")
    request, data = panel["request"], panel["data"]
    if (command.request_id != request.request_id or command.expected_basis != request.analytical_basis_digest
            or command.expected_gate_version != request.gate_version):
        raise InputError("STALE_FINANCIAL_REVIEW_BASIS")
    reason = panel["actions"].get(command.action, "ACTION_UNAVAILABLE_FOR_CASE")
    if reason is not None:
        raise InputError(reason)
    readiness_preconditions=()
    from .readiness_service import require_approval, assess_current, key as readiness_key
    if command.action in ("APPROVE","CONDITIONAL_APPROVE"):
        if command.expected_readiness_version is None or command.expected_readiness_digest is None:
            raise InputError("LATEST_READINESS_VERSION_REQUIRED")
        current_readiness=require_approval(store,run,command.expected_readiness_version,command.expected_readiness_digest)
        readiness_preconditions=((readiness_key(run["context"]["scope"]["run_id"]),current_readiness[0]),)
    readiness_snapshot=assess_current(store,run["context"],run["artifacts"]).model_dump()
    # Refuse stale/changed source packages before recording a disposition.
    packet = source_packet(config.workspace, run)
    stamp = datetime.now(timezone.utc).isoformat()
    final = command.action in ("APPROVE", "REJECT", "CONDITIONAL_APPROVE")
    decision = {"APPROVE": "Approve", "REJECT": "Reject", "CONDITIONAL_APPROVE": "Conditional Approve"}.get(command.action)
    updated = dict(data)
    if final:
        accepted = accept_review(request, actor, command.operation_id, decision,
                                expected_basis=command.expected_basis, expected_gate_version=command.expected_gate_version,
                                draft=decode_draft(data.get("condition_draft")))
        updated.update(request=primitive(asdict(replace(request, state="RECORDED", recorded_operation_id=command.operation_id))),
                       status={"Approve": "APPROVED", "Reject": "REJECTED", "Conditional Approve": "CONDITIONALLY_APPROVED"}[decision])
    elif command.action == "REQUEST_INFORMATION":
        updated.update(status="PENDING_INFORMATION", information_pending=True)
    event = dict(operation_id=command.operation_id, command_digest=payload_digest, scope=data["scope"],
                 run_operation=run_operation, previous_status=data["status"], new_status=updated["status"],
                 action=command.action, decision=decision, comments=command.comments,
                 approval_readiness=readiness_snapshot,ai_proposal=run.get("ai_proposal"),human_decision=decision,
                 requested_items=command.requested_items, reviewer_name="Simulated " + actor.persona,
                 reviewer_role=actor.persona, timestamp_utc=stamp, provenance="EXECUTED_FIXTURE_REVIEW",
                 analysis_snapshot=dict(deal=event_deal_snapshot(run), ai=run["artifacts"]["synthesizer"]["payload"],
                                        risk=run["artifacts"]["risk_quantifier"]["payload"],
                                        compliance=run["artifacts"]["synthesizer"]["payload"]["routing"]["final_policy"],
                                        sources={key: value for key, value in packet["request"]["reference_dictionary"].items()
                                                 if value["kind"] == "SOURCE"},
                                        source_dependency=run["context"]["case_dependency_digest"]))
    updated["event_ids"] = data["event_ids"] + [command.operation_id]
    if final:
        updated["human_record"] = dict(request=updated["request"], accepted=primitive(asdict(accepted)), event=event,
            **({"exception_events": [exception_receipt(e) for e in panel["events"] if e["action"] == "EXCEPTION_DISPOSITION"]} if data.get("exception_handling") else {}))
        if data.get("condition_draft"):
            updated["human_record"].update(condition_draft=data["condition_draft"], condition_events=[exception_receipt(e) for e in panel["events"] if e["action"] in ("CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED")])
            event["condition_record"] = condition_record(data["scope"], run["artifacts"]["synthesizer"]["payload"], decode_draft(data["condition_draft"]))
    result_key = "normal-result:" + run_operation
    outcome_version, outcome = store.get_record(result_key)
    new_outcome = {**outcome, "status": "REVIEW_RECORDED" if final else outcome["status"] if command.action == "ADD_COMMENT"
                   else "WAITING_INFORMATION" if updated["information_pending"] else "WAITING_REVIEW"}
    if final:
        new_outcome["human_disposition"] = decision
    try:
        receipt = store.admit(command.operation_id, data["scope"], {"action": "FINANCIAL_" + command.action, "digest": payload_digest},
            writes=(RecordWrite(request_key(data["scope"]["run_id"]), "FINANCIAL_REVIEW", updated, panel["version"]),
                    RecordWrite(event_key, "FINANCIAL_REVIEW_EVENT", event),
                    RecordWrite(result_key, "NORMAL_FIXTURE_OUTCOME", new_outcome, outcome_version)),expected_records=readiness_preconditions)
    except OperationConflict:
        concurrent = store.get_record(event_key)
        if concurrent is None or concurrent[1]["command_digest"] != payload_digest:
            raise
        return dict(event=concurrent[1], duplicate=True, outcome=get_run(store, actor, run_operation)["outcome"])
    if receipt.duplicate:
        raise InputError("FINANCIAL_ADMISSION_REQUIRES_RECONCILIATION")
    if not final:
        store.release(receipt, confirmed_idle=True)
        return dict(event=event, duplicate=False, outcome=new_outcome)
    try:
        outcome = run_normal_fixture(config.workspace, run_operation, variant="review", scenario_id=run["context"]["scenario_id"],
                                     _resume=dict(receipt=receipt, human_record=updated["human_record"]))
    except BaseException:
        # Original command/decision is retained; never replay it automatically.
        with store.connection() as connection:
            state = connection.execute("SELECT state FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()[0]
        if state == "HELD":
            store.mark_unknown(receipt)
        raise
    return dict(event=event, duplicate=False, outcome=outcome)


class InformationResponseCommand(StrictModel):
    operation_id: str
    expected_version: Annotated[int, Field(gt=0)]
    expected_basis: str
    comments: Annotated[str, Field(min_length=1, max_length=4096)]
    reference_by_item: Annotated[list[str], Field(min_length=1, max_length=100)]

    @field_validator("comments")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("RESPONSE_ASSESSMENT_REQUIRED")
        return value


def respond_and_reassess(root: Path, actor: Actor, run_operation: str,
                         command: InformationResponseCommand, document: bytes):
    """Explicit bounded response: exact registered source, no new financial facts."""
    from .budgets import Ledger, Usage
    from .command_center import get_run, source_packet
    from .configuration import load_configuration
    from .worker import run_normal_fixture
    command = InformationResponseCommand.model_validate(command.model_dump())
    if str(UUID(command.operation_id)) != command.operation_id:
        raise InputError("CANONICAL_OPERATION_UUID_REQUIRED")
    if type(document) is not bytes or not document or len(document) > 10485760:
        raise InputError("BOUNDED_REGISTERED_PDF_REQUIRED")
    config = load_configuration(root)
    store = Store(config.database)
    run = get_run(store, actor, run_operation)
    if run["context"]["scenario_id"] != "E-N01":
        raise InputError("SCENARIO_INFORMATION_CONTINUATION_UNAVAILABLE")
    panel = get_financial_review(store, actor, run)
    if actor.persona != "RiskManager" or panel is None:
        raise InputError("RISK_MANAGER_RESPONSE_ASSESSMENT_REQUIRED")
    digest = fingerprint("FINANCIAL_RESPONSE_COMMAND", dict(command=command.model_dump(), actor=asdict(actor),
                         run=run_operation, document_sha256=sha256(document).hexdigest()))
    event_key = "financial-review-event:" + command.operation_id
    prior = store.get_record(event_key)
    if prior:
        if prior[1]["command_digest"] != digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return dict(event=prior[1], duplicate=True, outcome=store.get_record("normal-result:" + command.operation_id)[1])
    if (run["status"] != "WAITING_INFORMATION" or not panel["data"]["information_pending"]
            or panel["request"].state != "PENDING"):
        raise InputError("CURRENT_INFORMATION_REQUEST_REQUIRED")
    if command.expected_version != panel["version"] or command.expected_basis != panel["request"].analytical_basis_digest:
        raise StaleRecord("STALE_INFORMATION_RESPONSE")
    packet = source_packet(config.workspace, run)
    refs = packet["request"]["reference_dictionary"]
    supported = {key for key, ref in refs.items() if ref["kind"] == "SOURCE"
                 and ref["source_sha256"] == sha256(document).hexdigest()}
    items = [item for e in panel["events"] if e["action"] == "REQUEST_INFORMATION" for item in e["requested_items"]]
    if not supported or len(command.reference_by_item) != len(items) or not set(command.reference_by_item) <= supported:
        raise InputError("REGISTERED_DOCUMENT_AND_ALL_REQUEST_ITEM_REFERENCES_REQUIRED")
    ledger_key = "ledger:" + run["context"]["scope"]["review_id"]
    ledger_version, ledger_data = store.get_record(ledger_key)
    ledger = Ledger.from_dict(ledger_data)
    if ledger.correction_used:
        raise InputError("REGISTERED_CORRECTION_ALLOWANCE_ALREADY_USED")
    # Charge the logical interrupted node, excluding human wait; retire its unused timeout.
    ledger = ledger.settle(run_operation + ":human_review", Usage(nodes=1, active_ms=1))
    ledger = replace(ledger, correction_used=True)
    ledger.require_path("FINANCIAL_CORRECTION_REVIEWED", fixture=True)
    stamp = datetime.now(timezone.utc).isoformat()
    event = dict(operation_id=command.operation_id, command_digest=digest, scope=panel["data"]["scope"],
        run_operation=run_operation, previous_status="PENDING_INFORMATION", new_status="SUPERSEDED_BY_REASSESSMENT",
        action="INFORMATION_RESPONSE", decision=None, comments=command.comments, requested_items=items,
        reviewer_name="Simulated RiskManager", reviewer_role="RiskManager", timestamp_utc=stamp,
        provenance="EXECUTED_FIXTURE_REVIEW", response_source_sha256=sha256(document).hexdigest(),
        reference_by_item=command.reference_by_item, analysis_snapshot=dict(deal=event_deal_snapshot(run), source_dependency=run["context"]["case_dependency_digest"],
            limitation="RiskManager assessment of unchanged registered evidence; not acceptance of new financial values."),
        reassessment_operation=command.operation_id)
    data = panel["data"]
    stale = {**data, "request": primitive(asdict(replace(panel["request"], state="STALE"))),
             "status": "SUPERSEDED_BY_REASSESSMENT", "information_pending": False,
             "event_ids": data["event_ids"] + [command.operation_id], "reassessment_operation": command.operation_id}
    outcome_version, outcome = store.get_record("normal-result:" + run_operation)
    writes = (RecordWrite(request_key(data["scope"]["run_id"]), "FINANCIAL_REVIEW", stale, panel["version"]),
              RecordWrite(event_key, "FINANCIAL_REVIEW_EVENT", event),
              RecordWrite("normal-result:" + run_operation, "NORMAL_FIXTURE_OUTCOME",
                          {**outcome, "status": "SUPERSEDED", "reassessment_operation": command.operation_id}, outcome_version))
    try:
        result = run_normal_fixture(config.workspace, command.operation_id, variant="review",
                 _continuation=dict(parent=run, ledger=ledger.to_dict(), ledger_version=ledger_version, writes=writes))
    except OperationConflict:
        concurrent = store.get_record(event_key)
        if concurrent is None or concurrent[1]["command_digest"] != digest:
            raise
        return dict(event=concurrent[1], duplicate=True, outcome=store.get_record("normal-result:" + command.operation_id)[1])
    return dict(event=event, duplicate=False, outcome=result)


def financial_history(store: Store, actor: Actor, deal_id: str | None = None):
    """Read frozen event-time data in one SQLite snapshot; never latest analysis."""
    from .command_center import ROLES
    from .context import strict_json
    if actor.persona not in ROLES or actor.attribution != "SIMULATED" or (deal_id is not None and deal_id not in actor.allowed_deal_ids):
        raise InputError("FINANCIAL_HISTORY_OUT_OF_SCOPE")
    if not store.path.exists():
        return []
    with store.connection() as connection:
        connection.execute("BEGIN")
        events = []
        for row in connection.execute("SELECT record_key,payload FROM app_records WHERE kind='FINANCIAL_REVIEW_EVENT'"):
            event = strict_json(row["payload"], envelope=True)
            scope = event["scope"]
            if (scope["workspace_id"] != actor.workspace_id or scope["deal_id"] not in actor.allowed_deal_ids
                    or deal_id is not None and scope["deal_id"] != deal_id):
                continue
            if row["record_key"] != "financial-review-event:" + event["operation_id"] or event["provenance"] not in ("EXECUTED_FIXTURE_REVIEW","LIVE_ANALYSIS_HUMAN_REVIEW"):
                raise InputError("FINANCIAL_HISTORY_EVENT_MISMATCH")
            if event['provenance']=='LIVE_ANALYSIS_HUMAN_REVIEW':
                context=connection.execute('SELECT payload FROM app_records WHERE record_key=?',('live-context:'+event['run_operation'],)).fetchone()
                if not context or strict_json(context[0])['scope']!=scope or not strict_json(context[0]).get('upload_origin'):
                    raise InputError('LIVE_FINANCIAL_HISTORY_SCOPE_MISMATCH')
            events.append(event)
            if len(events) > 5000:
                raise InputError("FINANCIAL_HISTORY_LIMIT")
        return sorted(events, key=lambda e: (e["timestamp_utc"], e["operation_id"]))


def financial_history_csv(store, actor, deal_id, *, expected_digest, filters=None):
    import csv
    import io
    import json
    from .decision_history import _csv_cell
    events = financial_history(store, actor, deal_id)
    if filters is not None:
        events = filter_financial_events(events, filters)
    if fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events) != expected_digest:
        raise StaleRecord("FINANCIAL_HISTORY_CHANGED")
    output = io.StringIO(newline="")
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["event_id", "deal_id", "run_id", "revision", "time_utc", "action", "previous_status", "new_status",
                     "reviewer", "role", "comments", "requested_items", "analysis_snapshot", "provenance",
                     "exception_handling", "rule_id", "issue_id", "evidence_refs", "previous_gate_version", "condition_record", "condition_text", "support_domain", "corrected_field", "old_fact", "corrected_fact", "ai_proposal", "approval_readiness", "human_decision"])
    for event in events:
        values = [event["operation_id"], event["scope"]["deal_id"], event["scope"]["run_id"], str(event["scope"]["input_revision"]),
                  event["timestamp_utc"], event["action"], event["previous_status"], event["new_status"],
                  event["reviewer_name"], event["reviewer_role"], event["comments"], json.dumps(event["requested_items"]),
                  json.dumps(event["analysis_snapshot"], ensure_ascii=False), "EXECUTED_FIXTURE_REVIEW / SIMULATED_IDENTITY",
                  event.get("handling", "Not applicable"), event.get("rule_id", "Not applicable"), event.get("issue_id", "Not applicable"),
                  json.dumps(event.get("evidence_refs", [])), str(event.get("previous_gate_version", "Not applicable")), json.dumps(event.get("condition_record")), event.get("condition_text", ""), event.get("domain") or "",
                  event.get("field", ""), json.dumps(event.get("old_fact")), json.dumps(event.get("corrected_fact")), json.dumps(event.get("ai_proposal")), json.dumps(event.get("approval_readiness")), json.dumps(event.get("human_decision",event.get("decision")))]
        writer.writerow([_csv_cell(value) for value in values])
    return output.getvalue().encode("utf-8-sig")


class FinancialHistoryFilters(HistoryFilters):
    actions: list[Literal["ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION", "INFORMATION_RESPONSE", "EXCEPTION_DISPOSITION", "CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED", "CONDITIONAL_APPROVE", "SOURCE_CORRECTION_SAVED", "CORRECTION_APPLIED"]] = Field(default_factory=list, max_length=11)
    statuses: list[Literal["AWAITING_DECISION", "PENDING_INFORMATION", "APPROVED", "REJECTED", "SUPERSEDED_BY_REASSESSMENT", "CONDITIONALLY_APPROVED", "READY", "SUPERSEDED_BY_CORRECTION", "UPDATED_FINDINGS_REQUESTED"]] = Field(default_factory=list, max_length=9)


def filter_financial_events(events, filters):
    """Filter frozen authorized records only; no latest-data backfill."""
    filters = FinancialHistoryFilters.model_validate(filters.model_dump())
    result = []
    for event in events:
        stamp = datetime.fromisoformat(event["timestamp_utc"].replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise InputError("FINANCIAL_HISTORY_TIMESTAMP_UNAVAILABLE")
        day = stamp.astimezone(timezone.utc).date()
        deal = event["analysis_snapshot"].get("deal", {})
        if (filters.deal_id.casefold() not in event["scope"]["deal_id"].casefold()
            or filters.borrower.casefold() not in (deal.get("borrower") or "").casefold()
            or filters.reviewer.casefold() not in (event["reviewer_name"] + " " + event["reviewer_role"]).casefold()
            or filters.actions and event["action"] not in filters.actions
            or filters.statuses and event["new_status"] not in filters.statuses
            or filters.start_date and day < filters.start_date
            or filters.end_date and day > filters.end_date):
            continue
        result.append(event)
    return sorted(result, key=lambda e: (e["timestamp_utc"], e["operation_id"]), reverse=filters.newest_first)


def query_financial_history(store, actor, filters, *, offset=0, limit=25):
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100:
        raise InputError("INVALID_FINANCIAL_HISTORY_PAGE")
    events = filter_financial_events(financial_history(store, actor), filters)
    return dict(total=len(events), rows=events[offset:offset + limit],
                snapshot_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))
