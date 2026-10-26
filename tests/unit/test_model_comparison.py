"""GEN-COMPARE harness controls, not real-model quality or savings."""

from copy import deepcopy
from decimal import Decimal
import json
import subprocess
import sys

from pydantic import ValidationError

from deal_or_no_deal_ai.context import InputError, canonical_json, fingerprint
from deal_or_no_deal_ai.model_comparison import (
    ComparisonProfile, check_extraction_response, estimate_generation_cost,
    load_comparison_profile, prepare_comparison,
)
from deal_or_no_deal_ai.services import load_registered_case
from tests.support import OfflineTest, ROOT


class ModelComparisonTests(OfflineTest):
    def test_only_selected_pair_and_disabled_execution_configuration_are_accepted(self):
        profile = load_comparison_profile(ROOT)
        for change in ({"paid_execution_enabled": True}, {"allowance_status": "APPROVED"},
                       {"provider_contract_status": "VERIFIED"},
                       {"challenger": profile.baseline.model_dump()},
                       {"api_key": "SYNTHETIC_NOT_A_KEY"}):
            supplied = profile.model_dump()
            supplied.update(change)
            with self.subTest(change=change), self.assertRaises(ValidationError):
                ComparisonProfile.model_validate(supplied)

    def test_paired_packet_has_identical_identity_and_no_expected_response_or_gold(self):
        report = prepare_comparison(ROOT)
        case = load_registered_case(ROOT)
        packet = report["shared_task_packet"]
        self.assertEqual(report["shared_task_digest"], fingerprint("GEN-COMPARE-TASK-1.0", packet))
        self.assertEqual({a["shared_task_digest"] for a in report["arms"]}, {report["shared_task_digest"]})
        self.assertEqual(set(packet), {"task", "instruction", "output_schema", "sources", "bases", "review_basis"})
        self.assertEqual(set(packet["sources"]), set(case.registration.expected_pages))
        self.assertEqual(packet["sources"]["FIN-P1"]["text"], next(b.text for b in case.inventory if b.block_id == "FIN-P1"))
        self.assertNotIn(canonical_json(case.wire.model_dump()), canonical_json(packet))
        self.assertNotIn("gold", packet)
        self.assertEqual(report["instruction_hashes"], case.registration.instruction_hashes)
        self.assertEqual(set(report["task_packets"]), {"extractor", "synthesizer"})
        self.assertEqual(report["task_digests"]["synthesizer"], fingerprint(
            "GEN-COMPARE-TASK-1.0", report["task_packets"]["synthesizer"]))
        self.assertTrue(all(arm["shared_task_digests"] == report["task_digests"] for arm in report["arms"]))
        self.assertNotIn("panel_decision", report["task_packets"]["synthesizer"]["context"])

    def test_missing_cases_and_unrun_measurements_are_explicit_not_zero_or_success(self):
        report = prepare_comparison(ROOT)
        self.assertIsNone(report["winner"])
        self.assertIsNone(report["token_count"])
        self.assertFalse(report["application_model_changed"])
        for arm in report["arms"]:
            self.assertEqual(arm["status"], "NOT_RUN")
            for key in ("schema_valid", "field_accuracy", "source_grounding", "latency_ms", "actual_cost_usd", "requests"):
                self.assertIsNone(arm[key])
        for row in report["readiness"]:
            if row["scenario"] != "E-N01":
                self.assertEqual(row["source_status"], "NOT_READY")
            self.assertNotEqual(row["execution_status"], "READY")

    def test_dated_price_estimate_counts_billed_output_without_claiming_actual_cost(self):
        profile = load_comparison_profile(ROOT)
        self.assertEqual(estimate_generation_cost(profile.baseline, input_tokens=6000, billed_output_tokens=1500), "0.00105")
        self.assertEqual(estimate_generation_cost(profile.challenger, input_tokens=6000, billed_output_tokens=1500), "0.00072")
        for bad in (True, -1, Decimal("1"), "1"):
            with self.subTest(bad=bad), self.assertRaises(InputError):
                estimate_generation_cost(profile.baseline, input_tokens=bad, billed_output_tokens=0)

    def test_matching_reference_response_does_not_grant_grounding_or_credit_disposition(self):
        case = load_registered_case(ROOT)
        result = check_extraction_response(canonical_json(case.wire.model_dump()), case)
        self.assertTrue(result["schema_valid"])
        self.assertEqual((result["fields_exact_value_basis_match"], result["fields_total"]), (31, 31))
        self.assertEqual(result["unresolved_source_refs"], 0)
        self.assertEqual(result["source_grounding"], "MANUAL_REVIEW_REQUIRED")
        self.assertEqual(result["model_quality_status"], "NOT_ESTABLISHED")
        self.assertIsNone(result["credit_disposition"])

    def test_wrong_values_and_unknown_references_are_visible_in_local_checks(self):
        case = load_registered_case(ROOT)
        wire = deepcopy(case.wire.model_dump())
        wire["financial_inputs"]["cash_available_for_debt_service"].update(
            value="1", refs=["OUT_OF_SCOPE"], basis_id="WRONG_PERIOD")
        result = check_extraction_response(canonical_json(wire), case)
        self.assertTrue(result["schema_valid"])
        self.assertEqual(result["fields_exact_value_basis_match"], 30)
        self.assertEqual(result["unresolved_source_refs"], 1)
        self.assertEqual(result["unresolved_basis_refs"], 1)

    def test_malformed_or_duplicate_key_outputs_fail_without_becoming_reject(self):
        case = load_registered_case(ROOT)
        for raw in ('{}', '{"terms":{},"terms":{}}', '{"confidence":NaN}', 'not JSON'):
            with self.subTest(raw=raw):
                result = check_extraction_response(raw, case)
                self.assertFalse(result["schema_valid"])
                self.assertEqual(result["fields_total"], 31)
                self.assertEqual(result["fields_exact_value_basis_match"], 0)
                self.assertIsNone(result["credit_disposition"])

    def test_import_and_actual_preparation_read_no_secret_or_database_and_load_no_clients(self):
        script = '''import sys,os,json
from pathlib import Path
def guard(event,args):
 if event in ('socket.connect','socket.getaddrinfo','sqlite3.connect','os.mkdir'):
  raise AssertionError('SIDE_EFFECT_DENIED')
sys.addaudithook(guard)
original=os._Environ.__getitem__
def read(self,key):
 if key=='NEBIUS_API_KEY': raise AssertionError('SECRET_READ_DENIED')
 return original(self,key)
os._Environ.__getitem__=read
from deal_or_no_deal_ai.model_comparison import prepare_comparison
report=prepare_comparison(Path.cwd())
assert not any(m in sys.modules for m in ('openai','torch','sentence_transformers','langsmith'))
assert report['preparation_provider_requests']==0
print(json.dumps({'status':'OFFLINE_ONLY','arms':len(report['arms'])}))'''
        result = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"status": "OFFLINE_ONLY", "arms": 2})
