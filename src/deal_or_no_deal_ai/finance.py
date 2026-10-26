"""FIN-1.0 arithmetic kernel, not the trusted source-backed financial stage."""

from dataclasses import dataclass
from decimal import Decimal, DecimalException, Inexact, ROUND_HALF_UP, localcontext
from typing import Literal, Mapping

from .context import FINANCIAL_FIELDS, InputError, money_string


@dataclass(frozen=True)
class MetricValue:
    metric_id: str
    inputs: tuple[str, ...]
    unit: Literal["USD", "RATIO", "PERCENT"]
    validity: Literal["VALID", "UNKNOWN", "NOT_MEANINGFUL", "INVALID"]
    reason: str
    numerator: Decimal | None = None
    denominator: Decimal | None = None
    multiplier: Decimal = Decimal(1)
    value: Decimal | None = None
    display: str | None = None
    definition_version: str = "FIN-1.0"


NONNEGATIVE = frozenset((
    "annual_principal_payments", "annual_interest_payments", "existing_funded_debt",
    "proposed_funded_borrowing", "transaction_debt_repaid", "eligible_equipment_value",
    "prior_ranking_liens", "secured_facility_exposure", "current_assets", "current_liabilities",
))


def calculate_metrics(inputs: Mapping[str, str | None], *, secured_equipment: bool) -> dict[str, MetricValue]:
    """Calculate only; caller must establish support/scope/periods before trust.

    Exactly eighteen normalized fields are required. None is not zero. This
    helper neither normalizes source formatting nor certifies source evidence.
    """
    if set(inputs) != set(FINANCIAL_FIELDS) or type(secured_equipment) is not bool:
        raise InputError("FINANCIAL_KERNEL_PROFILE_MISMATCH")
    values = {k: None if v is None else Decimal(money_string(v)) for k, v in inputs.items()}
    results: dict[str, MetricValue] = {}

    def metric(number, names, unit, operation, *, percent=False, enabled=True):
        metric_id = f"CALC-{number:03}"
        names = tuple(names)
        common = dict(metric_id=metric_id, inputs=names, unit=unit)
        multiplier = Decimal(100) if percent else Decimal(1)
        if not enabled:
            result = MetricValue(**common, validity="UNKNOWN", reason="EQUIPMENT_NOT_APPLICABLE")
        elif any(values[k] is None for k in names):
            result = MetricValue(**common, validity="UNKNOWN", reason="MISSING_INPUT")
        elif any(values[k] < 0 for k in names if k in NONNEGATIVE):
            result = MetricValue(**common, validity="INVALID", reason="INVALID_OPERAND_SIGN")
        else:
            try:
                with localcontext() as arithmetic:
                    arithmetic.prec = 50
                    arithmetic.traps[Inexact] = True
                    if "transaction_debt_repaid" in names and (
                        values["transaction_debt_repaid"] > values["existing_funded_debt"] + values["proposed_funded_borrowing"]
                    ):
                        result = MetricValue(**common, validity="INVALID", reason="UNRECONCILED_DEBT_REPAYMENT")
                    else:
                        numerator, denominator = operation(values)
                        if denominator <= 0:
                            result = MetricValue(**common, validity="NOT_MEANINGFUL",
                                                 reason="NONPOSITIVE_DENOMINATOR", numerator=numerator,
                                                 denominator=denominator, multiplier=multiplier)
                        else:
                            scaled = numerator * multiplier
                            arithmetic.traps[Inexact] = False
                            arithmetic.rounding = ROUND_HALF_UP
                            value = scaled / denominator
                            display = format(value.quantize(Decimal("0.01")), "f")
                            result = MetricValue(**common, validity="VALID", reason="ARITHMETIC_ONLY",
                                                 numerator=numerator, denominator=denominator,
                                                 multiplier=multiplier, value=value, display=display)
            except DecimalException:
                result = MetricValue(**common, validity="INVALID", reason="ARITHMETIC_LIMIT")
        results[metric_id] = result

    ebit = ("net_income", "interest_expense", "income_tax_expense")
    ebitda = (*ebit, "depreciation", "amortization")
    debt = ("existing_funded_debt", "proposed_funded_borrowing", "transaction_debt_repaid")
    add = lambda v, keys: sum((v[k] for k in keys), Decimal(0))
    funded = lambda v: v[debt[0]] + v[debt[1]] - v[debt[2]]
    metric(1, ebit, "USD", lambda v: (add(v, ebit), Decimal(1)))
    metric(2, ebitda, "USD", lambda v: (add(v, ebitda), Decimal(1)))
    metric(3, debt, "USD", lambda v: (funded(v), Decimal(1)))
    metric(4, ("cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments"),
           "RATIO", lambda v: (v["cash_available_for_debt_service"], v["annual_principal_payments"] + v["annual_interest_payments"]))
    metric(5, (*debt, *ebitda), "RATIO", lambda v: (funded(v), add(v, ebitda)))
    metric(6, ("secured_facility_exposure", "prior_ranking_liens", "eligible_equipment_value"), "PERCENT",
           lambda v: (v["secured_facility_exposure"] + v["prior_ranking_liens"], v["eligible_equipment_value"]),
           percent=True, enabled=secured_equipment)
    metric(7, ("current_revenue", "previous_revenue"), "PERCENT",
           lambda v: (v["current_revenue"] - v["previous_revenue"], v["previous_revenue"]), percent=True)
    metric(8, ("current_assets", "current_liabilities"), "RATIO",
           lambda v: (v["current_assets"], v["current_liabilities"]))
    metric(9, ebit, "RATIO", lambda v: (add(v, ebit), v["interest_expense"]))
    return results


def compare_threshold(metric: MetricValue, *, operator: Literal["LT", "GT"], threshold: str) -> bool:
    """Exact cross-product comparison; no policy applicability or decision logic."""
    if (operator not in ("LT", "GT") or metric.validity != "VALID" or metric.numerator is None
            or metric.denominator is None or metric.denominator <= 0):
        raise InputError("THRESHOLD_REQUIRES_VALID_METRIC")
    limit = Decimal(money_string(threshold))
    try:
        with localcontext() as arithmetic:
            arithmetic.prec = 50
            arithmetic.traps[Inexact] = True
            left = metric.numerator * metric.multiplier
            right = limit * metric.denominator
            return left < right if operator == "LT" else left > right
    except DecimalException as exc:
        raise InputError("THRESHOLD_ARITHMETIC_LIMIT") from exc
