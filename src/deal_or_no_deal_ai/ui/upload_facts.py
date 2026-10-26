"""Manual source-bound candidate/review controls; no model or credit action."""
from .labels import friendly, FINANCIAL_HELP

from uuid import UUID, uuid5
import sqlite3

from ..context import fingerprint, InputError
from ..upload_facts import (FIELDS, CHECKS, ProposalCommand, SupportCommand,
                           get_fact_review, record_fact_action, dscr_preview)


def open_source(st, operation, source, number):
    st.session_state["upload-source:" + operation] = source
    st.session_state["upload-page:" + operation] = number


def render(st, root, actor, operation, page):
    panel = get_fact_review(root, actor, operation)
    st.subheader("Financial evidence review")
    with st.expander("Financial terms explained"):
        st.write(FINANCIAL_HELP)
    st.caption("Values entered by a reviewer · No AI extraction. The Risk Manager verifies evidence, not credit approval. Only annual CFADS/principal/interest are supported in this step.")
    preview = dscr_preview(panel)
    st.metric("Annual DSCR preview", preview["display"] + "x" if preview["display"] else "Unknown")
    for reason in preview["blockers"]:
        st.caption(reason)
    st.caption("Supplied annual inputs only; full-term repayment, risk score and policy clearance are not assessed.")
    if panel["latest"]:
        st.dataframe([dict(Field=friendly(name), Value=e["content"]["value"], Subject=e["content"]["subject"],
            Period=e["content"]["period_start"] + " to " + e["content"]["period_end"],
            Status=friendly(panel["supports"].get(name, {}).get("command", {}).get("status", "PENDING"))) for name, e in panel["latest"].items()], hide_index=True)
    if actor.persona == "Analyst":
        st.caption("Use the original page above. Copy an exact quote and the number exactly as printed; the proposal does not certify its meaning. Saving a replacement invalidates previous support.")
        with st.form("upload-fact-proposal:" + operation + ":" + page["ref"]):
            field = st.selectbox("Financial information to review", FIELDS, format_func=friendly)
            quote = st.text_area("Exact source quote")
            raw_label = st.text_input("Field label as printed in quote")
            number = st.text_input("Number exactly as printed (plain decimal)")
            unit = st.text_input("Unit label as printed on this page")
            scale = st.selectbox("How amounts are reported", ("1", "1000", "1000000"), index=None, format_func=lambda v: {"1": "Actual amounts", "1000": "Amounts in thousands", "1000000": "Amounts in millions"}[v])
            subject = st.text_input("Borrower or business name")
            facility = st.text_input("Loan or debt covered by these figures")
            start = st.text_input("Annual period start (YYYY-MM-DD)")
            end = st.text_input("Annual period end (YYYY-MM-DD)")
            kind = st.selectbox("Type of annual figures", ("ANNUAL_ACTUAL", "ANNUAL_PROJECTION"), index=None, format_func=friendly)
            comments = st.text_area("Reason for this proposed value")
            submitted = st.form_submit_button("Save value and supporting source")
        if submitted:
            offset = page["text"].find(quote) if quote else -1
            if offset < 0 or not all((raw_label, number, unit, scale, subject, facility, start, end, kind, comments.strip())):
                st.error("Enter an exact quote from this page, all basis fields and a reason. Nothing was saved.")
                return
            values = dict(expected_version=panel["version"], field=field, source_ref=page["ref"], quote=quote, quote_start=offset,
                raw_number=number, raw_label=raw_label, unit_label=unit, scale=scale, currency="USD", subject=subject,
                facility=facility, period_start=start, period_end=end, basis_kind=kind, comments=comments)
            action_id = str(uuid5(UUID(operation), fingerprint("UPLOAD_PROPOSAL_UI", values)))
            try:
                record_fact_action(root, actor, operation, ProposalCommand(operation_id=action_id, **values))
            except (InputError, ValueError, OSError, sqlite3.Error):
                st.error("Proposal not saved. Check the exact quote and number, annual dates, source scale and current version.")
            else:
                st.rerun()
    elif actor.persona == "RiskManager":
        pending = [e for name, e in panel["latest"].items() if name not in panel["supports"]]
        if pending:
            proposal_id = st.selectbox("Financial information awaiting review", [e["operation_id"] for e in pending],
                format_func=lambda pid: friendly(next(e["content"]["field"] for e in pending if e["operation_id"] == pid)))
            event = next(e for e in pending if e["operation_id"] == proposal_id)
            content = event["content"]
            st.write("Proposed value: " + content["value"])
            st.write("Borrower: " + content["subject"])
            with st.expander("Technical details"):
                st.json(content)
            st.text("Original exact quote: " + content["quote"])
            st.caption("Source citation: " + content["source_ref"] + ". Select its file/page above to inspect the complete context.")
            source, cited_page = next((s, p) for s in panel["package"]["sources"] for p in s["pages"] if p["ref"] == content["source_ref"])
            st.button("Open candidate source page", on_click=open_source, args=(st, operation, source["sha256"], cited_page["page"]))
            with st.form("upload-fact-support:" + proposal_id):
                status = st.selectbox("Evidence assessment", ("HUMAN_SUPPORTED", "UNSUPPORTED", "WITHHELD"), index=None, format_func=friendly)
                checks = st.multiselect("Verified evidence checks", CHECKS, format_func=friendly)
                comments = st.text_area("Evidence review reason")
                submitted = st.form_submit_button("Record evidence assessment")
            if submitted:
                if status is None or not comments.strip():
                    st.error("Select an assessment and enter a reason. Nothing was saved.")
                    return
                values = dict(expected_version=panel["version"], proposal_id=proposal_id, target_digest=content["target_digest"], status=status, checks=checks, comments=comments)
                action_id = str(uuid5(UUID(operation), fingerprint("UPLOAD_SUPPORT_UI", values)))
                try:
                    record_fact_action(root, actor, operation, SupportCommand(operation_id=action_id, **values))
                except (InputError, ValueError, OSError, sqlite3.Error):
                    st.error("Assessment not saved. Support requires every evidence check and the exact current candidate.")
                else:
                    st.rerun()
        else:
            st.info("No values are waiting for evidence review.")
    else:
        st.caption("The Analyst proposes values; the Risk Manager verifies their evidence. Other roles are read-only here.")
    with st.expander("Financial evidence history"):
        for event in panel["events"]:
            st.text(event["timestamp_utc"] + " · " + event["reviewer_role"] + " · " + event["action"])
            st.text(event["comments"])
            with st.expander("Technical details", expanded=False):
                st.json(event["command"])
