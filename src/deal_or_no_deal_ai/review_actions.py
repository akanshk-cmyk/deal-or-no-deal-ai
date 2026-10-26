"""Persisted REVIEW-UI-1.0 preview adapter; never a financial workflow resume.

Only ILLUSTRATIVE_UI_ONLY records are accepted. Real request registration,
checkpoint validation and RESUME-1.0 dispatch need the later workflow adapter.
"""

from dataclasses import asdict, fields, replace
from datetime import datetime, timezone
import json
from typing import Annotated, Literal
from uuid import NAMESPACE_URL, uuid5

from pydantic import Field, field_validator, model_validator

from .context import InputError, fingerprint, primitive, stable_id, unicode_scalar
from .contracts import Identifier, StrictModel
from .review import Actor, PendingReview, Requirement, accept_review, review_action_availability
from .storage import OperationConflict, RecordWrite, RunBusy, StaleRecord, Store


WORKSPACE_ID = str(uuid5(NAMESPACE_URL, "deal-or-no-deal-ai:illustrative-review-ui"))
ROLES = ("Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator")
EXAMPLES = (("ready", "Sample A — review actions", "NORMAL"),
            ("blocked", "Sample B — unresolved information", "NORMAL"),
            ("senior", "Sample C — senior review required", "SENIOR"))
ACTION_LABELS = {"ADD_COMMENT": "Add comment", "APPROVE": "Approve", "REJECT": "Reject",
                 "REQUEST_INFORMATION": "Request Additional Information (Pending)"}
REVIEWER_NAMES = {"Analyst": "Demo Credit Analyst", "RiskManager": "Demo Risk Manager",
                  "ComplianceOfficer": "Demo Compliance Officer", "AuthorizedApprover": "Demo Authorized Approver",
                  "Administrator": "Demo Administrator"}


def capture_decision_context(data: dict, request: PendingReview) -> dict:
    """Copy only trusted pre-action context; unknown is not zero or current data."""
    deal = data.get("deal_context", {})
    analysis = data.get("decision_context", {})
    return primitive(dict(version="DECISION-SNAPSHOT-1.0", deal_id=request.deal_id,
        deal_title=data.get("title"), borrower_name=deal.get("borrower_name"),
        loan_amount=deal.get("loan_amount"), currency=deal.get("currency"), deal_type=deal.get("deal_type"),
        ai_recommendation=analysis.get("ai_recommendation", data.get("original_ai_recommendation")),
        ai_analysis_version=analysis.get("ai_analysis_version"), risk_assessment=analysis.get("risk_assessment"),
        compliance_findings=analysis.get("compliance_findings"), policy_exceptions=analysis.get("policy_exceptions"),
        supporting_documents=analysis.get("supporting_documents")))


def _id(name):
    return stable_id(WORKSPACE_ID, name)


def _request_key(request_id):
    return "ui-review:request:" + request_id


def _decode_request(data):
    if type(data) is not dict or set(data) != {f.name for f in fields(PendingReview)}:
        raise InputError("INVALID_UI_REVIEW_REQUEST")
    restored = dict(data)
    restored["requirements"] = tuple(Requirement(**item) for item in restored["requirements"])
    request = PendingReview(**restored)
    if request.workspace_id != WORKSPACE_ID:
        raise InputError("UI_PREVIEW_SCOPE_REQUIRED")
    return request


class ReviewActionCommand(StrictModel):
    operation_id: Identifier
    request_id: Identifier
    expected_version: Annotated[int, Field(ge=1)]
    expected_gate_version: Annotated[int, Field(ge=1)]
    expected_basis: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    action: Literal["ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION"]
    comments: Annotated[str, Field(min_length=1, max_length=4096)]
    requested_items: list[Annotated[str, Field(min_length=1, max_length=512)]] = Field(max_length=20)

    @field_validator("comments")
    @classmethod
    def comment_required(cls, value):
        unicode_scalar(value)
        if not value.strip():
            raise ValueError("REVIEW_COMMENT_REQUIRED")
        return value

    @model_validator(mode="after")
    def information_items(self):
        items = [unicode_scalar(item).strip() for item in self.requested_items]
        if any(not item for item in items) or len(set(items)) != len(items):
            raise ValueError("DISTINCT_NONBLANK_INFORMATION_ITEMS_REQUIRED")
        if (self.action == "REQUEST_INFORMATION") != bool(items):
            raise ValueError("INFORMATION_ITEMS_REQUIRED_ONLY_FOR_REQUEST")
        return self


