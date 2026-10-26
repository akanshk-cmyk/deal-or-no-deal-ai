"""Reviewable LIVE-only packet proposal; no Runtime prompt/fixture/config edits."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from tokenizers import Tokenizer
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.synthesis import prepare_synthesis
from deal_or_no_deal_ai.provider import SCHEMAS


def main():
    from deal_or_no_deal_ai.live_context import prepare_live_tasks
    tasks = prepare_live_tasks(ROOT)
    case = load_registered_case(ROOT)
    manifest = json.loads((ROOT/'var/models/qwen-generation-tokenizer/manifest.json').read_bytes())
    tokenizer=Tokenizer.from_file(str(ROOT/'var/models/qwen-generation-tokenizer'/manifest['revision']/'tokenizer.json'))
    measurements={}
    for stage, task in tasks.items():
        measurements[stage]={k:len(tokenizer.encode(v if isinstance(v,str) else json.dumps(v,separators=(',',':'),ensure_ascii=False)).ids) for k,v in task.items()}
        measurements[stage]['component_total']=sum(measurements[stage].values())
    directory=ROOT/'var/evaluations/live-compaction-proposal'; directory.mkdir(parents=True,exist_ok=True)
    (directory/'packets.json').write_text(json.dumps(tasks,indent=2),encoding='utf-8')
    report=dict(status='APPROVED_PROFILE_NOT_DISPATCHED', full_original_source_pages_retained=len(case.inventory),
        tokenizer_revision=manifest['revision'],measurements=measurements, provider_overhead_verified=False,
        semantic_prompt_equivalence_verified=False, fixture_prompts_and_aggregate_budgets_unchanged=True)
    (directory/'measurement.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':
    main()
