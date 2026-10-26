"""No-network paid-dispatch guards, actual native ID metrics and retrieval mechanics."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import os
import json
import socket

from deal_or_no_deal_ai.live_setup import read_api_key
from deal_or_no_deal_ai.nebius_transport import dispatch_generation
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.retrieval_benchmark import Passage, retrieve
from deal_or_no_deal_ai.ragas_evaluation import native_id_scores
from deal_or_no_deal_ai.storage import Store, RecordWrite
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import internal_event_loop_pair, widget
from tests.support import OfflineTest, uid


class LiveFoundationTests(OfflineTest):
    def setUp(self):
        super().setUp()
        folder = TemporaryDirectory(); self.addCleanup(folder.cleanup)
        self.root = Path(folder.name); copy_workspace(self.root)

    def enable_mock_contract(self):
        path = self.root / "config/live_smoke.toml"
        path.write_text(path.read_text().replace('provider_contract_verified = false', 'provider_contract_verified = true') + '\ntoken_count_strategy="PROVIDER_VERIFIED_WHOLE_REQUEST"\ninput_usd_per_million="0.10"\noutput_usd_per_million="0.30"\nrates_verified_on="SYNTHETIC_MOCK_ONLY"\n')
        (self.root / ".env").write_text("NEBIUS_API_KEY=synthetic-test-key\n")

    def dispatch(self, operation=None):
        return dispatch_generation(self.root, operation or uid("paid-test"), uid("live-review"), stage="extractor", instruction="Extract synthetic fields", context={"synthetic": True}, verified_input_tokens=20)

    def response(self):
        return dict(model="Qwen/Qwen3-30B-A3B-Instruct-2507", choices=[dict(finish_reason="stop", message=dict(role="assistant", content=(self.root / "fixtures/development/e-n01/extraction.candidate.json").read_text()))], usage=dict(prompt_tokens=20, completion_tokens=900, total_tokens=920))

    def test_key_loading_is_explicit_and_contract_blocks_before_dispatch(self):
        with patch.dict(os.environ, {"NEBIUS_API_KEY": ""}):
            with self.assertRaisesRegex(InputError, "NOT_CONFIGURED"):
                read_api_key(self.root)
            (self.root / ".env").write_text('# not executed\nNEBIUS_API_KEY="test-value"\n')
            self.assertEqual(read_api_key(self.root), "test-value")
            with patch("deal_or_no_deal_ai.nebius_transport._post", side_effect=AssertionError("NO_DISPATCH")):
                with self.assertRaisesRegex(InputError, "CONTRACT_REQUIRED"):
                    self.dispatch()
        self.assertFalse((self.root / "var").exists())

    def test_mock_response_settles_shared_allowance_and_duplicate_never_calls_again(self):
        self.enable_mock_contract()
        with patch("deal_or_no_deal_ai.nebius_transport._post", return_value=self.response()) as post:
            result = self.dispatch()
            duplicate = self.dispatch()
        self.assertEqual(post.call_count, 1)
        self.assertEqual(result, duplicate)
        self.assertEqual(result["response"]["status"], "VALIDATED")
        store = Store(self.root / "var/deal_review.sqlite3")
        budget = store.get_record("paid-allowance:first-synthetic-010")[1]
        self.assertEqual(budget["reservations"], {})
        self.assertEqual(budget["committed_usd"], "0.000272")
        ledger = store.get_record("ledger:" + uid("live-review"))[1]
        self.assertEqual(ledger["committed"]["attempts"], 1)

    def test_unknown_dispatch_keeps_maximum_reservation_and_no_secret_in_error(self):
        self.enable_mock_contract()
        with patch("deal_or_no_deal_ai.nebius_transport._post", side_effect=TimeoutError("synthetic-test-key")):
            with self.assertRaisesRegex(InputError, "RECONCILIATION") as error:
                self.dispatch()
        self.assertNotIn("synthetic-test-key", str(error.exception))
        budget = Store(self.root / "var/deal_review.sqlite3").get_record("paid-allowance:first-synthetic-010")[1]
        self.assertTrue(budget["reservations"])

    def test_three_generation_requests_block_fourth_and_keep_cached_result(self):
        self.enable_mock_contract()
        response = self.response()
        response["usage"] = dict(prompt_tokens=20, completion_tokens=100, total_tokens=120)
        with patch("deal_or_no_deal_ai.nebius_transport._post", return_value=response) as post:
            first = self.dispatch(uid("bounded-request-1"))
            self.dispatch(uid("bounded-request-2"))
            self.dispatch(uid("bounded-request-3"))
            store = Store(self.root / "var/deal_review.sqlite3")
            before = store.path.read_bytes()
            with self.assertRaisesRegex(InputError, "LIVE_GENERATION_REQUEST_LIMIT_REACHED"):
                self.dispatch(uid("bounded-request-4"))
            self.assertEqual(store.path.read_bytes(), before)
            self.assertEqual(self.dispatch(uid("bounded-request-1")), first)
        self.assertEqual(post.call_count, 3)

    def test_uncertain_request_is_not_retried_with_same_or_new_operation_id(self):
        self.enable_mock_contract()
        with patch("deal_or_no_deal_ai.nebius_transport._post", side_effect=TimeoutError("do-not-log")) as post:
            with self.assertRaisesRegex(InputError, "RECONCILIATION"):
                self.dispatch(uid("uncertain-original"))
            store = Store(self.root / "var/deal_review.sqlite3")
            before = store.path.read_bytes()
            with self.assertRaisesRegex(InputError, "UNCERTAIN"):
                self.dispatch(uid("uncertain-original"))
            from deal_or_no_deal_ai.storage import RunBusy
            with self.assertRaises(RunBusy):
                self.dispatch(uid("uncertain-new-id"))
            self.assertEqual(store.path.read_bytes(), before)
        self.assertEqual(post.call_count, 1)

    def test_scoped_four_arm_mechanics_and_real_native_ragas_ids(self):
        passages = [Passage("a", "annual cash flow", "scope", "a" * 64, 1, True),
            Passage("b", "collateral equipment", "scope", "b" * 64, 2, True),
            Passage("old", "annual cash flow", "other", "c" * 64, 1, True)]
        for arm in ("DIRECT", "KEYWORD", "VECTOR", "HYBRID"):
            result = retrieve(passages, "annual cash", scope_digest="scope", strategy=arm,
                vectors={"a": [1., 0.], "b": [0., 1.]}, query_vector=[1., 0.], top_k=1)
            self.assertNotIn("old", result["passage_ids"])
            if arm != "DIRECT":
                self.assertEqual(result["passage_ids"], ["a"])
        with self.assertRaises(InputError):
            retrieve(passages, "cash", scope_digest="scope", strategy="VECTOR")
        with patch.object(socket, "socketpair", internal_event_loop_pair):
            scores = native_id_scores(["a", "b"], ["a", "c"], ranked=True)
        self.assertEqual(scores["native_id_context_precision"], .5)
        self.assertEqual(scores["native_id_context_recall"], .5)
        self.assertIsNone(scores["faithfulness"])

    def test_readiness_button_never_dispatches_or_exposes_key(self):
        from tests.integration.test_command_center import CommandCenterTests
        (self.root / '.env').write_text('NEBIUS_API_KEY=synthetic-readiness-secret\n')
        with patch('deal_or_no_deal_ai.nebius_transport._post', side_effect=AssertionError('NO_DISPATCH')):
            app = CommandCenterTests.app(self)
            widget(app.sidebar.radio, 'Page').set_value('New Deal').run()
            self.assertFalse(any(b.label == 'Check live AI readiness' for b in app.main.button))
            widget(app.sidebar.button, 'Check live AI readiness').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Local setup needs attention' in item.value for item in app.warning))
        self.assertTrue(any('API key: Configured' in item.value for item in app.markdown))
        self.assertNotIn('synthetic-readiness-secret', str(app.code))
        self.assertTrue(any(code.language=='text' for code in app.code))
        widget(app.sidebar.radio,'Page').set_value('Agent Activity').run()
        self.assertTrue(any('API key: Configured' in item.value for item in app.markdown))
        self.assertFalse((self.root / 'var').exists())
