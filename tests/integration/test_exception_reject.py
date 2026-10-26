"""Actual supported Reject through separate handling and the shared paused graph."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from deal_or_no_deal_ai.command_center import get_run, start_run, workspace_id
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.financial_review import (ExceptionHandlingCommand, get_financial_review,
    record_exception_handling, record_financial_action, financial_history, financial_history_csv)
from deal_or_no_deal_ai.context import fingerprint
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.review_actions import ReviewActionCommand
from deal_or_no_deal_ai.storage import OperationConflict, StaleRecord, RecordWrite, Store
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import widget
from tests.support import OfflineTest, ROOT, uid


class ExceptionRejectTests(OfflineTest):
    def setUp(self):
        super().setUp()
        temp = TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); copy_workspace(self.root)
        shutil.copytree(ROOT / "fixtures/development/e-f03", self.root / "fixtures/development/e-f03")
        from deal_or_no_deal_ai.context import strict_json
        deal = strict_json((self.root / "config/registrations/e-f03.json").read_bytes())["deal_id"]
        self.actor = Actor("AuthorizedApprover", workspace_id(self.root), frozenset({deal}), frozenset({"NORMAL"}))
        self.operation = uid("supported-reject")
        start_run(self.root, replace(self.actor, persona="Analyst"), self.operation, scenario_id="E-F03", variant="review")
        self.store = Store(self.root / "var/deal_review.sqlite3")

    def panel(self, actor=None):
        return get_financial_review(self.store, actor or self.actor, get_run(self.store, actor or self.actor, self.operation))

    def handling(self, **changes):
        p = self.panel(); q = p["request"]
        values = dict(operation_id=uid("risk-handling"), request_id=q.request_id, expected_version=p["version"],
            expected_gate_version=q.gate_version, expected_basis=q.analytical_basis_digest, rule_id="SYN-ESC-001",
            handling="RECOMMEND_REJECT", comments="Negative supplied CFADS cannot cover service; no supported remedy supplied.",
            evidence_refs=["E-F03:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"])
        values.update(changes)
        return ExceptionHandlingCommand(**values)

    def final(self, action="REJECT"):
        p = self.panel(); q = p["request"]
        return ReviewActionCommand(operation_id=uid("supported-final:" + action), request_id=q.request_id,
            expected_version=p["version"], expected_gate_version=q.gate_version, expected_basis=q.analytical_basis_digest,
            action=action, comments="Reviewed negative annual CFADS and RiskManager's supported exception handling.",
            requested_items=["Confirm no repayment remedy is documented."] if action == "REQUEST_INFORMATION" else [])

    def test_supported_reject_preserves_findings_and_never_replays_generation(self):
        before = get_run(self.store, self.actor, self.operation)
        self.assertEqual(before["status"], "WAITING_REVIEW")
        self.assertEqual(before["artifacts"]["risk_quantifier"]["payload"]["score"]["display"], "45.00")
        for action in ("APPROVE", "REJECT"):
            with self.assertRaisesRegex(InputError, "PREREQUISITE_UNSATISFIED"):
                record_financial_action(self.root, self.actor, self.operation, self.final(action))
        stale = self.final()
        risk_manager = replace(self.actor, persona="RiskManager", allowed_review_tiers=frozenset())
        command = self.handling()
        with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=AssertionError("NO_MODEL_REPLAY")):
            record_exception_handling(self.root, risk_manager, self.operation, command)
            self.assertTrue(record_exception_handling(self.root, risk_manager, self.operation, command)["duplicate"])
            after_handling = get_run(self.store, self.actor, self.operation)
            self.assertEqual(after_handling["status"], "WAITING_REVIEW")
            self.assertEqual(after_handling["artifacts"], before["artifacts"])
            self.assertFalse(after_handling["unhandled_exception_ids"])
            with self.assertRaises(StaleRecord):
                record_financial_action(self.root, self.actor, self.operation, stale)
            with self.assertRaisesRegex(InputError, "RECOMMENDS_REJECT"):
                record_financial_action(self.root, self.actor, self.operation, self.final("APPROVE"))
            with self.assertRaisesRegex(InputError, "APPROVER_TIER_REQUIRED"):
                record_financial_action(self.root, risk_manager, self.operation, self.final())
            result = record_financial_action(self.root, self.actor, self.operation, self.final())["outcome"]
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["human_disposition"], "Reject")
        self.assertEqual(result["ledger"]["committed"]["nodes"], 11)
        self.assertEqual(result["provider_requests"], 0)
        for text in ("Simulated recommendation: **Reject**", "Human disposition: Reject", "RECOMMEND", "Original policy outcome remains Exception"):
            self.assertIn(text, result["report_markdown"])
        final = get_run(self.store, self.actor, self.operation)
        self.assertEqual(final["artifacts"]["synthesizer"], before["artifacts"]["synthesizer"])
        from deal_or_no_deal_ai.command_center import source_packet
        from deal_or_no_deal_ai.contracts import Scope
        from deal_or_no_deal_ai.memo import ReportInput, render_memo
        human = deepcopy(final["artifacts"]["human_review"]["payload"])
        self.assertNotIn("analysis_snapshot", human["exception_events"][0])
        self.assertIn("event_snapshot_digest", human["exception_events"][0])
        human["exception_events"] = []
        metadata = final["outcome"]["report_metadata"]
        with self.assertRaisesRegex(InputError, "FINAL_EXCEPTION_RECEIPTS_REQUIRED"):
            render_memo(ReportInput(Scope.model_validate(final["context"]["scope"]), source_packet(self.root, final),
                final["artifacts"]["synthesizer"]["payload"],
                tuple(e for e in final["events"] if e["sequence"] <= metadata["audit_cutoff_sequence"]), metadata["generation_time"], human))
        events = financial_history(self.store, self.actor)
        self.assertEqual([e["action"] for e in events], ["EXCEPTION_DISPOSITION", "REJECT"])
        raw = financial_history_csv(self.store, self.actor, None, expected_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))
        self.assertIn(b"EXCEPTION_DISPOSITION", raw)
        self.assertIn(b"Negative supplied CFADS", raw)
        self.assertIn(b"exception_handling", raw)
        self.assertIn(b"RECOMMEND_REJECT", raw)

    def test_wrong_role_scope_refs_source_version_and_payload_conflict(self):
        command = self.handling()
        for role in ("Analyst", "AuthorizedApprover", "ComplianceOfficer", "Administrator"):
            with self.assertRaisesRegex(InputError, "RISK_MANAGER"):
                record_exception_handling(self.root, replace(self.actor, persona=role), self.operation, command)
        manager = replace(self.actor, persona="RiskManager")
        with self.assertRaises(InputError):
            record_exception_handling(self.root, replace(manager, allowed_deal_ids=frozenset()), self.operation, command)
        with self.assertRaisesRegex(InputError, "REFERENCE_OUT_OF_SCOPE"):
            record_exception_handling(self.root, manager, self.operation, self.handling(evidence_refs=["FIN-P2"]))
        with self.assertRaisesRegex(InputError, "EVIDENCE_MISMATCH"):
            record_exception_handling(self.root, manager, self.operation, self.handling(evidence_refs=["calc:DSCR"]))
        record_exception_handling(self.root, manager, self.operation, command)
        with self.assertRaises(OperationConflict):
            record_exception_handling(self.root, manager, self.operation, command.model_copy(update={"comments": "Different reason"}))
        source = self.root / "fixtures/development/e-f03/financials.pdf"
        source.write_bytes(source.read_bytes() + b"changed")
        with self.assertRaises(InputError):
            record_financial_action(self.root, self.actor, self.operation, self.final())

    def test_concurrent_identical_handling_commits_one_event(self):
        command = self.handling(); manager = replace(self.actor, persona="RiskManager")
        barrier = Barrier(2)
        def submit():
            barrier.wait(timeout=10)
            return record_exception_handling(self.root, manager, self.operation, command)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: submit(), range(2)))
        self.assertEqual(sum(not r["duplicate"] for r in results), 1)
        self.assertEqual(len(financial_history(self.store, self.actor)), 1)
        self.assertEqual(self.panel()["request"].gate_version, 2)

    def test_forged_handling_map_is_rejected_and_information_stays_blocking(self):
        manager = replace(self.actor, persona="RiskManager")
        record_exception_handling(self.root, manager, self.operation, self.handling())
        cmd = self.final("REQUEST_INFORMATION").model_copy(update={"requested_items": ["Confirm no repayment remedy is documented."]})
        record_financial_action(self.root, self.actor, self.operation, cmd)
        with self.assertRaisesRegex(InputError, "INFORMATION_REQUEST_OUTSTANDING"):
            record_financial_action(self.root, self.actor, self.operation, self.final())
        p = self.panel(); bad = deepcopy(p["data"]); bad["exception_handling"] = {}
        self.store.put_record(RecordWrite("financial-review:" + bad["scope"]["run_id"], "FINANCIAL_REVIEW", bad, p["version"]))
        with self.assertRaisesRegex(InputError, "RECEIPT_MISMATCH"):
            get_run(self.store, self.actor, self.operation)

    def test_ui_role_handoff_handling_then_reject_and_memo(self):
        from tests.integration.test_command_center import CommandCenterTests
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        widget(app.sidebar.selectbox, "Demo role").select("AuthorizedApprover").run()
        self.assertNotIn("REJECT", widget(app.selectbox, "Financial review action").options)
        widget(app.sidebar.selectbox, "Demo role").select("RiskManager").run()
        refs = ["E-F03:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"]
        widget(app.multiselect, "Exception supporting evidence").set_value(refs)
        widget(app.text_area, "Risk Manager handling reason (required)").input("Negative CFADS and documented service shortfall support rejection.")
        widget(app.button, "Record exception handling · Recommend Reject").click().run()
        self.assertEqual(len(app.exception), 0)
        widget(app.sidebar.selectbox, "Demo role").select("AuthorizedApprover").run()
        self.assertNotIn("APPROVE", widget(app.selectbox, "Financial review action").options)
        widget(app.selectbox, "Financial review action").select("REJECT").run()
        widget(app.text_area, "Financial review comments (required)").input("Reject following supported CFADS and independent RiskManager review.")
        widget(app.checkbox, "Confirm this simulated final decision").check()
        widget(app.button, "Record financial review action").click().run()
        self.assertEqual(len(app.exception), 0)
        widget(app.sidebar.radio, "Page").set_value("Credit Memo").run()
        self.assertTrue(any("Human disposition: Reject" in item.value for item in app.markdown))
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("EXCEPTION_DISPOSITION", widget(app.multiselect, "History actions").options)
