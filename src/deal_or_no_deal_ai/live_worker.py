"""LIVE-GRAPH-1.0: shared LangGraph/domain services, explicit provider and support pauses."""
from contextlib import closing
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import os
import time
import tomllib
from decimal import Decimal
from uuid import UUID, uuid5

from .budgets import Ledger, Usage
from .command_center import _scope, workspace_id
from .configuration import load_configuration
from .context import InputError, fingerprint, primitive
from .contracts import Scope, hydrate_narrative, parse_extraction, parse_synthesis, wire_json
from .graph import STAGES, TOOL_STAGES, build_graph
from .live_context import prepare_live_tasks, live_synthesis_task
from .live_review import request_key, support_key, supported
from .nebius_transport import dispatch_generation
from .panel_codec import restore_compliance, restore_financial, restore_risk
from .policy import PolicyConfig, evaluate_policy, aggregate_workflow
from .services import (load_registered_case, ReviewedLiveCase, _binding, _validate_inputs,
                       compute_financials, compute_compliance, compute_risk)
from .storage import Store, RecordWrite
from .synthesis import prepare_synthesis

LIVE_ORDER = STAGES[:2] + ("fact_review",) + STAGES[2:]

def now():
    return datetime.now(timezone.utc).isoformat()


def verification_policy(root):
    with (Path(root)/"config/app.toml").open("rb") as stream:
        policy=tomllib.load(stream).get("live_verification_policy","HUMAN_REQUIRED")
    if policy not in ("HUMAN_REQUIRED","DEMO_DRAFT"):
        raise InputError("LIVE_VERIFICATION_POLICY_NOT_APPROVED")
    return policy

def packet_tokens(root, task, *, stage="extractor"):
    """Only exact, separately verified whole-request counts; never a local heuristic."""
    with (Path(root)/"config/live_smoke.toml").open("rb") as stream:
        profile = tomllib.load(stream)
    if profile.get("provider_contract_verified") is not True:
        raise InputError("VERIFIED_PROVIDER_CONTRACT_REQUIRED")
    if profile.get("token_count_strategy") != "PROVIDER_VERIFIED_WHOLE_REQUEST":
        raise InputError("VERIFIED_FULL_REQUEST_TOKEN_ACCOUNTING_REQUIRED")
    from .provider import MODELS, prepare_request
    if profile.get("generation_model")!=MODELS[0] or profile.get("total_allowance_usd")!="0.10" or profile.get("prompt_profile")!="LIVE-COMPACT-1.0":
        raise InputError("LIVE_APPROVED_PROFILE_REQUIRED")
    try:
        rates=[Decimal(profile[k]) for k in ("input_usd_per_million","output_usd_per_million")]
    except (KeyError, ValueError, TypeError):
        raise InputError("VERIFIED_POSITIVE_PROVIDER_RATES_REQUIRED") from None
    if not profile.get("rates_verified_on") or any(not r.is_finite() or r<=0 for r in rates):
        raise InputError("VERIFIED_POSITIVE_PROVIDER_RATES_REQUIRED")
    count = profile.get("verified_packet_tokens", {}).get(fingerprint("LIVE_PACKET", task))
    if type(count) is not int or count <= 0:
        raise InputError("EXACT_LIVE_PACKET_TOKEN_VERIFICATION_REQUIRED")
    from .provider import LIVE_STAGE_CAPS
    payload=prepare_request(model_id=MODELS[0],stage=stage,instruction=task["instruction"],context=task["context"],verified_input_tokens=count,max_output_tokens=LIVE_STAGE_CAPS[stage][1],profile="LIVE-COMPACT-1.0")
    if payload["response_format"]["json_schema"]["schema"]!=task["schema"]:
        raise InputError("LIVE_REQUEST_SCHEMA_CHANGED")
    return count


def load_live(root, actor, operation):
    UUID(operation)
    config = load_configuration(Path(root)); store = Store(config.database)
    if not store.path.exists():
        raise InputError("LIVE_REVIEW_UNAVAILABLE")
    context = store.get_record("live-context:"+operation)
    progress = store.get_record("live-progress:"+operation)
    if context is None or progress is None:
        raise InputError("LIVE_REVIEW_UNAVAILABLE")
    _scope(actor, context[1]["scope"])
    state = progress[1]
    if state["context"] != context[1]:
        raise InputError("LIVE_CONTEXT_CHANGED")
    if context[1].get("upload_origin"):
        from .upload_live import case_for_context
        try:
            case_for_context(root,actor,context[1])
        except (InputError,ValueError,OSError):
            # Keep the scoped historical review visible without substituting sources.
            state={**state,"status":"RECOVERY_REQUIRED","source_validation_failed":True}
    with store.connection() as connection:
        active = connection.execute("SELECT state FROM app_operations WHERE review_id=? AND state!='RELEASED'", (context[1]["scope"]["review_id"],)).fetchall()
    if active:
        state = {**state, "status":"RECOVERY_REQUIRED" if any(r[0]=="RECOVERY_REQUIRED" for r in active) else "RUNNING"}
    quarantine = store.get_record("quarantine-review:" + context[1]["scope"]["review_id"])
    if quarantine:
        state = {**state, "status":"RECOVERY_REQUIRED", "quarantine":quarantine[1]}
    return state


