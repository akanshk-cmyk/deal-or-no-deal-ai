"""CORRECTION-1.0: one source-backed missing-CFADS repair, explicit Save/Update."""
from dataclasses import asdict, replace
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID, uuid5
from pydantic import Field

from .budgets import Ledger
from .context import InputError, fingerprint
from .contracts import Identifier, Scope, StrictModel, Text
from .storage import OperationConflict, RecordWrite, StaleRecord, Store

FIELD = "cash_available_for_debt_service"


class SaveCorrectionCommand(StrictModel):
    operation_id: Identifier
    expected_version: Annotated[int, Field(ge=1)]
    expected_basis: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    field: Literal["cash_available_for_debt_service"]
    value: Text
    basis_id: Text
    evidence_ref: Text
    comments: Annotated[str, Field(min_length=1, max_length=4096)]


class UpdateCorrectionCommand(StrictModel):
    expected_version: Annotated[int, Field(ge=1)]
    expected_basis: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]


def correction_basis(run):
    return fingerprint("SOURCE_CORRECTION_BASIS", dict(scope=run["context"]["scope"],
        case=run["context"]["case_dependency_digest"], extractor=run["artifacts"]["extractor"]["content_digest"]))


def draft_basis(draft):
    return fingerprint("SAVED_CORRECTION_BASIS", dict(context=draft["context"], event_id=draft["event_id"],
        original_basis=draft["original_basis"], command_digest=draft["command_digest"]))


