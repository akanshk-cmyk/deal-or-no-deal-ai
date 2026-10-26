"""Actual extraction miss→saved READY correction→recomputed source-bound report."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.command_center import start_run, get_run, workspace_id, source_packet
from deal_or_no_deal_ai.context import strict_json, InputError
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.source_correction import (SaveCorrectionCommand, UpdateCorrectionCommand, correction_basis,
    draft_basis, save_source_correction, update_affected_findings)
from deal_or_no_deal_ai.storage import Store, StaleRecord, OperationConflict
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import widget
from tests.support import OfflineTest, uid


class SourceCorrectionTests(OfflineTest):
    def setUp(self):
        super().setUp()
        folder = TemporaryDirectory(); self.addCleanup(folder.cleanup)
        self.root = Path(folder.name); copy_workspace(self.root)
        deal = strict_json((self.root / "config/registrations/e-n01.json").read_bytes())["deal_id"]
        self.actor = Actor("Analyst", workspace_id(self.root), frozenset({deal}))
        self.operation = uid("extraction-miss")
        self.result = start_run(self.root, self.actor, self.operation, variant="extraction-miss")
        self.store = Store(self.root / "var/deal_review.sqlite3")

    def command(self, **changes):
        parent = get_run(self.store, self.actor, self.operation)
        values = dict(operation_id=uid("save-source-correction"), expected_version=self.store.get_record("normal-result:" + self.operation)[0],
            expected_basis=correction_basis(parent), field="cash_available_for_debt_service", value="900000", basis_id="FY-ASSESS",
            evidence_ref="FIN-P2", comments="Verified annual CFADS900000 on original financial schedule, not a new document.")
        values.update(changes)
        return SaveCorrectionCommand(**values)

    def save(self):
        return save_source_correction(self.root, self.actor, self.operation, self.command())

    def update_command(self, operation):
        version, draft = self.store.get_record("source-correction:" + operation)
        return UpdateCorrectionCommand(expected_version=version, expected_basis=draft_basis(draft))

    def test_save_is_metadata_only_and_explicit_update_recomputes_with_shared_budget(self):
        self.assertEqual(self.result["status"], "WAITING_INFORMATION")
        self.assertEqual(self.result["ledger"]["committed"]["nodes"], 5)
        parent = get_run(self.store, self.actor, self.operation)
        self.assertNotIn("synthesizer", parent["artifacts"])
        self.assertIsNone(parent["artifacts"]["extractor"]["payload"]["wire"]["financial_inputs"]["cash_available_for_debt_service"]["value"])
        self.assertIn("900000", source_packet(self.root, parent)["request"]["reference_dictionary"]["FIN-P2"]["text"])
        with patch("deal_or_no_deal_ai.worker.run_normal_fixture", side_effect=AssertionError("SAVE_MUST_NOT_RUN_GRAPH")):
            saved = self.save()
        child = get_run(self.store, self.actor, saved["operation_id"])
        self.assertEqual(child["status"], "READY")
        self.assertFalse(child["artifacts"])
        old = get_run(self.store, self.actor, self.operation)
        self.assertEqual(old["status"], "SUPERSEDED")
        self.assertEqual(old["artifacts"], parent["artifacts"])
        self.assertEqual(child["context"]["scope"]["review_id"], parent["context"]["scope"]["review_id"])
        self.assertNotEqual(child["context"]["scope"]["thread_id"], parent["context"]["scope"]["thread_id"])
        self.assertEqual(child["context"]["scope"]["input_revision"], 2)
        command = self.update_command(saved["operation_id"])
        result = update_affected_findings(self.root, self.actor, saved["operation_id"], command)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["ledger"]["committed"]["nodes"], 12)
        self.assertEqual(result["ledger"]["committed"]["tools"], 7)
        self.assertEqual(result["provider_requests"], 0)
        self.assertIsNone(result["human_disposition"])
        final = get_run(self.store, self.actor, saved["operation_id"])
        self.assertEqual(final["artifacts"]["extractor"]["payload"]["provenance"], "REVIEWER_SOURCE_CORRECTION")
        self.assertEqual(final["events"][1]["event"], "reviewer_correction_applied")
        self.assertIn("1\\.50", result["report_markdown"])
        self.assertIn("Reviewer-corrected extraction", result["report_markdown"])
        self.assertIn("Source correction:", result["report_markdown"])
        from deal_or_no_deal_ai.financial_review import financial_history, financial_history_csv
        from deal_or_no_deal_ai.context import fingerprint
        events = financial_history(self.store, self.actor)
        self.assertEqual([e["action"] for e in events], ["SOURCE_CORRECTION_SAVED", "CORRECTION_APPLIED"])
        raw = financial_history_csv(self.store, self.actor, None, expected_digest=fingerprint("FINANCIAL_HISTORY_SNAPSHOT", events))
        self.assertIn(b"900000", raw)
        self.assertIn(b"corrected_fact", raw)
        self.assertTrue(update_affected_findings(self.root, self.actor, saved["operation_id"], command)["duplicate"])

    def test_exact_value_basis_source_role_scope_and_duplicate_save(self):
        for changes in (dict(value="910000"), dict(basis_id="TXN-1"), dict(evidence_ref="FIN-P1"), dict(comments=" ")):
            with self.assertRaises(InputError):
                save_source_correction(self.root, self.actor, self.operation, self.command(**changes))
        for role in ("RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"):
            with self.assertRaisesRegex(InputError, "ANALYST_EXTRACTION"):
                save_source_correction(self.root, replace(self.actor, persona=role), self.operation, self.command())
        with self.assertRaises(InputError):
            save_source_correction(self.root, replace(self.actor, allowed_deal_ids=frozenset()), self.operation, self.command())
        command = self.command(); saved = self.save()
        self.assertTrue(save_source_correction(self.root, self.actor, self.operation, command)["duplicate"])
        with self.assertRaises(OperationConflict):
            save_source_correction(self.root, self.actor, self.operation, command.model_copy(update={"comments": "Changed"}))
        with self.assertRaises(InputError):
            update_affected_findings(self.root, replace(self.actor, persona="RiskManager"), saved["operation_id"], self.update_command(saved["operation_id"]))

    def test_stale_source_and_tampered_saved_revision_do_not_dispatch(self):
        from copy import deepcopy
        from deal_or_no_deal_ai.storage import RecordWrite
        with self.assertRaises(StaleRecord):
            save_source_correction(self.root, self.actor, self.operation, self.command(expected_version=1))
        saved = self.save(); operation = saved["operation_id"]
        command = self.update_command(operation)
        with self.assertRaises(StaleRecord):
            update_affected_findings(self.root, self.actor, operation, command.model_copy(update={"expected_version": 99}))
        version, event = self.store.get_record("financial-review-event:" + saved["event"]["operation_id"])
        bad = deepcopy(event); bad["corrected_fact"]["value"] = "910000"
        self.store.put_record(RecordWrite("financial-review-event:" + event["operation_id"], "FINANCIAL_REVIEW_EVENT", bad, version))
        with self.assertRaisesRegex(InputError, "BINDING_MISMATCH"):
            update_affected_findings(self.root, self.actor, operation, command)
        self.assertEqual(get_run(self.store, self.actor, operation)["status"], "READY")

    def test_changed_source_blocks_saved_update_without_creating_child_checkpoint(self):
        saved = self.save(); operation = saved["operation_id"]
        command = self.update_command(operation)
        pack = self.root / "fixtures/development/e-n01"
        source = pack / strict_json((pack / "manifest.json").read_bytes())["sources"][0]["path"]
        source.write_bytes(source.read_bytes() + b"changed")
        with self.assertRaises(InputError):
            update_affected_findings(self.root, self.actor, operation, command)
        self.assertEqual(get_run(self.store, self.actor, operation)["status"], "READY")
        self.assertIsNone(self.store.get_record("normal-progress:" + operation))

    def test_concurrent_identical_save_and_update_commit_one_revision(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        command = self.command(); original = Store.admit; barrier = Barrier(2)
        def synchronized(store, operation, *args, **kwargs):
            if operation == command.operation_id:
                barrier.wait(timeout=30)
            return original(store, operation, *args, **kwargs)
        with patch.object(Store, "admit", synchronized), ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(save_source_correction, self.root, self.actor, self.operation, command) for _ in range(2)]
            results = [task.result() for task in tasks]
        self.assertEqual(sum(not r["duplicate"] for r in results), 1)
        operation = results[0]["operation_id"]; update = self.update_command(operation); barrier = Barrier(2)
        def sync_update(store, current, *args, **kwargs):
            if current == operation:
                barrier.wait(timeout=30)
            return original(store, current, *args, **kwargs)
        with patch.object(Store, "admit", sync_update), ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(update_affected_findings, self.root, self.actor, operation, update) for _ in range(2)]
            results = [task.result() for task in tasks]
        self.assertEqual(sum(not r.get("duplicate") for r in results), 1)
        self.assertEqual(get_run(self.store, self.actor, operation)["status"], "COMPLETED")
        self.assertEqual(len([r for r in results if not r.get("duplicate")]), 1)

    def test_ui_save_ready_update_memo_history_and_original_citation(self):
        from tests.integration.test_command_center import CommandCenterTests
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception), 0)
        self.assertFalse(any(b.label == "Update affected findings" for b in app.button))
        next(b for b in app.button if b.label == "↗ FIN-P2").click().run()
        self.assertEqual(widget(app.selectbox, "Evidence reference").value, "FIN-P2")
        widget(app.text_input, "Corrected CFADS (USD whole units)").input("900000")
        widget(app.selectbox, "Correction financial basis").select("FY-ASSESS")
        widget(app.selectbox, "Correction source page").select("FIN-P2")
        widget(app.text_area, "Correction reason (required)").input("Verified CFADS in original source. Restore missed extraction.")
        widget(app.checkbox, "I verified this value in the original cited document").check()
        widget(app.button, "Save source-backed correction").click().run()
        self.assertEqual(len(app.exception), 0)
        operation = app.session_state["selected_financial_operation"]
        self.assertNotEqual(operation, self.operation)
        self.assertEqual(get_run(self.store, self.actor, operation)["status"], "READY")
        widget(app.sidebar.radio, "Page").set_value("Deal Dashboard").run()
        self.assertEqual(len(app.exception), 0)
        widget(app.button, "View latest review").click().run()
        widget(app.button, "Update affected findings").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(get_run(self.store, self.actor, operation)["status"], "COMPLETED")
        widget(app.sidebar.radio, "Page").set_value("Credit Memo").run()
        self.assertTrue(any("Reviewer-corrected extraction" in item.value for item in app.markdown))
        widget(app.sidebar.radio, "Page").set_value("Decision History").run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("SOURCE_CORRECTION_SAVED", widget(app.multiselect, "History actions").options)
