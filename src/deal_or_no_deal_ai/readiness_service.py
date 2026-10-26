"""Scoped readiness snapshots and human evaluations in the existing local database."""
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from typing import Literal
from pydantic import Field
from .context import InputError, fingerprint, primitive
from .contracts import StrictModel, Identifier, Text, parse_synthesis, parse_extraction
from .readiness import CovenantEvaluation, EvaluatedRequirement, ApprovalReadiness, evaluate_approval_readiness
from .storage import Store, RecordWrite, StaleRecord, OperationConflict

CORE=("pdf_input","extractor","fact_review","financial_analyst","compliance_check","risk_quantifier","synthesizer","evidence_review")


def key(run_id):
    return "readiness-current:"+run_id


def basis(context,artifacts):
    return fingerprint("READINESS_ANALYSIS",dict(scope=context["scope"],source=context.get("source_binding",context.get("case_dependency_digest")),artifacts={n:artifacts[n] for n in CORE if n in artifacts}))


def proposal(artifacts,mode):
    synth=artifacts.get("synthesizer",{}).get("payload")
    if not synth:
        return None
    wire=parse_synthesis(synth["wire_json"])
    return dict(decision=wire.panel_decision.decision,rationale=wire.panel_decision.rationale,original_wire_json=synth["wire_json"],mode=mode,parent_digest=fingerprint("ORIGINAL_AI_PROPOSAL",synth))


def covenants_from(artifacts):
    extraction=artifacts.get("extractor",{}).get("payload",{})
    wire=parse_extraction(extraction["wire_json"]) if "wire_json" in extraction else None
    terms=wire.model_dump()["terms"] if wire else extraction.get("wire",{}).get("terms",{})
    value=terms.get("covenants",{})
    return terms,value


def _review(store,run_id,part,analysis):
    if store is None or not store.path.exists():
        return None
    saved=store.get_record("readiness-review:"+run_id+":"+part)
    if saved is None:
        return None
    event=saved[1]
    if event["analysis_digest"]!=analysis:
        return dict(stale=True)
    if event["digest"]!=fingerprint("READINESS_REVIEW_EVENT",{k:v for k,v in event.items() if k!="digest"}):
        raise InputError("READINESS_REVIEW_CHANGED")
    return event


