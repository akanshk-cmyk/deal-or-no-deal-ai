"""Shared formatted results and actual Streamlit/Memo behavior, no model calls."""
from copy import deepcopy
from deal_or_no_deal_ai.command_center import get_run
from deal_or_no_deal_ai.recommendation import from_run,markdown
from deal_or_no_deal_ai.memo import inert
from tests.integration.test_approval_readiness import saved_deal
from tests.integration import test_command_center as command_center_tests


def test_standard_deal_formatter_and_memo_use_identical_current_facts(saved_deal):
    root,operation,actor,store,result=saved_deal
    run=get_run(store,actor,operation);before=deepcopy(run);db_before=store.path.read_bytes()
    r=from_run(run)
    assert r["outcome"]=="Pending Review"
    assert r["recommendation"]=="Defer approval pending additional validation."
    assert r["human_decision"]=="Not recorded"
    assert len(r["rationale"])==4
    assert any("1.50x" in p["text"] for p in r["rationale"])
    assert any("Low (21.00/100)" in p["text"] for p in r["rationale"])
    assert any("not complete" in p["text"] for p in r["rationale"])
    assert "annual financial-statement" in r["next_action"]
    assert "Verify" in r["next_action"]
    assert not any("exception" in p["text"].lower() for p in r["issues"])
    report=result["report_markdown"]
    effective=report.split("## Decision\n",1)[1].split("## Conditions",1)[0]
    assert "**Recommended AI Outcome:** Pending Review" in effective
    assert "**Recommendation:** "+inert(r["recommendation"]) in effective
    for paragraph in r["rationale"]:
        assert inert(paragraph["text"]) in effective
    assert inert(r["next_action"]) in effective
    assert "Simulated recommendation: **Approve**" not in effective
    assert "Original AI proposal and historical review details" in report
    assert run["ai_proposal"]["decision"]=="Approve"
    assert run==before and store.path.read_bytes()==db_before
    assert result["ledger"]["committed"]["nodes"]==9
    assert result["ledger"]["committed"]["attempts"]==0


def test_workspace_dashboard_and_citation_navigation():
    # Reuse the established offline AppTest setup and its socket-pair workaround.
    CommandCenterTests=command_center_tests.CommandCenterTests
    from tests.integration.test_human_review_ui import widget
    from tests.support import uid
    from deal_or_no_deal_ai.worker import run_normal_fixture
    harness=CommandCenterTests(methodName="runTest");harness.setUp()
    try:
        run_normal_fixture(harness.root,uid("recommendation-ui"))
        app=harness.app()
        assert not app.exception
        assert any("AI Recommendation: Pending Review" in item.value for item in app.markdown)
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        assert not app.exception
        assert any("AI Recommendation" in item.value and "Pending Review" in item.value for item in app.markdown)
        assert any("Defer approval pending additional validation" in item.value for item in app.markdown)
        assert any("Required Next Action" in item.value for item in app.markdown)
        assert any("Human Decision:** Not recorded" in item.value for item in app.markdown)
        # This is the formatter's real citation button, using the existing explorer.
        button=next(b for b in app.button if b.key=="ref:recommendation:0")
        button.click().run()
        assert widget(app.selectbox,"Evidence reference").value=="calc:DSCR"
        assert not app.exception
        widget(app.sidebar.radio,"Page").set_value("Credit Memo").run()
        assert not app.exception
        assert any("**Recommended AI Outcome:** Pending Review" in item.value for item in app.markdown)
    finally:
        harness.doCleanups()
