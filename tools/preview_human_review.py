"""Run with Streamlit on localhost; isolated educational review-UI examples."""

from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main(workspace=ROOT):
    import streamlit as st
    from deal_or_no_deal_ai.configuration import load_configuration
    from deal_or_no_deal_ai.context import InputError
    from deal_or_no_deal_ai.review_actions import (
        ROLES, list_review_examples, prepare_review_examples, preview_actor,
    )
    from deal_or_no_deal_ai.storage import RunBusy, Store
    from deal_or_no_deal_ai.ui.human_review import render_human_review
    from deal_or_no_deal_ai.ui.decision_history import render_decision_history

    st.set_page_config(page_title="Deal or No Deal AI — Human review preview", layout="wide")
    st.title("Deal or No Deal AI")
    st.caption("Every deal has a story. Our agents find the plot holes.")
    st.info("EDUCATIONAL UI PREVIEW · Role simulation · Synthetic examples · No model calls")
    config = load_configuration(Path(workspace))
    store = Store(config.database)
    persona = st.sidebar.selectbox("Demo role", ROLES)
    senior = st.sidebar.checkbox("Senior approver tier", value=False) if persona == "AuthorizedApprover" else False
    actor = preview_actor(persona, senior=senior)
    st.sidebar.caption("Role selection is a demonstration control, not sign-in or verified authority.")
    page = st.sidebar.radio("Page", ("Human review", "Decision History"))
    try:
        if page == "Decision History":
            render_decision_history(store, actor)
            return
        examples = list_review_examples(store, actor)
        if not examples:
            st.info("Prepare the three illustrative UI examples to try review comments and role-based actions. Existing loan-review records are preserved.")
            if st.button("Prepare UI review samples"):
                prepare_review_examples(store)
                st.rerun()
            return
        selected = st.selectbox("Deal", examples, format_func=lambda item: item["title"])
        render_human_review(store, selected["request_id"], actor)
    except (InputError, RunBusy, OSError, sqlite3.Error):
        st.error("The preview is unavailable or another execution is active. No automatic reset or recovery was attempted.")


if __name__ == "__main__":
    main()
