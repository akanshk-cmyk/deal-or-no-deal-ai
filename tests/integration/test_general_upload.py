"""New PDF contents, explicit profiles, true graph branches and human interrupts."""
import json,threading
from dataclasses import replace
from unittest.mock import patch
from tests.integration import test_upload_live_demo as support
from tests.support import uid
from deal_or_no_deal_ai.upload_intake import inspect_package
from deal_or_no_deal_ai.upload_live import identities,run_uploaded,load_uploaded_case
from deal_or_no_deal_ai.upload_profile import UploadProfile,save_profile
from deal_or_no_deal_ai.services import _expected_basis
from deal_or_no_deal_ai.context import InputError


class GeneralUploadTests(support.UploadLiveTests):
    def test_general_ai_review_is_separate_and_cannot_clear_human_gate(self):
        from deal_or_no_deal_ai.ai_evidence_review import record
        from deal_or_no_deal_ai.live_review import request_key,supported
        operation,actor,case=self.prepare_new_deal()
        state=run_uploaded(self.root,actor,operation);review=state['context']['operation_id']
        before=self.store.get_record('live-progress:'+review)
        request=self.store.get_record(request_key(state['context']['scope']['run_id'],'fact_review'))[1]
        target=request['targets'][0]
        item=dict(target_id=target['id'],target_digest=target['digest'],domain=target['domains'][0],status='AI_SUPPORTED',reason='Synthetic AI review of the supplied borrower statement only.',quotes={r:request['sources'][r] for r in target['source_refs']})
        with self.assertRaises(InputError):record(self.root,actor,review,request['digest'],[{**item,'quotes':{target['source_refs'][0]:'invented text'}}])
        result=record(self.root,actor,review,request['digest'],[item])
        self.assertFalse(result['human_supported'])
        self.assertFalse(result['credit_approval'])
        self.assertEqual(record(self.root,actor,review,request['digest'],[item]),result)
        with self.assertRaises(InputError):supported(self.store,request)
        self.assertEqual(self.store.get_record('live-progress:'+review),before)
        self.assertEqual(self.post.call_count,1)
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        app=CommandCenterTests.app(self)
        app.session_state['selected_financial_operation']=review
        widget(app.sidebar.radio,'Page').set_value('Review Workspace').run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any(e.label=='AI-assisted evidence review results' for e in app.expander))
        self.assertEqual(self.post.call_count,1)

    def test_general_uploaded_calculations_populate_all_screens_and_roles(self):
        from deal_or_no_deal_ai.uploaded_calculations import preview
        from deal_or_no_deal_ai.command_center import get_run
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        operation,actor,case=self.prepare_new_deal()
        state=run_uploaded(self.root,actor,operation)
        review=state['context']['operation_id']
        before=self.store.get_record('live-progress:'+review)
        app=CommandCenterTests.app(self)
        app.session_state['selected_financial_operation']=review
        for role in ('Analyst','RiskManager','ComplianceOfficer','AuthorizedApprover','Administrator'):
            scoped=replace(actor,persona=role)
            run=get_run(self.store,scoped,review)
            calculated=preview(self.root,scoped,run)
            self.assertEqual(next(m['display'] for m in calculated['metrics'] if m['metric_id']=='CALC-004'),'1.75')
            self.assertFalse(calculated['human_verified'])
            self.assertIsNone(calculated['risk']['score']['total'])
            self.assertEqual(len(calculated['risk']['score']['missing']),5)
            self.assertTrue(calculated['policy']['exception_rule_ids'])
            self.assertTrue(calculated['risk']['risk_flags'])
            widget(app.sidebar.selectbox,'Demo role').select(role).run(timeout=90)
            for page in ('Deal Dashboard','New Deal','Review Workspace','Agent Activity','Credit Memo','Decision History'):
                widget(app.sidebar.radio,'Page').set_value(page).run(timeout=90)
                if page=='New Deal':widget(app.radio,'Intake mode').set_value('Upload New Deal').run(timeout=90)
                self.assertEqual(len(app.exception),0,(role,page))
                self.assertTrue(any(e.label=='Uploaded deal calculations - preliminary' for e in app.expander),(role,page))
                self.assertTrue(any(e.label=='Uploaded policy checks - preliminary' for e in app.expander),(role,page))
                self.assertTrue(any(e.label=='Uploaded risk assessment - preliminary' for e in app.expander),(role,page))
        self.assertEqual(self.store.get_record('live-progress:'+review),before)
        self.assertEqual(self.post.call_count,1)
        with self.assertRaises(InputError):preview(self.root,replace(actor,allowed_deal_ids=frozenset()),get_run(self.store,actor,review))

    def test_general_save_profile_during_unrelated_recovery_keeps_execution_lock(self):
        operation,package,actor=self.prepare_upload(partial=True)
        locked=uid('unrelated-unknown-execution')
        receipt=self.store.admit(locked,dict(workspace_id=actor.workspace_id,review_id=uid('other-review')),dict(action='TEST_EXECUTION'))
        self.store.mark_unknown(receipt)
        profile=UploadProfile(borrower='Example Equipment LLC',review_as_of='2026-10-23',annual_start='2027-01-01',annual_end='2027-12-31',previous_start='2026-01-01',previous_end='2026-12-31',transaction_date='2026-10-23',annual_kind='SUPPLIED_ANNUAL_PROJECTION')
        save_profile(self.root,actor,operation,profile)
        saved=self.store.get_record('upload-profile:'+operation)
        self.assertEqual(saved[1]['profile']['annual_start'],'2027-01-01')
        save_profile(self.root,actor,operation,profile)
        self.assertEqual(self.store.get_record('upload-profile:'+operation),saved)
        self.assertIsNotNone(self.store.get_record('upload-profile-declaration:'+operation+':1'))
        with self.store.connection() as c:
            claim=c.execute('SELECT state,active_execution_key FROM app_operations WHERE operation_id=?',(locked,)).fetchone()
        self.assertEqual(claim['state'],'RECOVERY_REQUIRED')
        self.assertEqual(claim['active_execution_key'],'LOCAL_EXECUTION')
        with self.assertRaises(InputError):save_profile(self.root,replace(actor,persona='RiskManager'),operation,profile)
        self.assertEqual(self.post.call_count,0)

        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,'Page').set_value('New Deal').run()
        widget(app.radio,'Intake mode').set_value('Upload New Deal').run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(widget(app.button,'Run AI Deal Review').disabled)
        self.assertTrue(any('Reporting basis is saved. AI analysis cannot start' in e.value for e in app.error))
        self.assertEqual(self.post.call_count,0)

    def test_general_ui_save_profile_enables_run_without_manual_values(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        operation,package,actor=self.prepare_upload(partial=True)
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,'Page').set_value('New Deal').run()
        app.session_state['upload-profile-field:'+operation+':borrower']=''
        widget(app.radio,'Intake mode').set_value('Upload New Deal').run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(widget(app.button,'Run AI Deal Review').disabled)
        self.assertEqual(widget(app.text_input,'Documented borrower / legal entity').value,'Example Equipment LLC')
        self.assertEqual(widget(app.text_input,'Balance-sheet / transaction as-of date (YYYY-MM-DD)').value,'2026-10-23')
        widget(app.text_input,'Documented borrower / legal entity').set_value('Reviewer edit')
        widget(app.button,'Save reporting basis').click().run()
        self.assertEqual(widget(app.text_input,'Documented borrower / legal entity').value,'Reviewer edit')
        widget(app.button,'Refill from uploaded documents').click().run()
        self.assertEqual(widget(app.text_input,'Documented borrower / legal entity').value,'Example Equipment LLC')
        self.assertFalse(widget(app.checkbox,'I checked borrower, periods and USD whole-unit basis against the uploaded documents').value)
        widget(app.button,'Save reporting basis').click().run()
        self.assertTrue(any('Complete:' in e.value and 'confirmation checkbox' in e.value for e in app.error))
        values={'Documented borrower / legal entity':'Example Equipment LLC','Review date (YYYY-MM-DD)':'2026-10-23','Annual period start (YYYY-MM-DD)':'2027-01-01','Annual period end (YYYY-MM-DD)':'2027-12-31','Balance-sheet / transaction as-of date (YYYY-MM-DD)':'2026-10-23'}
        for label,value in values.items():widget(app.text_input,label).set_value(value)
        widget(app.selectbox,'Annual figures are').select('SUPPLIED_ANNUAL_PROJECTION')
        widget(app.checkbox,'I checked borrower, periods and USD whole-unit basis against the uploaded documents').check()
        widget(app.button,'Save reporting basis').click().run(timeout=90)
        self.assertEqual(len(app.exception),0)
        self.assertFalse(widget(app.button,'Run AI Deal Review').disabled)
        self.assertIsNotNone(self.store.get_record('upload-profile:'+operation))
        self.assertEqual(self.post.call_count,0)
        with patch('deal_or_no_deal_ai.upload_live.run_uploaded',return_value={'status':'WAITING_EVIDENCE'}) as run:
            widget(app.button,'Run AI Deal Review').click().run(timeout=90)
            self.assertEqual(run.call_count,1)
        self.assertEqual(len(app.exception),0)
        with patch('deal_or_no_deal_ai.upload_live.run_uploaded',side_effect=InputError('EVALUATION_REQUEST_UNCERTAIN_NO_RETRY')) as run:
            widget(app.button,'Run AI Deal Review').click().run(timeout=90)
            self.assertEqual(run.call_count,1)
            self.assertTrue(any('Deal analysis has not started' in e.value for e in app.warning))
            app.run()
            self.assertEqual(run.call_count,1)

    def prepare_new_deal(self):
        from tools.prepare_e_n01 import pdf_bytes
        text='''FICTIONAL EDUCATIONAL DEAL - NOT AN EXECUTED AGREEMENT
Borrower and legal entity: Northstar Widgets LLC
USD whole units. Term loan: 800000; term: 36 months; fixed rate: 6.5%.
Annual projection 2027-01-01 through 2027-12-31.
Comparative annual projection 2026-01-01 through 2026-12-31.
Transaction as of 2026-10-23. Guarantees: None.
Annual financial statements required; contractual due date not supplied.
Net income 200000; interest expense 40000; tax expense 40000.
Depreciation 20000; amortization 0.
Cash available for debt service 420000.
Annual principal payments 200000; annual interest payments 40000.
Existing funded debt 600000; proposed funded borrowing 800000; debt repaid 0.
Eligible equipment value 1000000; prior ranking liens 0; exposure 800000.
Revenue current period 2000000; comparative revenue 1800000.
Current assets 600000; current liabilities 300000.
Borrower factor assessments, KYC and sanctions evidence not supplied.
'''
        operation=uid('entirely-new-upload');package=inspect_package(self.root,self.actor(),operation,[('new-borrower.pdf',pdf_bytes([text]))],synthetic_confirmed=True)
        actor=replace(self.actor(),allowed_deal_ids=frozenset({identities(operation)['deal_id']}))
        save_profile(self.root,actor,operation,UploadProfile(borrower='Northstar Widgets LLC',review_as_of='2026-10-23',annual_start='2027-01-01',annual_end='2027-12-31',previous_start='2026-01-01',previous_end='2026-12-31',transaction_date='2026-10-23',annual_kind='SUPPLIED_ANNUAL_PROJECTION',secured_equipment=True))
        case,origin=load_uploaded_case(self.root,actor,operation);wire=case.wire.model_dump()
        ref=case.inventory[0].block_id
        for key,value in dict(borrower='Northstar Widgets LLC',legal_entity='Northstar Widgets LLC',facility_type='TERM_LOAN',requested_amount='800000',currency='USD',term_months=36,guarantees=[],covenants=['Supply annual financial statements']).items():
            wire['terms'][key]=dict(value=value,refs=[ref],basis_id=None)
        values=dict(net_income='200000',interest_expense='40000',income_tax_expense='40000',depreciation='20000',amortization='0',cash_available_for_debt_service='420000',annual_principal_payments='200000',annual_interest_payments='40000',existing_funded_debt='600000',proposed_funded_borrowing='800000',transaction_debt_repaid='0',eligible_equipment_value='1000000',prior_ranking_liens='0',secured_facility_exposure='800000',current_revenue='2000000',previous_revenue='1800000',current_assets='600000',current_liabilities='300000')
        for key,value in values.items():wire['financial_inputs'][key]=dict(value=value,refs=[ref],basis_id=_expected_basis(key))
        from deal_or_no_deal_ai.contracts import parse_extraction
        parse_extraction(json.dumps(wire))
        synth=dict(wire_version='SYN-WIRE-1.0',panel_decision=dict(decision='Conditional Approve',confidence=.8,rationale='Leverage and absent borrower risk assessments require further review.',conditions=['Obtain borrower risk assessments'],escalate_to_human=True),observations=[dict(panel=p,text=t,refs=['panel:'+p]) for p,t in [('FINANCIAL','Annual debt coverage is 1.75x; full-term adequacy is not established.'),('COMPLIANCE','The leverage exception and unknown control applicability remain unresolved.'),('RISK','No composite score: borrower factor assessments and concentration analysis are absent.')]],rationale_refs=['panel:FINANCIAL','panel:COMPLIANCE','panel:RISK'],condition_links=[dict(index=0,refs=['panel:RISK'])],proposed_action=None)
        def response(payload,key):
            extraction=payload['response_format']['json_schema']['name']=='extractor'
            return dict(model=payload['model'],choices=[dict(finish_reason='stop',message=dict(role='assistant',content=json.dumps(wire if extraction else synth)))],usage=dict(prompt_tokens=2400 if extraction else 2200,completion_tokens=900 if extraction else 500,total_tokens=3300 if extraction else 2700))
        self.post.side_effect=response
        return operation,actor,case

    def test_general_new_pdf_pauses_parallel_panels_unscored_partial_memo(self):
        operation,actor,case=self.prepare_new_deal()
        state=run_uploaded(self.root,actor,operation)
        self.assertEqual(state['pending_stage'],'fact_review')
        self.assertEqual(state['context']['verification_policy'],'HUMAN_REQUIRED')
        self.assertNotIn('financial_analyst',state['artifacts'])
        with self.assertRaises(InputError):
            from deal_or_no_deal_ai.live_demo import run_demo
            run_demo(self.root,actor,state['context']['operation_id'],resume_operation_id=uid('unsupported-resume'))
        state=self.finish_upload(state,actor)
        self.assertEqual(state['status'],'COMPLETED')
        self.assertEqual(state['artifacts']['specialist_panel']['payload']['execution'],'PARALLEL_FAN_OUT_JOIN')
        metrics=state['artifacts']['financial_analyst']['payload']['metric_results']
        self.assertEqual(next(m for m in metrics if m['metric_id']=='CALC-004')['display'],'1.75')
        self.assertIsNone(state['artifacts']['risk_quantifier']['payload']['score']['total'])
        self.assertFalse(state['approval_readiness']['approval_eligible'])
        self.assertIn('Northstar Widgets LLC',state['report_markdown'])
        self.assertNotIn('Example Equipment LLC',state['report_markdown'])
        self.assertIn('Insufficient data; no composite credit risk score',state['report_markdown'])
        from deal_or_no_deal_ai.command_center import source_packet,get_run
        packet=source_packet(self.root,get_run(self.store,actor,state['context']['operation_id']))
        self.assertEqual(packet['request']['terms']['requested_amount']['value'],'800000')
        self.assertEqual(self.post.call_count,2)

        # Real Streamlit rendering of this new borrower; rendering must not call inference.
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        app=CommandCenterTests.app(self)
        app.session_state['selected_financial_operation']=state['context']['operation_id']
        for page in ('Review Workspace','Agent Activity','Credit Memo','Decision History','Deal Dashboard'):
            widget(app.sidebar.radio,'Page').set_value(page).run(timeout=90)
            self.assertEqual(len(app.exception),0)
            self.assertEqual(app.session_state['selected_financial_operation'],state['context']['operation_id'])
        self.assertEqual(self.post.call_count,2)

    def test_general_parallel_branches_really_fan_out_and_join(self):
        from deal_or_no_deal_ai.graph import run_specialist_branches
        barrier=threading.Barrier(3);threads=set()
        def action():threads.add(threading.get_ident());barrier.wait(timeout=5);return {'done':True}
        outputs=run_specialist_branches({n:action for n in ('financial_analyst','compliance_check','risk_quantifier')})
        self.assertEqual(len(outputs),3);self.assertEqual(len(threads),3)

    def test_general_declared_period_validation_and_frozen_profile(self):
        operation,actor,case=self.prepare_new_deal()
        profile=UploadProfile(borrower='Northstar Widgets LLC',review_as_of='2026-10-23',annual_start='2027-01-01',annual_end='2027-12-31',previous_start='2026-01-01',previous_end='2026-12-31',transaction_date='2026-10-23',annual_kind='SUPPLIED_ANNUAL_PROJECTION')
        with self.assertRaises(InputError):save_profile(self.root,actor,operation,profile.model_copy(update={'annual_end':'2020-01-01'}))
        run_uploaded(self.root,actor,operation)
        with self.assertRaises(InputError):save_profile(self.root,actor,operation,profile.model_copy(update={'borrower':'Another company'}))