def inputs(context,artifacts,store=None,recovery=False):
    analysis=basis(context,artifacts);run_id=context["scope"]["run_id"]
    terms,cov=covenants_from(artifacts)
    financial=artifacts.get("financial_analyst",{}).get("payload",{})
    synth=artifacts.get("synthesizer",{}).get("payload",{})
    policy=synth.get("routing",{}).get("final_policy",artifacts.get("compliance_check",{}).get("payload",{}))
    if context.get("mode")=="LIVE" and "route_review" in artifacts:
        policy=artifacts["route_review"]["payload"].get("final_policy",policy)
    review_as_of=financial.get("review_source_basis",{}).get("review_as_of")
    if not review_as_of:
        review_as_of=context.get("readiness_review_as_of") or context["generation_time"][:10]
    covenants=[]
    for i,clause in enumerate(cov.get("value") or []):
        cid=fingerprint("COVENANT_ID",dict(index=i,clause=clause,refs=cov.get("refs",[])))
        assessment=_review(store,run_id,"covenant:"+cid,analysis)
        if assessment and not assessment.get("stale"):
            c=CovenantEvaluation.model_validate(assessment["command"]["covenant"])
        else:
            c=CovenantEvaluation(covenant_id=cid,clause=clause,evidence_refs=cov.get("refs",[]),evidence_status="STALE" if assessment else "PENDING",reason="Contractual timing and requirements have not been evaluated")
        covenants.append(c)
    def requirement(identifier,label,status,reason,refs,action):
        return EvaluatedRequirement(requirement_id=identifier,label=label,status=status,reason=reason,evidence_refs=sorted(set(refs)),next_action=action)
    required_metrics={"CALC-004","CALC-005","CALC-006"}
    metrics={m["metric_id"]:m for m in financial.get("metric_results",[])}
    missing=financial.get("missing_dependencies",[])
    usable=financial.get("completeness")=="COMPLETE" and all(metrics.get(m,{}).get("validity")=="VALID" for m in required_metrics)
    req=[requirement("covenant_coverage","Covenant inventory", "SATISFIED" if cov.get("value") is not None and cov.get("refs") else "PENDING","Covenants extracted; each mandatory clause still requires evaluation" if cov.get("value") is not None else "Covenant coverage has not been established",cov.get("refs",[]),"Review the complete contractual covenant inventory.")]
    req.append(requirement("financial","Mandatory financial calculations","SATISFIED" if usable else "MISSING" if missing else "PENDING","Required annual calculations are usable" if usable else "Required financial calculations or inputs are incomplete",[r for _,refs in financial.get("metric_source_refs",[]) for r in refs],"Supply and verify missing financial inputs and recalculate affected findings."))
    rules=policy.get("rules",[])
    unknown=any(r["evaluation_state"] in ("UNKNOWN","NOT_EVALUATED") or r["applicability"]=="UNKNOWN" for r in rules)
    exceptions=[r for r in rules if r.get("outcome")=="Exception" or r.get("workflow") in ("ESCALATE","BLOCKED")]
    req.append(requirement("policy","Applicable policy requirements","PENDING" if not rules or unknown else "EXCEPTION" if exceptions else "SATISFIED","Applicable policy evaluation is incomplete" if not rules or unknown else "Policy exceptions require explicit review" if exceptions else "Applicable sample policy checks evaluated",[r for rule in rules for r in rule.get("source_refs",[])],"Evaluate or disposition applicable policy requirements; preserve the original exceptions."))
    req.append(requirement("critical_exceptions","Unresolved critical exceptions","EXCEPTION" if exceptions else "SATISFIED" if rules else "PENDING","Unresolved policy or control exceptions prevent approval eligibility" if exceptions else "No unresolved critical exception is recorded" if rules else "Critical exception review is incomplete",[r for rule in exceptions for r in rule.get("source_refs",[])],"Obtain the permitted specialist exception review; a policy breach is not an automatic rejection."))
    evidence_ready=context.get("mode")=="LIVE" and all(artifacts.get(s,{}).get("payload",{}).get("human_supported") is True for s in ("fact_review","evidence_review"))
    reviews=[_review(store,run_id,"evidence:"+d,analysis) for d in ("FINANCIAL_RISK","POLICY_CONTROL")]
    verified=all(r and not r.get("stale") and r["command"]["status"]=="VERIFIED" for r in reviews)
    evidence_refs=list(dict.fromkeys(r for group in terms.values() for r in group.get("refs",[])))
    req.append(requirement("evidence","Current evidence verification","SATISFIED" if evidence_ready or verified else "STALE" if any(r and r.get("stale") for r in reviews) else "PENDING","Current financial and policy evidence review recorded" if evidence_ready or verified else "Saved response matching is not human evidence verification",evidence_refs,"Verify the current critical facts and conclusions against their source evidence."))
    if recovery:
        req.append(requirement("recovery","Execution integrity","RECOVERY","Execution or stored evidence requires technical recovery",[],"Resolve the technical recovery before any financial decision."))
    if context.get('upload_origin',{}).get('profile')=='USER_DECLARED_UPLOAD-1.0':
        risk=artifacts.get('risk_quantifier',{}).get('payload',{}).get('score',{})
        req.append(requirement('risk_assessment','Source-supported credit risk assessment','SATISFIED' if risk.get('total') is not None and not risk.get('missing') else 'MISSING','No approved borrower factor assessments were supplied' if risk.get('total') is None else 'Credit risk inputs evaluated',[], 'Supply and verify borrower-specific risk assessments; never substitute the sample score.'))
    return dict(scope=context["scope"],analysis_digest=analysis,review_as_of=review_as_of,requirements=req,covenants=covenants)


