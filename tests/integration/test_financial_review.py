"""Actual financial fixture interrupt/resume, no provider or illustrative actions."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from deal_or_no_deal_ai.command_center import get_run, workspace_id
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.financial_review import get_financial_review, record_financial_action
from deal_or_no_deal_ai.financial_review import InformationResponseCommand, respond_and_reassess, financial_history, financial_history_csv
from deal_or_no_deal_ai.context import fingerprint, strict_json
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.review_actions import ReviewActionCommand
from deal_or_no_deal_ai.storage import OperationConflict, StaleRecord, Store
from deal_or_no_deal_ai.worker import run_normal_fixture
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import OfflineTest, uid


class FinancialReviewTests(OfflineTest):
    def setUp(self):
        super().setUp()
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        copy_workspace(self.root)
        self.store = Store(self.root / "var/deal_review.sqlite3")
        self.operation = uid("financial-review-run")
        self.paused = run_normal_fixture(self.root, self.operation, variant="review")
        self.actor = Actor("AuthorizedApprover", workspace_id(self.root),
                           frozenset({self.paused["scope"]["deal_id"]}), frozenset({"NORMAL"}))

    def panel(self, actor=None):
        return get_financial_review(self.store, actor or self.actor,
                                    get_run(self.store, actor or self.actor, self.operation))

    def command(self, action, **changes):
        panel = self.panel()
        values = dict(operation_id=uid("financial-action:" + action + str(panel["version"])),
                      request_id=panel["request"].request_id, expected_version=panel["version"],
                      expected_gate_version=panel["request"].gate_version, expected_basis=panel["request"].analytical_basis_digest,
                      action=action, comments="Synthetic committee review; source basis inspected.", requested_items=[])
        values.update(changes)
        return ReviewActionCommand(**values)

    def test_actual_pause_reopen_reject_resume_memo_and_duplicate(self):
        self.assertEqual(self.paused["status"], "WAITING_REVIEW")
        self.assertIsNone(self.paused["report_markdown"])
        self.assertEqual(self.paused["ledger"]["committed"]["nodes"], 9)
        self.assertEqual(len(self.paused["ledger"]["reservations"]), 1)
        with self.assertRaisesRegex(InputError,"APPROVAL_READINESS_BLOCKED"):
            record_financial_action(self.root,self.actor,self.operation,self.command("APPROVE"))
        command = self.command("REJECT")
        result = record_financial_action(self.root, self.actor, self.operation, command)
        outcome = result["outcome"]
        self.assertEqual(outcome["status"], "COMPLETED")
        self.assertEqual(outcome["human_disposition"], "Reject")
        self.assertEqual(outcome["scope"]["thread_id"], self.paused["scope"]["thread_id"])
        self.assertEqual(outcome["ledger"]["committed"]["nodes"], 11)
        self.assertEqual(outcome["ledger"]["reservations"], {})
        self.assertEqual(outcome["provider_requests"], 0)
        self.assertIn("Human disposition: Reject", outcome["report_markdown"])
        self.assertEqual(len(self.panel()["events"]), 1)
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_REPLAY")):
            duplicate = record_financial_action(self.root, self.actor, self.operation, command)
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(duplicate["event"], result["event"])
        with self.assertRaises(OperationConflict):
            record_financial_action(self.root, self.actor, self.operation,
                                    command.model_copy(update={"comments": "Changed"}))

    def test_role_gate_information_request_and_comment_never_clear_blocker(self):
        analyst = replace(self.actor, persona="Analyst", allowed_review_tiers=frozenset())
        with self.assertRaises(InputError):
            record_financial_action(self.root, analyst, self.operation, self.command("APPROVE"))
        result = record_financial_action(self.root, analyst, self.operation,
                    self.command("REQUEST_INFORMATION", requested_items=["Confirm financial statement basis."]))
        self.assertEqual(result["outcome"]["status"], "WAITING_INFORMATION")
        record_financial_action(self.root, analyst, self.operation, self.command("ADD_COMMENT"))
        self.assertTrue(self.panel()["data"]["information_pending"])
        with self.assertRaisesRegex(InputError, "INFORMATION_REQUEST_OUTSTANDING"):
            record_financial_action(self.root, self.actor, self.operation, self.command("APPROVE"))

    def test_reject_preserves_ai_and_never_reexecutes_model_stages(self):
        before = get_run(self.store, self.actor, self.operation)
        with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=AssertionError("NO_GENERATION_REPLAY")):
            result = record_financial_action(self.root, self.actor, self.operation,
                self.command("REJECT", comments="Synthetic committee declines the proposed exposure after review."))
        self.assertEqual(result["outcome"]["human_disposition"], "Reject")
        after = get_run(self.store, self.actor, self.operation)
        self.assertEqual(before["artifacts"]["synthesizer"], after["artifacts"]["synthesizer"])
        self.assertIn("Human disposition: Reject", result["outcome"]["report_markdown"])
        self.assertEqual(result["outcome"]["report_metadata"]["renderer_version"], "E-N01-REVIEW-MEMO-1.0/READINESS-1.0/RECOMMENDATION-1.0")

    def test_financial_history_filters_pagination_and_all_page_export(self):
        from datetime import datetime, timezone
        from deal_or_no_deal_ai.financial_review import FinancialHistoryFilters, query_financial_history
        record_financial_action(self.root, self.actor, self.operation, self.command("ADD_COMMENT", comments="First review note."))
        record_financial_action(self.root, self.actor, self.operation, self.command("ADD_COMMENT", comments="Second review note."))
        record_financial_action(self.root, self.actor, self.operation, self.command("REJECT"))
        day = datetime.now(timezone.utc).date()
        filters = FinancialHistoryFilters(borrower="equipment", reviewer="authorizedapprover", start_date=day, end_date=day)
        before = self.store.path.read_bytes()
        result = query_financial_history(self.store, self.actor, filters, limit=1)
        self.assertEqual(result["total"], 3)
        self.assertEqual(len(result["rows"]), 1)
        second = query_financial_history(self.store, self.actor, filters, offset=1, limit=1)
        self.assertNotEqual(result["rows"][0]["operation_id"], second["rows"][0]["operation_id"])
        raw = financial_history_csv(self.store, self.actor, None, expected_digest=result["snapshot_digest"], filters=filters)
        self.assertIn(b"First review note.", raw)
        self.assertIn(b"Second review note.", raw)
        approved = query_financial_history(self.store, self.actor, FinancialHistoryFilters(actions=["REJECT"], statuses=["REJECTED"]))
        self.assertEqual(approved["total"], 1)
        excluded = replace(self.actor, allowed_deal_ids=frozenset())
        self.assertEqual(query_financial_history(self.store, excluded, filters)["total"], 0)
        self.assertEqual(self.store.path.read_bytes(), before)
        stale = result["snapshot_digest"]
        record_financial_action(self.root, self.actor, self.operation, self.command("ADD_COMMENT", comments="Later comment."))
        with self.assertRaises(StaleRecord):
            financial_history_csv(self.store, self.actor, None, expected_digest=stale, filters=filters)

    def test_wrong_tier_stale_and_out_of_scope_cannot_record(self):
        with self.assertRaises(InputError):
            record_financial_action(self.root, replace(self.actor, allowed_deal_ids=frozenset()), self.operation, self.command("APPROVE"))
        with self.assertRaisesRegex(InputError, "APPROVER_TIER_REQUIRED"):
            record_financial_action(self.root, replace(self.actor, allowed_review_tiers=frozenset()), self.operation, self.command("APPROVE"))
        stale = self.command("APPROVE")
        record_financial_action(self.root, self.actor, self.operation, self.command("ADD_COMMENT"))
        with self.assertRaises(StaleRecord):
            record_financial_action(self.root, self.actor, self.operation, stale)
        self.assertEqual(len(self.panel()["events"]), 1)

    def test_resume_failure_retains_one_decision_and_requires_recovery(self):
        command = self.command("REJECT")
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=InputError("CONTROLLED_CHECKPOINT_FAULT")):
            with self.assertRaisesRegex(InputError, "CONTROLLED_CHECKPOINT_FAULT"):
                record_financial_action(self.root, self.actor, self.operation, command)
        run = get_run(self.store, self.actor, self.operation)
        self.assertEqual(run["status"], "RECOVERY_REQUIRED")
        self.assertIsNone(run["outcome"]["report_markdown"])
        duplicate = record_financial_action(self.root, self.actor, self.operation, command)
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(len(self.panel()["events"]), 1)

    def test_registered_response_reassesses_new_revision_same_budget_and_stales_old_review(self):
        record_financial_action(self.root, self.actor, self.operation,
            self.command("REQUEST_INFORMATION", requested_items=["Confirm supplied annual financial basis."]))
        stale_approval = self.command("APPROVE")
        panel = self.panel()
        command = InformationResponseCommand(operation_id=uid("registered-response"), expected_version=panel["version"],
            expected_basis=panel["request"].analytical_basis_digest, comments="Registered financial source inspected for the requested basis.",
            reference_by_item=["FIN-P2"])
        pack = self.root / "fixtures/development/e-n01"
        manifest = strict_json((pack / "manifest.json").read_bytes())
        document = (pack / next(s["path"] for s in manifest["sources"] if s["source_id"] == "FINANCIALS-1")).read_bytes()
        risk_manager = replace(self.actor, persona="RiskManager", allowed_review_tiers=frozenset())
        with self.assertRaisesRegex(InputError, "REGISTERED_DOCUMENT"):
            respond_and_reassess(self.root, risk_manager, self.operation, command, b"Unregistered PDF")
        result = respond_and_reassess(self.root, risk_manager, self.operation, command, document)
        child = result["outcome"]
        self.assertEqual(child["status"], "WAITING_REVIEW")
        self.assertEqual(child["scope"]["input_revision"], 2)
        self.assertEqual(child["scope"]["review_id"], self.paused["scope"]["review_id"])
        self.assertNotEqual(child["scope"]["thread_id"], self.paused["scope"]["thread_id"])
        parent = get_run(self.store, self.actor, self.operation)
        self.assertEqual(parent["status"], "SUPERSEDED")
        with self.assertRaises(StaleRecord):
            record_financial_action(self.root, self.actor, self.operation, stale_approval)
        run = get_run(self.store, self.actor, command.operation_id)
        current = get_financial_review(self.store, self.actor, run)
        approval = ReviewActionCommand(operation_id=uid("revision2-approval"), request_id=current["request"].request_id,
            expected_version=current["version"], expected_basis=current["request"].analytical_basis_digest,
            expected_gate_version=current["request"].gate_version, action="REJECT", comments="Reassessment reviewed; separate human rejection decision.", requested_items=[])
        completed = record_financial_action(self.root, self.actor, command.operation_id, approval)["outcome"]
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(completed["ledger"]["committed"]["nodes"], 19)
        self.assertTrue(completed["ledger"]["correction_used"])
        self.assertEqual(completed["ledger"]["reservations"], {})
        self.assertEqual(completed["report_metadata"]["input_revision"], 2)
        self.assertEqual([e["event"] for e in completed["audit_events"][:2]], ["artifact_reused", "artifact_reused"])
        duplicate = respond_and_reassess(self.root, risk_manager, self.operation, command, document)
        self.assertTrue(duplicate["duplicate"])

    def test_financial_history_export_is_scoped_frozen_and_rejects_stale_snapshot(self):
        record_financial_action(self.root, self.actor, self.operation,
            self.command("REJECT", comments="=HYPERLINK(\"https://example.invalid\")"))
        deal = self.paused["scope"]["deal_id"]
        events = financial_history(self.store, self.actor, deal)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["analysis_snapshot"]["ai"]["raw_escalate_to_human"], True)
        self.assertIn("FIN-P2", events[0]["analysis_snapshot"]["sources"])
        data = financial_history_csv(self.store, self.actor, deal, expected_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))
        self.assertIn("'=HYPERLINK", data.decode("utf-8-sig"))
        with self.assertRaises(InputError):
            financial_history(self.store, replace(self.actor, allowed_deal_ids=frozenset()), deal)
        comment = self.command("ADD_COMMENT", comments="Post-decision note; no change in disposition.")
        result = record_financial_action(self.root, self.actor, self.operation, comment)
        self.assertEqual(result["outcome"]["status"], "COMPLETED")
        self.assertEqual(result["outcome"]["human_disposition"], "Reject")
        with self.assertRaises(StaleRecord):
            financial_history_csv(self.store, self.actor, deal, expected_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))

    def test_concurrent_identical_responses_admit_one_reassessment(self):
        record_financial_action(self.root, self.actor, self.operation,
            self.command("REQUEST_INFORMATION", requested_items=["Confirm annual financial basis."]))
        panel = self.panel()
        command = InformationResponseCommand(operation_id=uid("concurrent-response"), expected_version=panel["version"],
            expected_basis=panel["request"].analytical_basis_digest, comments="Registered basis assessed.", reference_by_item=["FIN-P2"])
        pack = self.root / "fixtures/development/e-n01"
        manifest = strict_json((pack / "manifest.json").read_bytes())
        document = (pack / next(s["path"] for s in manifest["sources"] if s["source_id"] == "FINANCIALS-1")).read_bytes()
        actor = replace(self.actor, persona="RiskManager", allowed_review_tiers=frozenset())
        barrier = Barrier(2)
        original = Store.admit
        def synchronized(store, operation, *args, **kwargs):
            if operation == command.operation_id:
                barrier.wait(timeout=30)
            return original(store, operation, *args, **kwargs)
        with patch.object(Store, "admit", synchronized), ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(respond_and_reassess, self.root, actor, self.operation, command, document) for _ in range(2)]
            results = [task.result() for task in tasks]
        self.assertEqual(sum(result["duplicate"] for result in results), 1)
        child = get_run(self.store, self.actor, command.operation_id)
        self.assertEqual(child["status"], "WAITING_REVIEW")
        self.assertEqual(len(financial_history(self.store, self.actor, child["context"]["scope"]["deal_id"])), 2)
