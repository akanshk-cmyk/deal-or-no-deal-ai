"""SPEC-013 read-only scope/snapshot/filter/export checks on synthetic UI records."""

import csv
from dataclasses import replace
from datetime import date, datetime, timezone
from hashlib import sha256
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pydantic import ValidationError

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.decision_history import (
    HistoryFilters, export_decision_history_csv, get_deal_timeline, query_decision_history,
)
from deal_or_no_deal_ai.review_actions import (
    ReviewActionCommand, get_review_panel, list_review_examples, prepare_review_examples,
    preview_actor, record_review_action,
)
from deal_or_no_deal_ai.storage import RecordWrite, Store
from tests.support import OfflineTest, uid


class DecisionHistoryTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.store = Store(Path(self.folder.name) / "review.sqlite3")
        prepare_review_examples(self.store)
        self.actor = preview_actor("Analyst")
        self.reviews = list_review_examples(self.store, self.actor)
        self.deals = [get_review_panel(self.store, r["request_id"], self.actor)["request"]["deal_id"] for r in self.reviews]
        self.sequence = 0

    def action(self, index=0, action="ADD_COMMENT", *, text="Synthetic comment", stamp="2026-10-24T12:00:00+00:00"):
        panel = get_review_panel(self.store, self.reviews[index]["request_id"], self.actor)
        self.sequence += 1
        command = ReviewActionCommand(operation_id=uid("history-event:" + str(self.sequence)),
            request_id=panel["request"]["request_id"], expected_version=panel["record_version"],
            expected_gate_version=panel["request"]["gate_version"], expected_basis=panel["request"]["analytical_basis_digest"],
            action=action, comments=text, requested_items=["Updated statement"] if action == "REQUEST_INFORMATION" else [])
        actor = preview_actor("AuthorizedApprover", senior=True) if action in ("APPROVE", "REJECT") else self.actor
        return record_review_action(self.store, actor, command, clock=lambda: datetime.fromisoformat(stamp))

    def update_context(self, index, **changes):
        key = "ui-review:request:" + self.reviews[index]["request_id"]
        version, data = self.store.get_record(key)
        data.update(changes)
        self.store.put_record(RecordWrite(key, "ILLUSTRATIVE_UI_REVIEW", data, version))

    def test_new_event_captures_transition_name_and_context_before_later_changes(self):
        self.update_context(0, deal_context=dict(borrower_name="Original borrower", loan_amount="1200000", currency="USD", deal_type="TERM_LOAN"),
            decision_context=dict(ai_recommendation="Approve", ai_analysis_version="TEST-ANALYSIS-1",
                risk_assessment={"score": "21", "band": "LOW", "basis": "SYNTHETIC_TEST_ONLY"},
                compliance_findings=["Synthetic policy result"], policy_exceptions=[],
                supporting_documents=[dict(source_id="TEST-P1", version="1", page=1, text="Synthetic evidence")] ))
        self.action(stamp="2026-10-20T09:00:00+00:00")
        self.action(action="APPROVE")
        self.update_context(0, deal_context={"borrower_name": "Later name", "loan_amount": "999"},
                            decision_context={"ai_recommendation": "Reject", "risk_assessment": {"score": "99"}})
        rows = get_deal_timeline(self.store, self.actor, self.deals[0])
        self.assertEqual(rows[0]["previous_status"], "AWAITING_REVIEW")
        self.assertEqual(rows[0]["new_status"], "AWAITING_REVIEW")
        self.assertEqual(rows[0]["current_status"], "APPROVED")
        self.assertEqual(rows[1]["new_status"], "APPROVED")
        self.assertEqual(rows[1]["reviewer_name"], "Demo Authorized Approver")
        for row in rows:
            self.assertEqual(row["borrower_name"], "Original borrower")
            self.assertEqual(row["loan_amount"], "1200000")
            self.assertEqual(row["context_snapshot"]["risk_assessment"]["score"], "21")
            self.assertEqual(row["context_snapshot"]["ai_analysis_version"], "TEST-ANALYSIS-1")
            self.assertEqual(row["context_snapshot"]["supporting_documents"][0]["text"], "Synthetic evidence")

    def test_legacy_event_uses_exact_saved_version_and_never_invents_a_reviewer_name(self):
        self.update_context(0, deal_context={})
        event = self.action()
        key = "ui-review:event:" + event["operation_id"]
        version, saved = self.store.get_record(key)
        for field in ("context_snapshot", "previous_status", "reviewer_name", "event_sequence"):
            saved.pop(field)
        self.store.put_record(RecordWrite(key, "ILLUSTRATIVE_UI_REVIEW_EVENT", saved, version))
        self.update_context(0, deal_context={"borrower_name": "Future borrower"})
        original = self.store.get_record(key)
        row = query_decision_history(self.store, self.actor)["rows"][0]
        self.assertEqual(row["snapshot_source"], "RECORDED_PRE_ACTION_VERSION")
        self.assertEqual(row["previous_status"], "AWAITING_REVIEW")
        self.assertIsNone(row["borrower_name"])
        self.assertIsNone(row["reviewer_name"])
        self.assertEqual(self.store.get_record(key), original)

    def test_scope_filtering_happens_before_counts_and_export(self):
        self.action(0)
        self.action(1, "REQUEST_INFORMATION")
        subset = replace(self.actor, allowed_deal_ids=frozenset({self.deals[0]}))
        for role in ("Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"):
            actor = replace(subset, persona=role)
            view = query_decision_history(self.store, actor)
            self.assertEqual(view["total"], 1)
            self.assertEqual({row["deal_id"] for row in view["rows"]}, {self.deals[0]})
            report = export_decision_history_csv(self.store, actor, HistoryFilters(), expected_digest=view["snapshot_digest"])
            self.assertEqual(report["row_count"], 1)
            self.assertNotIn(self.deals[1], report["content"].decode("utf-8-sig"))
        with self.assertRaises(InputError):
            get_deal_timeline(self.store, subset, self.deals[1])
        self.assertEqual(query_decision_history(self.store, replace(self.actor, workspace_id=uid("foreign-workspace")))["total"], 0)
        for actor in (replace(self.actor, persona="Unknown"), replace(self.actor, attribution="UNVERIFIED")):
            with self.assertRaises(InputError):
                query_decision_history(self.store, actor)

    def test_all_filters_and_inclusive_utc_dates_work_before_pagination(self):
        self.action(0, stamp="2026-10-23T23:59:59+00:00")
        self.action(0, "APPROVE", stamp="2026-10-24T23:59:59+00:00")
        self.action(1, "REQUEST_INFORMATION", stamp="2026-10-25T00:00:00+00:00")
        cases = [(HistoryFilters(deal_id=self.deals[0][4:20]), 2),
                 (HistoryFilters(borrower="UI SAMPLE READY"), 2),
                 (HistoryFilters(reviewer="authorizedapprover"), 1),
                 (HistoryFilters(actions=["REQUEST_INFORMATION"]), 1),
                 (HistoryFilters(statuses=["APPROVED"]), 1),
                 (HistoryFilters(start_date=date(2026, 10, 24), end_date=date(2026, 10, 24)), 1),
                 (HistoryFilters(borrower="not-present"), 0)]
        for filters, expected in cases:
            with self.subTest(filters=filters):
                self.assertEqual(query_decision_history(self.store, self.actor, filters, limit=1)["total"], expected)
        with self.assertRaises(ValidationError):
            HistoryFilters(start_date=date(2026, 10, 25), end_date=date(2026, 10, 24))

    def test_stable_order_pagination_and_complete_timeline_independent_of_filters(self):
        for i in range(4):
            self.action(0, text="Comment " + str(i), stamp="2026-10-24T12:00:00+00:00")
        first = query_decision_history(self.store, self.actor, offset=0, limit=2)
        second = query_decision_history(self.store, self.actor, offset=2, limit=2)
        self.assertEqual(first["snapshot_digest"], second["snapshot_digest"])
        self.assertEqual([row["event_sequence"] for row in first["rows"]], [4, 3])
        self.assertEqual([row["event_sequence"] for row in second["rows"]], [2, 1])
        timeline = get_deal_timeline(self.store, self.actor, self.deals[0])
        self.assertEqual([row["event_sequence"] for row in timeline], [1, 2, 3, 4])
        self.assertEqual(query_decision_history(self.store, self.actor, HistoryFilters(reviewer="no such reviewer"))["total"], 0)
        self.assertEqual(len(get_deal_timeline(self.store, self.actor, self.deals[0])), 4)

    def test_export_contains_all_pages_and_formula_neutralization_preserves_stored_comment(self):
        malicious = '=HYPERLINK("https://example.invalid","synthetic")\nSecond line'
        event = self.action(text=malicious)
        self.action(1, "REQUEST_INFORMATION")
        view = query_decision_history(self.store, self.actor, limit=1)
        export = export_decision_history_csv(self.store, self.actor, HistoryFilters(), expected_digest=view["snapshot_digest"],
            clock=lambda: datetime(2026, 10, 24, 16, tzinfo=timezone.utc))
        rows = list(csv.DictReader(StringIO(export["content"].decode("utf-8-sig"))))
        self.assertEqual(len(rows), 2)
        row = next(row for row in rows if row["event_id"] == event["operation_id"])
        self.assertEqual(row["comments"], "'" + malicious)
        self.assertEqual(row["ai_recommendation"], "Not captured")
        self.assertEqual(row["exported_at_utc"], "2026-10-24T16:00:00+00:00")
        self.assertEqual(get_deal_timeline(self.store, self.actor, self.deals[0])[0]["comments"], malicious)

    def test_stale_or_other_actor_digest_cannot_export_cached_rows(self):
        self.action()
        view = query_decision_history(self.store, self.actor)
        self.action(text="Later event")
        with self.assertRaisesRegex(InputError, "STALE_REFRESH"):
            export_decision_history_csv(self.store, self.actor, HistoryFilters(), expected_digest=view["snapshot_digest"])
        fresh = query_decision_history(self.store, self.actor)
        with self.assertRaises(InputError):
            export_decision_history_csv(self.store, preview_actor("Administrator"), HistoryFilters(), expected_digest=fresh["snapshot_digest"])

    def test_bounded_export_and_timeline_fail_instead_of_silently_truncating(self):
        self.action()
        self.action(text="Second")
        view = query_decision_history(self.store, self.actor)
        with patch("deal_or_no_deal_ai.decision_history.MAX_EXPORT_EVENTS", 1):
            with self.assertRaisesRegex(InputError, "EXPORT_LIMIT"):
                export_decision_history_csv(self.store, self.actor, HistoryFilters(), expected_digest=view["snapshot_digest"])
            with self.assertRaisesRegex(InputError, "TIMELINE_LIMIT"):
                get_deal_timeline(self.store, self.actor, self.deals[0])

    def test_history_and_export_do_not_write_and_missing_database_stays_missing(self):
        missing = Store(Path(self.folder.name) / "not-created.sqlite3")
        self.assertEqual(query_decision_history(missing, self.actor)["total"], 0)
        self.assertFalse(missing.path.exists())
        self.action()
        before = sha256(self.store.path.read_bytes()).hexdigest()
        view = query_decision_history(self.store, self.actor)
        get_deal_timeline(self.store, self.actor, self.deals[0])
        export_decision_history_csv(self.store, self.actor, HistoryFilters(), expected_digest=view["snapshot_digest"])
        self.assertEqual(sha256(self.store.path.read_bytes()).hexdigest(), before)

    def test_page_and_filter_types_are_strict_and_corrupt_cross_deal_event_is_withheld(self):
        for kwargs in ({"offset": -1}, {"limit": 101}, {"offset": True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(InputError):
                query_decision_history(self.store, self.actor, **kwargs)
        for kwargs in ({"borrower": "x" * 201}, {"actions": ["Unknown"]}, {"start_date": "2026-10-24"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValidationError):
                HistoryFilters(**kwargs)
        event = self.action()
        key = "ui-review:event:" + event["operation_id"]
        version, payload = self.store.get_record(key)
        payload["context_snapshot"]["deal_id"] = self.deals[1]
        self.store.put_record(RecordWrite(key, "ILLUSTRATIVE_UI_REVIEW_EVENT", payload, version))
        with self.assertRaisesRegex(InputError, "SNAPSHOT_SCOPE"):
            query_decision_history(self.store, self.actor)
