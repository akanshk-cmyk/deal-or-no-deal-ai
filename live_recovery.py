"""Guarded settled-output recovery and exact user-approved uncertain quarantine."""
from datetime import datetime,timezone
from decimal import Decimal
from uuid import UUID,uuid5
from .command_center import _scope
from .context import InputError
from .storage import Receipt,RecordWrite
from .budgets import Ledger,Usage
import json

QUARANTINE_OPERATION = "aab508af-564d-461f-a4e7-cf0708ec29b6"
ADDITIONAL_QUARANTINE_OPERATION = "54b1dd19-7dad-4ead-b297-31aae29a0d86"
LATEST_SAMPLE_QUARANTINE_OPERATION = "51eef80e-e890-4c62-91bb-c25478a5adf1"
NETWORK_BLOCKED_SAMPLE_OPERATION = "1d478574-1e3d-426c-bfe5-622b75872e79"


def quarantine_unknown_extraction(store, actor, operation, *, expected_versions, reason):
    """Approved administrative abandonment, never provider-usage reconciliation.

    Only the specifically approved attempt is eligible. Preserve its full ledger,
    checkpoints and allowance reservation; release only the exclusive local claim.
    """
    if actor.persona != "Administrator":
        raise InputError("ADMINISTRATOR_QUARANTINE_REQUIRED")
    if operation not in (QUARANTINE_OPERATION,ADDITIONAL_QUARANTINE_OPERATION,LATEST_SAMPLE_QUARANTINE_OPERATION,NETWORK_BLOCKED_SAMPLE_OPERATION):
        raise InputError("APPROVED_QUARANTINE_OPERATION_REQUIRED")
    if type(reason) is not str or not reason.strip() or len(reason) > 4000:
        raise InputError("QUARANTINE_REASON_REQUIRED")
    if (type(expected_versions) is not dict or set(expected_versions) != {"context","progress","ledger","allowance","request"}
        or any(type(v) is not int or v < 1 for v in expected_versions.values())):
        raise InputError("QUARANTINE_EXPECTED_VERSIONS_REQUIRED")
    paid_id = str(uuid5(UUID(operation), "paid:extractor"))
    with store.transaction() as connection:
        def read(key):
            row = connection.execute("SELECT version,payload FROM app_records WHERE record_key=?",(key,)).fetchone()
            if row is None:
                raise InputError("QUARANTINE_RECORD_REQUIRED")
            return row["version"], json.loads(row["payload"])
        cv, context = read("live-context:" + operation)
        _scope(actor, context["scope"])
        review = context["scope"]["review_id"]
        quarantine_key = "quarantine-review:" + review
        prior = connection.execute("SELECT payload FROM app_records WHERE record_key=?",(quarantine_key,)).fetchone()
        if prior:
            original = json.loads(prior[0])
            if original["operation_id"] != operation or original["reason"] != reason or original["expected_versions"] != expected_versions:
                raise InputError("QUARANTINE_COMMAND_CONFLICT")
            return original
        pv, progress = read("live-progress:" + operation)
        lv, ledger_data = read("ledger:" + review)
        av, allowance = read("paid-allowance:first-synthetic-010")
        rv, request = read("paid-request:" + paid_id)
        if expected_versions != dict(context=cv, progress=pv, ledger=lv, allowance=av, request=rv):
            raise InputError("QUARANTINE_STALE_RECORD_VERSION")
        claim = connection.execute("SELECT * FROM app_operations WHERE operation_id=?",(operation,)).fetchone()
        ledger = Ledger.from_dict(ledger_data)
        node = operation + ":node:extractor"
        if (claim is None or claim["state"] != "RECOVERY_REQUIRED" or claim["active_execution_key"] != "LOCAL_EXECUTION"
            or claim["review_id"] != review or json.loads(claim["scope_payload"]) != context["scope"]
            or progress["context"] != context or set(progress["artifacts"]) != {"pdf_input"}
            or progress.get("pending_stage") is not None or progress.get("report_markdown")
            or request.get("scope",{}).get("review_id") != review
            or request.get("scope",{}).get("workspace_id") != context["scope"]["workspace_id"]
            or set(ledger.reservations) != {paid_id,node} or ledger.unknown != frozenset({paid_id})
            or allowance.get("limit_usd") != "0.10"
            or allowance.get("reservations",{}).get(paid_id) != "0.0007"
            or ledger.reservations[paid_id].cost_usd != Decimal("0.0007")
            or connection.execute("SELECT 1 FROM app_records WHERE record_key=?",("paid-result:"+paid_id,)).fetchone()):
            raise InputError("EXACT_UNCERTAIN_EXTRACTION_QUARANTINE_REQUIRED")
        audit = dict(version="UNKNOWN-QUARANTINE-1.0", operation_id=operation, paid_request_id=paid_id,
            scope=context["scope"], reason=reason, expected_versions=expected_versions,
            reviewer_role=actor.persona, reviewer_name="Demo Administrator", attribution="SIMULATED",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            provider_usage_status="UNKNOWN", provider_usage_reconciled=False,
            retained_reservation_usd="0.0007", replay_permitted=False,
            original_request_digest=request["request_digest"], admission_payload_digest=claim["payload_digest"])
        store._write(connection,RecordWrite(quarantine_key,"LIVE_QUARANTINE",audit,0))
        connection.execute("UPDATE app_operations SET state='RELEASED',active_execution_key=NULL WHERE operation_id=?",(operation,))
    return audit


