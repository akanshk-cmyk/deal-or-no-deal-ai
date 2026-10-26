"""Explicit first live journey; all human evidence/credit interrupts remain intact."""
import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))


def main():
    from deal_or_no_deal_ai.live_worker import run_live
    from deal_or_no_deal_ai.command_center import workspace_id
    from deal_or_no_deal_ai.review import Actor
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--continue",dest="resume",action="store_true");parser.add_argument("--correct-known-invalid",action="store_true");args=parser.parse_args()
    pointer=ROOT/"var/evaluations/first-live-journey.json"
    if pointer.exists(): operation=json.loads(pointer.read_text(encoding="utf-8"))["operation_id"]
    else:
        operation=str(uuid4());pointer.parent.mkdir(parents=True,exist_ok=True);pointer.write_text(json.dumps(dict(operation_id=operation)),encoding="utf-8")
    deal=json.loads((ROOT/"config/registrations/e-n01.json").read_text(encoding="utf-8"))["deal_id"]
    actor=Actor("Analyst",workspace_id(ROOT),frozenset({deal}))
    if args.correct_known_invalid:
        previous=json.loads(pointer.read_text(encoding="utf-8"))
        if len(previous.get("previous_attempts",[])) >= 2:raise ValueError("BOUNDED_EXPLICIT_CORRECTIONS_EXHAUSTED")
        from deal_or_no_deal_ai.live_recovery import close_known_invalid_extraction
        from deal_or_no_deal_ai.storage import Store
        from dataclasses import replace
        close_known_invalid_extraction(Store(ROOT/"var/deal_review.sqlite3"),replace(actor,persona="Administrator"),operation)
        old=operation;operation=str(uuid4())
        pointer.write_text(json.dumps(dict(operation_id=operation,previous_attempts=previous.get("previous_attempts",[])+[old],correction_reason="Explicit known invalid-output correction; original retained")),encoding="utf-8")
    state=run_live(ROOT,actor,operation,resume_operation_id=str(uuid4()) if args.resume else None)
    print(json.dumps(dict(operation_id=operation,status=state["status"],pending_stage=state["pending_stage"],completed_stages=list(state["artifacts"]),ledger=state["ledger"]["committed"],human_reviews_bypassed=False,report_generated=bool(state["report_markdown"]))))


if __name__=="__main__":
    try:main()
    except Exception as error:
        print(json.dumps(dict(status="STOPPED",error_type=type(error).__name__,reason="Required evidence/configuration or execution guard prevented continuation; no automatic retry, approval or credential display.")));raise SystemExit(1)
