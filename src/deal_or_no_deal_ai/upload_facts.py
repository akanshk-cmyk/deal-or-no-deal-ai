"""Source-bound reviewer candidates and data-quality support, never deal approval."""
from dataclasses import asdict
from datetime import date, datetime, timezone
from decimal import Decimal, localcontext
from typing import Annotated, Literal
from pydantic import Field

from .context import InputError, FINANCIAL_FIELDS, fingerprint, money_string, canonical_decimal
from .contracts import StrictModel, Identifier, Text
from .configuration import load_configuration
from .finance import calculate_metrics
from .storage import Store, RecordWrite, StaleRecord, OperationConflict
from .upload_intake import load_package, _authorize

FIELDS = ("cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments")
CHECKS = ("reference", "row_label", "value", "units_scale", "period", "subject_facility", "debt_service_scope")
FieldName = Literal["cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments"]


class ProposalCommand(StrictModel):
    operation_id: Identifier
    expected_version: Annotated[int, Field(ge=0)]
    field: FieldName
    source_ref: Text
    quote: Annotated[str, Field(min_length=1, max_length=4096)]
    quote_start: Annotated[int, Field(ge=0)]
    raw_number: Text
    raw_label: Text
    unit_label: Text
    scale: Literal["1", "1000", "1000000"]
    currency: Literal["USD"]
    subject: Text
    facility: Text
    period_start: Text
    period_end: Text
    basis_kind: Literal["ANNUAL_ACTUAL", "ANNUAL_PROJECTION"]
    comments: Annotated[str, Field(min_length=1, max_length=4096)]


class SupportCommand(StrictModel):
    operation_id: Identifier
    expected_version: Annotated[int, Field(ge=1)]
    proposal_id: Identifier
    target_digest: Text
    status: Literal["HUMAN_SUPPORTED", "UNSUPPORTED", "WITHHELD"]
    checks: list[Literal["reference", "row_label", "value", "units_scale", "period", "subject_facility", "debt_service_scope"]] = Field(max_length=7)
    comments: Annotated[str, Field(min_length=1, max_length=4096)]


def _key(operation):
    return "upload-facts:" + operation


def _proposal(package, command):
    page = next((p for s in package["sources"] for p in s["pages"] if p["ref"] == command.source_ref), None)
    if (page is None or not command.quote.strip() or not command.comments.strip() or not command.subject.strip()
        or not command.facility.strip() or not command.raw_label.strip() or not command.unit_label.strip()
        or page["text"][command.quote_start:command.quote_start + len(command.quote)] != command.quote
        or command.raw_number not in command.quote or command.raw_label not in command.quote or command.unit_label not in page["text"]):
        raise InputError("EXACT_FACT_SOURCE_SPAN_REQUIRED")
    start, end = date.fromisoformat(command.period_start), date.fromisoformat(command.period_end)
    if start.isoformat() != command.period_start or end.isoformat() != command.period_end or (end - start).days not in (364, 365):
        raise InputError("ANNUAL_FINANCIAL_PERIOD_REQUIRED")
    raw = money_string(command.raw_number)
    # Prevent substring support: e.g. 90 must not be accepted from a quoted 900000.
    offset = command.quote.find(command.raw_number); stop = offset + len(command.raw_number)
    if (offset > 0 and command.quote[offset - 1] in "+-0123456789.," or stop < len(command.quote) and command.quote[stop] in "0123456789.,"):
        raise InputError("EXACT_NUMERIC_TOKEN_REQUIRED")
    with localcontext() as context:
        context.prec = 50
        value = money_string(canonical_decimal(Decimal(raw) * Decimal(command.scale)))
    if command.field != "cash_available_for_debt_service" and Decimal(value) < 0:
        raise InputError("NEGATIVE_DEBT_SERVICE_INPUT")
    content = {k: v for k, v in command.model_dump().items() if k not in ("operation_id", "expected_version", "comments")}
    content.update(value=value, package_digest=package["package_digest"], page_text_digest=page["text_sha256"],
        normalized_currency="USD", origin="REVIEWER_PROVIDED", purpose="UPLOAD_CANDIDATE_ONLY")
    content["target_digest"] = fingerprint("UPLOAD_FACT_TARGET", content)
    return content


