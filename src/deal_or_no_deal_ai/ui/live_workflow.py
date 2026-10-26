"""Live review screens; viewing never dispatches, supports or resumes work."""
import sqlite3
from uuid import uuid4

from ..context import InputError
from ..live_review import Assessment, assess, request_key, support_key, supported, required_checks
from ..live_worker import run_live, record_credit
from .labels import friendly


def _next_action(state):
    if state.get("quarantine"):
        return "This attempt was set aside and cannot restart. Select the earlier live review awaiting fact verification; actual cost remains unknown."
    if state["status"] == "WAITING_CONFIGURATION":
        return "Verify AI setup and request limits in the sidebar; Analyst continues after verification."
    if state["status"] in ("RECOVERY_REQUIRED", "MODEL_OUTPUT_INVALID"):
        return "Inspect the preserved validation or recovery details; do not repeat the AI call."
    return {"fact_review": "Risk Manager verifies extracted facts against sources; Analyst then continues.",
            "evidence_review": "Required specialists verify AI conclusions against sources; Analyst then continues.",
            "human_review": "Authorized Approver reviews the permitted credit actions."}.get(
                state["pending_stage"], "Read the recorded memo and current readiness." if state["status"] == "COMPLETED" else "Inspect outstanding information and review requirements.")

CHECK_LABELS={"row_label":"I checked the correct financial row or source item", "debt_service_scope":"I checked which debts and repayments are included, where applicable","reference":"I checked the cited source and page", "value":"I checked the value or claim", "units_scale":"I checked units and scale", "period":"I checked the reporting period", "subject_facility":"I checked the borrower and loan", "qualifications":"I checked limitations and required findings", "meaning":"The evidence supports the complete meaning"}


def assessment_errors(request,target,status,quotes,checks,comments):
    """Explain exact missing inputs without recording support or exposing secrets."""
    errors=[]
    if status is None:errors.append('Choose an evidence assessment.')
    if not comments.strip():errors.append('Enter review comments explaining your assessment.')
    present={ref:quote for ref,quote in quotes.items() if quote.strip()}
    if not present:errors.append('Enter an exact supporting quote from a displayed source page; comments alone are not evidence.')
    if status=='HUMAN_SUPPORTED':
        missing=[ref for ref in target['source_refs'] if ref not in present]
        if missing:errors.append('A quote is required from every source cited for this item: '+', '.join(missing)+'.')
        missing_checks=[CHECK_LABELS[c] for c in required_checks(request['stage']) if c not in checks]
        if missing_checks:errors.append('Complete these checks: '+'; '.join(missing_checks)+'.')
    for ref,quote in present.items():
        if ref not in target['source_refs'] or quote not in request['sources'].get(ref,''):
            errors.append('The quote for '+ref+' must match a continuous passage on that displayed page exactly, including spaces and punctuation.')
    return errors


def _sources(st,store,state):
    st.subheader("Evidence explorer")
    found=False
    for stage in ("evidence_review","fact_review"):
        request=store.get_record(request_key(state["context"]["scope"]["run_id"],stage))
        if request:
            found=True
            for ref,text in request[1]["sources"].items():
                with st.expander("Supporting source: "+ref+" · "+friendly(stage)):
                    metadata=request[1]["source_metadata"][ref]
                    st.caption("Original page "+str(metadata["page"])+" | Version "+metadata["source_version"])
                    st.text(text)
    if not found:
        st.info("Source evidence appears when extraction is ready for review.")




def _history(st,store,state,scope):
    st.caption("Live evidence assessments are not credit approvals. Times below are UTC.")
    if state.get("quarantine"):
        audit=state["quarantine"]
        st.warning("Interrupted attempt set aside; restart is blocked. Actual provider usage remains unknown and USD0.0007 remains reserved. This is not a credit decision.")
        st.write(audit["timestamp_utc"]+" | "+audit["reviewer_name"]+" | Simulated administrative action")
        st.write(audit["reason"])
    for stage in ("fact_review","evidence_review"):
        request=store.get_record(request_key(scope["run_id"],stage))
        if request:
            for target in request[1]["targets"]:
                for domain in target["domains"]:
                    event=store.get_record(support_key(request[1],target["id"],domain))
                    if event:
                        value=event[1];st.write(value["timestamp_utc"]+" | "+friendly(value["reviewer_role"])+" | "+friendly(value["command"]["status"]));st.write(value["command"]["comments"])
    credit=store.get_record("live-credit:"+scope["run_id"])
    if credit:
        st.write(credit[1]["timestamp_utc"]+" | Authorized Approver | "+credit[1]["decision"]);st.write(credit[1]["comments"])
    else:
        st.info("No human credit decision recorded for this live review.")

