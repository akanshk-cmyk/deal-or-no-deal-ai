"""Read-only dashboard projection and presentation; no execution entry points."""
from .labels import friendly, FINANCIAL_HELP, case_label


from datetime import datetime, timezone
from decimal import Decimal

from ..command_center import policy_display
from ..contracts import parse_synthesis
from ..financial_review import get_financial_review


def project_deals(runs):
    groups = {}
    for run in sorted(runs, key=lambda r: (r["context"]["generation_time"], r["operation_id"]), reverse=True):
        groups.setdefault(run["context"]["scope"]["deal_id"], []).append(run)
    rows = []
    for deal_id, history in groups.items():
        run = history[0]
        artifacts = run["artifacts"]
        from .command_center import terms as review_terms
        terms = review_terms(run)
        risk = artifacts.get("risk_quantifier", {}).get("payload", {}).get("score", {})
        policy = policy_display(run, None)
        status = run["status"]
        decision = run.get("human_disposition") or {
            "WAITING_REVIEW": "Awaiting Decision", "WAITING_INFORMATION": "Pending Information",
            "SUPERSEDED": "Superseded"}.get(status, "Not recorded")
        exceptions = policy["exception_rule_ids"]
        high = risk.get("band") in ("HIGH", "VERY_HIGH", "VERY HIGH")
        if run.get("outcome",{}).get("quarantine"):
            priority, next_action, owner = 0, "This attempt was set aside. Open its history and select the earlier live review awaiting fact verification; do not restart this attempt.", "Administrative abandonment recorded"
        elif status in ("RECOVERY_REQUIRED","MODEL_OUTPUT_INVALID"):
            priority, next_action, owner = 0, "Inspect execution recovery details; do not record a lending rejection", "Technical recovery — not assigned"
        elif run["context"].get("mode")=="LIVE" and status!="COMPLETED":
            from .live_workflow import _next_action
            priority,next_action,owner=1,_next_action(run["outcome"]),"Follow the required simulated role"
        elif status == "WAITING_INFORMATION":
            priority, next_action, owner = 1, "Assess the requested registered information response", 'Risk Manager (simulated required role)'
            if run["context"]["scenario_id"] == "E-M01":
                next_action, owner = "Obtain the missing 2027 CFADS schedule; continuation is not connected", "Analyst (simulated required role)"
            elif run["context"].get("profile") == "extraction-miss":
                next_action, owner = "Inspect original FIN-P2 and save the supported CFADS correction", "Analyst (simulated required role)"
        elif status == "READY":
            priority, next_action, owner = 1, "Explicitly Update affected findings for the saved correction", "Analyst (simulated required role)"
        elif status == "WAITING_REVIEW":
            priority, next_action, owner = 2, "Validate findings and record a permitted human decision", 'Authorized Approver (simulated required role)'
            if run.get("unhandled_exception_ids"):
                next_action, owner = "Inspect the supported policy exception and record handling before a final decision", 'Risk Manager (simulated required role)'
            elif run.get("pending_condition_roles"):
                next_action, owner = "Review the unchanged source-backed condition; specialist checks are required before a final decision", ", ".join(run["pending_condition_roles"]) + " (simulated required role)"
        elif exceptions:
            priority, next_action, owner = 3, "Inspect recorded policy exceptions and required checks and approvals", "Not assigned"
        elif high:
            priority, next_action, owner = 4, "Inspect risk drivers and recorded routing requirements", "Not assigned"
        else:
            priority, next_action, owner = 5, "Inspect recorded findings and credit memo", "Not assigned"
        readiness=run.get("approval_readiness")
        if readiness and not readiness["approval_eligible"] and status not in ("RECOVERY_REQUIRED","MODEL_OUTPUT_INVALID","WAITING_INFORMATION","WAITING_EVIDENCE","WAITING_CONFIGURATION","READY") and not run.get("human_disposition"):
            next_action=readiness["permitted_next_actions"][0]
            owner="Compliance Officer / Risk Manager (simulated required roles)"
            priority=min(priority,2)
        if status in ("RUNNING", "REVIEW_RECORDED"):
            next_action = "Inspect recorded activity; execution is not confirmed complete"
        if decision=='Pending Information':
            priority=min(priority,2);next_action='Review the information request and provide supporting evidence';owner='Analyst / Risk Manager'
        elif decision in ('Approve','Reject'):
            next_action='Inspect the recorded human decision and its supporting review history';owner='Authorized Approver'
        timestamps = [e["timestamp"] for e in run["events"] if e.get("timestamp")]
        rows.append(dict(deal_id=deal_id, run=run, history=history, terms=terms, risk=risk,
                         policy=policy, exceptions=exceptions, high=high, decision=decision,
                         borrower=terms.get("borrower", {}).get("value") or "Borrower not available",
                         priority=priority, next_action=next_action, owner=owner,
                         updated=max(timestamps) if timestamps else "Not recorded"))
    return sorted(rows, key=lambda row: (row["priority"], row["deal_id"]))


