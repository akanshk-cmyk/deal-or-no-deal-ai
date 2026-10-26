"""Actual shared graph/checkpoints with mocked Nebius; no paid model-quality claim."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import os

from deal_or_no_deal_ai.command_center import workspace_id
from deal_or_no_deal_ai.context import InputError, fingerprint
from deal_or_no_deal_ai.contracts import parse_extraction, wire_json
from deal_or_no_deal_ai.live_context import prepare_live_tasks, live_synthesis_task
from deal_or_no_deal_ai.live_review import Assessment, assess, request_key, CHECKS, required_checks
from deal_or_no_deal_ai.live_worker import run_live, load_live
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.storage import Store
from deal_or_no_deal_ai.synthesis import prepare_synthesis
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import OfflineTest, uid
from tests.integration.test_human_review_ui import internal_event_loop_pair

class LiveGraphTests(OfflineTest):
    def test_known_invalid_extraction_can_be_closed_without_retry_or_unknown_usage(self):
        from dataclasses import replace
        from deal_or_no_deal_ai.live_recovery import close_known_invalid_extraction
        original=self.response
        def invalid(payload,key):
            result=original(payload,key)
            wire=json.loads(result["choices"][0]["message"]["content"])
            wire["terms"]["guarantees"]={"value":None,"refs":["AGREEMENT-P1"],"basis_id":None}
            result["choices"][0]["message"]["content"]=json.dumps(wire)
            return result
        self.post.side_effect=invalid
        with self.assertRaises(InputError):
            run_live(self.root,self.actor(),self.operation)
        with self.assertRaisesRegex(InputError,"ADMINISTRATOR"):
            close_known_invalid_extraction(self.store,self.actor(),self.operation)
        admin=replace(self.actor(),persona="Administrator")
        closed=close_known_invalid_extraction(self.store,admin,self.operation)
        self.assertEqual(closed["status"],"MODEL_OUTPUT_INVALID")
        self.assertNotIn("extractor",closed["artifacts"])
        self.assertEqual(closed["ledger"]["reservations"],{})
        self.assertEqual(close_known_invalid_extraction(self.store,admin,self.operation),closed)
        self.assertEqual(self.post.call_count,1)

    def setUp(self):
        super().setUp()
        from tests.integration.test_human_review_ui import internal_event_loop_pair
        import socket
        pair=patch.object(socket,"socketpair",internal_event_loop_pair)
        pair.start();self.addCleanup(pair.stop)
        folder=TemporaryDirectory();self.addCleanup(folder.cleanup)
        self.root=Path(folder.name);copy_workspace(self.root)
        case=load_registered_case(self.root)
        self.deal=case.scope.deal_id
        self.store=Store(self.root/"var/deal_review.sqlite3")
        self.operation=uid("live-e-n01")
        tasks=prepare_live_tasks(self.root)
        profile=self.root/"config/live_smoke.toml"
        profile.write_text(profile.read_text(encoding="utf-8").replace("provider_contract_verified = false","provider_contract_verified = true")+'\ntoken_count_strategy="PROVIDER_VERIFIED_WHOLE_REQUEST"\ninput_usd_per_million="0.10"\noutput_usd_per_million="0.30"\nrates_verified_on="MOCK_TEST_ONLY"\n[verified_packet_tokens]\n"'+fingerprint("LIVE_PACKET",tasks["extractor"])+'"=3900\n',encoding="utf-8")
        (self.root/".env").write_text("NEBIUS_API_KEY=synthetic-key-never-printed\n")
        self.env=patch.dict(os.environ,{"NEBIUS_API_KEY":""});self.env.start();self.addCleanup(self.env.stop)
        self.responses=[]
        self.post=patch("deal_or_no_deal_ai.nebius_transport._post",side_effect=self.response).start()
        self.addCleanup(patch.stopall)

    def actor(self,role="Analyst"):
        return Actor(role,workspace_id(self.root),frozenset({self.deal}),frozenset({"NORMAL"}) if role=="AuthorizedApprover" else frozenset())

    def response(self,payload,key):
        stage=payload["response_format"]["json_schema"]["name"]
        raw=(self.root/("fixtures/development/e-n01/extraction.candidate.json" if stage=="extractor" else "fixtures/development/e-n01/synthesis.default.json")).read_text(encoding="utf-8")
        self.responses.append((stage,raw))
        return dict(model=payload["model"],choices=[dict(finish_reason="stop",message=dict(role="assistant",content=raw))],usage=dict(prompt_tokens=3700 if stage=="extractor" else 2300,completion_tokens=950 if stage=="extractor" else 600,total_tokens=4650 if stage=="extractor" else 2900))

    def support_all(self,state):
        stage=state["pending_stage"]; request=self.store.get_record(request_key(state["context"]["scope"]["run_id"],stage))[1]
        for target in request["targets"]:
            for domain in target["domains"]:
                role="RiskManager" if domain=="FINANCIAL_RISK" else "ComplianceOfficer"
                command=Assessment(operation_id=uid(stage+target["id"]+domain),request_digest=request["digest"],target_id=target["id"],target_digest=target["digest"],domain=domain,status="HUMAN_SUPPORTED",quotes={ref:request["sources"][ref] for ref in target["source_refs"]},checks=list(required_checks(stage)),comments="Synthetic test reviewer checked exact source, value, period, units, identity, meaning and qualifications.")
                assess(self.root,self.actor(role),state["context"]["scope"]["run_id"],stage,command)
        return request

    def allow_current_synthesis(self,state):
        from deal_or_no_deal_ai.live_worker import _live_case
        from deal_or_no_deal_ai.panel_codec import restore_financial,restore_compliance,restore_risk
        case=_live_case(load_registered_case(self.root),state,self.store)
        # Paused before calculations: compute the exact same deterministic packet for mock token evidence only.
        from deal_or_no_deal_ai.services import evaluate_panels
        packet=prepare_synthesis(case,panels=evaluate_panels(case))
        task=live_synthesis_task(self.root,packet["request"])
        with (self.root/"config/live_smoke.toml").open("a",encoding="utf-8") as stream:
            stream.write('"'+fingerprint("LIVE_PACKET",task)+'"=2450\n')

    def test_complete_actual_graph_pauses_and_requires_both_narrative_domains(self):
        first=run_live(self.root,self.actor(),self.operation)
        self.assertEqual(first["status"],"WAITING_EVIDENCE")
        self.assertEqual(first["pending_stage"],"fact_review")
        self.assertEqual(set(first["artifacts"]),{"pdf_input","extractor"})
        self.assertEqual(len(self.responses),1)
        from uuid import UUID,uuid5
        request=self.store.get_record("paid-request:"+str(uuid5(UUID(self.operation),"paid:extractor")))[1]
        self.assertEqual(request["payload"]["model"],"Qwen/Qwen3-30B-A3B-Instruct-2507")
        self.assertNotIn("synthetic-key",str(request))
        self.assertEqual(first["artifacts"]["extractor"]["payload"]["wire_json"],self.responses[0][1])
        with self.assertRaisesRegex(InputError,"INCOMPLETE"):
            run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("no-support"))
        self.support_all(first)
        self.allow_current_synthesis(first)
        second=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("after-facts"))
        self.assertEqual(second["pending_stage"],"evidence_review")
        self.assertEqual(second["status"],"WAITING_EVIDENCE")
        self.assertIsNone(second["report_markdown"])
        self.assertEqual(len(self.responses),2)
        self.assertTrue(all(f["human_supported"] for f in second["artifacts"]["financial_analyst"]["payload"]["input_facts"] if f["value"] is not None))
        request=self.support_all(second)
        self.assertTrue(all(set(t["domains"])=={"FINANCIAL_RISK","POLICY_CONTROL"} for t in request["targets"]))
        final=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("after-narrative"))
        self.assertEqual(final["status"],"COMPLETED")
        self.assertEqual(final["ledger"]["committed"]["attempts"],2)
        self.assertEqual(final["ledger"]["committed"]["nodes"],10)
        self.assertEqual(final["ledger"]["reservations"],{})
        self.assertEqual(len(self.responses),2)
        self.assertIn("Actual provider responses",final["report_markdown"])
        self.assertIn("Supporting sources and calculations",final["report_markdown"])
        self.assertNotIn("Canned stage response",final["report_markdown"])
        duplicate=run_live(self.root,self.actor(),self.operation)
        self.assertEqual(duplicate["report_markdown"],final["report_markdown"])
        self.assertEqual(len(self.responses),2)

    def test_live_layout_renders_narrative_pause_and_completed_memo_without_dispatch(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        first=run_live(self.root,self.actor(),self.operation)
        self.support_all(first)
        self.allow_current_synthesis(first)
        second=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("layout-after-facts"))
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(widget(app.metric,"Credit risk · illustrative").value,"21.00 / 100")
        self.assertEqual(widget(app.metric,"Evidence checks").value,"Reviewer checks required")
        self.assertTrue(any(s.value=="Verify AI conclusions" for s in app.subheader))
        self.assertEqual(self.post.call_count,2)
        self.support_all(second)
        run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("layout-after-narrative"))
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(widget(app.metric,"Evidence checks").value,"Reviewer checks completed")
        widget(app.sidebar.radio,"Page").set_value("Credit Memo").run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("CREDIT REVIEW MEMORANDUM" in c.value for c in app.caption))
        self.assertEqual(self.post.call_count,2)

    def test_new_deal_failed_attempt_keeps_reference_without_retry(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        self.post.side_effect=TimeoutError('synthetic transport interruption')
        with self.assertRaises(InputError):run_live(self.root,self.actor(),self.operation)
        config=self.root/'config/app.toml'
        config.write_text(config.read_text().replace('mode = "FIXTURE"','mode = "LIVE"'))
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,'Page').set_value('New Deal').run()
        app.session_state['financial_operation']=self.operation
        self.assertEqual(len(app.exception),0)
        self.assertTrue(widget(app.button,'Run AI Deal Review').disabled)
        self.assertTrue(any('execution lock affects both Sample Deal and Upload New Deal' in item.value for item in app.error))
        self.assertTrue(any(self.operation in item.value for item in app.caption))
        self.assertEqual(self.post.call_count,1)

    def test_new_deal_modes_share_intake_preview_and_keep_explicit_live_start(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        app=CommandCenterTests.app(self)
        self.assertFalse(any(r.label=="Review mode" for r in app.sidebar.radio))
        widget(app.sidebar.radio,"Page").set_value("New Deal").run()
        saved_cards=[m.value for m in app.markdown if 'surface-label' in m.value]
        config=self.root/"config/app.toml"
        config.write_text(config.read_text().replace('mode = "FIXTURE"','mode = "LIVE"'))
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(sum(b.label=="Run AI Deal Review" for b in app.button),1)
        self.assertEqual(widget(app.radio,"Intake mode").value,"Sample Deal")
        self.assertEqual(widget(app.selectbox,"Sample scenario").value,"default")
        for card in saved_cards:
            self.assertTrue(any(m.value==card for m in app.markdown))
        self.assertEqual(self.post.call_count,0)
        widget(app.radio,"Intake mode").set_value("Upload New Deal").run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("declare their reporting basis" in item.value for item in app.info))
        self.assertFalse(any(b.label=="Run AI Deal Review" for b in app.button))
        self.assertEqual(self.post.call_count,0)
        widget(app.radio,"Intake mode").set_value("Sample Deal").run()
        widget(app.button,"Run AI Deal Review").click().run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,1)
        self.assertTrue(any("Review needs attention:" in item.value for item in app.warning))
        self.assertEqual(len(app.success),0)
        self.assertTrue(any(b.label=="Open review workspace" for b in app.button))
        # A returned recovery state is an error, never a green success notice.
        with patch("deal_or_no_deal_ai.live_worker.run_live",return_value={"status":"RECOVERY_REQUIRED","pending_stage":"extractor"}):
            widget(app.button,"Run AI Deal Review").click().run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("Technical assistance required" in item.value for item in app.error))
        self.assertEqual(len(app.success),0)
        self.assertEqual(self.post.call_count,1)

    def test_unified_history_keeps_saved_and_live_sources_independent_of_new_run_config(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        from deal_or_no_deal_ai.worker import run_normal_fixture
        from deal_or_no_deal_ai.command_center import get_run
        saved=uid("unified-original-saved")
        run_normal_fixture(self.root,saved,generation_time="2026-10-24T01:00:00+00:00")
        original=get_run(self.store,self.actor(),saved)
        run_live(self.root,self.actor(),self.operation)
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.session_state["selected_financial_operation"],self.operation)
        self.assertEqual(len(widget(app.selectbox,"Review attempt").options),2)
        widget(app.selectbox,"Review attempt").select(saved).run()
        self.assertTrue(any("Saved AI responses" in m.value and 'context-card' in m.value for m in app.markdown))
        config=self.root/"config/app.toml"
        config.write_text(config.read_text().replace('mode = "FIXTURE"','mode = "LIVE"'))
        app.run()
        self.assertEqual(app.session_state["selected_financial_operation"],saved)
        widget(app.sidebar.radio,"Page").set_value("Credit Memo").run()
        self.assertTrue(any("Saved demo output" in c.value for c in app.caption))
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        widget(app.selectbox,"Review attempt").select(self.operation).run()
        self.assertTrue(any("Live AI response" in m.value and 'context-card' in m.value for m in app.markdown))
        self.assertTrue(any(s.value=="Verify extracted facts" for s in app.subheader))
        widget(app.sidebar.radio,"Page").set_value("Decision History").run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("Selected review source: Live AI response" in c.value for c in app.caption))
        self.assertEqual(get_run(self.store,self.actor(),saved),original)
        self.assertEqual(self.post.call_count,1)

    def test_unified_live_start_failure_never_calls_saved_execution(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        config=self.root/"config/app.toml"
        config.write_text(config.read_text().replace('mode = "FIXTURE"','mode = "LIVE"'))
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("New Deal").run()
        with patch("deal_or_no_deal_ai.live_worker.run_live",side_effect=InputError("LIVE_TEST_SETUP_BLOCKED")) as live, patch("deal_or_no_deal_ai.ui.command_center.start_run") as saved:
            widget(app.button,"Run AI Deal Review").click().run()
            self.assertEqual(live.call_count,1)
            saved.assert_not_called()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("No reset or automatic retry" in e.value for e in app.error))
        self.assertEqual(self.post.call_count,0)

    def test_live_attempt_history_is_scoped_and_preserves_selection_across_pages(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        run_live(self.root,self.actor(),self.operation)
        newer=uid("live-layout-newer-attempt")
        run_live(self.root,self.actor(),newer)
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.session_state["selected_financial_operation"],newer)
        widget(app.selectbox,"Review attempt").select(self.operation).run()
        widget(app.sidebar.radio,"Page").set_value("Agent Activity").run()
        self.assertEqual(app.session_state["selected_financial_operation"],self.operation)
        widget(app.button,"Open latest review").click().run()
        self.assertEqual(app.session_state["selected_financial_operation"],newer)
        widget(app.sidebar.radio,"Page").set_value("Deal Dashboard").run()
        self.assertEqual(widget(app.metric,"Registered deals reviewed").value,"1")
        self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,2)

    def test_wrong_role_stale_target_missing_checks_and_withheld_cannot_continue(self):
        state=run_live(self.root,self.actor(),self.operation)
        request=self.store.get_record(request_key(state["context"]["scope"]["run_id"],"fact_review"))[1];target=request["targets"][0]
        values=dict(operation_id=uid("assessment-invalid"),request_digest=request["digest"],target_id=target["id"],target_digest=target["digest"],domain="FINANCIAL_RISK",status="HUMAN_SUPPORTED",quotes={r:request["sources"][r] for r in target["source_refs"]},checks=list(required_checks("fact_review")),comments="Synthetic test only")
        for actor,changes in [(self.actor(),{}),(self.actor("RiskManager"),dict(target_digest="stale")),(self.actor("RiskManager"),dict(checks=[])),(self.actor("RiskManager"),dict(quotes={"FIN-P1":"Not in source"}))]:
            with self.assertRaises(InputError):
                assess(self.root,actor,state["context"]["scope"]["run_id"],"fact_review",Assessment(**{**values,**changes}))
        assess(self.root,self.actor("RiskManager"),state["context"]["scope"]["run_id"],"fact_review",Assessment(**{**values,"status":"WITHHELD"}))
        with self.assertRaises(InputError):
            run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("withheld-continue"))
        self.assertEqual(len(self.responses),1)

    def test_source_change_stales_continuation_before_another_call(self):
        state=run_live(self.root,self.actor(),self.operation)
        self.support_all(state)
        p=self.root/"docs/agents/live-extractor.md"
        p.write_text(p.read_text(encoding="utf-8")+" Changed live prompt",encoding="utf-8")
        with self.assertRaisesRegex(InputError,"SOURCE_OR_PROMPT_CHANGED"):
            run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("stale-source"))
        self.assertEqual(len(self.responses),1)

    def test_missing_material_input_stops_before_calculations_or_synthesis(self):
        original=self.response
        def missing(payload,key):
            response=original(payload,key)
            raw=json.loads(response["choices"][0]["message"]["content"])
            raw["financial_inputs"]["cash_available_for_debt_service"]=dict(value=None,refs=[],basis_id=None)
            response["choices"][0]["message"]["content"]=json.dumps(raw)
            return response
        self.post.side_effect=missing
        result=run_live(self.root,self.actor(),self.operation)
        self.assertEqual(result["status"],"WAITING_INFORMATION")
        self.assertNotIn("financial_analyst",result["artifacts"])
        self.assertNotIn("synthesizer",result["artifacts"])
        self.assertIsNone(result["report_markdown"])

    def test_low_confidence_requires_separate_credit_decision(self):
        original=self.response
        def low_confidence(payload,key):
            result=original(payload,key)
            if payload["response_format"]["json_schema"]["name"]=="synthesizer":
                raw=json.loads(result["choices"][0]["message"]["content"])
                raw["panel_decision"]["confidence"]=0.65
                # Intentionally false: Python, not the model, controls escalation.
                raw["panel_decision"]["escalate_to_human"]=False
                result["choices"][0]["message"]["content"]=json.dumps(raw)
            return result
        self.post.side_effect=low_confidence
        first=run_live(self.root,self.actor(),self.operation);self.support_all(first);self.allow_current_synthesis(first)
        second=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("low-after-facts"));self.support_all(second)
        third=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("low-after-narrative"))
        self.assertEqual(third["status"],"WAITING_REVIEW")
        self.assertIsNone(third["report_markdown"])
        from deal_or_no_deal_ai.live_worker import record_credit
        with self.assertRaises(InputError):
            run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("low-without-decision"))
        basis=third["artifacts"]["review_prepare"]["payload"]["analysis_digest"]
        with self.assertRaises(InputError):
            record_credit(self.root,self.actor("RiskManager"),self.operation,uid("wrong-approver"),basis,"Approve","No credit authority")
        readiness=third["approval_readiness"]
        with self.assertRaisesRegex(InputError,"APPROVAL_READINESS_BLOCKED"):
            record_credit(self.root,self.actor("AuthorizedApprover"),self.operation,uid("live-credit-approve"),basis,"Approve","Covenant not evaluated",expected_readiness_version=readiness["version"],expected_readiness_digest=readiness["assessment_digest"])
        record_credit(self.root,self.actor("AuthorizedApprover"),self.operation,uid("live-credit-reject"),basis,"Reject","Separate simulated human rejection; not inferred from missing covenant evaluation.")
        final=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("low-after-credit"))
        self.assertEqual(final["status"],"COMPLETED")
        self.assertEqual(final["ledger"]["committed"]["nodes"],12)
        self.assertIn("Human credit decision: Reject",final["report_markdown"])
        self.assertEqual(len(self.responses),2)

    def test_provider_timeout_has_no_fallback_and_retains_unknown_allowance(self):
        self.post.side_effect=TimeoutError("synthetic-key-never-printed")
        with self.assertRaisesRegex(InputError,"RECONCILIATION") as caught:
            run_live(self.root,self.actor(),self.operation)
        self.assertNotIn("synthetic-key",str(caught.exception))
        state=load_live(self.root,self.actor(),self.operation)
        self.assertEqual(state["status"],"RECOVERY_REQUIRED")
        self.assertNotIn("extractor",state["artifacts"])
        budget=self.store.get_record("paid-allowance:first-synthetic-010")[1]
        self.assertTrue(budget["reservations"])
        ledger=self.store.get_record("ledger:"+state["context"]["scope"]["review_id"])[1]
        self.assertTrue(ledger["unknown"])

    def test_live_ui_review_is_explicit_and_metadata_submit_does_not_dispatch(self):
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        first=run_live(self.root,self.actor(),self.operation)
        from deal_or_no_deal_ai.live_review import assessment_progress
        request=self.store.get_record(request_key(first['context']['scope']['run_id'],'fact_review'))[1]
        progress=assessment_progress(self.store,request)
        self.assertEqual(progress['supported'],0)
        self.assertGreater(progress['required'],0)
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,1)
        self.assertTrue(any('paused for fact verification' in e.value for e in app.warning))
        from deal_or_no_deal_ai.ui.presentation import WORKSPACE_TABS
        self.assertEqual(tuple(tab.label for tab in app.tabs),WORKSPACE_TABS)
        self.assertTrue(any("Live AI response" in item.value for item in app.markdown))
        self.assertTrue(any(item.value=="Evidence explorer" for item in app.subheader))
        self.assertEqual(len(widget(app.selectbox,"Select Deal").options),1)
        # Navigation is read-only, including New Deal: starting remains explicit.
        for page in ("Deal Dashboard","New Deal","Agent Activity","Credit Memo","Decision History","Review Workspace"):
            widget(app.sidebar.radio,"Page").set_value(page).run()
            self.assertEqual(len(app.exception),0,page)
            self.assertEqual(self.post.call_count,1,page)
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,1)
        widget(app.sidebar.selectbox,"Demo role").select("RiskManager").run()
        self.assertEqual(len(app.exception),0)
        request=self.store.get_record(request_key(first["context"]["scope"]["run_id"],"fact_review"))[1]
        target=request["targets"][0]
        for ref in target["source_refs"]:
            self.assertEqual(widget(app.text_area,"Exact supporting quote from "+ref).value,request["sources"][ref])
            widget(app.text_area,"Exact supporting quote from "+ref).input(request["sources"][ref])
        self.assertFalse(any(c.value for c in app.checkbox))
        for check in app.checkbox:
            check.check()
        widget(app.selectbox,"Evidence assessment").select("HUMAN_SUPPORTED")
        widget(app.text_area,"Review comments (required)").input("Synthetic UI reviewer verified the source and borrower.")
        widget(app.button,"Record evidence review").click().run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(self.post.call_count,1)
        self.assertTrue(widget(app.button,"Continue live review").disabled)
        from deal_or_no_deal_ai.live_review import support_key
        saved=self.store.get_record(support_key(request,target["id"],"FINANCIAL_RISK"))
        self.assertEqual(saved[1]["reviewer_role"],"RiskManager")
        self.assertEqual(saved[1]["command"]["status"],"HUMAN_SUPPORTED")

    def test_unverified_synthesis_packet_pauses_without_spending_or_recovery(self):
        first=run_live(self.root,self.actor(),self.operation);self.support_all(first)
        paused=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("config-after-facts"))
        self.assertEqual(paused["status"],"WAITING_CONFIGURATION")
        self.assertEqual(paused["pending_stage"],"synthesizer")
        self.assertEqual(self.post.call_count,1)
        self.assertEqual(paused["ledger"]["reservations"],{})
        with self.assertRaisesRegex(InputError,"TOKEN_VERIFICATION_REQUIRED"):
            run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("still-unverified"))
        self.assertEqual(load_live(self.root,self.actor(),self.operation)["status"],"WAITING_CONFIGURATION")
        prepared=self.store.get_record("live-provider-request:"+paused["context"]["scope"]["run_id"]+":synthesizer")[1]
        with (self.root/"config/live_smoke.toml").open("a",encoding="utf-8") as stream:
            stream.write('"'+prepared["task_digest"]+'"=2450\n')
        result=run_live(self.root,self.actor(),self.operation,resume_operation_id=uid("config-verified"))
        self.assertEqual(result["status"],"WAITING_EVIDENCE")
        self.assertEqual(result["pending_stage"],"evidence_review")
        self.assertEqual(self.post.call_count,2)
