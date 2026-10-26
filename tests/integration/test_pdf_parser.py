"""Actual known-corpus parser parts of TEST-001-02/03/04, TEST-006-02/03."""

from pathlib import Path
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError
from tests.support import OfflineTest, ROOT
from tools.verify_e_n01_pdfs import revenue_columns, verify_pack


class KnownCorpusParserTests(OfflineTest):
    def test_all_actual_pages_preserve_text_columns_notes_and_pending_authority(self):
        report, texts = verify_pack()
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["source_files"], 3)
        self.assertEqual(report["actual_page_count"], 5)
        self.assertEqual(report["license_expression"], "BSD-3-Clause")
        self.assertTrue(all(report["focused_checks"].values()))
        self.assertEqual(report["revenue_columns"]["values"], {"2026": "4000000", "2027": "4400000"})
        self.assertEqual(len(texts), 10)
        self.assertIn("COLLATERAL-1's pool", texts["FINANCIALS-1/page-2.plain.txt"])
        self.assertIn("case's stated basis", texts["COLLATERAL-1/page-1.layout.txt"])
        self.assertTrue(all(b["parser_verified"] and not b["source_fit_verified"] for b in report["parsed_inventory"]))
        for coverage in report["coverage"].values():
            self.assertEqual(coverage["status"], "UNVERIFIED")
            self.assertEqual(coverage["reasons"], ("SOURCE_FIT_UNVERIFIED",))
            self.assertEqual(coverage["exposed_blocks"], 0)
        self.assertIsNone(report["case_approved"])
        self.assertIsNone(report["registered"])
        self.assertFalse(report["registration_checked"])
        self.assertFalse(report["human_supported"])

    def test_changed_pdf_is_rejected_before_the_known_corpus_parser_can_run(self):
        source = ROOT / "fixtures/development/e-n01/sources/financials.pdf"
        read_bytes = Path.read_bytes

        def tampered(path):
            original = read_bytes(path)
            return original + b" altered" if path == source else original

        with patch.object(Path, "read_bytes", tampered), patch("pypdf.PdfReader") as reader:
            with self.assertRaisesRegex(InputError, "KNOWN_CORPUS_BYTES_MISMATCH"):
                verify_pack()
            reader.assert_not_called()

    def test_column_diagnostic_uses_headers_and_rejects_ambiguity(self):
        header = "ANNUAL PROJECTION" + " " * 21 + "2026" + " " * 14 + "2027"
        row = "Revenue" + " " * 28 + "4000000" + " " * 11 + "4400000"
        table = header + "\n" + row + "\n\nRevenue growth is explanatory prose."
        self.assertEqual(revenue_columns(table)["values"], {"2026": "4000000", "2027": "4400000"})
        reverse = table.replace("2026", "TEMP").replace("2027", "2026").replace("TEMP", "2027")
        self.assertEqual(revenue_columns(reverse)["values"], {"2027": "4000000", "2026": "4400000"})
        invalid = (
            table.replace("2027", "2026"), table.replace("2027", "    "),
            header + "\n" + row + "\n" + row,
            header + "\n" + "Revenue".ljust(45) + "4000000" + " " * 3 + "4400000",
            header + "\nRevenue 4000000\n",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(InputError):
                revenue_columns(value)
