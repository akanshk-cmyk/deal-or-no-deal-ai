"""Scoped TEST-011-01/03, TEST-006-05, TEST-003-06 and TEST-004-11."""

from dataclasses import asdict
from decimal import Decimal
import json
from pathlib import Path
import tempfile

from deal_or_no_deal_ai.context import InputError, canonical_json, fingerprint
from deal_or_no_deal_ai.storage import (
    RecordWrite, StateSnapshot, Store, apply_patch, decode_state, encode_state,
)
from tests.support import OfflineTest, snapshot


class CodecTests(OfflineTest):
    def test_exact_roundtrip_across_reopened_sqlite(self):
        original = snapshot()
        before = fingerprint("TEST_SNAPSHOT", asdict(original))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "shared.sqlite3"
            store = Store(path); store.initialize()
            store.put_record(RecordWrite("snapshot", "TEST_SNAPSHOT", encode_state(original)))
            version, saved = Store(path).get_record("snapshot")
        restored = decode_state(saved)
        self.assertEqual(version, 1)
        self.assertEqual(restored, original)
        self.assertLess(restored.confidence, Decimal("0.7"))
        self.assertGreater(restored.risk_score, Decimal("25"))
        self.assertEqual(restored.financial_inputs["prior_ranking_liens"], Decimal("0"))
        self.assertIsNone(restored.financial_inputs["net_income"])
        self.assertEqual(fingerprint("TEST_SNAPSHOT", asdict(restored)), before)

    def test_unknown_versions_types_and_schemas_fail_without_migration(self):
        saved = encode_state(snapshot())
        for key in ("schema_version", "state_codec_version"):
            with self.assertRaises(InputError):
                decode_state({**saved, key: "unknown"})
        for confidence in (0.7, "NaN", "0.70", True):
            with self.subTest(value=confidence), self.assertRaises((InputError, ValueError)):
                decode_state({**saved, "snapshot": {**saved["snapshot"], "confidence": confidence}})
        with self.assertRaises(InputError):
            decode_state({**saved, "snapshot": {**saved["snapshot"], "client": "forbidden"}})

    def test_null_clears_differ_from_omission_and_identity_cannot_change(self):
        original = snapshot()
        self.assertEqual(apply_patch(original, {}).report_markdown, "Historical report")
        updated = apply_patch(original, {"report_markdown": None, "panel_refs": []})
        restored = decode_state(json.loads(canonical_json(encode_state(updated))))
        self.assertIsNone(restored.report_markdown)
        self.assertEqual(restored.panel_refs, [])
        with self.assertRaises(InputError):
            apply_patch(original, {"input_revision": 2})

    def test_invalid_state_fails_instead_of_guessing(self):
        for changes in ({"confidence": "0.7"}, {"risk_score": Decimal("101")},
                        {"financial_inputs": {"made_up": Decimal("1")}}, {"input_revision": True}):
            with self.subTest(changes=changes), self.assertRaises(InputError):
                snapshot(**changes)
