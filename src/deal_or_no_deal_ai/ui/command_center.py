"""V2 presentation over unchanged financial commands, artifacts and permissions."""
from .labels import friendly, FINANCIAL_HELP, case_label


from decimal import Decimal
from pathlib import Path
import sqlite3
from uuid import uuid4

from ..command_center import ROLES, get_run, list_runs, policy_display, source_packet, start_run, workspace_id
from ..configuration import load_configuration
from ..context import InputError, strict_json
from ..contracts import parse_synthesis
from ..graph import STAGES
from ..review import Actor
from ..storage import RunBusy, Store
from .presentation import CSS, WORKSPACE_TABS, context_header, safe, surface

PAGES = ("Deal Dashboard", "New Deal", "Review Workspace", "Agent Activity", "Credit Memo", "Decision History")
STAGE_NAMES = dict(zip(STAGES, ("Document validation", "Term extraction", "Financial calculations", "Policy compliance",
                               "Risk scoring", "Synthesis", "Evidence checks", "Decision routing", "Memo generation")))
STAGE_NAMES.update(review_prepare="Review preparation", human_review="Human review")
METRIC_NAMES = {"CALC-001": "EBIT", "CALC-002": "EBITDA", "CALC-003": "Funded debt",
                "CALC-004": "Debt-service coverage (DSCR)", "CALC-005": "Debt / EBITDA",
                "CALC-006": "Loan-to-value (LTV)", "CALC-007": "Revenue growth",
                "CALC-008": "Current ratio", "CALC-009": "Interest coverage"}


def term_value(name, value):
    if value is None:
        return "Not available"
    if name == "requested_amount":
        return f"{Decimal(value):,.2f}"
    if isinstance(value, list):
        return " · ".join(str(item) for item in value) or "None recorded"
    if name == "interest_terms" and isinstance(value, dict):
        return " · ".join(k.replace("_", " ").title() + ": " + str(v) for k, v in value.items() if v is not None)
    return str(value)


def terms(run):
    if run["context"].get("mode")=="LIVE":
        payload=run["artifacts"].get("extractor",{}).get("payload")
        if payload:
            from ..contracts import parse_extraction
            return parse_extraction(payload["wire_json"]).terms.model_dump(mode="json")
        return {}
    return run["artifacts"].get("extractor", {}).get("payload", {}).get("wire", {}).get("terms", {})


def go(st, page):
    st.session_state.financial_page = page


def prepare_review_sample(st):
    """Explicit navigation only; never start a run or change the selected role."""
    st.session_state.sample_scenario = "review"
    st.session_state.financial_operation = str(uuid4())
    st.session_state.operation_variant = "review"
    go(st, "New Deal")


def open_run(st, operation):
    st.session_state.selected_financial_operation = operation
    st.session_state.run_selector = operation
    go(st, "Review Workspace")


def _use_review(st, operation):
    st.session_state.selected_financial_operation = operation
    st.session_state.run_selector = operation


def _change_deal(st, latest):
    _use_review(st, latest[st.session_state.financial_deal_selector])


def _change_review_attempt(st):
    st.session_state.selected_financial_operation = st.session_state.run_selector


