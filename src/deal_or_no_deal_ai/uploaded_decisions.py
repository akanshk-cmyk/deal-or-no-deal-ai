"""Explicit post-analysis human actions; original live draft/checkpoints unchanged."""
from pathlib import Path
from uuid import UUID
from datetime import datetime,timezone
from dataclasses import asdict
from typing import Literal
from pydantic import Field
from .contracts import StrictModel,Identifier,Text,parse_extraction
from .context import InputError,fingerprint,primitive
from .storage import Store,RecordWrite,StaleRecord,OperationConflict
from .configuration import load_configuration
from .readiness_service import assess_current,require_approval,key as readiness_key


class UploadedDecisionCommand(StrictModel):
    operation_id: Identifier
    expected_version: int=Field(ge=0)
    expected_readiness_version: int=Field(ge=0)
    expected_analysis: Text
    expected_readiness_digest: Text
    action: Literal['APPROVE','REJECT','REQUEST_INFORMATION','ADD_COMMENT','INFORMATION_RESPONSE']
    comments: Text=Field(max_length=4096)
    requested_items: list[Text]=Field(default_factory=list,max_length=30)
    reviewed_items: list[Text]=Field(default_factory=list,max_length=30)
    quotes: dict[str,Text]=Field(default_factory=dict,max_length=64)
    demo_override: bool=False


def demo_override_available(assessment):
    """Educational human exception only; never clears or changes readiness."""
    data=assessment.model_dump() if hasattr(assessment,'model_dump') else assessment
    blockers=set(data['blockers'])
    checks=[r for r in data['evaluated_requirements'] if r['requirement_id'] in blockers]
    return data['outcome']=='Pending Review' and bool(blockers) and len(checks)==len(blockers) and all(r['status']=='PENDING' for r in checks)


