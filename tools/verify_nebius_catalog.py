"""Explicit free model/catalog checks; no generation or embedding request."""
import json
from pathlib import Path
import sys
from urllib.request import Request,build_opener
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))


def main():
    from deal_or_no_deal_ai.live_setup import read_api_key
    from deal_or_no_deal_ai.nebius_transport import NoRedirect
    selected={"Qwen/Qwen3-30B-A3B-Instruct-2507","Qwen/Qwen3-Embedding-8B"}
    opener=build_opener(NoRedirect)
    with opener.open(Request("https://tokenfactory.nebius.com/api/public/models_info"),timeout=30) as response:
        catalog=json.loads(response.read(2000000))
    records=[]
    for model in catalog:
        for flavor in model.get("flavors",[]):
            if flavor.get("model_id") in selected:
                records.append(dict(status=model["status"],**{k:flavor[k] for k in ("model_id","max_model_len","input_price_per_million_tokens","output_price_per_million_tokens") if k in flavor},embedding_size=model.get("embedding_size"),catalog_tags=model.get("tags",[])))
    with opener.open(Request("https://api.tokenfactory.nebius.com/v1/models",headers={"Authorization":"Bearer "+read_api_key(ROOT)}),timeout=30) as response:
        available=json.loads(response.read(2000000))
    ids={r["id"] for r in available["data"]}
    result=dict(catalog_source="https://tokenfactory.nebius.com/api/public/models_info",models=records,authenticated_models_available=sorted(selected&ids),paid_requests=0)
    directory=ROOT/"var/evaluations";directory.mkdir(parents=True,exist_ok=True)
    (directory/"nebius-model-verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result))


if __name__=="__main__":
    try:main()
    except HTTPError as error:
        print(json.dumps(dict(status="FAILED",http_status=error.code,credentials_displayed=False)));raise SystemExit(1)
    except Exception as error:
        print(json.dumps(dict(status="FAILED",error_type=type(error).__name__,credentials_displayed=False)));raise SystemExit(1)
