"""Approved live allocation, source preservation and unchanged Fixture defaults."""
from pathlib import Path
import json
import pytest
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.live_context import prepare_live_tasks, compact_schema, alias_definitions
from deal_or_no_deal_ai.provider import MODELS, SCHEMAS, stage_caps, prepare_request, normalize_response
from deal_or_no_deal_ai.services import load_registered_case

ROOT = Path(__file__).resolve().parents[2]

def test_live_packets_preserve_every_source_and_policy_predicate():
    case = load_registered_case(ROOT)
    tasks = prepare_live_tasks(ROOT)
    assert tasks["extractor"]["context"]["sources"] == {b.block_id: b.text for b in case.inventory}
    policy = tasks["synthesizer"]["context"]["policy"]
    assert {"predicate", "applicability", "result", "workflow", "ref"} <= set(policy["columns"])
    assert tasks["synthesizer"]["context"]["concentration"] == "NOT_ASSESSED"

@pytest.mark.parametrize("stage", ["extractor", "synthesizer"])
def test_schema_aliases_preserve_all_validation_constraints(stage):
    original = compact_schema(SCHEMAS[stage].model_json_schema())
    aliased = alias_definitions(original)
    reverse = {"d" + str(i): name for i, name in enumerate(original.get("$defs", {}))}
    def restore(value):
        if isinstance(value, list):
            return [restore(v) for v in value]
        if isinstance(value, dict):
            return {k: ("#/$defs/" + reverse[v[len("#/$defs/"):]] if k == "$ref" and isinstance(v, str) and v.startswith("#/$defs/") else {reverse[n]: restore(d) for n, d in v.items()} if k == "$defs" else restore(v)) for k, v in value.items()}
        return value
    assert restore(aliased) == original

@pytest.mark.parametrize("stage,count,output", [("extractor",4000,1000),("synthesizer",2500,650)])
def test_live_caps_are_explicit_and_fixture_default_remains_stricter(stage,count,output):
    kwargs = dict(model_id=MODELS[0], stage=stage, instruction="Synthetic task", context={}, verified_input_tokens=count, max_output_tokens=output)
    with pytest.raises(InputError):
        prepare_request(**kwargs)
    payload = prepare_request(**kwargs, profile="LIVE-COMPACT-1.0")
    assert payload["max_tokens"] == output
    with pytest.raises(InputError):
        prepare_request(**{**kwargs,"verified_input_tokens":count+1},profile="LIVE-COMPACT-1.0")
    with pytest.raises(InputError):
        stage_caps("unknown")
    assert 4000 + 2500 + 1500 == 8000
    assert 1000 + 650 + 350 == 2000

def test_synthesis_response_uses_selected_caps_and_original_full_parser():
    response = dict(model=MODELS[0],choices=[dict(finish_reason="stop",message=dict(role="assistant",content=(ROOT/"fixtures/development/e-n01/synthesis.default.json").read_text()))],usage=dict(prompt_tokens=2200,completion_tokens=600,total_tokens=2800))
    assert normalize_response(response,model_id=MODELS[0],stage="synthesizer").reason == "PROVIDER_USAGE_EXCEEDS_STAGE_CAP"
    assert normalize_response(response,model_id=MODELS[0],stage="synthesizer",profile="LIVE-COMPACT-1.0").status == "VALIDATED"
