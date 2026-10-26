"""Prepare by default; --run explicitly invokes guarded paid offline evaluation."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import UUID, uuid5

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    from deal_or_no_deal_ai.answer_evaluation import freeze_sample, evaluate, report_digest
    from deal_or_no_deal_ai.command_center import workspace_id
    from deal_or_no_deal_ai.review import Actor
    from deal_or_no_deal_ai.context import fingerprint, InputError
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--run", action="store_true", help="Explicitly spend within the shared USD0.10 allowance after verified setup")
    parser.add_argument("--retry-failed",action="store_true",help="One explicit correction; retain the failed report and reuse settled native requests")
    parser.add_argument("--reference", type=Path, help="Independent evaluator answer file, never added to generation context")
    args = parser.parse_args()
    permitted = frozenset(json.loads(p.read_text(encoding="utf-8"))["deal_id"] for p in (ROOT/"config/registrations").glob("*.json") if "deal_id" in json.loads(p.read_text(encoding="utf-8")))
    actor = Actor("Administrator", workspace_id(ROOT), permitted)
    sample = freeze_sample(ROOT, actor, args.operation)
    if args.reference:
        if args.reference.stat().st_size > 8192: raise InputError("EVALUATOR_REFERENCE_LIMIT")
        reference = json.loads(args.reference.read_text(encoding="utf-8"))
        if reference.get("scenario_id") != "E-N01" or not reference.get("reference") or not reference.get("basis"):
            raise InputError("SCOPED_REFERENCE_AND_BASIS_REQUIRED")
        # The supplied reference is for the approved Standard Deal only.
        registered = json.loads((ROOT/"config/registrations/e-n01.json").read_text(encoding="utf-8"))
        if sample["scope"]["deal_id"] != registered["deal_id"] or sample["scope"]["input_revision"] != 1:
            raise InputError("REFERENCE_SUBJECT_MISMATCH")
        sample.update(reference=reference["reference"],reference_basis=reference["basis"])
        sample["digest"] = fingerprint("ANSWER_SAMPLE", {k:v for k,v in sample.items() if k != "digest"})
    profile_digest = fingerprint("EVALUATION_PROFILE", (ROOT/"config/evaluation.toml").read_text(encoding="utf-8"))
    evaluation_id = str(uuid5(UUID(args.operation),sample["digest"]+profile_digest))
    directory = ROOT/"var/evaluations"; directory.mkdir(parents=True,exist_ok=True)
    destination = directory/("answer-quality-"+evaluation_id+".json")
    parent_report = None
    report_id = evaluation_id
    correction_id = str(uuid5(UUID(evaluation_id),"explicit-correction-1"))
    correction_path = directory/("answer-quality-"+correction_id+".json")
    if correction_path.exists():
        existing=json.loads(correction_path.read_text(encoding="utf-8"))
        print(json.dumps(dict(status=existing["result"]["status"],report=str(correction_path),replayed=False)));return
    if destination.exists():
        existing = json.loads(destination.read_text(encoding="utf-8"))
        if args.retry_failed and args.run and existing["result"]["status"] == "FAILED" and not any(a["status"]=="UNKNOWN" for a in existing["result"].get("paid_attempts",[])):
            parent_report=existing["evaluation_id"]; report_id=correction_id; destination=correction_path
        else:
            print(json.dumps(dict(status=existing["result"]["status"],report=str(destination),replayed=False)));return
    if not args.run:
        target = directory/("answer-sample-"+evaluation_id+".json")
        target.write_text(json.dumps(sample,indent=2,ensure_ascii=False),encoding="utf-8")
        print(json.dumps(dict(status="PREPARED_NOT_SCORED",evaluation_id=evaluation_id,sample=str(target),provider_calls=0,
            next_action="Configure the ignored .env and verify provider contracts before explicit --run. Human graph evidence reviews remain separate.")))
        return
    from deal_or_no_deal_ai.evaluation_transport import EvaluationTransport
    transport = EvaluationTransport(ROOT,evaluation_id,sample["scope"])
    instruction = (ROOT/"docs/agents/ragas-evaluator.md").read_text(encoding="utf-8").split("## Runtime prompt",1)[1].split("## Native metric reporting boundary",1)[0]
    result = evaluate(sample,transport.judge,transport.embed,rubric_instruction=instruction)
    from decimal import Decimal
    uncertain = any(a["status"] == "UNKNOWN" for a in transport.attempts)
    result.update(evidence="EXECUTED_RAGAS_DIAGNOSTIC",paid_requests=len(transport.attempts),paid_attempts=transport.attempts,usage_status="UNKNOWN_COST_REQUIRES_RECONCILIATION" if uncertain else "REPORTED",
        paid_usage=transport.receipts,cost_at_verified_rates_usd=None if uncertain else str(sum((Decimal(r["cost_usd"]) for r in transport.receipts if not r["cached"]),Decimal(0))))
    report = dict(version="ANSWER-REPORT-1.0",evaluation_id=report_id,parent_report=parent_report,evaluated_at_utc=datetime.now(timezone.utc).isoformat(),sample=sample,result=result,profile_digest=profile_digest)
    report["digest"] = report_digest(report)
    temporary = destination.with_suffix(".tmp"); temporary.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8"); temporary.replace(destination)
    print(json.dumps(dict(status=result["status"],report=str(destination),cost_usd=result["cost_at_verified_rates_usd"],paid_requests=result["paid_requests"])))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Do not expose provider bodies, credential-bearing exceptions or full paths.
        print(json.dumps(dict(status="BLOCKED",error_type=type(error).__name__,reason="Required saved synthesis, scoped inputs or verified provider configuration is unavailable; no automatic retry.")))
        raise SystemExit(1)
