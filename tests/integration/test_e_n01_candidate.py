"""Candidate integrity and nonapproval, not a parsed or registered loan run."""

import hashlib
import json

from deal_or_no_deal_ai.contracts import parse_extraction
from deal_or_no_deal_ai.documents import OriginalBlock, ReviewScope, SourceVersion, verify_evidence
from tests.support import OfflineTest, ROOT


PACK = ROOT / "fixtures/development/e-n01"


class CandidateCaseTests(OfflineTest):
    def test_source_bytes_page_maps_and_candidate_wire_retain_draft_boundaries(self):
        manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
        case = json.loads((PACK / "case.json").read_text(encoding="utf-8"))
        wire = parse_extraction((PACK / "extraction.candidate.json").read_bytes())
        self.assertFalse(manifest["registered"])
        self.assertFalse(case["case_approved"])
        self.assertEqual(case["approved_assumption_ids"], [])
        self.assertEqual(manifest["package_digest"], case["package_digest"])
        self.assertEqual(len(manifest["sources"]), 3)
        self.assertEqual(manifest["page_count"], 5)
        self.assertLessEqual(manifest["byte_count"], 10000000)
        for source in manifest["sources"]:
            raw = (PACK / source["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), source["content_digest"])
            self.assertEqual(len(raw), source["byte_count"])
            self.assertFalse(source["parser_verified"])
        for handle, page in manifest["page_handles"].items():
            original = (PACK / page["manuscript"]).read_text(encoding="utf-8")
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), page["manuscript_sha256"])
            for paragraph in page["paragraphs"]:
                self.assertEqual(original[paragraph["start"]:paragraph["end"]], paragraph["text"])
            self.assertEqual(page["location_kind"], "AUTHORING_MAP_NOT_PARSER_OUTPUT")
        for group in (wire.terms, wire.financial_inputs):
            for value in group.__dict__.values():
                self.assertTrue(set(value.refs) <= manifest["page_handles"].keys())
                if value.basis_id:
                    self.assertIn(value.basis_id, case["bases"])
        self.assertTrue(all(a["status"] == "PROPOSED_NOT_USABLE" for a in case["factor_assessments"]))

    def test_full_authored_text_cannot_masquerade_as_verified_parsing_or_source_fit(self):
        manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
        case = json.loads((PACK / "case.json").read_text(encoding="utf-8"))
        scope = ReviewScope(**case["scope"], revision=1, basis_digest="UNAPPROVED-AUTHORING-BASIS")
        sources = tuple(SourceVersion(s["source_id"], s["version"], s["content_digest"]) for s in manifest["sources"])
        by_source = {s.source_id: s for s in sources}
        blocks = tuple(OriginalBlock(p["block_id"], scope, by_source[page["source_id"]], page["page"],
                                     p["start"], p["text"])
                       for page in manifest["page_handles"].values() for p in page["paragraphs"])
        self.assertLessEqual(len(blocks), 64)
        for mode in ("BASELINE", "ADAPTIVE"):
            result = verify_evidence(scope=scope, sources=sources, inventory=blocks, roots=(),
                                     selected=tuple(b.block_id for b in blocks), purpose="FULL_EXTRACTION",
                                     max_context_bytes=100000, mode=mode)
            self.assertEqual(result.status, "UNVERIFIED")
            self.assertIn("PARSER_OR_DEPENDENCIES_UNVERIFIED", result.reasons)
            self.assertIn("SOURCE_FIT_UNVERIFIED", result.reasons)
            self.assertFalse(result.dispatch_blocks)
