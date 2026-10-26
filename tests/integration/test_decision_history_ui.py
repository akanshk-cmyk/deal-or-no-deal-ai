"""SPEC-013 real Streamlit page tests; not manual browser/accessibility evidence."""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import socket
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from deal_or_no_deal_ai.review_actions import (
    ReviewActionCommand, get_review_panel, list_review_examples, prepare_review_examples,
    preview_actor, record_review_action,
)
from deal_or_no_deal_ai.storage import Store
from tests.integration.test_human_review_ui import internal_event_loop_pair, widget
from tests.support import OfflineTest, ROOT, uid


class DecisionHistoryUITests(OfflineTest):
    def setUp(self):
        super().setUp()
        socketpair = patch.object(socket, "socketpair", internal_event_loop_pair)
        socketpair.start()
        self.addCleanup(socketpair.stop)
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        self.store = Store(self.root / "var/deal_review.sqlite3")
        self.actor = preview_actor("Analyst")

    def seed_events(self):
        prepare_review_examples(self.store)
        reviews = list_review_examples(self.store, self.actor)
        self.events = []
        self.deals = []
        for i, action in enumerate(("APPROVE", "REQUEST_INFORMATION", "REJECT")):
            panel = get_review_panel(self.store, reviews[i]["request_id"], self.actor)
            self.deals.append(panel["request"]["deal_id"])
            command = ReviewActionCommand(operation_id=uid("history-ui-event:" + str(i)),
                request_id=reviews[i]["request_id"], expected_version=panel["record_version"], expected_gate_version=1,
                expected_basis=panel["request"]["analytical_basis_digest"], action=action,
                comments="Synthetic history reason " + str(i), requested_items=["Updated financial statement"] if i == 1 else [])
            actor = self.actor if i == 1 else preview_actor("AuthorizedApprover", senior=True)
            self.events.append(record_review_action(self.store, actor, command,
                clock=lambda: datetime(2026, 10, 24, 12, tzinfo=timezone.utc)))

    def app(self, *, seed=True):
        if seed:
            self.seed_events()
        code = "from pathlib import Path\nfrom tools.preview_human_review import main\nmain(Path(" + repr(str(self.root)) + "))\n"
        app = AppTest.from_string(code, default_timeout=20).run()
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertEqual(len(app.exception), 0)
        return app

    def test_navigation_empty_history_is_read_only_and_never_seeds_fake_events(self):
        app = self.app(seed=False)
        self.assertFalse(self.store.path.exists())
        self.assertTrue(any(element.value == "Decision History" for element in app.header))
        self.assertEqual(next(item for item in app.metric if item.label == "Matching history events").value, "0")
        self.assertTrue(widget(app.button, "Prepare CSV audit report").disabled)
        self.assertTrue(any("No recorded events" in item.value for item in app.info))

    def test_dashboard_fields_filters_and_selected_event_show_original_comments(self):
        app = self.app()
        self.assertEqual(next(item for item in app.metric if item.label == "Matching history events").value, "3")
        widget(app.text_input, "Borrower").input("UI Sample blocked borrower").run()
        self.assertEqual(next(item for item in app.metric if item.label == "Matching history events").value, "1")
        event_id = self.events[1]["operation_id"]
        widget(app.selectbox, "Open event details").select(event_id).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any(item.value == "Synthetic history reason 1" for item in app.text))
        self.assertTrue(any(item.value == "Requested information: Updated financial statement" for item in app.text))
        self.assertTrue(any("Not captured for this event" in item.value for item in app.info))
        self.assertTrue(any("Historical risk assessment" == item.label for item in app.expander))

    def test_timeline_is_clickable_and_not_limited_by_dashboard_action_filter(self):
        app = self.app()
        widget(app.multiselect, "Decision / action type").set_value(["REQUEST_INFORMATION"]).run()
        widget(app.selectbox, "Timeline deal").select(self.deals[0]).run()
        event_id = self.events[0]["operation_id"]
        next(button for button in app.button if button.key == "history_timeline:" + event_id).click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any(item.value == "Synthetic history reason 0" for item in app.text))
        self.assertTrue(any("Demo Authorized Approver" in item.value for item in app.text))

    def test_export_is_explicit_and_filter_change_invalidates_prepared_download(self):
        app = self.app()
        self.assertNotIn("history_prepared_export", app.session_state)
        widget(app.button, "Prepare CSV audit report").click().run()
        self.assertEqual(len(app.exception), 0)
        report = app.session_state["history_prepared_export"]
        self.assertEqual(report["row_count"], 3)
        self.assertIn(b"timestamp_utc", report["content"])
        self.assertEqual(len(app.get("download_button")), 1)
        widget(app.text_input, "Reviewer name, ID or role").input("no such reviewer").run()
        self.assertNotIn("history_prepared_export", app.session_state)
        self.assertEqual(len(app.get("download_button")), 0)

    def test_administrator_history_access_does_not_grant_review_actions(self):
        app = self.app()
        widget(app.sidebar.selectbox, "Demo role").select("Administrator").run()
        self.assertEqual(next(item for item in app.metric if item.label == "Matching history events").value, "3")
        widget(app.button, "Prepare CSV audit report").click().run()
        self.assertEqual(app.session_state["history_prepared_export"]["row_count"], 3)
        widget(app.sidebar.radio, "Page").set_value("Human review").run()
        self.assertTrue(widget(app.button, "Record review action").disabled)
