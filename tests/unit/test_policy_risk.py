"""Scoped TEST-004-01/02/03/04/05/07/09/10/11; no model-quality claims."""

from dataclasses import asdict, replace
from decimal import Decimal

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.policy import PolicyConfig, aggregate_workflow
from deal_or_no_deal_ai.risk import assess_risk, classify_score
from tests.panel_support import REFS, SCOPE, factors, policy_inputs
from tests.support import OfflineTest


def rule(panel, suffix):
    return next(r for r in panel.rules if r.rule_id == "SYN-ESC-" + suffix)


def score(*, ratings=None, changes=None, replacements=None, available_refs=REFS):
    _, values, metrics, policy = policy_inputs(changes=changes)
    assessments = factors() if ratings is None else factors(ratings)
    if replacements is not None:
        assessments = replacements(assessments)
    return assess_risk(factors=assessments, metrics=metrics, financial_values=values,
                       available_refs=available_refs, scope=SCOPE, as_of="2026-10-23",
                       compliance=policy, dependency_digest="unit-dependency")


class PolicyTests(OfflineTest):
    def test_numerical_boundaries_and_trace_use_unrounded_operands(self):
        tests = (
            ({"cash_available_for_debt_service": "750000"}, "001", False),
            ({"cash_available_for_debt_service": "749999.999999"}, "001", True),
            ({"existing_funded_debt": "3500000"}, "002", False),
            ({"existing_funded_debt": "3500000.000001"}, "002", True),
            ({"secured_facility_exposure": "1600000"}, "004", False),
            ({"secured_facility_exposure": "1600000.000001"}, "004", True),
        )
        for changed, suffix, breached in tests:
            with self.subTest(change=changed):
                _, _, metrics, panel = policy_inputs(changes=changed)
                actual = rule(panel, suffix)
                self.assertEqual(actual.condition_result, breached)
                self.assertEqual(actual.outcome, "Exception" if breached else "Pass")
                self.assertEqual(actual.numerator, metrics[actual.calculation_ref].numerator)
                self.assertEqual(actual.denominator, metrics[actual.calculation_ref].denominator)
                self.assertIn(f"policy:SAMPLE-LOAN-POLICY-1.0:{actual.rule_id}", actual.source_refs)
                self.assertEqual(actual.workflow, "ESCALATE" if breached else "CONTINUE")

    def test_term_amount_confidence_and_retired_rule_remain_separate(self):
        for months, expected in ((60, "Pass"), (61, "Exception")):
            panel = policy_inputs(term_changes={"term_months": months})[-1]
            self.assertEqual(rule(panel, "005").outcome, expected)
        for amount, expected in (("5000000", False), ("9999999.999999", False), ("10000000", True)):
            panel = policy_inputs(term_changes={"requested_amount": amount})[-1]
            self.assertEqual(rule(panel, "011").condition_result, expected)
            self.assertIsNone(rule(panel, "011").outcome)
            self.assertEqual(rule(panel, "011").control_result, "TRIGGERED" if expected else "NOT_TRIGGERED")
            self.assertEqual(panel.review_trigger_group["result"], True if expected else None)
            self.assertNotIn("SYN-ESC-011", panel.exception_rule_ids)
            self.assertNotIn("SYN-ESC-003", [r.rule_id for r in panel.rules])
        for confidence, expected in ((Decimal("0.699999999999999999999999"), True), (Decimal("0.7"), False)):
            panel = policy_inputs(synthesis_complete=True, confidence=confidence)[-1]
            self.assertEqual(rule(panel, "012").condition_result, expected)
            self.assertNotIn("SYN-ESC-012", panel.exception_rule_ids)
        pending = rule(policy_inputs()[-1], "012")
        self.assertEqual(pending.evaluation_state, "NOT_EVALUATED")
        self.assertIsNone(pending.outcome)
        self.assertIsNone(pending.condition_result)

    def test_missing_financials_and_unknown_applicability_never_pass(self):
        panel = policy_inputs(changes={"cash_available_for_debt_service": None})[-1]
        self.assertEqual(rule(panel, "001").outcome, "Unknown")
        self.assertEqual(rule(panel, "007").workflow, "NEEDS_INFORMATION")
        self.assertEqual(panel.completeness, "PARTIAL")
        unknown = policy_inputs(config=PolicyConfig(None, None, None, "Unknown applicability test"))[-1]
        self.assertEqual(unknown.workflow, "BLOCKED")
        for suffix in ("004", "006", "009", "010"):
            self.assertEqual(rule(unknown, suffix).applicability, "UNKNOWN")

    def test_synthetic_control_requirements_and_inapplicability_are_explicit(self):
        cfg = PolicyConfig(True, True, True, "Explicit required synthetic controls")
        blocked = policy_inputs(config=cfg)[-1]
        self.assertEqual(blocked.workflow, "BLOCKED")
        self.assertEqual(rule(blocked, "009").outcome, "Unknown")
        self.assertEqual(rule(blocked, "010").owner, "ComplianceOfficer")
        unresolved = policy_inputs(config=cfg, control_statuses={"SYN-ESC-009": "UNRESOLVED_SYNTHETIC_FIXTURE"})[-1]
        self.assertTrue(rule(unresolved, "009").condition_result)
        default = policy_inputs()[-1]
        self.assertEqual(rule(default, "009").outcome, "Not applicable")
        nonequipment = policy_inputs(config=PolicyConfig(False, False, False, "Explicit nonequipment test"))[-1]
        self.assertEqual(rule(nonequipment, "004").outcome, "Not applicable")

    def test_workflow_precedence_preserves_all_findings_and_reject_is_not_an_output(self):
        panel = policy_inputs(changes={"cash_available_for_debt_service": "690000"},
                              config=PolicyConfig(True, True, False, "Required test control"))[-1]
        self.assertEqual(panel.workflow, "BLOCKED")
        self.assertIn("SYN-ESC-001", panel.exception_rule_ids)
        self.assertEqual(rule(panel, "001").workflow, "ESCALATE")
        self.assertEqual(len(panel.rules), 11)
        self.assertNotIn("Reject", str(asdict(panel)))
        for values, expected in ((("CONTINUE", "REVIEW_REQUIRED"), "REVIEW_REQUIRED"),
                                 (("ESCALATE", "NEEDS_INFORMATION"), "NEEDS_INFORMATION"),
                                 (("NEEDS_INFORMATION", "BLOCKED"), "BLOCKED")):
            self.assertEqual(aggregate_workflow(values), expected)


