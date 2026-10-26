"""Scoped TEST-007-03/06/08, TEST-006-08; no actual provider work."""

from decimal import Decimal

from deal_or_no_deal_ai.budgets import BudgetExceeded, Ledger, LIMIT, Usage
from deal_or_no_deal_ai.context import InputError
from tests.support import OfflineTest, uid


class BudgetTests(OfflineTest):
    def test_equality_passes_and_each_ceiling_overrun_fails(self):
        ledger = Ledger(uid("review"), committed=LIMIT)
        self.assertEqual(ledger.total, LIMIT)
        for counter in ("input_tokens", "output_tokens", "attempts", "nodes", "tools", "active_ms", "cost_usd"):
            extra = Decimal("0.000001") if counter == "cost_usd" else 1
            with self.subTest(counter=counter), self.assertRaises(BudgetExceeded):
                ledger.reserve(uid(counter), Usage(**{counter: extra}))

    def test_reservations_and_actuals_are_counted_once(self):
        maximum = Usage(input_tokens=3000, output_tokens=1000, attempts=1, active_ms=45000, cost_usd=Decimal("0.10"))
        ledger = Ledger(uid("review")).reserve("extract", maximum)
        self.assertEqual(ledger.reserve("extract", maximum), ledger)
        actual = Usage(input_tokens=2800, output_tokens=700, attempts=1, active_ms=2000, cost_usd=Decimal("0.01"))
        ledger = ledger.settle("extract", actual)
        self.assertEqual(ledger.total, actual)
        self.assertEqual(ledger.settle("extract", actual), ledger)
        self.assertEqual(Ledger.from_dict(ledger.to_dict()), ledger)
        broken = ledger.to_dict()
        broken["committed"]["attempts"] = 0
        with self.assertRaisesRegex(InputError, "EXCEEDS_COMMITTED"):
            Ledger.from_dict(broken)
        broken = actual.to_dict(); broken["cost_usd"] = "0.010"
        with self.assertRaisesRegex(InputError, "NONCANONICAL"):
            Usage.from_dict(broken)

    def test_unknown_reservation_survives_restart_and_needs_reconciliation(self):
        maximum = Usage(attempts=1, input_tokens=3000, output_tokens=1000, cost_usd=Decimal("0.1"))
        ledger = Ledger(uid("review")).reserve("request", maximum).mark_unknown("request")
        restored = Ledger.from_dict(ledger.to_dict())
        self.assertEqual(restored.total, maximum)
        with self.assertRaisesRegex(InputError, "RECONCILIATION_REQUIRED"):
            restored.settle("request", maximum)
        self.assertEqual(restored.settle("request", maximum, reconciled=True).total, maximum)

    def test_correction_reserve_is_protected_and_cumulative(self):
        ledger = Ledger(uid("review"), committed=Usage(input_tokens=4500, output_tokens=1350, attempts=2))
        with self.assertRaises(BudgetExceeded):
            ledger.reserve("optional", Usage(output_tokens=301), purpose="OPTIONAL_REPAIR")
        ledger = ledger.reserve("correction", Usage(input_tokens=1500, output_tokens=350, attempts=1), purpose="SYNTHESIS_CORRECTION")
        self.assertEqual(ledger.total.input_tokens, 6000)
        self.assertEqual(ledger.total.output_tokens, 1700)
        ledger = Ledger.from_dict(ledger.to_dict())
        with self.assertRaises(BudgetExceeded):
            ledger.reserve("another", Usage(), purpose="SYNTHESIS_CORRECTION")

    def test_reviewed_original_plus_correction_has_no_node_headroom(self):
        ledger = Ledger(uid("review"), committed=Usage(nodes=11, tools=4, attempts=2))
        estimate = ledger.require_path("FINANCIAL_CORRECTION_REVIEWED")
        self.assertEqual(estimate.nodes, 9)
        self.assertEqual(ledger.committed.nodes, 11)  # Preview is not a reservation.
        with self.assertRaises(BudgetExceeded):
            Ledger(uid("review"), committed=Usage(nodes=12)).require_path("FINANCIAL_CORRECTION_REVIEWED")
        self.assertEqual(Ledger(uid("review")).require_path("INITIAL_REVIEWED", fixture=True).attempts, 0)

    def test_timeout_uses_remaining_active_allowance(self):
        self.assertEqual(Ledger(uid("review")).operation_timeout_ms(), 45000)
        self.assertEqual(Ledger(uid("review"), committed=Usage(active_ms=170000)).operation_timeout_ms(), 10000)
        with self.assertRaises(BudgetExceeded):
            Ledger(uid("review"), committed=Usage(active_ms=180000)).operation_timeout_ms()
        with self.assertRaises(InputError):
            Usage(attempts=True)
