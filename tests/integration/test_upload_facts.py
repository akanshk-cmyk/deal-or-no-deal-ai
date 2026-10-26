"""Actual source-bound candidate/support and existing DSCR, without deal admission."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from copy import deepcopy

from deal_or_no_deal_ai.command_center import workspace_id, list_runs
from deal_or_no_deal_ai.context import InputError, strict_json
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store, StaleRecord, OperationConflict
from deal_or_no_deal_ai.upload_intake import inspect_package
from deal_or_no_deal_ai.upload_facts import (FIELDS, CHECKS, ProposalCommand, SupportCommand,
    get_fact_review, record_fact_action, dscr_preview)
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import widget
from tests.support import OfflineTest, uid


class UploadFactTests(OfflineTest):
    def setUp(self):
        super().setUp()
        temp = TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); copy_workspace(self.root)
        self.actor = Actor("Analyst", workspace_id(self.root), frozenset())
        self.operation = uid("fact-upload")
        pack = self.root / "fixtures/development/e-n01"
        manifest = strict_json((pack / "manifest.json").read_bytes())
        raw = (pack / next(s["path"] for s in manifest["sources"] if s["source_id"] == "FINANCIALS-1")).read_bytes()
        self.package = inspect_package(self.root, self.actor, self.operation, [("financials.pdf", raw)], synthetic_confirmed=True)
        self.page = self.package["sources"][0]["pages"][1]

    def panel(self):
        return get_fact_review(self.root, self.actor, self.operation)

    def proposal(self, field=FIELDS[0], **changes):
        labels = dict(zip(FIELDS, ("Cash available for debt service:", "Annual principal payments:", "Annual interest payments:")))
        quote = next(line for line in self.page["text"].splitlines() if labels[field] in line)
        values = dict(operation_id=uid(field + str(self.panel()["version"])), expected_version=self.panel()["version"], field=field,
            source_ref=self.page["ref"], quote=quote, quote_start=self.page["text"].find(quote), raw_number=quote.split()[-1],
            raw_label=labels[field], unit_label="USD whole units", scale="1", currency="USD", subject="Example Equipment LLC",
            facility="E-N01-FACILITY", period_start="2027-01-01", period_end="2027-12-31", basis_kind="ANNUAL_PROJECTION", comments="Proposed from exact supplied annual schedule.")
        values.update(changes)
        return ProposalCommand(**values)

    def propose(self, field=FIELDS[0], **changes):
        return record_fact_action(self.root, self.actor, self.operation, self.proposal(field, **changes))

    def support_command(self, field=FIELDS[0], **changes):
        panel = self.panel(); proposal = panel["latest"][field]
        values = dict(operation_id=uid("support:" + field + str(panel["version"])), expected_version=panel["version"],
            proposal_id=proposal["operation_id"], target_digest=proposal["content"]["target_digest"], status="HUMAN_SUPPORTED",
            checks=list(CHECKS), comments="Verified row, units, annual projection, borrower, facility and complete debt service scope.")
        values.update(changes)
        return SupportCommand(**values)

    def support(self, field=FIELDS[0], **changes):
        return record_fact_action(self.root, replace(self.actor, persona="RiskManager"), self.operation, self.support_command(field, **changes))

    def test_supported_three_fact_preview_and_replacement_invalidates_old_support(self):
        self.assertIsNone(dscr_preview(self.panel())["display"])
        for field in FIELDS:
            self.propose(field)
            self.assertIsNone(dscr_preview(self.panel())["display"])
            self.support(field)
        result = dscr_preview(self.panel())
        self.assertEqual(result["display"], "1.50")
        self.assertEqual(result["definition"], "FIN-1.0")
        self.assertFalse(list_runs(Store(self.root / "var/deal_review.sqlite3"), self.actor))
        self.propose(comments="New exact proposal requires fresh support.")
        self.assertIsNone(dscr_preview(self.panel())["display"])
        self.assertEqual(len(self.panel()["events"]), 7)

    def test_wrong_role_scope_quote_token_unit_stale_and_duplicate(self):
        command = self.proposal()
        for role in ("RiskManager", "AuthorizedApprover", "ComplianceOfficer", "Administrator"):
            with self.assertRaises(InputError):
                record_fact_action(self.root, replace(self.actor, persona=role), self.operation, command)
        for changes in (dict(quote="Invented"), dict(raw_number="90"), dict(unit_label="USD millions"), dict(quote_start=0), dict(period_end="2027-05-31")):
            with self.assertRaises((InputError, ValueError)):
                self.propose(**changes)
        self.propose()
        self.assertEqual(record_fact_action(self.root, self.actor, self.operation, command)["operation_id"], command.operation_id)
        with self.assertRaises(OperationConflict):
            record_fact_action(self.root, self.actor, self.operation, command.model_copy(update={"comments": "Changed"}))
        support = self.support_command()
        with self.assertRaises(InputError):
            self.support(checks=["reference"])
        with self.assertRaises(InputError):
            record_fact_action(self.root, self.actor, self.operation, support)
        self.propose(FIELDS[1])
        with self.assertRaises(StaleRecord):
            record_fact_action(self.root, replace(self.actor, persona="RiskManager"), self.operation, support)

    def test_withheld_and_incompatible_basis_keep_preview_unknown(self):
        for field in FIELDS:
            self.propose(field, subject="Other borrower" if field == FIELDS[2] else "Example Equipment LLC")
            self.support(field)
        self.assertIsNone(dscr_preview(self.panel())["display"])
        self.assertIn("does not match", dscr_preview(self.panel())["blockers"][0])
        self.propose(FIELDS[2])
        self.support(FIELDS[2], status="WITHHELD", checks=[], comments="Debt-scope meaning not established.")
        self.assertIsNone(dscr_preview(self.panel())["display"])

    def test_exact_target_source_change_and_concurrent_duplicate_support(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        self.propose()
        with self.assertRaises(InputError):
            self.support(target_digest="0" * 64)
        command = self.support_command(); barrier = Barrier(2); original = Store.admit
        def synchronized(store, operation, *args, **kwargs):
            if operation == command.operation_id:
                barrier.wait(timeout=30)
            return original(store, operation, *args, **kwargs)
        manager = replace(self.actor, persona="RiskManager")
        with patch.object(Store, "admit", synchronized), ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(record_fact_action, self.root, manager, self.operation, command) for _ in range(2)]
            results = [t.result() for t in tasks]
        self.assertEqual(results[0], results[1])
        self.assertEqual(len(self.panel()["events"]), 2)
        source = self.package["sources"][0]
        path = self.root / "var/uploads" / self.actor.workspace_id / self.package["package_id"] / (source["sha256"] + ".pdf")
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaisesRegex(InputError, "SOURCE_CHANGED"):
            self.panel()

    def test_ui_manual_proposal_support_and_citation_handoff(self):
        from tests.integration.test_command_center import CommandCenterTests
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.radio, "Intake mode").set_value("Upload New Deal").run()
        widget(app.selectbox, "Uploaded source page").select(2).run()
        command = self.proposal()
        for label, value in (("Field label as printed in quote", command.raw_label), ("Number exactly as printed (plain decimal)", command.raw_number),
            ("Unit label as printed on this page", command.unit_label), ("Borrower or business name", command.subject),
            ("Loan or debt covered by these figures", command.facility), ("Annual period start (YYYY-MM-DD)", command.period_start), ("Annual period end (YYYY-MM-DD)", command.period_end)):
            widget(app.text_input, label).input(value)
        widget(app.text_area, "Exact source quote").input(command.quote)
        widget(app.text_area, "Reason for this proposed value").input(command.comments)
        widget(app.selectbox, "How amounts are reported").select("1")
        widget(app.selectbox, "Type of annual figures").select("ANNUAL_PROJECTION")
        widget(app.button, "Save value and supporting source").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn(FIELDS[0], self.panel()["latest"])
        widget(app.sidebar.selectbox, "Demo role").select("RiskManager").run()
        widget(app.button, "Open candidate source page").click().run()
        self.assertEqual(widget(app.selectbox, "Uploaded source page").value, 2)
        widget(app.selectbox, "Evidence assessment").select("HUMAN_SUPPORTED")
        widget(app.multiselect, "Verified evidence checks").set_value(list(CHECKS))
        widget(app.text_area, "Evidence review reason").input("Reviewed original source and all semantic checks.")
        widget(app.button, "Record evidence assessment").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.panel()["supports"][FIELDS[0]]["command"]["status"], "HUMAN_SUPPORTED")