def preview_actor(persona: str, *, senior: bool = False) -> Actor:
    """Trusted demo configuration; explicitly simulated, never authentication."""
    if persona not in ROLES or type(senior) is not bool:
        raise InputError("INVALID_DEMO_PERSONA")
    tiers = frozenset({"NORMAL", "SENIOR"} if senior else {"NORMAL"}) if persona == "AuthorizedApprover" else frozenset()
    return Actor(persona, WORKSPACE_ID, frozenset(_id("deal:" + name) for name, _, _ in EXAMPLES), tiers)


def _scope(actor, request):
    # Shared capability projection validates workspace/deal/simulation first.
    return review_action_availability(request, actor)


def _read(connection, key):
    row = connection.execute("SELECT version,kind,payload FROM app_records WHERE record_key=?", (key,)).fetchone()
    return None if row is None else (row["version"], row["kind"], json.loads(row["payload"]))


def _payload(saved):
    if saved is None or saved[1] != "ILLUSTRATIVE_UI_REVIEW":
        raise InputError("UI_PREVIEW_REQUEST_NOT_FOUND")
    data = saved[2]
    if data.get("version") != "REVIEW-UI-1.0" or data.get("provenance") != "ILLUSTRATIVE_UI_ONLY":
        raise InputError("UI_PREVIEW_RECORD_REQUIRED")
    return data, _decode_request(data["request"])


def prepare_review_examples(store: Store) -> None:
    """Explicit instructor action; opening a screen never seeds review records."""
    store.initialize()
    with store.transaction() as connection:
        if connection.execute("SELECT 1 FROM app_operations WHERE active_execution_key IS NOT NULL").fetchone():
            raise RunBusy("RUN_BUSY")
        for name, title, tier in EXAMPLES:
            request_id = _id("request:" + name)
            if _read(connection, _request_key(request_id)) is not None:
                continue  # Preserve decisions/comments across app restarts.
            requirements = (Requirement("UI-only missing evidence example", False, None, 1),) if name == "blocked" else ()
            request = PendingReview(request_id, WORKSPACE_ID, _id("deal:" + name), _id("thread:" + name), 1,
                fingerprint("ILLUSTRATIVE_UI_BASIS", {"sample": name, "financial_analysis": None}), 1, tier, requirements)
            data = dict(version="REVIEW-UI-1.0", provenance="ILLUSTRATIVE_UI_ONLY", title=title,
                request=primitive(asdict(request)), decision_status="AWAITING_REVIEW", information_pending=False,
                event_ids=[], original_ai_recommendation=None, graph_progress="NOT_CONNECTED",
                deal_context=dict(borrower_name="UI Sample " + name + " borrower", loan_amount=None,
                                  currency=None, deal_type="Illustrative UI sample"))
            store._write(connection, RecordWrite(_request_key(request_id), "ILLUSTRATIVE_UI_REVIEW", data))


def list_review_examples(store: Store, actor: Actor) -> list[dict]:
    if not store.path.exists():
        return []
    results = []
    with store.connection() as connection:
        for name, _, _ in EXAMPLES:
            saved = _read(connection, _request_key(_id("request:" + name)))
            if saved is None:
                continue
            data, request = _payload(saved)
            _scope(actor, request)
            results.append(dict(request_id=request.request_id, title=data["title"], decision_status=data["decision_status"]))
    return results


def get_review_panel(store: Store, request_id: str, actor: Actor) -> dict:
    with store.connection() as connection:
        saved = _read(connection, _request_key(request_id))
        data, request = _payload(saved)
        _scope(actor, request)
        busy = connection.execute("SELECT 1 FROM app_operations WHERE active_execution_key IS NOT NULL").fetchone() is not None
        events = []
        for operation_id in data["event_ids"]:
            event = _read(connection, "ui-review:event:" + operation_id)
            if event is None or event[1] != "ILLUSTRATIVE_UI_REVIEW_EVENT" or event[2]["request_id"] != request_id:
                raise InputError("UI_REVIEW_HISTORY_MISMATCH")
            events.append(event[2])
    actions = review_action_availability(request, actor, information_pending=data["information_pending"])
    if busy:
        actions = {action: "RUN_BUSY" if reason is None else reason for action, reason in actions.items()}
    return dict(**data, record_version=saved[0], history=events, actions=actions)


