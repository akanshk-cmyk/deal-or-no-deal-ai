"""Prepare by default; --run explicitly makes at most three advisory Nebius judge calls."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import sys
from uuid import UUID, uuid5

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))


def main():
    from deal_or_no_deal_ai.fact_judge import freeze, run, markdown, validate_batch_diagnostic, batches
    from deal_or_no_deal_ai.review import Actor
    from deal_or_no_deal_ai.command_center import workspace_id
    from deal_or_no_deal_ai.context import fingerprint
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation',default='46802df1-4f6b-435d-895e-61576fca3d9b')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--continue-independent',action='store_true',help='Reuse the settled first batch with evidence flags; judge only the two remaining independent batches.')
    args=parser.parse_args()
    deal=json.loads((ROOT/'config/registrations/e-n01.json').read_text(encoding='utf-8'))['deal_id']
    actor=Actor('Administrator',workspace_id(ROOT),frozenset({deal}))
    sample=freeze(ROOT,actor,args.operation)
    directory=ROOT/'var/evaluations'
    directory.mkdir(parents=True,exist_ok=True)
    path=directory/('fact-judge-'+sample['evaluation_id']+'.json')
    parent=None
    report_id=sample['evaluation_id']
    if path.exists():
        report=json.loads(path.read_text(encoding='utf-8'))
        clean={k:v for k,v in report.items() if k!='report_digest'}
        expected=fingerprint('FACT_JUDGE_REPORT',json.dumps(clean,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')))
        if report['sample']['digest']!=sample['digest'] or report.get('report_digest')!=expected:
            raise ValueError('FACT_JUDGE_REPORT_IDENTITY_OR_DIGEST_MISMATCH')
        if not args.continue_independent:
            print(json.dumps(dict(status=report['status'],report=str(path),replayed=False,
                reason='Existing evaluation retained; no automatic retry or report replacement.')))
            return
        if (report['status']!='FAILED' or report.get('usage_status')!='REPORTED'
            or len(report.get('paid_attempts',[]))!=1 or report['paid_attempts'][0]['status']!='SETTLED'
            or len(report.get('paid_usage',[]))!=1 or 'last_raw_result' not in report):
            raise ValueError('ONLY_KNOWN_SETTLED_FIRST_BATCH_CAN_CONTINUE')
        targets,_=next(batches(sample))
        flagged=validate_batch_diagnostic(report['last_raw_result'],targets,sample['request']['sources'])
        if not any(v['validation_status']=='INVALID_EVIDENCE' for v in flagged):
            raise ValueError('EXPECTED_FIRST_BATCH_EVIDENCE_FLAG_REQUIRED')
        parent=report
        report_id=str(uuid5(UUID(sample['evaluation_id']),'continue-independent-batches-1'))
        path=directory/('fact-judge-'+report_id+'.json')
        if path.exists():
            existing=json.loads(path.read_text(encoding='utf-8'))
            clean={k:v for k,v in existing.items() if k!='report_digest'}
            if existing.get('report_digest')!=fingerprint('FACT_JUDGE_REPORT',json.dumps(clean,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':'))):
                raise ValueError('FACT_JUDGE_CONTINUATION_DIGEST_MISMATCH')
            print(json.dumps(dict(status=existing['status'],report=str(path),replayed=False)))
            return
    elif args.continue_independent:
        raise ValueError('KNOWN_SETTLED_PARENT_REPORT_REQUIRED')
    prepared=directory/('fact-judge-sample-'+sample['evaluation_id']+'.json')
    prepared.write_text(json.dumps(sample,indent=2,ensure_ascii=False),encoding='utf-8')
    if not args.run:
        print(json.dumps(dict(status='PREPARED_NOT_SCORED',targets=36,batches=3,maximum_paid_requests=3,
            sample=str(prepared),provider_calls=0,human_verification_changed=False)))
        return
    from deal_or_no_deal_ai.evaluation_transport import EvaluationTransport
    transport=EvaluationTransport(ROOT,sample['evaluation_id'],sample['scope'])
    logical_calls=0
    def judge(prompt,schema):
        nonlocal logical_calls
        logical_calls+=1
        if parent and logical_calls==1:
            attempt=parent['paid_attempts'][0]['operation_id']
            request=transport.store.get_record('evaluation-paid-request:'+attempt)
            result=transport.store.get_record('evaluation-paid-result:'+attempt)
            if request is None or result is None or request[1]['payload']['messages'][1]['content']!=prompt:
                raise ValueError('EXACT_SETTLED_FIRST_BATCH_REQUIRED')
            response=json.loads(result[1]['response_json'])
            raw=json.loads(response['choices'][0]['message']['content'])
            if raw!=parent['last_raw_result'] or response['choices'][0]['finish_reason']!='stop':
                raise ValueError('ORIGINAL_FIRST_BATCH_CHANGED')
            transport.receipts.append({**parent['paid_usage'][0],'cached':True})
            return raw
        if logical_calls>3 or (parent and len(transport.attempts)>=2):
            raise ValueError('THREE_TOTAL_FACT_JUDGE_REQUESTS_EXHAUSTED')
        return transport.judge(prompt,schema)
    def save(report):
        uncertain=any(a['status']=='UNKNOWN' for a in transport.attempts)
        report.update(version='FACT-JUDGE-REPORT-1.0',evaluated_at_utc=datetime.now(timezone.utc).isoformat(),
            evaluation_id=report_id,parent_report=None if parent is None else parent['evaluation_id'],
            paid_attempts=transport.attempts,paid_usage=transport.receipts,
            cost_usd=None if uncertain else str(sum((Decimal(r['cost_usd']) for r in transport.receipts if not r['cached']),Decimal(0))),
            total_judging_cost_usd=None if uncertain else str(sum((Decimal(r['cost_usd']) for r in transport.receipts),Decimal(0))),
            usage_status='UNKNOWN_REQUIRES_RECONCILIATION' if uncertain else 'REPORTED',
            human_verification_changed=False,credit_decision_recorded=False)
        clean={k:v for k,v in report.items() if k!='report_digest'}
        report['report_digest']=fingerprint('FACT_JUDGE_REPORT',json.dumps(clean,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')))
        temp=path.with_suffix('.tmp')
        temp.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
        temp.replace(path)
        if 'counts' in report:
            path.with_suffix('.md').write_text(markdown(report),encoding='utf-8')
    save(dict(status='IN_PROGRESS',evaluation_id=sample['evaluation_id'],sample=sample,results=[],
              batches_completed=0,judge_invocations=0,grants_human_support=False))
    report=run(sample,judge,checkpoint=save,retain_invalid_evidence=parent is not None)
    print(json.dumps(dict(status=report['status'],counts=report['counts'],paid_requests=len(transport.attempts),
        cost_usd=report['cost_usd'],total_judging_cost_usd=report['total_judging_cost_usd'],report=str(path),markdown=str(path.with_suffix('.md')),
        human_verification_changed=False,native_ragas_metrics='NOT_RUN_CUSTOM_FACT_JUDGE_ONLY')))


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps(dict(status='BLOCKED',error_type=type(error).__name__,
            reason='Current scoped facts, source bindings or verified evaluator setup were unavailable; no automatic retry.')))
        raise SystemExit(1)
