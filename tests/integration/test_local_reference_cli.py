"""TEST-001/006: explicit local source retention and stopped-command behavior."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools import inspect_local_reference as command

ROOT = Path(__file__).resolve().parents[2]


class LocalReferenceCLITests(unittest.TestCase):
    def invoke(self, root, source):
        output = StringIO()
        with patch.object(command, "ROOT", root), patch("sys.argv", ["inspect", str(source)]), \
                patch("socket.socket.connect", side_effect=AssertionError("NO_NETWORK")), \
                patch("sqlite3.connect", side_effect=AssertionError("NO_DATABASE")), redirect_stdout(output):
            code = command.main()
        return code, json.loads(output.getvalue())

    def test_each_explicit_observation_retains_bytes_report_and_prior_history(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config/source_ingestion.toml").write_bytes((ROOT / "config/source_ingestion.toml").read_bytes())
            source = root / "synthetic.html"
            content = b"<html><body><p>Synthetic CLI input, not a real company statement.</p></body></html>"
            source.write_bytes(content)
            reports = []
            for _ in range(2):
                code, result = self.invoke(root, source)
                self.assertEqual(code, 0)
                report = root / result["report"]
                saved = json.loads(report.read_text(encoding="utf-8"))
                self.assertEqual((report.parent / "source.html").read_bytes(), content)
                self.assertEqual(saved["content_sha256"], sha256(content).hexdigest())
                self.assertEqual(saved["status"], "INSPECTION_ONLY")
                self.assertEqual(saved["origin_status"], "UNBOUND_LOCAL_UPLOAD")
                self.assertIsNone(saved["corpus_id"])
                self.assertEqual(saved["declared_source"], {})
                self.assertEqual(saved["scope_status"], "NO_CORPUS_ADMISSION")
                self.assertFalse(saved["index_created"] or saved["final_ready"])
                reports.append(report)
            self.assertNotEqual(*reports)
            self.assertTrue(all(p.exists() for p in reports))
            self.assertEqual(source.read_bytes(), content)

    def test_stopped_file_does_not_create_success_report_or_index(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config/source_ingestion.toml").write_bytes((ROOT / "config/source_ingestion.toml").read_bytes())
            source = root / "unsupported.txt"
            source.write_text("Not a supported reference upload", encoding="utf-8")
            code, result = self.invoke(root, source)
            self.assertEqual(code, 2)
            self.assertEqual(result["status"], "STOPPED")
            self.assertEqual(result["reason"], "UNSUPPORTED_REFERENCE_FILE_TYPE")
            self.assertFalse((root / "var").exists())