def assess_current(store,context,artifacts,receipt=None,recovery=False):
    """Persist only under an existing admitted command; no writes on projection."""
    if receipt is not None:
        store.assert_claim(receipt)
    data=inputs(context,artifacts,store,recovery)
    current=store.get_record(key(context["scope"]["run_id"])) if store.path.exists() else None
    old=ApprovalReadiness.model_validate(current[1]) if current else None
    signature=lambda a:fingerprint("READINESS_CONTENT",dict(analysis=a.analysis_digest,requirements=[r.model_dump() for r in a.evaluated_requirements],covenants=[c.model_dump() for c in a.covenants],review_as_of=a.review_as_of))
    assessment=evaluate_approval_readiness(**data,version=old.version+1 if old else 1,evaluated_at_utc=datetime.now(timezone.utc).isoformat(),previous_assessment_id=old.assessment_id if old else None)
    if old and signature(old)==signature(assessment):
        return old
    if receipt is None:
        # Safe current projection, explicitly not a newly persisted assessment.
        return evaluate_approval_readiness(**data,version=0,evaluated_at_utc=None)
    with store.transaction() as connection:
        store._write(connection,RecordWrite("readiness-assessment:"+assessment.assessment_id,"READINESS_ASSESSMENT",assessment.model_dump(),0))
        store._write(connection,RecordWrite(key(context["scope"]["run_id"]),"APPROVAL_READINESS",assessment.model_dump(),current[0] if current else 0))
    return assessment


def projection(store,run):
    assessment=assess_current(store,run["context"],run["artifacts"],recovery=run.get("status")=="RECOVERY_REQUIRED")
    human=store.get_record("readiness-human:"+run["context"]["scope"]["run_id"]) if store.path.exists() else None
    decision=human[1] if human else run.get("outcome",{}).get("human_decision") or run.get("human_disposition")
    return dict(ai_proposal=proposal(run["artifacts"],run["context"]["mode"]),approval_readiness=assessment.model_dump(),human_decision=decision,human_disposition=decision.get("decision") if isinstance(decision,dict) else decision)


def require_approval(store,run,expected_version=None,expected_digest=None):
    if expected_version is None or expected_digest is None:
        raise InputError("LATEST_READINESS_VERSION_REQUIRED")
    current=store.get_record(key(run["context"]["scope"]["run_id"]))
    if current is None:
        raise InputError("CURRENT_APPROVAL_READINESS_REQUIRED")
    assessment=ApprovalReadiness.model_validate(current[1])
    checked=assess_current(store,run["context"],run["artifacts"],recovery=run.get("status")=="RECOVERY_REQUIRED")
    if assessment.assessment_digest!=checked.assessment_digest or not assessment.approval_eligible:
        raise InputError("APPROVAL_READINESS_BLOCKED")
    if expected_version is not None and (expected_version!=assessment.version or expected_digest!=assessment.assessment_digest):
        raise StaleRecord("STALE_APPROVAL_READINESS")
    return current


class ReadinessReviewCommand(StrictModel):
    operation_id: Identifier
    expected_version: int = Field(ge=0)
    expected_analysis: Text
    part: Literal["COVENANT", "EVIDENCE"]
    covenant: CovenantEvaluation | None = None
    domain: Literal["FINANCIAL_RISK", "POLICY_CONTROL"] | None = None
    status: Literal["VERIFIED", "PENDING"] = "PENDING"
    checked_targets: list[Text] = Field(default_factory=list,max_length=128)
    checks: list[Text] = Field(default_factory=list,max_length=8)
    quotes: dict[str,Text] = Field(min_length=1,max_length=64)
    comments: Text

CHECKS=("reference","value","units_scale","period","subject_facility","qualifications","meaning")


def evidence_targets(artifacts,domain):
    terms,cov=covenants_from(artifacts)
    extraction=artifacts.get("extractor",{}).get("payload",{})
    wire=parse_extraction(extraction["wire_json"]).model_dump() if "wire_json" in extraction else extraction.get("wire",{})
    targets=[]
    if domain=="FINANCIAL_RISK":
        targets=[group+"."+n for group in ("terms","financial_inputs") for n,f in wire.get(group,{}).items() if f.get("value") is not None]
        targets+= ["risk."+f["factor_id"] for f in artifacts.get("risk_quantifier",{}).get("payload",{}).get("score",{}).get("factors",[])]
    synth=artifacts.get("synthesizer",{}).get("payload")
    if synth:
        s=parse_synthesis(synth["wire_json"])
        targets+=["observations["+str(i)+"]" for i in range(len(s.observations))]+["rationale"]+["condition["+str(i)+"]" for i in range(len(s.panel_decision.conditions))]
        if s.proposed_action:
            targets.append("proposed_action")
    if domain=="POLICY_CONTROL":
        policy=artifacts.get('route_review',{}).get('payload',{}).get('final_policy',synth.get('routing',{}).get('final_policy',{}) if synth else {})
        targets+=["policy."+r["rule_id"] for r in policy.get('rules',[])]
    return targets


