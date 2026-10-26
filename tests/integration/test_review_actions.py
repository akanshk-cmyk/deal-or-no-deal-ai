"""Scoped REVIEW-UI-1.0 persistence/permissions, not real credit dispositions."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pydantic import ValidationError

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.review_actions import (
    ReviewActionCommand, get_review_panel, list_review_examples, prepare_review_examples,
    preview_actor, record_review_action,
)
from deal_or_no_deal_ai.storage import OperationConflict, RecordWrite, RunBusy, StaleRecord, Store
from tests.support import OfflineTest, uid


class ReviewActionTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.store = Store(Path(self.folder.name) / "review.sqlite3")
        prepare_review_examples(self.store)
        self.analyst = preview_actor("Analyst")
        self.approver = preview_actor("AuthorizedApprover")
        self.rows = list_review_examples(self.store, self.analyst)
        self.request_id = self.rows[0]["request_id"]
        self.clock = lambda: datetime(2026, 10, 24, 10, 30, tzinfo=timezone(timedelta(hours=-7)))

    def panel(self, actor=None, request_id=None):
        return get_review_panel(self.store, request_id or self.request_id, actor or self.analyst)

    def command(self, action="ADD_COMMENT", *, request_id=None, **changes):
        panel = self.panel(request_id=request_id)
        data = dict(operation_id=uid("review-action:" + str(panel["record_version"]) + action),
            request_id=panel["request"]["request_id"], expected_version=panel["record_version"],
            expected_gate_version=panel["request"]["gate_version"],
            expected_basis=panel["request"]["analytical_basis_digest"], action=action,
            comments="Synthetic review comment", requested_items=[])
        data.update(changes)
        return ReviewActionCommand(**data)

    def test_role_matrix_is_enforced_by_service_as_well_as_projection(self):
        for role in ("Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"):
            actor = preview_actor(role)
            actions = self.panel(actor)["actions"]
            with self.subTest(role=role):
                self.assertEqual(actions["ADD_COMMENT"] is None, role != "Administrator")
                self.assertEqual(actions["REQUEST_INFORMATION"] is None, role != "Administrator")
                self.assertEqual(actions["APPROVE"] is None, role == "AuthorizedApprover")
                self.assertEqual(actions["REJECT"] is None, role == "AuthorizedApprover")
                if role != "AuthorizedApprover":
                    with self.assertRaises(InputError):
                        record_review_action(self.store, actor, self.command("APPROVE"), clock=self.clock)
        self.assertEqual(self.panel()["history"], [])

    def test_approval_records_comment_role_status_utc_and_duplicate_timestamp_once(self):
        command = self.command("APPROVE", comments="Evidence reviewed for the UI example.")
        event = record_review_action(self.store, self.approver, command, clock=self.clock)
        self.assertEqual(event["timestamp_utc"], "2026-10-24T17:30:00+00:00")
        self.assertEqual(event["decision_status"], "APPROVED")
        self.assertEqual(event["reviewer_role"], "AuthorizedApprover")
        self.assertEqual(event["comments"], command.comments)
        self.assertEqual(event["graph_progress"], "NOT_CONNECTED")
        self.assertEqual(event["provenance"], "ILLUSTRATIVE_UI_ONLY")
        def no_clock():
            raise AssertionError("DUPLICATE_MUST_KEEP_ORIGINAL_TIME")
        duplicate = record_review_action(self.store, self.approver, command, clock=no_clock)
        self.assertEqual(duplicate, event)
        self.assertEqual(len(self.panel()["history"]), 1)
        self.assertIsNone(self.panel()["original_ai_recommendation"])
        with self.assertRaises(OperationConflict):
            record_review_action(self.store, self.approver, command.model_copy(update={"comments": "Changed"}))

    def test_rejection_is_final_but_later_comment_does_not_change_decision(self):
        record_review_action(self.store, self.approver, self.command("REJECT"), clock=self.clock)
        self.assertEqual(self.panel()["decision_status"], "REJECTED")
        record_review_action(self.store, self.analyst, self.command("ADD_COMMENT"), clock=self.clock)
        self.assertEqual(self.panel()["decision_status"], "REJECTED")
        self.assertEqual(len(self.panel()["history"]), 2)
        with self.assertRaises(InputError):
            record_review_action(self.store, self.approver, self.command("APPROVE"))

    def test_information_request_is_pending_and_cannot_be_cleared_by_note_or_role_switch(self):
        command = self.command("REQUEST_INFORMATION", requested_items=["Provide the missing statement."])
        record_review_action(self.store, self.analyst, command, clock=self.clock)
        panel = self.panel(self.approver)
        self.assertEqual(panel["decision_status"], "NEEDS_INFORMATION")
        self.assertEqual(panel["request"]["state"], "PENDING")
        self.assertEqual(panel["actions"]["APPROVE"], "INFORMATION_REQUEST_OUTSTANDING")
        record_review_action(self.store, self.approver, self.command("ADD_COMMENT"), clock=self.clock)
        self.assertTrue(self.panel()["information_pending"])
        for action in ("APPROVE", "REJECT"):
            with self.subTest(action=action), self.assertRaises(InputError):
                record_review_action(self.store, self.approver, self.command(action))
        self.assertEqual(self.panel()["history"][0]["requested_items"], command.requested_items)

    def test_blockers_and_senior_tier_cannot_be_bypassed(self):
        blocked, senior = self.rows[1]["request_id"], self.rows[2]["request_id"]
        with self.assertRaisesRegex(InputError, "PREREQUISITE_UNSATISFIED"):
            record_review_action(self.store, self.approver, self.command("REJECT", request_id=blocked))
        with self.assertRaisesRegex(InputError, "APPROVER_TIER_REQUIRED"):
            record_review_action(self.store, self.approver, self.command("APPROVE", request_id=senior))
        event = record_review_action(self.store, preview_actor("AuthorizedApprover", senior=True),
                                    self.command("APPROVE", request_id=senior), clock=self.clock)
        self.assertEqual(event["reviewer_tiers"], ["NORMAL", "SENIOR"])

    def test_out_of_scope_and_unknown_roles_cannot_read_or_write(self):
        for actor in (replace(self.analyst, workspace_id=uid("foreign-workspace")),
                      replace(self.analyst, allowed_deal_ids=frozenset()),
                      replace(self.analyst, attribution="UNVERIFIED"),
                      replace(self.analyst, persona="UnknownRole")):
            with self.subTest(actor=actor), self.assertRaises(InputError):
                get_review_panel(self.store, self.request_id, actor)
            with self.subTest(actor=actor), self.assertRaises(InputError):
                record_review_action(self.store, actor, self.command())
        self.assertEqual(self.panel()["history"], [])

    def test_comments_and_information_items_are_required_and_bounded(self):
        original = self.command().model_dump()
        for update in ({"comments": "   "}, {"comments": "x" * 4097}, {"expected_version": True},
                       {"action": "REQUEST_INFORMATION"}, {"requested_items": ["Unexpected"]},
                       {"action": "REQUEST_INFORMATION", "requested_items": ["a", " a "]},
                       {"action": "REQUEST_INFORMATION", "requested_items": ["x" * 513]}):
            with self.subTest(update=list(update)), self.assertRaises(ValidationError):
                ReviewActionCommand.model_validate(original | update)
        self.assertEqual(self.panel()["history"], [])

    def test_stale_version_basis_or_gate_and_busy_execution_record_nothing(self):
        old = self.command()
        record_review_action(self.store, self.analyst, old, clock=self.clock)
        with self.assertRaises(StaleRecord):
            record_review_action(self.store, self.analyst, old.model_copy(update={"operation_id": uid("competing")}))
        for update in ({"expected_basis": "0" * 64}, {"expected_gate_version": 999}):
            with self.subTest(update=update), self.assertRaises(InputError):
                record_review_action(self.store, self.analyst, self.command(**update))
        claim = self.store.admit(uid("active"), {"review_id": uid("active-review")}, {"action": "RUN"})
        self.assertEqual(self.panel(self.approver)["actions"]["APPROVE"], "RUN_BUSY")
        with self.assertRaises(RunBusy):
            record_review_action(self.store, self.approver, self.command("APPROVE"))
        self.assertEqual(len(self.panel()["history"]), 1)
        self.store.release(claim, confirmed_idle=True)

    def test_failed_transaction_rolls_back_event_and_status_and_naive_time_is_denied(self):
        original = Store._write
        def fail(connection, write):
            if write.kind == "ILLUSTRATIVE_UI_REVIEW":
                raise OSError("controlled write failure")
            return original(connection, write)
        with patch.object(Store, "_write", side_effect=fail), self.assertRaises(OSError):
            record_review_action(self.store, self.approver, self.command("APPROVE"), clock=self.clock)
        self.assertEqual(self.panel()["history"], [])
        self.assertEqual(self.panel()["decision_status"], "AWAITING_REVIEW")
        with self.assertRaisesRegex(InputError, "TIMESTAMP_REQUIRED"):
            record_review_action(self.store, self.analyst, self.command(), clock=lambda: datetime(2026, 10, 24))

    def test_preparation_reuses_same_database_and_preserves_original_records_and_history(self):
        self.store.put_record(RecordWrite("existing-normal-artifact", "NORMAL_FIXTURE", {"keep": True}))
        record_review_action(self.store, self.analyst, self.command(), clock=self.clock)
        before = self.panel()
        prepare_review_examples(self.store)
        self.assertEqual(self.panel(), before)
        self.assertEqual(self.store.get_record("existing-normal-artifact"), (1, {"keep": True}))
        with self.store.connection() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM app_record_history WHERE record_key=?",
                ("ui-review:request:" + self.request_id,)).fetchone()[0], 2)
