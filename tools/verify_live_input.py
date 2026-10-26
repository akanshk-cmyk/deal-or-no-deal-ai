"""One paid output token measures actual provider prompt usage for an exact task."""
import argparse
import json
from pathlib import Path
import sys
from uuid import UUID,uuid5
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))


def main():
    from deal_or_no_deal_ai.live_context import prepare_live_tasks
    from deal_or_no_deal_ai.command_center import workspace_id
    from deal_or_no_deal_ai.evaluation_transport import EvaluationTransport
    from deal_or_no_deal_ai.context import fingerprint,InputError
    from deal_or_no_deal_ai.storage import Store
    from deal_or_no_deal_ai.provider import LIVE_STAGE_CAPS,prepare_request
    import tomllib
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage",choices=("extractor","synthesizer"),default="extractor")
    parser.add_argument("--operation")
    args=parser.parse_args();workspace=workspace_id(ROOT)
    if args.stage=="extractor":
        task=prepare_live_tasks(ROOT)["extractor"]
    else:
        if not args.operation:raise InputError("CURRENT_LIVE_OPERATION_REQUIRED")
        store=Store(ROOT/"var/deal_review.sqlite3")
        context=store.get_record("live-context:"+args.operation)
        if not context or context[1]["scope"]["workspace_id"]!=workspace:raise InputError("LIVE_SCOPE_REQUIRED")
        prepared=store.get_record("live-provider-request:"+context[1]["scope"]["run_id"]+":synthesizer")
        if prepared is None:raise InputError("ACTUAL_SYNTHESIS_PACKET_NOT_PREPARED")
        task=prepared[1]["task"]
    digest=fingerprint("LIVE_PACKET",task)
    payload=dict(model="Qwen/Qwen3-30B-A3B-Instruct-2507",messages=[dict(role="system",content=task["instruction"]),dict(role="user",content=json.dumps(task["context"],ensure_ascii=False,allow_nan=False,separators=(",",":")))],response_format=dict(type="json_schema",json_schema=dict(name=args.stage,strict=True,schema=task["schema"])),max_tokens=1,temperature=0,stream=False,n=1)
    scope=dict(workspace_id=workspace,review_id=str(uuid5(UUID(workspace),"input-token-probe:"+digest)),purpose="INPUT_TOKEN_PROBE")
    transport=EvaluationTransport(ROOT,str(uuid5(UUID(workspace),"input-token-evaluation:"+digest)),scope)
    response=transport._dispatch("chat/completions",payload,_token_probe=True)
    count=response["usage"]["prompt_tokens"]
    if count>LIVE_STAGE_CAPS[args.stage][0]:raise InputError("PROVIDER_INPUT_EXCEEDS_APPROVED_CAP")
    actual=prepare_request(model_id=payload["model"],stage=args.stage,instruction=task["instruction"],context=task["context"],verified_input_tokens=count,max_output_tokens=LIVE_STAGE_CAPS[args.stage][1],profile="LIVE-COMPACT-1.0")
    if {k:v for k,v in actual.items() if k!="max_tokens"}!={k:v for k,v in payload.items() if k!="max_tokens"}:
        raise InputError("PROBE_AND_ACTUAL_INPUT_DIFFER")
    path=ROOT/"config/live_smoke.toml";text=path.read_text(encoding="utf-8")
    with path.open("rb") as stream:profile=tomllib.load(stream)
    updates=dict(provider_contract_verified=True,token_count_strategy="PROVIDER_VERIFIED_WHOLE_REQUEST",input_usd_per_million=transport.profile["input_usd_per_million"],output_usd_per_million=transport.profile["output_usd_per_million"],rates_verified_on=transport.profile["rates_verified_on"])
    # Keep scalar fields before the TOML table and retain every older packet count.
    scalar,sep,table=text.partition("[verified_packet_tokens]")
    lines=[]
    for line in scalar.splitlines():
        key=line.partition("=")[0].strip()
        lines.append(key+" = "+json.dumps(updates.pop(key)).lower() if key=="provider_contract_verified" and key in updates else key+" = "+json.dumps(updates.pop(key)) if key in updates else line)
    lines += [key+" = "+json.dumps(value) for key,value in updates.items()]
    counts=dict(profile.get("verified_packet_tokens",{}));counts[digest]=count
    path.write_text("\n".join(lines)+"\n[verified_packet_tokens]\n"+"\n".join(json.dumps(k)+" = "+str(v) for k,v in counts.items())+"\n",encoding="utf-8")
    record=dict(stage=args.stage,task_digest=digest,verified_prompt_tokens=count,max_output_tokens_during_probe=1,input_matches_actual_request=True,usage=transport.receipts,verified_at_utc=datetime.now(timezone.utc).isoformat(),evidence="ACTUAL_PROVIDER_PROMPT_USAGE_NOT_LOCAL_ESTIMATE")
    output=ROOT/"var/evaluations"/("live-input-"+digest+".json");output.write_text(json.dumps(record,indent=2),encoding="utf-8")
    print(json.dumps(record))


if __name__=="__main__":
    try:main()
    except Exception as error:
        print(json.dumps(dict(status="NOT_VERIFIED",error_type=type(error).__name__,reason="Retain diagnostics and reservations; no automatic retry or activation.")));raise SystemExit(1)
