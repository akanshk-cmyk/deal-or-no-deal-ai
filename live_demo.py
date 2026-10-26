"""Explicit Phase 1 UI coordination; existing graph owns all analysis and state."""
import json
from pathlib import Path
import tomllib
from uuid import UUID,uuid5

from .context import InputError,fingerprint
from . import live_worker
from .storage import Store
from .configuration import load_configuration
from .evaluation_transport import EvaluationTransport
from .provider import LIVE_STAGE_CAPS,prepare_request


def verify_synthesis_input(root,actor,operation):
    """One paid output-token setup probe, not a judge or quality evaluation."""
    root=Path(root)
    state=live_worker.load_live(root,actor,operation)
    if actor.persona!="Analyst" or state["status"]!="WAITING_CONFIGURATION" or state["pending_stage"]!="synthesizer":
        raise InputError("CURRENT_ANALYST_SYNTHESIS_SETUP_REQUIRED")
    scope=state["context"]["scope"]
    store=Store(load_configuration(root).database)
    store.assert_review_open(scope["review_id"])
    saved=store.get_record("live-provider-request:"+scope["run_id"]+":synthesizer")
    if saved is None or saved[1]["scope"]!=scope:
        raise InputError("CURRENT_PREPARED_SYNTHESIS_REQUIRED")
    task=saved[1]["task"];digest=fingerprint("LIVE_PACKET",task)
    if digest!=saved[1]["task_digest"]:
        raise InputError("PREPARED_SYNTHESIS_CHANGED")
    payload=dict(model="Qwen/Qwen3-30B-A3B-Instruct-2507",messages=[dict(role="system",content=task["instruction"]),
        dict(role="user",content=json.dumps(task["context"],ensure_ascii=False,allow_nan=False,separators=(",",":")))],
        response_format=dict(type="json_schema",json_schema=dict(name="synthesizer",strict=True,schema=task["schema"])),
        max_tokens=1,temperature=0,stream=False,n=1)
    probe_scope=dict(workspace_id=scope["workspace_id"],review_id=str(uuid5(UUID(scope["workspace_id"]),"input-token-probe:"+digest)),purpose="INPUT_TOKEN_PROBE")
    transport=EvaluationTransport(root,str(uuid5(UUID(scope["workspace_id"]),"input-token-evaluation:"+digest)),probe_scope)
    response=transport._dispatch("chat/completions",payload,_token_probe=True)
    count=response["usage"]["prompt_tokens"]
    if count>LIVE_STAGE_CAPS["synthesizer"][0]:
        raise InputError("PROVIDER_INPUT_EXCEEDS_APPROVED_CAP")
    actual=prepare_request(model_id=payload["model"],stage="synthesizer",instruction=task["instruction"],context=task["context"],
        verified_input_tokens=count,max_output_tokens=LIVE_STAGE_CAPS["synthesizer"][1],profile="LIVE-COMPACT-1.0")
    if {k:v for k,v in actual.items() if k!="max_tokens"}!={k:v for k,v in payload.items() if k!="max_tokens"}:
        raise InputError("PROBE_AND_ACTUAL_INPUT_DIFFER")
    path=root/"config/live_smoke.toml"
    text=path.read_text(encoding="utf-8")
    profile=tomllib.loads(text)
    counts=dict(profile.get("verified_packet_tokens",{}));counts[digest]=count
    scalar=text.partition("[verified_packet_tokens]")[0]
    temp=path.with_suffix(".tmp")
    temp.write_text(scalar+"[verified_packet_tokens]\n"+"\n".join(json.dumps(k)+" = "+str(v) for k,v in counts.items())+"\n",encoding="utf-8")
    temp.replace(path)
    return dict(task_digest=digest,verified_prompt_tokens=count,usage=transport.receipts)


def run_demo(root,actor,operation,*,resume_operation_id=None,upload_operation_id=None):
    """Called only by explicit Run/Continue, never page rendering. No retry loop."""
    kwargs=dict(resume_operation_id=resume_operation_id)
    if upload_operation_id:kwargs['upload_operation_id']=upload_operation_id
    state=live_worker.run_live(root,actor,operation,**kwargs)
    if ((state.get("context",{}).get("verification_policy")=="DEMO_DRAFT" or state.get('context',{}).get('upload_origin'))
        and state["status"]=="WAITING_CONFIGURATION" and state["pending_stage"]=="synthesizer"):
        probe=verify_synthesis_input(root,actor,operation)
        state=live_worker.run_live(root,actor,operation,resume_operation_id=str(uuid5(UUID(operation),"demo-setup:"+probe["task_digest"])))
    return state
