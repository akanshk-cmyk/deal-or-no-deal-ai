"""Post-live human actions with offline provider mocks and original draft preservation."""
from dataclasses import replace
from unittest.mock import patch
from uuid import uuid4
from tests.integration import test_upload_live_demo as support
from tests.integration.test_human_review_ui import widget
from deal_or_no_deal_ai.upload_live import run_uploaded,identities
from deal_or_no_deal_ai.command_center import get_run,source_packet
from deal_or_no_deal_ai.uploaded_decisions import UploadedDecisionCommand,record_action
from deal_or_no_deal_ai.storage import StaleRecord
from deal_or_no_deal_ai.context import InputError


class UploadedHumanTests(support.UploadLiveTests):
    def test_human_pending_demo_override_is_explicit_authorized_and_preserves_readiness(self):
        self.prepare_human()
        run=get_run(self.store,self.hactor,self.hop)
        self.assertEqual(run['approval_readiness']['outcome'],'Pending Review')
        with self.assertRaises(InputError):record_action(self.root,self.hactor,self.hop,self.cmd('APPROVE',demo_override=True))
        with self.assertRaises(InputError):record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,self.cmd('APPROVE'))
        command=self.cmd('APPROVE',demo_override=True)
        event=record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,command)
        self.assertTrue(event['demo_override'])
        self.assertEqual(event['decision'],'Approve')
        self.assertFalse(event['approval_readiness']['approval_eligible'])
        self.assertEqual(event['approval_readiness']['outcome'],'Pending Review')
        self.assertTrue(event['unresolved_requirement_ids'])
        self.assertIn('EDUCATIONAL APPROVAL OVERRIDE',event['comments'])
        self.assertEqual(record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,command),event)
        self.assertEqual(self.store.get_record('live-progress:'+self.hop)[1]['report_markdown'],self.original['report_markdown'])
        from deal_or_no_deal_ai.uploaded_decisions import memo_with_review_history
        self.assertIn('EDUCATIONAL APPROVAL OVERRIDE',memo_with_review_history(self.root,self.hactor,self.hop))

    def prepare_human(self):
        upload,package,actor=self.prepare_upload()
        self.hactor=actor;self.hop=identities(upload)['operation_id']
        self.original=self.finish_upload(run_uploaded(self.root,actor,upload),actor)
        return self.hop

    def hrole(self,role):
        return replace(self.hactor,persona=role,allowed_review_tiers=frozenset({'NORMAL'}) if role=='AuthorizedApprover' else frozenset())

    def cmd(self,action,**extra):
        run=get_run(self.store,self.hactor,self.hop);a=run['approval_readiness']
        prior=self.store.get_record('readiness-human:'+run['context']['scope']['run_id'])
        return UploadedDecisionCommand(operation_id=str(uuid4()),expected_version=prior[0] if prior else 0,
            expected_readiness_version=a['version'],expected_readiness_digest=a['assessment_digest'],expected_analysis=a['analysis_digest'],
            action=action,comments='Synthetic reviewer explanation.',**extra)

    def test_human_pending_comments_response_reject_and_history(self):
        self.prepare_human()
        with self.assertRaises(InputError):record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,self.cmd('APPROVE'))
        with self.assertRaises(InputError):record_action(self.root,self.hactor,self.hop,self.cmd('REJECT'))
        stale=self.cmd('REJECT')
        comment=self.cmd('ADD_COMMENT');event=record_action(self.root,self.hactor,self.hop,comment)
        self.assertEqual(record_action(self.root,self.hactor,self.hop,comment),event)
        pending=self.cmd('REQUEST_INFORMATION',requested_items=['Clarify the annual reporting obligation'])
        record_action(self.root,self.hactor,self.hop,pending)
        with self.assertRaises(StaleRecord):record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,stale)
        with self.assertRaises(InputError):record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,self.cmd('APPROVE'))
        run=get_run(self.store,self.hactor,self.hop)
        self.assertEqual(run['human_disposition'],'Pending Information')
        refs=source_packet(self.root,run)['request']['reference_dictionary']
        from deal_or_no_deal_ai.readiness_service import evidence_targets
        self.assertTrue(any(t.startswith('policy.') for t in evidence_targets(run['artifacts'],'POLICY_CONTROL')))
        response=self.cmd('INFORMATION_RESPONSE',reviewed_items=pending.requested_items,quotes={'AGREEMENT-P1':refs['AGREEMENT-P1']['text'][:100]})
        with self.assertRaises(InputError):record_action(self.root,self.hactor,self.hop,response)
        record_action(self.root,self.hrole('RiskManager'),self.hop,response)
        reject=self.cmd('REJECT');event=record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,reject)
        self.assertEqual(event['new_status'],'REJECTED')
        with self.assertRaises(InputError):record_action(self.root,self.hactor,self.hop,self.cmd('REQUEST_INFORMATION',requested_items=['New request']))
        self.assertEqual(get_run(self.store,self.hactor,self.hop)['human_disposition'],'Reject')
        self.assertEqual(self.store.get_record('live-progress:'+self.hop)[1]['report_markdown'],self.original['report_markdown'])
        from deal_or_no_deal_ai.financial_review import financial_history
        self.assertEqual(len(financial_history(self.store,self.hactor)),4)
        from deal_or_no_deal_ai.uploaded_decisions import memo_with_review_history
        export=memo_with_review_history(self.root,self.hactor,self.hop)
        self.assertIn('Subsequent human review history',export)
        self.assertTrue(export.startswith(self.original['report_markdown']))
        self.assertEqual(self.post.call_count,2)

    def test_human_controlled_ready_approval_requires_latest_version_and_role(self):
        self.prepare_human()
        # Controlled ready-requirements test only; does not assert Standard Deal's unknown timing is resolved.
        from tests.unit.test_readiness import ready_inputs
        from deal_or_no_deal_ai.readiness_service import assess_current,basis
        run=get_run(self.store,self.hactor,self.hop);data=ready_inputs()
        for k in ('version','evaluated_at_utc'):data.pop(k)
        data.update(scope=run['context']['scope'],analysis_digest=basis(run['context'],run['artifacts']))
        with patch('deal_or_no_deal_ai.readiness_service.inputs',return_value=data):
            receipt=self.store.admit(str(uuid4()),run['context']['scope'],dict(action='CONTROLLED_READY_TEST'))
            assess_current(self.store,run['context'],run['artifacts'],receipt);self.store.release(receipt,confirmed_idle=True)
            command=self.cmd('APPROVE')
            with self.assertRaises(InputError):record_action(self.root,self.hactor,self.hop,command)
            event=record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,command)
            self.assertEqual(event['decision'],'Approve');self.assertTrue(event['approval_readiness']['approval_eligible'])
            self.assertEqual(record_action(self.root,self.hrole('AuthorizedApprover'),self.hop,command),event)

    def test_human_ui_controls_comment_pending_and_same_deal_history(self):
        self.prepare_human()
        from tests.integration.test_command_center import CommandCenterTests
        app=CommandCenterTests.app(self)
        app.session_state.selected_financial_operation=self.hop
        widget(app.sidebar.radio,'Page').set_value('Review Workspace').run(timeout=120)
        self.assertEqual(len(app.exception),0)
        self.assertTrue(widget(app.button,'Approve').disabled)
        self.assertTrue(widget(app.button,'Reject').disabled)
        widget(app.sidebar.selectbox,'Demo role').select('AuthorizedApprover').run(timeout=120)
        self.assertFalse(widget(app.button,'Approve').disabled)
        self.assertFalse(widget(app.checkbox,'I acknowledge the unresolved checks and approve as an educational demo override').value)
        widget(app.sidebar.selectbox,'Demo role').select('Analyst').run(timeout=120)
        widget(app.text_area,'Deal review comments (required)').set_value('Need clarification on annual reporting.')
        widget(app.text_area,'Requested information — one item per line').set_value('Clarify reporting timing')
        widget(app.button,'Mark Pending').click().run(timeout=120)
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any('Pending Information' in e.value for e in app.markdown))
        widget(app.sidebar.selectbox,'Demo role').select('AuthorizedApprover').run(timeout=120)
        self.assertTrue(widget(app.button,'Approve').disabled)
        self.assertFalse(widget(app.button,'Reject').disabled)
        for page in ('Decision History','Credit Memo','Deal Dashboard'):
            widget(app.sidebar.radio,'Page').set_value(page).run(timeout=120)
            self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,2)
