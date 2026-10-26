"""Explicit funded fixed capability probes, sharing the approved USD0.10 cap."""
import json
from datetime import datetime,timezone
from pathlib import Path
from uuid import UUID,uuid5
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))


def main():
    from deal_or_no_deal_ai.command_center import workspace_id
    from deal_or_no_deal_ai.evaluation_transport import EvaluationTransport
    from deal_or_no_deal_ai.context import InputError
    proof=ROOT/"var/evaluations/nebius-contract-probe.json"
    if proof.exists():
        print(json.dumps(dict(status="PREVIOUS_PROBE_RETAINED",report=str(proof),additional_paid_calls=0)));return
    catalog=json.loads((ROOT/"var/evaluations/nebius-model-verification.json").read_text(encoding="utf-8"))
    generation=next(r for r in catalog["models"] if r["model_id"]=="Qwen/Qwen3-30B-A3B-Instruct-2507")
    embedding=next(r for r in catalog["models"] if r["model_id"]=="Qwen/Qwen3-Embedding-8B")
    if any(r["status"]!="active" or r["model_id"] not in catalog["authenticated_models_available"] for r in (generation,embedding)):
        raise InputError("SELECTED_PROVIDER_MODELS_UNAVAILABLE")
    config=ROOT/"config/evaluation.toml";text=config.read_text(encoding="utf-8")
    values=dict(input_usd_per_million=str(generation["input_price_per_million_tokens"]),output_usd_per_million=str(generation["output_price_per_million_tokens"]),embedding_usd_per_million=str(embedding["input_price_per_million_tokens"]),verified_generation_input_ceiling=generation["max_model_len"],verified_embedding_input_ceiling=embedding["max_model_len"],rates_basis="Authenticated model list and official public model catalog verified before fixed probes")
    lines=[]
    for line in text.splitlines():
        key=line.partition("=")[0].strip()
        lines.append(key+" = "+json.dumps(values[key]) if key in values else line)
    if "rates_verified_on" not in text: lines.append('rates_verified_on = '+json.dumps(datetime.now(timezone.utc).isoformat()))
    config.write_text("\n".join(lines)+"\n",encoding="utf-8")
    workspace=workspace_id(ROOT);identifier=lambda name:str(uuid5(UUID(workspace),"nebius-fixed-probe:"+name))
    scope=dict(workspace_id=workspace,review_id=identifier("review"),run_id=identifier("run"),purpose="CAPABILITY_PROBE")
    transport=EvaluationTransport(ROOT,identifier("evaluation"),scope,probe=True)
    schema={"type":"object","properties":{"ok":{"type":"boolean"}},"required":["ok"],"additionalProperties":False}
    result=transport.judge("Return the object with ok set to true.",schema)
    if result!={"ok":True}:raise InputError("STRUCTURED_OUTPUT_PROBE_FAILED")
    vector=transport.embed("synthetic smoke test")
    record=dict(status="VERIFIED_FIXED_PROBES",generation_model=generation["model_id"],embedding_model=embedding["model_id"],embedding_dimensions=len(vector),usage=transport.receipts,attempts=transport.attempts,limitations=["Deployed context ceilings reserve worst-case cost; these are not exact per-review input token counts.","Generation packet counts and human evidence checkpoints remain mandatory; this probe does not activate the review graph."])
    proof.write_text(json.dumps(record,indent=2),encoding="utf-8")
    config.write_text(config.read_text(encoding="utf-8").replace("provider_contract_verified = false","provider_contract_verified = true"),encoding="utf-8")
    print(json.dumps(record))


if __name__=="__main__":
    try:main()
    except Exception as error:
        print(json.dumps(dict(status="PROBE_INCOMPLETE",error_type=type(error).__name__,reason="Inspect retained allowance/operations; no automatic retry or credential display.")));raise SystemExit(1)