def list_live(root, actor):
    store = Store(load_configuration(Path(root)).database)
    if not store.path.exists():
        return []
    with store.connection() as connection:
        if not connection.execute("SELECT 1 FROM sqlite_master WHERE name='app_records'").fetchone():
            return []
        operations = [r[0].split(":",1)[1] for r in connection.execute("SELECT record_key FROM app_records WHERE kind='LIVE_CONTEXT'")]
    result=[]
    for operation in operations:
        try:
            result.append(load_live(root,actor,operation))
        except InputError:
            continue
    return sorted(result,key=lambda s:s["context"]["generation_time"],reverse=True)


def _live_case(base, state, store):
    request = store.get_record(request_key(state["context"]["scope"]["run_id"],"fact_review"))[1]
    demo=state["context"].get("verification_policy")=="DEMO_DRAFT"
    support = fingerprint("DEMO_SOURCE_INTEGRITY",request) if demo else supported(store,request)
    wire = parse_extraction(state["artifacts"]["extractor"]["payload"]["wire_json"])
    _validate_inputs(base.registration,base.scope,wire,base.case_data,base.inventory,registered_extraction=False)
    digest = fingerprint("REVIEWED_LIVE_CASE",dict(inputs=_binding(base.registration,base.scope,wire,base.case_data,base.inventory),support=support,
        **({"verification_policy":"DEMO_DRAFT"} if demo else {})))
    return ReviewedLiveCase(base.registration,base.scope,wire,base.case_data,base.inventory,digest,support,not demo)


def _request(base, state, stage, packet=None):
    sources={b.block_id:b.text for b in base.inventory}
    if stage=="fact_review":
        wire=parse_extraction(state["artifacts"]["extractor"]["payload"]["wire_json"])
        targets=[]
        for group in ("terms","financial_inputs"):
            for name,fact in getattr(wire,group).__dict__.items():
                if fact.value is not None:
                    targets.append(dict(label=name.replace("_"," ").capitalize(),id=group+"."+name,text=primitive(fact.model_dump()),source_refs=fact.refs,domains=["FINANCIAL_RISK"]))
        for factor in base.case_data["factor_assessments"]:
            targets.append(dict(label="Scoring premise: "+factor["factor_id"].replace("_"," "),id="assessment:"+factor["factor_id"],text=factor,source_refs=sorted(set(factor["refs"]+factor["material_source_refs"])),domains=["FINANCIAL_RISK"]))
    else:
        wire=parse_synthesis(state["artifacts"]["synthesizer"]["payload"]["wire_json"])
        scope=Scope.model_validate(state["context"]["scope"])
        refs=packet["request"]["reference_dictionary"]
        hydrated=hydrate_narrative(wire,scope,state["context"]["operation_id"],{k:scope for k in refs},dict(input_digest=packet["input_digest"],case=packet["case_dependency_digest"]))
        texts={"observations["+str(i)+"].text":o.text for i,o in enumerate(wire.observations)}
        texts["panel_decision.rationale"]=wire.panel_decision.rationale
        texts.update({"panel_decision.conditions["+str(i)+"]":v for i,v in enumerate(wire.panel_decision.conditions)})
        if wire.proposed_action:
            texts["proposed_action.reason"]=wire.proposed_action.reason
        def leaves(ref,ancestors=()):
            if ref not in refs or ref in ancestors:
                raise InputError("LIVE_REFERENCE_MISSING_OR_CYCLIC")
            if refs[ref]["kind"]=="SOURCE":
                return [ref]
            return [leaf for child in refs[ref]["refs"] for leaf in leaves(child,ancestors+(ref,))]
        targets=[]
        for target in hydrated:
            domains=["FINANCIAL_RISK","POLICY_CONTROL"]
            if target.field_path.startswith("observations["):
                index=int(target.field_path.split("[")[1].split("]")[0])
                # Panel labels are model output, not authority to reduce review.
                # This bounded live slice treats all narrative as potentially mixed.
            label=target.field_path
            if target.field_path.startswith("observations["):
                label=wire.observations[index].panel.title()+" finding"
            elif target.field_path=="panel_decision.rationale":
                label="Recommendation rationale"
            elif target.field_path.startswith("panel_decision.conditions["):
                label="Proposed condition"
            elif target.field_path=="proposed_action.reason":
                label="Suggested next step"
            targets.append(dict(label=label,id=target.claim_ref,field_path=target.field_path,text=texts[target.field_path],
                source_refs=sorted(set(leaf for ref in target.refs for leaf in leaves(ref))),domains=domains, refs=target.refs))
    if stage=='fact_review' and base.registration.version=='UPLOAD-PROFILE-1.0':
        targets.append(dict(label='Uploaded borrower, periods, units and policy applicability',id='upload_profile',text=dict(bases=base.case_data['bases'],subject=base.case_data['subject_registry'],policy=base.case_data['policy_config']),source_refs=list(sources),domains=['FINANCIAL_RISK','POLICY_CONTROL']))
    for target in targets:
        if not target["source_refs"] or not set(target["source_refs"])<=set(sources):
            raise InputError("LIVE_TARGET_SOURCE_MISSING")
        target["digest"]=fingerprint("LIVE_REVIEW_TARGET",target)
    request=dict(review_basis=dict(bases=base.case_data["bases"],review_as_of=base.registration.review_as_of,evidence_cutoff=base.registration.evidence_cutoff_at,subject=base.case_data["subject_registry"]),stage=stage,scope=state["context"]["scope"],operation_id=state["context"]["operation_id"],
        source_metadata={b.block_id:dict(page=b.page,source_version=b.source.version,source_sha256=b.source.content_digest) for b in base.inventory},source_binding=state["context"]["source_binding"],parent_digest=fingerprint("LIVE_REVIEW_PARENTS",state["artifacts"]),targets=targets,sources=sources)
    request["digest"]=fingerprint("LIVE_REVIEW_REQUEST",request)
    return request