def record_action(root,actor,operation,command):
    from .command_center import get_run,source_packet
    root=Path(root);store=Store(load_configuration(root).database)
    command=UploadedDecisionCommand.model_validate(command.model_dump())
    if str(UUID(command.operation_id))!=command.operation_id:raise InputError('CANONICAL_OPERATION_UUID_REQUIRED')
    run=get_run(store,actor,operation)
    if not run['context'].get('upload_origin') or run['status']!='COMPLETED':
        raise InputError('COMPLETED_UPLOADED_DEMO_REQUIRED')
    digest=fingerprint('UPLOADED_DECISION_COMMAND',dict(command=command.model_dump(),actor=primitive(asdict(actor)),operation=operation))
    event_key='uploaded-decision-event:'+command.operation_id
    previous=store.get_record(event_key)
    if previous:
        if previous[1]['command_digest']!=digest:raise OperationConflict('DECISION_COMMAND_CONFLICT')
        return previous[1]
    if not command.comments.strip():raise InputError('DECISION_COMMENTS_REQUIRED')
    pointer_key='readiness-human:'+run['context']['scope']['run_id']
    prior=store.get_record(pointer_key);old=prior[1] if prior else None
    if (prior[0] if prior else 0)!=command.expected_version:raise StaleRecord('STALE_HUMAN_REVIEW')
    a=assess_current(store,run['context'],run['artifacts'])
    if (command.expected_analysis,command.expected_readiness_version,command.expected_readiness_digest)!=(a.analysis_digest,a.version,a.assessment_digest):
        raise StaleRecord('STALE_REVIEW_ANALYSIS')
    packet=source_packet(root,run)
    sources={k:v['text'] for k,v in packet['request']['reference_dictionary'].items() if v['kind']=='SOURCE'}
    action=command.action
    if command.demo_override and action!='APPROVE':raise InputError('DEMO_OVERRIDE_APPROVAL_ONLY')
    if action in ('APPROVE','REJECT') and (actor.persona!='AuthorizedApprover' or 'NORMAL' not in actor.allowed_review_tiers):
        raise InputError('AUTHORIZED_APPROVER_REQUIRED')
    if action=='REQUEST_INFORMATION' and actor.persona not in ('Analyst','RiskManager','ComplianceOfficer','AuthorizedApprover'):
        raise InputError('REVIEWER_ROLE_REQUIRED')
    if old and old['decision'] in ('Approve','Reject') and action!='ADD_COMMENT':
        raise InputError('FINAL_DECISION_ALREADY_RECORDED')
    if action=='REQUEST_INFORMATION' and (not command.requested_items or any(not v.strip() for v in command.requested_items) or len(set(command.requested_items))!=len(command.requested_items)):
        raise InputError('SPECIFIC_INFORMATION_ITEMS_REQUIRED')
    if action=='INFORMATION_RESPONSE':
        if actor.persona!='RiskManager' or not old or old['decision']!='Pending Information':raise InputError('PENDING_RISK_MANAGER_REVIEW_REQUIRED')
        if set(command.reviewed_items)!=set(old['requested_items']) or len(command.reviewed_items)!=len(set(command.reviewed_items)):
            raise InputError('EVERY_REQUESTED_ITEM_REQUIRES_REVIEW')
        if not command.quotes or any(ref not in sources or not quote.strip() or quote not in sources[ref] for ref,quote in command.quotes.items()):
            raise InputError('SOURCE_SUPPORTED_RESPONSE_REVIEW_REQUIRED')
    readiness_pointer=store.get_record(readiness_key(run['context']['scope']['run_id']))
    if action=='APPROVE':
        if old and old['decision']=='Pending Information':raise InputError('OUTSTANDING_INFORMATION_REQUEST')
        if command.demo_override:
            if not demo_override_available(a):raise InputError('PENDING_ONLY_DEMO_OVERRIDE_REQUIRED')
        else:
            readiness_pointer=require_approval(store,run,a.version,a.assessment_digest)
    decisions=dict(APPROVE='Approve',REJECT='Reject',REQUEST_INFORMATION='Pending Information',INFORMATION_RESPONSE='Under Review')
    statuses=dict(APPROVE='APPROVED',REJECT='REJECTED',REQUEST_INFORMATION='PENDING_INFORMATION',INFORMATION_RESPONSE='AWAITING_DECISION')
    before=old['new_status'] if old else 'AWAITING_DECISION'
    terms=parse_extraction(run['artifacts']['extractor']['payload']['wire_json']).terms
    event=dict(operation_id=command.operation_id,scope=run['context']['scope'],run_operation=operation,command_digest=digest,
        action=action,decision=decisions.get(action),previous_status=before,new_status=statuses.get(action,before),
        comments=command.comments,requested_items=list(dict.fromkeys((old['requested_items'] if old and old['decision']=='Pending Information' and action=='REQUEST_INFORMATION' else [])+command.requested_items)),reviewed_items=command.reviewed_items,quotes=command.quotes,
        reviewer_role=actor.persona,reviewer_name='Simulated '+actor.persona,reviewer_tier='NORMAL' if actor.persona=='AuthorizedApprover' else None,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),ai_proposal=run['ai_proposal'],approval_readiness=a.model_dump(),analysis_digest=a.analysis_digest,
        provenance='LIVE_ANALYSIS_HUMAN_REVIEW',analysis_snapshot=dict(deal=dict(deal_id=run['context']['scope']['deal_id'],borrower=terms.borrower.value,amount=terms.requested_amount.value,currency=terms.currency.value,deal_type=terms.facility_type.value),
            ai=run['artifacts']['synthesizer']['payload'],risk=run['artifacts']['risk_quantifier']['payload'],compliance=run['artifacts']['route_review']['payload']['final_policy'],source_dependency=run['context']['source_binding']))
    if command.demo_override:
        event.update(demo_override=True,unresolved_requirement_ids=list(a.blockers),reviewer_comments=command.comments)
        event['comments']='EDUCATIONAL APPROVAL OVERRIDE: readiness remains '+a.outcome+'; mandatory checks are not cleared. Reviewer reason: '+command.comments
    writes=[RecordWrite(event_key,'UPLOADED_DECISION_EVENT',event,0),RecordWrite('financial-review-event:'+command.operation_id,'FINANCIAL_REVIEW_EVENT',event,0)]
    if action!='ADD_COMMENT':writes.append(RecordWrite(pointer_key,'READINESS_HUMAN_DECISION',event,prior[0] if prior else 0))
    receipt=store.admit(command.operation_id,run['context']['scope'],dict(action='UPLOADED_HUMAN_REVIEW',digest=digest),writes=tuple(writes),
        expected_records=((pointer_key,prior[0] if prior else 0),(readiness_key(run['context']['scope']['run_id']),readiness_pointer[0] if readiness_pointer else 0)))
    if not receipt.duplicate:store.release(receipt,confirmed_idle=True)
    return event


def memo_with_review_history(root,actor,operation):
    """Read-only export; never rewrite the original draft or claim it was verified."""
    from .command_center import get_run,source_packet
    from .financial_review import financial_history
    from .memo import inert
    store=Store(load_configuration(Path(root)).database);run=get_run(store,actor,operation)
    if not run['context'].get('upload_origin') or run['status']!='COMPLETED':raise InputError('COMPLETED_UPLOADED_DEMO_REQUIRED')
    source_packet(Path(root),run)
    events=[e for e in financial_history(store,actor,run['context']['scope']['deal_id']) if e['run_operation']==operation]
    text=run['outcome']['report_markdown']+'\n\n# Subsequent human review history\n\nThe original draft above is preserved as generated. The following separately recorded actions do not retroactively verify its statements.\n\n'
    for e in events:
        text+='- '+inert(e['timestamp_utc'])+' | '+inert(e['reviewer_name'])+' | '+inert(e['action'])+' | '+inert(e['new_status'])+'\n\n'+inert(e['comments'])+'\n\n'
    return text
