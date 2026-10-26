"""TEST-002-04/07, TEST-005-01/03/04/06 portions; requires Pydantic.

No skip-on-missing-dependency: ordinary discovery must fail until setup succeeds.
These paper examples are schema tests, not registered case/execution evidence.
"""

from copy import deepcopy
from decimal import Decimal
import json
import re

from pydantic import ValidationError

from deal_or_no_deal_ai.context import InputError, instruction_manifest, load_instruction, request_size
from deal_or_no_deal_ai.contracts import (
    DealTermsWire, Scope, SynthesisWire, hydrate_extraction, hydrate_narrative,
    parse_extraction, parse_synthesis, wire_json,
)
from tests.support import OfflineTest, ROOT, uid


def examples(path):
    return re.findall(r"~~~json\s*\n(.*?)~~~", (ROOT / path).read_text(encoding="utf-8"), re.S)


class WireTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.extraction = examples("docs/specs/examples/extraction-wire.md")[0]
        self.syntheses = examples("docs/specs/synthesis-evidence.md")
        self.scope = Scope(workspace_id=uid("workspace"), deal_id=uid("deal"), review_id=uid("review"),
                           run_id=uid("run"), thread_id=uid("thread"), input_revision=1)

    def test_complete_extraction_shape_and_missing_conflict_hydration(self):
        wire = parse_extraction(self.extraction)
        self.assertEqual(len(type(wire.terms).model_fields), 13)
        self.assertEqual(len(type(wire.financial_inputs).model_fields), 18)
        handles = {key: self.scope for key in ("P1", "P2", "P3", "P4")}
        bases = {key: self.scope for key in ("FY-ASSESS", "FY-PREV", "TXN-1")}
        facts = hydrate_extraction(wire, self.scope, uid("extract"), handles, bases)
        self.assertEqual(len(facts), 31)
        by_name = {item.field_name: item for item in facts}
        self.assertEqual(by_name["terms.use_of_proceeds"].status, "CONFLICT")
        self.assertEqual(by_name["terms.maturity_date"].status, "MISSING")
        self.assertEqual(by_name["financial_inputs.prior_ranking_liens"].value, Decimal("0"))
        self.assertTrue(all(item.support == "PENDING" for item in facts))
        self.assertEqual(parse_extraction(wire_json(wire)), wire)

    def test_extraction_rejects_extra_authority_and_wrong_field_types(self):
        original = json.loads(self.extraction)
        for field, bad in (("term_months", True), ("requested_amount", 1200000),
                           ("requested_amount", "0"), ("requested_amount", "-1"),
                           ("maturity_date", "Unknown")):
            candidate = deepcopy(original); candidate["terms"][field]["value"] = bad
            with self.subTest(field=field), self.assertRaises((InputError, ValidationError)):
                parse_extraction(json.dumps(candidate))
        for field in ("notes", "status", "source_refs"):
            candidate = deepcopy(original); candidate["terms"]["borrower"][field] = "forbidden"
            with self.subTest(field=field), self.assertRaises(ValidationError):
                parse_extraction(json.dumps(candidate))

    def test_out_of_scope_reference_never_hydrates(self):
        wire = parse_extraction(self.extraction)
        wrong = self.scope.model_copy(update={"deal_id": uid("another-deal")})
        with self.assertRaisesRegex(InputError, "OUT_OF_SCOPE"):
            hydrate_extraction(wire, self.scope, uid("extract"), {"P1": wrong}, {})

    def test_full_synthesis_roundtrips_all_narrative_fields(self):
        for raw in self.syntheses:
            wire = parse_synthesis(raw)
            refs = set(wire.rationale_refs)
            for observation in wire.observations: refs.update(observation.refs)
            for link in wire.condition_links: refs.update(link.refs)
            if wire.proposed_action: refs.update(wire.proposed_action.refs)
            targets = hydrate_narrative(wire, self.scope, uid("synthesis"),
                                        {ref: self.scope for ref in refs}, {"policy": "v1"})
            count = 4 + len(wire.panel_decision.conditions) + int(wire.proposed_action is not None)
            self.assertEqual(len(targets), count)
            self.assertTrue(all(item.support == "PENDING" for item in targets))
            self.assertEqual(parse_synthesis(wire_json(wire)), wire)

    def test_schema_advertises_numeric_confidence_and_exact_five_fields(self):
        schema = SynthesisWire.model_json_schema()
        decision = schema["$defs"]["PanelDecision"]
        self.assertEqual(set(decision["properties"]), {"decision", "confidence", "rationale", "conditions", "escalate_to_human"})
        self.assertEqual(decision["properties"]["confidence"]["type"], "number")

    def test_exact_confidence_and_number_emission(self):
        raw = self.syntheses[0].replace('0.85', '0.699999999999999999999999')
        wire = parse_synthesis(raw)
        self.assertLess(wire.panel_decision.confidence, Decimal("0.7"))
        self.assertIn('"confidence":0.699999999999999999999999', wire_json(wire))
        for value in ('"0.85"', 'true', 'NaN'):
            with self.subTest(value=value), self.assertRaises((InputError, ValidationError)):
                parse_synthesis(self.syntheses[0].replace('0.85', value))

    def test_missing_panels_bad_links_and_extra_authority_fail(self):
        original = json.loads(self.syntheses[1])
        candidates = []
        bad = deepcopy(original); bad["observations"][1]["panel"] = "FINANCIAL"; candidates.append(bad)
        bad = deepcopy(original); bad["condition_links"][0]["index"] = True; candidates.append(bad)
        bad = deepcopy(original); bad["panel_decision"]["approved"] = True; candidates.append(bad)
        bad = deepcopy(original); bad["condition_links"] = []; candidates.append(bad)
        for bad in candidates:
            with self.assertRaises(ValidationError): parse_synthesis(json.dumps(bad))

    def test_complete_schema_context_byte_measurement_does_not_claim_tokens(self):
        hashes = instruction_manifest(ROOT)
        for raw in self.syntheses:
            measurement = request_size(load_instruction(ROOT, "synthesizer", hashes["synthesizer"]),
                SynthesisWire.model_json_schema(), {"status": "TEST_DICTIONARY_NOT_SOURCE_PACK"},
                wire_json(parse_synthesis(raw)))
            self.assertGreater(measurement["schema"], 0)
            self.assertEqual(measurement["measurement"], "UTF8_BYTES_NOT_TOKENS")