def record_review(root,actor,operation,command):
    """Source-bound metadata evaluation; never a model call or credit decision."""
    from .command_center import get_run,source_packet
    from .configuration import load_configuration
    config=load_configuration(Path(root));store=Store(config.database)
    run=get_run(store,actor,operation)
    payload=fingerprint("READINESS_REVIEW_COMMAND",dict(command=command.model_dump(),actor=primitive(asdict(actor)),run=operation))
    previous=store.get_record("readiness-review-event:"+command.operation_id)
    if previous:
        if previous[1]["command_digest"]!=payload:
            raise OperationConflict("READINESS_REVIEW_COMMAND_CONFLICT")
        return previous[1]
    human=store.get_record('readiness-human:'+run['context']['scope']['run_id'])
    if run['context'].get('upload_origin') and human and human[1].get('decision') in ('Approve','Reject'):
        raise InputError('FINAL_UPLOADED_REVIEW_ALREADY_RECORDED')
    if not command.comments.strip():
        raise InputError("REVIEW_COMMENTS_REQUIRED")
    current=assess_current(store,run["context"],run["artifacts"])
    if current.version!=command.expected_version or current.analysis_digest!=command.expected_analysis:
        raise StaleRecord("STALE_READINESS_REVIEW")
    packet=source_packet(config.workspace,run)
    pointer=store.get_record(key(run["context"]["scope"]["run_id"]))
    sources={r:v["text"] for r,v in packet["request"]["reference_dictionary"].items() if v["kind"]=="SOURCE"}
    if any(ref not in sources or quote not in sources[ref] for ref,quote in command.quotes.items()):
        raise InputError("READINESS_QUOTE_OUT_OF_SCOPE")
    if command.part=="COVENANT":
        if actor.persona!="ComplianceOfficer" or command.covenant is None:
            raise InputError("COVENANT_REVIEW_PERMISSION_REQUIRED")
        cov=next((c for c in current.covenants if c.covenant_id==command.covenant.covenant_id),None)
        if cov is None or cov.clause!=command.covenant.clause or not command.covenant.mandatory or not set(command.covenant.evidence_refs)<=set(command.quotes):
            raise InputError("COVENANT_SOURCE_BINDING_REQUIRED")
        if command.covenant.due_date and not any(command.covenant.due_date in q for q in command.quotes.values()):
            raise InputError("EXPLICIT_CONTRACTUAL_DUE_DATE_EVIDENCE_REQUIRED")
        part="covenant:"+cov.covenant_id
    else:
        if command.domain is None or actor.persona!={"FINANCIAL_RISK":"RiskManager","POLICY_CONTROL":"ComplianceOfficer"}[command.domain]:
            raise InputError("READINESS_EVIDENCE_PERMISSION_REQUIRED")
        if command.status=="VERIFIED" and (set(command.checked_targets)!=set(evidence_targets(run["artifacts"],command.domain)) or len(command.checked_targets)!=len(set(command.checked_targets)) or set(command.checks)!=set(CHECKS) or len(command.checks)!=len(CHECKS) or set(command.quotes)!=set(sources)):
            raise InputError("ALL_CURRENT_TARGETS_CHECKS_AND_SOURCES_REQUIRED")
        part="evidence:"+command.domain
    event=dict(command=command.model_dump(),command_digest=payload,analysis_digest=current.analysis_digest,scope=run["context"]["scope"],run_operation=operation,reviewer_role=actor.persona,reviewer_name="Simulated "+actor.persona,timestamp_utc=datetime.now(timezone.utc).isoformat())
    event["digest"]=fingerprint("READINESS_REVIEW_EVENT",event)
    existing=store.get_record("readiness-review:"+run["context"]["scope"]["run_id"]+":"+part)
    receipt=store.admit(command.operation_id,run["context"]["scope"],dict(action="READINESS_REVIEW",digest=payload),writes=(RecordWrite("readiness-review-event:"+command.operation_id,"READINESS_REVIEW_EVENT",event,0),RecordWrite("readiness-review:"+run["context"]["scope"]["run_id"]+":"+part,"READINESS_REVIEW",event,existing[0] if existing else 0)),expected_records=((key(run["context"]["scope"]["run_id"]),pointer[0] if pointer else 0),))
    if receipt.duplicate:
        return event
    try:
        assess_current(store,run["context"],run["artifacts"],receipt)
        store.release(receipt,confirmed_idle=True)
    except BaseException:
        store.mark_unknown(receipt);raise
    return event