def validate_saved_correction(root, store, parent, context, draft):
    """Rebuild from original event and exact registrations; no trusted clearance flag."""
    from .services import load_registered_case
    from .command_center import source_packet
    source_packet(root, parent)
    old = load_registered_case(root, profile="extraction-miss")
    new = load_registered_case(root, profile="correction")
    event = store.get_record("financial-review-event:" + draft["event_id"])
    if event is None:
        raise InputError("CORRECTION_EVENT_REQUIRED")
    event = event[1]
    expected_scope = {**parent["context"]["scope"], "input_revision": 2,
        "run_id": str(uuid5(UUID(context["operation_id"]), "run")),
        "thread_id": str(uuid5(UUID(context["operation_id"]), "thread"))}
    if (parent["context"].get("profile") != "extraction-miss" or parent["status"] != "SUPERSEDED"
        or draft["context"] != context or context["scope"] != expected_scope
        or context["variant"] != "default" or context.get("profile") != "correction"
        or context.get("parent_operation") != parent["operation_id"]
        or context.get("correction_event_id") != draft["event_id"]
        or context["case_dependency_digest"] != new.dependency_digest
        or parent["context"]["case_dependency_digest"] != old.dependency_digest
        or draft["original_basis"] != correction_basis(parent)
        or event.get("action") != "SOURCE_CORRECTION_SAVED" or event.get("reviewer_role") != "Analyst"
        or event.get("scope") != parent["context"]["scope"] or not event.get("comments", "").strip()
        or event.get("provenance") != "EXECUTED_FIXTURE_REVIEW"
        or event.get("new_operation") != context["operation_id"]
        or event.get("original_basis") != draft["original_basis"]
        or event.get("command_digest") != draft["command_digest"]
        or event.get("field") != FIELD or event.get("old_fact") != old.wire.financial_inputs.cash_available_for_debt_service.model_dump()
        or event.get("corrected_fact") != new.wire.financial_inputs.cash_available_for_debt_service.model_dump()
        or event.get("evidence_refs") != new.wire.financial_inputs.cash_available_for_debt_service.refs
        or event.get("analysis_snapshot", {}).get("original_extraction") != parent["artifacts"]["extractor"]["payload"]["wire"]
        or parent["artifacts"]["extractor"]["payload"]["wire"] != old.wire.model_dump()
        or parent["outcome"].get("correction_operation") != context["operation_id"]):
        raise InputError("SAVED_CORRECTION_BINDING_MISMATCH")
    stamp = datetime.fromisoformat(event["timestamp_utc"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise InputError("CORRECTION_UTC_TIME_REQUIRED")
    before, after = old.wire.model_dump(), new.wire.model_dump()
    before["financial_inputs"].pop(FIELD); after["financial_inputs"].pop(FIELD)
    if before != after or old.registration.package_digest != new.registration.package_digest:
        raise InputError("CORRECTION_CHANGED_UNAPPROVED_FACTS")
    from .synthesis import prepare_synthesis
    if context["synthesis_input_digest"] != prepare_synthesis(new)["input_digest"]:
        raise InputError("CORRECTION_SYNTHESIS_BINDING_MISMATCH")
    return event


def save_source_correction(root, actor, parent_operation, command):
    from .command_center import get_run, source_packet
    from .configuration import load_configuration
    from .financial_review import event_deal_snapshot
    from .services import load_registered_case
    from .synthesis import prepare_synthesis
    command = SaveCorrectionCommand.model_validate(command.model_dump())
    config = load_configuration(root); store = Store(config.database)
    parent = get_run(store, actor, parent_operation)
    if actor.persona != "Analyst" or parent["context"].get("profile") != "extraction-miss":
        raise InputError("ANALYST_EXTRACTION_MISS_CORRECTION_REQUIRED")
    digest = fingerprint("SAVE_SOURCE_CORRECTION", dict(command=command.model_dump(), actor=asdict(actor), parent=parent_operation))
    event_key = "financial-review-event:" + command.operation_id
    prior = store.get_record(event_key)
    if prior:
        if prior[1]["command_digest"] != digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return dict(event=prior[1], operation_id=prior[1]["new_operation"], duplicate=True)
    version, outcome = store.get_record("normal-result:" + parent_operation)
    if (parent["status"] != "WAITING_INFORMATION" or version != command.expected_version
        or correction_basis(parent) != command.expected_basis):
        raise StaleRecord("STALE_SOURCE_CORRECTION")
    packet = source_packet(root, parent)
    corrected = load_registered_case(root, profile="correction")
    fact = corrected.wire.financial_inputs.cash_available_for_debt_service.model_dump()
    if (not command.comments.strip() or command.value != fact["value"] or command.basis_id != fact["basis_id"]
        or [command.evidence_ref] != fact["refs"] or command.evidence_ref not in packet["request"]["reference_dictionary"]):
        raise InputError("EXACT_SOURCE_BACKED_CORRECTION_REQUIRED")
    operation = str(uuid5(UUID(command.operation_id), "corrected-run"))
    scope = Scope(**{**parent["context"]["scope"], "run_id": str(uuid5(UUID(operation), "run")),
                    "thread_id": str(uuid5(UUID(operation), "thread")), "input_revision": 2})
    stamp = datetime.now(timezone.utc).isoformat()
    context = dict(scope=scope.model_dump(), operation_id=operation, generation_time=stamp,
        case_dependency_digest=corrected.dependency_digest, synthesis_input_digest=prepare_synthesis(corrected)["input_digest"],
        mode="FIXTURE", scenario_id="E-N01", variant="default", profile="correction", entry_stage="financial_analyst",
        parent_operation=parent_operation, correction_event_id=command.operation_id)
    ledger_key = "ledger:" + scope.review_id
    ledger_version, ledger_data = store.get_record(ledger_key)
    ledger = Ledger.from_dict(ledger_data)
    if ledger.correction_used:
        raise InputError("CORRECTION_ALLOWANCE_ALREADY_USED")
    ledger.require_path("FINANCIAL_CORRECTION_DIRECT", fixture=True)
    ledger = replace(ledger, correction_used=True)
    event = dict(operation_id=command.operation_id, command_digest=digest, scope=parent["context"]["scope"],
        run_operation=parent_operation, previous_status="PENDING_INFORMATION", new_status="SUPERSEDED_BY_CORRECTION",
        action="SOURCE_CORRECTION_SAVED", decision=None, comments=command.comments, requested_items=[],
        reviewer_name="Simulated Analyst", reviewer_role="Analyst", timestamp_utc=stamp,
        provenance="EXECUTED_FIXTURE_REVIEW", new_operation=operation, original_basis=command.expected_basis,
        field=FIELD, old_fact=parent["artifacts"]["extractor"]["payload"]["wire"]["financial_inputs"][FIELD], corrected_fact=fact,
        evidence_refs=[command.evidence_ref], analysis_snapshot=dict(deal=event_deal_snapshot(parent),
            original_extraction=parent["artifacts"]["extractor"]["payload"]["wire"],
            risk=parent["artifacts"]["risk_quantifier"]["payload"], compliance=parent["artifacts"]["compliance_check"]["payload"],
            source_dependency=parent["context"]["case_dependency_digest"], ai={}))
    draft = dict(state="READY", context=context, event_id=command.operation_id, original_basis=command.expected_basis, command_digest=digest)
    ready = dict(status="READY", evidence_type="REVIEWER_CORRECTION_SAVED_NOT_EXECUTED", scope=scope.model_dump(),
        report_markdown=None, report_metadata=None, human_disposition=None, provider_requests=0,
        human_credit_review="Updated findings have not run; no credit decision available")
    try:
        receipt = store.admit(command.operation_id, parent["context"]["scope"], {"action": "SAVE_SOURCE_CORRECTION", "digest": digest}, writes=(
            RecordWrite(event_key, "FINANCIAL_REVIEW_EVENT", event),
            RecordWrite("normal-result:" + parent_operation, "NORMAL_FIXTURE_OUTCOME", {**outcome, "status": "SUPERSEDED", "correction_operation": operation}, version),
            RecordWrite("normal-context:" + operation, "NORMAL_FIXTURE_CONTEXT", context),
            RecordWrite("normal-result:" + operation, "NORMAL_FIXTURE_OUTCOME", ready),
            RecordWrite("source-correction:" + operation, "SOURCE_CORRECTION", draft),
            RecordWrite(ledger_key, "BUDGET_LEDGER", ledger.to_dict(), ledger_version)))
    except OperationConflict:
        prior = store.get_record(event_key)
        if prior is None or prior[1]["command_digest"] != digest:
            raise
        return dict(event=prior[1], operation_id=prior[1]["new_operation"], duplicate=True)
    if receipt.duplicate:
        return dict(event=store.get_record(event_key)[1], operation_id=operation, duplicate=True)
    store.release(receipt, confirmed_idle=True)
    return dict(event=event, operation_id=operation, duplicate=False)


def update_affected_findings(root, actor, operation, command):
    from .command_center import get_run
    from .configuration import load_configuration
    from .worker import run_normal_fixture
    command = UpdateCorrectionCommand.model_validate(command.model_dump())
    config = load_configuration(root); store = Store(config.database)
    run = get_run(store, actor, operation)
    if actor.persona != "Analyst" or run["context"].get("profile") != "correction":
        raise InputError("ANALYST_SAVED_CORRECTION_REQUIRED")
    saved = store.get_record("source-correction:" + operation)
    if saved is None:
        raise InputError("SAVED_CORRECTION_REQUIRED")
    version, draft = saved
    digest = fingerprint("UPDATE_SOURCE_CORRECTION", dict(command=command.model_dump(), actor=asdict(actor), operation=operation))
    if draft.get("dispatch_digest") is not None:
        if draft["dispatch_digest"] != digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return {**run["outcome"], "duplicate": True, "status": run["status"]}
    if run["status"] != "READY" or version != command.expected_version or command.expected_basis != draft_basis(draft):
        raise StaleRecord("STALE_READY_CORRECTION")
    parent = get_run(store, actor, run["context"]["parent_operation"])
    event = validate_saved_correction(config.workspace, store, parent, run["context"], draft)
    ledger_version, ledger_data = store.get_record("ledger:" + run["context"]["scope"]["review_id"])
    ledger = Ledger.from_dict(ledger_data)
    if not ledger.correction_used:
        raise InputError("SAVED_CORRECTION_ALLOWANCE_REQUIRED")
    ledger.require_path("FINANCIAL_CORRECTION_DIRECT", fixture=True)
    dispatch_event = dict(operation_id=str(uuid5(UUID(operation), "update-event")), command_digest=digest, scope=run["context"]["scope"],
        run_operation=operation, previous_status="READY", new_status="UPDATED_FINDINGS_REQUESTED", action="CORRECTION_APPLIED", decision=None,
        comments=event["comments"], requested_items=[], reviewer_name="Simulated Analyst", reviewer_role="Analyst",
        timestamp_utc=datetime.now(timezone.utc).isoformat(), provenance="EXECUTED_FIXTURE_REVIEW", evidence_refs=event["evidence_refs"],
        field=FIELD, old_fact=event["old_fact"], corrected_fact=event["corrected_fact"], correction_event_id=event["operation_id"],
        analysis_snapshot=event["analysis_snapshot"])
    try:
        return run_normal_fixture(config.workspace, operation, variant="default", _continuation=dict(kind="SOURCE_CORRECTION", parent=parent,
            ledger=ledger.to_dict(), ledger_version=ledger_version, event_id=event["operation_id"], draft=draft,
            writes=(RecordWrite("source-correction:" + operation, "SOURCE_CORRECTION", {**draft, "state": "DISPATCHED", "dispatch_digest": digest}, version),
                    RecordWrite("financial-review-event:" + dispatch_event["operation_id"], "FINANCIAL_REVIEW_EVENT", dispatch_event))))
    except OperationConflict:
        concurrent = store.get_record("source-correction:" + operation)
        if concurrent is None or concurrent[1].get("dispatch_digest") != digest:
            raise
        current = get_run(store, actor, operation)
        return {**current["outcome"], "duplicate": True, "status": current["status"]}