def _review(st,root,actor,store,state):
    if state['context'].get('upload_origin') and state['status']=='COMPLETED':
        from .uploaded_decisions import render
        render(st,root,actor,store,state)
        return
    scope=state["context"]["scope"];stage=state["pending_stage"]
    if state["status"]=="WAITING_CONFIGURATION":
        st.info("The next AI request needs setup or exact token-limit verification. No call was made for this pending step. Use Live AI setup and readiness in the sidebar.")
        prepared=store.get_record("live-provider-request:"+scope["run_id"]+":"+stage)
        if prepared:
            with st.expander("Technical details: prepared AI request"):
                st.json(prepared[1])
        if st.button("Continue after setup verification",disabled=actor.persona!="Analyst"):
            _continue(st,root,actor,state)
    if state["status"]=="WAITING_INFORMATION":
        st.warning("Required information is missing or conflicting. No complete risk score, final decision or memo is available. Source corrections for live reviews are not connected in this bounded first version.")
    if state["status"]=="BLOCKED_POLICY":
        st.warning("An unresolved policy, score or condition requires a workflow beyond this first live example. A generic approval cannot clear it.")
    if stage in ("fact_review","evidence_review"):
        request=store.get_record(request_key(scope["run_id"],stage))[1]
        st.subheader("Verify extracted facts" if stage=="fact_review" else "Verify AI conclusions")
        target_id=st.selectbox("Information to verify",[t["id"] for t in request["targets"]],format_func=lambda k, targets=request["targets"]:next(t["label"] for t in targets if t["id"]==k))
        target=next(t for t in request["targets"] if t["id"]==target_id)
        from ..ai_evidence_review import key as ai_review_key
        ai_review=store.get_record(ai_review_key(request))
        if ai_review:
            st.caption('AI-assisted review is recorded separately. It does not count as human verification or clear this checkpoint.')
            with st.expander('AI-assisted evidence review results',expanded=False):
                labels={t['id']:t['label'] for t in request['targets']}
                st.dataframe([{'Item':labels[i['target_id']],'AI assessment':i['status'].removeprefix('AI_').replace('_',' ').title(),'Explanation':i['reason']} for i in ai_review[1]['assessments']],hide_index=True)
            for item in ai_review[1]['assessments']:
                if item['target_id']==target_id:
                    label={'AI_SUPPORTED':'AI-reviewed: supported by supplied sources','AI_FLAGGED':'AI-reviewed: issue found','AI_NEEDS_INFORMATION':'AI-reviewed: more information needed'}[item['status']]
                    st.info(label+' — '+item['reason'])
        if isinstance(target["text"],dict) and "value" in target["text"]:
            st.write("Extracted value:",target["text"]["value"])
            basis=target["text"].get("basis_id")
            if basis:
                st.write("Reporting basis:",request["review_basis"]["bases"].get(basis,"Not available"))
        else:
            st.write(target["text"])
        with st.expander("Borrower and reporting periods"):
            st.write(request["review_basis"])

        for ref in target["source_refs"]:
            with st.expander("Supporting source: "+ref):
                metadata=request["source_metadata"][ref]
                st.caption("Original page "+str(metadata["page"])+" | Version "+metadata["source_version"])
                st.text(request["sources"][ref])
        allowed=[d for d in target["domains"] if actor.persona=={"FINANCIAL_RISK":"RiskManager","POLICY_CONTROL":"ComplianceOfficer"}[d]]
        for domain in target["domains"]:
            event=store.get_record(support_key(request,target_id,domain))
            st.caption(friendly(domain)+": "+(friendly(event[1]["command"]["status"]) if event else "Awaiting reviewer verification"))
        for domain in allowed:
            if store.get_record(support_key(request,target_id,domain)):
                continue
            with st.form("live-support:"+request["digest"]+target_id+domain):
                st.caption("Source text is prefilled from this deal for review. You may shorten it to the relevant exact passage. Prefill does not verify the claim or approve credit; choose your own assessment and checks.")
                quotes={ref:st.text_area("Exact supporting quote from "+ref,value=request['sources'][ref],key="live-quote:"+request['digest']+target_id+domain+ref) for ref in target["source_refs"]}
                checks=[c for c in required_checks(stage) if st.checkbox(CHECK_LABELS[c],key="live-check:"+request['digest']+target_id+domain+c)]
                status=st.selectbox("Evidence assessment",("HUMAN_SUPPORTED","UNSUPPORTED","WITHHELD"),index=None,format_func=friendly)
                comments=st.text_area("Review comments (required)")
                submitted=st.form_submit_button("Record evidence review")
            if submitted:
                errors=assessment_errors(request,target,status,quotes,checks,comments)
                if errors:
                    for message in errors:st.error(message)
                    continue
                try:
                    command=Assessment(operation_id=str(uuid4()),request_digest=request["digest"],target_id=target_id,target_digest=target["digest"],domain=domain,status=status,quotes={ref:q for ref,q in quotes.items() if q.strip()},checks=checks,comments=comments)
                    assess(root,actor,scope["run_id"],stage,command)
                except (InputError,ValueError,OSError,sqlite3.Error) as error:
                    messages={
                        'LIVE_SUPPORT_SOURCE_OR_PROMPT_CHANGED':'The sources or AI instructions changed since this review started. This assessment cannot be applied to the old version.',
                        'LIVE_SUPPORT_ROLE_OR_VERSION_MISMATCH':'The reviewer role or review version changed. Select the required role and current review.',
                        'LIVE_SUPPORT_ALREADY_RECORDED':'This item already has a recorded assessment. It was not overwritten.',
                        'LIVE_SUPPORT_NOT_CURRENT_PAUSE':'This review is no longer paused at this verification step. Refresh and select its current stage.',
                    }
                    st.error(messages.get(str(error),'Evidence review could not be saved. The review may have changed or another execution may require attention. Your existing evidence remains unchanged.'))
                    if isinstance(error,InputError) and str(error) in messages:st.caption('Support reference: '+str(error))
                else:
                    st.rerun()
        try:
            supported(store,request);complete=True
        except InputError:
            complete=False
        st.caption("All required evidence assessments are complete." if complete else "Every required value or claim needs support from the permitted reviewer before continuation.")
        if st.button("Continue live review",disabled=not complete or actor.persona!="Analyst"):
            _continue(st,root,actor,state)
    elif stage=="human_review" and state["status"]=="WAITING_REVIEW":
        from ..readiness_service import assess_current
        current_readiness=assess_current(store,state["context"],state["artifacts"]).model_dump()
        st.info("Evidence checks are complete. A separate Authorized Approver with normal review permission must record a credit decision.")
        if actor.persona=="AuthorizedApprover":
            with st.form("live-credit:"+scope["run_id"]):
                decision=st.selectbox("Credit decision",(("Approve","Reject") if current_readiness["approval_eligible"] else ("Reject",)),index=None)
                comments=st.text_area("Decision comments (required)")
                submitted=st.form_submit_button("Record credit decision")
            if submitted:
                try:
                    record_credit(root,actor,state["context"]["operation_id"],str(uuid4()),state["artifacts"]["review_prepare"]["payload"]["analysis_digest"],decision,comments,expected_readiness_version=current_readiness["version"],expected_readiness_digest=current_readiness["assessment_digest"])
                except (InputError,ValueError,OSError,sqlite3.Error):
                    st.error("Decision not recorded. Check role, current review and required comments.")
                else:
                    st.rerun()
        credit=store.get_record("live-credit:"+scope["run_id"])
        if st.button("Continue to credit memo",disabled=actor.persona!="Analyst" or credit is None):
            _continue(st,root,actor,state)
    # Keep original citations available after completion as well as during a pause.
    for source_stage in ("fact_review","evidence_review"):
        request=store.get_record(request_key(scope["run_id"],source_stage))
        if request:
            with st.expander("All original sources: "+friendly(source_stage)):
                for ref,text in request[1]["sources"].items():
                    st.write(ref);st.text(text)


def _continue(st,root,actor,state):
    try:
        from ..live_demo import run_demo
        run_demo(root,actor,state["context"]["operation_id"],resume_operation_id=str(uuid4()))
    except (InputError,ValueError,OSError,sqlite3.Error):
        st.error("Review did not continue. Check current evidence, provider setup and remaining allowance. Any uncertain work is retained for technical review; no automatic retry occurred.")
    else:
        st.rerun()
