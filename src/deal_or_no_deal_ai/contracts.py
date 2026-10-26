"""Strict model wires and application-owned hydration (SPEC-002/005).

No model client, automatic JSON repair, source lookup or database is initialized.
"""

from datetime import date
from decimal import Decimal
import json
from typing import Annotated, Generic, Literal, TypeVar
from uuid import UUID

from pydantic import (
    AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field,
    WithJsonSchema, create_model, field_validator, model_validator,
)

from .context import (
    FINANCIAL_FIELDS, InputError, exact_confidence, fingerprint,
    money_string, narrative_parent, stable_id, strict_json,
)


def _text(value: str) -> str:
    if not value.strip() or value == "Unknown":
        raise ValueError("NONBLANK_SUPPORTED_TEXT_REQUIRED")
    return value  # Preserve exact submitted content for evidence identity.


Text = Annotated[str, Field(min_length=1, max_length=4096), AfterValidator(_text)]


def _identifier(value: str) -> str:
    if str(UUID(value)) != value:
        raise ValueError("CANONICAL_UUID_REQUIRED")
    return value


Identifier = Annotated[str, AfterValidator(_identifier)]
Money = Annotated[str, AfterValidator(money_string)]
Confidence = Annotated[Decimal, BeforeValidator(exact_confidence),
                       WithJsonSchema({"type": "number", "minimum": 0, "maximum": 1})]
