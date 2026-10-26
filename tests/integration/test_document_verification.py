"""Scoped TEST-001-04 and TEST-006-02/03/07, not real PDF/model quality."""

from tests.document_verification_cases import compare_cases
from tests.support import OfflineTest


class PairedDocumentVerificationTests(OfflineTest):
    def test_same_inputs_safe_baseline_and_opt_in_expansion(self):
        report = compare_cases()
        self.assertGreaterEqual(report["unique_case_count"], 10)
        self.assertEqual(report["failures"], 0, report)
        self.assertFalse(report["adaptive_adopted"])
        for case in report["cases"]:
            with self.subTest(case=case["case_id"]):
                baseline, adaptive = case["arms"]["BASELINE"], case["arms"]["ADAPTIVE"]
                self.assertEqual(baseline["input_digest"], adaptive["input_digest"])
                self.assertEqual(baseline["expanded"], [])
                if case["case_id"] == "cross-page-disclosure":
                    self.assertEqual(baseline["status"], "INCOMPLETE")
                    self.assertEqual(baseline["blocks"], [])
                    self.assertEqual(adaptive["status"], "COMPLETE")
                    self.assertEqual(adaptive["expanded"], ["definition", "note-2"])
                    self.assertEqual({b["page"] for b in adaptive["blocks"]}, {1, 2, 3})