def close_known_invalid_demo(store, actor, operation):
    """Close a proved, settled demo failure; never release unknown paid usage."""
    context=store.get_record("live-context:"+operation)
    if context is None or actor.persona!="Administrator":
        raise InputError("ADMINISTRATOR_DEMO_RECOVERY_REQUIRED")
    context=context[1];_scope(actor,context["scope"])
    if context.get("verification_policy")!="DEMO_DRAFT":
        raise InputError("EXPLICIT_DEMO_CONTEXT_REQUIRED")
    pv,state=store.get_record("live-progress:"+operation)
    if state["status"]=="MODEL_OUTPUT_INVALID":return state
    stage=state.get("pending_stage")
    if stage not in ("extractor","synthesizer") or stage in state["artifacts"]:
        raise InputError("FAILED_DEMO_PROVIDER_STAGE_REQUIRED")
    paid_id=str(uuid5(UUID(operation),"paid:"+stage))
    paid=store.get_record("paid-result:"+paid_id)
    lv,data=store.get_record("ledger:"+context["scope"]["review_id"])
    ledger=Ledger.from_dict(data)
    allowance=store.get_record("paid-allowance:first-synthetic-010")
    node=operation+":node:"+stage
    if (paid is None or not paid[1].get("actual_provider_response")
        or paid[1]["response"]["status"] not in ("TRUNCATED","INVALID_OUTPUT")
        or any(type(paid[1]["response"].get(k)) is not int for k in ("prompt_tokens","completion_tokens"))
        or ledger.unknown or set(ledger.reservations)!={node}
        or allowance is None or paid_id in allowance[1]["reservations"]):
        raise InputError("KNOWN_SETTLED_DEMO_FAILURE_REQUIRED")
    with store.connection() as c:
        claims=c.execute("SELECT * FROM app_operations WHERE review_id=? AND state='RECOVERY_REQUIRED'",(context["scope"]["review_id"],)).fetchall()
    if len(claims)!=1:raise InputError("EXACT_FAILED_DEMO_CLAIM_REQUIRED")
    claim=claims[0]
    settled=ledger.settle(node,Usage(nodes=1))
    event=dict(sequence=len(state["events"])+1,run_id=context["scope"]["run_id"],stage=stage,event="model_output_rejected",timestamp=datetime.now(timezone.utc).isoformat(),reason="Settled invalid demo output retained; no memo or credit decision",provider_result_ref="paid-result:"+paid_id)
    updated={**state,"status":"MODEL_OUTPUT_INVALID","pending_stage":None,"ledger":settled.to_dict(),"events":state["events"]+[event]}
    with store.transaction() as c:
        store._write(c,RecordWrite("ledger:"+context["scope"]["review_id"],"BUDGET_LEDGER",settled.to_dict(),lv))
        store._write(c,RecordWrite("live-progress:"+operation,"LIVE_PROGRESS",updated,pv))
    store.reconcile_idle(Receipt(claim["operation_id"],claim["payload_digest"],claim["state"],False),evidence_ref=event["provider_result_ref"],administrator_authorized=True)
    return updated


def close_known_invalid_extraction(store,actor,operation):
    context=store.get_record("live-context:"+operation)
    if context is None:raise InputError("LIVE_CONTEXT_REQUIRED")
    context=context[1];_scope(actor,context["scope"])
    if actor.persona!="Administrator":raise InputError("ADMINISTRATOR_RECOVERY_REQUIRED")
    progress_version,state=store.get_record("live-progress:"+operation)
    if state["status"]=="MODEL_OUTPUT_INVALID":return state
    paid=store.get_record("paid-result:"+str(uuid5(UUID(operation),"paid:extractor")))
    with store.connection() as connection:
        claim=connection.execute("SELECT * FROM app_operations WHERE operation_id=?",(operation,)).fetchone()
    ledger_key="ledger:"+context["scope"]["review_id"]
    ledger_version,data=store.get_record(ledger_key);ledger=Ledger.from_dict(data)
    allowance=store.get_record("paid-allowance:first-synthetic-010")
    if (claim is None or claim["state"]!="RECOVERY_REQUIRED" or paid is None or paid[1]["response"]["status"]!="INVALID_OUTPUT"
        or paid[1]["response"]["prompt_tokens"] is None or paid[1]["response"]["completion_tokens"] is None
        or not paid[1].get("actual_provider_response") or "extractor" in state["artifacts"]
        or set(state["artifacts"])!={"pdf_input"} or ledger.unknown or allowance is None or allowance[1]["reservations"]):
        raise InputError("KNOWN_SETTLED_EXTRACTION_FAILURE_EVIDENCE_REQUIRED")
    reservation=operation+":node:extractor"
    if set(ledger.reservations)!={reservation}:raise InputError("EXACT_FAILED_NODE_RESERVATION_REQUIRED")
    settled=ledger.settle(reservation,Usage(nodes=1))
    event=dict(sequence=len(state["events"])+1,run_id=context["scope"]["run_id"],stage="extractor",event="model_output_rejected",timestamp=datetime.now(timezone.utc).isoformat(),reason="Strict extraction schema rejected the original provider output; no facts admitted",provider_result_ref="paid-result:"+str(uuid5(UUID(operation),"paid:extractor")))
    updated={**state,"status":"MODEL_OUTPUT_INVALID","pending_stage":None,"ledger":settled.to_dict(),"events":state["events"]+[event]}
    with store.transaction() as connection:
        store._write(connection,RecordWrite(ledger_key,"BUDGET_LEDGER",settled.to_dict(),ledger_version))
        store._write(connection,RecordWrite("live-progress:"+operation,"LIVE_PROGRESS",updated,progress_version))
    receipt=Receipt(operation,claim["payload_digest"],claim["state"],False)
    store.reconcile_idle(receipt,evidence_ref=event["provider_result_ref"],administrator_authorized=True)
    return updated