class HumanReadinessDecision(StrictModel):
    operation_id: Identifier
    expected_version: int = Field(ge=1)
    expected_digest: Text
    expected_analysis: Text
    decision: Literal["Approve"]
    comments: Text


def record_ready_decision(root,actor,operation,command):
    """Default completed analysis may receive an explicit human decision; no rerun."""
    from .command_center import get_run,source_packet
    from .configuration import load_configuration
    config=load_configuration(Path(root));store=Store(config.database);run=get_run(store,actor,operation)
    if actor.persona!="AuthorizedApprover" or "NORMAL" not in actor.allowed_review_tiers or run["context"].get("variant")!="default" or run["status"]!="COMPLETED":
        raise InputError("AUTHORIZED_CURRENT_DEFAULT_DECISION_REQUIRED")
    digest=fingerprint("READY_HUMAN_COMMAND",dict(command=command.model_dump(),actor=primitive(asdict(actor)),operation=operation))
    prior=store.get_record("readiness-decision-event:"+command.operation_id)
    if prior:
        if prior[1]["command_digest"]!=digest:
            raise OperationConflict("DECISION_COMMAND_CONFLICT")
        return prior[1]
    if not command.comments.strip():
        raise InputError("DECISION_COMMENTS_REQUIRED")
    source_packet(config.workspace,run)
    pointer=require_approval(store,run,command.expected_version,command.expected_digest)
    if pointer[1]["analysis_digest"]!=command.expected_analysis:
        raise StaleRecord("STALE_DECISION_ANALYSIS")
    human_key="readiness-human:"+run["context"]["scope"]["run_id"]
    if store.get_record(human_key):
        raise InputError("HUMAN_DECISION_ALREADY_RECORDED")
    from .financial_review import event_deal_snapshot
    event=dict(operation_id=command.operation_id,scope=run["context"]["scope"],run_operation=operation,command_digest=digest,decision=command.decision,comments=command.comments,reviewer_role=actor.persona,reviewer_name="Simulated "+actor.persona,reviewer_tier="NORMAL",timestamp_utc=datetime.now(timezone.utc).isoformat(),ai_proposal=run["ai_proposal"],approval_readiness=pointer[1],analysis_digest=command.expected_analysis,action="APPROVE",previous_status="AWAITING_DECISION",new_status="APPROVED",requested_items=[],provenance="EXECUTED_FIXTURE_REVIEW",analysis_snapshot=dict(deal=event_deal_snapshot(run),ai=run["artifacts"]["synthesizer"]["payload"],risk=run["artifacts"]["risk_quantifier"]["payload"],compliance=run["artifacts"]["synthesizer"]["payload"]["routing"]["final_policy"],source_dependency=run["context"]["case_dependency_digest"]))
    receipt=store.admit(command.operation_id,run["context"]["scope"],dict(action="READY_HUMAN_DECISION",digest=digest),writes=(RecordWrite(human_key,"READINESS_HUMAN_DECISION",event,0),RecordWrite("readiness-decision-event:"+command.operation_id,"READINESS_DECISION_EVENT",event,0),RecordWrite("financial-review-event:"+command.operation_id,"FINANCIAL_REVIEW_EVENT",event,0)),expected_records=((key(run["context"]["scope"]["run_id"]),pointer[0]),))
    if not receipt.duplicate:
        store.release(receipt,confirmed_idle=True)
    return event
