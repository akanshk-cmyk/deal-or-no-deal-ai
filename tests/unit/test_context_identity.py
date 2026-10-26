"""Scoped portions of TEST-002-04/07 and TEST-006-01/04/05/08."""

from decimal import Decimal, localcontext
import json
import socket
import tempfile
import tomllib
from pathlib import Path

from deal_or_no_deal_ai.context import (
    InputError, canonical_decimal, canonical_json, exact_confidence, fingerprint,
    instruction_manifest, load_instruction, money_string, narrative_parent,
    request_size, strict_json,
)
from deal_or_no_deal_ai.configuration import load_configuration
from tests.support import OfflineTest, ROOT


class InputAndContextTests(OfflineTest):
    def test_nested_and_escaped_duplicate_keys_fail(self):
        for raw in ('{"a":{"decision":1,"decision":2}}',
                    '{"a":{"x":1,"\\u0078":2}}'):
            with self.subTest(raw=raw), self.assertRaisesRegex(InputError, "DUPLICATE"):
                strict_json(raw)

    def test_bounded_parser_rejects_resource_and_unicode_errors(self):
        cases = ['{"x":NaN}', '{"x":Infinity}', '{"x":1e999999}',
                 '{"x":1234567890123456789}', '{"x":"\\ud800"}',
                 '{"x":' + '[' * 12 + '0' + ']' * 12 + '}',
                 json.dumps({"x": list(range(65))}), json.dumps({"x": "a" * 4097}),
                 '{"x":0}{}', '[]', '{"x":"' + 'a' * 65536 + '"}']
        for raw in cases:
            with self.subTest(prefix=raw[:25]), self.assertRaises(InputError):
                strict_json(raw)

    def test_confidence_preserves_exact_boundary(self):
        low = strict_json('{"confidence":0.699999999999999999999999}')['confidence']
        self.assertLess(exact_confidence(low), Decimal("0.7"))
        self.assertEqual(exact_confidence(strict_json('{"confidence":7e-1}')["confidence"]), Decimal("0.7"))
        for invalid in (True, "0.7", 0.7, Decimal("NaN"), Decimal("1.1")):
            with self.subTest(value=repr(invalid)), self.assertRaises(InputError):
                exact_confidence(invalid)

    def test_money_rejects_coercion_and_noncanonical_forms(self):
        for good in ("0", "-50000", "999999999999999999.999999", "0.000001"):
            self.assertEqual(money_string(good), good)
        for bad in (True, 0, "-0", "1.00", "01", "+1", "1e3", "1,000", "0.0000001"):
            with self.subTest(value=bad), self.assertRaises(InputError):
                money_string(bad)

    def test_canonicalization_is_exact_and_order_aware(self):
        with localcontext() as context:
            context.prec = 2
            self.assertEqual(canonical_decimal(Decimal("123456789.123400")), "123456789.1234")
        self.assertEqual(canonical_decimal(Decimal("-0")), "0")
        self.assertEqual(fingerprint("X", {"b": {"P2", "P1"}, "a": Decimal("1.00")}),
                         fingerprint("X", {"a": Decimal("1"), "b": {"P1", "P2"}}))
        self.assertNotEqual(fingerprint("X", ["first", "second"]), fingerprint("X", ["second", "first"]))
        self.assertNotEqual(fingerprint("X", None), fingerprint("X", 0))
        self.assertNotEqual(fingerprint("X", "café"), fingerprint("X", "cafe\u0301"))
        with self.assertRaises(InputError):
            canonical_json({"unsupported_float": 0.7})

    def test_runtime_only_instructions_and_hash_enforcement(self):
        with (ROOT / "config/model.toml").open("rb") as stream:
            hashes = tomllib.load(stream)["instructions"]
        text = load_instruction(ROOT, "extractor", hashes["extractor"])
        self.assertIn("DealTermsWire", text)
        self.assertNotIn("## Engineering authority", text)
        self.assertNotIn("## Required checks", text)
        with self.assertRaisesRegex(InputError, "HASH_MISMATCH"):
            load_instruction(ROOT, "extractor", "0" * 64)
        with self.assertRaisesRegex(InputError, "ROLE_NOT_ALLOWED"):
            load_instruction(ROOT, "compliance", "0" * 64)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); target = root / "docs/agents"; target.mkdir(parents=True)
            (target / "shared-contract.md").write_text("## Model context rules\nOne\n", encoding="utf-8")
            (target / "extractor.md").write_text("## Runtime prompt\nOne\n## Runtime prompt\nTwo\n", encoding="utf-8")
            with self.assertRaisesRegex(InputError, "AMBIGUOUS"):
                instruction_manifest(root)

    def test_narrative_hash_has_no_self_reference(self):
        wire = {key: [] for key in ("panel_decision", "observations", "rationale_refs", "condition_links")}
        wire.update(wire_version="SYN-WIRE-1.0", proposed_action=None)
        base = narrative_parent(wire, {"sources": "v1"})
        self.assertEqual(base, narrative_parent({**wire, "parent_digest": base, "evidence_target_refs": ["id"]}, {"sources": "v1"}))
        self.assertNotEqual(base, narrative_parent(wire, {"sources": "v2"}))

    def test_byte_measurement_is_not_tokens(self):
        value = request_size("é", {}, {}, {})
        self.assertEqual(value["measurement"], "UTF8_BYTES_NOT_TOKENS")
        self.assertEqual(value["instructions"], 4)  # JSON quotes plus UTF-8 é.

    def test_configuration_opens_no_database_and_network_is_denied(self):
        config = load_configuration(ROOT)
        self.assertEqual(config.mode, "FIXTURE")
        self.assertTrue(config.database.is_relative_to(ROOT))
        with self.assertRaisesRegex(AssertionError, "NETWORK_FORBIDDEN"):
            socket.create_connection(("example.invalid", 443))

    def test_explicit_execution_source_config_is_validated_without_activation(self):
        from shutil import copyfile
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/"config").mkdir()
            for name in ("app.toml","model.toml"):
                copyfile(ROOT/"config"/name,root/"config"/name)
            path=root/"config/app.toml"
            original=path.read_text()
            path.write_text(original.replace('mode = "FIXTURE"','mode = "LIVE"'))
            self.assertEqual(load_configuration(root).mode,"LIVE")
            self.assertFalse((root/"var").exists())
            path.write_text(original.replace('mode = "FIXTURE"','mode = "AUTO"'))
            with self.assertRaises(ValueError):
                load_configuration(root)
            path.write_text(original.replace('tracing_enabled = false','tracing_enabled = true'))
            with self.assertRaises(ValueError):
                load_configuration(root)

    def test_envelope_and_embedded_content_have_separate_bounds(self):
        raw = json.dumps({"content": "a" * 5000})
        self.assertEqual(len(strict_json(raw, envelope=True)["content"]), 5000)
        with self.assertRaisesRegex(InputError, "STRING_LIMIT"):
            strict_json(raw)
