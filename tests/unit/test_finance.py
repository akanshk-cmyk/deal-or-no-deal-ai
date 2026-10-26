"""FIN-1.0 kernel parts of TEST-003-01/02/03/05/06/07, not source support."""

from decimal import Decimal, Inexact, localcontext
import json

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.finance import calculate_metrics, compare_threshold
from tests.support import OfflineTest, ROOT


PACK = ROOT / "fixtures/development/e-n01"


def financial_values():
    wire = json.loads((PACK / "extraction.candidate.json").read_text(encoding="utf-8"))
    return {k: v["value"] for k, v in wire["financial_inputs"].items()}


class FinancialKernelTests(OfflineTest):
    def test_nine_metrics_match_independent_authored_gold(self):
        gold = json.loads((PACK / "gold.json").read_text(encoding="utf-8"))["metrics"]
        actual = calculate_metrics(financial_values(), secured_equipment=True)
        self.assertEqual(set(actual), set(gold))
        for key, expected in gold.items():
            with self.subTest(metric=key):
                self.assertEqual(actual[key].validity, "VALID")
                self.assertEqual(actual[key].value, Decimal(expected["value"]))
                self.assertEqual(actual[key].display, expected["display"])
                self.assertEqual(actual[key].unit, expected["unit"])
                self.assertEqual(actual[key].reason, "ARITHMETIC_ONLY")

    def test_missing_is_not_zero_and_only_dependent_metrics_are_withheld(self):
        values = financial_values() | {"cash_available_for_debt_service": None}
        actual = calculate_metrics(values, secured_equipment=True)
        self.assertEqual(actual["CALC-004"].validity, "UNKNOWN")
        self.assertIsNone(actual["CALC-004"].value)
        self.assertEqual(actual["CALC-005"].value, Decimal(3))
        no_liens = calculate_metrics(financial_values() | {"prior_ranking_liens": None}, secured_equipment=True)
        self.assertEqual(no_liens["CALC-006"].validity, "UNKNOWN")
        self.assertEqual(calculate_metrics(financial_values(), secured_equipment=True)["CALC-006"].value, Decimal(60))

    def test_zero_and_nonpositive_denominators_are_not_passing_ratios(self):
        changes = (
            ({"annual_principal_payments": "0", "annual_interest_payments": "0"}, "CALC-004"),
            ({"net_income": "-400000"}, "CALC-005"),
            ({"net_income": "-500000"}, "CALC-005"),
            ({"eligible_equipment_value": "0"}, "CALC-006"),
            ({"previous_revenue": "0"}, "CALC-007"),
            ({"current_liabilities": "0"}, "CALC-008"),
            ({"interest_expense": "0"}, "CALC-009"),
        )
        for change, key in changes:
            with self.subTest(change=change):
                result = calculate_metrics(financial_values() | change, secured_equipment=True)[key]
                self.assertEqual(result.validity, "NOT_MEANINGFUL")
                self.assertIsNone(result.value)
                with self.assertRaises(InputError):
                    compare_threshold(result, operator="GT", threshold="4")

    def test_negative_supported_cash_and_ebit_remain_meaningful(self):
        values = financial_values() | {"cash_available_for_debt_service": "-300000", "net_income": "-300000"}
        actual = calculate_metrics(values, secured_equipment=True)
        self.assertEqual(actual["CALC-004"].value, Decimal("-0.5"))
        self.assertEqual(actual["CALC-001"].value, Decimal("-100000"))
        self.assertEqual(actual["CALC-009"].value, Decimal("-1"))

    def test_sign_errors_and_unreconciled_debt_repayment_are_explicit(self):
        for field, key in (("existing_funded_debt", "CALC-003"), ("annual_principal_payments", "CALC-004"),
                           ("prior_ranking_liens", "CALC-006"), ("current_assets", "CALC-008")):
            with self.subTest(field=field):
                result = calculate_metrics(financial_values() | {field: "-1"}, secured_equipment=True)[key]
                self.assertEqual(result.validity, "INVALID")
        too_much = calculate_metrics(financial_values() | {"transaction_debt_repaid": "3600000.000001"}, secured_equipment=True)
        self.assertEqual(too_much["CALC-003"].reason, "UNRECONCILED_DEBT_REPAYMENT")
        self.assertEqual(too_much["CALC-005"].validity, "INVALID")

    def test_liens_and_transaction_repayment_are_counted_once(self):
        results = calculate_metrics(financial_values() | {"prior_ranking_liens": "100000"}, secured_equipment=True)
        self.assertEqual(results["CALC-003"].value, Decimal("3300000"))
        self.assertEqual(results["CALC-006"].numerator, Decimal("1300000"))
        self.assertEqual(results["CALC-006"].value, Decimal(65))

    def test_dscr_and_ltv_thresholds_use_exact_operands_not_rounded_display(self):
        for cash, breached in (("749999.999999", True), ("750000", False), ("750000.000001", False)):
            with self.subTest(cash=cash):
                result = calculate_metrics(financial_values() | {"cash_available_for_debt_service": cash}, secured_equipment=True)["CALC-004"]
                self.assertEqual(result.display, "1.25")
                self.assertEqual(compare_threshold(result, operator="LT", threshold="1.25"), breached)
        for exposure, breached in (("1600000", False), ("1600000.000001", True)):
            with self.subTest(exposure=exposure):
                result = calculate_metrics(financial_values() | {"secured_facility_exposure": exposure}, secured_equipment=True)["CALC-006"]
                self.assertEqual(result.display, "80.00")
                self.assertEqual(compare_threshold(result, operator="GT", threshold="80"), breached)

    def test_repeating_division_and_maximum_input_precision_ignore_host_context(self):
        with localcontext() as host:
            host.prec = 2
            host.traps[Inexact] = True
            result = calculate_metrics(financial_values() | {"cash_available_for_debt_service": "1",
                "annual_principal_payments": "3", "annual_interest_payments": "0"}, secured_equipment=True)["CALC-004"]
            self.assertEqual(result.validity, "VALID")
            self.assertEqual(result.display, "0.33")
            self.assertTrue(compare_threshold(result, operator="GT", threshold="0.333333"))
            values = financial_values() | {k: "999999999999999999.999999" for k in (
                "net_income", "interest_expense", "income_tax_expense", "depreciation", "amortization")}
            maximum = calculate_metrics(values, secured_equipment=True)["CALC-002"]
            self.assertEqual(maximum.value, Decimal("4999999999999999999.999995"))

    def test_profile_rejects_coercion_and_does_not_invent_inapplicable_ltv(self):
        for invalid in (True, 1.5, "1e3", "1,000", "1.00", "NaN"):
            with self.subTest(invalid=invalid), self.assertRaises(InputError):
                calculate_metrics(financial_values() | {"net_income": invalid}, secured_equipment=True)
        values = financial_values()
        del values["prior_ranking_liens"]
        with self.assertRaises(InputError):
            calculate_metrics(values, secured_equipment=True)
        result = calculate_metrics(financial_values(), secured_equipment=False)["CALC-006"]
        self.assertEqual(result.reason, "EQUIPMENT_NOT_APPLICABLE")
        self.assertIsNone(result.value)
