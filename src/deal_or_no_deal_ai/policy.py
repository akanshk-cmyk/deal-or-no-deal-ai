"""Versioned fictional policy handlers and recorded arithmetic traces; no LLM."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping

from .context import InputError, canonical_decimal, exact_confidence, fingerprint
from .contracts import TermFields
from .finance import MetricValue, compare_threshold


POLICY_VERSION = "SAMPLE-LOAN-POLICY-1.0"
NUMERIC_RULES = (
    ("001", "CALC-004", "LT", "1.25", "RATIO"),
    ("002", "CALC-005", "GT", "4", "RATIO"),
    ("004", "CALC-006", "GT", "80", "PERCENT"),
)


def sample_policy_spec():
    return dict(version=POLICY_VERSION, authority="INTERNAL_SAMPLE_POLICY",
                numerical_rules=[dict(rule_id="SYN-ESC-" + n, metric_id=m, comparator=o, threshold=t, unit=u)
                                 for n, m, o, t, u in NUMERIC_RULES],
                max_term_months=60, amount_review_usd="10000000", confidence_review_below="0.7",
                evidence_rules=["SYN-ESC-006", "SYN-ESC-007", "SYN-ESC-008"],
                synthetic_control_rules=["SYN-ESC-009", "SYN-ESC-010"],
                retired_rule_ids=["SYN-ESC-003"], no_automatic_reject=True)


@dataclass(frozen=True)
class PolicyConfig:
    secured_equipment: bool | None
    kyc_required: bool | None
    sanctions_required: bool | None
    applicability_basis: str
    version: str = POLICY_VERSION

    def __post_init__(self):
        if self.version != POLICY_VERSION or not self.applicability_basis:
            raise InputError("POLICY_CONFIGURATION_REQUIRED")
        if any(v is not None and type(v) is not bool for v in (
            self.secured_equipment, self.kyc_required, self.sanctions_required
        )):
            raise InputError("INVALID_POLICY_APPLICABILITY")


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    policy_version: str
    authority: str
    applicability: str
    evaluation_state: str
    predicate: str
    observed: str | None
    threshold: str | None
    unit: str | None
    condition_result: bool | None
    outcome: str | None
    control_result: str | None
    workflow: str
    severity: str | None
    owner: str | None
    issue_id: str | None
    source_refs: tuple[str, ...]
    calculation_ref: str | None
    numerator: Decimal | None
    denominator: Decimal | None
    multiplier: Decimal | None
    reason: str
    dependency_digest: str
    handler_version: str = "POLICY-HANDLERS-1.0"


@dataclass(frozen=True)
class CompliancePanel:
    policy_version: str
    rules: tuple[RuleResult, ...]
    exception_rule_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    workflow: str
    completeness: str
    dependency_digest: str
    review_trigger_group: dict


def aggregate_workflow(values):
    order = ("CONTINUE", "REVIEW_REQUIRED", "ESCALATE", "NEEDS_INFORMATION", "BLOCKED")
    values = tuple(values)
    if any(value not in order for value in values):
        raise InputError("UNKNOWN_WORKFLOW_STATUS")
    return max(values, key=order.index, default="CONTINUE")


def evaluate_policy(
    metrics: Mapping[str, MetricValue], terms: TermFields, *, config: PolicyConfig,
    dependency_digest: str, metric_source_refs: Mapping[str, tuple[str, ...]],
    material_financial_ready: bool, term_conflicts: bool = False,
    control_statuses: Mapping[str, str] | None = None,
    synthesis_complete: bool = False, confidence: Decimal | int | None = None,
) -> CompliancePanel:
    """Caller supplies scoped/source-validated inputs; this handler grants no support."""
    if type(material_financial_ready) is not bool or type(term_conflicts) is not bool or type(synthesis_complete) is not bool:
        raise InputError("INVALID_POLICY_FLAGS")
    if config.version != POLICY_VERSION:
        raise InputError("POLICY_CONFIGURATION_REQUIRED")
    rules = []

    def add(number, predicate, *, state="EVALUATED", applicability="APPLIES", observed=None,
            threshold=None, unit=None, condition=None, outcome="Pass", workflow="CONTINUE",
            reason="RECORDED_PREDICATE", refs=(), metric=None, product=False):
        rule_id = "SYN-ESC-" + number
        active = workflow != "CONTINUE"
        if workflow == "BLOCKED":
            owner = "ComplianceOfficer" if number in ("009", "010") else "Administrator"
            severity = "CRITICAL"
        elif workflow == "NEEDS_INFORMATION":
            owner, severity = "Analyst", "HIGH"
        elif number in ("011", "012") and active:
            owner, severity = "AuthorizedApprover", "HIGH" if number == "011" else "MEDIUM"
        elif active:
            owner, severity = "RiskManager", "HIGH"
        else:
            owner = severity = None
        control_result = ("TRIGGERED" if condition is True else "NOT_TRIGGERED" if condition is False else state) if product else None
        rules.append(RuleResult(
            rule_id, POLICY_VERSION, "DEMO_PRODUCT_CONTROL" if product else "INTERNAL_SAMPLE_POLICY",
            applicability, state, predicate, observed, threshold, unit, condition, None if product else outcome, control_result, workflow,
            severity, owner, fingerprint("POLICY_ISSUE", dict(dependency=dependency_digest, rule=rule_id)) if active else None,
            tuple(sorted(set(refs))) + (f"policy:{POLICY_VERSION}:{rule_id}",),
            metric.metric_id if metric else None, metric.numerator if metric else None,
            metric.denominator if metric else None, metric.multiplier if metric else None,
            reason, dependency_digest,
        ))

    for number, metric_id, operator, threshold, unit in NUMERIC_RULES:
        metric = metrics.get(metric_id)
        predicate = f"{metric_id} {'<' if operator == 'LT' else '>'} {threshold}"
        if number == "004" and config.secured_equipment is False:
            add(number, predicate, state="NOT_APPLICABLE", applicability="NOT_APPLICABLE", outcome="Not applicable",
                threshold=threshold, unit=unit, reason="APPROVED_NON_EQUIPMENT_CASE")
        elif config.secured_equipment is None and number == "004":
            add(number, predicate, state="UNKNOWN", applicability="UNKNOWN", outcome="Unknown", workflow="BLOCKED",
                threshold=threshold, unit=unit, reason="COLLATERAL_APPLICABILITY_REQUIRED")
        elif metric is None or metric.validity != "VALID":
            add(number, predicate, state="UNKNOWN", outcome="Unknown", workflow="NEEDS_INFORMATION",
                threshold=threshold, unit=unit, metric=metric, reason="METRIC_NOT_USABLE",
                refs=metric_source_refs.get(metric_id, ()))
        else:
            breach = compare_threshold(metric, operator=operator, threshold=threshold)
            add(number, predicate, observed=canonical_decimal(metric.value), threshold=threshold, unit=unit,
                condition=breach, outcome="Exception" if breach else "Pass", workflow="ESCALATE" if breach else "CONTINUE",
                metric=metric, refs=metric_source_refs.get(metric_id, ()))

    term = terms.term_months
    if term.value is None:
        add("005", "term_months > 60", state="UNKNOWN", outcome="Unknown", workflow="NEEDS_INFORMATION", reason="TERM_MISSING")
    else:
        breach = term.value > 60
        add("005", "term_months > 60", observed=str(term.value), threshold="60", unit="MONTHS", condition=breach,
            outcome="Exception" if breach else "Pass", workflow="ESCALATE" if breach else "CONTINUE", refs=term.refs)

    ltv = metrics.get("CALC-006")
    if config.secured_equipment is False:
        add("006", "required_equipment_evidence_unusable", applicability="NOT_APPLICABLE", state="NOT_APPLICABLE",
            outcome="Not applicable", reason="APPROVED_NON_EQUIPMENT_CASE")
    elif config.secured_equipment is None:
        add("006", "required_equipment_evidence_unusable", applicability="UNKNOWN", state="UNKNOWN",
            outcome="Unknown", workflow="BLOCKED", reason="COLLATERAL_APPLICABILITY_REQUIRED")
    else:
        unusable = ltv is None or ltv.validity != "VALID"
        add("006", "required_equipment_evidence_unusable", condition=unusable,
            outcome="Unknown" if unusable else "Pass", state="UNKNOWN" if unusable else "EVALUATED",
            workflow="NEEDS_INFORMATION" if unusable else "CONTINUE", reason="COLLATERAL_EVIDENCE_REQUIRED" if unusable else "SUPPORTED_FIXTURE_INPUTS",
            metric=ltv, refs=metric_source_refs.get("CALC-006", ()))
    add("007", "required_financial_inputs_unusable", condition=not material_financial_ready,
        state="EVALUATED" if material_financial_ready else "UNKNOWN", outcome="Pass" if material_financial_ready else "Unknown",
        workflow="CONTINUE" if material_financial_ready else "NEEDS_INFORMATION", reason="FINANCIAL_PREREQUISITES")
    add("008", "unresolved_material_rate_or_term_conflict", condition=term_conflicts,
        state="UNKNOWN" if term_conflicts else "EVALUATED", outcome="Unknown" if term_conflicts else "Pass",
        workflow="NEEDS_INFORMATION" if term_conflicts else "CONTINUE", reason="SOURCE_CONFLICT_CHECK")
    for number, required in (("009", config.kyc_required), ("010", config.sanctions_required)):
        status = (control_statuses or {}).get("SYN-ESC-" + number)
        if required is False:
            add(number, "required_synthetic_control_unresolved", state="NOT_APPLICABLE", applicability="NOT_APPLICABLE",
                outcome="Not applicable", reason="APPROVED_SYNTHETIC_CASE_NOT_REQUIRED")
        elif required is None:
            add(number, "required_synthetic_control_unresolved", state="UNKNOWN", applicability="UNKNOWN",
                outcome="Unknown", workflow="BLOCKED", reason="CONTROL_APPLICABILITY_REQUIRED")
        elif status == "RESOLVED_SYNTHETIC_FIXTURE":
            add(number, "required_synthetic_control_unresolved", condition=False, reason="SYNTHETIC_FIXTURE_ONLY")
        else:
            add(number, "required_synthetic_control_unresolved", state="UNKNOWN", outcome="Unknown", workflow="BLOCKED",
                condition=True if status == "UNRESOLVED_SYNTHETIC_FIXTURE" else None, reason="REQUIRED_SYNTHETIC_CONTROL_PENDING")

    amount = terms.requested_amount
    if amount.value is None:
        add("011", "requested_amount >= 10000000", state="UNKNOWN", outcome="Unknown", workflow="NEEDS_INFORMATION",
            reason="REQUESTED_AMOUNT_MISSING", product=True)
    else:
        triggered = Decimal(amount.value) >= Decimal("10000000")
        add("011", "requested_amount >= 10000000", observed=amount.value, threshold="10000000", unit="USD",
            condition=triggered, outcome="Exception" if triggered else "Pass",
            workflow="REVIEW_REQUIRED" if triggered else "CONTINUE", product=True, refs=amount.refs)
    if not synthesis_complete:
        add("012", "confidence < 0.7", state="NOT_EVALUATED", outcome=None, threshold="0.7",
            reason="AWAITING_VALIDATED_SYNTHESIS", product=True)
    elif confidence is None:
        add("012", "confidence < 0.7", state="UNKNOWN", outcome="Unknown", workflow="BLOCKED",
            threshold="0.7", reason="VALIDATED_CONFIDENCE_REQUIRED", product=True)
    else:
        value = exact_confidence(confidence)
        triggered = value < Decimal("0.7")
        add("012", "confidence < 0.7", observed=canonical_decimal(value), threshold="0.7", condition=triggered,
            outcome="Exception" if triggered else "Pass", workflow="REVIEW_REQUIRED" if triggered else "CONTINUE", product=True)
    controls = [r.condition_result for r in rules if r.rule_id in ("SYN-ESC-011", "SYN-ESC-012")]
    group = dict(operator="OR", rule_ids=("SYN-ESC-011", "SYN-ESC-012"), condition_states=tuple(controls),
                 result=True if any(v is True for v in controls) else False if all(v is False for v in controls) else None)
    return CompliancePanel(
        POLICY_VERSION, tuple(rules), tuple(sorted(r.rule_id for r in rules if r.outcome == "Exception" and r.authority == "INTERNAL_SAMPLE_POLICY")),
        tuple(sorted(r.issue_id for r in rules if r.issue_id)), aggregate_workflow(r.workflow for r in rules),
        "PARTIAL" if any(r.evaluation_state == "UNKNOWN" for r in rules) else "PRE_SYNTHESIS" if not synthesis_complete else "COMPLETE",
        dependency_digest, group,
    )