def run_live(root, actor, operation_id, *, resume_operation_id=None, upload_operation_id=None):
    """Explicit start/continue only; two provider stages, no fallback or automatic resume."""
    root=Path(root); config=load_configuration(root); root=config.workspace
    if any(os.environ.get(k,"").strip().lower() not in ("","false","0","off","no") for k in ("LANGSMITH_TRACING","LANGCHAIN_TRACING","LANGCHAIN_TRACING_V2")):
        raise InputError("LIVE_HOSTED_TRACING_MUST_BE_DISABLED")
    if str(UUID(operation_id))!=operation_id or resume_operation_id and str(UUID(resume_operation_id))!=resume_operation_id:
        raise InputError("CANONICAL_OPERATION_UUID_REQUIRED")
    store=Store(config.database)
    prior=None if not store.path.exists() else store.get_record("live-context:"+operation_id)
    origin=None
    if prior and prior[1].get("upload_origin"):
        from .upload_live import case_for_context
        base=case_for_context(root,actor,prior[1]);origin=prior[1]["upload_origin"]
        if upload_operation_id and upload_operation_id!=origin["upload_operation_id"]:
            raise InputError("UPLOADED_REVIEW_IDENTITY_CHANGED")
    elif upload_operation_id:
        if prior:raise InputError("UPLOADED_REVIEW_IDENTITY_CHANGED")
        from .upload_live import load_uploaded_case,identities
        base,origin=load_uploaded_case(root,actor,upload_operation_id)
        if operation_id!=identities(upload_operation_id)["operation_id"]:
            raise InputError("UPLOADED_REVIEW_IDENTITY_CHANGED")
    else:
        base=load_registered_case(root)
    _scope(actor,dict(workspace_id=workspace_id(root),deal_id=base.scope.deal_id))
    if actor.persona!="Analyst":
        raise InputError("LIVE_ANALYST_COMMAND_REQUIRED")
    tasks=prepare_live_tasks(root,case=base) if origin else prepare_live_tasks(root)
    policy=prior[1].get("verification_policy","HUMAN_REQUIRED") if prior else verification_policy(root)
    general=base.registration.version=='UPLOAD-PROFILE-1.0'
    if general or origin and not prior:policy='HUMAN_REQUIRED'
    parallel=general or bool(origin) and (not prior or prior[1].get('parallel_specialists',False))
    demo=policy=="DEMO_DRAFT"
    source_binding=fingerprint("LIVE_SOURCE_AND_PROMPTS",dict(case=base.dependency_digest,instructions={k:v["instruction"] for k,v in tasks.items()},schemas={k:v["schema"] for k,v in tasks.items()},
        **({"verification_policy":"DEMO_DRAFT"} if demo else {})))
    command_id=resume_operation_id or operation_id
    if prior is None:
        if resume_operation_id:
            raise InputError("LIVE_PENDING_RUN_REQUIRED")
        try:packet_tokens(root,tasks['extractor'])
        except InputError as error:
            if not general or str(error)!='EXACT_LIVE_PACKET_TOKEN_VERIFICATION_REQUIRED':raise
            from .upload_profile import verify_new_task_tokens
            verify_new_task_tokens(root,tasks['extractor'],'extractor',actor.workspace_id)
        from .live_setup import read_api_key
        read_api_key(root)
        uid=lambda label:str(uuid5(UUID(operation_id),"live:"+label))
        scope=Scope(workspace_id=workspace_id(root),deal_id=base.scope.deal_id,review_id=uid("review"),run_id=uid("run"),thread_id=uid("thread"),input_revision=1)
        context=dict(scope=scope.model_dump(),operation_id=operation_id,mode="LIVE",scenario_id="E-N01",variant="live",generation_time=now(),source_binding=source_binding)
        if demo:
            context["verification_policy"]="DEMO_DRAFT"
        if origin:
            context["upload_origin"]=origin
        if origin and not demo:context['verification_policy']='HUMAN_REQUIRED'
        if parallel:context['parallel_specialists']=True
        initial=dict(version="LIVE-GRAPH-1.0",context=context,artifacts={},events=[],ledger=Ledger(scope.review_id).to_dict(),status="RUNNING",pending_stage=None,report_markdown=None,report_metadata=None)
        store.initialize()
    else:
        context=prior[1];scope=Scope.model_validate(context["scope"])
        _scope(actor,scope.model_dump())
        store.assert_review_open(scope.review_id)
        if context["source_binding"]!=source_binding:
            raise InputError("LIVE_SOURCE_OR_PROMPT_CHANGED")
        initial=load_live(root,actor,operation_id)
        if resume_operation_id is None:
            return initial
        if initial["status"] not in ("WAITING_EVIDENCE","WAITING_REVIEW","WAITING_CONFIGURATION"):
            raise InputError("LIVE_CURRENT_PAUSE_REQUIRED")
        if initial["status"]=="WAITING_EVIDENCE":
            supported(store,store.get_record(request_key(scope.run_id,initial["pending_stage"]))[1])
        elif initial["status"]=="WAITING_CONFIGURATION":
            prepared=store.get_record("live-provider-request:"+scope.run_id+":"+initial["pending_stage"])
            if prepared is None:
                raise InputError("LIVE_PREPARED_PROVIDER_REQUEST_REQUIRED")
            packet_tokens(root,prepared[1]["task"],stage=initial["pending_stage"])
            from .live_setup import read_api_key
            read_api_key(root)
        else:
            _credit_record(store,context)
    receipt=store.admit(command_id,scope.model_dump(),dict(action="LIVE_CONTINUE" if prior else "LIVE_START",run=operation_id,source_binding=source_binding),
        writes=() if prior else (RecordWrite("live-context:"+operation_id,"LIVE_CONTEXT",context,0),RecordWrite("live-progress:"+operation_id,"LIVE_PROGRESS",initial,0),RecordWrite("ledger:"+scope.review_id,"BUDGET_LEDGER",initial["ledger"],0)))
    if receipt.duplicate:
        return load_live(root,actor,operation_id)
    ledger_key="ledger:"+scope.review_id

    def persist(state):
        with store.transaction() as connection:
            store.assert_claim(receipt, connection=connection)
            saved=store.get_record("live-progress:"+operation_id)
            store._write(connection,RecordWrite("live-progress:"+operation_id,"LIVE_PROGRESS",state,saved[0]))

    def packet(state):
        case=_live_case(base,state,store)
        panels=(restore_financial(state["artifacts"]["financial_analyst"]["payload"]),restore_compliance(state["artifacts"]["compliance_check"]["payload"]),restore_risk(state["artifacts"]["risk_quantifier"]["payload"]))
        return prepare_synthesis(case,panels=panels)

    def action(name):
        def invoke(state):
            store.assert_claim(receipt)
            if state["context"]!=context:
                raise InputError("LIVE_CHECKPOINT_CONTEXT_CHANGED")
            for a in state["artifacts"].values():
                if a["digest"]!=fingerprint("LIVE_ARTIFACT",{k:v for k,v in a.items() if k!="digest"}):
                    raise InputError("LIVE_HANDOFF_CHANGED")
            if name in ("fact_review","evidence_review"):
                if name=="fact_review":
                    wire=parse_extraction(state["artifacts"]["extractor"]["payload"]["wire_json"])
                    _validate_inputs(base.registration,base.scope,wire,base.case_data,base.inventory,registered_extraction=False)
                    required={f for a in base.case_data["factor_assessments"] for f in a["material_financial_fields"]}
                    if not general and (wire.conflicts or any(getattr(wire.financial_inputs,f).value is None for f in required) or any(getattr(wire.terms,f).value is None for f in ("requested_amount","borrower","legal_entity","term_months","interest_terms","currency"))):
                        stopped={**state,"status":"WAITING_INFORMATION","pending_stage":None}
                        persist(stopped)
                        return stopped
                request=_request(base,state,name,packet(state) if name=="evidence_review" else None)
                key=request_key(scope.run_id,name); saved=store.get_record(key)
                if saved is None:
                    store.put_record(RecordWrite(key,"LIVE_REVIEW_REQUEST",request,0))
                elif saved[1]!=request:
                    raise InputError("LIVE_REVIEW_REQUEST_CHANGED")
                if demo:
                    payload=dict(support_digest=fingerprint("DEMO_SOURCE_INTEGRITY",request),request_digest=request["digest"],
                        human_supported=False,verification_policy="DEMO_DRAFT",automated_integrity_checked=True,
                        limitation="Schema, source identity, references and financial basis checked; semantic and human verification not performed.")
                else:
                    paused={**state,"status":"WAITING_EVIDENCE","pending_stage":name};persist(paused)
                    from langgraph.types import interrupt
                    signal=interrupt(dict(stage=name,request_digest=request["digest"]))
                    digest=supported(store,request)
                    if signal!={"operation_id":command_id}:
                        raise InputError("LIVE_RESUME_RECEIPT_REQUIRED")
                    payload=dict(support_digest=digest,request_digest=request["digest"],human_supported=True)
            elif name=="human_review":
                paused={**state,"status":"WAITING_REVIEW","pending_stage":name};persist(paused)
                from langgraph.types import interrupt
                signal=interrupt(dict(stage=name,run_id=scope.run_id))
                if signal!={"operation_id":command_id}:
                    raise InputError("LIVE_CREDIT_RESUME_RECEIPT_REQUIRED")
                payload=_credit_record(store,context)
            else:
                payload=None
            provider=name in ("extractor","synthesizer")
            task=None
            if provider:
                task=tasks["extractor"] if name=="extractor" else live_synthesis_task(root,packet(state)["request"])
                if demo and name=="synthesizer":
                    task={**task,"context":{**task["context"],"verification_status":"Unverified educational draft. Automated integrity checks only; no human evidence verification or credit decision.",
                        "demo_output_budget":"Complete JSON within 650 output tokens. Rationale at most 35 words. observations MUST contain exactly one FINANCIAL, one COMPLIANCE, and one RISK entry; never repeat a panel. Each observation at most 20 words, with one or two exact supplied refs. Use only minimal supplied references supporting each statement. Conditions are actual proposed obligations, not passed policy tests. For Approve use empty conditions and condition_links. Retain annual-analysis, full-term and concentration limitations. Human evidence verification and mandatory annual-statement covenant evaluation are incomplete: do not state all requirements are satisfied or no issues remain. A PanelDecision is only an original AI proposal; Python readiness prevents credit approval. proposed_action may be null."}}
                prepared_key="live-provider-request:"+scope.run_id+":"+name
                if origin and not demo and name=='synthesizer':
                    task={**task,'context':{**task['context'],'output_guidance':'Complete JSON within 650 output tokens: exactly one FINANCIAL, COMPLIANCE and RISK observation, each <=20 words; rationale <=35 words; minimal supplied refs. Missing scores/inputs/applicability are unknown, never Low/Pass. Keep annual/full-term/concentration limitations. Python readiness alone controls eligibility; proposed_action may be null.'}}
                prepared=store.get_record(prepared_key)
                try:
                    from .live_setup import read_api_key
                    read_api_key(root)
                    count=packet_tokens(root,task,stage=name)
                    needs_verification=False
                except InputError:
                    needs_verification=True
                if needs_verification or prepared is not None:
                    request=dict(scope=scope.model_dump(),stage=name,task=task,task_digest=fingerprint("LIVE_PACKET",task))
                    if prepared is None:
                        store.put_record(RecordWrite(prepared_key,"LIVE_PROVIDER_REQUEST",request,0))
                    elif prepared[1]!=request:
                        raise InputError("LIVE_PREPARED_PROVIDER_REQUEST_CHANGED")
                    persist({**state,"status":"WAITING_CONFIGURATION","pending_stage":name})
                    from langgraph.types import interrupt
                    signal=interrupt(dict(stage=name,task_digest=request["task_digest"],reason="PROVIDER_PACKET_VERIFICATION_REQUIRED"))
                    if signal!={"operation_id":command_id}:
                        raise InputError("LIVE_CONFIGURATION_RESUME_RECEIPT_REQUIRED")
                    count=packet_tokens(root,task,stage=name)
            ledger_version,ledger_data=store.get_record(ledger_key)
            ledger=Ledger.from_dict(ledger_data)
            reservation=operation_id+":node:"+name
            reserved=ledger.reserve(reservation,Usage(nodes=4 if name=='specialist_panel' else 1,tools=3 if name=='specialist_panel' else int(name in TOOL_STAGES),active_ms=0 if provider else ledger.operation_timeout_ms()))
            store.put_record(RecordWrite(ledger_key,"BUDGET_LEDGER",reserved.to_dict(),ledger_version))
            clock=time.monotonic()
            if payload is None:
                if name=="pdf_input":
                    payload=dict(source_binding=source_binding,pages=len(base.inventory))
                    if origin:payload["upload_origin"]=origin
                elif provider:
                    result=dispatch_generation(root,str(uuid5(UUID(operation_id),"paid:"+name)),scope.review_id,stage=name,instruction=task["instruction"],context=task["context"],verified_input_tokens=count,_held_receipt=receipt)
                    if result["response"]["status"]!="VALIDATED":
                        raise InputError("LIVE_PROVIDER_OUTPUT_NOT_VALIDATED")
                    payload=dict(wire_json=result["response"]["output_text"],provider_result=result,provenance="ACTUAL_PROVIDER_RESPONSE")
                    if name=="synthesizer":
                        payload["packet"]=packet(state)
                elif name=="financial_analyst":
                    payload=primitive(asdict(compute_financials(_live_case(base,state,store))))
                elif name=='specialist_panel':
                    from .graph import run_specialist_branches
                    case=_live_case(base,state,store)
                    def calculate(which):
                        started=time.monotonic();financial=compute_financials(case)
                        result=financial
                        if which!='financial_analyst':
                            compliance=compute_compliance(case,financial);result=compliance
                            if which=='risk_quantifier':result=compute_risk(case,financial,compliance)
                        return dict(payload=primitive(asdict(result)),active_ms=max(1,int((time.monotonic()-started)*1000)),input_digest=case.dependency_digest)
                    outputs=run_specialist_branches({n:lambda n=n:calculate(n) for n in ('financial_analyst','compliance_check','risk_quantifier')})
                    payload=dict(branches=outputs,execution='PARALLEL_FAN_OUT_JOIN')
                elif name=="compliance_check":
                    payload=primitive(asdict(compute_compliance(_live_case(base,state,store),restore_financial(state["artifacts"]["financial_analyst"]["payload"]))))
                elif name=="risk_quantifier":
                    payload=primitive(asdict(compute_risk(_live_case(base,state,store),restore_financial(state["artifacts"]["financial_analyst"]["payload"]),restore_compliance(state["artifacts"]["compliance_check"]["payload"]))))
                elif name=="route_review":
                    case=_live_case(base,state,store);financial=restore_financial(state["artifacts"]["financial_analyst"]["payload"])
                    wire=parse_synthesis(state["artifacts"]["synthesizer"]["payload"]["wire_json"]);cfg=case.case_data["policy_config"]
                    final=evaluate_policy({m.metric_id:m for m in financial.metric_results},case.wire.terms,config=PolicyConfig(cfg["secured_equipment"],cfg["kyc_fixture_required"],cfg["sanctions_fixture_required"],cfg["basis"]),dependency_digest=case.dependency_digest,metric_source_refs=dict(financial.metric_source_refs),material_financial_ready=financial.completeness=="COMPLETE",synthesis_complete=True,confidence=wire.panel_decision.confidence)
                    workflow=aggregate_workflow((final.workflow,state["artifacts"]["risk_quantifier"]["payload"]["score"]["workflow"]))
                    payload=dict(workflow="BLOCKED" if wire.panel_decision.conditions and not demo else workflow,final_policy=primitive(asdict(final)))
                    from .readiness_service import assess_current, proposal
                    provisional={**state["artifacts"],"route_review":{"payload":payload}}
                    assessment=assess_current(store,context,provisional,receipt)
                    payload.update(ai_proposal=proposal(state["artifacts"],"LIVE"),approval_readiness=assessment.model_dump(),human_decision=None)
                elif name=="review_prepare":
                    payload=dict(required_role="AuthorizedApprover",required_tier="NORMAL",analysis_digest=fingerprint("LIVE_CREDIT_BASIS",state["artifacts"]))
                elif name=="report_generator":
                    from .memo import render_live_memo
                    reviews=[]
                    for review_stage in ("fact_review","evidence_review"):
                        request=store.get_record(request_key(scope.run_id,review_stage))[1]
                        if demo:
                            reviews.append(dict(target=review_stage,domain="TECHNICAL_INTEGRITY_ONLY",reviewer="Application â€” not a human reviewer",timestamp_utc=now(),
                                comments="Automated demo checks only. Human evidence verification and credit decision are not recorded.",source_refs=list(request["sources"])))
                            continue
                        supported(store,request)
                        for target in request["targets"]:
                            for domain in target["domains"]:
                                record=store.get_record(support_key(request,target["id"],domain))[1]
                                reviews.append(dict(target=target["label"],domain=domain,reviewer=record["reviewer_name"],timestamp_utc=record["timestamp_utc"],comments=record["command"]["comments"],source_refs=target["source_refs"]))
                    from .readiness_service import assess_current
                    current=assess_current(store,context,state["artifacts"],receipt)
                    payload=render_live_memo({**state,"approval_readiness":current.model_dump()},now(),reviews)
                else:
                    raise InputError("LIVE_STAGE_UNKNOWN")
            elapsed=max(1,int((time.monotonic()-clock)*1000))
            lv,ld=store.get_record(ledger_key)
            completed=Ledger.from_dict(ld).settle(reservation,Usage(nodes=4 if name=='specialist_panel' else 1,tools=3 if name=='specialist_panel' else int(name in TOOL_STAGES),active_ms=0 if provider else elapsed))
            artifact=dict(stage=name,payload=primitive(payload),source_binding=source_binding)
            artifact["digest"]=fingerprint("LIVE_ARTIFACT",artifact)
            event=dict(sequence=len(state["events"])+1,run_id=scope.run_id,stage=name,event="stage_completed",timestamp=now(),active_ms=elapsed,artifact_digest=artifact["digest"])
            updated={**state,"artifacts":{**state["artifacts"],name:artifact},"events":state["events"]+[event],"ledger":completed.to_dict(),"status":"RUNNING","pending_stage":None}
            if name=='specialist_panel':
                for branch,output in payload['branches'].items():
                    item=dict(stage=branch,payload=output['payload'],source_binding=source_binding);item['digest']=fingerprint('LIVE_ARTIFACT',item)
                    updated['artifacts'][branch]=item
                    updated['events'].append(dict(sequence=len(updated['events'])+1,run_id=scope.run_id,stage=branch,event='stage_completed',timestamp=now(),active_ms=output['active_ms'],artifact_digest=item['digest'],execution_group='specialist_panel',input_digest=output['input_digest']))
            if name=="risk_quantifier" and (payload["score"]["total"] is None or payload["score"]["missing"]):
                updated["status"]="WAITING_INFORMATION"
            if name=="risk_quantifier" and updated["status"]=="RUNNING" and aggregate_workflow((state["artifacts"]["compliance_check"]["payload"]["workflow"],payload["score"]["workflow"]))!="CONTINUE":
                updated["status"]="BLOCKED_POLICY"
            if name=="route_review":
                updated.update(ai_proposal=payload["ai_proposal"],approval_readiness=payload["approval_readiness"],human_decision=None)
                updated["status"]={"CONTINUE":"REPORT_ALLOWED","REVIEW_REQUIRED":"WAITING_REVIEW"}.get(payload["workflow"],"BLOCKED_POLICY")
                if general or demo and payload["workflow"]=="REVIEW_REQUIRED":
                    updated["status"]="REPORT_ALLOWED"
            if name=="human_review":
                updated["human_decision"]=payload
                updated["status"]="REPORT_ALLOWED"
            if name=="report_generator":
                updated.update(status="COMPLETED",report_markdown=payload["markdown"],report_metadata=payload["metadata"])
            with store.transaction() as connection:
                store.assert_claim(receipt, connection=connection)
                store._write(connection,RecordWrite(ledger_key,"BUDGET_LEDGER",completed.to_dict(),lv))
                saved=store.get_record("live-progress:"+operation_id)
                store._write(connection,RecordWrite("live-progress:"+operation_id,"LIVE_PROGRESS",updated,saved[0]))
            return updated
        return invoke
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
        from langgraph.types import Command
        with closing(sqlite3.connect(config.database,check_same_thread=False)) as connection:
            graph=build_graph({n:action(n) for n in LIVE_ORDER+("review_prepare","human_review")+(('specialist_panel',) if parallel else ())},live=True,parallel_specialists=parallel,checkpointer=SqliteSaver(connection,serde=JsonPlusSerializer(pickle_fallback=False,allowed_json_modules=None,allowed_msgpack_modules=None)))
            invocation=dict(configurable=dict(thread_id=scope.thread_id),recursion_limit=20)
            if prior:
                checkpoint=graph.get_state(invocation)
                if checkpoint.values["context"]!=context or checkpoint.next!=(initial["pending_stage"],):
                    raise InputError("LIVE_PENDING_CHECKPOINT_CHANGED")
                result=graph.invoke(Command(resume={"operation_id":command_id}),invocation)
            else:
                result=graph.invoke(initial,invocation)
            result={k:v for k,v in result.items() if k!="__interrupt__"}
            if graph.get_state(invocation).next:
                result=store.get_record("live-progress:"+operation_id)[1]
            persist(result)
        store.release(receipt,confirmed_idle=True)
        return result
    except BaseException:
        store.mark_unknown(receipt)
        raise


