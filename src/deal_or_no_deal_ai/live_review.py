"""Scoped immutable Live FACT/CLAIM support; metadata commands never run a graph."""
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import UUID

from pydantic import Field
from .contracts import StrictModel, Identifier, Text
from .context import InputError, fingerprint
from .configuration import load_configuration
from .storage import Store, RecordWrite
from .command_center import _scope

CHECKS = ("reference", "value", "units_scale", "period", "subject_facility", "qualifications", "meaning")
FACT_CHECKS = ("reference", "row_label", "value", "units_scale", "period", "subject_facility", "debt_service_scope")


def required_checks(stage):
    return FACT_CHECKS if stage=="fact_review" else CHECKS

class Assessment(StrictModel):
    operation_id: Identifier
    request_digest: Text
    target_id: Text
    target_digest: Text
    domain: Literal["FINANCIAL_RISK", "POLICY_CONTROL"]
    status: Literal["HUMAN_SUPPORTED", "UNSUPPORTED", "WITHHELD"]
    quotes: dict[str, Text] = Field(min_length=1, max_length=64)
    checks: list[Text] = Field(max_length=7)
    comments: Text


def request_key(run_id, stage):
    return "live-review:" + run_id + ":" + stage


def support_key(request, target, domain):
    return "live-support:" + fingerprint("LIVE_SUPPORT_KEY", dict(request=request["digest"], target=target, domain=domain))


def assessment_progress(store,request):
    """Read-only progress; supported() remains the authoritative continuation gate."""
    verify_request(request)
    rows=[]
    for target in request['targets']:
        for domain in target['domains']:
            saved=store.get_record(support_key(request,target['id'],domain))
            status=saved[1]['command']['status'] if saved else 'NOT_RECORDED'
            rows.append(dict(item=target['label'],role='RiskManager' if domain=='FINANCIAL_RISK' else 'ComplianceOfficer',status=status))
    return dict(required=len(rows),recorded=sum(r['status']!='NOT_RECORDED' for r in rows),
        supported=sum(r['status']=='HUMAN_SUPPORTED' for r in rows),remaining=[r for r in rows if r['status']!='HUMAN_SUPPORTED'])


def verify_request(request):
    if request["digest"] != fingerprint("LIVE_REVIEW_REQUEST", {k:v for k,v in request.items() if k != "digest"}):
        raise InputError("LIVE_REVIEW_REQUEST_CHANGED")


def supported(store, request):
    verify_request(request)
    receipts = []
    for target in request["targets"]:
        for domain in target["domains"]:
            saved = store.get_record(support_key(request, target["id"], domain))
            if saved is None:
                raise InputError("LIVE_EVIDENCE_REVIEW_INCOMPLETE")
            item = saved[1]
            command = Assessment.model_validate(item["command"])
            if (command.request_digest != request["digest"] or command.target_digest != target["digest"]
                    or command.status != "HUMAN_SUPPORTED" or command.target_id != target["id"] or command.domain != domain):
                raise InputError("LIVE_EVIDENCE_NOT_SUPPORTED")
            if item.get("scope")!=request["scope"] or item.get("reviewer_role")!={"FINANCIAL_RISK":"RiskManager","POLICY_CONTROL":"ComplianceOfficer"}[domain] or set(command.checks)!=set(required_checks(request["stage"])) or len(command.checks)!=len(required_checks(request["stage"])) or set(command.quotes)!=set(target["source_refs"]):
                raise InputError("LIVE_SUPPORT_RECEIPT_CHANGED")
            if any(quote not in request["sources"].get(ref,"") for ref,quote in command.quotes.items()):
                raise InputError("LIVE_SUPPORT_QUOTE_CHANGED")
            receipts.append(item)
    return fingerprint("LIVE_SUPPORT_RECEIPTS", receipts)


def assess(root, actor, run_id, stage, command: Assessment):
    if stage not in ("fact_review", "evidence_review"):
        raise InputError("LIVE_SUPPORT_STAGE_REQUIRED")
    store = Store(load_configuration(Path(root)).database)
    saved = store.get_record(request_key(run_id, stage))
    if saved is None:
        raise InputError("LIVE_REVIEW_UNAVAILABLE")
    request = saved[1]; verify_request(request); _scope(actor, request["scope"])
    from .live_context import prepare_live_tasks
    from .services import load_registered_case
    context=store.get_record('live-context:'+request['operation_id'])[1]
    from .upload_live import case_for_context
    base=case_for_context(Path(root),actor,context)
    tasks=prepare_live_tasks(root,case=base) if context.get('upload_origin') else prepare_live_tasks(root)
    binding=fingerprint("LIVE_SOURCE_AND_PROMPTS",dict(case=base.dependency_digest,instructions={k:v["instruction"] for k,v in tasks.items()},schemas={k:v["schema"] for k,v in tasks.items()},**({'verification_policy':'DEMO_DRAFT'} if context.get('verification_policy')=='DEMO_DRAFT' else {})))
    if binding!=request["source_binding"]:
        raise InputError("LIVE_SUPPORT_SOURCE_OR_PROMPT_CHANGED")
    expected_role = {"FINANCIAL_RISK":"RiskManager", "POLICY_CONTROL":"ComplianceOfficer"}[command.domain]
    if actor.persona != expected_role or request["digest"] != command.request_digest:
        raise InputError("LIVE_SUPPORT_ROLE_OR_VERSION_MISMATCH")
    target = next((t for t in request["targets"] if t["id"] == command.target_id), None)
    if target is None or target["digest"] != command.target_digest or command.domain not in target["domains"]:
        raise InputError("LIVE_SUPPORT_TARGET_CHANGED")
    if len(command.checks) != len(set(command.checks)) or not set(command.checks) <= set(required_checks(stage)):
        raise InputError("LIVE_SUPPORT_CHECKS_INVALID")
    if command.status == "HUMAN_SUPPORTED" and set(command.checks) != set(required_checks(stage)):
        raise InputError("LIVE_SUPPORT_ALL_CHECKS_REQUIRED")
    for ref, quote in command.quotes.items():
        if ref not in target["source_refs"] or quote not in request["sources"].get(ref, ""):
            raise InputError("LIVE_SUPPORT_QUOTE_OUT_OF_SCOPE")
    if command.status == "HUMAN_SUPPORTED" and set(command.quotes) != set(target["source_refs"]):
        raise InputError("LIVE_SUPPORT_ALL_SOURCES_REQUIRED")
    key = support_key(request, target["id"], command.domain)
    existing = store.get_record(key)
    if existing:
        if existing[1]["command"] == command.model_dump():
            return existing[1]
        raise InputError("LIVE_SUPPORT_ALREADY_RECORDED")
    progress = store.get_record("live-progress:" + request["operation_id"])
    if progress is None or progress[1]["pending_stage"] != stage or progress[1]["status"] != "WAITING_EVIDENCE":
        raise InputError("LIVE_SUPPORT_NOT_CURRENT_PAUSE")
    event = dict(command=command.model_dump(), scope=request["scope"], reviewer_role=actor.persona,
                 reviewer_name="Demo " + actor.persona, timestamp_utc=datetime.now(timezone.utc).isoformat())
    receipt = store.admit(command.operation_id, request["scope"], dict(action="LIVE_SUPPORT", command=command.model_dump()),
        writes=(RecordWrite(key,"LIVE_SUPPORT", event,0),))
    if not receipt.duplicate:
        store.release(receipt, confirmed_idle=True)
    return event