def get_fact_review(root, actor, upload_operation):
    package = load_package(root, actor, upload_operation)
    store = Store(load_configuration(root).database)
    saved = store.get_record(_key(upload_operation))
    version, data = saved if saved else (0, dict(package_digest=package["package_digest"], event_ids=[]))
    if data["package_digest"] != package["package_digest"]:
        raise InputError("UPLOAD_FACT_PACKAGE_CHANGED")
    latest, supports, events = {}, {}, []
    for event_id in data["event_ids"]:
        saved_event = store.get_record("upload-fact-event:" + event_id)
        if saved_event is None:
            raise InputError("UPLOAD_FACT_EVENT_MISSING")
        event = saved_event[1]
        if (event["upload_operation"] != upload_operation or event["workspace_id"] != actor.workspace_id
            or event["previous_version"] != len(events) or not event["comments"].strip()):
            raise InputError("UPLOAD_FACT_EVENT_CHANGED")
        if event["command"]["expected_version"] != event["previous_version"] or event["command"]["comments"] != event["comments"]:
            raise InputError("UPLOAD_FACT_COMMAND_CHANGED")
        if event["action"] == "PROPOSE_FACT":
            command = ProposalCommand.model_validate(event["command"])
            content = _proposal(package, command)
            if event["reviewer_role"] != "Analyst" or event["content"] != content or event_id != command.operation_id:
                raise InputError("UPLOAD_FACT_PROPOSAL_CHANGED")
            latest[command.field] = event
            supports.pop(command.field, None)
        elif event["action"] == "REVIEW_FACT":
            command = SupportCommand.model_validate(event["command"])
            proposal = next((e for e in latest.values() if e["operation_id"] == command.proposal_id), None)
            if (event["reviewer_role"] != "RiskManager" or event_id != command.operation_id or proposal is None
                or proposal["content"]["target_digest"] != command.target_digest
                or command.status == "HUMAN_SUPPORTED" and set(command.checks) != set(CHECKS)
                or len(command.checks) != len(set(command.checks)) or proposal["content"]["field"] in supports):
                raise InputError("UPLOAD_FACT_SUPPORT_CHANGED")
            supports[proposal["content"]["field"]] = event
        else:
            raise InputError("UNKNOWN_UPLOAD_FACT_EVENT")
        events.append(event)
    return dict(version=version, package=package, data=data, latest=latest, supports=supports, events=events)


def record_fact_action(root, actor, upload_operation, command):
    _authorize(load_configuration(root).workspace, actor)
    proposal_action = isinstance(command, ProposalCommand)
    command = (ProposalCommand if proposal_action else SupportCommand).model_validate(command.model_dump())
    if actor.persona != ("Analyst" if proposal_action else "RiskManager"):
        raise InputError("UPLOAD_FACT_ROLE_REQUIRED")
    panel = get_fact_review(root, actor, upload_operation)
    store = Store(load_configuration(root).database)
    key = "upload-fact-event:" + command.operation_id
    digest = fingerprint("UPLOAD_FACT_COMMAND", dict(command=command.model_dump(), actor=asdict(actor), upload=upload_operation))
    prior = store.get_record(key)
    if prior:
        if prior[1]["command_digest"] != digest:
            raise OperationConflict("OPERATION_CONFLICT")
        return prior[1]
    if panel["version"] != command.expected_version:
        raise StaleRecord("STALE_UPLOAD_FACT_REVIEW")
    if len(panel["events"]) >= 1000:
        raise InputError("UPLOAD_FACT_HISTORY_LIMIT")
    if not command.comments.strip():
        raise InputError("FACT_REVIEW_REASON_REQUIRED")
    content = _proposal(panel["package"], command) if proposal_action else None
    if not proposal_action:
        target = next((e for e in panel["latest"].values() if e["operation_id"] == command.proposal_id), None)
        if (target is None or target["content"]["target_digest"] != command.target_digest
            or target["content"]["field"] in panel["supports"] or len(command.checks) != len(set(command.checks))
            or command.status == "HUMAN_SUPPORTED" and set(command.checks) != set(CHECKS)):
            raise InputError("CURRENT_EXACT_FACT_SUPPORT_REQUIRED")
    event = dict(operation_id=command.operation_id, command_digest=digest, upload_operation=upload_operation,
        workspace_id=actor.workspace_id, previous_version=panel["version"], action="PROPOSE_FACT" if proposal_action else "REVIEW_FACT",
        command=command.model_dump(), content=content, comments=command.comments, reviewer_role=actor.persona,
        reviewer_name="Simulated " + actor.persona, timestamp_utc=datetime.now(timezone.utc).isoformat())
    scope = dict(workspace_id=actor.workspace_id, package_id=panel["package"]["package_id"], review_id=upload_operation)
    data = {**panel["data"], "event_ids": panel["data"]["event_ids"] + [command.operation_id]}
    try:
        receipt = store.admit(command.operation_id, scope, dict(action=event["action"], digest=digest), writes=(
            RecordWrite(key, "UPLOAD_FACT_EVENT", event), RecordWrite(_key(upload_operation), "UPLOAD_FACT_REVIEW", data, panel["version"])))
    except OperationConflict:
        prior = store.get_record(key)
        if prior is None or prior[1]["command_digest"] != digest:
            raise
        return prior[1]
    if not receipt.duplicate:
        store.release(receipt, confirmed_idle=True)
    return store.get_record(key)[1]


def dscr_preview(panel):
    blockers, contents = [], []
    for name in FIELDS:
        proposed = panel["latest"].get(name); support = panel["supports"].get(name)
        if proposed is None or support is None or support["command"]["status"] != "HUMAN_SUPPORTED":
            blockers.append(name + ": supported current evidence required")
        else:
            contents.append(proposed["content"])
    basis_keys = ("subject", "facility", "period_start", "period_end", "basis_kind", "normalized_currency")
    if not blockers and len({tuple(c[k] for k in basis_keys) for c in contents}) != 1:
        blockers.append("Subject, facility, period or actual/projection basis does not match")
    if blockers:
        return dict(status="UNKNOWN", display=None, blockers=blockers)
    values = {k: None for k in FINANCIAL_FIELDS}
    values.update({c["field"]: c["value"] for c in contents})
    # Only CALC-004 is exposed; no collateral classification/result is inferred.
    metric = calculate_metrics(values, secured_equipment=True)["CALC-004"]
    return dict(status=metric.validity, display=metric.display, blockers=[] if metric.validity == "VALID" else [metric.reason],
        definition=metric.definition_version, refs=[c["source_ref"] for c in contents])
