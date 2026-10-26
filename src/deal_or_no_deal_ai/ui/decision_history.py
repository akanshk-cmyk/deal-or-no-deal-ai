"""Dedicated read-only history page; export is an explicit scoped service call."""
from .labels import friendly, FINANCIAL_HELP


import sqlite3

from pydantic import ValidationError

from ..context import InputError, fingerprint
from ..decision_history import (
    HistoryFilters, MAX_EXPORT_EVENTS, STATUSES, export_decision_history_csv,
    get_deal_timeline, query_decision_history,
)
from ..review_actions import ACTION_LABELS
from .human_review import STATUS_LABELS


def _shown(value):
    return "Not captured" if value is None else str(value)


def _event_details(st, row):
    st.subheader("Event details")
    st.text(row["timestamp_utc"] + " · " + ACTION_LABELS[row["action"]])
    st.text("Deal ID: " + row["deal_id"])
    st.text("Borrower: " + _shown(row["borrower_name"]))
    st.text("Loan amount: " + _shown(row["loan_amount"]) + " · Currency: " + _shown(row["currency"]))
    st.text("Deal type: " + _shown(row["deal_type"]))
    st.text("Transition: " + friendly(row["previous_status"]) + " → " + friendly(row["new_status"]))
    st.text("Current deal status: " + friendly(row["current_status"]))
    st.text("Reviewer: " + _shown(row["reviewer_name"]) + " · " + friendly(row["reviewer_role"]) + " (simulated)")
    st.caption("Reviewer ID: " + row["reviewer_id"])
    st.text("Decision reason / comments:")
    st.text(row["comments"])
    for item in row["requested_items"]:
        st.text("Requested information: " + item)
    with st.expander("Technical details"):
        st.caption("Analysis revision: " + str(row["input_revision"]) + " · Basis: " + row["analytical_basis_digest"])
    context = row["context_snapshot"]
    for field, label in (("ai_recommendation", "AI recommendation at action time"),
                         ("ai_analysis_version", "AI analysis version at action time"),
                         ("risk_assessment", "Historical risk assessment"),
                         ("compliance_findings", "Historical compliance findings"),
                         ("policy_exceptions", "Historical policy exceptions"),
                         ("supporting_documents", "Captured supporting documents")):
        with st.expander(label):
            value = context.get(field)
            if value is None:
                st.info("Not captured for this event. No current analysis or document is substituted.")
            elif isinstance(value, (dict, list)):
                st.json(value)
            else:
                st.text(str(value))
    with st.expander("Technical details"):
        st.caption("Snapshot source: " + row["snapshot_source"] + " · " + row["provenance"])