Owner = Literal["Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, allow_inf_nan=False)


class InterestTerms(StrictModel):
    kind: Literal["FIXED", "FLOATING"]
    annual_rate_percent: Money | None
    index: Text | None
    spread_bps: Money | None
    reset_frequency: Text | None
    floor_percent: Money | None

    @model_validator(mode="after")
    def consistent(self):
        if self.kind == "FIXED" and (
            self.annual_rate_percent is None
            or any(item is not None for item in
                   (self.index, self.spread_bps, self.reset_frequency))
        ):
            raise ValueError("INVALID_FIXED_INTEREST_TERMS")
        if self.kind == "FLOATING" and (self.index is None or self.spread_bps is None):
            raise ValueError("INCOMPLETE_FLOATING_INTEREST_TERMS")
        return self


T = TypeVar("T")


class WireFact(StrictModel, Generic[T]):
    value: T | None
    refs: list[Text] = Field(max_length=64)
    basis_id: Text | None

    @field_validator("refs")
    @classmethod
    def distinct_refs(cls, value):
        if len(value) != len(set(value)):
            raise ValueError("DUPLICATE_REFERENCE")
        return value

    @model_validator(mode="after")
    def missing_or_known(self):
        if self.value is None and (self.refs or self.basis_id is not None):
            raise ValueError("MISSING_FACT_HAS_NO_REFS_OR_BASIS")
        if self.value is not None and not self.refs:
            raise ValueError("KNOWN_FACT_REQUIRES_REFS")
        return self


def _iso_date(value: str) -> str:
    if date.fromisoformat(value).isoformat() != value:
        raise ValueError("ISO_DATE_REQUIRED")
    return value


class TermFields(StrictModel):
    borrower: WireFact[Text]
    legal_entity: WireFact[Text]
    facility_type: WireFact[Literal["TERM_LOAN"]]
    requested_amount: WireFact[Money]
    currency: WireFact[Literal["USD"]]
    term_months: WireFact[Annotated[int, Field(gt=0, le=999999999999999999)]]
    maturity_date: WireFact[Annotated[str, AfterValidator(_iso_date)]]
    interest_terms: WireFact[InterestTerms]
    repayment_structure: WireFact[Text]
    collateral: WireFact[list[Text]]
    guarantees: WireFact[list[Text]]
    covenants: WireFact[list[Text]]
    use_of_proceeds: WireFact[Text]

    @model_validator(mode="after")
    def positive_requested_amount(self):
        if self.requested_amount.value is not None and Decimal(self.requested_amount.value) <= 0:
            raise ValueError("POSITIVE_REQUESTED_AMOUNT_REQUIRED")
        return self


FinancialInputsWire = create_model(
    "FinancialInputsWire", __base__=StrictModel,
    **{name: (WireFact[Money], ...) for name in FINANCIAL_FIELDS},
)


class WireConflict(StrictModel):
    field_name: Text
    # The path-specific WireFact type is enforced by DealTermsWire below.
    candidates: list[dict] = Field(min_length=2, max_length=64)


class DealTermsWire(StrictModel):
    terms: TermFields
    financial_inputs: FinancialInputsWire
    conflicts: list[WireConflict] = Field(max_length=31)

    @model_validator(mode="after")
    def validate_conflicts(self):
        seen = set()
        for fact in self.financial_inputs.__dict__.values():
            if fact.value is not None and fact.basis_id is None:
                raise ValueError("FINANCIAL_BASIS_REQUIRED")
        for conflict in self.conflicts:
            if conflict.field_name in seen:
                raise ValueError("DUPLICATE_CONFLICT_FIELD")
            seen.add(conflict.field_name)
            pieces = conflict.field_name.split(".")
            if len(pieces) != 2 or pieces[0] not in ("terms", "financial_inputs"):
                raise ValueError("UNKNOWN_CONFLICT_FIELD")
            group = getattr(self, pieces[0])
            field = type(group).model_fields.get(pieces[1])
            if field is None or getattr(group, pieces[1]).value is not None:
                raise ValueError("CONFLICT_REQUIRES_NULL_MAIN_VALUE")
            fact_type = field.annotation
            candidates = [fact_type.model_validate(item) for item in conflict.candidates]
            if any(item.value is None for item in candidates):
                raise ValueError("CONFLICT_CANDIDATE_REQUIRES_VALUE")
            if pieces[0] == "financial_inputs" and any(item.basis_id is None for item in candidates):
                raise ValueError("FINANCIAL_BASIS_REQUIRED")
            identities = [fingerprint("CANDIDATE", item.model_dump()) for item in candidates]
            if len(set(identities)) != len(identities):
                raise ValueError("DUPLICATE_CONFLICT_CANDIDATE")
        return self


class PanelDecision(StrictModel):
    decision: Literal["Approve", "Conditional Approve", "Reject"]
    confidence: Confidence
    rationale: Text
    conditions: list[Text] = Field(max_length=64)
    escalate_to_human: bool

    @model_validator(mode="after")
    def conditional_requires_conditions(self):
        if self.decision == "Conditional Approve" and not self.conditions:
            raise ValueError("CONDITIONS_REQUIRED")
        return self


Refs = Annotated[list[Text], Field(min_length=1, max_length=64)]


class Observation(StrictModel):
    panel: Literal["FINANCIAL", "COMPLIANCE", "RISK"]
    text: Text
    refs: Refs


class ConditionLink(StrictModel):
    index: Annotated[int, Field(ge=0)]
    refs: Refs


class ProposedAction(StrictModel):
    kind: Literal["CONTINUE_STANDARD_REVIEW", "NORMAL_HUMAN_REVIEW",
                  "REFER_CREDIT_RISK_MANAGER", "REFER_SENIOR_CREDIT_AUTHORITY", "REQUEST_EVIDENCE"]
    target: Owner
    reason: Text
    refs: Refs

    @model_validator(mode="after")
    def compatible_owner(self):
        required = {
            "CONTINUE_STANDARD_REVIEW": "Analyst", "NORMAL_HUMAN_REVIEW": "AuthorizedApprover",
            "REFER_CREDIT_RISK_MANAGER": "RiskManager",
            "REFER_SENIOR_CREDIT_AUTHORITY": "AuthorizedApprover",
        }.get(self.kind)
        if required is not None and self.target != required:
            raise ValueError("ACTION_OWNER_MISMATCH")
        return self


class SynthesisWire(StrictModel):
    wire_version: Literal["SYN-WIRE-1.0"]
    panel_decision: PanelDecision
    observations: list[Observation] = Field(min_length=3, max_length=3)
    rationale_refs: Refs
    condition_links: list[ConditionLink] = Field(max_length=64)
    proposed_action: ProposedAction | None

    @model_validator(mode="after")
    def complete_panels_and_links(self):
        if {item.panel for item in self.observations} != {"FINANCIAL", "COMPLIANCE", "RISK"}:
            raise ValueError("ALL_THREE_PANELS_REQUIRED")
        indexes = [item.index for item in self.condition_links]
        if sorted(indexes) != list(range(len(self.panel_decision.conditions))):
            raise ValueError("CONDITION_LINKS_MISMATCH")
        refs = [self.rationale_refs, *(item.refs for item in self.observations),
                *(item.refs for item in self.condition_links)]
        if self.proposed_action is not None:
            refs.append(self.proposed_action.refs)
        if any(len(items) != len(set(items)) for items in refs):
            raise ValueError("DUPLICATE_REFERENCE")
        return self


class Scope(StrictModel):
    workspace_id: Identifier
    deal_id: Identifier
    review_id: Identifier
    run_id: Identifier
    thread_id: Identifier
    input_revision: Annotated[int, Field(gt=0)]


class Fact(StrictModel):
    fact_id: Identifier
    field_name: Text
    value: str | int | Decimal | list[str] | InterestTerms | None
    status: Literal["KNOWN", "MISSING", "CONFLICT"]
    refs: list[Text]
    basis_id: Text | None
    candidates: list[dict]
    support: Literal["PENDING", "REFERENCE_CHECKED"]


class NarrativeTarget(StrictModel):
    claim_ref: Identifier
    field_path: Text
    parent_digest: Text
    text_digest: Text
    dependency_digest: Text
    refs: Refs
    support: Literal["PENDING"]


def _resolve(refs: list[str], dictionary: dict[str, Scope], scope: Scope):
    if any(ref not in dictionary or dictionary[ref] != scope for ref in refs):
        raise InputError("REFERENCE_OUT_OF_SCOPE")


def parse_extraction(raw: str | bytes) -> DealTermsWire:
    return DealTermsWire.model_validate(strict_json(raw))


def parse_synthesis(raw: str | bytes) -> SynthesisWire:
    return SynthesisWire.model_validate(strict_json(raw))


def wire_json(wire: DealTermsWire | SynthesisWire) -> str:
    """Exact external JSON: confidence stays a number; money stays a string."""
    def encode(value):
        if isinstance(value, Decimal):
            from .context import canonical_decimal
            return canonical_decimal(value)
        if type(value) is dict:
            return "{" + ",".join(json.dumps(key) + ":" + encode(item) for key, item in value.items()) + "}"
        if type(value) is list:
            return "[" + ",".join(encode(item) for item in value) + "]"
        return json.dumps(value, ensure_ascii=False, allow_nan=False)
    return encode(wire.model_dump())


def hydrate_extraction(wire: DealTermsWire, scope: Scope, operation_id: str,
                       source_handles: dict[str, Scope], basis_handles: dict[str, Scope]) -> list[Fact]:
    conflicts = {item.field_name: item for item in wire.conflicts}
    facts = []
    for group_name in ("terms", "financial_inputs"):
        group = getattr(wire, group_name)
        for name in type(group).model_fields:
            item = getattr(group, name)
            path = group_name + "." + name
            conflict = conflicts.get(path)
            candidates = []
            all_items = [item]
            if conflict is not None:
                all_items.extend(type(item).model_validate(value) for value in conflict.candidates)
            for candidate in all_items:
                _resolve(candidate.refs, source_handles, scope)
                if candidate.basis_id is not None:
                    _resolve([candidate.basis_id], basis_handles, scope)
            value = item.value
            if value is not None and (group_name == "financial_inputs" or name == "requested_amount"):
                value = Decimal(value)
            elif isinstance(value, BaseModel):
                value = value.model_dump()
            if conflict:
                candidates = conflict.candidates
            facts.append(Fact(
                fact_id=stable_id(operation_id, path), field_name=path, value=value,
                status="CONFLICT" if conflict else "MISSING" if value is None else "KNOWN",
                refs=item.refs, basis_id=item.basis_id, candidates=candidates,
                # Scope-only M1 test dictionaries are not a full manifest/evidence check.
                support="PENDING",
            ))
    return facts


def hydrate_narrative(wire: SynthesisWire, scope: Scope, operation_id: str,
                      handles: dict[str, Scope], dependencies: dict) -> list[NarrativeTarget]:
    parent = narrative_parent(wire.model_dump(), dependencies)
    fields = [(f"observations[{index}].text", item.text, item.refs)
              for index, item in enumerate(wire.observations)]
    fields.append(("panel_decision.rationale", wire.panel_decision.rationale, wire.rationale_refs))
    links = {item.index: item.refs for item in wire.condition_links}
    fields.extend((f"panel_decision.conditions[{i}]", text, links[i])
                  for i, text in enumerate(wire.panel_decision.conditions))
    if wire.proposed_action is not None:
        fields.append(("proposed_action.reason", wire.proposed_action.reason, wire.proposed_action.refs))
    targets = []
    for path, text, refs in fields:
        _resolve(refs, handles, scope)
        targets.append(NarrativeTarget(
            claim_ref=stable_id(operation_id, path), field_path=path, parent_digest=parent,
            text_digest=fingerprint("NARRATIVE_TEXT", text),
            dependency_digest=fingerprint("NARRATIVE_DEPENDENCIES", dependencies),
            refs=refs, support="PENDING",
        ))
    return targets