def record_review_action(store: Store, actor: Actor, command: ReviewActionCommand, *, clock=None) -> dict:
    """Atomically record a scoped UI-only action and history; zero graph work."""
    if type(command) is not ReviewActionCommand:
        raise InputError("VALIDATED_REVIEW_COMMAND_REQUIRED")
    command = ReviewActionCommand.model_validate(command.model_dump())
    clock = clock or (lambda: datetime.now(timezone.utc))
    reviewer_id = stable_id(actor.workspace_id, "SIMULATED_REVIEWER:" + actor.persona)
    digest = fingerprint("UI_REVIEW_COMMAND", {"command": command.model_dump(), "actor": asdict(actor)})
    with store.transaction() as connection:
        saved = _read(connection, _request_key(command.request_id))
        data, request = _payload(saved)
        _scope(actor, request)
        event_key = "ui-review:event:" + command.operation_id
        prior = _read(connection, event_key)
        if prior is not None:
            if prior[1] != "ILLUSTRATIVE_UI_REVIEW_EVENT" or prior[2]["command_digest"] != digest:
                raise OperationConflict("OPERATION_CONFLICT")
            return prior[2]  # Keep the original timestamp; no duplicate event.
        if saved[0] != command.expected_version:
            raise StaleRecord("REVIEW_RECORD_CHANGED")
        if request.analytical_basis_digest != command.expected_basis or request.gate_version != command.expected_gate_version:
            raise InputError("STALE_REVIEW_BASIS")
        if connection.execute("SELECT 1 FROM app_operations WHERE active_execution_key IS NOT NULL").fetchone():
            raise RunBusy("RUN_BUSY")
        reason = review_action_availability(request, actor, information_pending=data["information_pending"])[command.action]
        if reason is not None:
            raise InputError(reason)
        updated = dict(data)
        if command.action in ("APPROVE", "REJECT"):
            decision = "Approve" if command.action == "APPROVE" else "Reject"
            accept_review(request, actor, command.operation_id, decision,
                expected_basis=command.expected_basis, expected_gate_version=command.expected_gate_version)
            updated["request"] = primitive(asdict(replace(request, state="RECORDED", recorded_operation_id=command.operation_id)))
            updated["decision_status"] = "APPROVED" if command.action == "APPROVE" else "REJECTED"
        elif command.action == "REQUEST_INFORMATION":
            updated.update(decision_status="NEEDS_INFORMATION", information_pending=True)
        stamp = clock()
        if not isinstance(stamp, datetime) or stamp.tzinfo is None or stamp.utcoffset() is None:
            raise InputError("APPLICATION_TIMESTAMP_REQUIRED")
        timestamp = stamp.astimezone(timezone.utc).isoformat()
        event = dict(version="REVIEW-UI-1.0", provenance="ILLUSTRATIVE_UI_ONLY", operation_id=command.operation_id,
            command_digest=digest, request_id=request.request_id, deal_id=request.deal_id,
            thread_id=request.thread_id, input_revision=request.input_revision,
            analytical_basis_digest=request.analytical_basis_digest, gate_version=request.gate_version,
            expected_record_version=command.expected_version, reviewer_id=reviewer_id, reviewer_role=actor.persona,
            reviewer_tiers=sorted(actor.allowed_review_tiers), attribution="SIMULATED", timestamp_utc=timestamp,
            reviewer_name=REVIEWER_NAMES[actor.persona], previous_status=data["decision_status"],
            event_sequence=len(data["event_ids"]) + 1, context_snapshot=capture_decision_context(data, request),
            action=command.action, comments=command.comments, requested_items=command.requested_items,
            decision_status=updated["decision_status"], graph_progress="NOT_CONNECTED")
        updated["event_ids"] = [*data["event_ids"], command.operation_id]
        store._write(connection, RecordWrite(event_key, "ILLUSTRATIVE_UI_REVIEW_EVENT", event))
        store._write(connection, RecordWrite(_request_key(request.request_id), "ILLUSTRATIVE_UI_REVIEW", updated, saved[0]))
        return event
