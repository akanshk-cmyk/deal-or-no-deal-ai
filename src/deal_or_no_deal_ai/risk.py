"""Approved educational factor aggregation and policy-linked flags; no grading LLM."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Mapping

from .context import InputError, money_string
from .documents import ReviewScope
from .finance import MetricValue
from .policy import CompliancePanel


WEIGHTS = (
    ("repayment_capacity", Decimal("0.3")), ("financial_leverage", Decimal("0.2")),
    ("collateral_quality", Decimal("0.2")), ("borrower_credit_profile", Decimal("0.2")),
    ("business_industry_risk", Decimal("0.1")),
)


@dataclass(frozen=True)
class FactorAssessment:
    factor_id: str
    rating: str | None
    assessment_id: str
    version: str
    reason: str
    refs: tuple[str, ...]
    material_fields: tuple[str, ...]
    required_metrics: tuple[str, ...]
    scope: ReviewScope
    as_of: str
    status: str = "CASE_AUTHOR_ASSESSED"
    method: str = "RISK-EDU-1.0"

    def __post_init__(self):
        if self.rating is not None:
            value = Decimal(money_string(self.rating))
            if not Decimal(0) <= value <= Decimal(100):
                raise InputError("FACTOR_RATING_OUT_OF_RANGE")


@dataclass(frozen=True)
class ScoreResult:
    status: str
    total: Decimal | None
    display: str | None
    band: str | None
    factors: tuple[dict, ...]
    missing: tuple[str, ...]
    workflow: str
    owner: str | None
    required_review_tier: str | None
    control_id: str | None
    dependency_digest: str
    method: str = "RISK-EDU-1.0"
    band_version: str = "SCORE-BANDS-1.0"
    routing_version: str = "SCORE-ROUTING-1.0"
    interpretation: str = "Illustrative risk from authored assessments; not probability of default"


@dataclass(frozen=True)
class RiskFlag:
    flag_id: str
    rule_id: str
    observed: Decimal
    threshold: Decimal
    gap: Decimal
    direction: str
    unit: str
    source_refs: tuple[str, ...]
    owner: str
    severity: str


@dataclass(frozen=True)
class RiskPanel:
    score: ScoreResult
    risk_flags: tuple[RiskFlag, ...]
    concentration_status: str = "NOT_ASSESSED"
    concentration_reason: str = "No approved method or portfolio exposure base"


def classify_score(value: Decimal) -> str:
    if not isinstance(value, Decimal) or not value.is_finite() or not Decimal(0) <= value <= Decimal(100):
        raise InputError("INVALID_COMPOSITE_SCORE")
    return "LOW" if value <= 25 else "MODERATE" if value <= 50 else "HIGH" if value <= 75 else "VERY_HIGH"


def assess_risk(
    *, factors: tuple[FactorAssessment, ...], metrics: Mapping[str, MetricValue],
    financial_values: Mapping[str, str | None], available_refs: frozenset[str],
    scope: ReviewScope, as_of: str, compliance: CompliancePanel, dependency_digest: str,
) -> RiskPanel:
    if compliance.dependency_digest != dependency_digest:
        raise InputError("STALE_POLICY_PANEL")
    known = {name for name, _ in WEIGHTS}
    ids = [a.factor_id for a in factors]
    invalid = len(ids) != len(set(ids)) or not set(ids) <= known
    missing = {"factor:" + name for name in known - set(ids)}
    contributions = []
    for assessment in factors:
        if (assessment.scope != scope or assessment.as_of != as_of or assessment.method != "RISK-EDU-1.0"
                or assessment.status != "CASE_AUTHOR_ASSESSED" or not assessment.assessment_id
                or not assessment.version or not assessment.reason.strip()):
            invalid = True
        if not assessment.refs or not set(assessment.refs) <= available_refs:
            missing.add("assessment_source:" + assessment.factor_id)
        if assessment.rating is None:
            missing.add("factor:" + assessment.factor_id)
        for field in assessment.material_fields:
            if financial_values.get(field) is None:
                missing.add("financial_input:" + field)
        for metric_id in assessment.required_metrics:
            if metric_id not in metrics or metrics[metric_id].validity != "VALID":
                missing.add("metric:" + metric_id)
    if invalid or missing:
        if invalid:
            missing.add("configuration:FACTOR_SCOPE_METHOD_OR_ID_INVALID")
        score = ScoreResult("INVALID" if invalid else "INSUFFICIENT_DATA", None, None, None, (), tuple(sorted(missing)),
                            "BLOCKED" if invalid else "NEEDS_INFORMATION", "Administrator" if invalid else "Analyst",
                            None, None if invalid else "SCORE-DATA-MISSING", dependency_digest)
    else:
        by_id = {a.factor_id: a for a in factors}
        with localcontext() as arithmetic:
            arithmetic.prec = 50
            total = Decimal(0)
            for name, weight in WEIGHTS:
                a = by_id[name]
                value = Decimal(a.rating)
                contribution = value * weight
                total += contribution
                contributions.append(dict(factor_id=name, rating=value, weight=weight, contribution=contribution,
                                          assessment_id=a.assessment_id, assessment_version=a.version, reason=a.reason,
                                          refs=a.refs, material_fields=a.material_fields, required_metrics=a.required_metrics))
            band = classify_score(total)
            display = format(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")
        routes = {
            "LOW": ("CONTINUE", None, None, None),
            "MODERATE": ("REVIEW_REQUIRED", "AuthorizedApprover", "NORMAL", "SCORE-REVIEW-MODERATE"),
            "HIGH": ("ESCALATE", "RiskManager", "NORMAL_AFTER_CREDIT_RISK_HANDLING", "SCORE-REVIEW-HIGH"),
            "VERY_HIGH": ("ESCALATE", "AuthorizedApprover", "SENIOR", "SCORE-REVIEW-VERY-HIGH"),
        }
        workflow, owner, tier, control = routes[band]
        score = ScoreResult("COMPUTED_FROM_SYNTHETIC_ASSESSMENTS", total, display, band, tuple(contributions), (),
                            workflow, owner, tier, control, dependency_digest)
    flags = []
    with localcontext() as arithmetic:
        arithmetic.prec = 50
        for rule in compliance.rules:
            if rule.outcome != "Exception" or rule.authority != "INTERNAL_SAMPLE_POLICY":
                continue
            if rule.rule_id not in ("SYN-ESC-001", "SYN-ESC-002", "SYN-ESC-004", "SYN-ESC-005"):
                continue
            observed, threshold = Decimal(rule.observed), Decimal(rule.threshold)
            shortfall = rule.rule_id == "SYN-ESC-001"
            flags.append(RiskFlag(rule.issue_id, rule.rule_id, observed, threshold,
                                  threshold - observed if shortfall else observed - threshold,
                                  "SHORTFALL" if shortfall else "EXCESS",
                                  "PERCENTAGE_POINTS" if rule.unit == "PERCENT" else rule.unit,
                                  rule.source_refs, rule.owner, rule.severity))
    return RiskPanel(score, tuple({f.flag_id: f for f in flags}.values()))
