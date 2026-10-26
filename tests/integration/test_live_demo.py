"""Phase 1 functional behavior with mocked provider calls, not model-quality scores."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import os
import socket

from deal_or_no_deal_ai.live_demo import run_demo
from deal_or_no_deal_ai.live_worker import run_live,record_credit
from deal_or_no_deal_ai.context import InputError,fingerprint
from deal_or_no_deal_ai.live_context import prepare_live_tasks
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.storage import Store
from tests.integration import test_live_graph as support
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import internal_event_loop_pair,widget
from tests.support import OfflineTest,uid


class LiveDemoTests(OfflineTest):
    actor=support.LiveGraphTests.actor
    response=support.LiveGraphTests.response

    def setUp(self):
        super().setUp()
        pair=patch.object(socket,"socketpair",internal_event_loop_pair);pair.start();self.addCleanup(pair.stop)
        folder=TemporaryDirectory();self.addCleanup(folder.cleanup)
        self.root=Path(folder.name);copy_workspace(self.root)
        self.deal=load_registered_case(self.root).scope.deal_id
        self.store=Store(self.root/"var/deal_review.sqlite3");self.operation=uid("phase1-live-demo")
        profile=self.root/"config/live_smoke.toml";tasks=prepare_live_tasks(self.root)
        profile.write_text(profile.read_text(encoding="utf-8").replace("provider_contract_verified = false","provider_contract_verified = true")+'\ntoken_count_strategy="PROVIDER_VERIFIED_WHOLE_REQUEST"\ninput_usd_per_million="0.10"\noutput_usd_per_million="0.30"\nrates_verified_on="MOCK_TEST_ONLY"\n[verified_packet_tokens]\n"'+fingerprint("LIVE_PACKET",tasks["extractor"])+'"=3900\n',encoding="utf-8")
        (self.root/".env").write_text("NEBIUS_API_KEY=synthetic-key-never-printed\n")
        env=patch.dict(os.environ,{"NEBIUS_API_KEY":""});env.start();self.addCleanup(env.stop)
        self.responses=[]
        generation=patch("deal_or_no_deal_ai.nebius_transport._post",side_effect=self.response)
        self.post=generation.start();self.addCleanup(generation.stop)
        def probe(endpoint,payload,key):
            self.assertEqual(endpoint,"chat/completions");self.assertEqual(payload["max_tokens"],1)
            return dict(model=payload["model"],usage=dict(prompt_tokens=2400,completion_tokens=1,total_tokens=2401))
        setup=patch("deal_or_no_deal_ai.evaluation_transport._post",side_effect=probe)
        self.probe=setup.start();self.addCleanup(setup.stop)
        self.policy("DEMO_DRAFT")

    def policy(self,value):
        p=self.root/"config/app.toml"
        text=p.read_text(encoding="utf-8").replace('mode = "FIXTURE"','mode = "LIVE"')
        text=text.replace('live_verification_policy = "DEMO_DRAFT"','live_verification_policy = "'+value+'"')
        text=text.replace('live_verification_policy = "HUMAN_REQUIRED"','live_verification_policy = "'+value+'"')
        p.write_text(text,encoding="utf-8")

    def test_run_completes_draft_with_live_handoffs_no_human_support_or_approval(self):
        result=run_demo(self.root,self.actor(),self.operation)
        self.assertEqual(result["status"],"COMPLETED")
        self.assertEqual(result["context"]["verification_policy"],"DEMO_DRAFT")
        self.assertEqual(self.post.call_count,2);self.assertEqual(self.probe.call_count,1)
        self.assertEqual(result["report_metadata"]["report_kind"],"UNVERIFIED_DRAFT")
        self.assertIn("UNVERIFIED EDUCATIONAL DRAFT",result["report_markdown"])
        self.assertFalse(result["approval_readiness"]["approval_eligible"])
        self.assertEqual(result["approval_readiness"]["outcome"],"Pending Review")
        for stage in ("fact_review","evidence_review"):
            self.assertFalse(result["artifacts"][stage]["payload"]["human_supported"])
            self.assertTrue(result["artifacts"][stage]["payload"]["automated_integrity_checked"])
        facts=result["artifacts"]["financial_analyst"]["payload"]["input_facts"]
        self.assertTrue(all(not f["human_supported"] for f in facts))
        metrics=result["artifacts"]["financial_analyst"]["payload"]["metric_results"]
        self.assertEqual(next(m for m in metrics if m["metric_id"]=="CALC-004")["display"],"1.50")
        self.assertEqual(result["artifacts"]["risk_quantifier"]["payload"]["score"]["display"],"21.00")
        from deal_or_no_deal_ai.command_center import get_run,source_packet
        self.assertTrue(source_packet(self.root,get_run(self.store,self.actor(),self.operation))['request']['reference_dictionary'])
        with self.store.connection() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM app_records WHERE kind IN ('LIVE_SUPPORT','LIVE_CREDIT_DECISION')").fetchone()[0],0)
        duplicate=run_demo(self.root,self.actor(),self.operation)
        self.assertEqual(duplicate["report_markdown"],result["report_markdown"])
        self.assertEqual(self.post.call_count,2);self.assertEqual(self.probe.call_count,1)
        with self.assertRaises(InputError):
            record_credit(self.root,self.actor("AuthorizedApprover"),self.operation,uid("forged-demo-approval"),"wrong-analysis","Approve","Cannot approve an unverified demo.",expected_readiness_version=result["approval_readiness"]["version"],expected_readiness_digest=result["approval_readiness"]["assessment_digest"])

    def test_historical_review_keeps_original_human_checkpoint_after_config_change(self):
        self.policy("HUMAN_REQUIRED")
        original=run_live(self.root,self.actor(),self.operation)
        context=self.store.get_record("live-context:"+self.operation)
        self.policy("DEMO_DRAFT")
        result=run_demo(self.root,self.actor(),self.operation)
        self.assertEqual(result["pending_stage"],"fact_review")
        self.assertEqual(result["status"],"WAITING_EVIDENCE")
        self.assertEqual(self.store.get_record("live-context:"+self.operation),context)
        self.assertEqual(self.post.call_count,1);self.assertEqual(self.probe.call_count,0)

    def test_unauthorized_role_and_invalid_inference_cannot_create_draft(self):
        with self.assertRaises(InputError):
            run_demo(self.root,self.actor("RiskManager"),self.operation)
        self.assertEqual(self.post.call_count,0)
        self.post.side_effect=TimeoutError("synthetic unavailable provider")
        with self.assertRaises(InputError):
            run_demo(self.root,self.actor(),self.operation)
        self.assertEqual(self.post.call_count,1);self.assertEqual(self.probe.call_count,0)
        self.assertFalse(self.store.get_record("live-progress:"+self.operation)[1].get("report_markdown"))
        from deal_or_no_deal_ai.live_recovery import close_known_invalid_demo
        with self.assertRaises(InputError):
            close_known_invalid_demo(self.store,self.actor('Administrator'),self.operation)

    def test_streamlit_run_to_workspace_activity_memo_history_without_replay(self):
        from tests.integration.test_command_center import CommandCenterTests
        app=CommandCenterTests.app(self)
        widget(app.sidebar.radio,"Page").set_value("New Deal").run()
        self.assertTrue(any("unverified educational draft" in i.value for i in app.info))
        widget(app.button,"Run AI Deal Review").click().run(timeout=180)
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any("Review completed" in i.value for i in app.success))
        self.assertEqual(self.post.call_count,2);self.assertEqual(self.probe.call_count,1)
        for page in ("Review Workspace","Agent Activity","Credit Memo","Decision History","Deal Dashboard"):
            widget(app.sidebar.radio,"Page").set_value(page).run()
            self.assertEqual(len(app.exception),0)
            if page=="Review Workspace":
                self.assertTrue(any(e.label=="Evidence reference" for e in app.selectbox))
        self.assertEqual(self.post.call_count,2);self.assertEqual(self.probe.call_count,1)

    def test_settled_truncation_can_close_but_unknown_failure_cannot(self):
        from deal_or_no_deal_ai.live_recovery import close_known_invalid_demo
        def truncated(payload,key):
            response=self.response(payload,key)
            if payload['response_format']['json_schema']['name']=='synthesizer':
                response['choices'][0]['finish_reason']='length'
            return response
        self.post.side_effect=truncated
        with self.assertRaises(InputError):run_demo(self.root,self.actor(),self.operation)
        with self.assertRaises(InputError):close_known_invalid_demo(self.store,self.actor(),self.operation)
        result=close_known_invalid_demo(self.store,self.actor('Administrator'),self.operation)
        self.assertEqual(result['status'],'MODEL_OUTPUT_INVALID')
        self.assertFalse(result.get('report_markdown'))
        self.assertEqual(close_known_invalid_demo(self.store,self.actor('Administrator'),self.operation),result)
        self.assertEqual(self.post.call_count,2)
