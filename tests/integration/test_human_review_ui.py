"""Streamlit AppTest of the actual reusable panel; no browser/accessibility claim."""

from pathlib import Path
import shutil
import socket
import threading
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from deal_or_no_deal_ai.review_actions import get_review_panel, list_review_examples, prepare_review_examples, preview_actor
from deal_or_no_deal_ai.storage import Store
from tests.support import OfflineTest, ROOT


_REAL_CONNECT = socket.socket.connect
_REAL_SOCKETPAIR = socket.socketpair


def internal_event_loop_pair(*args, **kwargs):
    """Windows asyncio wake-up pair only; never allow HTTP/provider traffic."""
    owner = threading.get_ident()
    def connect(sock, address):
        if threading.get_ident() == owner and isinstance(address, tuple) and address[0] == "127.0.0.1":
            return _REAL_CONNECT(sock, address)
        raise AssertionError("OUTBOUND_NETWORK_FORBIDDEN_IN_UI_TESTS")
    with patch.object(socket.socket, "connect", connect):
        return _REAL_SOCKETPAIR(*args, **kwargs)


def widget(elements, label):
    return next(element for element in elements if element.label == label)


class HumanReviewUITests(OfflineTest):
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

    def app(self, *, prepared=True):
        if prepared:
            prepare_review_examples(self.store)
        code = "from pathlib import Path\nfrom tools.preview_human_review import main\nmain(Path(" + repr(str(self.root)) + "))\n"
        return AppTest.from_string(code, default_timeout=20).run()

    def role(self, app, role):
        widget(app.sidebar.selectbox, "Demo role").select(role).run()
        self.assertEqual(len(app.exception), 0)

    def test_open_is_read_only_and_preparation_requires_explicit_click(self):
        app = self.app(prepared=False)
        self.assertEqual(len(app.exception), 0)
        self.assertFalse(self.store.path.exists())
        widget(app.button, "Prepare UI review samples").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(list_review_examples(self.store, preview_actor("Analyst"))), 3)
        action = widget(app.selectbox, "Review action")
        self.assertIsNone(action.value)
        self.assertTrue(widget(app.button, "Record review action").disabled)

    def test_analyst_can_comment_but_cannot_select_approve_or_reject_and_text_is_inert(self):
        app = self.app()
        action = widget(app.selectbox, "Review action")
        self.assertNotIn("Approve", action.options)
        self.assertNotIn("Reject", action.options)
        action.select("ADD_COMMENT").run()
        raw = '<script>alert("example")</script> [link](https://example.invalid)'
        widget(app.text_area, "Review comments (required)").input(raw)
        widget(app.button, "Record review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any(item.value == raw for item in app.text))
        rows = list_review_examples(self.store, preview_actor("Analyst"))
        panel = get_review_panel(self.store, rows[0]["request_id"], preview_actor("Analyst"))
        self.assertEqual(panel["history"][0]["comments"], raw)
        self.assertEqual(panel["decision_status"], "AWAITING_REVIEW")

    def test_approver_records_approval_with_comments_and_timestamp(self):
        app = self.app()
        self.role(app, "AuthorizedApprover")
        widget(app.selectbox, "Review action").select("APPROVE").run()
        widget(app.text_area, "Review comments (required)").input("Synthetic approval explanation.")
        widget(app.button, "Record review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.success), 1)
        self.assertEqual(next(item for item in app.metric if item.label == "Review status").value,
                         "Approved — simulated UI decision")
        rows = list_review_examples(self.store, preview_actor("Analyst"))
        panel = get_review_panel(self.store, rows[0]["request_id"], preview_actor("Analyst"))
        self.assertEqual(panel["decision_status"], "APPROVED")
        self.assertEqual(panel["history"][0]["reviewer_role"], "AuthorizedApprover")
        self.assertTrue(panel["history"][0]["timestamp_utc"].endswith("+00:00"))
        self.assertEqual(panel["graph_progress"], "NOT_CONNECTED")

    def test_information_request_creates_pending_history_and_blocks_later_approval(self):
        app = self.app()
        widget(app.selectbox, "Review action").select("REQUEST_INFORMATION").run()
        widget(app.text_area, "Review comments (required)").input("Need supporting information.")
        widget(app.text_area, "Requested information (required — one item per line)").input("Updated statement\nCollateral schedule")
        widget(app.button, "Record review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.role(app, "AuthorizedApprover")
        self.assertNotIn("Approve", widget(app.selectbox, "Review action").options)
        self.assertTrue(any("Pending — additional information requested" in item.value for item in app.text))

    def test_missing_comment_error_preserves_draft_and_administrator_is_read_only(self):
        app = self.app()
        widget(app.selectbox, "Review action").select("REQUEST_INFORMATION").run()
        widget(app.text_area, "Requested information (required — one item per line)").input("Retain this requested item")
        widget(app.button, "Record review action").click().run()
        self.assertGreater(len(app.error), 0)
        self.assertEqual(widget(app.text_area, "Requested information (required — one item per line)").value,
                         "Retain this requested item")
        self.role(app, "Administrator")
        self.assertTrue(widget(app.selectbox, "Review action").disabled)
        self.assertTrue(widget(app.button, "Record review action").disabled)
        self.assertEqual(len(app.exception), 0)

    def test_refresh_reveals_new_status_and_keeps_comment_draft(self):
        app = self.app()
        widget(app.selectbox, "Review action").select("ADD_COMMENT").run()
        widget(app.text_area, "Review comments (required)").input("Retain my review context.")
        widget(app.button, "Record review action").click().run()
        app.run()
        self.assertTrue(any("review has changed" in item.value for item in app.warning))
        widget(app.button, "Refresh review").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(widget(app.text_area, "Review comments (required)").value, "Retain my review context.")

    def test_switching_deals_preserves_draft_without_recording_it_against_another_deal(self):
        app = self.app()
        rows = list_review_examples(self.store, preview_actor("Analyst"))
        widget(app.text_area, "Review comments (required)").input("Draft belongs to sample A.").run()
        widget(app.selectbox, "Deal").select(rows[1]).run()
        self.assertEqual(widget(app.text_area, "Review comments (required)").value, "")
        widget(app.selectbox, "Deal").select(rows[0]).run()
        self.assertEqual(widget(app.text_area, "Review comments (required)").value, "Draft belongs to sample A.")
        for row in rows:
            self.assertEqual(get_review_panel(self.store, row["request_id"], preview_actor("Analyst"))["history"], [])
