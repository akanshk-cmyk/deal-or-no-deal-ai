"""Approved case arithmetic only; these are NOT source-registered graph walks."""

from decimal import Decimal

import pytest

from deal_or_no_deal_ai.risk import assess_risk
from tests.panel_support import policy_inputs, SCOPE


@pytest.mark.parametrize("scenario,changes,expected_dscr,expected_flags", [
    ("E-P01", {"cash_available_for_debt_service": "690000"}, "1.15", {"SYN-ESC-001"}),
    ("E-M01", {"cash_available_for_debt_service": None}, None, set()),
    ("E-F03", {"net_income": "-300000", "interest_expense": "100000", "income_tax_expense": "0",
               "depreciation": "500000", "amortization": "800000", "cash_available_for_debt_service": "-300000"}, "-0.50", {"SYN-ESC-001"}),
])
def test_core_scenario_arithmetic_abstention_and_false_positives(scenario, changes, expected_dscr, expected_flags, record_property):
    _, values, metrics, policy = policy_inputs(changes=changes)
    assert metrics["CALC-004"].display == expected_dscr
    risk = assess_risk(factors=(), metrics=metrics, financial_values=values, available_refs=frozenset(),
                      scope=SCOPE, as_of="2026-10-23", compliance=policy, dependency_digest="unit-dependency")
    # No approved scenario factor assessments exist; never borrow normal-case grades.
    assert risk.score.total is None and risk.score.band is None
    actual = {flag.rule_id for flag in risk.risk_flags}
    false_positive_count = len(actual - expected_flags)
    record_property("scenario", scenario)
    record_property("evidence_label", "DETERMINISTIC_KERNEL_ONLY_NOT_SOURCE_REGISTERED_WALKTHROUGH")
    record_property("false_positive_risk_count", false_positive_count)
    record_property("risk_recall", str(len(actual & expected_flags) / len(expected_flags)) if expected_flags else "NOT_APPLICABLE_NO_EXPECTED_POSITIVES")
    assert false_positive_count == 0
    assert actual == expected_flags
    if scenario == "E-M01":
        assert metrics["CALC-004"].validity == "UNKNOWN"
        assert policy.workflow == "NEEDS_INFORMATION"
    if scenario == "E-F03":
        assert metrics["CALC-009"].value == Decimal("-2")
        assert metrics["CALC-002"].value == Decimal("1100000")
        assert policy.workflow == "ESCALATE"  # Not a general Reject rule.