def _credit_record(store,context):
    saved=store.get_record("live-credit:"+context["scope"]["run_id"])
    if saved is None:
        raise InputError("LIVE_CREDIT_DECISION_REQUIRED")
    event=saved[1]
    progress=store.get_record("live-progress:"+context["operation_id"])
    request=None if progress is None else progress[1]["artifacts"].get("review_prepare")
    if request is None or event.get("scope")!=context["scope"] or event.get("analysis_digest")!=request["payload"]["analysis_digest"] or event.get("reviewer_role")!="AuthorizedApprover" or event.get("reviewer_tier")!="NORMAL" or event.get("decision") not in ("Approve","Reject") or not event.get("comments","").strip() or not event.get("timestamp_utc"):
        raise InputError("LIVE_CREDIT_RECORD_CHANGED")
    if event["decision"]=="Approve":
        from .readiness_service import require_approval
        snap=event.get("approval_readiness",{})
        require_approval(store,dict(context=context,artifacts=progress[1]["artifacts"],status=progress[1]["status"]),snap.get("version"),snap.get("assessment_digest"))
    return event


def record_credit(root,actor,operation,command_id,analysis_digest,decision,comments,*,expected_readiness_version=None,expected_readiness_digest=None):
    state=load_live(root,actor,operation);scope=state["context"]["scope"]
    if actor.persona!="AuthorizedApprover" or "NORMAL" not in actor.allowed_review_tiers or state["status"]!="WAITING_REVIEW" or decision not in ("Approve","Reject") or not comments.strip() or len(comments)>4096:
        raise InputError("LIVE_CREDIT_ACTION_NOT_PERMITTED")
    basis=state["artifacts"]["review_prepare"]["payload"]["analysis_digest"]
    if basis!=analysis_digest:
        raise InputError("LIVE_CREDIT_BASIS_CHANGED")
    if str(UUID(command_id))!=command_id:
        raise InputError("CANONICAL_OPERATION_UUID_REQUIRED")
    store=Store(load_configuration(Path(root)).database)
    from .readiness_service import assess_current,require_approval,key as readiness_key
    snapshot=assess_current(store,state["context"],state["artifacts"])
    preconditions=()
    if decision=="Approve":
        if expected_readiness_version is None or expected_readiness_digest is None:
            raise InputError("LATEST_READINESS_VERSION_REQUIRED")
        current=require_approval(store,dict(context=state["context"],artifacts=state["artifacts"],status=state["status"]),expected_readiness_version,expected_readiness_digest)
        preconditions=((readiness_key(scope["run_id"]),current[0]),)
    event=dict(operation_id=command_id,scope=scope,analysis_digest=basis,approval_readiness=snapshot.model_dump(),decision=decision,comments=comments,reviewer_role=actor.persona,reviewer_tier="NORMAL",reviewer_name="Demo Authorized Approver",timestamp_utc=now())
    receipt=store.admit(command_id,scope,dict(action="LIVE_CREDIT_DECISION",analysis_digest=basis,decision=decision,comments=comments),writes=(RecordWrite("live-credit:"+scope["run_id"],"LIVE_CREDIT_DECISION",event,0),),expected_records=preconditions)
    if not receipt.duplicate:
        store.release(receipt,confirmed_idle=True)
    return event

