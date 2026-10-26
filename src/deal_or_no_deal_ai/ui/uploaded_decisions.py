"""Shared Human Review controls for completed uploaded live drafts."""
from uuid import uuid4
import sqlite3
from ..context import InputError
from ..uploaded_decisions import UploadedDecisionCommand,record_action,demo_override_available
from ..storage import StaleRecord,OperationConflict,RunBusy


def render(st,root,actor,store,state):
    from ..command_center import get_run,source_packet
    from .readiness import _evaluate
    run=get_run(store,actor,state['context']['operation_id'])
    a=run['approval_readiness'];scope=run['context']['scope']
    pointer=store.get_record('readiness-human:'+scope['run_id']);human=pointer[1] if pointer else None
    final=bool(human and human['decision'] in ('Approve','Reject'))
    pending=bool(human and human['decision']=='Pending Information')
    approver=actor.persona=='AuthorizedApprover' and 'NORMAL' in actor.allowed_review_tiers
    override_available=demo_override_available(a) and not pending and not final
    st.subheader('Human deal review')
    st.caption('Simulated role permissions apply. Verifying evidence, AI recommendations and human credit decisions are separate records.')
    st.write('**Current human status:** '+(human['decision'] if human else 'Not recorded'))
    if human:
        st.caption(human['reviewer_name']+' · '+human['timestamp_utc']);st.text(human['comments'])
        if human.get('demo_override'):st.warning('Educational approval override recorded. AI readiness remains Pending Review; outstanding requirements were not verified or waived.')
    if not final:
        with st.expander('Verify evidence and covenant checks'):
            _evaluate(st,run,store,root,actor)
    if not a['approval_eligible'] and not final:
        if override_available:
            st.warning('Readiness remains Pending Review: '+a['reason']+'. An Authorized Approver may record an educational approval override with a reason and explicit acknowledgment. This does not clear the outstanding checks.')
        else:st.info('Approve is unavailable: '+a['reason']+'. Complete the source-supported readiness checks; a Low score cannot clear them.')
    if not approver:
        st.caption('Approve and Reject require simulated Authorized Approver with normal review permission.')
    if pending:
        st.warning('Additional information is outstanding. A Risk Manager must review every requested item before approval can be considered.')
        for item in human['requested_items']:st.write('- '+item)
    with st.form('uploaded-human-actions:'+scope['run_id']):
        comments=st.text_area('Deal review comments (required)',key='uploaded-comments:'+scope['run_id'])
        requested=st.text_area('Requested information — one item per line',key='uploaded-request:'+scope['run_id'])
        confirmed=st.checkbox('I confirm this simulated credit decision',key='uploaded-confirm:'+scope['run_id'])
        override=st.checkbox('I acknowledge the unresolved checks and approve as an educational demo override',key='uploaded-override:'+scope['run_id']) if override_available and approver else False
        cols=st.columns(4)
        approve=cols[0].form_submit_button('Approve',disabled=not approver or final or pending or not (a['approval_eligible'] or override_available))
        reject=cols[1].form_submit_button('Reject',disabled=not approver or final)
        request=cols[2].form_submit_button('Mark Pending',disabled=final or actor.persona=='Administrator')
        comment=cols[3].form_submit_button('Add Comment')
    action='APPROVE' if approve else 'REJECT' if reject else 'REQUEST_INFORMATION' if request else 'ADD_COMMENT' if comment else None
    def save(action,comments,**extra):
        try:
            record_action(root,actor,run['operation_id'],UploadedDecisionCommand(operation_id=str(uuid4()),expected_version=pointer[0] if pointer else 0,
                expected_readiness_version=a['version'],expected_readiness_digest=a['assessment_digest'],expected_analysis=a['analysis_digest'],action=action,comments=comments,**extra))
        except (InputError,ValueError,OSError,sqlite3.Error,StaleRecord,OperationConflict,RunBusy):
            st.error('Not recorded. Check comments, current review version, role, source evidence and required checks. Refresh before trying again.')
        else:st.rerun()
    if action:
        if action in ('APPROVE','REJECT') and not confirmed:st.error('Confirm the simulated credit decision before submitting.')
        elif action=='APPROVE' and not a['approval_eligible'] and not override:st.error('Acknowledge the educational override or complete the outstanding readiness checks before approving.')
        else:save(action,comments,demo_override=bool(action=='APPROVE' and override and not a['approval_eligible']),requested_items=[s.strip() for s in requested.splitlines() if s.strip()] if action=='REQUEST_INFORMATION' else [])
    if pending and actor.persona=='RiskManager':
        with st.expander('Review the requested information'):
            packet=source_packet(root,run)
            sources={k:v['text'] for k,v in packet['request']['reference_dictionary'].items() if v['kind']=='SOURCE'}
            with st.form('uploaded-information-response:'+scope['run_id']):
                reviewed=[item for item in human['requested_items'] if st.checkbox('Reviewed: '+item)]
                quotes={ref:st.text_area('Response evidence quote from '+ref) for ref in sources}
                reason=st.text_area('Information review comments (required)')
                returned=st.form_submit_button('Return to Review')
            if returned:save('INFORMATION_RESPONSE',reason,reviewed_items=reviewed,quotes={k:v for k,v in quotes.items() if v.strip()})
    st.caption('The original draft memo remains unchanged. Decisions and comments are recorded separately with UTC timestamps in Decision History.')
    from ..financial_review import financial_history
    events=[e for e in financial_history(store,actor,scope['deal_id']) if e['run_operation']==run['operation_id']]
    if events:
        with st.expander('Review comments and actions',expanded=True):
            for e in events:
                st.write(e['timestamp_utc']+' · '+e['reviewer_name']+' · '+e['action'].replace('_',' ').title())
                st.text(e['comments'])
