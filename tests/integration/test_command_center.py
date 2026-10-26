"""Actual worker-to-screen integration and provenance failures, without network."""

from dataclasses import replace
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import socket

from streamlit.testing.v1 import AppTest

from deal_or_no_deal_ai.command_center import get_run, list_runs, policy_display, source_packet, start_run, workspace_id
from deal_or_no_deal_ai.context import InputError, strict_json
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.memo import inert
from deal_or_no_deal_ai.storage import RecordWrite, Store
from deal_or_no_deal_ai.worker import run_normal_fixture
from tests.integration.test_human_review_ui import internal_event_loop_pair, widget
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import OfflineTest, uid


class CommandCenterTests(OfflineTest):
    def setUp(self):
        super().setUp()
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        copy_workspace(self.root)
        self.store = Store(self.root / "var/deal_review.sqlite3")
        deal = strict_json((self.root / "config/registrations/e-n01.json").read_bytes())["deal_id"]
        self.actor = Actor("Analyst", workspace_id(self.root), frozenset({deal}))

    def app(self):
        pair = patch.object(socket, "socketpair", internal_event_loop_pair)
        pair.start()
        self.addCleanup(pair.stop)
        code = ("from pathlib import Path\nfrom deal_or_no_deal_ai.ui.command_center import main\n"
                + "main(Path(" + repr(str(self.root)) + "))\n")
        return AppTest.from_string(code, default_timeout=30).run()

    def test_redesign_groups_runs_and_keeps_older_selection_across_pages(self):
        older, newer = uid("v2-older"), uid("v2-newer")
        run_normal_fixture(self.root, older, generation_time="2026-10-24T01:00:00+00:00")
        run_normal_fixture(self.root, newer, generation_time="2026-10-24T02:00:00+00:00")
        app = self.app()
        self.assertEqual(widget(app.metric, "Registered deals reviewed").value, "1")
        self.assertEqual(widget(app.metric, "Recorded review runs").value, "2")
        widget(app.button, "View latest review").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["selected_financial_operation"], newer)
        widget(app.selectbox, "Review attempt").select(older).run()
        for page in ("Credit Memo", "Deal Dashboard", "Decision History", "Review Workspace"):
            widget(app.sidebar.radio, "Page").set_value(page).run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(app.session_state["selected_financial_operation"], older)
            if page != "Deal Dashboard":
                self.assertEqual(widget(app.selectbox, "Review attempt").value, older)

    def test_deal_selector_scopes_history_defaults_latest_and_preserves_records(self):
        import shutil
        from tests.support import ROOT
        for name in ("e-m01", "e-p01"):
            shutil.copytree(ROOT / "fixtures/development" / name, self.root / "fixtures/development" / name)
        older, newer = uid("navigation-old"), uid("navigation-new")
        first = run_normal_fixture(self.root, older, generation_time="2026-10-24T01:00:00+00:00")
        run_normal_fixture(self.root, newer, generation_time="2026-10-24T02:00:00+00:00")
        missing_operation = uid("navigation-missing")
        missing = run_normal_fixture(self.root, missing_operation, scenario_id="E-M01",
                                     generation_time="2026-10-24T03:00:00+00:00")
        run_normal_fixture(self.root, uid("navigation-policy"), scenario_id="E-P01", variant="review",
                           generation_time="2026-10-24T04:00:00+00:00")
        before = self.store.path.read_bytes()
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_NAVIGATION_REPLAY")):
            app = self.app()
            self.assertEqual(widget(app.metric, "Registered deals reviewed").value, "3")
            widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
            self.assertEqual(len(widget(app.selectbox, "Select Deal").options), 3)
            widget(app.selectbox, "Select Deal").select(first["scope"]["deal_id"]).run()
            self.assertEqual(app.session_state["selected_financial_operation"], newer)
            self.assertEqual(len(widget(app.selectbox, "Review attempt").options), 2)
            self.assertTrue(any("Review History" in exp.label for exp in app.expander))
            widget(app.selectbox, "Review attempt").select(older).run()
            self.assertEqual(app.session_state["selected_financial_operation"], older)
            self.assertTrue(any("Viewing an earlier review" in item.value for item in app.info))
            widget(app.button, "Open latest review").click().run()
            self.assertEqual(app.session_state["selected_financial_operation"], newer)
            widget(app.selectbox, "Select Deal").select(missing["scope"]["deal_id"]).run()
            self.assertEqual(app.session_state["selected_financial_operation"], missing_operation)
            self.assertFalse(any(s.label == "Review attempt" for s in app.selectbox))
            self.assertTrue(any("No earlier reviews" in item.value for item in app.caption))
            widget(app.selectbox, "Select Deal").select(first["scope"]["deal_id"]).run()
            self.assertEqual(app.session_state["selected_financial_operation"], newer)
            self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.store.path.read_bytes(), before)

    def test_redesign_evidence_buttons_and_unavailable_human_actions(self):
        run_normal_fixture(self.root, uid("v2-evidence"))
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        factor = "assessment:E-N01:repayment_capacity"
        widget(app.button, "↗ " + factor.replace("E-N01", "Standard Deal")).click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(widget(app.selectbox, "Evidence reference").value, factor)
        next(button for button in app.button if button.label == "↗ FIN-P1").click().run()
        self.assertEqual(widget(app.selectbox, "Evidence reference").value, "FIN-P1")
        self.assertTrue(any("Original page" in c.value for c in app.caption))
        for role in ("Analyst", "AuthorizedApprover"):
            widget(app.sidebar.selectbox, "Demo role").select(role).run()
            for action in ("Approve", "Reject", "Request More Information", "Return for Reassessment"):
                self.assertTrue(widget(app.button, action).disabled)
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertEqual(len(app.dataframe), 0)
        self.assertTrue(any("No human decisions recorded" in item.value for item in app.markdown))

    def test_dashboard_filters_and_citation_navigation_are_read_only(self):
        operation = uid("dashboard-read-only")
        run_normal_fixture(self.root, operation)
        before = self.store.path.read_bytes()
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_REPLAY")):
            app = self.app()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(widget(app.metric, "Awaiting Decision").value, "0")
            widget(app.button, "View awaiting decision").click().run()
            self.assertTrue(any("No matching" in item.value for item in app.info))
            widget(app.button, "View all deals").click().run()
            widget(app.button, "Inspect Debt-service coverage (DSCR)").click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(widget(app.selectbox, "Evidence reference").value, "calc:DSCR")
            self.assertEqual(app.session_state["selected_financial_operation"], operation)
        self.assertEqual(self.store.path.read_bytes(), before)

    def test_read_only_review_explains_and_prepares_editable_sample_without_execution(self):
        operation = uid("readonly-form-route")
        run_normal_fixture(self.root, operation)
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        self.assertFalse(any(area.label == "Review comments" for area in app.text_area))
        self.assertTrue(any("no human-review request" in message.value for message in app.info))
        before = self.store.path.read_bytes()
        widget(app.button, "Prepare a review-required sample").click().run()
        self.assertEqual(widget(app.selectbox, "Sample scenario").value, "review")
        self.assertEqual(widget(app.sidebar.radio, "Page").value, "New Deal")
        self.assertEqual(self.store.path.read_bytes(), before)

    def test_review_form_validates_and_submits_current_comment_in_one_batch(self):
        from deal_or_no_deal_ai.financial_review import financial_history
        run_normal_fixture(self.root, uid("form-submit-current"), variant="review")
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        widget(app.selectbox, "Financial review action").select("ADD_COMMENT").run()
        self.assertFalse(widget(app.text_area, "Financial review comments (required)").disabled)
        self.assertFalse(widget(app.button, "Record financial review action").disabled)
        before = self.store.path.read_bytes()
        widget(app.button, "Record financial review action").click().run()
        self.assertTrue(any("enter review comments" in message.value for message in app.error))
        self.assertEqual(self.store.path.read_bytes(), before)
        widget(app.text_area, "Financial review comments (required)").input("One-submit comment retained without a field rerun.")
        widget(app.button, "Record financial review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Review action saved" in message.value for message in app.success))
        events = financial_history(self.store, self.actor)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["comments"], "One-submit comment retained without a field rerun.")

    def test_dashboard_low_score_does_not_hide_mandatory_human_review(self):
        run_normal_fixture(self.root, uid("dashboard-review"), variant="review")
        app = self.app()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(widget(app.metric, "Awaiting Decision").value, "1")
        self.assertEqual(widget(app.metric, "High-Risk Deals").value, "0")
        self.assertTrue(any("Compliance" in item.value for item in app.info))
        self.assertTrue(any("Original AI proposal" in item.value for item in app.caption))

    def test_upload_placeholder_does_not_ingest_or_write(self):
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.radio, "Intake mode").set_value("Upload New Deal").run()
        self.assertEqual(len(app.exception), 0)
        self.assertFalse(self.store.path.exists())
        self.assertFalse(any(b.label == "Run AI Deal Review" for b in app.button))

    def test_connected_financial_review_ui_decision_memo_and_history(self):
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.selectbox, "Sample scenario").select("review").run()
        widget(app.button, "Run AI Deal Review").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Waiting for a credit decision" in warning.value for warning in app.warning))
        widget(app.button, "Open review workspace").click().run()
        self.assertNotIn("APPROVE", widget(app.selectbox, "Financial review action").options)
        self.assertNotIn("Approve", widget(app.selectbox, "Financial review action").options)
        widget(app.sidebar.selectbox, "Demo role").select("AuthorizedApprover").run()
        self.assertNotIn("Approve",widget(app.selectbox,"Financial review action").options)
        widget(app.selectbox, "Financial review action").select("REJECT").run()
        widget(app.text_area, "Financial review comments (required)").input("Synthetic analyst package and sources reviewed.")
        widget(app.checkbox, "Confirm this simulated final decision").check()
        widget(app.button, "Record financial review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("REJECTED" in caption.value for caption in app.caption))
        widget(app.sidebar.radio, "Page").set_value("Credit Memo").run()
        self.assertTrue(any("Human disposition: Reject" in item.value for item in app.markdown))
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("1 recorded decision(s)" in item.value for item in app.markdown))
        self.assertTrue(any("Synthetic analyst package and sources reviewed." == t.value for t in app.text))
        history_before = self.store.path.read_bytes()
        widget(app.text_input, "History reviewer or role").input("unrecorded-person").run()
        self.assertTrue(any("No history events match" in item.value for item in app.info))
        self.assertTrue(widget(app.button, "Prepare financial history CSV").disabled)
        widget(app.text_input, "History reviewer or role").input("").run()
        widget(app.multiselect, "History actions").set_value(["REJECT"]).run()
        widget(app.checkbox, "Filter by UTC dates").check().run()
        widget(app.button, "Prepare financial history CSV").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.store.path.read_bytes(), history_before)

    def test_registered_response_ui_opens_revision2_after_risk_manager_assessment(self):
        from deal_or_no_deal_ai.financial_review import get_financial_review, record_financial_action
        from deal_or_no_deal_ai.review_actions import ReviewActionCommand
        operation = uid("response-ui-parent")
        run_normal_fixture(self.root, operation, variant="review")
        panel = get_financial_review(self.store, self.actor, get_run(self.store, self.actor, operation))
        request = panel["request"]
        command = ReviewActionCommand(operation_id=uid("response-ui-request"), request_id=request.request_id,
            expected_version=panel["version"], expected_gate_version=request.gate_version,
            expected_basis=request.analytical_basis_digest, action="REQUEST_INFORMATION",
            comments="Confirm supplied annual financial basis.", requested_items=["Confirm financial period."])
        record_financial_action(self.root, self.actor, operation, command)
        pack = self.root / "fixtures/development/e-n01"
        manifest = strict_json((pack / "manifest.json").read_bytes())
        document = (pack / next(s["path"] for s in manifest["sources"] if s["source_id"] == "FINANCIALS-1")).read_bytes()
        class UploadedRegisteredPDF:
            def getvalue(self):
                return document
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        with patch("streamlit.file_uploader", return_value=UploadedRegisteredPDF()):
            widget(app.sidebar.selectbox, "Demo role").select("RiskManager").run()
            widget(app.selectbox, "Evidence for request 1: Confirm financial period.").select("FIN-P2").run()
            widget(app.text_area, "Risk Manager response assessment (required)").input("Registered period inspected; source answers this request.").run()
            widget(app.button, "Accept registered response and reassess").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 0)
        selected = app.session_state["selected_financial_operation"]
        self.assertNotEqual(selected, operation)
        result = get_run(self.store, self.actor, selected)
        self.assertEqual(result["context"]["scope"]["input_revision"], 2)
        self.assertEqual(result["status"], "WAITING_REVIEW")

    def test_read_only_scope_and_original_source_version(self):
        self.assertEqual(list_runs(self.store, self.actor), [])
        self.assertFalse(self.store.path.exists())
        operation = uid("command-center-sources")
        outcome = run_normal_fixture(self.root, operation)
        run = get_run(self.store, self.actor, operation)
        self.assertEqual(run["outcome"], outcome)
        self.assertEqual(len(run["events"]), 18)
        self.assertTrue(all(event.get("timestamp") for event in run["events"]))
        packet = source_packet(self.root, run)
        self.assertEqual(packet["input_digest"], run["context"]["synthesis_input_digest"])
        outsider = replace(self.actor, allowed_deal_ids=frozenset())
        self.assertEqual(list_runs(self.store, outsider), [])
        with self.assertRaisesRegex(InputError, "OUT_OF_SCOPE"):
            get_run(self.store, outsider, operation)
        changed = {**run, "context": {**run["context"], "synthesis_input_digest": "changed"}}
        with self.assertRaisesRegex(InputError, "SOURCE_VERSION_UNAVAILABLE"):
            source_packet(self.root, changed)

    def test_policy_display_uses_final_recorded_evaluation_without_mutating_history(self):
        operation = uid("policy-final-view")
        run_normal_fixture(self.root, operation)
        run = get_run(self.store, self.actor, operation)
        packet = source_packet(self.root, run)
        original_run, original_packet = deepcopy(run), deepcopy(packet)
        view = policy_display(run, packet)
        handle = "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-012"
        final = next(rule for rule in view["rules"] if rule["ref"] == handle)
        self.assertEqual(view["basis"], "POST_SYNTHESIS_RECORDED")
        self.assertEqual(final["state"], "EVALUATED")
        self.assertEqual(final["observed"], "0.85")
        self.assertEqual(final["result"], "NOT_TRIGGERED")
        self.assertEqual(final["result_kind"], "Workflow control")
        recorded_rule = next(r for r in run["artifacts"]["synthesizer"]["payload"]["routing"]["final_policy"]["rules"]
                             if r["rule_id"] == "SYN-ESC-012")
        self.assertEqual(view["references"][handle]["value"], recorded_rule)
        self.assertIn(inert(recorded_rule["rule_id"]) + ": " + inert(recorded_rule["control_result"]),
                      run["outcome"]["report_markdown"])
        self.assertEqual(packet["request"]["reference_dictionary"][handle]["value"]["evaluation_state"], "NOT_EVALUATED")
        self.assertEqual(run, original_run)
        self.assertEqual(packet, original_packet)
        self.assertEqual(get_run(self.store, self.actor, operation), original_run)
        preliminary = deepcopy(run)
        preliminary["artifacts"].pop("synthesizer")
        prior = policy_display(preliminary, packet)
        self.assertEqual(prior["basis"], "PRE_SYNTHESIS_PRELIMINARY")
        self.assertEqual(next(r for r in prior["rules"] if r["ref"] == handle)["result"], "Pending")
        self.assertEqual(policy_display(run, None)["references"], {})
        wrong = deepcopy(packet)
        wrong["input_digest"] = "another-input"
        with self.assertRaisesRegex(InputError, "SOURCE_MISMATCH"):
            policy_display(run, wrong)
        wrong_run = deepcopy(run)
        wrong_run["artifacts"]["synthesizer"]["scope"]["run_id"] = uid("different-run")
        with self.assertRaisesRegex(InputError, "SYNTHESIS_MISMATCH"):
            policy_display(wrong_run, packet)

    def test_final_policy_card_and_evidence_agree_and_source_mismatch_withholds_links(self):
        run_normal_fixture(self.root, uid("policy-final-ui"))
        app = self.app()
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Recorded final policy evaluation" in c.value for c in app.caption))
        self.assertTrue(any("Observed: 0.85 | Threshold: 0.7" == t.value for t in app.text))
        label = "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-012"
        self.assertTrue(any(label + " · NOT_TRIGGERED" in m.value for m in app.markdown))
        widget(app.button, "↗ " + label).click().run()
        self.assertEqual(widget(app.selectbox, "Evidence reference").value, label)
        rows = [row for frame in app.dataframe for row in frame.value.to_dict("records")]
        self.assertTrue(any(row.get("Property") == "Evaluation State" and row.get("Recorded value") == "EVALUATED" for row in rows))
        self.assertTrue(any(row.get("Property") == "Observed" and row.get("Recorded value") == "0.85" for row in rows))
        with patch("deal_or_no_deal_ai.ui.command_center.source_packet", side_effect=InputError("SOURCE_MISMATCH")):
            app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Citations are withheld" in w.value for w in app.warning))
        self.assertFalse(any(b.label.startswith("↗ ") for b in app.button))

    def test_start_authorization_and_uncertain_execution_not_complete(self):
        with patch("deal_or_no_deal_ai.worker.run_normal_fixture", side_effect=AssertionError("NO_DISPATCH")):
            with self.assertRaisesRegex(InputError, "START_NOT_PERMITTED"):
                start_run(self.root, replace(self.actor, persona="Administrator"), uid("denied"))
        self.assertFalse(self.store.path.exists())
        operation = uid("command-center-uncertain")
        with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=InputError("FAULT")):
            with self.assertRaisesRegex(InputError, "FAULT"):
                run_normal_fixture(self.root, operation)
        run = get_run(self.store, self.actor, operation)
        self.assertEqual(run["status"], "RECOVERY_REQUIRED")
        self.assertIsNone(run["outcome"].get("report_markdown"))
        self.assertIsNone(run["human_disposition"])

    def test_changed_stored_report_is_not_presented_as_original_pipeline_output(self):
        operation = uid("command-center-changed-report")
        run_normal_fixture(self.root, operation)
        key = "normal-result:" + operation
        version, original = self.store.get_record(key)
        self.store.put_record(RecordWrite(key, "NORMAL_FIXTURE_OUTCOME",
                                         {**original, "report_markdown": "Replaced report"}, version))
        with self.assertRaisesRegex(InputError, "REPORT_MISMATCH"):
            get_run(self.store, self.actor, operation)

    def test_explicit_ui_run_to_workspace_citations_memo_history_and_no_replay(self):
        pair = patch.object(socket, "socketpair", internal_event_loop_pair)
        pair.start()
        self.addCleanup(pair.stop)
        code = ("from pathlib import Path\nfrom deal_or_no_deal_ai.ui.command_center import main\n"
                + "main(Path(" + repr(str(self.root)) + "))\n")
        app = AppTest.from_string(code, default_timeout=30).run()
        self.assertFalse(self.store.path.exists())
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.button, "Run AI Deal Review").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(list_runs(self.store, self.actor)), 1)
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_REPLAY")):
            widget(app.button, "Run AI Deal Review").click().run()
            for page in ("Deal Dashboard", "Review Workspace", "Agent Activity", "Credit Memo", "Decision History"):
                widget(app.sidebar.radio, "Page").set_value(page).run()
                self.assertEqual(len(app.exception), 0, page)
                self.assertEqual(len(app.error), 0, page)
                if page == "Review Workspace":
                    self.assertTrue(widget(app.selectbox, "Evidence reference").options)
                    self.assertTrue(any("Original page" in item.value for item in app.caption))
                if page == "Credit Memo":
                    self.assertTrue(any("Executive Summary" in item.value for item in app.markdown))
        self.assertEqual(len(list_runs(self.store, self.actor)), 1)
