"""Scoped, read-only decision history and explicit CSV export; no reconstruction LLM."""

import csv
from datetime import date, datetime, timezone
from io import StringIO
import json
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator

from .context import InputError, canonical_json, fingerprint, unicode_scalar
from .contracts import StrictModel
from .review_actions import ROLES, _payload, _read, capture_decision_context


STATUSES = ("AWAITING_REVIEW", "NEEDS_INFORMATION", "APPROVED", "REJECTED")
MAX_EXPORT_EVENTS = 5000


class HistoryFilters(StrictModel):
    deal_id: Annotated[str, Field(max_length=200)] = ""
    borrower: Annotated[str, Field(max_length=200)] = ""
    reviewer: Annotated[str, Field(max_length=200)] = ""
    actions: list[Literal["ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION"]] = Field(default_factory=list, max_length=4)
    statuses: list[Literal["AWAITING_REVIEW", "NEEDS_INFORMATION", "APPROVED", "REJECTED"]] = Field(default_factory=list, max_length=4)
    start_date: date | None = None
    end_date: date | None = None
    newest_first: bool = True

    @field_validator("deal_id", "borrower", "reviewer")
    @classmethod
    def text_is_inert(cls, value):
        return unicode_scalar(value)

    @model_validator(mode="after")
    def dates_in_order(self):
        if self.start_date is not None and self.end_date is not None and self.start_date > self.end_date:
            raise ValueError("HISTORY_DATE_RANGE_REVERSED")
        return self


def _authorize(actor):
    if actor.attribution != "SIMULATED" or actor.persona not in ROLES:
        raise InputError("HISTORY_ACCESS_DENIED")


def _timestamp(value):
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError
        return stamp.astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError):
        raise InputError("HISTORY_TIMESTAMP_UNAVAILABLE") from None


def _all_scoped_rows(store, actor):
    _authorize(actor)
    if not store.path.exists():
        return [], []
    rows, deals = [], []
    with store.connection() as connection:
        connection.execute("BEGIN")  # One consistent read snapshot; no writes/init.
        records = connection.execute("SELECT record_key,version,kind,payload FROM app_records WHERE kind=?",
                                     ("ILLUSTRATIVE_UI_REVIEW",)).fetchall()
        for record in records:
            data = json.loads(record["payload"])
            if type(data) is not dict or type(data.get("request")) is not dict:
                raise InputError("HISTORY_REQUEST_UNAVAILABLE")
            scope = data.get("request", {})
            # Exclude other scopes before collecting event details or counts.
            if scope.get("workspace_id") != actor.workspace_id or scope.get("deal_id") not in actor.allowed_deal_ids:
                continue
            data, request = _payload((record["version"], record["kind"], data))
            deals.append(dict(deal_id=request.deal_id, title=data["title"], current_status=data["decision_status"]))
            for index, event_id in enumerate(data["event_ids"], 1):
                saved = _read(connection, "ui-review:event:" + event_id)
                if saved is None or saved[1] != "ILLUSTRATIVE_UI_REVIEW_EVENT":
                    raise InputError("HISTORY_EVENT_UNAVAILABLE")
                event = saved[2]
                if (type(event) is not dict or event.get("request_id") != request.request_id or event.get("deal_id") != request.deal_id
                        or event.get("operation_id") != event_id or event.get("provenance") != "ILLUSTRATIVE_UI_ONLY"):
                    raise InputError("HISTORY_EVENT_SCOPE_MISMATCH")
                context = event.get("context_snapshot")
                previous = event.get("previous_status")
                source = "EVENT_TIME_SNAPSHOT"
                if context is None:
                    # Faithfully recover only the saved pre-action version, not latest context.
                    prior = connection.execute("SELECT payload FROM app_record_history WHERE record_key=? AND version=?",
                        (record["record_key"], event.get("expected_record_version"))).fetchone()
                    if prior is not None:
                        old = json.loads(prior[0])
                        old_scope = old.get("request", {})
                        if old_scope.get("request_id") != request.request_id or old_scope.get("deal_id") != request.deal_id:
                            raise InputError("HISTORY_PRIOR_SCOPE_MISMATCH")
                        context = capture_decision_context(old, request)
                        previous = old.get("decision_status")
                        source = "RECORDED_PRE_ACTION_VERSION"
                    else:
                        context = dict(version="DECISION-SNAPSHOT-1.0", deal_id=request.deal_id)
                        source = "LEGACY_NOT_CAPTURED"
                if (type(context) is not dict or context.get("version") != "DECISION-SNAPSHOT-1.0"
                        or context.get("deal_id") != request.deal_id):
                    raise InputError("HISTORY_SNAPSHOT_SCOPE_MISMATCH")
                if event.get("action") not in ("ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION") or event.get("decision_status") not in STATUSES:
                    raise InputError("HISTORY_EVENT_STATE_UNAVAILABLE")
                stamp = _timestamp(event["timestamp_utc"])
                rows.append(dict(event_id=event_id, timestamp_utc=stamp.isoformat(),
                    event_sequence=event.get("event_sequence", index), deal_id=request.deal_id,
                    borrower_name=context.get("borrower_name"), loan_amount=context.get("loan_amount"),
                    currency=context.get("currency"), deal_type=context.get("deal_type"),
                    deal_title=context.get("deal_title"), current_status=data["decision_status"],
                    previous_status=previous, new_status=event["decision_status"], action=event["action"],
                    reviewer_id=event["reviewer_id"], reviewer_name=event.get("reviewer_name"),
                    reviewer_role=event["reviewer_role"], reviewer_tiers=event["reviewer_tiers"],
                    comments=event["comments"], decision_reason=event["comments"], requested_items=event["requested_items"],
                    input_revision=event["input_revision"], analytical_basis_digest=event["analytical_basis_digest"],
                    context_snapshot=context, snapshot_source=source, provenance=event["provenance"]))
        connection.execute("COMMIT")
    return rows, sorted(deals, key=lambda item: item["deal_id"])


