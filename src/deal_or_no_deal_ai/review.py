"""Pure M1 review-basis/draft guards. Full review commands belong to M3.

All actors/requirements/handle dictionaries are trusted service inputs, not
provider-supplied authorities. No function executes a graph or clears a policy.
"""

from dataclasses import dataclass, replace
from typing import Literal

from .context import InputError, fingerprint, stable_id


ANALYSIS_FIELDS = frozenset({"sources", "facts", "subject", "period", "review_source_basis",
    "policy", "formula", "factors", "analysis_support", "panels", "synthesis",
    "instructions", "schema", "config"})
DOMAINS = {"FINANCIAL_RISK": "RiskManager", "POLICY_CONTROL": "ComplianceOfficer"}


@dataclass(frozen=True)
class Actor:
    persona: str
    workspace_id: str
    allowed_deal_ids: frozenset[str]
    allowed_review_tiers: frozenset[str] = frozenset()
    attribution: Literal["SIMULATED"] = "SIMULATED"


def analytical_basis(projection: dict) -> str:
    if set(projection) != ANALYSIS_FIELDS:
        raise InputError("EXACT_ANALYTICAL_PROJECTION_REQUIRED")
    return fingerprint("REVIEW_ANALYSIS", projection)


@dataclass(frozen=True)
class Requirement:
    key: str
    satisfied: bool
    receipt_ref: str | None
    record_version: int

    def __post_init__(self):
        if not self.key or type(self.satisfied) is not bool or type(self.record_version) is not int or self.record_version < 1:
            raise InputError("INVALID_REVIEW_REQUIREMENT")
        if self.satisfied and not self.receipt_ref:
            raise InputError("REQUIREMENT_RECEIPT_REQUIRED")


@dataclass(frozen=True)
class PendingReview:
    request_id: str
    workspace_id: str
    deal_id: str
    thread_id: str
    input_revision: int
    analytical_basis_digest: str
    gate_version: int
    required_tier: str
    requirements: tuple[Requirement, ...]
    draft_ref: str | None = None
    draft_digest: str | None = None
    state: str = "PENDING"
    recorded_operation_id: str | None = None

    def __post_init__(self):
        if self.required_tier not in ("NORMAL", "SENIOR") or self.state not in ("PENDING", "RECORDED", "STALE"):
            raise InputError("INVALID_REVIEW_STATE")
        if type(self.gate_version) is not int or self.gate_version < 1 or type(self.input_revision) is not int or self.input_revision < 1:
            raise InputError("INVALID_REVIEW_VERSION")
        if len({item.key for item in self.requirements}) != len(self.requirements):
            raise InputError("DUPLICATE_REVIEW_REQUIREMENT")

    @property
    def gate_digest(self):
        # The package disposition itself is deliberately excluded from prerequisites.
        return fingerprint("REVIEW_GATE", {
            "request_id": self.request_id, "analysis": self.analytical_basis_digest,
            "version": self.gate_version, "tier": self.required_tier,
            "requirements": [{"key": item.key, "satisfied": item.satisfied,
                "receipt_ref": item.receipt_ref, "record_version": item.record_version}
                for item in sorted(self.requirements, key=lambda item: item.key)],
            "draft_ref": self.draft_ref, "draft_digest": self.draft_digest,
        })


def _actor_scope(actor: Actor, request: PendingReview):
    if actor.attribution != "SIMULATED" or actor.workspace_id != request.workspace_id or request.deal_id not in actor.allowed_deal_ids:
        raise InputError("ACTOR_OUT_OF_SCOPE")


def _current(request: PendingReview, expected_basis: str, expected_gate_version: int):
    if request.state != "PENDING" or request.analytical_basis_digest != expected_basis or request.gate_version != expected_gate_version:
        raise InputError("STALE_REVIEW")


def advance_handling(request: PendingReview, requirement: Requirement, *, expected_gate_version: int) -> PendingReview:
    _current(request, request.analytical_basis_digest, expected_gate_version)
    old = next((item for item in request.requirements if item.key == requirement.key), None)
    if old is None:
        raise InputError("UNKNOWN_PREREQUISITE")
    if old == requirement:
        return request
    if requirement.record_version <= old.record_version:
        raise InputError("STALE_HANDLING_RECORD")
    return replace(request, gate_version=request.gate_version + 1,
                   requirements=tuple(requirement if item.key == old.key else item for item in request.requirements))


@dataclass(frozen=True)
class DraftTarget:
    target_id: str
    text_digest: str
    refs: tuple[str, ...]
    domains: frozenset[str]


@dataclass(frozen=True)
class ConditionDraft:
    draft_id: str
    request_id: str
    analytical_basis_digest: str
    content_digest: str
    conditions: tuple[str, ...]
    targets: tuple[DraftTarget, ...]


