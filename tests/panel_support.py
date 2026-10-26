"""Controlled policy/risk application inputs; not registered alternate loans."""

from dataclasses import replace
from decimal import Decimal
import json

from deal_or_no_deal_ai.contracts import DealTermsWire
from deal_or_no_deal_ai.documents import ReviewScope
from deal_or_no_deal_ai.finance import calculate_metrics
from deal_or_no_deal_ai.policy import PolicyConfig, evaluate_policy
from deal_or_no_deal_ai.risk import FactorAssessment, WEIGHTS
from tests.support import ROOT


SCOPE = ReviewScope("unit-deal", 1, "unit-subject", "unit-facility", "unit-basis")
REFS = frozenset(("AGREEMENT-P1", "FIN-P1", "FIN-P2", "COLLATERAL-P1", "ASSESSMENT-P2"))


def policy_inputs(*, changes=None, term_changes=None, config=None, **options):
    data = json.loads((ROOT / "fixtures/development/e-n01/extraction.candidate.json").read_text(encoding="utf-8"))
    for key, value in (changes or {}).items():
        data["financial_inputs"][key] = (dict(value=None, refs=[], basis_id=None) if value is None
                                          else data["financial_inputs"][key] | dict(value=value))
    for key, value in (term_changes or {}).items():
        data["terms"][key]["value"] = value
    wire = DealTermsWire.model_validate(data)
    values = {k: f.value for k, f in wire.financial_inputs.__dict__.items()}
    metrics = calculate_metrics(values, secured_equipment=True)
    refs = {key: tuple(sorted({r for name in metric.inputs for r in getattr(wire.financial_inputs, name).refs}))
            for key, metric in metrics.items()}
    cfg = config or PolicyConfig(True, False, False, "Controlled synthetic application test")
    panel = evaluate_policy(metrics, wire.terms, config=cfg, dependency_digest="unit-dependency",
                            metric_source_refs=refs, material_financial_ready=all(
                                metrics[m].validity == "VALID" for m in ("CALC-004", "CALC-005", "CALC-006")), **options)
    return wire, values, metrics, panel


def factors(ratings=("20", "25", "20", "15", "30")):
    material = {
        "repayment_capacity": (("cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments"), ("CALC-004",)),
        "financial_leverage": (("existing_funded_debt", "proposed_funded_borrowing", "transaction_debt_repaid", "net_income", "interest_expense", "income_tax_expense", "depreciation", "amortization"), ("CALC-005",)),
        "collateral_quality": (("eligible_equipment_value", "prior_ranking_liens", "secured_facility_exposure"), ("CALC-006",)),
    }
    return tuple(FactorAssessment(name, rating, "unit-assessment:" + name, "unit-v1", "Explicit test-author assessment",
                                  ("ASSESSMENT-P2",), *material.get(name, ((), ())), SCOPE, "2026-10-23")
                 for (name, _), rating in zip(WEIGHTS, ratings))
