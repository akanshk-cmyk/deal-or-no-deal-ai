"""Scoped TEST-007-05/06/07, TEST-011-02/03/04, using real local SQLite."""

from pathlib import Path
import multiprocessing
import tempfile

from deal_or_no_deal_ai.budgets import Usage
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.storage import OperationConflict, RecordWrite, RunBusy, StaleRecord, Store
from tests.support import OfflineTest, uid


SCOPE = {"workspace_id": uid("workspace"), "deal_id": uid("deal"), "review_id": uid("review")}


def contend(path, name, start, output):
    store = Store(Path(path))
    start.wait(10)
    try:
        receipt = store.admit(uid(name), SCOPE, {"action": "TEST_START", "actor": "SIMULATED"},
            writes=(RecordWrite("disposition:" + name, "TEST_DISPOSITION", {"state": "RECORDED"}),),
            reservation=(name, Usage(nodes=1), "ORDINARY"))
        output.put((name, "HELD", receipt.operation_id))
    except RunBusy:
        output.put((name, "BUSY", None))
    except Exception as exc:
        output.put((name, "ERROR", type(exc).__name__))


class AdmissionTests(OfflineTest):
    def setUp(self):
        super().setUp()
        folder = tempfile.TemporaryDirectory(); self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "shared.sqlite3"
        self.store = Store(self.path); self.store.initialize()

    def test_two_independent_processes_admit_exactly_one(self):
        context = multiprocessing.get_context("spawn")
        start = context.Event(); output = context.Queue()
        children = [context.Process(target=contend, args=(str(self.path), name, start, output))
                    for name in ("one", "two")]
        try:
            for child in children: child.start()
            start.set()
            results = [output.get(timeout=20), output.get(timeout=20)]
            self.assertEqual(sorted(item[1] for item in results), ["BUSY", "HELD"])
            winner = next(item[0] for item in results if item[1] == "HELD")
            loser = next(item[0] for item in results if item[1] == "BUSY")
            self.assertIsNotNone(self.store.get_record("disposition:" + winner))
            self.assertIsNone(self.store.get_record("disposition:" + loser))
            _, ledger = self.store.get_record("ledger:" + SCOPE["review_id"])
            self.assertEqual(set(ledger["reservations"]), {winner})
        finally:
            for child in children:
                child.join(timeout=5)
                if child.is_alive(): child.terminate(); child.join(timeout=5)
            output.close(); output.join_thread()
        for child in children: self.assertEqual(child.exitcode, 0)

    def test_duplicate_receipt_does_not_reacquire_or_rewrite(self):
        writes = (RecordWrite("disposition", "TEST_DISPOSITION", {"outcome": "Reject"}),)
        first = self.store.admit(uid("operation"), SCOPE, {"action": "TEST_RESUME"}, writes=writes)
        self.store.release(first, confirmed_idle=True)
        duplicate = self.store.admit(uid("operation"), SCOPE, {"action": "TEST_RESUME"}, writes=writes)
        self.assertTrue(duplicate.duplicate)
        self.assertEqual(duplicate.state, "RELEASED")
        self.assertEqual(self.store.get_record("disposition")[0], 1)
        with self.assertRaises(OperationConflict):
            self.store.admit(uid("operation"), SCOPE, {"action": "DIFFERENT"}, writes=writes)
        with self.assertRaises(InputError): self.store.assert_claim(duplicate)

    def test_unknown_claim_is_retained_until_explicit_recovery(self):
        receipt = self.store.admit(uid("operation"), SCOPE, {"action": "TEST_START"})
        self.store.mark_unknown(receipt)
        restarted = Store(self.path); restarted.initialize()
        with self.assertRaises(RunBusy):
            restarted.admit(uid("other"), SCOPE, {"action": "TEST_START"})
        with self.assertRaises(InputError): restarted.release(receipt, confirmed_idle=True)
        with self.assertRaises(InputError):
            restarted.reconcile_idle(receipt, evidence_ref="", administrator_authorized=True)
        restarted.reconcile_idle(receipt, evidence_ref="test:confirmed-no-work", administrator_authorized=True)
        self.assertEqual(restarted.admit(uid("other"), SCOPE, {"action": "TEST_START"}).state, "HELD")

    def test_duplicate_held_receipt_cannot_dispatch_again(self):
        original = self.store.admit(uid("operation"), SCOPE, {"action": "TEST_START"})
        duplicate = self.store.admit(uid("operation"), SCOPE, {"action": "TEST_START"})
        self.store.assert_claim(original)
        with self.assertRaisesRegex(InputError, "READ_ONLY"):
            self.store.assert_claim(duplicate)

    def test_stale_write_rolls_back_acceptance_and_claim(self):
        self.store.put_record(RecordWrite("request", "TEST_REQUEST", {"state": "PENDING"}))
        with self.assertRaises(StaleRecord):
            self.store.admit(uid("bad"), SCOPE, {"action": "TEST_RESUME"},
                writes=(RecordWrite("disposition", "TEST_DISPOSITION", {"decision": "Approve"}),
                        RecordWrite("request", "TEST_REQUEST", {"state": "RECORDED"}, 0)))
        self.assertIsNone(self.store.get_record("disposition"))
        self.assertEqual(self.store.get_record("request")[1]["state"], "PENDING")
        self.assertEqual(self.store.admit(uid("good"), SCOPE, {"action": "TEST_START"}).state, "HELD")

    def test_pause_releases_slot_without_renewing_review_allowance(self):
        first = self.store.admit(uid("first"), SCOPE, {"action": "TEST_START"}, reservation=("node", Usage(nodes=1), "ORDINARY"))
        self.store.release(first, confirmed_idle=True)
        self.store.admit(uid("resume"), SCOPE, {"action": "TEST_RESUME"}, reservation=("resume-node", Usage(nodes=1), "ORDINARY"))
        _, saved = self.store.get_record("ledger:" + SCOPE["review_id"])
        self.assertEqual(sum(value["nodes"] for value in saved["reservations"].values()), 2)

    def test_wrong_database_version_is_not_migrated(self):
        with self.store.transaction() as connection:
            connection.execute("UPDATE app_meta SET value='unsupported' WHERE key='schema'")
        with self.assertRaisesRegex(InputError, "INCOMPATIBLE_DATABASE"):
            Store(self.path).initialize()

    def test_metadata_update_retains_every_prior_version(self):
        self.store.put_record(RecordWrite("request", "TEST_REQUEST", {"state": "PENDING"}))
        self.store.put_record(RecordWrite("request", "TEST_REQUEST", {"state": "RECORDED"}, 1))
        with self.store.connection() as connection:
            rows = connection.execute("SELECT version,payload FROM app_record_history WHERE record_key=? ORDER BY version", ("request",)).fetchall()
        self.assertEqual([row["version"] for row in rows], [1, 2])
        self.assertIn("PENDING", rows[0]["payload"])
        self.assertIn("RECORDED", rows[1]["payload"])

    def test_unknown_claim_and_budget_reservation_are_marked_atomically(self):
        receipt = self.store.admit(uid("request"), SCOPE, {"action": "TEST_PROVIDER_BOUNDARY"},
            reservation=("provider-request", Usage(attempts=1, input_tokens=1000), "ORDINARY"))
        self.store.mark_unknown(receipt)
        _, saved = Store(self.path).get_record("ledger:" + SCOPE["review_id"])
        self.assertEqual(saved["unknown"], ["provider-request"])
        self.assertEqual(saved["reservations"]["provider-request"]["input_tokens"], 1000)