def _matches(row, filters):
    for field, text in (("deal_id", filters.deal_id), ("borrower_name", filters.borrower)):
        if text.strip().casefold() not in str(row.get(field) or "").casefold():
            return False
    reviewer = " ".join(str(row.get(field) or "") for field in ("reviewer_id", "reviewer_name", "reviewer_role"))
    if filters.reviewer.strip().casefold() not in reviewer.casefold():
        return False
    if filters.actions and row["action"] not in filters.actions:
        return False
    if filters.statuses and row["new_status"] not in filters.statuses:
        return False
    day = _timestamp(row["timestamp_utc"]).date()
    return not ((filters.start_date is not None and day < filters.start_date)
                or (filters.end_date is not None and day > filters.end_date))


def _filtered(store, actor, filters):
    if type(filters) is not HistoryFilters:
        raise InputError("VALIDATED_HISTORY_FILTERS_REQUIRED")
    filters = HistoryFilters.model_validate(filters.model_dump())
    rows, deals = _all_scoped_rows(store, actor)
    matched = [row for row in rows if _matches(row, filters)]
    matched.sort(key=lambda row: (_timestamp(row["timestamp_utc"]), row["event_sequence"], row["event_id"]),
                 reverse=filters.newest_first)
    digest = fingerprint("HISTORY_VIEW-1.0", dict(workspace=actor.workspace_id,
        allowed_deal_ids=actor.allowed_deal_ids, persona=actor.persona, filters=filters.model_dump(), rows=matched))
    return matched, deals, digest


def query_decision_history(store, actor, filters=None, *, offset=0, limit=50):
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100:
        raise InputError("INVALID_HISTORY_PAGE")
    filters = filters if filters is not None else HistoryFilters()
    rows, deals, digest = _filtered(store, actor, filters)
    return dict(version="DECISION-HISTORY-1.0", total=len(rows), offset=offset, limit=limit,
        rows=rows[offset:offset + limit], deals=deals, snapshot_digest=digest,
        coverage="Recorded illustrative review actions only; upload/agent lifecycle events are not connected.")


def get_deal_timeline(store, actor, deal_id):
    _authorize(actor)
    if deal_id not in actor.allowed_deal_ids:
        raise InputError("HISTORY_DEAL_ACCESS_DENIED")
    rows, _ = _all_scoped_rows(store, actor)
    rows = [row for row in rows if row["deal_id"] == deal_id]
    if len(rows) > MAX_EXPORT_EVENTS:
        raise InputError("HISTORY_TIMELINE_LIMIT")
    return sorted(rows, key=lambda row: (_timestamp(row["timestamp_utc"]), row["event_sequence"], row["event_id"]))


def _csv_cell(value):
    if value is None:
        return "Not captured"
    text = canonical_json(value) if isinstance(value, (dict, list)) else str(value)
    # Quoting alone does not stop spreadsheet formulas; preserve original in DB.
    if text.startswith(("\t", "\r", "\n")) or text.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def export_decision_history_csv(store, actor, filters, *, expected_digest, clock=None):
    rows, _, digest = _filtered(store, actor, filters)
    if expected_digest != digest:
        raise InputError("HISTORY_EXPORT_STALE_REFRESH_REQUIRED")
    if len(rows) > MAX_EXPORT_EVENTS:
        raise InputError("HISTORY_EXPORT_LIMIT_NARROW_FILTERS")
    clock = clock or (lambda: datetime.now(timezone.utc))
    stamp = clock()
    if not isinstance(stamp, datetime) or stamp.tzinfo is None or stamp.utcoffset() is None:
        raise InputError("HISTORY_EXPORT_UTC_TIME_REQUIRED")
    exported_at = stamp.astimezone(timezone.utc).isoformat()
    columns = ["timestamp_utc", "event_id", "deal_id", "borrower_name", "loan_amount", "currency", "deal_type",
        "previous_status", "new_status", "current_status", "action", "reviewer_name", "reviewer_role", "reviewer_id",
        "comments", "decision_reason", "requested_items", "input_revision", "analytical_basis_digest", "snapshot_source",
        "provenance", "ai_recommendation", "ai_analysis_version", "risk_assessment", "compliance_findings",
        "policy_exceptions", "supporting_documents", "exported_at_utc", "export_snapshot_digest"]
    stream = StringIO(newline="")
    writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
    writer.writerow(columns)
    for row in rows:
        context = row["context_snapshot"]
        values = {**row, **{key: context.get(key) for key in (
            "ai_recommendation", "ai_analysis_version", "risk_assessment", "compliance_findings", "policy_exceptions", "supporting_documents")},
            "exported_at_utc": exported_at, "export_snapshot_digest": digest}
        writer.writerow([_csv_cell(values.get(key)) for key in columns])
    return dict(content=stream.getvalue().encode("utf-8-sig"), row_count=len(rows), snapshot_digest=digest,
                exported_at_utc=exported_at, filename="decision-history-" + stamp.astimezone(timezone.utc).strftime("%Y%m%d") + ".csv")
