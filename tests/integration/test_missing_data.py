"""Source-backed E-M01 information pause through actual graph and Streamlit."""
from dataclasses import replace
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.command_center import get_run, list_runs, source_packet, start_run, workspace_id
from deal_or_no_deal_ai.context import InputError, strict_json
from deal_or_no_deal_ai.graph import STAGES
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store
from deal_or_no_deal_ai.synthesis import prepare_synthesis, synthesis_task
from deal_or_no_deal_ai.services import load_registered_case
from tests.integration.test_human_review_ui import widget
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import OfflineTest, ROOT, uid


class MissingDataTests(OfflineTest):
    def setUp(self):
        super().setUp()
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        copy_workspace(self.root)
        shutil.copytree(ROOT / "fixtures/development/e-m01", self.root / "fixtures/development/e-m01")
        self.store = Store(self.root / "var/deal_review.sqlite3")
        self.deal = strict_json((self.root / "config/registrations/e-m01.json").read_bytes())["deal_id"]
        normal = strict_json((self.root / "config/registrations/e-n01.json").read_bytes())["deal_id"]
        self.actor = Actor("Analyst", workspace_id(self.root), frozenset({self.deal, normal}))
        self.operation = uid("e-m01-graph")

    def test_graph_stops_before_synthesis_with_saved_partial_evidence_and_no_replay(self):
        with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=AssertionError("NO_SYNTHESIS")), patch("deal_or_no_deal_ai.worker.render_memo", side_effect=AssertionError("NO_MEMO")):
            outcome = start_run(self.root, self.actor, self.operation, scenario_id="E-M01")
        self.assertEqual(outcome["status"], "WAITING_INFORMATION")
        self.assertEqual(outcome["stages"], list(STAGES[:5]))
        self.assertIsNone(outcome["report_markdown"])
        self.assertIsNone(outcome["human_disposition"])
        self.assertEqual(outcome["provider_requests"], 0)
        self.assertEqual(outcome["ledger"]["committed"]["nodes"], 5)
        self.assertIn("financial_input:cash_available_for_debt_service", outcome["missing_items"])
        run = get_run(self.store, self.actor, self.operation)
        score = run["artifacts"]["risk_quantifier"]["payload"]["score"]
        self.assertIsNone(score["total"])
        self.assertIsNone(score["band"])
        packet = source_packet(self.root, run)
        self.assertIn("E-M01:FIN-P2", packet["request"]["reference_dictionary"])
        self.assertNotIn("FIN-P2", packet["request"]["reference_dictionary"])
        self.assertEqual(next(m for m in packet["request"]["financial"]["metrics"] if m["metric_id"] == "CALC-004")["validity"], "UNKNOWN")
        case = load_registered_case(self.root, scenario_id="E-M01")
        with self.assertRaisesRegex(InputError, "PREREQUISITES_INCOMPLETE"):
            prepare_synthesis(case)
        with self.assertRaises(InputError):
            synthesis_task(self.root, case, packet)
        before = self.store.path.read_bytes()
        with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_REPLAY")):
            duplicate = start_run(self.root, self.actor, self.operation, scenario_id="E-M01")
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(duplicate["status"], "WAITING_INFORMATION")
        self.assertEqual(self.store.path.read_bytes(), before)
        with self.assertRaisesRegex(InputError, "EXISTING_OPERATION_VARIANT_CHANGED"):
            start_run(self.root, self.actor, self.operation, scenario_id="E-N01")
        excluded = replace(self.actor, allowed_deal_ids=frozenset())
        self.assertEqual(list_runs(self.store, excluded), [])
        with self.assertRaises(InputError):
            get_run(self.store, excluded, self.operation)

    def test_non_analyst_denied_before_database_and_changed_sources_denied(self):
        for role in ("RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"):
            with self.assertRaisesRegex(InputError, "START_NOT_PERMITTED"):
                start_run(self.root, replace(self.actor, persona=role), self.operation, scenario_id="E-M01")
        self.assertFalse(self.store.path.exists())
        source = self.root / "fixtures/development/e-m01/financials.pdf"
        source.write_bytes(source.read_bytes() + b"changed")
        with self.assertRaisesRegex(InputError, "SOURCE_CHANGED"):
            load_registered_case(self.root, scenario_id="E-M01")

    def test_distinct_normal_and_missing_deals_keep_sources_and_counts_separate(self):
        from deal_or_no_deal_ai.ui.dashboard import project_deals
        start_run(self.root, self.actor, uid("normal-beside-missing"))
        start_run(self.root, self.actor, self.operation, scenario_id="E-M01")
        rows = project_deals(list_runs(self.store, self.actor))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["run"]["context"]["scenario_id"], "E-M01")
        self.assertEqual(rows[0]["decision"], "Pending Information")
        self.assertIn("Analyst", rows[0]["owner"])
        only_normal = replace(self.actor, allowed_deal_ids=frozenset({rows[1]["deal_id"]}))
        self.assertEqual(len(list_runs(self.store, only_normal)), 1)

    def test_streamlit_missing_sample_sources_and_blocked_final_decisions(self):
        from tests.integration.test_command_center import CommandCenterTests
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.selectbox, "Sample scenario").select("missing").run()
        widget(app.button, "Run AI Deal Review").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Waiting for additional information" in w.value for w in app.warning))
        widget(app.button, "Open review workspace").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 0)
        self.assertEqual(widget(app.metric, "Credit risk · illustrative").value, "Not computed")
        self.assertIn("Missing Information:FIN-P2", widget(app.selectbox, "Evidence reference").options)
        for role in ("Analyst", "AuthorizedApprover"):
            widget(app.sidebar.selectbox, "Demo role").select(role).run()
            self.assertTrue(widget(app.button, "Approve").disabled)
            self.assertTrue(widget(app.button, "Reject").disabled)
        widget(app.sidebar.radio, "Page").set_value("Credit Memo").run()
        self.assertTrue(any("No completed memo" in item.value for item in app.info))
        widget(app.sidebar.radio, "Page").set_value("Deal Dashboard").run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(widget(app.metric, "Pending Information").value, "1")
        self.assertTrue(any("Analyst" in item.value and "CFADS" in item.value for item in app.info))
