"""Presentation safeguards reuse readiness without underwriting decisions."""
from copy import deepcopy
import pytest
from deal_or_no_deal_ai.readiness import evaluate_approval_readiness
from deal_or_no_deal_ai.recommendation import format_recommendation
from tests.unit.test_readiness import ready_inputs


def assessment(**changes):
    data=ready_inputs();data.update(changes)
    return evaluate_approval_readiness(**data).model_dump()


def test_unknown_readiness_is_not_approval_even_with_favorable_proposal():
    r=format_recommendation(None,ai_proposal={"decision":"Approve"})
    assert r["outcome"]=="Pending Review"
    assert "absence of a recorded blocker" in r["rationale"][1]["text"]


@pytest.mark.parametrize("status,expected",[("PENDING","Pending Review"),("MISSING","Additional Information Required"),("EXCEPTION","Exception Review Required"),("RECOVERY","Recovery Required")])
def test_existing_gate_controls_outcome_without_score_rules(status,expected):
    data=ready_inputs();data["requirements"][0]=data["requirements"][0].model_copy(update={"status":status,"reason":"Existing recorded blocker"})
    a=evaluate_approval_readiness(**data).model_dump();before=deepcopy(a)
    for band,score in (("LOW","1.00"),("VERY_HIGH","99.00")):
        r=format_recommendation(a,risk={"score":{"band":band,"display":score}},ai_proposal={"decision":"Approve"})
        assert r["outcome"]==expected
        assert r["issues"] and r["recommendation"]
        assert len(r["rationale"]) in (2,3,4)
    assert a==before


def test_ready_covenant_not_yet_due_does_not_become_a_breach():
    r=format_recommendation(assessment(),ai_proposal={"decision":"Approve"})
    assert r["outcome"]=="Ready for Human Decision"
    assert "consideration for approval" in r["recommendation"]
    assert not r["issues"]
    assert "breach" not in str(r).lower()


def test_ready_never_turns_unfavorable_proposal_into_approval_or_changes_human_status():
    r=format_recommendation(assessment(),ai_proposal={"decision":"Reject"},human_decision={"decision":"Reject"})
    assert "rejection" in r["recommendation"]
    assert "consideration for approval" not in r["recommendation"]
    assert r["human_decision"]=="Reject"


def test_missing_financial_values_are_not_invented_or_invalid_ratios_reported():
    r=format_recommendation(assessment(),financial={"metrics":[{"metric_id":"CALC-004","validity":"UNKNOWN","display":None}]})
    assert "ratio is" not in str(r)
    assert "Low" not in str(r)
    assert not r["issues"]