def select_deal_review(st, runs):
    """Select a unique deal first; historical attempts stay scoped and read-only."""
    from datetime import datetime
    groups = {}
    ordered = sorted(runs, key=lambda r: (r["context"]["generation_time"], r["operation_id"]), reverse=True)
    by_operation = {r["operation_id"]: r for r in ordered}
    for run in ordered:
        groups.setdefault(run["context"]["scope"]["deal_id"], []).append(run)
    latest = {deal: attempts[0]["operation_id"] for deal, attempts in groups.items()}
    requested = st.session_state.pop("next_financial_run", None)
    selected = requested if requested in by_operation else st.session_state.get("selected_financial_operation")
    if selected not in by_operation:
        selected = ordered[0]["operation_id"]
    deal = by_operation[selected]["context"]["scope"]["deal_id"]
    # Explicit navigation (Dashboard, corrections, reassessments) selects its exact
    # run. Widget callbacks update the durable selection before this script reruns.
    st.session_state.financial_deal_selector = deal
    labels = {}
    for identifier, attempts in groups.items():
        newest = attempts[0]
        borrower = terms(newest).get("borrower", {}).get("value") or "Borrower not available"
        labels[identifier] = borrower + " · " + case_label(newest["context"]["scenario_id"])
        if newest['context'].get('upload_origin'):
            labels[identifier]+=' · Uploaded deal '+identifier[:8]
    st.selectbox("Select Deal", list(groups), key="financial_deal_selector",
                 format_func=lambda identifier: labels[identifier], on_change=_change_deal, args=(st, latest))
    attempts = groups[deal]
    operations = [r["operation_id"] for r in attempts]
    st.session_state.selected_financial_operation = selected
    st.session_state.run_selector = selected
    attempt_labels = {}
    for index, run in enumerate(attempts):
        context = run["context"]
        stamp = datetime.fromisoformat(context["generation_time"].replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M:%S UTC")
        attempt_labels[run["operation_id"]] = ("Review " + str(len(attempts) - index)
            + (" (latest)" if index == 0 else "") + " · Version " + str(context["scope"]["input_revision"])
            + " · " + stamp + " · " + friendly(run["status"])
            + " · " + ("Nebius" if context.get("mode")=="LIVE" else "Saved example"))
    st.caption(str(len(groups)) + " deal(s) · " + str(len(attempts)) + " recorded review(s) for this deal. Selecting a deal opens its latest review.")
    if selected != latest[deal]:
        st.info("Viewing an earlier review. Its findings and decisions are historical; the latest review is available below.")
        st.button("Open latest review", on_click=_use_review, args=(st, latest[deal]))
    else:
        st.caption("Showing the latest review · " + attempt_labels[selected])
    if len(attempts) > 1:
        earlier = len(attempts) - 1
        with st.expander(f"Review History ({earlier} earlier {'review' if earlier == 1 else 'reviews'})", expanded=selected != latest[deal]):
            st.caption("Only reviews for the selected deal are listed. Opening one does not rerun analysis or change any decision.")
            st.selectbox("Review attempt", operations, key="run_selector",
                         format_func=lambda operation: attempt_labels[operation], on_change=_change_review_attempt, args=(st,))
    else:
        st.caption("No earlier reviews for this deal.")
    return selected


def choose_evidence(st, handle):
    st.session_state.evidence_reference = handle


def references(st, handles, key):
    for index, handle in enumerate(dict.fromkeys(handles)):
        st.button("↗ " + case_label(handle), key=f"ref:{key}:{index}", on_click=choose_evidence,
                  args=(st, handle), help="Open this reference in the evidence explorer")


def quick_actions(st):
    for col, label, page in zip(st.columns(3), ("Open review workspace", "Open credit memo", "View agent activity"),
                                ("Review Workspace", "Credit Memo", "Agent Activity")):
        col.button(label, on_click=go, args=(st, page), width="stretch")


def new_deal(st, root, actor):
    st.header("New Deal")
    live=load_configuration(root).mode=="LIVE"
    from ..live_worker import verification_policy
    demo=live and verification_policy(root)=="DEMO_DRAFT"
    st.caption("Start with a complete package. Review the details before running the analysis.")
    mode = st.radio("Intake mode", ("Sample Deal", "Upload New Deal"), horizontal=True)
    if mode == "Upload New Deal":
        if live:
            st.caption("Upload one deal's synthetic PDFs and declare its reporting basis for live analysis with mandatory human verification.")
        from .upload_intake import render
        render(st, root, actor)
        return
    variants=("default",) if live else ("default", "review", "missing", "reject", "conditional", "extraction-miss")
    if st.session_state.get("sample_scenario") not in variants:
        st.session_state.sample_scenario="default"
    variant = st.selectbox("Sample scenario", variants, key="sample_scenario",
                           format_func=lambda v: {"default": "Standard Deal", "review": "Human review required · confidence 0.65", "missing": "Missing Information - review pauses for documents", "reject": "Rejection Example - Risk Manager review", "conditional": "Policy Exception - specialist condition review", "extraction-miss": "Extraction Correction - verify the original source"}[v])
    scenario = {"missing": "E-M01", "reject": "E-F03", "conditional": "E-P01"}.get(variant, "E-N01")
    if st.session_state.get("operation_variant", variant) != variant or st.session_state.get("operation_execution",live)!=live:
        st.session_state.financial_operation = str(uuid4())
    st.session_state.operation_variant = variant
    st.session_state.operation_execution=live
    st.markdown('<div class="demo-strip">REGISTERED SAMPLE · ' + case_label(scenario) + ' · Fictional documents · '+('Nebius live draft: unverified; no human credit decision' if demo else 'Nebius live analysis: paid calls on Run or Continue; human verification required' if live else 'This review uses saved AI responses; no model calls')+'</div>', unsafe_allow_html=True)
    if live:
        st.caption("Standard Deal is the supported live example. Shared test allowance: USD0.10. Setup and request limits must be verified in the sidebar. Failure never substitutes saved answers.")
    if demo:
        st.info("Run generates an unverified educational draft using live AI. Two analysis calls and, when needed, one small request-size setup call use the shared allowance. Financial calculations and sample rules run in Python. Human verification and credit approval are not recorded.")
    if scenario == "E-M01":
        st.info("This package deliberately omits annual cash available for debt service (CFADS). It should pause for information, with no complete risk score, AI decision or final memo.")
    if scenario == "E-F03":
        st.info('Negative supplied cash flow supports this case-specific Reject recommendation. Risk Manager must record DSCR exception handling before an Authorized Approver can record Reject. A policy breach alone is not a rejection rule.')
    if scenario == "E-P01":
        st.info('DSCR 1.15x remains a policy Exception. Review the annual-statements condition through Risk Manager handling, Authorized Approver draft preparation, then Risk Manager and Compliance Officer support before the final decision. The condition remains outstanding.')
    if variant == "extraction-miss":
        st.info("The source contains CFADS900000 but this deliberately flawed extraction misses it. Review Workspace lets an Analyst save a source-backed correction, then explicitly update findings. This tests correction handling, not live model quality.")
    sample_package_preview(st)
    if "financial_operation" not in st.session_state:
        st.session_state.financial_operation = str(uuid4())
    blockers=[]
    database=load_configuration(root).database
    if database.exists():
        with Store(database).connection() as connection:
            blockers=connection.execute('SELECT operation_id,state FROM app_operations WHERE active_execution_key IS NOT NULL').fetchall()
    if blockers:
        st.error('AI review cannot start: another attempt is running or requires recovery. This execution lock affects both Sample Deal and Upload New Deal; changing inputs will not clear it.')
        for blocker in blockers:
            st.caption('Blocking attempt: '+blocker['operation_id']+' | '+('Recovery required' if blocker['state']=='RECOVERY_REQUIRED' else 'Execution in progress'))
    if st.button("Run AI Deal Review", disabled=actor.persona != "Analyst" or bool(blockers), type="primary"):
        try:
            with st.spinner("Running live agents and preparing the draft memo…" if demo else "Validating documents and extracting facts for human review…" if live else "Validating documents → analysing the deal → preparing the memo…"):
                if live:
                    from ..live_demo import run_demo
                    result=run_demo(root,actor,st.session_state.financial_operation)
                else:
                    result = start_run(root, actor, st.session_state.financial_operation, variant="default" if variant == "missing" else "review" if variant in ("reject", "conditional") else variant, scenario_id=scenario)
        except (InputError,RunBusy,ValueError,OSError,sqlite3.Error):
            operation=st.session_state.financial_operation
            store=Store(load_configuration(root).database)
            retained=store.get_record('live-context:'+operation) if live else None
            st.error('Review stopped. No saved response was substituted and no automatic retry was made.')
            st.caption('Attempt reference: '+operation)
            if retained:
                st.session_state.selected_financial_operation=operation
                st.warning('This attempt was retained. Open Review Workspace or Agent Activity for its recorded status. An uncertain provider request requires recovery before another run; do not repeatedly click Run.')
                quick_actions(st)
            else:
                st.warning('Analysis could not start. Another active request or a setup check may require attention. Check Live AI setup and readiness in the sidebar.')
            return
        st.session_state.selected_financial_operation = st.session_state.financial_operation
        if result["status"] == "COMPLETED":
            st.success("Existing result retrieved — no agents rerun." if result.get("duplicate")
                       else "Review completed. Findings and the credit memo are ready; no human decision was recorded.")
            quick_actions(st)
        else:
            message="Review needs attention: " + friendly(result["status"])
            if live:
                from .live_workflow import _next_action
                message+=". "+_next_action(result)
            if result["status"] in ("RECOVERY_REQUIRED","MODEL_OUTPUT_INVALID"):
                st.error(message)
            else:
                st.warning(message)
            for item in result.get("requested_information", []):
                st.write(item)
            quick_actions(st)
    if actor.persona != "Analyst":
        st.caption("Switch to the simulated Analyst role to start a sample review.")
    if st.button("Prepare a separate sample run", disabled=actor.persona != "Analyst"):
        st.session_state.financial_operation = str(uuid4())
        st.rerun()
    with st.expander("Technical details"):
        st.text(st.session_state.financial_operation)
        st.caption("The same operation ID retrieves its recorded result; a separate sample run creates a new ID.")


def sample_package_preview(st):
    """Shared registered package presentation, not a validation result."""
    details, documents, submit = st.columns(3)
    surface(details, "01 / Deal details", "Example Equipment LLC", "USD 1,200,000 · Term loan · 48 months")
    surface(documents, "02 / Documents", "5 registered pages", "Agreement, financials, collateral and authored assessment")
    surface(submit, "03 / Review & submit", "Ready for validation", "Source identities are checked before analysis.")
    with st.expander("Document checklist", expanded=True):
        st.dataframe([
            {"Source": "Loan agreement", "Pages": 1, "Validation": "Terms, identity and registration"},
            {"Source": "Financial statements / debt-service inputs", "Pages": 2, "Validation": "Reporting basis, units and completeness"},
            {"Source": "Collateral evidence", "Pages": 1, "Validation": "Value, exposure and liens"},
            {"Source": "Educational factor assessments", "Pages": 1, "Validation": "Approved illustrative scoring premises"},
        ], hide_index=True, width="stretch")
    st.caption("Validation occurs when you start. The checklist describes the package; it is not a new verification result.")


def evidence(st, refs):
    st.subheader("Evidence explorer")
    st.caption("Select a finding reference to trace it back to the registered source.")
    if not refs:
        st.warning("The recorded source version cannot be verified. Citations are withheld; current documents were not substituted.")
        return
    if st.session_state.get("evidence_reference") not in refs:
        st.session_state.evidence_reference = next(iter(refs))
    handle = st.selectbox("Evidence reference", list(refs), key="evidence_reference", format_func=case_label)
    reference = refs[handle]
    st.text(case_label(reference["label"]))
    st.caption(reference["kind"].title() + " · " + case_label(handle))
    if reference["kind"] == "SOURCE":
        st.caption("Original page " + str(reference["page"]) + " · Source version " + reference["source_version"])
        with st.container(border=True):
            st.text(reference["text"])
        with st.expander("Source identity"):
            st.text(reference["source_sha256"])
    else:
        value = reference.get("value", {})
        if isinstance(value, dict):
            st.dataframe([{"Property": k.replace("_", " ").title(), "Recorded value": str(v)}
                          for k, v in value.items() if k not in ("source_refs", "refs")], hide_index=True)
        else:
            st.text(str(value))
    if reference["refs"]:
        st.caption("Follow supporting evidence")
        references(st, [r for r in reference["refs"] if r in refs], "explorer:" + case_label(handle))
    st.caption("A resolvable citation identifies a source; it does not independently prove claim correctness.")


def render_workspace(st, run, packet, store, actor, root):
    live=run["context"].get("mode")=="LIVE"
    stages = run["artifacts"]
    preliminary=None
    if live and run['context'].get('upload_origin') and 'extractor' in stages and 'financial_analyst' not in stages:
        from ..uploaded_calculations import preview
        try:preliminary=preview(root,actor,run)
        except (InputError,ValueError,OSError):pass
    if live and run.get('outcome',{}).get('pending_stage')=='fact_review':
        from ..live_review import request_key,assessment_progress
        recorded=store.get_record(request_key(run['context']['scope']['run_id'],'fact_review'))
        if recorded:
            progress=assessment_progress(store,recorded[1])
            st.warning('Verified specialist analysis is paused for fact verification: '+str(progress['supported'])+' of '+str(progress['required'])+' required assessments have recorded support. Preliminary upload calculations, policy checks and risk findings are available; synthesis and verified graph stages remain pending. Open Human Review for the remaining items.')
            with st.expander('Remaining evidence assessments',expanded=False):
                st.dataframe([{'Item':r['item'],'Required reviewer':friendly(r['role']),'Status':friendly(r['status'])} for r in progress['remaining']],hide_index=True)
            st.caption('Unsupported or withheld assessments remain blockers. Do not mark incorrect extraction as supported to continue.')
    risk = stages.get("risk_quantifier", {}).get("payload", {}).get("score", {})
    compliance = policy_display(run, packet)
    cols = st.columns(3)
    cols[0].metric("Credit risk · illustrative", risk["display"] + " / 100" if risk.get("display") else "Insufficient Data" if preliminary else "Not computed")
    cols[0].caption("Risk band: " + (risk.get("band") or "Insufficient Data"))
    cols[1].metric("Policy exceptions", len(compliance["exception_rule_ids"]) if compliance["exception_rule_ids"] is not None else str(len(preliminary['policy']['exception_rule_ids']))+' (preliminary)' if preliminary else "Not checked")
    if live:
        from ..live_review import request_key,supported
        request=store.get_record(request_key(run["context"]["scope"]["run_id"],"evidence_review"))
        complete=False
        if request:
            try:
                supported(store,request[1]);complete=True
            except InputError:
                pass
        cols[2].metric("Evidence checks","Reviewer checks completed" if complete else "Reviewer checks required")
    else:
        cols[2].metric("Evidence checks", "Sample checks completed" if "evidence_review" in stages else "Not checked")
    st.caption("The score is not probability of default. Evidence availability and claim correctness are separate checks.")
    if run["context"]["scenario_id"] == "E-M01":
        st.warning("Missing CFADS: the annual cash available for debt service schedule is required. No complete score, AI recommendation or final memo can be generated.")
        st.caption("Next owner: simulated Analyst. Obtain the 2027 CFADS schedule. Replacement-document validation and continuation are not connected in this MVP slice; final decisions remain blocked.")
    if run["context"].get("profile") in ("extraction-miss", "correction"):
        render_source_correction(st, store, actor, root, run)
    analysis, source = st.columns([1.9, 1], gap="large")
    refs = compliance["references"]
    with analysis:
        tabs = st.tabs(WORKSPACE_TABS)
        with tabs[0]:
            synth = stages.get("synthesizer", {}).get("payload")
            from .readiness import render as render_readiness
            render_readiness(st,run,store,root,actor,review=not bool(run['context'].get('upload_origin')),evidence_available=packet is not None)
            st.info("Human credit review: " + (run.get('human_disposition') or run["outcome"].get("human_credit_review", "Not recorded")))
            st.write("**What to do next**")
            if live:
                from .live_workflow import _next_action
                st.write(_next_action(run["outcome"]))
            elif run["context"]["scenario_id"] == "E-F03" and run["status"] == "WAITING_REVIEW":
                st.write('Open the Human Review tab. The simulated Risk Manager must record supported exception handling, then the Authorized Approver can review and record Reject. The original policy Exception stays visible.')
            elif run["context"]["scenario_id"] == "E-P01" and run["status"] == "WAITING_REVIEW":
                st.write('Open Human Review: Risk Manager handles the exception; Authorized Approver prepares the registered condition; Risk Manager and Compliance Officer support it; Authorized Approver records Conditional Approve or Reject. Follow the next-role prompt. The condition remains outstanding.')
            elif run["context"].get("profile") == "extraction-miss":
                st.write("Inspect FIN-P2 and use Correct a value using its source above. The source contains the value; the extraction missed it. Save first, then explicitly update findings on the new revision.")
            elif run["status"] == "READY":
                st.write("Correction saved. The Analyst must explicitly Update affected findings above; no analysis has run for this revision.")
            else:
                st.write("Obtain the missing annual CFADS schedule; inspect the available facts and calculations below." if run["context"]["scenario_id"] == "E-M01" else "Verify the terms, calculations and policy results against their evidence, then read the recorded credit memo.")
            st.caption("Full-term repayment adequacy and portfolio concentration are not established by this sample.")
            st.button("Read credit memo", disabled=run["status"] != "COMPLETED", on_click=go, args=(st, "Credit Memo"))
        with tabs[1]:
            for name, term in terms(run).items():
                st.write("**" + name.replace("_", " ").title() + "**")
                st.text(term_value(name, term.get("value")))
                if refs:
                    references(st, [r for r in term.get("refs", []) if r in refs], "term:" + name)
                elif live:
                    st.caption("Sources: "+(", ".join(term.get("refs",[])) or "Not available"))
        with tabs[2]:
            if live and 'extractor' in stages:
                from ..contracts import parse_extraction
                extracted=parse_extraction(stages['extractor']['payload']['wire_json'])
                st.subheader('Financial inputs from uploaded documents' if run['context'].get('upload_origin') else 'Extracted financial inputs')
                st.caption('Automatically populated for all permitted roles. Extracted inputs are not yet human-verified; calculations appear after the required verification checkpoint.')
                st.dataframe([{'Financial input':name.replace('_',' ').title(),'Extracted value':fact.value if fact.value is not None else 'Not supplied','Reporting basis':fact.basis_id or 'Not supplied','Sources':', '.join(fact.refs)} for name,fact in extracted.financial_inputs],hide_index=True)
            metrics = [] if packet is None else packet["request"]["financial"]["metrics"]
            if not metrics:
                st.info("Calculated results are awaiting the required verification and analysis stages. Available extracted inputs are shown above." if live and 'extractor' in stages else "Financial details are not available from verified documents.")
            for metric in metrics:
                with st.container(border=True):
                    st.write("**" + METRIC_NAMES.get(metric["metric_id"], metric["metric_id"]) + "**")
                    st.metric("Recorded value · " + metric["unit"], metric.get("display") or "Not available")
                    with st.expander("Technical details"):
                        st.caption(metric["metric_id"] + " · " + metric["definition_version"] + " · " + metric["validity"])
                    st.text("Calculation: " + str(metric.get("numerator")) + " ÷ " + str(metric.get("denominator"))
                            + " × " + str(metric.get("multiplier")))
                    st.caption("Inputs: " + ", ".join(metric.get("inputs", [])))
                    references(st, [r for r in metric.get("source_refs", []) if r in refs], "metric:" + metric["metric_id"])
        with tabs[3]:
            if preliminary:
                from .uploaded_calculations import render_policy
                render_policy(st,preliminary)
            if compliance["basis"] == "POST_SYNTHESIS_RECORDED":
                st.caption("Recorded final policy evaluation · Same analytical basis as the credit memo.")
            elif compliance["basis"] == "PRE_SYNTHESIS_PRELIMINARY":
                st.warning("Preliminary policy evaluation · Synthesis-dependent checks may still be pending.")
            else:
                st.info("Policy checks have not run yet.")
            for rule in compliance["rules"]:
                with st.container(border=True):
                    st.write("**" + rule["ref"] + " · " + str(rule["result"] or "Pending") + "**")
                    st.text("Observed: " + str(rule["observed"]) + " | Threshold: " + str(rule["threshold"]))
                    st.text("Rule: " + str(rule["predicate"]))
                    st.caption("State: " + friendly(rule["state"]) + " · Workflow: " + friendly(rule["workflow"] or "Pending"))
                    if rule["workflow"] != "CONTINUE" and run["human_disposition"] is not None:
                        st.caption("Original referral retained · Human package review recorded: " + run["human_disposition"])
                    st.caption(rule["result_kind"] + " · " + rule["reason"])
                    if rule["ref"] in refs:
                        references(st, [rule["ref"]], "rule:" + rule["ref"])
        with tabs[4]:
            if preliminary:
                from .uploaded_calculations import render_risk
                render_risk(st,preliminary)
            for factor in risk.get("factors", []):
                with st.container(border=True):
                    st.write("**" + factor["factor_id"].replace("_", " ").title() + "**")
                    st.text("Rating " + factor["rating"] + "/100 · Weight " + str(Decimal(factor["weight"]) * 100)
                            + "% · Contribution " + factor["contribution"])
                    st.text(factor["reason"])
                    if refs:
                        references(st, [factor["assessment_id"]], "risk:" + factor["factor_id"])
            st.caption("Factor ratings are authored educational premises, not a trained predictive credit model.")
        with tabs[5]:
            if live:
                from .live_workflow import _review
                _review(st,root,actor,store,run["outcome"])
            else:
                render_financial_review(st, store, actor, root, run)
    with source:
        if live and not refs:
            from .live_workflow import _sources
            _sources(st,store,run["outcome"])
        else:
            evidence(st, refs)
    with st.expander("Technical details"):
        st.caption("Original artifacts retained unchanged. The compliance_check artifact precedes synthesis; current policy cards use the synthesizer's recorded final_policy when available.")
        st.json(stages)


def render_financial_review(st, store, actor, root, run):
    from ..financial_review import get_financial_review, record_financial_action, FinancialActionCommand
    from ..context import fingerprint
    from uuid import UUID, uuid5
    panel = get_financial_review(store, actor, run)
    if panel is None:
        if run["context"].get("profile") == "extraction-miss" or run["status"] == "READY":
            st.info("No human credit-decision request exists here. Use the source-backed correction controls above; a saved correction is not an approval.")
        elif run["context"]["scenario_id"] == "E-M01":
            st.info("This case is waiting for missing CFADS, not a human credit decision. Review comments and final decisions are unavailable in this sample; document continuation is not connected.")
        else:
            st.info("This Normal review has no human-review request, so comments and decisions are read-only. To type and submit a review, prepare a Human review required sample, run it as Analyst, then return here.")
            st.button("Prepare a review-required sample", on_click=prepare_review_sample, args=(st,))
        for col, label in zip(st.columns(3), ("Approve", "Reject", "Request More Information")):
            col.button(label, disabled=True, width="stretch")
        st.button("Return for Reassessment", disabled=True)
        return
    st.caption("Saved demo deal review · " + panel["data"]["status"] + " · Simulated role: " + actor.persona)
    notice = st.session_state.pop("review-saved:" + run["operation_id"], None)
    if notice:
        st.success(notice)
    render_exception_handling(st, actor, root, run, panel)
    if run["context"]["scenario_id"] == "E-P01":
        render_condition_review(st, actor, root, run, panel)
    if panel["data"]["information_pending"]:
        st.warning("Requested information is outstanding. Notes or a role change cannot clear it. " + ("A Risk Manager must assess a registered-source response." if run["context"]["scenario_id"] == "E-N01" else "Response/continuation for this scenario is not connected; final decisions stay blocked."))
        if actor.persona == "RiskManager" and run["status"] == "WAITING_INFORMATION" and run["context"]["scenario_id"] == "E-N01":
            render_information_response(st, store, actor, root, run, panel)
    actions = [action for action, reason in panel["actions"].items() if reason is None]
    if actions:
        labels = dict(ADD_COMMENT="Add Comment", APPROVE="Approve", REJECT="Reject", REQUEST_INFORMATION="Request Additional Information", CONDITIONAL_APPROVE="Conditional Approve")
        action = st.selectbox("Financial review action", actions, index=None, placeholder="Choose a permitted action", format_func=lambda value: labels[value])
        with st.form("financial-review-form:" + run["operation_id"] + ":" + str(action) + ":" + actor.persona):
            st.caption("Choose an action above, enter comments, then submit. Submit saves the current text without a separate blur or refresh.")
            comments = st.text_area("Financial review comments (required)", key="review-comments:" + run["operation_id"])
            items = st.text_area("Requested documents — one per line") if action == "REQUEST_INFORMATION" else ""
            confirmation = st.checkbox("Confirm this simulated final decision") if action in ("APPROVE", "REJECT", "CONDITIONAL_APPROVE") else True
            submitted = st.form_submit_button("Record financial review action", type="primary")
        if submitted:
            if not action or not comments.strip():
                st.error("Choose an action and enter review comments before submitting. Nothing was saved.")
                return
            if not confirmation:
                st.error("Confirm the simulated final decision before submitting. Nothing was saved.")
                return
            requested = [line.strip() for line in items.splitlines() if line.strip()]
            if action == "REQUEST_INFORMATION" and (not requested or len(set(requested)) != len(requested)):
                st.error("Enter at least one distinct requested document or clarification. Nothing was saved.")
                return
            request = panel["request"]
            operation = str(uuid5(UUID(request.request_id), fingerprint("FINANCIAL_UI_ACTION",
                dict(version=panel["version"], action=action, comments=comments, items=items, persona=actor.persona))))
            command = FinancialActionCommand(expected_readiness_version=run["approval_readiness"]["version"], expected_readiness_digest=run["approval_readiness"]["assessment_digest"], operation_id=operation, request_id=request.request_id,
                expected_version=panel["version"], expected_gate_version=request.gate_version,
                expected_basis=request.analytical_basis_digest, action=action, comments=comments,
                requested_items=requested)
            try:
                record_financial_action(root, actor, run["operation_id"], command)
            except (InputError, ValueError, OSError, sqlite3.Error):
                st.error("Action was not completed. Refresh the current review; any recorded decision is retained and will not be automatically replayed.")
            else:
                st.session_state["review-saved:" + run["operation_id"]] = "Review action saved with comments and timestamp."
                st.rerun()
    else:
        st.info("No decision action is permitted for this role or current state.")
    st.button("Return for Reassessment", disabled=True)
    st.caption("The Policy Exception example supports one unchanged source-backed condition. Arbitrary condition editing and changed/unregistered financial documents remain unavailable.")
    for event in panel["events"]:
        with st.expander(event["action"] + " · " + event["timestamp_utc"]):
            st.text(event["reviewer_name"] + " · " + event["previous_status"] + " → " + event["new_status"])
            st.text(event["comments"])
            if event["requested_items"]:
                st.text("Requested: " + "; ".join(event["requested_items"]))


def render_source_correction(st, store, actor, root, run):
    from ..source_correction import (SaveCorrectionCommand, UpdateCorrectionCommand, correction_basis,
        draft_basis, save_source_correction, update_affected_findings)
    from ..context import fingerprint
    from uuid import UUID, uuid5
    with st.container(border=True):
        st.subheader("Correct a value using its source")
        if run["context"].get("profile") == "correction":
            version, draft = store.get_record("source-correction:" + run["operation_id"])
            event = store.get_record("financial-review-event:" + draft["event_id"])[1]
            st.text("CFADS: Missing → " + event["corrected_fact"]["value"] + " USD · FY-ASSESS · FIN-P2")
            st.text("Reviewer: " + event["reviewer_name"] + " · Saved " + event["timestamp_utc"])
            st.text("Reason: " + event["comments"])
            references(st, ["FIN-P2"], "saved-correction")
            if run["status"] == "READY":
                st.warning("Saved, not analysed. Financial metrics, policies, risk, recommendation and memo must be updated. No model call occurred on Save.")
                if st.button("Update affected findings", disabled=actor.persona != "Analyst", type="primary"):
                    try:
                        with st.spinner("Recalculating affected findings from the saved correction…"):
                            update_affected_findings(root, actor, run["operation_id"], UpdateCorrectionCommand(expected_version=version, expected_basis=draft_basis(draft)))
                    except (InputError, ValueError, OSError, sqlite3.Error):
                        st.error("Update was not completed. Refresh to inspect current state; no automatic retry or budget reset occurred.")
                    else:
                        st.rerun()
            else:
                st.caption("Reviewer-corrected revision. Original extraction remains historical; this is not an original model-quality result.")
            return
        if run["status"] == "SUPERSEDED":
            st.info("This extraction is historical and has been superseded by a saved correction.")
            operation = run["outcome"].get("correction_operation")
            if operation:
                st.button("Open corrected revision", on_click=open_run, args=(st, operation))
            return
        st.warning("Extraction missed CFADS. DSCR and the complete score are unavailable until the original source is reviewed.")
        references(st, ["FIN-P2"], "correction-source")
        st.caption("Only the registered annual CFADS correction is supported. No new documents, unsupported values or other field edits.")
        if actor.persona != "Analyst" or run["status"] != "WAITING_INFORMATION":
            st.info("Required role: Analyst (simulated).")
            return
        with st.form("save-correction:" + run["operation_id"]):
            value = st.text_input("Corrected CFADS (USD whole units)")
            basis = st.selectbox("Correction financial basis", ("FY-ASSESS",), index=None)
            ref = st.selectbox("Correction source page", ("FIN-P2",), index=None)
            comments = st.text_area("Correction reason (required)")
            confirmed = st.checkbox("I verified this value in the original cited document")
            submitted = st.form_submit_button("Save source-backed correction")
        if submitted:
            if not value.strip() or not comments.strip() or not basis or not ref or not confirmed:
                st.error("Enter the documented value, basis, page and reason, then confirm verification. Nothing was saved.")
                return
            version = store.get_record("normal-result:" + run["operation_id"])[0]
            operation = str(uuid5(UUID(run["operation_id"]), fingerprint("CORRECTION_UI_SAVE", dict(version=version, value=value, basis=basis, ref=ref, comments=comments))))
            try:
                saved = save_source_correction(root, actor, run["operation_id"], SaveCorrectionCommand(operation_id=operation,
                    expected_version=version, expected_basis=correction_basis(run), field="cash_available_for_debt_service",
                    value=value.strip(), basis_id=basis, evidence_ref=ref, comments=comments))
            except (InputError, ValueError, OSError, sqlite3.Error):
                st.error("Correction was not saved. This sample accepts only the exact registered CFADS value, basis and original page. Refresh if the run changed.")
            else:
                st.session_state.next_financial_run = saved["operation_id"]
                st.rerun()


def render_exception_handling(st, actor, root, run, panel):
    from ..financial_review import ExceptionHandlingCommand, handling_references, record_exception_handling
    from ..context import fingerprint
    from uuid import UUID, uuid5
    requirements = [r for r in panel["request"].requirements if r.key.startswith("exception:")]
    conditional = run["context"]["scenario_id"] == "E-P01"
    handling = "ACCEPT_FOR_CONDITIONAL_REVIEW" if conditional else "RECOMMEND_REJECT"
    handling_label = "Accept for conditional review" if conditional else "Recommend Reject"
    if not requirements:
        return
    st.subheader("Policy exception handling")
    st.caption('Handling preserves the original Exception. Risk Manager recommends; Authorized Approver makes the separate final decision.')
    for requirement in requirements:
        rule_id = requirement.key.split(":", 1)[1]
        if requirement.satisfied:
            st.success(rule_id + " · Handling recorded: " + handling_label + ". Original policy outcome remains Exception.")
            continue
        st.warning(rule_id + ' · Risk Manager handling required. Approve and Reject are blocked until this gate is handled.')
        if actor.persona != "RiskManager" or run["status"] != "WAITING_REVIEW" or panel["data"]["information_pending"]:
            continue
        packet = source_packet(root, run)
        rule = next(r for r in run["artifacts"]["synthesizer"]["payload"]["routing"]["final_policy"]["rules"] if r["rule_id"] == rule_id)
        refs = handling_references(rule)
        if conditional:
            st.caption("Registered condition: Supply annual financial statements. This does not cure DSCR; specialist support and final review are still required.")
            references(st, ["E-P01:AGREEMENT-P1"], "conditional-handling-source")
        st.text("Observed " + str(rule["observed"]) + " · " + rule["predicate"] + " · " + rule["workflow"])
        references(st, refs, "handling:" + rule_id)
        with st.form("exception-handling-form:" + run["operation_id"] + rule_id):
            selected = st.multiselect("Exception supporting evidence", refs, key="exception-refs:" + run["operation_id"] + rule_id,
                format_func=lambda ref: packet["request"]["reference_dictionary"][ref]["label"])
            comments = st.text_area("Risk Manager handling reason (required)", key="exception-comments:" + run["operation_id"] + rule_id)
            acknowledged = st.checkbox("I acknowledge this condition does not cure the DSCR exception") if conditional else True
            submitted = st.form_submit_button("Record exception handling · " + handling_label)
        if submitted:
            if not comments.strip() or set(selected) != set(refs) or not acknowledged:
                st.error("Select all supporting references and enter a handling reason. Nothing was saved.")
                return
            request = panel["request"]
            operation = str(uuid5(UUID(request.request_id), fingerprint("EXCEPTION_HANDLING_UI", dict(
                version=panel["version"], gate=request.gate_version, rule=rule_id, comments=comments, refs=sorted(selected)))))
            command = ExceptionHandlingCommand(operation_id=operation, request_id=request.request_id,
                expected_version=panel["version"], expected_gate_version=request.gate_version, expected_basis=request.analytical_basis_digest,
                rule_id=rule_id, handling=handling, comments=comments, evidence_refs=selected)
            try:
                record_exception_handling(root, actor, run["operation_id"], command)
            except (InputError, ValueError, OSError, sqlite3.Error):
                st.error("Handling was not completed. Refresh the review and verify its source version, role and gate.")
            else:
                st.session_state["review-saved:" + run["operation_id"]] = 'Risk Manager handling saved. The Authorized Approver must make the separate final decision.'
                st.rerun()


def render_condition_review(st, actor, root, run, panel):
    from ..conditional_review import supported_condition, DOMAINS, record_condition_action
    from ..financial_review import ConditionActionCommand
    from ..context import fingerprint
    from uuid import UUID, uuid5
    st.subheader("Review conditions and supporting evidence")
    text, refs = supported_condition(run["artifacts"]["synthesizer"]["payload"])
    st.write("**" + text + "**")
    st.caption("OUTSTANDING · Owner: Unassigned · Source covenant: EXTRACTED_NOT_EVALUATED. Annual statements do not cure DSCR. No funding authorization.")
    references(st, refs, "condition-review")
    draft = panel["data"].get("condition_draft")
    if any(not r.satisfied for r in panel["request"].requirements if r.key.startswith("exception:")):
        st.info('Next: Risk Manager must record exception handling above.')
        return
    if draft is None:
        action, domain, label = "CONDITION_DRAFT_PREPARED", None, "Prepare registered condition draft"
        role = "AuthorizedApprover"
    else:
        pending = []
        for name, role_name in DOMAINS.items():
            requirement = next(r for r in panel["request"].requirements if r.key == "draft:" + draft["targets"][0]["target_id"] + ":" + name)
            st.write(name.replace("_", " ").title() + ": " + ("Supported" if requirement.satisfied else "Awaiting " + role_name))
            if not requirement.satisfied:
                pending.append((name, role_name))
        if not pending:
            st.success('Both specialist reviews recorded. Authorized Approver may choose Conditional Approve or Reject. The condition remains outstanding.')
            return
        eligible = next(((name, role_name) for name, role_name in pending if role_name == actor.persona), pending[0])
        domain, role = eligible
        action, label = "CONDITION_SUPPORTED", "Record " + domain.replace("_", " ").title() + " support"
    st.info("Next required role: " + role + " (simulated).")
    if actor.persona != role or run["status"] != "WAITING_REVIEW" or panel["data"]["information_pending"]:
        return
    with st.form("condition-form:" + run["operation_id"] + ":" + action + ":" + str(domain)):
        comments = st.text_area("Condition review reason (required)")
        selected = st.multiselect("Condition supporting evidence", refs)
        confirmed = st.checkbox("I verified the unchanged condition and acknowledge it does not cure DSCR or authorize funding")
        submitted = st.form_submit_button(label)
    if submitted:
        if not comments.strip() or set(selected) != set(refs) or not confirmed:
            st.error("Enter a reason, select every supporting reference and confirm the review. Nothing was saved.")
            return
        request = panel["request"]
        operation = str(uuid5(UUID(request.request_id), fingerprint("CONDITION_UI_ACTION", dict(version=panel["version"], action=action, domain=domain, comments=comments))))
        command = ConditionActionCommand(operation_id=operation, request_id=request.request_id, expected_version=panel["version"],
            expected_gate_version=request.gate_version, expected_basis=request.analytical_basis_digest, action=action,
            condition_text=text, evidence_refs=selected, comments=comments, domain=domain, draft_digest=None if draft is None else draft["content_digest"])
        try:
            record_condition_action(root, actor, run["operation_id"], command)
        except (InputError, ValueError, OSError, sqlite3.Error):
            st.error("Condition review was not completed. Refresh and check role, evidence and current version.")
        else:
            st.session_state["review-saved:" + run["operation_id"]] = "Condition review saved with comments and timestamp."
            st.rerun()


def render_information_response(st, store, actor, root, run, panel):
    from ..financial_review import InformationResponseCommand, respond_and_reassess
    from ..context import fingerprint
    from uuid import UUID, uuid5
    from hashlib import sha256
    with st.expander("Assess registered document response", expanded=True):
        st.caption("Educational path: exact registered PDF only. This does not accept new financial facts or a newer statement. Confirm each requested item against its original page.")
        try:
            packet = source_packet(root, run)
        except (InputError, ValueError, OSError):
            st.error("Registered source version is unavailable; response cannot be accepted.")
            return
        refs = [key for key, value in packet["request"]["reference_dictionary"].items() if value["kind"] == "SOURCE"]
        items = [item for event in panel["events"] if event["action"] == "REQUEST_INFORMATION" for item in event["requested_items"]]
        pack = (root / "fixtures/development/e-n01").resolve()
        manifest = strict_json((pack / "manifest.json").read_bytes())
        with st.expander("Registered PDF examples for this response"):
            for source in manifest["sources"]:
                path = (pack / source["path"]).resolve()
                if not path.is_relative_to(pack):
                    raise InputError("SOURCE_PATH_OUT_OF_SCOPE")
                raw = path.read_bytes()
                if sha256(raw).hexdigest() != source["content_digest"]:
                    raise InputError("REGISTERED_SOURCE_CHANGED")
                st.download_button("Download registered source " + source["source_id"], raw,
                                   file_name=path.name, mime="application/pdf")
        upload = st.file_uploader("Registered PDF response", type=["pdf"], key="response-file:" + run["operation_id"])
        mapped = [st.selectbox("Evidence for request " + str(index + 1) + ": " + item, refs, index=None,
                              key="response-ref:" + run["operation_id"] + ":" + str(index)) for index, item in enumerate(items)]
        comments = st.text_area("Risk Manager response assessment (required)", key="response-assessment:" + run["operation_id"])
        if st.button("Accept registered response and reassess", disabled=not (upload and comments.strip() and mapped and all(mapped))):
            raw = upload.getvalue()
            operation = str(uuid5(UUID(panel["request"].request_id), fingerprint("REGISTERED_RESPONSE_UI",
                dict(version=panel["version"], comments=comments, refs=mapped, document=sha256(raw).hexdigest()))))
            command = InformationResponseCommand(operation_id=operation, expected_version=panel["version"],
                expected_basis=panel["request"].analytical_basis_digest, comments=comments, reference_by_item=mapped)
            try:
                outcome = respond_and_reassess(root, actor, run["operation_id"], command, raw)["outcome"]
            except (InputError, ValueError, OSError, sqlite3.Error):
                st.error("Response not accepted. Check the exact registered PDF, every requested-item reference, current version and remaining correction allowance.")
            else:
                st.session_state.next_financial_run = operation
                st.rerun()


def activity(st, run):
    st.caption("Recorded workflow execution · Not a live progress stream")
    completed = {e["stage"] for e in run["events"] if e["event"] == "stage_completed"}
    started = {e["stage"] for e in run["events"] if e["event"] == "stage_started"}
    reused = {e["stage"] for e in run["events"] if e["event"] == "artifact_reused"}
    stage_order = STAGES if run["context"]["variant"] != "review" else STAGES[:-1] + ("review_prepare", "human_review", "report_generator")
    for offset in range(0, len(stage_order), 3):
        for col, stage in zip(st.columns(3), stage_order[offset:offset + 3]):
            corrected = any(e["stage"] == stage and e["event"] == "reviewer_correction_applied" for e in run["events"])
            state = "Reviewer correction applied" if corrected else "Reused · identical registered inputs" if stage in reused else "Completed" if stage in completed else ("Started · no completion recorded" if stage in started else "Not started")
            css = "stage-done" if stage in completed else ("stage-active" if stage in started else "")
            col.markdown('<div class="stage ' + css + '"><div class="stage-num">STEP ' + str(stage_order.index(stage) + 1)
                         + '</div><div class="stage-name">' + safe(STAGE_NAMES[stage])
                         + '</div><div class="stage-state">' + safe(state) + '</div></div>', unsafe_allow_html=True)
    if run["status"] == "RECOVERY_REQUIRED":
        last = next((s for s in reversed(stage_order) if s in completed), None)
        st.warning("Last completed stage: " + (STAGE_NAMES[last] if last else "None")
                   + ". Retain this operation ID for investigation; automatic replay is disabled.")
    st.subheader("Review progress timeline")
    st.dataframe([{"#": e["sequence"], "Stage": STAGE_NAMES[e["stage"]], "Event": friendly(e["event"]),
                   "Time (UTC)": e.get("timestamp", "Not captured"), "Processing time (milliseconds)": e.get("active_ms")}
                  for e in run["events"]], hide_index=True, width="stretch")
    with st.expander("Technical details: agent results"):
        stage = st.selectbox("Agent output", list(run["artifacts"]), format_func=lambda s: STAGE_NAMES[s]) if run["artifacts"] else None
        if stage:
            artifact = run["artifacts"][stage]
            st.caption("Input digest: " + artifact["input_digest"])
            st.caption("Output digest: " + artifact["content_digest"])
            st.json(artifact["payload"])
    st.caption("This recorded review used saved AI responses: 0 model calls. A live test will report its actual calls, token usage, cost and response time separately.")


def history(st, runs, selected, store, actor):
    from datetime import datetime, timezone
    from ..financial_review import (financial_history, financial_history_csv,
        FinancialHistoryFilters, query_financial_history)
    from ..context import fingerprint
    from pydantic import ValidationError
    st.caption("Business decisions across your permitted deals · Simulated identities")
    st.caption("Selected review source: "+("Live AI response · Nebius" if selected["context"].get("mode")=="LIVE" else "Saved AI responses"))
    from .live_workflow import _history
    for live in runs:
        if live["context"].get("mode")=="LIVE" and live["context"]["scope"]["deal_id"]==selected["context"]["scope"]["deal_id"]:
            with st.expander("Live AI response · "+live["context"]["generation_time"],expanded=live["operation_id"]==selected["operation_id"]):
                _history(st,store,live["outcome"],live["context"]["scope"])
    deal_id = selected["context"]["scope"]["deal_id"]
    from .readiness import render as render_readiness
    render_readiness(st,selected,store)
    with st.expander("Readiness assessment history"):
        with store.connection() as connection:
            rows=connection.execute("SELECT payload FROM app_records WHERE kind='READINESS_ASSESSMENT'").fetchall()
        snapshots=[strict_json(row[0],envelope=True) for row in rows]
        for snapshot in sorted((v for v in snapshots if v["scope"]==selected["context"]["scope"]),key=lambda v:v["version"]):
            st.write("Version "+str(snapshot["version"])+" - "+snapshot["outcome"]+" - "+str(snapshot["evaluated_at_utc"]));st.caption(snapshot["reason"])
    events = financial_history(store, actor)
    decisions = [event for event in events if event["decision"] is not None]
    live_decisions=[record for r in runs if r["context"].get("mode")=="LIVE" for record in [store.get_record("live-credit:"+r["context"]["scope"]["run_id"])] if record]
    decision_count=len(decisions)+len(live_decisions)
    surface(st, "Human decision history", str(decision_count) + " recorded decision(s)" if decision_count else "No human decisions recorded",
            "Pipeline completion does not approve or reject a loan. All identities are simulated.")
    if events:
        with st.expander("Search and filter decision history", expanded=True):
            a, b, c = st.columns(3)
            deal_search = a.text_input("History Deal ID")
            borrower = b.text_input("History borrower")
            reviewer = c.text_input("History reviewer or role")
            actions = a.multiselect("History actions", ("ADD_COMMENT", "APPROVE", "REJECT", "REQUEST_INFORMATION", "INFORMATION_RESPONSE", "EXCEPTION_DISPOSITION", "CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED", "CONDITIONAL_APPROVE", "SOURCE_CORRECTION_SAVED", "CORRECTION_APPLIED"))
            statuses = b.multiselect("History statuses", ("AWAITING_DECISION", "PENDING_INFORMATION", "APPROVED", "REJECTED", "SUPERSEDED_BY_REASSESSMENT", "CONDITIONALLY_APPROVED", "READY", "SUPERSEDED_BY_CORRECTION", "UPDATED_FINDINGS_REQUESTED"))
            date_filter = c.checkbox("Filter by UTC dates")
            utc_today = datetime.now(timezone.utc).date()
            start = a.date_input("History start date (UTC)", value=utc_today) if date_filter else None
            end = b.date_input("History end date (UTC)", value=utc_today) if date_filter else None
            try:
                filters = FinancialHistoryFilters(deal_id=deal_search, borrower=borrower, reviewer=reviewer,
                    actions=actions, statuses=statuses, start_date=start, end_date=end)
            except ValidationError:
                st.error("Choose a start date on or before the end date. No export is available for an invalid filter.")
                return
        size = st.selectbox("History page size", (10, 25, 50, 100), index=1)
        first = query_financial_history(store, actor, filters, limit=size)
        pages = max(1, (first["total"] + size - 1) // size)
        page = st.selectbox("History page", list(range(1, pages + 1)))
        result = first if page == 1 else query_financial_history(store, actor, filters, offset=(page - 1) * size, limit=size)
        st.caption(str(result["total"]) + " matching event(s) · Export includes every matching page, up to the 5,000-event safety limit.")
        visible = result["rows"]
        if visible:
            st.dataframe([dict(Time=e["timestamp_utc"], Deal=e["scope"]["deal_id"],
                Borrower=e["analysis_snapshot"].get("deal", {}).get("borrower") or "Not captured",
                Action=e["action"], Previous=e["previous_status"], Status=e["new_status"],
                Reviewer=e["reviewer_name"], Role=e["reviewer_role"], Comments=e["comments"])
                for e in visible], hide_index=True, width="stretch")
            event_id = st.selectbox("Financial decision event", [e["operation_id"] for e in visible])
            event = next(e for e in visible if e["operation_id"] == event_id)
            st.text(event["comments"])
            st.caption(event["previous_status"] + " → " + event["new_status"] + " · " + event["timestamp_utc"])
            if event["action"] == "EXCEPTION_DISPOSITION":
                st.write("**Exception handling:** " + event["rule_id"] + " · " + event["handling"])
                st.caption("Original policy outcome remains Exception. Supporting references: " + ", ".join(event["evidence_refs"]))
            if event.get("condition_record"):
                st.json(event["condition_record"])
            if event.get("corrected_fact"):
                st.write("Reviewer-corrected field: " + event["field"])
                st.json(dict(original=event["old_fact"], corrected=event["corrected_fact"]))
            if event.get("condition_text"):
                st.write(event["condition_text"])
                st.caption("Review area: " + friendly(event.get("domain") or "Draft preparation") + " · " + ", ".join(event["evidence_refs"]))
            original = event["analysis_snapshot"]
            ai = original.get("ai", {})
            if ai.get("wire_json"):
                recommendation = parse_synthesis(ai["wire_json"]).panel_decision
                st.write("**Original AI proposal at this event:** " + recommendation.decision)
                st.caption("Readiness at decision: "+event.get("approval_readiness",{}).get("outcome","Not captured for this historical event"))
                st.caption("Original model-stage confidence: " + str(recommendation.confidence) + " · Not a human decision")
            else:
                st.caption("AI recommendation at this event: Not captured")
            original_risk = original.get("risk", {}).get("score", {})
            st.caption("Credit risk at this event: " + (original_risk.get("display") or "Not captured")
                       + " · " + (original_risk.get("band") or "Not captured"))
            if event["requested_items"]:
                st.write("Requested information:")
                for item in event["requested_items"]:
                    st.text(item)
            with st.expander("Technical details: original analysis and source identifiers"):
                st.json(event["analysis_snapshot"])
            if any(r["operation_id"] == event["run_operation"] for r in runs):
                st.button("Open original review and evidence", on_click=open_run, args=(st, event["run_operation"]))
        else:
            st.info("No history events match these filters. Clear filters to see permitted records.")
        cache_id = fingerprint("FINANCIAL_CSV_UI", dict(actor=actor.persona, workspace=actor.workspace_id,
                               allowed=actor.allowed_deal_ids, filters=filters.model_dump(), snapshot=result["snapshot_digest"]))
        if st.button("Prepare financial history CSV", disabled=not result["total"]):
            st.session_state.financial_csv = dict(key=cache_id, data=financial_history_csv(store, actor, None,
                expected_digest=result["snapshot_digest"], filters=filters))
        cache = st.session_state.get("financial_csv")
        if cache and cache["key"] == cache_id:
            st.download_button("Download financial history CSV", cache["data"], "financial-decision-history.csv", "text/csv")
        with st.expander("Complete selected-deal decision timeline (independent of filters)"):
            timeline = financial_history(store, actor, deal_id)
            if not timeline:
                st.info("No recorded review actions for the selected deal.")
            else:
                timeline_id = st.selectbox("Timeline event", [e["operation_id"] for e in timeline],
                    format_func=lambda key: next(e["timestamp_utc"] + " · " + e["action"] for e in timeline if e["operation_id"] == key))
                original = next(e for e in timeline if e["operation_id"] == timeline_id)
                st.text(original["comments"])
                st.json(original["analysis_snapshot"])
    st.caption("Illustrative preview records are excluded from this financial history.")
    st.subheader("Recorded review milestones")
    for run in reversed(runs):
        if run["context"]["scope"]["deal_id"] != selected["context"]["scope"]["deal_id"]:
            continue
        final = next((e for e in reversed(run["events"]) if e["stage"] == "report_generator" and e["event"] == "stage_completed"), None)
        stamp = final.get("timestamp", "Not captured") if final else run["context"]["generation_time"]
        st.markdown('<div class="milestone"><strong>' + safe(friendly(run["status"]))
                    + '</strong><div class="surface-note">' + safe(stamp) + '<br>Run '
                    + safe(run["context"]["scope"]["run_id"]) + '<br>No human decision inferred.</div></div>', unsafe_allow_html=True)
    st.caption("History is saved on this computer and is not tamper-proof.")


def main(workspace: Path):
    import streamlit as st

    st.set_page_config(page_title="Deal or No Deal AI", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    config = load_configuration(workspace)
    store = Store(config.database)
    with st.sidebar:
        st.markdown('<div class="brand">Deal or No Deal<span class="brand-accent"> AI</span></div>'
                    '<div class="brand-sub">AI CREDIT INTELLIGENCE</div>', unsafe_allow_html=True)
        st.divider()
        page = st.radio("Page", PAGES, key="financial_page")
        st.divider()
        persona = st.selectbox("Demo role", ROLES, format_func=friendly)
        st.caption("DEMO MODE · Simulated role\n\nNot authenticated lending authority.")
        st.caption("Every deal has a story. Our agents find the plot holes.")
        st.divider()
        with st.expander("Live AI demo: setup and readiness"):
            st.write("The live demo will test the complete coordinated workflow using fictional deal documents. Extraction and synthesis use Nebius model calls; policy checks, financial calculations, risk scoring, routing and report assembly run in Python.")
            st.info("New reviews follow mode in config/app.toml: FIXTURE uses saved example answers; LIVE uses Nebius. Provider verification and exact token limits are required before paid calls. An API key alone does not start a review.")
            st.caption("Generation: Qwen/Qwen3-30B-A3B-Instruct-2507 · Embeddings: Qwen/Qwen3-Embedding-8B · Approved shared test ceiling: USD0.10.")
            st.caption("Configure NEBIUS_API_KEY in the ignored project .env file. Readiness does not send a request or enable Live mode.")
            from .live_setup_panel import render as render_live_setup
            render_live_setup(st,config.workspace)
    mode_banner = 'New reviews use Nebius - paid calls only on explicit Run or Continue' if config.mode == 'LIVE' else 'New reviews use saved example answers - no model calls'
    st.markdown('<div class="eyebrow">Workspace / Commercial lending</div>'
                '<div class="demo-strip">EDUCATIONAL DEMO · Prepared fictional sample deals · Current mode: ' + mode_banner + '</div>', unsafe_allow_html=True)
    registry = strict_json((config.workspace / "config/registrations/e-n01.json").read_bytes())
    permitted = {registry["deal_id"]}
    missing_registry = config.workspace / "config/registrations/e-m01.json"
    if missing_registry.exists():
        permitted.add(strict_json(missing_registry.read_bytes())["deal_id"])
    reject_registry = config.workspace / "config/registrations/e-f03.json"
    if reject_registry.exists():
        permitted.add(strict_json(reject_registry.read_bytes())["deal_id"])
    conditional_registry = config.workspace / "config/registrations/e-p01.json"
    if conditional_registry.exists():
        permitted.add(strict_json(conditional_registry.read_bytes())["deal_id"])
    from ..upload_live import uploaded_deal_ids
    reader=Actor(persona,workspace_id(config.workspace),frozenset(permitted))
    permitted.update(uploaded_deal_ids(config.workspace,reader))
    actor = Actor(persona, workspace_id(config.workspace), frozenset(permitted),
                  frozenset({"NORMAL"}) if persona == "AuthorizedApprover" else frozenset())
    try:
        if page == "New Deal":
            new_deal(st, config.workspace, actor)
            return
        runs = list_runs(store, actor)
        from ..live_worker import list_live
        runs += [get_run(store,actor,state["context"]["operation_id"]) for state in list_live(config.workspace,actor)]
        runs.sort(key=lambda run:(run["context"]["generation_time"],run["operation_id"]),reverse=True)
        if page == "Deal Dashboard":
            from .dashboard import render
            render(st, runs, store, actor, {**METRIC_NAMES, **STAGE_NAMES})
            return
        st.header(page)
        if not runs:
            surface(st, "No recorded review", "Your next step: start a sample deal", "Findings, activity and the memo appear after an explicit run.")
            st.button("Go to New Deal", on_click=go, args=(st, "New Deal"))
            return
        operation = select_deal_review(st, runs)
        run = get_run(store, actor, operation)
        live=run["context"].get("mode")=="LIVE"
        context_header(st, run, terms(run),answer_source="Live AI response · Nebius" if live else "Saved AI responses")
        if run['context'].get('upload_origin'):
            st.caption('Uploaded deal · Deal ID: '+run['context']['scope']['deal_id']+' · Analysis uses the retained uploaded documents.')
            from .uploaded_calculations import render as render_uploaded_calculations
            render_uploaded_calculations(st,config.workspace,actor,run,METRIC_NAMES)
            with st.expander('Uploaded document citation map'):
                st.dataframe([dict(Reference=k,File=v['filename'],Page=v['page'],Uploaded_reference=v['upload_ref']) for k,v in run['context']['upload_origin']['page_map'].items()],hide_index=True)
        if run["context"].get("verification_policy")=="DEMO_DRAFT":
            st.info("Unverified live demo draft. Automated integrity checks are complete for recorded stages; human evidence verification and a credit decision have not been recorded.")
        if run["status"] == "RECOVERY_REQUIRED":
            quarantine = run["outcome"].get("quarantine") if live else None
            if quarantine:
                st.warning("This interrupted attempt has been set aside and cannot run again. Its AI response and actual cost remain unknown; USD0.0007 remains reserved. Other reviews can continue. This is not a lending rejection.")
                with st.expander("Why this attempt was set aside"):
                    st.write(quarantine["reason"])
                    st.caption(quarantine["reviewer_name"] + " · " + quarantine["timestamp_utc"] + " · Simulated administrative action")
                candidates = [r for r in runs if r["context"].get("mode")=="LIVE"
                    and r["context"]["scope"]["deal_id"]==run["context"]["scope"]["deal_id"]
                    and r["status"]=="WAITING_EVIDENCE" and r["outcome"].get("pending_stage")=="fact_review"]
                if candidates:
                    st.button("Open live review awaiting fact verification",on_click=_use_review,args=(st,candidates[0]["operation_id"]))
            else:
                st.error("Execution needs recovery. Partial findings are not a final report. Retain the run ID; no automatic reset or replay is performed.")
        if page == "Agent Activity":
            from .specialists import render as render_specialists
            render_specialists(st,run)
            if live:
                state=run["outcome"]
                st.dataframe([dict(Step=friendly(e["stage"]),Status="Completed",Time_UTC=e["timestamp"]) for e in state["events"]],hide_index=True)
                if state["pending_stage"]:
                    st.info("Paused for: "+friendly(state["pending_stage"]))
                with st.expander("Technical details: original AI responses"):
                    for stage in ("extractor","synthesizer"):
                        if stage in run["artifacts"]:
                            st.write(stage)
                            st.code(run["artifacts"][stage]["payload"]["wire_json"],language="json")
            else:
                activity(st, run)
            from .quality import render as render_quality
            render_quality(st,config.workspace,run["context"]["scope"])
        elif page == "Decision History":
            history(st, runs, run, store, actor)
        elif page == "Credit Memo":
            from .readiness import render as render_readiness
            render_readiness(st,run,store)
            st.caption("The recorded memo is a snapshot from its generation time. Current readiness and later human decisions are shown above; historical memo content is preserved.")
            report = run["outcome"].get("report_markdown")
            if run["status"] == "COMPLETED" and report:
                with st.container(border=True):
                    st.caption("CREDIT REVIEW MEMORANDUM · "+("Live AI response · Nebius" if live else "Saved demo output")+" · Final human decision: " + (run["human_disposition"] or "Not recorded"))
                    meta = run["outcome"]["report_metadata"]
                    with st.expander("Technical details"):
                        st.caption("Report format version " + meta["renderer_version"] + " · Generated " + meta["generation_time"])
                    st.markdown(report, unsafe_allow_html=False)
                st.download_button("Download recorded memo", report, file_name="educational-credit-memo.md", mime="text/markdown", type="primary")
                if run['context'].get('upload_origin'):
                    from ..financial_review import financial_history
                    if any(e['run_operation']==run['operation_id'] for e in financial_history(store,actor,run['context']['scope']['deal_id'])):
                        from ..uploaded_decisions import memo_with_review_history
                        st.download_button('Download memo with review history',memo_with_review_history(config.workspace,actor,run['operation_id']),file_name='credit-memo-with-review-history.md',mime='text/markdown')
                st.button("Validate memo evidence", on_click=go, args=(st, "Review Workspace"))
            else:
                st.info("No completed memo is available for this run.")
        else:
            try:
                packet = None if live and "synthesizer" not in run["artifacts"] else source_packet(config.workspace, run)
            except (InputError, ValueError, OSError):
                packet = None
            render_workspace(st, run, packet, store, actor, config.workspace)
    except (InputError, RunBusy, ValueError, OSError, sqlite3.Error):
        st.error("This review is unavailable, its sources changed, or another execution needs attention. Retain the operation/run ID for diagnosis. No reset or automatic retry occurred.")
