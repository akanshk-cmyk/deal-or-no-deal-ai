"""Exact E-N01 fixture support and pure rendering, not general model quality."""

from copy import deepcopy
from dataclasses import asdict, replace
from decimal import Decimal
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError, instruction_manifest, primitive
from deal_or_no_deal_ai.contracts import Scope, parse_synthesis
from deal_or_no_deal_ai.memo import ReportInput, SECTIONS, inert, render_memo
from deal_or_no_deal_ai.panel_codec import restore_compliance, restore_financial, restore_risk
from deal_or_no_deal_ai.services import compute_compliance, evaluate_panels, load_registered_case
from deal_or_no_deal_ai.synthesis import prepare_synthesis, synthesis_task, validate_fixture_synthesis
from tests.support import OfflineTest, ROOT, uid


class SynthesisMemoTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.case = load_registered_case(ROOT)
        self.packet = prepare_synthesis(self.case)
        self.scope = Scope(workspace_id=uid("normal-workspace"), deal_id=self.case.scope.deal_id,
            review_id=uid("normal-review"), run_id=uid("normal-run"), thread_id=uid("normal-thread"), input_revision=1)
        self.accepted = validate_fixture_synthesis(ROOT, self.case, self.packet, self.scope, uid("normal-operation"))

    def report_input(self, **changes):
        values = dict(scope=self.scope, packet=self.packet, synthesis=self.accepted,
                      events=(dict(sequence=1, run_id=self.scope.run_id, stage="pdf_input", event="stage_completed"),),
                      generation_time="2026-10-24T05:00:00+00:00")
        values.update(changes)
        return ReportInput(**values)

    def test_packet_is_current_three_panel_context_with_no_expected_response_or_rubric(self):
        task = synthesis_task(ROOT, self.case, self.packet)
        self.assertEqual(set(task["context"]) - {"references", "scope", "review_basis", "terms"},
                         {"financial", "compliance", "risk"})
        self.assertEqual(len(self.packet["request"]["financial"]["metrics"]), 9)
        self.assertEqual(self.packet["request"]["risk"]["score"]["total"], "21")
        self.assertEqual(self.packet["request"]["review_basis"]["financial_assessment_basis"]["start"], "2027-01-01")
        self.assertEqual(task["context"]["references"]["calc:DSCR"]["refs"], ["FIN-P2"])
        self.assertNotIn("wire_json", task)
        self.assertNotIn("rubric", task)
        self.assertNotIn("text", task["context"]["references"]["FIN-P2"])
        self.assertEqual(instruction_manifest(ROOT), self.case.registration.instruction_hashes)

    def test_four_targets_resolve_and_confidence_stays_exact_without_human_support(self):
        self.assertEqual(len(self.accepted["targets"]), 4)
        self.assertEqual({t["field_path"] for t in self.accepted["targets"]},
                         {"observations[0].text", "observations[1].text", "observations[2].text", "panel_decision.rationale"})
        self.assertTrue(all(t["support"] == "PENDING" for t in self.accepted["targets"]))
        wire = parse_synthesis(self.accepted["effective_wire_json"])
        self.assertEqual(wire.panel_decision.confidence, Decimal("0.85"))
        self.assertFalse(wire.panel_decision.escalate_to_human)
        self.assertIsNone(self.accepted["routing"]["human_disposition"])

    def test_altered_packet_scope_or_stage_fixture_is_not_matched_to_canned_answer(self):
        changed = deepcopy(self.packet)
        changed["request"]["financial"]["metrics"][3]["value"] = "0.5"
        with self.assertRaisesRegex(InputError, "CURRENT_INPUT_MISMATCH"):
            validate_fixture_synthesis(ROOT, self.case, changed, self.scope, uid("normal-operation"))
        with self.assertRaisesRegex(InputError, "CURRENT_INPUT_MISMATCH"):
            validate_fixture_synthesis(ROOT, self.case, self.packet,
                self.scope.model_copy(update={"deal_id": uid("other-deal")}), uid("normal-operation"))
        with TemporaryDirectory() as folder:
            local = Path(folder)
            (local / "config/registrations").mkdir(parents=True)
            (local / "fixtures/development/e-n01").mkdir(parents=True)
            shutil.copyfile(ROOT / "config/registrations/e-n01-synthesis.json", local / "config/registrations/e-n01-synthesis.json")
            for name in ("synthesis.default.json", "synthesis.rubric.json"):
                shutil.copyfile(ROOT / "fixtures/development/e-n01" / name, local / "fixtures/development/e-n01" / name)
            wire_path = local / "fixtures/development/e-n01/synthesis.default.json"
            wire_path.write_bytes(wire_path.read_bytes().replace(b'"Approve"', b'"Reject"'))
            with self.assertRaisesRegex(InputError, "FIXTURE_OR_RUBRIC_CHANGED"):
                validate_fixture_synthesis(local, self.case, self.packet, self.scope, uid("normal-operation"))

    def test_memo_is_deterministic_seven_sections_with_inline_exact_citations(self):
        with patch("builtins.open", side_effect=AssertionError("RENDERER_NO_FILES")), \
                patch("sqlite3.connect", side_effect=AssertionError("RENDERER_NO_DATABASE")):
            first = render_memo(self.report_input())
        self.assertEqual(first, render_memo(self.report_input()))
        self.assertEqual([line[3:] for line in first["markdown"].splitlines() if line.startswith("## ")], list(SECTIONS))
        self.assertIn("1\\.50", first["markdown"])
        self.assertIn("21\\.00", first["markdown"])
        self.assertIn("Not required by configured demo rules", first["markdown"])
        self.assertIn("Human disposition: None recorded", first["markdown"])
        self.assertIn("not HUMAN_SUPPORTED", first["markdown"])
        self.assertIn("Fixed annual rate 6%", first["markdown"])
        self.assertIn("matched: No", first["markdown"])
        self.assertNotIn("AWAITING", first["markdown"])
        self.assertEqual(self.packet["request"]["reference_dictionary"][
            "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-012"]["value"]["evaluation_state"], "NOT_EVALUATED")
        for item in first["citation_index"].values():
            self.assertIn("#### " + item["anchor"], first["markdown"])
        self.assertIn("](#cite-", first["markdown"])

    def test_render_rejects_stale_scope_changed_narrative_and_future_audit(self):
        changed = deepcopy(self.accepted)
        changed["wire_json"] = changed["wire_json"].replace("Annual DSCR", "Guaranteed repayment; annual DSCR")
        with self.assertRaisesRegex(InputError, "SYNTHESIS_CHANGED"):
            render_memo(self.report_input(synthesis=changed))
        with self.assertRaisesRegex(InputError, "SCOPE_OR_DIGEST"):
            render_memo(self.report_input(scope=self.scope.model_copy(update={"input_revision": 2})))
        future = (dict(sequence=1, run_id=self.scope.run_id, stage="report_generator", event="stage_completed"),)
        with self.assertRaisesRegex(InputError, "OWN_FUTURE_COMPLETION"):
            render_memo(self.report_input(events=future))

    def test_embedded_html_images_and_links_are_inert(self):
        escaped = inert('<script>alert(1)</script> ![image](https://example.invalid/x)')
        self.assertNotIn("<script>", escaped)
        self.assertNotIn("![image](", escaped)
        self.assertIn("&lt;script&gt;", escaped)

    def test_actual_panel_handoffs_roundtrip_exactly_and_produce_same_synthesis_packet(self):
        panels = evaluate_panels(self.case)
        restored = tuple(restore(primitive(asdict(panel))) for restore, panel in
                         zip((restore_financial, restore_compliance, restore_risk), panels))
        for before, after in zip(panels, restored):
            self.assertEqual(primitive(asdict(before)), primitive(asdict(after)))
        self.assertEqual(prepare_synthesis(self.case, panels=restored), self.packet)

    def test_handoffs_reject_unknown_schema_coerced_numbers_and_wrong_dependency(self):
        financial = evaluate_panels(self.case)[0]
        unknown = primitive(asdict(financial)); unknown["extra"] = "not allowed"
        with self.assertRaisesRegex(InputError, "EXACT_PANEL"):
            restore_financial(unknown)
        coerced = primitive(asdict(financial)); coerced["metric_results"][0]["value"] = 900000
        with self.assertRaisesRegex(InputError, "DECIMAL_STRING"):
            restore_financial(coerced)
        with self.assertRaisesRegex(InputError, "HANDOFF_SCOPE"):
            compute_compliance(self.case, replace(financial, dependency_digest="wrong"))
