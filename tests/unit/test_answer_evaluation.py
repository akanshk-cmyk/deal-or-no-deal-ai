"""Real native RAGAS algorithms with explicitly controlled, unpaid adapters."""
from copy import deepcopy
import socket
import pytest
from deal_or_no_deal_ai.answer_evaluation import evaluate, EvaluatorWire, validate_rubric, DIMENSIONS
from deal_or_no_deal_ai.context import InputError, fingerprint
from tests.integration.test_human_review_ui import internal_event_loop_pair


@pytest.fixture(autouse=True)
def event_loop(monkeypatch):
    monkeypatch.setattr(socket,"socketpair",internal_event_loop_pair)


def sample(**changes):
    s=dict(version="ANSWER-SAMPLE-1.0",query="What is DSCR?",response="DSCR is 1.50.",response_fields={"rationale":"DSCR is 1.50."},
        contexts=["DSCR is 1.50.","Annual statements remain unevaluated."],handles=["calc:DSCR"],reference="DSCR is 1.50.",
        ranked=True,application_mode="FIXTURE",subject="SYNTHESIS_ORIGINAL",context_origin="GENERATION_PACKET",independent_checks={"grants_credit_authority":False})
    s.update(changes);s["digest"]=fingerprint("ANSWER_SAMPLE",s)
    return s


def custom():
    return dict(dimensions={name:dict(status="SCORED",score=5,explanation="Controlled adapter example, not live quality evidence",examples=[dict(kind="SUPPORTED",response_field_path="rationale",response_excerpt="1.50",evidence_handles=["calc:DSCR"],evidence_excerpt="1.50",observation="Both exact supplied texts contain this value")],evaluation_limitations=["APPLICATION_TEST"]) for name in DIMENSIONS})


def judge(prompt,schema):
    name=schema["title"]
    if name=="StatementGeneratorOutput": return {"statements":["DSCR is 1.50."]}
    if name=="NLIStatementOutput": return {"statements":[dict(statement="DSCR is 1.50.",reason="Exact supplied context",verdict=1)]}
    if name=="AnswerRelevanceOutput": return dict(question="Generated question",noncommittal=0)
    if name=="ContextPrecisionOutput": return dict(reason="Controlled context relevance",verdict=1)
    if name=="ContextRecallOutput": return dict(classifications=[dict(statement="DSCR is 1.50.",reason="Exact supplied context",attributed=1)])
    if name=="EvaluatorWire": return custom()
    raise AssertionError(name)


def test_all_native_metrics_and_cached_custom_ragas_projections():
    embedding_calls=[]
    def embed(text):
        embedding_calls.append(text)
        return [1.0,0.0] if text=="What is DSCR?" else [-1.0,0.0]
    result=evaluate(sample(),judge,embed)
    assert result["status"]=="COMPLETE",result
    assert result["native"]["faithfulness"]["value"]==1
    assert result["native"]["response_relevancy"]["value"]==-1  # do not clip cosine
    assert result["native"]["context_recall"]["value"]==1
    assert result["native"]["context_precision"]["value"]==pytest.approx(1)
    assert len(embedding_calls)==2  # generated question reused across strictness=3
    assert result["calls"]==dict(judge=9,embedding=2)
    assert len(result["custom_ragas_projections"])==5
    assert not result["independent_checks"]["grants_credit_authority"]


def test_direct_missing_reference_and_embeddings_are_not_fake_zero_scores():
    result=evaluate(sample(ranked=False,reference=None),judge)
    assert result["status"]=="PARTIAL"
    assert result["native"]["context_precision"]["status"]=="NOT_APPLICABLE"
    for name in ("response_relevancy","context_recall"):
        assert result["native"][name]["status"]=="INPUT_UNAVAILABLE"
        assert result["native"][name]["value"] is None
    assert result["calls"]["judge"]==3  # two faithfulness requests + one shared rubric


@pytest.mark.parametrize("change",["score","quote","handle","extra","reference_leak"])
def test_reject_invalid_or_fabricated_custom_scores(change):
    wire=custom(); d=wire["dimensions"]["faithfulness"]
    if change=="score": d["score"]=True
    elif change=="quote": d["examples"][0]["response_excerpt"]="99.99"
    elif change=="handle": d["examples"][0]["evidence_handles"]=["other-deal"]
    elif change=="extra": wire["dimensions"]["unknown"]=deepcopy(d)
    else: d["examples"][0]["evidence_excerpt"]="Evaluator-only secret"
    with pytest.raises((ValueError,InputError)):
        validate_rubric(EvaluatorWire.model_validate(wire),sample(reference="Evaluator-only secret"))


def test_request_limit_failure_is_explicit_and_never_retries():
    result=evaluate(sample(),judge,max_judge_requests=1)
    assert result["status"]=="FAILED"
    assert result["calls"]["judge"]==1
    assert result["native"]["faithfulness"]["value"] is None


def test_empty_claims_are_undefined_not_perfect_faithfulness():
    result=evaluate(sample(),lambda p,s:{"statements":[]},metrics=("faithfulness",),rubric=False)
    assert result["native"]["faithfulness"]["value"] is None
    assert result["native"]["faithfulness"]["status"]=="NOT_EVALUABLE"


def test_changed_frozen_context_is_rejected_before_any_judge():
    s=sample();s["contexts"]=["poisoned context"]
    with pytest.raises(InputError,match="CHANGED"):
        evaluate(s,lambda *args:pytest.fail("No judge allowed"))