class RiskTests(OfflineTest):
    def test_approved_ratings_and_user_worked_example_match_exact_contributions(self):
        normal = score()
        self.assertEqual(normal.score.total, Decimal(21))
        self.assertEqual(normal.score.band, "LOW")
        example = score(ratings=("60", "40", "30", "20", "50"))
        self.assertEqual(example.score.total, Decimal(41))
        self.assertEqual([f["contribution"] for f in example.score.factors], list(map(Decimal, (18, 8, 6, 4, 5))))
        self.assertEqual(example.score.workflow, "REVIEW_REQUIRED")
        self.assertEqual(example.score.owner, "AuthorizedApprover")
        self.assertEqual(example.concentration_status, "NOT_ASSESSED")

    def test_continuous_bands_and_routes_precede_display_rounding(self):
        for raw, band in (("0", "LOW"), ("25", "LOW"), ("25.0001", "MODERATE"), ("25.5", "MODERATE"),
                          ("50", "MODERATE"), ("50.004", "HIGH"), ("75", "HIGH"), ("75.0001", "VERY_HIGH"), ("100", "VERY_HIGH")):
            with self.subTest(raw=raw):
                self.assertEqual(classify_score(Decimal(raw)), band)
                result = score(ratings=(raw,) * 5).score
                self.assertEqual(result.band, band)
                if band == "HIGH":
                    self.assertEqual((result.workflow, result.owner), ("ESCALATE", "RiskManager"))
                elif band == "VERY_HIGH":
                    self.assertEqual((result.workflow, result.owner, result.required_review_tier),
                                     ("ESCALATE", "AuthorizedApprover", "SENIOR"))
        self.assertEqual(score(ratings=("25.0001",) * 5).score.display, "25.00")

    def test_missing_factor_material_metric_or_source_withholds_full_score(self):
        results = (score(ratings=(None, "25", "20", "15", "30")),
                   score(changes={"cash_available_for_debt_service": None}),
                   score(changes={"annual_principal_payments": "0", "annual_interest_payments": "0"}),
                   score(available_refs=frozenset()))
        for result in results:
            self.assertEqual(result.score.status, "INSUFFICIENT_DATA")
            self.assertIsNone(result.score.total)
            self.assertIsNone(result.score.band)
            self.assertEqual(result.score.workflow, "NEEDS_INFORMATION")
            self.assertEqual(result.score.factors, ())

    def test_invalid_rating_duplicate_or_stale_scope_cannot_become_a_grade(self):
        for invalid in (True, "NaN", "100.1", "-1", 20.0, "20.00"):
            with self.subTest(rating=invalid), self.assertRaises(InputError):
                factors((invalid, "25", "20", "15", "30"))
        duplicate = score(replacements=lambda a: (a[0], a[0], *a[2:]))
        self.assertEqual(duplicate.score.status, "INVALID")
        stale = score(replacements=lambda a: (replace(a[0], scope=replace(SCOPE, revision=2)), *a[1:]))
        self.assertEqual(stale.score.status, "INVALID")
        self.assertIsNone(stale.score.total)

    def test_risk_flags_reuse_policy_issues_and_preserve_gap_units(self):
        result = score(changes={"cash_available_for_debt_service": "690000", "secured_facility_exposure": "1700000"})
        self.assertEqual(len(result.risk_flags), 2)
        flags = {f.rule_id: f for f in result.risk_flags}
        self.assertEqual(flags["SYN-ESC-001"].gap, Decimal("0.1"))
        self.assertEqual(flags["SYN-ESC-004"].gap, Decimal(5))
        self.assertEqual(flags["SYN-ESC-004"].unit, "PERCENTAGE_POINTS")
        self.assertEqual(len({f.flag_id for f in result.risk_flags}), 2)
