"""Known primitive panel handoffs; exact Decimal restoration, no pickle."""

from dataclasses import fields
from decimal import Decimal

from .context import InputError, canonical_decimal
from .documents import ReviewScope
from .finance import MetricValue
from .policy import CompliancePanel, RuleResult
from .risk import RiskFlag, RiskPanel, ScoreResult
from .services import FinancialPanel


def _known(kind, payload):
    if type(payload) is not dict or set(payload) != {f.name for f in fields(kind)}:
        raise InputError("EXACT_PANEL_HANDOFF_SCHEMA_REQUIRED")
    return dict(payload)


def _decimal(value):
    if value is None:
        return None
    if type(value) is not str:
        raise InputError("PANEL_DECIMAL_STRING_REQUIRED")
    number = Decimal(value)
    if canonical_decimal(number) != value:
        raise InputError("PANEL_CANONICAL_DECIMAL_REQUIRED")
    return number


def restore_financial(payload):
    data = _known(FinancialPanel, payload)
    metrics = []
    for item in data["metric_results"]:
        row = _known(MetricValue, item)
        for name in ("value", "numerator", "denominator", "multiplier"):
            row[name] = _decimal(row[name])
        row["inputs"] = tuple(row["inputs"])
        metrics.append(MetricValue(**row))
    data.update(metric_results=tuple(metrics), scope=ReviewScope(**_known(ReviewScope, data["scope"])),
                metric_source_refs=tuple((key, tuple(refs)) for key, refs in data["metric_source_refs"]),
                missing_dependencies=tuple(data["missing_dependencies"]), input_facts=tuple(data["input_facts"]))
    return FinancialPanel(**data)


def restore_compliance(payload):
    data = _known(CompliancePanel, payload)
    rules = []
    for item in data["rules"]:
        row = _known(RuleResult, item)
        for name in ("numerator", "denominator", "multiplier"):
            row[name] = _decimal(row[name])
        row["source_refs"] = tuple(row["source_refs"])
        rules.append(RuleResult(**row))
    data.update(rules=tuple(rules), exception_rule_ids=tuple(data["exception_rule_ids"]), issue_ids=tuple(data["issue_ids"]))
    return CompliancePanel(**data)


def restore_risk(payload):
    data = _known(RiskPanel, payload)
    score = _known(ScoreResult, data["score"])
    score["total"] = _decimal(score["total"])
    factors = []
    for item in score["factors"]:
        row = dict(item)
        for name in ("rating", "weight", "contribution"):
            row[name] = _decimal(row[name])
        for name in ("refs", "material_fields", "required_metrics"):
            row[name] = tuple(row[name])
        factors.append(row)
    score.update(factors=tuple(factors), missing=tuple(score["missing"]))
    flags = []
    for item in data["risk_flags"]:
        row = _known(RiskFlag, item)
        for name in ("observed", "threshold", "gap"):
            row[name] = _decimal(row[name])
        row["source_refs"] = tuple(row["source_refs"])
        flags.append(RiskFlag(**row))
    return RiskPanel(**{**data, "score": ScoreResult(**score), "risk_flags": tuple(flags)})
