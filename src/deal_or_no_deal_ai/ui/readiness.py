"""Approval readiness presentation and explicit metadata reviews; no model dispatch."""
from uuid import uuid4
import sqlite3
from ..context import InputError
from ..readiness import CovenantEvaluation
from ..readiness_service import (ReadinessReviewCommand,record_review,evidence_targets,CHECKS,
                                 HumanReadinessDecision,record_ready_decision)
from .presentation import surface
from .labels import friendly,case_label


def render(st,run,store,root=None,actor=None,review=False,evidence_available=False):
    a=run.get("approval_readiness")
    if not a:
        return
    from ..recommendation import from_run
    recommendation=from_run(run)
    surface(st,"AI Recommendation",recommendation["outcome"],recommendation["recommendation"])
    st.write("**Supporting Rationale:** "+" ".join(p["text"] for p in recommendation["rationale"]))
    if recommendation["issues"]:
        with st.expander("Outstanding issues"):
            for issue in recommendation["issues"]:
                st.write("- "+issue["text"])
    st.write("**Required Next Action:** "+recommendation["next_action"])
    human=run.get("human_decision")
    st.write("**Human Decision:** "+recommendation["human_decision"])
    if review and evidence_available and run["context"].get("mode")!="LIVE":
        from .command_center import references
        handles=list(dict.fromkeys(ref for item in recommendation["rationale"]+recommendation["issues"] for ref in item["refs"]))
        with st.expander("Validate recommendation evidence"):
            references(st,handles,"recommendation")
    original=run.get("ai_proposal")
    if original:
        with st.expander("Original AI proposal and reasoning"):
            st.caption("Original AI proposal: "+original["decision"]+" - preserved for traceability, not the effective recommendation or a human credit decision.")
            st.write(original["rationale"])
    st.caption("Readiness version "+str(a["version"])+(" - current assessment" if a["version"] else " - not yet recorded for this historical review"))
    with st.expander("Required checks and supporting evidence"):
        for r in a["evaluated_requirements"]:
            st.write("**"+r["label"]+":** "+friendly(r["status"]));st.caption(r["reason"])
            if r["evidence_refs"]:
                st.caption("Sources: "+", ".join(case_label(v) for v in r["evidence_refs"]))
    if review and root is not None and actor is not None and "synthesizer" in run["artifacts"]:
        with st.expander("Evaluate approval-readiness requirements"):
            _evaluate(st,run,store,root,actor)
    if root is not None and actor is not None and actor.persona=="AuthorizedApprover" and run["context"].get("variant")=="default" and run.get("status")=="COMPLETED" and a["approval_eligible"] and not human:
        with st.form("ready-credit:"+a["assessment_digest"]):
            comments=st.text_area("Approval decision comments (required)")
            submit=st.form_submit_button("Record authorized human approval")
        if submit:
            try:
                record_ready_decision(root,actor,run["operation_id"],HumanReadinessDecision(operation_id=str(uuid4()),expected_version=a["version"],expected_digest=a["assessment_digest"],expected_analysis=a["analysis_digest"],decision="Approve",comments=comments))
            except (InputError,ValueError,OSError,sqlite3.Error):
                st.error("Approval not recorded. The current readiness, review version, role and source evidence must all remain valid.")
            else:
                st.rerun()


def _evaluate(st,run,store,root,actor):
    from ..command_center import source_packet
    try:
        packet=source_packet(root,run)
    except (InputError,ValueError,OSError,sqlite3.Error,KeyError):
        st.warning("Current source evidence is unavailable. Revalidate the source version before recording a readiness evaluation.")
        return
    a=run["approval_readiness"]
    sources={k:v["text"] for k,v in packet["request"]["reference_dictionary"].items() if v["kind"]=="SOURCE"}
    for ref,text in sources.items():
        with st.expander("Original source: "+case_label(ref)):
            st.text(text)
    if actor.persona=="ComplianceOfficer" and a["covenants"]:
        selected=st.selectbox("Reporting covenant to evaluate",[c["covenant_id"] for c in a["covenants"]],format_func=lambda k,items=a["covenants"]:next(c["clause"] for c in items if c["covenant_id"]==k))
        c=next(c for c in a["covenants"] if c["covenant_id"]==selected)
        st.caption("Future reporting is not automatically breached. Record the contractual timing; do not invent a due date.")
        with st.form("covenant:"+a["analysis_digest"]+selected):
            applicability=st.selectbox("Covenant applicability",("APPLICABLE","NOT_APPLICABLE","UNKNOWN"),index=None,format_func=friendly)
            timing=st.selectbox("Contractual timing",("PRE_DECISION","ONGOING","FUTURE","UNKNOWN"),index=None,format_func=friendly)
            due=st.text_input("Contractual due date (YYYY-MM-DD, only if documented)")
            compliance=st.selectbox("Covenant compliance",("COMPLIANT","NOT_YET_DUE","BREACHED","UNKNOWN"),index=None,format_func=friendly)
            evidence=st.selectbox("Covenant evidence",("VERIFIED","PENDING","MISSING","STALE"),index=None,format_func=friendly)
            quotes={ref:st.text_area("Supporting covenant quote from "+case_label(ref),key="cov-quote:"+selected+ref) for ref in sources}
            comments=st.text_area("Covenant evaluation reason (required)")
            submit=st.form_submit_button("Record covenant evaluation")
        if submit:
            try:
                quotes={r:q for r,q in quotes.items() if q.strip()}
                cov=CovenantEvaluation(covenant_id=selected,clause=c["clause"],applicability=applicability,timing=timing,due_date=due or None,evaluation_status="EVALUATED",compliance_status=compliance,evidence_status=evidence,evidence_refs=list(quotes),reason=comments)
                command=ReadinessReviewCommand(operation_id=str(uuid4()),expected_version=a["version"],expected_analysis=a["analysis_digest"],part="COVENANT",covenant=cov,quotes=quotes,comments=comments)
                record_review(root,actor,run["operation_id"],command)
            except (InputError,ValueError,OSError,sqlite3.Error):
                st.error("Evaluation not recorded. Check the current review, quoted source, role and contractual timing. A future due date needs explicit supporting date evidence.")
            else:
                st.rerun()
    if actor.persona in ("RiskManager","ComplianceOfficer"):
        domain="FINANCIAL_RISK" if actor.persona=="RiskManager" else "POLICY_CONTROL"
        with st.form("readiness-evidence:"+a["analysis_digest"]+domain):
            st.caption("Verify every listed current target against the source pages. This records evidence review only, not credit approval.")
            selected=[target for target in evidence_targets(run["artifacts"],domain) if st.checkbox("Verified: "+target.replace("_"," ").replace("."," - "),key="rt:"+domain+a["analysis_digest"]+target)]
            checks=st.multiselect("Evidence checks completed",CHECKS,format_func=friendly)
            quotes={ref:st.text_area("Evidence quote from "+case_label(ref),key="rquote:"+domain+ref) for ref in sources}
            comments=st.text_area("Evidence verification reason (required)")
            submit=st.form_submit_button("Record current evidence verification")
        if submit:
            try:
                command=ReadinessReviewCommand(operation_id=str(uuid4()),expected_version=a["version"],expected_analysis=a["analysis_digest"],part="EVIDENCE",domain=domain,status="VERIFIED",checked_targets=selected,checks=checks,quotes={r:q for r,q in quotes.items() if q.strip()},comments=comments)
                record_review(root,actor,run["operation_id"],command)
            except (InputError,ValueError,OSError,sqlite3.Error):
                st.error("Verification not recorded. Every current target, required check and source quote must be verified by the permitted reviewer.")
            else:
                st.rerun()
