"""Actual E-P01 source/graph, distinct specialist gates and outstanding condition."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.command_center import get_run, start_run, workspace_id
from deal_or_no_deal_ai.context import InputError, strict_json, fingerprint
from deal_or_no_deal_ai.financial_review import (ExceptionHandlingCommand, ConditionActionCommand, FinancialActionCommand,
    get_financial_review, record_exception_handling, record_financial_action, financial_history, financial_history_csv)
from deal_or_no_deal_ai.conditional_review import CONDITION, supported_condition, record_condition_action
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store, RecordWrite, StaleRecord, OperationConflict
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import widget
from tests.support import OfflineTest, ROOT, uid


class ConditionalReviewTests(OfflineTest):
    def setUp(self):
        super().setUp()
        temp = TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); copy_workspace(self.root)
        shutil.copytree(ROOT / "fixtures/development/e-p01", self.root / "fixtures/development/e-p01")
        deal = strict_json((self.root / "config/registrations/e-p01.json").read_bytes())["deal_id"]
        self.actor = Actor("AuthorizedApprover", workspace_id(self.root), frozenset({deal}), frozenset({"NORMAL"}))
        self.operation = uid("conditional-review")
        start_run(self.root, replace(self.actor, persona="Analyst"), self.operation, scenario_id="E-P01", variant="review")
        self.store = Store(self.root / "var/deal_review.sqlite3")

    def panel(self):
        return get_financial_review(self.store, self.actor, get_run(self.store, self.actor, self.operation))

    def base(self, name):
        p = self.panel(); q = p["request"]
        return dict(operation_id=uid(name), request_id=q.request_id, expected_version=p["version"],
            expected_gate_version=q.gate_version, expected_basis=q.analytical_basis_digest)

    def handling(self, **changes):
        values = dict(**self.base("conditional-handling"), rule_id="SYN-ESC-001", handling="ACCEPT_FOR_CONDITIONAL_REVIEW",
            comments="DSCR exception retained; annual statements do not cure repayment capacity. Refer for supported condition review.",
            evidence_refs=["E-P01:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"])
        values.update(changes)
        return ExceptionHandlingCommand(**values)

    def condition(self, domain=None, **changes):
        p = self.panel()
        refs = supported_condition(get_run(self.store, self.actor, self.operation)["artifacts"]["synthesizer"]["payload"])[1]
        values = dict(**self.base("condition:" + str(domain)), action="CONDITION_SUPPORTED" if domain else "CONDITION_DRAFT_PREPARED",
            condition_text=CONDITION, comments="Verified original covenant and retained DSCR exception. This is not a repayment cure.",
            evidence_refs=refs, domain=domain, draft_digest=p["data"].get("condition_draft", {}).get("content_digest"))
        values.update(changes)
        return ConditionActionCommand(**values)

    def final(self, action="CONDITIONAL_APPROVE"):
        return FinancialActionCommand(**self.base("conditional-final:" + action), action=action,
            comments="Reviewed specialist support and original DSCR exception; condition remains outstanding. No funding authorized.",
            requested_items=["Supply updated evidence"] if action == "REQUEST_INFORMATION" else [])

    def ready(self):
        risk = replace(self.actor, persona="RiskManager")
        record_exception_handling(self.root, risk, self.operation, self.handling())
        record_condition_action(self.root, self.actor, self.operation, self.condition())
        record_condition_action(self.root, risk, self.operation, self.condition("FINANCIAL_RISK"))
        record_condition_action(self.root, replace(self.actor, persona="ComplianceOfficer"), self.operation, self.condition("POLICY_CONTROL"))

    def test_actual_conditional_graph_preserves_original_findings_and_outstanding_condition(self):
        before = get_run(self.store, self.actor, self.operation)
        self.assertEqual(before["status"], "WAITING_REVIEW")
        self.assertEqual(before["artifacts"]["risk_quantifier"]["payload"]["score"]["display"], "33.00")
        for action in ("CONDITIONAL_APPROVE", "REJECT"):
            with self.assertRaisesRegex(InputError, "PREREQUISITE"):
                record_financial_action(self.root, self.actor, self.operation, self.final(action))
        with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=AssertionError("NO_REGENERATION")):
            self.ready()
            self.assertEqual(get_run(self.store, self.actor, self.operation)["artifacts"], before["artifacts"])
            with self.assertRaisesRegex(InputError, "CONDITIONAL_PATH_ONLY"):
                record_financial_action(self.root, self.actor, self.operation, self.final("APPROVE"))
            with self.assertRaisesRegex(InputError,"APPROVAL_READINESS_BLOCKED"):
                record_financial_action(self.root,self.actor,self.operation,self.final())
            result = record_financial_action(self.root, self.actor, self.operation, self.final("REJECT"))["outcome"]
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["human_disposition"], "Reject")
        self.assertEqual(result["ledger"]["committed"]["nodes"], 11)
        self.assertEqual(result["ledger"]["committed"]["tools"], 4)
        self.assertEqual(result["provider_requests"], 0)
        for text in ("OUTSTANDING", "Owner: Unassigned", "Original policy outcome remains Exception", "Conditional Approve"):
            self.assertIn(text, result["report_markdown"])
        events = financial_history(self.store, self.actor)
        self.assertEqual([e["action"] for e in events], ["EXCEPTION_DISPOSITION", "CONDITION_DRAFT_PREPARED", "CONDITION_SUPPORTED", "CONDITION_SUPPORTED", "REJECT"])
        self.assertEqual(events[-1]["new_status"], "REJECTED")
        self.assertEqual(events[-1]["condition_record"]["status"], "OUTSTANDING")
        raw = financial_history_csv(self.store, self.actor, None, expected_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))
        self.assertIn(b"OUTSTANDING", raw)
        final = get_run(self.store, self.actor, self.operation)
        human = deepcopy(final["artifacts"]["human_review"]["payload"])
        from deal_or_no_deal_ai.financial_review import validate_human_record
        from deal_or_no_deal_ai.contracts import Scope
        human["condition_events"].pop()
        with self.assertRaisesRegex(InputError, "CONDITION_RECEIPTS_REQUIRED"):
            validate_human_record(human, Scope.model_validate(final["context"]["scope"]))

    def test_roles_exact_condition_sources_stale_and_duplicate_receipts(self):
        with self.assertRaises(InputError):
            record_condition_action(self.root, self.actor, self.operation, self.condition())
        risk = replace(self.actor, persona="RiskManager")
        cmd = self.handling()
        record_exception_handling(self.root, risk, self.operation, cmd)
        self.assertTrue(record_exception_handling(self.root, risk, self.operation, cmd)["duplicate"])
        for role in ("RiskManager", "ComplianceOfficer", "Analyst", "Administrator"):
            with self.assertRaisesRegex(InputError, "ROLE_REQUIRED"):
                record_condition_action(self.root, replace(self.actor, persona=role), self.operation, self.condition())
        with self.assertRaisesRegex(InputError, "EVIDENCE_MISMATCH"):
            record_condition_action(self.root, self.actor, self.operation, self.condition(condition_text="Invented repayment cure"))
        cmd = self.condition(); stale = self.final()
        record_condition_action(self.root, self.actor, self.operation, cmd)
        self.assertTrue(record_condition_action(self.root, self.actor, self.operation, cmd)["duplicate"])
        with self.assertRaises(OperationConflict):
            record_condition_action(self.root, self.actor, self.operation, cmd.model_copy(update={"comments": "changed"}))
        with self.assertRaises(StaleRecord):
            record_financial_action(self.root, self.actor, self.operation, stale)
        with self.assertRaisesRegex(InputError, "ROLE_REQUIRED"):
            record_condition_action(self.root, replace(self.actor, persona="ComplianceOfficer"), self.operation, self.condition("FINANCIAL_RISK"))
        record_condition_action(self.root, risk, self.operation, self.condition("FINANCIAL_RISK"))
        with self.assertRaisesRegex(InputError, "PREREQUISITE"):
            record_financial_action(self.root, self.actor, self.operation, self.final())
        p = self.panel(); bad = deepcopy(p["data"]); bad["condition_draft"]["conditions"] = ["Changed condition"]
        self.store.put_record(RecordWrite("financial-review:" + bad["scope"]["run_id"], "FINANCIAL_REVIEW", bad, p["version"]))
        with self.assertRaisesRegex(InputError, "CONDITION_DRAFT_RECEIPT_MISMATCH"):
            get_run(self.store, self.actor, self.operation)

    def test_reject_is_distinct_human_choice_and_information_stays_blocking(self):
        self.ready()
        result = record_financial_action(self.root, self.actor, self.operation, self.final("REJECT"))["outcome"]
        self.assertEqual(result["human_disposition"], "Reject")
        self.assertIn("Simulated recommendation: **Conditional Approve**", result["report_markdown"])

    def test_information_request_blocks_condition_preparation_and_final(self):
        record_exception_handling(self.root, replace(self.actor, persona="RiskManager"), self.operation, self.handling())
        record_financial_action(self.root, self.actor, self.operation, self.final("REQUEST_INFORMATION"))
        with self.assertRaises(StaleRecord):
            record_condition_action(self.root, self.actor, self.operation, self.condition())
        with self.assertRaises(InputError):
            record_financial_action(self.root, self.actor, self.operation, self.final())

    def test_source_change_and_wrong_support_digest_are_blocked(self):
        record_exception_handling(self.root, replace(self.actor, persona="RiskManager"), self.operation, self.handling())
        record_condition_action(self.root, self.actor, self.operation, self.condition())
        with self.assertRaisesRegex(InputError, "CURRENT_CONDITION_DRAFT_REQUIRED"):
            record_condition_action(self.root, replace(self.actor, persona="RiskManager"), self.operation,
                                    self.condition("FINANCIAL_RISK", draft_digest="0" * 64))
        path = self.root / "fixtures/development/e-p01/agreement.pdf"
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaises(InputError):
            record_condition_action(self.root, replace(self.actor, persona="RiskManager"), self.operation, self.condition("FINANCIAL_RISK"))

    def test_concurrent_identical_preparation_records_one_event(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        record_exception_handling(self.root, replace(self.actor, persona="RiskManager"), self.operation, self.handling())
        command = self.condition(); barrier = Barrier(2); original = Store.admit
        def synchronized(store, operation, *args, **kwargs):
            if operation == command.operation_id:
                barrier.wait(timeout=30)
            return original(store, operation, *args, **kwargs)
        with patch.object(Store, "admit", synchronized), ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(record_condition_action, self.root, self.actor, self.operation, command) for _ in range(2)]
            results = [task.result() for task in tasks]
        self.assertEqual(sum(not r["duplicate"] for r in results), 1)
        self.assertEqual(len(financial_history(self.store, self.actor)), 2)

    def test_ui_specialist_handoff_conditional_memo_history_and_citations(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        self.assertTrue(any("Policy Exception" in option for option in widget(app.selectbox, "Sample scenario").options))
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        widget(app.sidebar.selectbox, "Demo role").select("RiskManager").run()
        widget(app.multiselect, "Exception supporting evidence").set_value(self.handling().evidence_refs)
        widget(app.text_area, "Risk Manager handling reason (required)").input("Refer for supported condition review; DSCR exception remains.")
        widget(app.checkbox, "I acknowledge this condition does not cure the DSCR exception").check()
        widget(app.button, "Record exception handling · Accept for conditional review").click().run()
        self.assertEqual(len(app.exception), 0)
        widget(app.sidebar.selectbox, "Demo role").select("AuthorizedApprover").run()
        self.assertNotIn("Conditional Approve", widget(app.selectbox, "Financial review action").options)
        def submit_condition(label):
            widget(app.text_area, "Condition review reason (required)").input("Verified covenant and unchanged DSCR exception; no repayment cure.")
            widget(app.multiselect, "Condition supporting evidence").set_value(supported_condition(get_run(self.store, self.actor, self.operation)["artifacts"]["synthesizer"]["payload"])[1])
            widget(app.checkbox, "I verified the unchanged condition and acknowledge it does not cure DSCR or authorize funding").check()
            widget(app.button, label).click().run()
            self.assertEqual(len(app.exception), 0)
        submit_condition("Prepare registered condition draft")
        widget(app.sidebar.selectbox, "Demo role").select("RiskManager").run()
        submit_condition("Record Financial Risk support")
        widget(app.sidebar.selectbox, "Demo role").select("ComplianceOfficer").run()
        submit_condition("Record Policy Control support")
        widget(app.sidebar.selectbox, "Demo role").select("AuthorizedApprover").run()
        self.assertNotIn("Conditional Approve",widget(app.selectbox,"Financial review action").options)
        widget(app.selectbox, "Financial review action").select("REJECT").run()
        widget(app.text_area, "Financial review comments (required)").input("Conditional approval after both specialist reviews. Condition outstanding.")
        widget(app.checkbox, "Confirm this simulated final decision").check()
        widget(app.button, "Record financial review action").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(get_run(self.store, self.actor, self.operation)["human_disposition"], "Reject")
        widget(app.sidebar.radio, "Page").set_value("Credit Memo").run()
        self.assertTrue(any("OUTSTANDING" in item.value for item in app.markdown))
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertIn("CONDITIONAL_APPROVE", widget(app.multiselect, "History actions").options)
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        next(b for b in app.button if b.label == "↗ Policy Exception:AGREEMENT-P1").click().run()
        self.assertEqual(widget(app.selectbox, "Evidence reference").value, "E-P01:AGREEMENT-P1")
        self.assertEqual(len(app.exception), 0)
