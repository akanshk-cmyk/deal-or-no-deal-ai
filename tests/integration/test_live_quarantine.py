"""Approved quarantine isolates uncertainty without inventing accounting or support."""
from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch
from uuid import UUID, uuid5
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import socket

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.live_recovery import quarantine_unknown_extraction
from deal_or_no_deal_ai.live_worker import run_live, load_live
from deal_or_no_deal_ai.nebius_transport import dispatch_generation
from deal_or_no_deal_ai.storage import RecordWrite, Receipt
from tests.integration import test_live_graph as graph_support
from tests.support import OfflineTest, uid


class LiveQuarantineTests(OfflineTest):
    actor = graph_support.LiveGraphTests.actor
    response = graph_support.LiveGraphTests.response
    support_all = graph_support.LiveGraphTests.support_all
    allow_current_synthesis = graph_support.LiveGraphTests.allow_current_synthesis

    def setUp(self):
        super().setUp()
        from tests.integration.test_human_review_ui import internal_event_loop_pair
        from tests.integration.test_normal_fixture_graph import copy_workspace
        from deal_or_no_deal_ai.services import load_registered_case
        from deal_or_no_deal_ai.live_context import prepare_live_tasks
        from deal_or_no_deal_ai.context import fingerprint
        from deal_or_no_deal_ai.storage import Store
        pair=patch.object(socket,"socketpair",internal_event_loop_pair)
        pair.start();self.addCleanup(pair.stop)
        folder=TemporaryDirectory();self.addCleanup(folder.cleanup)
        self.root=Path(folder.name);copy_workspace(self.root)
        self.deal=load_registered_case(self.root).scope.deal_id
        self.store=Store(self.root/"var/deal_review.sqlite3")
        self.operation=uid("quarantine-interrupted-live")
        tasks=prepare_live_tasks(self.root)
        profile=self.root/"config/live_smoke.toml"
        profile.write_text(profile.read_text(encoding="utf-8").replace("provider_contract_verified = false","provider_contract_verified = true")+'\ntoken_count_strategy="PROVIDER_VERIFIED_WHOLE_REQUEST"\ninput_usd_per_million="0.10"\noutput_usd_per_million="0.30"\nrates_verified_on="MOCK_TEST_ONLY"\n[verified_packet_tokens]\n"'+fingerprint("LIVE_PACKET",tasks["extractor"])+'"=3900\n',encoding="utf-8")
        (self.root/".env").write_text("NEBIUS_API_KEY=synthetic-key-never-printed\n")
        env=patch.dict(os.environ,{"NEBIUS_API_KEY":""});env.start();self.addCleanup(env.stop)
        self.responses=[]
        guard=patch("deal_or_no_deal_ai.nebius_transport._post",side_effect=self.response)
        self.post=guard.start();self.addCleanup(guard.stop)

    def uncertain(self):
        self.post.side_effect=TimeoutError("no-secret-in-output")
        with self.assertRaises(InputError):
            run_live(self.root,self.actor(),self.operation)
        self.context=self.store.get_record("live-context:"+self.operation)[1]
        self.review=self.context["scope"]["review_id"]
        self.paid=str(uuid5(UUID(self.operation),"paid:extractor"))
        keys=dict(context="live-context:"+self.operation,progress="live-progress:"+self.operation,
            ledger="ledger:"+self.review,allowance="paid-allowance:first-synthetic-010",request="paid-request:"+self.paid)
        self.expected={k:self.store.get_record(v)[0] for k,v in keys.items()}
        guard=patch("deal_or_no_deal_ai.live_recovery.QUARANTINE_OPERATION",self.operation)
        guard.start();self.addCleanup(guard.stop)

    def quarantine(self,actor=None,expected=None):
        return quarantine_unknown_extraction(self.store,actor or self.actor("Administrator"),self.operation,
            expected_versions=expected or self.expected,reason="Approved synthetic administrative abandonment; usage remains unknown.")

    def test_second_exact_approved_operation_is_allowed_but_random_operation_is_not(self):
        from deal_or_no_deal_ai.live_recovery import ADDITIONAL_QUARANTINE_OPERATION
        self.operation=ADDITIONAL_QUARANTINE_OPERATION
        self.uncertain()
        with patch('deal_or_no_deal_ai.live_recovery.QUARANTINE_OPERATION','aab508af-564d-461f-a4e7-cf0708ec29b6'):
            with self.assertRaisesRegex(InputError,'APPROVED_QUARANTINE'):
                quarantine_unknown_extraction(self.store,self.actor('Administrator'),uid('not-approved'),expected_versions=self.expected,reason='Not authorized')
            audit=self.quarantine()
        self.assertEqual(audit['operation_id'],ADDITIONAL_QUARANTINE_OPERATION)
        self.assertEqual(audit['retained_reservation_usd'],'0.0007')
        self.assertFalse(audit['replay_permitted'])

    def test_permissions_scope_and_version_fail_before_any_writes(self):
        self.uncertain()
        before=self.store.path.read_bytes()
        for actor in (self.actor(),replace(self.actor("Administrator"),workspace_id=uid("wrong-workspace")),
                      replace(self.actor("Administrator"),allowed_deal_ids=frozenset())):
            with self.assertRaises(InputError):
                self.quarantine(actor)
            self.assertEqual(self.store.path.read_bytes(),before)
        with self.assertRaisesRegex(InputError,"STALE"):
            self.quarantine(expected={**self.expected,"allowance":self.expected["allowance"]+1})
        self.assertEqual(self.store.path.read_bytes(),before)

    def test_latest_sample_exact_request_preserves_unknown_reservation(self):
        from deal_or_no_deal_ai.live_recovery import LATEST_SAMPLE_QUARANTINE_OPERATION
        self.operation=LATEST_SAMPLE_QUARANTINE_OPERATION
        self.uncertain()
        with patch('deal_or_no_deal_ai.live_recovery.QUARANTINE_OPERATION','aab508af-564d-461f-a4e7-cf0708ec29b6'):
            audit=self.quarantine()
        self.assertEqual(audit['operation_id'],LATEST_SAMPLE_QUARANTINE_OPERATION)
        self.assertEqual(audit['retained_reservation_usd'],'0.0007')
        self.assertFalse(audit['replay_permitted'])

    def test_network_blocked_exact_sample_can_be_isolated(self):
        from deal_or_no_deal_ai.live_recovery import NETWORK_BLOCKED_SAMPLE_OPERATION
        self.operation=NETWORK_BLOCKED_SAMPLE_OPERATION
        self.uncertain()
        with patch('deal_or_no_deal_ai.live_recovery.QUARANTINE_OPERATION','aab508af-564d-461f-a4e7-cf0708ec29b6'):
            audit=self.quarantine()
        self.assertEqual(audit['operation_id'],NETWORK_BLOCKED_SAMPLE_OPERATION)
        self.assertEqual(audit['retained_reservation_usd'],'0.0007')

    def test_missing_reservation_and_known_result_prevent_quarantine(self):
        self.uncertain()
        key="paid-allowance:first-synthetic-010"
        version,allowance=self.store.get_record(key)
        self.store.put_record(RecordWrite(key,"PAID_ALLOWANCE",{**allowance,"reservations":{}},version))
        self.expected["allowance"]=version+1
        with self.assertRaisesRegex(InputError,"EXACT_UNCERTAIN"):
            self.quarantine()
        self.store.put_record(RecordWrite(key,"PAID_ALLOWANCE",allowance,version+1))
        self.expected["allowance"]=version+2
        self.store.put_record(RecordWrite("paid-result:"+self.paid,"PAID_GENERATION_RESULT",dict(existing=True)))
        with self.assertRaisesRegex(InputError,"EXACT_UNCERTAIN"):
            self.quarantine()
        self.assertIsNone(self.store.get_record("quarantine-review:"+self.review))

    def test_atomic_failure_does_not_release_claim_or_leave_partial_audit(self):
        self.uncertain()
        before=self.store.path.read_bytes()
        original=self.store._write
        def fail_after_audit(connection,write):
            original(connection,write)
            if write.kind=="LIVE_QUARANTINE":
                raise RuntimeError("synthetic failure before release")
        with patch.object(self.store,"_write",side_effect=fail_after_audit):
            with self.assertRaises(RuntimeError):
                self.quarantine()
        self.assertEqual(self.store.path.read_bytes(),before)

    def test_quarantine_preserves_history_reservations_and_blocks_all_replays(self):
        self.uncertain()
        keys=("ledger:"+self.review,"paid-allowance:first-synthetic-010","live-progress:"+self.operation)
        original={k:deepcopy(self.store.get_record(k)) for k in keys}
        with self.store.connection() as c:
            checkpoints=[tuple(r) for r in c.execute("SELECT * FROM checkpoints")]
        audit=self.quarantine()
        self.assertFalse(audit["provider_usage_reconciled"])
        self.assertEqual(self.quarantine(),audit)
        for key in keys:
            self.assertEqual(self.store.get_record(key),original[key])
        with self.store.connection() as c:
            self.assertEqual([tuple(r) for r in c.execute("SELECT * FROM checkpoints")],checkpoints)
            self.assertEqual(c.execute("SELECT count(*) FROM app_operations WHERE active_execution_key IS NOT NULL").fetchone()[0],0)
            self.assertEqual(c.execute("SELECT count(*) FROM app_record_history WHERE kind='LIVE_QUARANTINE'").fetchone()[0],1)
        state=load_live(self.root,self.actor(),self.operation)
        self.assertEqual(state["status"],"RECOVERY_REQUIRED")
        self.assertEqual(state["quarantine"],audit)
        for resume in (None,uid("blocked-resume")):
            with self.assertRaisesRegex(InputError,"QUARANTINED"):
                run_live(self.root,self.actor(),self.operation,resume_operation_id=resume)
        for operation in (self.paid,uid("new-paid-id")):
            with self.assertRaisesRegex(InputError,"QUARANTINED"):
                dispatch_generation(self.root,operation,self.review,stage="extractor",instruction="test",context={},verified_input_tokens=20)
        with self.assertRaisesRegex(InputError,"QUARANTINED"):
            self.store.admit(uid("direct-admission"),self.context["scope"],dict(action="LIVE_CONTINUE"))
        self.assertEqual(self.post.call_count,1)

    def test_late_response_cannot_settle_unknown_or_release_other_review(self):
        original_response=self.response
        def late(payload,key):
            self.context=self.store.get_record("live-context:"+self.operation)[1]
            self.review=self.context["scope"]["review_id"]
            self.paid=str(uuid5(UUID(self.operation),"paid:extractor"))
            with self.store.connection() as c:
                row=c.execute("SELECT * FROM app_operations WHERE operation_id=?",(self.operation,)).fetchone()
            receipt=Receipt(self.operation,row["payload_digest"],row["state"],False)
            version,data=self.store.get_record("ledger:"+self.review)
            from deal_or_no_deal_ai.budgets import Ledger
            marked=Ledger.from_dict(data).mark_unknown(self.paid)
            self.store.put_record(RecordWrite("ledger:"+self.review,"BUDGET_LEDGER",marked.to_dict(),version))
            self.store.mark_unknown(receipt)
            keys=dict(context="live-context:"+self.operation,progress="live-progress:"+self.operation,
                ledger="ledger:"+self.review,allowance="paid-allowance:first-synthetic-010",request="paid-request:"+self.paid)
            self.expected={k:self.store.get_record(v)[0] for k,v in keys.items()}
            with patch("deal_or_no_deal_ai.live_recovery.QUARANTINE_OPERATION",self.operation):
                self.quarantine()
            self.other=self.store.admit(uid("unrelated-active"),dict(review_id=uid("other-review")),dict(action="TEST_OTHER_WORK"))
            self.before_late=self.store.get_record("paid-allowance:first-synthetic-010")
            return original_response(payload,key)
        self.post.side_effect=late
        with self.assertRaises(InputError):
            run_live(self.root,self.actor(),self.operation)
        self.assertIsNone(self.store.get_record("paid-result:"+self.paid))
        self.assertEqual(self.store.get_record("paid-allowance:first-synthetic-010"),self.before_late)
        self.store.assert_claim(self.other)
        self.assertEqual(self.post.call_count,1)

    def test_unrelated_review_keeps_verification_and_can_finish_with_reserve_retained(self):
        self.uncertain()
        self.quarantine()
        reserved=deepcopy(self.store.get_record("paid-allowance:first-synthetic-010")[1]["reservations"])
        self.post.side_effect=self.response
        operation=uid("unrelated-valid-live")
        first=run_live(self.root,self.actor(),operation)
        self.assertEqual(first["pending_stage"],"fact_review")
        with self.assertRaisesRegex(InputError,"INCOMPLETE"):
            run_live(self.root,self.actor(),operation,resume_operation_id=uid("without-human-support"))
        self.support_all(first)
        self.allow_current_synthesis(first)
        second=run_live(self.root,self.actor(),operation,resume_operation_id=uid("unrelated-after-facts"))
        self.assertEqual(second["pending_stage"],"evidence_review")
        self.support_all(second)
        final=run_live(self.root,self.actor(),operation,resume_operation_id=uid("unrelated-after-narrative"))
        self.assertEqual(final["status"],"COMPLETED")
        self.assertEqual(self.store.get_record("paid-allowance:first-synthetic-010")[1]["reservations"],reserved)

    def test_ui_shows_set_aside_history_and_opens_valid_pause_without_calls(self):
        self.uncertain()
        self.quarantine()
        self.post.side_effect=self.response
        operation=uid("earlier-valid-navigation")
        run_live(self.root,self.actor(),operation)
        from tests.integration.test_command_center import CommandCenterTests
        from tests.integration.test_human_review_ui import widget
        with patch("deal_or_no_deal_ai.nebius_transport._post",side_effect=AssertionError("NO_RENDER_DISPATCH")):
            app=CommandCenterTests.app(self)
            app.session_state["selected_financial_operation"]=self.operation
            widget(app.sidebar.radio,"Page").set_value("Review Workspace").run()
            self.assertEqual(len(app.exception),0)
            self.assertTrue(any("set aside" in item.value for item in app.warning))
            widget(app.button,"Open live review awaiting fact verification").click().run()
            self.assertEqual(app.session_state["selected_financial_operation"],operation)
            self.assertEqual(len(app.exception),0)
            widget(app.sidebar.radio,"Page").set_value("Decision History").run()
            self.assertEqual(len(app.exception),0)
            self.assertTrue(any("Interrupted attempt set aside" in item.value for item in app.warning))
        self.assertEqual(self.post.call_count,2)
