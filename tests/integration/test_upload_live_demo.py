"""Actual uploaded PDF parsing and graph/UI integration; provider responses mocked."""
from dataclasses import replace
from unittest.mock import patch

from deal_or_no_deal_ai.upload_intake import inspect_package
from deal_or_no_deal_ai.upload_live import load_uploaded_case,run_uploaded,identities
from deal_or_no_deal_ai.context import InputError,strict_json
from deal_or_no_deal_ai.command_center import get_run,source_packet
from tests.integration import test_live_demo as demo_support
from tests.integration.test_human_review_ui import widget
from tests.support import uid


class UploadLiveTests(demo_support.LiveDemoTests):
    def verify_upload_pause(self,state,actor):
        from deal_or_no_deal_ai.live_review import request_key,Assessment,required_checks,assess
        stage=state['pending_stage'];request=self.store.get_record(request_key(state['context']['scope']['run_id'],stage))[1]
        for target in request['targets']:
            for domain in target['domains']:
                reviewer=replace(actor,persona='RiskManager' if domain=='FINANCIAL_RISK' else 'ComplianceOfficer')
                assess(self.root,reviewer,state['context']['scope']['run_id'],stage,Assessment(operation_id=uid(stage+target['id']+domain),request_digest=request['digest'],target_id=target['id'],target_digest=target['digest'],domain=domain,status='HUMAN_SUPPORTED',quotes={r:request['sources'][r] for r in target['source_refs']},checks=list(required_checks(stage)),comments='Offline synthetic reviewer explicitly checked this test target.'))

    def finish_upload(self,state,actor):
        from deal_or_no_deal_ai.live_demo import run_demo
        for i in range(2):
            if state['status']=='WAITING_EVIDENCE':
                self.verify_upload_pause(state,actor)
                state=run_demo(self.root,actor,state['context']['operation_id'],resume_operation_id=uid('upload-verified-resume-'+str(i)))
        return state

    def prepare_upload(self,partial=False):
        operation=uid('new-uploaded-standard-deal')
        pack=self.root/'fixtures/development/e-n01'
        manifest=strict_json((pack/'manifest.json').read_bytes())
        files=[('renamed-'+str(i)+'.pdf',(pack/s['path']).read_bytes()) for i,s in enumerate(manifest['sources'])]
        package=inspect_package(self.root,self.actor(),operation,files[:1] if partial else list(reversed(files)),synthetic_confirmed=True)
        actor=replace(self.actor(),allowed_deal_ids=frozenset({identities(operation)['deal_id']}))
        return operation,package,actor

    def test_uploaded_live_new_identity_citations_and_memo(self):
        operation,package,actor=self.prepare_upload()
        case,origin=load_uploaded_case(self.root,actor,operation)
        self.assertNotEqual(case.scope.deal_id,self.deal)
        with patch('deal_or_no_deal_ai.worker.run_normal_fixture',side_effect=AssertionError('NO_SAVED_REVIEW')):
            result=run_uploaded(self.root,actor,operation)
            self.assertEqual(result['pending_stage'],'fact_review')
            result=self.finish_upload(result,actor)
        self.assertEqual(result['status'],'COMPLETED')
        self.assertEqual(result['context']['scope']['deal_id'],case.scope.deal_id)
        self.assertEqual(result['report_metadata']['scope']['deal_id'],case.scope.deal_id)
        self.assertEqual(result['context']['upload_origin']['package_digest'],package['package_digest'])
        from deal_or_no_deal_ai.memo import inert
        self.assertIn(inert(package['package_id']),result['report_markdown'])
        self.assertIn(inert(case.scope.deal_id),result['report_markdown'])
        self.assertFalse(result['approval_readiness']['approval_eligible'])
        packet=source_packet(self.root,get_run(self.store,actor,identities(operation)['operation_id']))
        self.assertTrue(packet['request']['reference_dictionary'])
        run_uploaded(self.root,actor,operation)
        self.assertEqual(self.post.call_count,2)
        with self.assertRaises(InputError):run_uploaded(self.root,self.actor(),operation)
        with self.assertRaises(InputError):run_uploaded(self.root,replace(actor,persona='RiskManager'),operation)
        source=package['sources'][0]
        path=self.root/'var/uploads'/actor.workspace_id/package['package_id']/(source['sha256']+'.pdf')
        path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaises(InputError):run_uploaded(self.root,actor,operation)
        self.assertEqual(self.post.call_count,2)
        from deal_or_no_deal_ai.live_worker import load_live,list_live
        retained=load_live(self.root,actor,identities(operation)['operation_id'])
        self.assertEqual(retained['status'],'RECOVERY_REQUIRED')
        self.assertTrue(retained['source_validation_failed'])
        self.assertTrue(any(s['context']['operation_id']==identities(operation)['operation_id'] for s in list_live(self.root,actor)))

    def test_uploaded_partial_package_never_dispatches(self):
        operation,package,actor=self.prepare_upload(partial=True)
        with self.assertRaisesRegex(InputError,'COMPLETE_STANDARD_DEAL'):
            run_uploaded(self.root,actor,operation)
        self.assertEqual(self.post.call_count,0)

    def test_uploaded_ui_run_and_existing_screens(self):
        from deal_or_no_deal_ai.worker import run_normal_fixture
        run_normal_fixture(self.root,uid('existing-standard-before-upload'))
        operation,package,actor=self.prepare_upload()
        from tests.integration.test_command_center import CommandCenterTests
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,'Page').set_value('New Deal').run()
        widget(app.radio,'Intake mode').set_value('Upload New Deal').run()
        self.assertEqual(len(app.exception),0)
        self.assertFalse(widget(app.button,'Run AI Deal Review').disabled)
        widget(app.button,'Run AI Deal Review').click().run(timeout=180)
        self.assertEqual(len(app.exception),0)
        state=self.store.get_record('live-progress:'+identities(operation)['operation_id'])[1]
        self.assertEqual(state['pending_stage'],'fact_review')
        self.finish_upload(state,actor)
        for page in ('Review Workspace','Agent Activity','Credit Memo','Decision History','Deal Dashboard'):
            widget(app.sidebar.radio,'Page').set_value(page).run(timeout=90)
            self.assertEqual(len(app.exception),0)
            self.assertEqual(app.session_state['selected_financial_operation'],identities(operation)['operation_id'])
            if page=='Review Workspace':
                self.assertTrue(any(e.label=='Evidence reference' for e in app.selectbox))
        self.assertEqual(self.post.call_count,2)
