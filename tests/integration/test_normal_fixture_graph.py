"""Actual nine-stage normal graph/checkpoints, not Live or other-case readiness."""

from pathlib import Path
from contextlib import closing
import shutil
import sqlite3
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.contracts import parse_synthesis
from deal_or_no_deal_ai.graph import STAGES, build_graph
from deal_or_no_deal_ai.storage import Store, RunBusy
from deal_or_no_deal_ai.worker import run_normal_fixture
from tests.support import OfflineTest, ROOT, uid


def copy_workspace(destination):
    for name in ("config", "fixtures/development/e-n01", "docs/agents"):
        shutil.copytree(ROOT / name, destination / name)
    # Functional fixture tests are isolated from the local presenter's LIVE
    # selection, just as their provider-verification profile is isolated below.
    app=destination/"config/app.toml"
    app.write_text(app.read_text(encoding="utf-8").replace('mode = "LIVE"','mode = "FIXTURE"'),encoding="utf-8")
    app.write_text(app.read_text(encoding="utf-8").replace('live_verification_policy = "DEMO_DRAFT"','live_verification_policy = "HUMAN_REQUIRED"'),encoding="utf-8")
    # Live verification belongs to the developer's local workspace, never the
    # copied offline test setup. Test cases explicitly enable their mocked profile.
    profile=destination/"config/live_smoke.toml"
    text=profile.read_text(encoding="utf-8").partition("[verified_packet_tokens]")[0]
    dynamic={"token_count_strategy","input_usd_per_million","output_usd_per_million","rates_verified_on"}
    text="\n".join(line for line in text.splitlines() if line.partition("=")[0].strip() not in dynamic)
    profile.write_text(text.replace("provider_contract_verified = true","provider_contract_verified = false")+"\n",encoding="utf-8")


class NormalFixtureGraphTests(OfflineTest):
    def test_enabled_hosted_tracing_is_rejected_before_any_workspace_or_execution_work(self):
        for key in ("LANGSMITH_TRACING", "LANGCHAIN_TRACING_V2", "LANGCHAIN_TRACING"):
            with self.subTest(key=key), patch.dict("os.environ", {key: "true"}), \
                    patch("deal_or_no_deal_ai.worker.load_configuration", side_effect=AssertionError("NO_WORKSPACE_WORK")), \
                    self.assertRaisesRegex(InputError, "TRACING_MUST_BE_DISABLED"):
                run_normal_fixture(ROOT, uid("tracing-denied"))

    def test_actual_normal_graph_memo_checkpoint_and_duplicate_read(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            operation = uid("executed-normal")
            result = run_normal_fixture(root, operation, generation_time="2026-10-24T05:00:00+00:00")
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["stages"], list(STAGES))
            self.assertEqual(result["ledger"]["committed"]["nodes"], 9)
            self.assertEqual(result["ledger"]["committed"]["tools"], 4)
            self.assertEqual(result["ledger"]["committed"]["attempts"], 0)
            self.assertEqual(result["ledger"]["committed"]["input_tokens"], 0)
            self.assertEqual(result["ledger"]["reservations"], {})
            self.assertEqual(len(result["audit_events"]), 18)
            self.assertEqual(result["report_metadata"]["audit_cutoff_sequence"], 17)
            self.assertIsNone(result["human_disposition"])
            self.assertIsNone(result["actual_model_cost_usd"])
            store = Store(root / "var/deal_review.sqlite3")
            saved = store.get_record("normal-progress:" + operation)[1]
            wire = parse_synthesis(saved["artifacts"]["synthesizer"]["payload"]["wire_json"])
            self.assertEqual(str(wire.panel_decision.confidence), "0.85")
            from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
            from langgraph.checkpoint.sqlite import SqliteSaver
            with closing(sqlite3.connect(store.path, check_same_thread=False)) as connection:
                saver = SqliteSaver(connection, serde=JsonPlusSerializer(pickle_fallback=False,
                                 allowed_json_modules=None, allowed_msgpack_modules=None))
                graph = build_graph({name: lambda state: state for name in STAGES}, checkpointer=saver)
                checkpoint = graph.get_state({"configurable": {"thread_id": result["scope"]["thread_id"]}})
                self.assertEqual(checkpoint.next, ())
                self.assertEqual(checkpoint.values["report_metadata"], result["report_metadata"])
            with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_REPLAY")):
                duplicate = run_normal_fixture(root, operation)
            self.assertTrue(duplicate["duplicate"])
            self.assertEqual(duplicate["report_markdown"], result["report_markdown"])
            self.assertEqual(duplicate["ledger"], result["ledger"])

    def test_shared_busy_claim_blocks_fixture_before_stage_dispatch(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            store = Store(root / "var/deal_review.sqlite3"); store.initialize()
            active = store.admit(uid("other-active"), {"review_id": uid("other-review")}, {"action": "TEST_ACTIVE"})
            with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_DISPATCH")), self.assertRaises(RunBusy):
                run_normal_fixture(root, uid("busy-normal"))
            store.release(active, confirmed_idle=True)

    def test_failure_retains_claim_and_reserved_usage_without_auto_replay(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            operation = uid("failed-normal")
            with patch("deal_or_no_deal_ai.worker.validate_fixture_synthesis", side_effect=InputError("CONTROLLED_LOCAL_FAULT")), \
                    self.assertRaisesRegex(InputError, "CONTROLLED_LOCAL_FAULT"):
                run_normal_fixture(root, operation)
            with patch("deal_or_no_deal_ai.worker.build_graph", side_effect=AssertionError("NO_AUTO_RECOVERY")):
                duplicate = run_normal_fixture(root, operation)
            self.assertEqual(duplicate["status"], "RECOVERY_REQUIRED")
            store = Store(root / "var/deal_review.sqlite3")
            with self.assertRaises(RunBusy):
                store.admit(uid("new-while-uncertain"), {"review_id": uid("another")}, {"action": "TEST_NEW"})
            saved = store.get_record("normal-progress:" + operation)[1]
            ledger = store.get_record("ledger:" + saved["context"]["scope"]["review_id"])[1]
            self.assertTrue(ledger["reservations"])
