"""Actual authored PDFs and scope checks, not executed alternate loan workflows."""

from hashlib import sha256
from decimal import Decimal
from io import BytesIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader

from deal_or_no_deal_ai.context import InputError
from tools.prepare_core_case_sources import prepare
from tests.support import OfflineTest, ROOT


class CoreCaseSourceTests(OfflineTest):
    def test_separate_sources_parse_with_explicit_missing_data_and_approved_bridge(self):
        original = (ROOT / "config/registrations/e-n01.json").read_bytes()
        with TemporaryDirectory() as folder:
            destination = Path(folder)
            result = prepare(ROOT, destination)
            self.assertEqual(set(result), {"E-P01", "E-M01", "E-F03"})
            hashes = []
            for name, expected_score, dscr in (("E-P01", "33.00", "1.15"), ("E-M01", None, None), ("E-F03", "45.00", "-0.50")):
                pack = destination / name.lower()
                manifest = json.loads((pack / "source-manifest.json").read_bytes())
                wire = json.loads((pack / "extraction.candidate.json").read_bytes())
                self.assertFalse(manifest["registered"])
                self.assertIsNone(manifest["panel_decision"])
                self.assertEqual(None if manifest["expected_score"] is None else Decimal(manifest["expected_score"]),
                                 None if expected_score is None else Decimal(expected_score))
                self.assertEqual(manifest["financial_results"]["CALC-004"]["display"], dscr)
                for fact in wire["financial_inputs"].values():
                    self.assertTrue(all(ref.startswith(name + ":") for ref in fact["refs"]))
                for source in manifest["sources"]:
                    raw = (pack / source["filename"]).read_bytes()
                    self.assertEqual(sha256(raw).hexdigest(), source["sha256"])
                    reader = PdfReader(BytesIO(raw), strict=True)
                    self.assertEqual(len(reader.pages), source["pages"])
                hashes.append(manifest["source_package_digest"])
            self.assertEqual(len(set(hashes)), 3)
            text = '\n'.join(p.extract_text() for p in PdfReader(str(destination / "e-f03/financials.pdf")).pages)
            self.assertIn("working-capital cash outflow 800000", text)
            self.assertIn("capital cash outflow 600000", text)
            self.assertEqual(prepare(ROOT, destination), result)
            target = destination / "e-p01/financials.pdf"
            target.write_bytes(b"changed")
            with self.assertRaisesRegex(InputError, "EXISTING_CORE_SOURCE_DIFFERS"):
                prepare(ROOT, destination)
            self.assertEqual(target.read_bytes(), b"changed")
        self.assertEqual((ROOT / "config/registrations/e-n01.json").read_bytes(), original)
