"""QUALITY-REVIEW contract checks, not observed model accuracy or human support."""

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError, canonical_json, strict_json
from deal_or_no_deal_ai.contracts import SynthesisWire, wire_json
from deal_or_no_deal_ai.model_comparison import (
    check_extraction_response, check_synthesis_response, prepare_extraction_task,
)
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.synthesis import prepare_synthesis
from tests.support import OfflineTest, ROOT


class ModelQualityTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.case = load_registered_case(ROOT)
        self.packet = prepare_synthesis(self.case)
        self.extraction = self.case.wire.model_dump()
        self.synthesis = strict_json((ROOT / "fixtures/development/e-n01/synthesis.default.json").read_bytes())

    def test_complete_source_context_keeps_exact_text_locations_periods_and_no_answers(self):
        task = prepare_extraction_task(ROOT, self.case)
        self.assertEqual(len(task["sources"]), 5)
        for block in self.case.inventory:
            actual = task["sources"][block.block_id]
            self.assertEqual(actual["text"], block.text)
            self.assertEqual(actual["source_sha256"], block.source.content_digest)
            self.assertEqual(actual["end"] - actual["start"], len(block.text))
            self.assertEqual(actual["dependencies"], list(block.dependencies))
        self.assertEqual(task["bases"]["FY-ASSESS"]["start"], "2027-01-01")
        self.assertEqual(task["review_basis"]["scope"]["subject_id"], self.case.scope.subject_id)
        self.assertNotIn(canonical_json(self.extraction), canonical_json(task))

    def test_mutated_or_unverified_source_never_becomes_a_ready_task(self):
        changed = replace(self.case, inventory=self.case.inventory[:-1])
        with self.assertRaisesRegex(InputError, "STALE_OR_MUTATED"):
            prepare_extraction_task(ROOT, changed)
        inventory = (replace(self.case.inventory[0], parser_verified=False), *self.case.inventory[1:])
        with patch("deal_or_no_deal_ai.model_comparison.validate_registered_case"), \
                self.assertRaisesRegex(InputError, "SOURCE_COVERAGE_UNVERIFIED"):
            prepare_extraction_task(ROOT, replace(self.case, inventory=inventory))

    def test_wrong_existing_page_is_visible_even_when_value_and_basis_match(self):
        raw = deepcopy(self.extraction)
        raw["financial_inputs"]["cash_available_for_debt_service"]["refs"] = ["AGREEMENT-P1"]
        result = check_extraction_response(canonical_json(raw), self.case)
        field = next(f for f in result["field_results"] if f["field"].endswith(".cash_available_for_debt_service"))
        self.assertTrue(field["value_match"])
        self.assertTrue(field["basis_match"])
        self.assertFalse(field["expected_reference_set_match"])
        self.assertEqual(result["unresolved_source_refs"], 0)
        self.assertEqual(field["semantic_support"], "MANUAL_REVIEW_REQUIRED")

    def test_missing_wrong_year_and_conflicts_are_not_hidden_by_one_average(self):
        raw = deepcopy(self.extraction)
        raw["financial_inputs"]["cash_available_for_debt_service"] = dict(value=None, refs=[], basis_id=None)
        raw["financial_inputs"]["net_income"]["basis_id"] = "FY-PREV"
        original = raw["terms"]["requested_amount"]
        raw["terms"]["requested_amount"] = dict(value=None, refs=[], basis_id=None)
        raw["conflicts"] = [dict(field_name="terms.requested_amount", candidates=[
            original, {**original, "value": "1300000"}])]
        result = check_extraction_response(canonical_json(raw), self.case)
        self.assertTrue(result["schema_valid"])
        self.assertIn("financial_inputs.cash_available_for_debt_service", result["missing_fields"])
        self.assertIn("terms.requested_amount", result["conflict_fields"])
        wrong = next(f for f in result["field_results"] if f["field"] == "financial_inputs.net_income")
        self.assertFalse(wrong["basis_match"])
        self.assertEqual(result["available_slots_exact_value_basis_match"], result["available_slots"] - 3)
        failed = check_extraction_response("not json", self.case)
        self.assertEqual(failed["available_slots"], result["available_slots"])
        self.assertEqual(failed["available_slots_exact_value_basis_match"], 0)

    def test_all_summary_fields_have_original_text_and_real_transitive_context(self):
        raw = deepcopy(self.synthesis)
        raw["panel_decision"].update(decision="Conditional Approve", conditions=["Review the cited annual projection."])
        raw["condition_links"] = [dict(index=0, refs=["calc:DSCR"])]
        raw["proposed_action"] = dict(kind="CONTINUE_STANDARD_REVIEW", target="Analyst",
                                     reason="Inspect the recorded annual analysis.", refs=["panel:FINANCIAL"])
        result = check_synthesis_response(wire_json(SynthesisWire.model_validate(raw)), self.case, self.packet)
        self.assertTrue(result["schema_valid"])
        self.assertEqual(len(result["narrative_targets"]), 6)
        target = next(t for t in result["narrative_targets"] if t["field_path"] == "panel_decision.rationale")
        self.assertEqual(target["text"], raw["panel_decision"]["rationale"])
        self.assertIn("FIN-P1", target["reference_closure"])
        self.assertIn("text", target["reference_closure"]["FIN-P1"])
        self.assertTrue(all(t["support"] == "MANUAL_REVIEW_REQUIRED" for t in result["narrative_targets"]))
        self.assertIsNone(result["credit_disposition"])

    def test_false_prose_with_real_citations_is_not_certified_by_reference_checks(self):
        raw = deepcopy(self.synthesis)
        raw["observations"][0]["text"] = "DSCR is 99 and full-term repayment is guaranteed."
        result = check_synthesis_response(wire_json(SynthesisWire.model_validate(raw)), self.case, self.packet)
        self.assertTrue(result["schema_valid"])
        self.assertEqual(result["reference_problems"], [])
        self.assertEqual(result["source_grounding"], "MANUAL_REVIEW_REQUIRED")
        self.assertIsNone(result["narrative_scores"])
        self.assertIsNone(result["ragas"])

    def test_unknown_reference_and_low_confidence_are_independent_diagnostics(self):
        raw = deepcopy(self.synthesis)
        raw["rationale_refs"] = ["not-a-current-source"]
        raw["panel_decision"]["confidence"] = Decimal("0.69")
        result = check_synthesis_response(wire_json(SynthesisWire.model_validate(raw)), self.case, self.packet)
        self.assertTrue(result["schema_valid"])
        self.assertEqual(len(result["reference_problems"]), 1)
        self.assertTrue(result["routing"]["mandatory_review_required"])
        self.assertFalse(result["routing"]["escalation_proposal_matches_controls"])
        self.assertIsNone(result["credit_disposition"])

    def test_wrong_packet_or_invalid_schema_never_produces_review_clearance(self):
        packet = deepcopy(self.packet)
        packet["request"]["review_basis"]["review_as_of"] = "2020-01-01"
        with self.assertRaisesRegex(InputError, "CURRENT_INPUT_MISMATCH"):
            check_synthesis_response(canonical_json(self.synthesis), self.case, packet)
        result = check_synthesis_response('{"wire_version":"SYN-WIRE-1.0"}', self.case, self.packet)
        self.assertFalse(result["schema_valid"])
        self.assertIsNone(result["routing"])
        self.assertIsNone(result["credit_disposition"])
