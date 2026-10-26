"""Preview by default; --apply performs the explicitly approved administrative quarantine."""
import argparse
import json
from pathlib import Path
import sys
from uuid import UUID, uuid5

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "src"))


def main():
    from deal_or_no_deal_ai.live_recovery import QUARANTINE_OPERATION, ADDITIONAL_QUARANTINE_OPERATION, quarantine_unknown_extraction
    from deal_or_no_deal_ai.storage import Store
    from deal_or_no_deal_ai.review import Actor
    from deal_or_no_deal_ai.command_center import workspace_id
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--expected-versions",type=Path)
    parser.add_argument("--operation",choices=(QUARANTINE_OPERATION,ADDITIONAL_QUARANTINE_OPERATION),default=QUARANTINE_OPERATION)
    args=parser.parse_args()
    store=Store(ROOT / "var/deal_review.sqlite3")
    operation=args.operation
    suffix="-new-demo" if operation==ADDITIONAL_QUARANTINE_OPERATION else ""
    context=store.get_record("live-context:"+operation)[1]
    scope=context["scope"]
    reason="User approved setting aside this exact interrupted attempt while retaining unknown usage and the USD0.0007 reservation; continue only the earlier valid review after genuine human verification."
    if suffix:
        reason="User explicitly approved isolation of operation 54b1dd19-7dad-4ead-b297-31aae29a0d86; retain unknown usage and USD0.0007 reservation, fence replay and release only its execution claim. No credit decision or usage reconciliation."
    if args.apply:
        if args.expected_versions is None:
            raise ValueError("PREVIEW_MANIFEST_REQUIRED")
        preview=json.loads(args.expected_versions.read_text(encoding="utf-8"))
        if preview["operation_id"]!=operation or preview["reason"]!=reason:
            raise ValueError("QUARANTINE_PREVIEW_MISMATCH")
        actor=Actor("Administrator",workspace_id(ROOT),frozenset({scope["deal_id"]}))
        audit=quarantine_unknown_extraction(store,actor,operation,
            expected_versions=preview["expected_versions"],reason=reason)
        target=ROOT / ("var/evaluations/quarantine-applied"+suffix+".json")
        target.write_text(json.dumps(audit,indent=2),encoding="utf-8")
        print(json.dumps(dict(status="QUARANTINED_NOT_RECONCILED",receipt=str(target),
            retained_reservation_usd=audit["retained_reservation_usd"],provider_calls=0)))
    else:
        keys=dict(context="live-context:"+operation,progress="live-progress:"+operation,
                  ledger="ledger:"+scope["review_id"],allowance="paid-allowance:first-synthetic-010",
                  request="paid-request:"+str(uuid5(UUID(operation),"paid:extractor")))
        preview=dict(operation_id=operation,reason=reason,
                     expected_versions={name:store.get_record(key)[0] for name,key in keys.items()})
        target=ROOT / ("var/evaluations/quarantine-preview"+suffix+".json")
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(preview,indent=2),encoding="utf-8")
        print(json.dumps(dict(status="PREVIEW_ONLY",manifest=str(target),provider_calls=0)))


if __name__=="__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps(dict(status="BLOCKED",error_type=type(error).__name__,
            reason="Quarantine identities, authorization or expected records were not verified; no automatic retry.")))
        raise SystemExit(1)
