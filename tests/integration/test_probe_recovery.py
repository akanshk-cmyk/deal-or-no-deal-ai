from copy import deepcopy
from dataclasses import replace
import pytest
from deal_or_no_deal_ai.probe_recovery import isolate_probe,TARGET,REVIEW,RESERVATION
from deal_or_no_deal_ai.storage import Store,RecordWrite
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.context import InputError
from tests.integration.test_evaluation_transport import setup


def prepare(root,scope):
    store=Store(root/'var/deal_review.sqlite3');store.initialize()
    scope={**scope,'review_id':REVIEW,'purpose':'INPUT_TOKEN_PROBE'}
    request=dict(scope=scope,payload={'max_tokens':1},maximum_cost_usd=RESERVATION,request_digest='synthetic-request')
    allowance=dict(limit_usd='0.10',committed_usd='0.0135178',reservations={TARGET:RESERVATION,'other':'0.0007'})
    receipt=store.admit(TARGET,scope,{'action':'OFFLINE_EVALUATION'},writes=(RecordWrite('evaluation-paid-request:'+TARGET,'EVALUATION_PAID_REQUEST',request,0),RecordWrite('paid-allowance:first-synthetic-010','PAID_ALLOWANCE',allowance,0)))
    store.mark_unknown(receipt)
    return store,Actor('Administrator',scope['workspace_id'],frozenset({scope['deal_id']})),allowance,receipt


def test_isolation_requires_approval_and_exact_versions(setup):
    root,scope=setup;store,actor,budget,receipt=prepare(root,scope)
    with pytest.raises(InputError,match='APPROVAL'):isolate_probe(store,actor,expected_versions={'request':1,'allowance':1})
    with pytest.raises(InputError,match='APPROVAL'):isolate_probe(store,replace(actor,persona='Analyst'),expected_versions={'request':1,'allowance':1},approved=True)
    with pytest.raises(InputError,match='STALE'):isolate_probe(store,actor,expected_versions={'request':2,'allowance':1},approved=True)
    assert store.get_record('paid-allowance:first-synthetic-010')[1]==budget
    audit=isolate_probe(store,actor,expected_versions={'request':1,'allowance':1},approved=True)
    assert not audit['provider_usage_reconciled']
    assert store.get_record('paid-allowance:first-synthetic-010')[1]==budget
    with store.connection() as c:assert c.execute('SELECT state,active_execution_key FROM app_operations WHERE operation_id=?',(TARGET,)).fetchone()[0]=='RELEASED'
    with pytest.raises(InputError,match='QUARANTINED'):store.assert_review_open(REVIEW)
    with pytest.raises(InputError):store.assert_claim(receipt)


def test_settled_result_forbids_isolation(setup):
    root,scope=setup;store,actor,budget,receipt=prepare(root,scope)
    store.put_record(RecordWrite('evaluation-paid-result:'+TARGET,'EVALUATION_PAID_RESULT',{'usage':'synthetic'},0))
    with pytest.raises(InputError,match='EXACT_UNKNOWN'):isolate_probe(store,actor,expected_versions={'request':1,'allowance':1},approved=True)