def navigate(st, operation, page="Review Workspace", reference=None):
    st.session_state.selected_financial_operation = operation
    st.session_state.run_selector = operation
    st.session_state.financial_page = page
    if reference:
        st.session_state.evidence_reference = reference


def apply_filter(st, value):
    st.session_state.dashboard_filter = value


def select_queue(st, deal_ids):
    selection = st.session_state.dashboard_queue.selection.rows
    if selection and selection[0] < len(deal_ids):
        st.session_state.dashboard_deal = deal_ids[selection[0]]


def render(st, runs, store, actor, names):
    rows = project_deals(runs)
    st.markdown("""<style>
    .st-key-dashboard-card-borrower,.st-key-dashboard-card-risk,.st-key-dashboard-card-financial,
    .st-key-dashboard-card-policy,.st-key-dashboard-card-workflow,.st-key-dashboard-card-actions
    {background:#fff;border-radius:12px;}
    </style>""", unsafe_allow_html=True)
    heading, action = st.columns([5, 1])
    heading.header("Deal Dashboard")
    action.button("New Deal", on_click=lambda: setattr(st.session_state, "financial_page", "New Deal"), width="stretch")
    st.caption("Which deals need attention, and what should I work on next?")
    st.caption("Monitor commercial loan reviews, credit risks, and outstanding actions. · Simulated role: " + actor.persona
               + " · View refreshed (UTC): " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
    filters = ("All deals", "Awaiting Decision", "High risk", "Policy exceptions", "Pending Information")
    counts = (len(rows), sum(r["decision"] == "Awaiting Decision" for r in rows), sum(r["high"] for r in rows),
              sum(len(r["exceptions"] or []) for r in rows), sum(r["decision"] == "Pending Information" for r in rows))
    for col, label, count, selection in zip(st.columns(5), ("Registered deals reviewed", "Awaiting Decision", "High-Risk Deals", "Recorded Policy Exceptions", "Pending Information"), counts, filters):
        col.metric(label, count)
        col.button("View " + selection.lower(), key="dash-kpi:" + selection, on_click=apply_filter, args=(st, selection), width="stretch")
    st.caption(f"Prepared fictional sample deals · Recorded runs: {len(runs)} · Recovery required: {sum(r['priority'] == 0 for r in rows)} · Uncomputed policy checks are not counted as passed.")
    # Preserve the established run-count metric for existing navigation clients.
    if not rows:
        st.info("Your workspace is ready. Start your first registered sample review to see findings and sources.")
        st.button("Start sample deal", on_click=lambda: setattr(st.session_state, "financial_page", "New Deal"), type="primary")
        return
    left, right, risk_col = st.columns([2, 1, 1])
    search = left.text_input("Search borrower or deal ID", placeholder="Borrower or deal ID")
    selection = right.selectbox("Attention filter", filters, key="dashboard_filter")
    band = risk_col.selectbox("Risk filter", ("All risk bands", "LOW", "MODERATE", "HIGH", "VERY_HIGH", "Not calculated"))
    visible = [r for r in rows if search.casefold() in (r["borrower"] + " " + r["deal_id"] + " " + case_label(r["run"]["context"]["scenario_id"])).casefold()
               and (selection == "All deals" or selection == r["decision"] or selection == "High risk" and r["high"] or selection == "Policy exceptions" and bool(r["exceptions"]))
               and (band == "All risk bands" or band == (r["risk"].get("band") or "Not calculated"))]
    st.subheader("Deal portfolio & attention queue")
    st.caption("Priority: recovery → pending information → human decision → policy exceptions → high risk → other reviews.")
    if not visible:
        st.info("No matching borrower or deal. Clear search and filters to see recorded cases.")
        return
    st.dataframe([{"Deal ID": r["deal_id"], "Borrower": r["borrower"],
                   "Loan amount": ((r["terms"].get("currency", {}).get("value") or "Currency unavailable") + " " + f"{Decimal(r['terms']['requested_amount']['value']):,.0f}") if r["terms"].get("requested_amount", {}).get("value") is not None else "Not available",
                   "Deal type": "Sample business loan", "Credit risk": (r["risk"].get("display") or "Not calculated") + " · " + (r["risk"].get("band") or "Not available"),
                   "Policy exceptions": str(len(r["exceptions"])) if r["exceptions"] is not None else "Not checked",
                   "Approval readiness": r["run"].get("approval_readiness",{}).get("outcome","Pending Review"), "Execution status": r["run"]["status"], "Human decision status": r["decision"], "Required role / owner": r["owner"],
                   "Last event (UTC)": r["updated"], "Next action": r["next_action"]} for r in visible], hide_index=True, width="stretch",
                 key="dashboard_queue", selection_mode="single-row", on_select=lambda: select_queue(st, [r["deal_id"] for r in visible]))
    choices = {r["deal_id"]: r for r in visible}
    if st.session_state.get("dashboard_deal") not in choices:
        st.session_state.dashboard_deal = next(iter(choices))
    selected = st.selectbox("Selected deal", list(choices), format_func=lambda key: case_label(choices[key]["run"]["context"]["scenario_id"]) + " · " + choices[key]["borrower"] + " · " + key, key="dashboard_deal")
    row = choices[selected]
    if row['run']['context'].get('upload_origin'):
        from .uploaded_calculations import render as render_uploaded_calculations
        render_uploaded_calculations(st,store.path.parent.parent,actor,row['run'],names)
    run, terms, risk = row["run"], row["terms"], row["risk"]
    op = run["operation_id"]
    st.info("Next action: " + row["next_action"] + " · " + row["owner"])
    panel = None if run["context"].get("mode")=="LIVE" else get_financial_review(store, actor, run)
    if panel and run["status"] == "WAITING_REVIEW":
        allowed = [key.replace("_", " ").title() for key, reason in panel["actions"].items() if reason is None]
        st.caption("Permitted in Review Workspace for this role: " + (", ".join(allowed) or "Inspect only"))
    def link(container, label, page="Review Workspace", ref=None):
        container.button(label, key="dash-link:" + label, on_click=navigate, args=(st, op, page, ref), width="stretch")
    def table(container, records):
        if records:
            container.dataframe(records, hide_index=True, width="stretch")
        else:
            container.info("Not available from this recorded review.")
    a, b, c = st.columns(3, gap="medium")
    with a.container(border=True, key="dashboard-card-borrower"):
        st.subheader("Borrower profile")
        st.write("**" + row["borrower"] + "**")
        amount = terms.get("requested_amount", {}).get("value")
        st.metric("Requested loan · " + (terms.get("currency", {}).get("value") or "Currency unavailable"), f"{Decimal(amount):,.0f}" if amount is not None else "Not available")
        st.caption("Sample business loan · Review revision " + str(run["context"]["scope"]["input_revision"]))
        st.caption("Industry, existing exposure and assigned reviewer: Not recorded")
        st.caption("Latest recorded event: " + row["updated"])
        st.caption("Review source: "+("Live AI response · Nebius" if run["context"].get("mode")=="LIVE" else "Saved AI responses"))
        link(st, "View latest review")
        link(st, "View source documents", ref=(run["context"]["scenario_id"] + ":" if run["context"]["scenario_id"] != "E-N01" else "") + "AGREEMENT-P1")
    with b.container(border=True, key="dashboard-card-risk"):
        st.subheader("Credit risk assessment")
        st.metric("Illustrative credit risk / 100", risk.get("display") or "Not calculated")
        st.write("**" + (risk.get("band") or "Insufficient Data") + "**")
        if risk.get("total") is not None:
            st.progress(float(Decimal(risk["total"]) / 100))
        st.caption("Higher means more modeled risk. Educational scoring method · Not probability of default.")
        table(st, [{"Factor": str(f.get("factor_id", "Not available")).replace("_", " ").title(), "Weighted contribution": f.get("contribution")} for f in sorted(risk.get("factors", []), key=lambda f: Decimal(str(f.get("contribution") or 0)), reverse=True)[:3]])
        synth = run["artifacts"].get("synthesizer", {}).get("payload")
        from ..recommendation import from_run
        recommendation=from_run(run)
        st.write("**AI Recommendation: "+recommendation["outcome"]+"**")
        st.caption(recommendation["brief_reason"])
        st.caption("Next action: "+recommendation["next_action"])
        if synth:
            with st.expander("Original AI proposal"):
                st.caption("Original AI proposal: "+parse_synthesis(synth["wire_json"]).panel_decision.decision+" - not the effective recommendation or a human credit decision")
        st.caption("Human decision: " + row["decision"] + " · Required policy checks and evidence verification still apply.")
        link(st, "View risk assessment")
    with c.container(border=True, key="dashboard-card-financial"):
        st.subheader("Financial summary")
        with st.expander("Financial terms explained"):
            st.write(FINANCIAL_HELP)
        metrics = run["artifacts"].get("financial_analyst", {}).get("payload", {}).get("metric_results", [])
        def value(metric):
            if metric.get("display") is None:
                return "Not available"
            number = Decimal(metric["display"])
            return f"USD {number:,.2f}" if metric["unit"] == "USD" else f"{number:,.2f}" + ("%" if metric["unit"] == "PERCENT" else "×")
        table(st, [{"Metric": names.get(m["metric_id"], m["metric_id"]), "Recorded value": value(m), "Reference": "calc:DSCR" if m["metric_id"] == "CALC-004" else "calc:" + m["metric_id"]} for m in metrics if m["metric_id"] in ("CALC-002", "CALC-003", "CALC-004", "CALC-005", "CALC-006")])
        st.caption("Calculation method and reporting periods of the calculation inputs are available in each reference. No comparable-period trend is inferred.")
        with st.expander("Validate calculation sources"):
            for m in metrics:
                handle = "calc:DSCR" if m["metric_id"] == "CALC-004" else "calc:" + m["metric_id"]
                link(st, "Inspect " + names.get(m["metric_id"], m["metric_id"]), ref=handle)
    a, b, c = st.columns(3, gap="medium")
    with a.container(border=True, key="dashboard-card-policy"):
        st.subheader("Policy checks")
        st.caption("Recorded policy results, not ongoing covenant monitoring. Workflow triggers are not policy exceptions.")
        table(st, [{"Result": p["result"], "Rule": p["ref"].split(":")[-1], "Actual": str(p["observed"]) if p["observed"] is not None else "Not available", "Predicate": str(p["predicate"]), "Threshold": str(p["threshold"]) if p["threshold"] is not None else "Not applicable"} for p in row["policy"]["rules"]])
        with st.expander("Validate rules & supporting evidence"):
            for p in row["policy"]["rules"]:
                link(st, "Validate " + p["ref"], ref=p["ref"])
    with b.container(border=True, key="dashboard-card-workflow"):
        st.subheader("Deal review workflow")
        stages = list(dict.fromkeys(e["stage"] for e in run["events"]))
        for stage in stages:
            events = [e for e in run["events"] if e["stage"] == stage]
            state = "Recorded complete" if any(e["event"] in ("stage_completed", "artifact_reused") for e in events) else "Started; completion not recorded"
            if stage == "human_review" and run["status"] in ("WAITING_REVIEW", "WAITING_INFORMATION"):
                state = "Waiting for human review" if run["status"] == "WAITING_REVIEW" else "Pending information"
            st.write(names.get(stage, stage) + " · " + state)
        st.caption("Only recorded stages shown. AI execution completion does not mean loan approval.")
        link(st, "View agent activity", "Agent Activity")
    with c.container(border=True, key="dashboard-card-actions"):
        st.subheader("Alerts & required actions")
        st.write("**Review status:** " + friendly(run["status"]))
        st.write("**Human decision:** " + row["decision"])
        st.write(row["next_action"])
        st.caption(row["owner"])
        for rule in row["policy"]["rules"]:
            if rule["workflow"] != "CONTINUE" or rule["ref"].split(":")[-1] in (row["exceptions"] or []):
                st.warning(rule["ref"] + " · " + rule["reason"])
        st.caption("Evidence checks: " + ("Inspect live reviewer assessments in Human Review" if run["context"].get("mode")=="LIVE" else "Saved sample checks; inspect supporting evidence" if "evidence_review" in run["artifacts"] else "Not checked"))
        link(st, "Open review workspace")
        link(st, "View memo", "Credit Memo")
        link(st, "Decision history", "Decision History")
    with st.expander("Review history · " + str(len(row["history"]))):
        st.metric("Recorded review runs", len(runs))
        st.caption("Latest review uses recorded generation time, then operation ID. Deal reference: " + row["deal_id"])
        table(st, [{"Started (UTC)": r["context"]["generation_time"], "Review status": friendly(r["status"]), "Run ID": r["context"]["scope"]["run_id"], "Human decision": r.get("human_disposition") or "Not recorded"} for r in row["history"]])
    st.caption("Portfolio trends unavailable: additional comparable deals and review periods are required. No fabricated exposure, PD or historical charts.")