def render_decision_history(store, actor):
    import streamlit as st

    st.header("Decision History")
    st.caption("Historical review actions across your permitted deals. Exact timestamps and date filters use UTC.")
    st.warning("Illustrative review records · Simulated identities · Local history is not tamper-proof audit storage.")
    with st.expander("Filters and search", expanded=True):
        a, b, c = st.columns(3)
        deal_id = a.text_input("Deal ID", max_chars=200)
        borrower = b.text_input("Borrower", max_chars=200)
        reviewer = c.text_input("Reviewer name, ID or role", max_chars=200)
        actions = st.multiselect("Decision / action type", list(ACTION_LABELS), format_func=ACTION_LABELS.get)
        statuses = st.multiselect("Status at event", list(STATUSES), format_func=STATUS_LABELS.get)
        start = end = None
        if st.checkbox("Filter by UTC date range"):
            start = st.date_input("Start date (UTC)", value=None)
            end = st.date_input("End date (UTC)", value=None)
        newest = st.selectbox("Chronological order", ("Newest first", "Oldest first")) == "Newest first"
    try:
        filters = HistoryFilters(deal_id=deal_id, borrower=borrower, reviewer=reviewer,
                                 actions=actions, statuses=statuses, start_date=start, end_date=end, newest_first=newest)
        view = query_decision_history(store, actor, filters, limit=25)
        scope = fingerprint("HISTORY_UI_SCOPE", dict(workspace=actor.workspace_id, role=actor.persona,
            deals=actor.allowed_deal_ids, filters=filters.model_dump()))
        st.metric("Matching history events", view["total"])
        st.caption(view["coverage"])
        if not view["rows"]:
            st.info("No recorded events match these filters. Record a review action in Human review or adjust the filters.")
        pages = max(1, (view["total"] + 24) // 25)
        page_key = "history_page:" + scope
        if st.session_state.get(page_key, 1) > pages:
            st.session_state[page_key] = pages
        page = st.number_input("History page", min_value=1, max_value=pages, value=1, step=1, key=page_key)
        if page > 1:
            view = query_decision_history(store, actor, filters, offset=(page - 1) * 25, limit=25)
        if view["rows"]:
            grid = []
            for row in view["rows"]:
                grid.append({"Date / time (UTC)": row["timestamp_utc"], "Deal ID": row["deal_id"],
                    "Borrower": _shown(row["borrower_name"]), "Loan amount": _shown(row["loan_amount"]),
                    "Currency": _shown(row["currency"]), "Deal type": _shown(row["deal_type"]),
                    "Reviewer": _shown(row["reviewer_name"]), "Role": row["reviewer_role"],
                    "Previous status": friendly(row["previous_status"]), "Status at event": row["new_status"],
                    "Current status": row["current_status"], "Action": ACTION_LABELS[row["action"]], "Comments": row["comments"]})
            st.dataframe(grid, hide_index=True, width="stretch")
            st.caption("Showing " + str(view["offset"] + 1) + "–" + str(view["offset"] + len(grid)) + " of " + str(view["total"]) + " events.")
            by_id = {row["event_id"]: row for row in view["rows"]}
            chosen = st.selectbox("Open event details", list(by_id), index=None,
                format_func=lambda event_id: by_id[event_id]["timestamp_utc"] + " · " + ACTION_LABELS[by_id[event_id]["action"]],
                key="history_event:" + scope + ":" + str(page))
            if chosen is not None:
                _event_details(st, by_id[chosen])
        st.subheader("Export audit report")
        st.caption("CSV contains all matching authorized events across pages, including historical context and export time. Maximum 5,000 events; PDF is not implemented.")
        if view["total"] > MAX_EXPORT_EVENTS:
            st.warning("Narrow the filters to 5,000 events or fewer before exporting.")
        export_key = "history_prepared_export"
        cached = st.session_state.get(export_key)
        if cached is not None and cached["snapshot_digest"] != view["snapshot_digest"]:
            del st.session_state[export_key]
        if st.button("Prepare CSV audit report", disabled=view["total"] == 0 or view["total"] > MAX_EXPORT_EVENTS):
            st.session_state[export_key] = export_decision_history_csv(store, actor, filters, expected_digest=view["snapshot_digest"])
        cached = st.session_state.get(export_key)
        if cached is not None and cached["snapshot_digest"] == view["snapshot_digest"]:
            st.download_button("Download CSV audit report", data=cached["content"], file_name=cached["filename"],
                               mime="text/csv", on_click="ignore")
            st.caption(str(cached["row_count"]) + " events · Prepared at " + cached["exported_at_utc"])
        st.subheader("Deal decision timeline")
        st.caption("Complete recorded review timeline for the selected deal, oldest first. Dashboard filters do not hide timeline events.")
        deals = {item["deal_id"]: item for item in view["deals"]}
        selected = st.selectbox("Timeline deal", list(deals), index=None,
            format_func=lambda value: deals[value]["title"] + " · " + value, key="history_timeline_deal:" + scope)
        if selected is not None:
            timeline = get_deal_timeline(store, actor, selected)
            if not timeline:
                st.info("No review actions have been recorded for this deal.")
            event_key = "history_timeline_event:" + scope + ":" + selected
            for row in timeline:
                label = row["timestamp_utc"] + " — " + ACTION_LABELS[row["action"]] + " · " + friendly(row["new_status"])
                if st.button("View event: " + label, key="history_timeline:" + row["event_id"]):
                    st.session_state[event_key] = row["event_id"]
            selected_event = st.session_state.get(event_key)
            for row in timeline:
                if row["event_id"] == selected_event:
                    _event_details(st, row)
    except ValidationError:
        st.error("Check the filters. The start date must be on or before the end date.")
    except (InputError, OSError, sqlite3.Error):
        st.error("History or export is unavailable for this scope, or the saved view changed. Refresh and try again. No records were modified.")
