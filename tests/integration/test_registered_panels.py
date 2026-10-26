"""Actual M2 source/period/policy/score binding; full graph remains a later test."""

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.contracts import DealTermsWire
from deal_or_no_deal_ai.documents import verify_evidence
from deal_or_no_deal_ai.services import _binding, compute_financials, evaluate_panels, load_registered_case
from tests.support import OfflineTest, ROOT
from tools.run_e_n01_panels import run


class RegisteredPanelTests(OfflineTest):
    def test_actual_registered_source_to_panels_has_citations_and_no_final_decision(self):
        case = load_registered_case(ROOT)
        financial, compliance, risk = evaluate_panels(case)
        self.assertEqual(financial.completeness, "COMPLETE")
        self.assertEqual(len(case.inventory), 5)
        self.assertTrue(all(b.parser_verified and b.fit_verified for b in case.inventory))
        self.assertEqual(financial.covenant_status, "EXTRACTED_NOT_EVALUATED")
        self.assertEqual(risk.score.display, "21.00")
        self.assertEqual(risk.score.band, "LOW")
        self.assertEqual(compliance.exception_rule_ids, ())
        self.assertEqual(compliance.completeness, "PRE_SYNTHESIS")
        source_refs = dict(financial.metric_source_refs)
        self.assertIn("FIN-P2", source_refs["CALC-004"])
        self.assertIn("COLLATERAL-P1", source_refs["CALC-006"])
        report = run(ROOT)
        self.assertEqual(report["assessments"], dict(credit_risk="21", credit_band="LOW", policy_exceptions=0, missing_evidence=0))
        self.assertEqual(report["qa"]["false_positive_risk_count"], 0)
        self.assertIsNone(report["qa"]["risk_recall"])
        self.assertFalse(report["final_ready"])
        self.assertIsNone(report["final_decision"])
        self.assertFalse(report["graph_invoked"])
        self.assertFalse(report["live_human_supported"])

    def test_runtime_does_not_read_evaluator_gold_or_authoring_manuscripts(self):
        original_bytes, original_text = Path.read_bytes, Path.read_text

        def guarded_bytes(path, *args, **kwargs):
            if path.name == "gold.json" or "authoring" in path.parts:
                raise AssertionError("EVALUATOR_OR_AUTHORING_REFERENCE_READ_BY_RUNTIME")
            return original_bytes(path, *args, **kwargs)

        def guarded_text(path, *args, **kwargs):
            if path.name == "gold.json" or "authoring" in path.parts:
                raise AssertionError("EVALUATOR_OR_AUTHORING_REFERENCE_READ_BY_RUNTIME")
            return original_text(path, *args, **kwargs)

        with patch.object(Path, "read_bytes", guarded_bytes), patch.object(Path, "read_text", guarded_text):
            self.assertEqual(run(ROOT)["risk"]["score"]["total"], "21")

    def test_unsupported_mode_scenario_and_edited_extraction_never_inherit_default(self):
        for args in (dict(mode="LIVE"), dict(scenario_id="Six Flags"), dict(variant="extraction-miss")):
            with self.subTest(args=args), self.assertRaisesRegex(InputError, "UNAVAILABLE"):
                load_registered_case(ROOT, **args)
        case = load_registered_case(ROOT)
        data = case.wire.model_dump()
        data["financial_inputs"]["cash_available_for_debt_service"] = dict(value=None, refs=[], basis_id=None)
        wire = DealTermsWire.model_validate(data)
        changed = replace(case, wire=wire, dependency_digest=_binding(case.registration, case.scope, wire, case.case_data, case.inventory))
        with self.assertRaisesRegex(InputError, "UNREGISTERED_EXTRACTION_VARIANT"):
            compute_financials(changed)

    def test_scope_basis_unit_and_source_changes_fail_even_with_recomputed_local_digest(self):
        case = load_registered_case(ROOT)
        changes = []
        for key in ("deal_id", "subject_id", "facility_id", "revision"):
            changes.append(dict(scope=replace(case.scope, **{key: 2 if key == "revision" else "other"})))
        data = deepcopy(case.case_data)
        data["bases"]["FY-ASSESS"]["currency"] = "EUR"
        changes.append(dict(case_data=data))
        data2 = deepcopy(case.case_data)
        data2["bases"]["FY-ASSESS"]["end"] = "2026-12-31"
        changes.append(dict(case_data=data2))
        first, *rest = case.inventory
        changes.append(dict(inventory=(replace(first, page=99), *rest)))
        changes.append(dict(inventory=case.inventory[:-1]))
        for kwargs in changes:
            with self.subTest(changed=list(kwargs)):
                changed = replace(case, **kwargs)
                changed = replace(changed, dependency_digest=_binding(changed.registration, changed.scope, changed.wire,
                                                                       changed.case_data, changed.inventory))
                with self.assertRaises(InputError):
                    compute_financials(changed)

    def test_required_related_page_cannot_be_omitted_to_claim_complete_coverage(self):
        case = load_registered_case(ROOT)
        sources = tuple(dict.fromkeys(b.source for b in case.inventory))
        checked = verify_evidence(scope=case.scope, sources=sources, inventory=case.inventory,
                                  roots=("FIN-P1",), selected=("FIN-P1",), max_context_bytes=100000)
        self.assertEqual(checked.status, "INCOMPLETE")
        self.assertIn("FIN-P2", checked.missing)
        self.assertIn("COLLATERAL-P1", checked.missing)
        self.assertFalse(checked.dispatch_blocks)

    def test_registered_source_and_policy_bytes_are_checked_in_an_isolated_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            relative = ["config/registrations/e-n01.json", "config/sample_policy.json",
                        "fixtures/development/e-n01/manifest.json", "fixtures/development/e-n01/case.json",
                        "fixtures/development/e-n01/extraction.candidate.json",
                        "fixtures/development/e-n01/sources/agreement.pdf", "fixtures/development/e-n01/sources/financials.pdf",
                        "fixtures/development/e-n01/sources/collateral-and-assessments.pdf",
                        "docs/agents/extractor.md", "docs/agents/synthesizer.md", "docs/agents/shared-contract.md"]
            for name in relative:
                destination = target / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / name).read_bytes())
            self.assertEqual(evaluate_panels(load_registered_case(target))[2].score.display, "21.00")
            pdf = target / "fixtures/development/e-n01/sources/financials.pdf"
            original = pdf.read_bytes()
            pdf.write_bytes(original + b" altered")
            with self.assertRaisesRegex(InputError, "REGISTERED_SOURCE_CHANGED"):
                load_registered_case(target)
            pdf.write_bytes(original)
            policy = target / "config/sample_policy.json"
            policy.write_text(policy.read_text().replace('"1.25"', '"1.2"'), encoding="utf-8")
            with self.assertRaisesRegex(InputError, "POLICY_PROFILE_CHANGED"):
                load_registered_case(target)