def prepare_review_conditions(request: PendingReview, actor: Actor, operation_id: str,
                              conditions: tuple[str, ...], links: tuple[tuple[str, ...], ...],
                              required_domains: tuple[frozenset[str], ...], scoped_handles: frozenset[str],
                              *, expected_basis: str, expected_gate_version: int) -> tuple[PendingReview, ConditionDraft]:
    _actor_scope(actor, request)
    _current(request, expected_basis, expected_gate_version)
    if actor.persona != "AuthorizedApprover" or request.required_tier not in actor.allowed_review_tiers:
        raise InputError("APPROVER_TIER_REQUIRED")
    if not conditions or len(conditions) != len(links) or len(conditions) != len(required_domains):
        raise InputError("CONDITION_DRAFT_SHAPE")
    for text, refs, domains in zip(conditions, links, required_domains):
        if not text.strip() or not refs or len(set(refs)) != len(refs) or not set(refs) <= scoped_handles:
            raise InputError("CONDITION_SUPPORT_REQUIRED")
        if not domains or not domains <= DOMAINS.keys():
            raise InputError("CONDITION_DOMAINS_REQUIRED")
    digest = fingerprint("HUMAN_CONDITION_CONTENT", {"analysis": expected_basis,
        "conditions": conditions, "links": links, "required_domains": required_domains})
    draft_id = stable_id(operation_id, "REVIEW_CONDITION_DRAFT")
    targets = tuple(DraftTarget(stable_id(operation_id, f"conditions[{i}]"),
        fingerprint("NARRATIVE_TEXT", text), refs, domains)
        for i, (text, refs, domains) in enumerate(zip(conditions, links, required_domains)))
    draft = ConditionDraft(draft_id, request.request_id, expected_basis, digest, conditions, targets)
    requirements = tuple(item for item in request.requirements if not item.key.startswith("draft:"))
    requirements += tuple(Requirement("draft:" + target.target_id + ":" + domain, False, None, 1)
                          for target in targets for domain in sorted(target.domains))
    updated = replace(request, draft_ref=draft_id, draft_digest=digest,
                      requirements=requirements, gate_version=request.gate_version + 1)
    return updated, draft


def support_draft(request: PendingReview, draft: ConditionDraft, actor: Actor,
                  target_id: str, domain: str, evidence_refs: tuple[str, ...],
                  receipt_ref: str, *, expected_gate_version: int) -> PendingReview:
    _actor_scope(actor, request)
    _current(request, draft.analytical_basis_digest, expected_gate_version)
    if request.draft_ref != draft.draft_id or request.draft_digest != draft.content_digest:
        raise InputError("STALE_CONDITION_DRAFT")
    target = next((item for item in draft.targets if item.target_id == target_id), None)
    if target is None or domain not in target.domains or actor.persona != DOMAINS[domain]:
        raise InputError("WRONG_SUPPORT_DOMAIN")
    if not evidence_refs or not set(evidence_refs) <= set(target.refs) or not receipt_ref.strip():
        raise InputError("SCOPED_SUPPORT_EVIDENCE_REQUIRED")
    key = "draft:" + target_id + ":" + domain
    old = next(item for item in request.requirements if item.key == key)
    if old.satisfied and old.receipt_ref == receipt_ref:
        return request
    return advance_handling(request, Requirement(key, True, receipt_ref, old.record_version + 1),
                            expected_gate_version=expected_gate_version)


@dataclass(frozen=True)
class AcceptedReview:
    operation_id: str
    request_id: str
    analytical_basis_digest: str
    gate_version: int
    gate_digest: str
    decision: str
    draft_ref: str | None
    condition_target_refs: tuple[str, ...]


def accept_review(request: PendingReview, actor: Actor, operation_id: str, decision: str,
                  *, expected_basis: str, expected_gate_version: int,
                  draft: ConditionDraft | None = None) -> AcceptedReview:
    _actor_scope(actor, request)
    _current(request, expected_basis, expected_gate_version)
    if actor.persona != "AuthorizedApprover" or request.required_tier not in actor.allowed_review_tiers:
        raise InputError("APPROVER_TIER_REQUIRED")
    if decision not in ("Approve", "Conditional Approve", "Reject"):
        raise InputError("INVALID_CREDIT_DECISION")
    if any(not item.satisfied for item in request.requirements):
        raise InputError("PREREQUISITE_UNSATISFIED")
    if request.draft_ref is not None and (draft is None or draft.draft_id != request.draft_ref
                                        or draft.content_digest != request.draft_digest):
        raise InputError("EXACT_REVIEWED_DRAFT_REQUIRED")
    if request.draft_ref is None and draft is not None:
        raise InputError("UNPREPARED_CONDITION_DRAFT")
    return AcceptedReview(operation_id, request.request_id, expected_basis,
        request.gate_version, request.gate_digest, decision, request.draft_ref,
        () if draft is None else tuple(target.target_id for target in draft.targets))


def consume_own_receipt(request: PendingReview, accepted: AcceptedReview):
    if (request.state != "RECORDED" or request.recorded_operation_id != accepted.operation_id
        or request.request_id != accepted.request_id
        or request.analytical_basis_digest != accepted.analytical_basis_digest
        or request.gate_version != accepted.gate_version or request.gate_digest != accepted.gate_digest
        or any(not item.satisfied for item in request.requirements)):
        raise InputError("STALE_OR_WRONG_REVIEW_RECEIPT")
    return accepted


def review_action_availability(request: PendingReview, actor: Actor, *, information_pending: bool = False) -> dict:
    """Shared UI/service permissions; role selection never satisfies a prerequisite."""
    _actor_scope(actor, request)
    if actor.persona not in {"Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"}:
        raise InputError("UNKNOWN_REVIEW_ROLE")
    if type(information_pending) is not bool:
        raise InputError("INVALID_INFORMATION_STATUS")
    allowed = actor.persona in {"Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover"}
    actions = {"ADD_COMMENT": None if allowed else "ROLE_READ_ONLY",
               "REQUEST_INFORMATION": None if allowed else "ROLE_READ_ONLY"}
    if request.state != "PENDING":
        actions["REQUEST_INFORMATION"] = "REVIEW_NOT_PENDING"
    for action, decision in (("APPROVE", "Approve"), ("REJECT", "Reject")):
        try:
            accept_review(request, actor, request.request_id, decision,
                          expected_basis=request.analytical_basis_digest, expected_gate_version=request.gate_version)
            actions[action] = "INFORMATION_REQUEST_OUTSTANDING" if information_pending else None
        except InputError as error:
            actions[action] = str(error)
    return actions
