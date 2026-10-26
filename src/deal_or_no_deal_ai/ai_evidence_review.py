"""Explicit AI-assisted review metadata, never a human support receipt."""
from pathlib import Path
from datetime import datetime,timezone
from .context import InputError,fingerprint,strict_json
from .configuration import load_configuration
from .storage import Store,RecordWrite
from .live_review import request_key,verify_request


def key(request):return 'live-ai-review:'+request['digest']


def record(root,actor,operation,request_digest,assessments):
    from .command_center import get_run
    from .upload_live import case_for_context
    root=Path(root);store=Store(load_configuration(root).database)
    run=get_run(store,actor,operation)
    if run['status']!='WAITING_EVIDENCE' or run['outcome']['pending_stage']!='fact_review':raise InputError('CURRENT_FACT_REVIEW_REQUIRED')
    case_for_context(root,actor,run['context'])
    saved=store.get_record(request_key(run['context']['scope']['run_id'],'fact_review'))
    request=saved[1];verify_request(request)
    if request['digest']!=request_digest:raise InputError('AI_REVIEW_STALE_REQUEST')
    targets={t['id']:t for t in request['targets']};seen=set()
    for item in assessments:
        t=targets.get(item.get('target_id'));pair=(item.get('target_id'),item.get('domain'))
        if not t or pair in seen or item.get('target_digest')!=t['digest'] or item.get('domain') not in t['domains']:raise InputError('AI_REVIEW_TARGET_MISMATCH')
        seen.add(pair)
        if item.get('status') not in ('AI_SUPPORTED','AI_FLAGGED','AI_NEEDS_INFORMATION') or not item.get('reason','').strip():raise InputError('AI_REVIEW_STATUS_OR_REASON_REQUIRED')
        quotes=item.get('quotes',{})
        if not quotes or any(ref not in t['source_refs'] or not quote.strip() or quote not in request['sources'][ref] for ref,quote in quotes.items()):raise InputError('AI_REVIEW_EXACT_SOURCE_REQUIRED')
        if item['status']=='AI_SUPPORTED' and set(quotes)!=set(t['source_refs']):raise InputError('AI_REVIEW_ALL_REFERENCES_REQUIRED')
    body=dict(scope=request['scope'],operation_id=operation,request_digest=request_digest,source_binding=request['source_binding'],
        reviewer_type='AI_ASSISTANT',reviewer_name='Codex',method='SOURCE_REVIEW_NOT_INDEPENDENT_EVALUATION',
        human_supported=False,credit_approval=False,assessments=assessments)
    body['assessment_digest']=fingerprint('AI_EVIDENCE_REVIEW',body)
    with store.transaction() as connection:
        current=connection.execute('SELECT version FROM app_records WHERE record_key=?',(request_key(run['context']['scope']['run_id'],'fact_review'),)).fetchone()
        progress=connection.execute('SELECT payload FROM app_records WHERE record_key=?',('live-progress:'+operation,)).fetchone()
        state=strict_json(progress[0],envelope=True) if progress else {}
        if not current or current[0]!=saved[0] or state.get('status')!='WAITING_EVIDENCE' or state.get('pending_stage')!='fact_review':raise InputError('AI_REVIEW_STALE_PAUSE')
        prior=connection.execute('SELECT payload FROM app_records WHERE record_key=?',(key(request),)).fetchone()
        if prior:
            result=strict_json(prior[0],envelope=True)
            if result['assessment_digest']!=body['assessment_digest']:raise InputError('AI_REVIEW_ALREADY_RECORDED')
            return result
        body['timestamp_utc']=datetime.now(timezone.utc).isoformat()
        store._write(connection,RecordWrite(key(request),'AI_EVIDENCE_REVIEW',body,0))
    return body
