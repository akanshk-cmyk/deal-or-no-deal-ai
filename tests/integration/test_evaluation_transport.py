"""No paid requests: shared reservation, cache, dimensions and unknown outcomes."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pytest
from deal_or_no_deal_ai.evaluation_transport import EvaluationTransport
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.storage import Store, RecordWrite
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import uid


@pytest.fixture
def setup():
    with TemporaryDirectory() as folder:
        root=Path(folder);copy_workspace(root)
        p=root/"config/evaluation.toml"
        original="\n".join(line for line in p.read_text(encoding="utf-8").splitlines() if not line.startswith("rates_verified_on"))
        p.write_text(original.replace("provider_contract_verified = false","provider_contract_verified = true").replace("embedding_dimensions = 4096","embedding_dimensions = 3")+'\nrates_verified_on="MOCK_ONLY"\n',encoding="utf-8")
        (root/".env").write_text("NEBIUS_API_KEY=synthetic-test-key")
        scope=dict(workspace_id=uid("eval-workspace"),review_id=uid("eval-review"),run_id=uid("eval-run"),deal_id=uid("eval-deal"),input_revision=1)
        yield root,scope


def response(endpoint,payload,key):
    assert key=="synthetic-test-key"
    if endpoint=="embeddings":
        return dict(model=payload["model"],usage={"prompt_tokens":3},data=[dict(index=0,embedding=[1.,0.,0.])])
    return dict(model=payload["model"],usage=dict(prompt_tokens=100,completion_tokens=10),choices=[dict(finish_reason="stop",message={"content":'{"ok":true}'})])


def test_guarded_paid_accounting_cache_and_shared_budget(setup):
    root,scope=setup
    with patch("deal_or_no_deal_ai.evaluation_transport._post",side_effect=response) as post:
        t=EvaluationTransport(root,uid("eval-one"),scope)
        assert t.judge("prompt",{"type":"object"})=={"ok":True}
        assert t.embed("query")==[1.,0.,0.]
        assert t.embed("query")==[1.,0.,0.]
        assert post.call_count==2
        assert t.receipts[-1]["cached"]
    budget=t.store.get_record("paid-allowance:first-synthetic-010")[1]
    assert budget["committed_usd"]=="0.00001303"
    assert not budget["reservations"]
    assert len(t.attempts)==2
    assert all(a["status"]=="SETTLED" for a in t.attempts)


def test_timeout_retains_allowance_and_never_retries(setup):
    root,scope=setup;t=EvaluationTransport(root,uid("eval-timeout"),scope)
    with patch("deal_or_no_deal_ai.evaluation_transport._post",side_effect=TimeoutError("do-not-expose-secret")) as post:
        with pytest.raises(InputError,match="UNCERTAIN") as caught:
            t.judge("prompt",{"type":"object"})
        assert "secret" not in str(caught.value)
        assert post.call_count==1
    assert t.attempts[0]["status"]=="UNKNOWN"
    assert t.store.get_record("paid-allowance:first-synthetic-010")[1]["reservations"]


def test_existing_generation_spend_blocks_evaluation_before_dispatch(setup):
    root,scope=setup;t=EvaluationTransport(root,uid("eval-budget-denied"),scope);t.store.initialize()
    t.store.put_record(RecordWrite("paid-allowance:first-synthetic-010","PAID_ALLOWANCE",dict(limit_usd="0.10",committed_usd="0.099",reservations={}),0))
    with patch("deal_or_no_deal_ai.evaluation_transport._post",side_effect=AssertionError("NO_POST")),pytest.raises(InputError,match="ALLOWANCE"):
        t.judge("prompt",{"type":"object"})
    assert not t.attempts


def test_disabled_configuration_never_initializes_or_dispatches(setup):
    root,scope=setup;p=root/"config/evaluation.toml";p.write_text(p.read_text().replace("provider_contract_verified = true","provider_contract_verified = false"))
    with pytest.raises(InputError,match="NOT_VERIFIED"):
        EvaluationTransport(root,uid("eval-disabled"),scope)
    assert not (root/"var/deal_review.sqlite3").exists()
    probe=EvaluationTransport(root,uid("eval-probe-restricted"),scope,probe=True)
    with pytest.raises(InputError,match="FIXED_CAPABILITY"):
        probe.judge("arbitrary prompt",{})
    with pytest.raises(InputError,match="FIXED_CAPABILITY"):
        probe.embed("arbitrary text")


def test_malformed_embedding_is_billed_but_never_used(setup):
    root,scope=setup;t=EvaluationTransport(root,uid("eval-bad-vector"),scope)
    def bad(*args):
        value=response(*args);value["data"][0]["embedding"]=[0.,0.,0.];return value
    with patch("deal_or_no_deal_ai.evaluation_transport._post",side_effect=bad),pytest.raises(InputError,match="DIMENSION_OR_VALUES"):
        t.embed("query")
    assert t.receipts[0]["cost_usd"]=="0.00000003"
    assert not t.store.get_record("paid-allowance:first-synthetic-010")[1]["reservations"]
