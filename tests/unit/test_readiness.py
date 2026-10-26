"""Educational readiness policy: no LLM and no automatic credit decision."""
from datetime import date
import pytest
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.readiness import CovenantEvaluation, EvaluatedRequirement, evaluate_approval_readiness


def ready_inputs():
    requirements=[EvaluatedRequirement(requirement_id=k,label=k,status="SATISFIED",reason="Synthetic requirement verified",evidence_refs=["SOURCE-1"],next_action="Review") for k in ("financial","policy","evidence","critical_exceptions","covenant_coverage")]
    covenant=CovenantEvaluation(covenant_id="annual-report",clause="Synthetic annual reporting obligation",applicability="APPLICABLE",timing="FUTURE",due_date="2027-03-31",evaluation_status="EVALUATED",compliance_status="NOT_YET_DUE",evidence_status="VERIFIED",evidence_refs=["SOURCE-1"],reason="Contractual future due date verified")
    return dict(scope={"input_revision":1},analysis_digest="synthetic-analysis",review_as_of="2026-10-24",requirements=requirements,covenants=[covenant],version=1,evaluated_at_utc="2026-10-24T00:00:00+00:00")


def test_verified_future_obligation_is_not_a_breach_and_ready_is_not_approval():
    result=evaluate_approval_readiness(**ready_inputs())
    assert result.outcome=="Ready for Human Decision"
    assert result.approval_eligible
    assert result.evaluated_requirements[0].status=="NOT_YET_DUE"
    assert "Authorized Approver" in result.permitted_next_actions[0]
    assert "decision" not in result.model_dump()


@pytest.mark.parametrize("updates,outcome",[
    ({"evaluation_status":"NOT_EVALUATED"},"Pending Review"),
    ({"timing":"UNKNOWN","due_date":None},"Pending Review"),
    ({"evidence_status":"MISSING"},"Additional Information Required"),
    ({"evidence_status":"STALE"},"Pending Review"),
    ({"compliance_status":"BREACHED"},"Exception Review Required"),
    ({"due_date":"2026-01-01"},"Pending Review"),
])
def test_covenant_blockers(updates,outcome):
    data=ready_inputs();data["covenants"][0]=data["covenants"][0].model_copy(update=updates)
    result=evaluate_approval_readiness(**data)
    assert result.outcome==outcome
    assert not result.approval_eligible


@pytest.mark.parametrize("identifier,status,outcome",[("financial","MISSING","Additional Information Required"),("evidence","PENDING","Pending Review"),("policy","EXCEPTION","Exception Review Required"),("critical_exceptions","EXCEPTION","Exception Review Required"),("financial","RECOVERY","Recovery Required")])
def test_mandatory_requirements_cannot_be_overridden_by_low_risk(identifier,status,outcome):
    data=ready_inputs()
    data["requirements"]=[r.model_copy(update={"status":status,"reason":"Blocking synthetic requirement"}) if r.requirement_id==identifier else r for r in data["requirements"]]
    result=evaluate_approval_readiness(**data)
    assert result.outcome==outcome and not result.approval_eligible
    assert result.reason=="Blocking synthetic requirement"


def test_complete_compliant_predecision_covenant():
    data=ready_inputs();data["covenants"][0]=data["covenants"][0].model_copy(update={"timing":"PRE_DECISION","due_date":None,"compliance_status":"COMPLIANT"})
    assert evaluate_approval_readiness(**data).approval_eligible


def test_missing_mandatory_check_cannot_silently_pass():
    data=ready_inputs();data["requirements"].pop()
    with pytest.raises(InputError,match="MANDATORY"):
        evaluate_approval_readiness(**data)
