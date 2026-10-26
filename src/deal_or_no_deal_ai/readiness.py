"""READINESS-1.0 pure approval eligibility. Never an AI or human credit decision."""
from datetime import date
from typing import Literal
from pydantic import Field, model_validator
from .contracts import StrictModel, Text
from .context import InputError, fingerprint

Outcome = Literal["Ready for Human Decision", "Pending Review", "Additional Information Required", "Exception Review Required", "Recovery Required"]
Status = Literal["SATISFIED", "NOT_APPLICABLE", "NOT_YET_DUE", "PENDING", "MISSING", "STALE", "EXCEPTION", "RECOVERY"]

class EvaluatedRequirement(StrictModel):
    requirement_id: Text
    label: Text
    mandatory: bool = True
    status: Status
    reason: Text
    evidence_refs: list[Text] = Field(max_length=128)
    next_action: Text

class CovenantEvaluation(StrictModel):
    covenant_id: Text
    clause: Text
    mandatory: bool = True
    applicability: Literal["APPLICABLE", "NOT_APPLICABLE", "UNKNOWN"] = "UNKNOWN"
    timing: Literal["PRE_DECISION", "ONGOING", "FUTURE", "UNKNOWN"] = "UNKNOWN"
    due_date: str | None = None
    evaluation_status: Literal["EVALUATED", "NOT_EVALUATED"] = "NOT_EVALUATED"
    compliance_status: Literal["COMPLIANT", "NOT_YET_DUE", "BREACHED", "UNKNOWN"] = "UNKNOWN"
    evidence_status: Literal["VERIFIED", "PENDING", "MISSING", "STALE"] = "PENDING"
    evidence_refs: list[Text] = Field(max_length=64)
    reason: Text

    @model_validator(mode="after")
    def due(self):
        if self.due_date is not None and date.fromisoformat(self.due_date).isoformat()!=self.due_date:
            raise ValueError("COVENANT_ISO_DUE_DATE_REQUIRED")
        return self

class ApprovalReadiness(StrictModel):
    schema_version: Literal["READINESS-1.0"] = "READINESS-1.0"
    assessment_id: Text
    version: int = Field(ge=0)
    scope: dict
    review_version: int = Field(ge=1)
    analysis_digest: Text
    evaluated_at_utc: str | None
    review_as_of: str
    outcome: Outcome
    approval_eligible: bool
    reason: Text
    evaluated_requirements: list[EvaluatedRequirement]
    covenants: list[CovenantEvaluation]
    blockers: list[Text]
    evidence_refs: list[Text]
    permitted_next_actions: list[Text]
    previous_assessment_id: str | None
    assessment_digest: Text

    @model_validator(mode="after")
    def integrity(self):
        if self.approval_eligible != (self.outcome=="Ready for Human Decision") or self.approval_eligible and self.blockers:
            raise ValueError("READINESS_ELIGIBILITY_MISMATCH")
        body=self.model_dump(exclude={"assessment_digest"})
        if self.assessment_digest!=fingerprint("APPROVAL_READINESS",body):
            raise ValueError("READINESS_DIGEST_MISMATCH")
        return self


def evaluate_covenant(covenant, review_as_of):
    c=covenant
    status="PENDING";reason="Mandatory covenant evaluation incomplete"
    action="Evaluate the annual financial-statement reporting covenant, including its contractual timing and requirements."
    if c.evidence_status=="STALE":
        status="STALE";reason="Covenant evidence is stale for this review version"
    elif c.evidence_status=="MISSING":
        status="MISSING";reason="Required covenant evidence is missing"
    elif c.evaluation_status=="EVALUATED" and c.evidence_status=="VERIFIED" and c.evidence_refs:
        if c.applicability=="NOT_APPLICABLE":
            status="NOT_APPLICABLE";reason=c.reason
        elif c.applicability=="APPLICABLE" and c.timing!="UNKNOWN":
            if c.compliance_status=="BREACHED":
                status="EXCEPTION";reason="An evaluated covenant breach requires exception review"
            elif c.compliance_status=="COMPLIANT" and (c.timing=="PRE_DECISION" or c.due_date is not None):
                status="SATISFIED";reason=c.reason
            elif c.compliance_status=="NOT_YET_DUE" and c.timing in ("FUTURE","ONGOING") and c.due_date and date.fromisoformat(c.due_date)>date.fromisoformat(review_as_of):
                status="NOT_YET_DUE";reason="Reviewed future obligation is not yet due; future fulfilment is not required now"
    return EvaluatedRequirement(requirement_id="covenant:"+c.covenant_id,label=c.clause,mandatory=c.mandatory,status=status,reason=reason,evidence_refs=c.evidence_refs,next_action=action)


def evaluate_approval_readiness(*, scope, analysis_digest, review_as_of, requirements, covenants, version, evaluated_at_utc, previous_assessment_id=None):
    date.fromisoformat(review_as_of)
    required={"financial","policy","evidence","critical_exceptions","covenant_coverage"}
    if not required<={r.requirement_id for r in requirements if r.mandatory}:
        raise InputError("MANDATORY_READINESS_CHECKS_REQUIRED")
    checks=[evaluate_covenant(c,review_as_of) for c in covenants]+list(requirements)
    ids=[r.requirement_id for r in checks]
    if len(ids)!=len(set(ids)):
        raise InputError("DUPLICATE_READINESS_REQUIREMENT")
    blockers=[r for r in checks if r.mandatory and r.status not in ("SATISFIED","NOT_APPLICABLE","NOT_YET_DUE")]
    statuses={r.status for r in blockers}
    outcome="Recovery Required" if "RECOVERY" in statuses else "Additional Information Required" if "MISSING" in statuses else "Exception Review Required" if "EXCEPTION" in statuses else "Pending Review" if blockers else "Ready for Human Decision"
    priority={"RECOVERY":0,"MISSING":1,"EXCEPTION":2,"STALE":3,"PENDING":3}
    blockers.sort(key=lambda r:priority[r.status])
    actions=list(dict.fromkeys(r.next_action for r in blockers)) or ["An Authorized Approver must review the current package before recording a credit decision."]
    body=dict(schema_version="READINESS-1.0",assessment_id=fingerprint("READINESS_ASSESSMENT_ID",dict(scope=scope,analysis=analysis_digest,version=version,checks=[c.model_dump() for c in checks])),version=version,scope=scope,review_version=scope["input_revision"],analysis_digest=analysis_digest,evaluated_at_utc=evaluated_at_utc,review_as_of=review_as_of,outcome=outcome,approval_eligible=not blockers,reason=blockers[0].reason if blockers else "All mandatory approval-readiness requirements are evaluated and satisfied",evaluated_requirements=[c.model_dump() for c in checks],covenants=[c.model_dump() for c in covenants],blockers=[c.requirement_id for c in blockers],evidence_refs=sorted({ref for c in checks for ref in c.evidence_refs}),permitted_next_actions=actions,previous_assessment_id=previous_assessment_id)
    return ApprovalReadiness(**body,assessment_digest=fingerprint("APPROVAL_READINESS",body))
