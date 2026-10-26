"""Original-response retention and safe local CLI, never a Live model evaluation."""

from copy import deepcopy
from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pydantic import ValidationError

from deal_or_no_deal_ai.context import InputError, canonical_json
from deal_or_no_deal_ai.model_comparison import prepare_comparison
from deal_or_no_deal_ai.quality_review import QualityCapture, review_capture
from tests.support import OfflineTest, ROOT, uid
from tools import review_model_response as command


def copy_workspace(root):
    for name in ("config", "fixtures/development/e-n01", "docs/agents"):
        shutil.copytree(ROOT / name, root / name)


def capture_for(stage="extractor", status="COMPLETE", name="capture"):
    plan = prepare_comparison(ROOT)
    path = ROOT / "fixtures/development/e-n01" / (
        "extraction.candidate.json" if stage == "extractor" else "synthesis.default.json")
    return dict(version="QUALITY-CAPTURE-1.0", attempt_id=uid(name), attempt_number=1,
        model_id=plan["arms"][0]["model_id"], stage=stage, task_digest=plan["task_digests"][stage],
        origin="FIXTURE_TEST", completion_status=status, output_text=path.read_text(encoding="utf-8"))


class QualityReviewTests(OfflineTest):
    def test_exact_first_capture_and_task_are_retained_without_touching_deal_database(self):
        capture = capture_for()
        raw = (json.dumps(capture, indent=3, ensure_ascii=False) + "\n\n").encode()
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            (root / "var").mkdir()
            database = root / "var/deal_review.sqlite3"
            database.write_bytes(b"DO_NOT_OPEN_OR_MODIFY")
            summary = review_capture(root, raw)
            result = json.loads((root / summary["report"]).read_text(encoding="utf-8"))
            dest = (root / summary["report"]).parent
            self.assertEqual((dest / "capture.json").read_bytes(), raw)
            self.assertEqual((dest / "original-output.txt").read_bytes(), capture["output_text"].encode())
            self.assertEqual(result["capture_sha256"], sha256(raw).hexdigest())
            task = json.loads((dest / "task.json").read_text(encoding="utf-8"))
            self.assertEqual(set(task["sources"]), set(prepare_comparison(root)["shared_task_packet"]["sources"]))
            self.assertEqual(result["checks"]["available_slots_exact_value_basis_match"], 31)
            self.assertFalse(result["accepted_for_application"])
            self.assertFalse(result["live_quality_established"])
            self.assertIsNone(result["actual_cost_usd"])
            self.assertEqual(database.read_bytes(), b"DO_NOT_OPEN_OR_MODIFY")
            self.assertEqual(review_capture(root, raw), summary)

    def test_changed_attempt_is_rejected_and_repair_has_separate_original(self):
        capture = capture_for()
        raw = canonical_json(capture).encode()
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            summary = review_capture(root, raw)
            changed = deepcopy(capture)
            changed["output_text"] = "not a valid response"
            with self.assertRaisesRegex(InputError, "ORIGINAL_RESPONSE_ARTIFACT_CHANGED"):
                review_capture(root, canonical_json(changed).encode())
            original = (root / summary["report"]).parent / "capture.json"
            self.assertEqual(original.read_bytes(), raw)
            changed.update(attempt_id=uid("repair"), attempt_number=2)
            repaired = review_capture(root, canonical_json(changed).encode())
            report = json.loads((root / repaired["report"]).read_text(encoding="utf-8"))
            self.assertEqual(report["output_cutoff"], "SEPARATE_DECLARED_LATER_ATTEMPT")
            self.assertFalse(report["checks"]["schema_valid"])
            self.assertEqual(original.read_bytes(), raw)

    def test_truncated_refused_error_and_unknown_never_accept_parseable_output(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            for stage in ("extractor", "synthesizer"):
                for status in ("TRUNCATED", "REFUSED", "ERROR", "UNKNOWN"):
                    with self.subTest(stage=stage, status=status):
                        capture = capture_for(stage, status, stage + status)
                        summary = review_capture(root, canonical_json(capture).encode())
                        report = json.loads((root / summary["report"]).read_text(encoding="utf-8"))
                        self.assertFalse(report["completion_eligible"])
                        self.assertFalse(report["checks"]["schema_valid"])
                        if stage == "extractor":
                            self.assertEqual(report["checks"]["available_slots"], 31)
                            self.assertEqual(report["checks"]["available_slots_exact_value_basis_match"], 0)
                        self.assertIsNone(report["checks"]["credit_disposition"])
                        self.assertIsNone(report["measured_provider_requests"])

    def test_synthesis_review_is_local_and_does_not_grant_fixture_or_live_support(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            capture = capture_for("synthesizer")
            capture["origin"] = "UNVERIFIED_CAPTURE"
            summary = review_capture(root, canonical_json(capture).encode())
            report = json.loads((root / summary["report"]).read_text(encoding="utf-8"))
            self.assertTrue(report["checks"]["schema_valid"])
            self.assertEqual(len(report["checks"]["narrative_targets"]), 4)
            self.assertEqual(report["provider_identity_status"], "UNVERIFIED_DECLARATION")
            self.assertIsNone(report["human_support"])
            self.assertIsNone(report["checks"]["narrative_scores"])

    def test_stale_task_invalid_utf8_duplicates_and_unsupported_claims_fail_before_retention(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            capture = capture_for()
            capture["task_digest"] = "0" * 64
            with self.assertRaisesRegex(InputError, "TASK_BINDING_MISMATCH"):
                review_capture(root, canonical_json(capture).encode())
            for bad in (b'\xff', b'{"version":"a","version":"b"}', b' ' * 262145):
                with self.subTest(raw=bad[:8]), self.assertRaises(InputError):
                    review_capture(root, bad)
            valid = capture_for()
            for update in ({"origin": "EXECUTED_LIVE"}, {"attempt_number": True},
                           {"attempt_id": "../../escape"}, {"completion_status": "stop"},
                           {"output_text": "x" * 65537}):
                with self.subTest(update=list(update)), self.assertRaises(ValidationError):
                    QualityCapture.model_validate(valid | update)
            self.assertFalse((root / "var").exists())

    def test_cli_outputs_only_safe_summary_and_sanitizes_validation_errors(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            source = root / "input.json"
            source.write_text(canonical_json(capture_for()), encoding="utf-8")
            output = StringIO()
            with patch.object(command, "ROOT", root), patch("sys.argv", ["review_model_response", str(source)]), \
                    redirect_stdout(output):
                self.assertEqual(command.main(), 0)
            self.assertNotIn("cash_available_for_debt_service", output.getvalue())
            self.assertEqual(json.loads(output.getvalue())["tool_provider_requests"], 0)
            source.write_text('{"secret_field":"SENSITIVE_TEST_TEXT"}', encoding="utf-8")
            output = StringIO()
            with patch.object(command, "ROOT", root), patch("sys.argv", ["review_model_response", str(source)]), \
                    redirect_stdout(output):
                self.assertEqual(command.main(), 1)
            self.assertNotIn("SENSITIVE_TEST_TEXT", output.getvalue())

    def test_review_no_secret_client_network_or_database_even_if_key_is_present(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            source = root / "capture.json"
            source.write_text(canonical_json(capture_for("synthesizer")), encoding="utf-8")
            script = '''import sys,os,json
from pathlib import Path
def guard(event,args):
 if event in ('socket.connect','socket.getaddrinfo','sqlite3.connect'):
  raise AssertionError('SIDE_EFFECT_DENIED')
sys.addaudithook(guard)
original=os._Environ.__getitem__
def read(self,key):
 if key=='NEBIUS_API_KEY': raise AssertionError('SECRET_READ_DENIED')
 return original(self,key)
os._Environ.__getitem__=read
from deal_or_no_deal_ai.quality_review import review_capture
root=Path(sys.argv[1])
result=review_capture(root,(root/'capture.json').read_bytes())
assert not any(m in sys.modules for m in ('openai','torch','sentence_transformers','langsmith'))
assert result['tool_provider_requests']==0
print('OFFLINE_ONLY')'''
            result = subprocess.run([sys.executable, "-c", script, str(root)], cwd=ROOT,
                                    capture_output=True, text=True, timeout=25)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "OFFLINE_ONLY")
