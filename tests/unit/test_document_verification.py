"""DOCVERIFY portions of TEST-001-04 and TEST-006-02/03/05/07."""

from dataclasses import replace
from decimal import Decimal

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.documents import align_table_value, verify_evidence
from tests.document_verification_cases import SCOPE, SOURCE, block, disclosure_blocks, table_inputs
from tests.support import OfflineTest


class DocumentVerificationTests(OfflineTest):
    def check(self, **changes):
        args = dict(scope=SCOPE, sources=(SOURCE,), inventory=disclosure_blocks(),
                    roots=("disclosure",), selected=("disclosure",), max_context_bytes=20000)
        return verify_evidence(**(args | changes))

    def test_baseline_withholds_missing_context_adaptive_restores_exact_originals(self):
        baseline, adaptive = self.check(), self.check(mode="ADAPTIVE")
        self.assertEqual(baseline.status, "INCOMPLETE")
        self.assertEqual(baseline.dispatch_blocks, ())
        self.assertEqual(adaptive.status, "COMPLETE")
        self.assertEqual(adaptive.dispatch_blocks, tuple(sorted(disclosure_blocks(), key=lambda b: b.block_id)))
        self.assertEqual(adaptive.required, ("definition", "disclosure", "note-2"))
        self.assertIsNotNone(adaptive.packet_digest)

    def test_absent_qualifier_and_unverified_fidelity_never_become_complete(self):
        absent = self.check(mode="ADAPTIVE", inventory=disclosure_blocks()[:1])
        self.assertEqual(absent.status, "INCOMPLETE")
        self.assertEqual(absent.missing, ("note-2",))
        for field in ("parser_verified", "fit_verified"):
            with self.subTest(field=field):
                inventory = (replace(disclosure_blocks()[0], **{field: False}), *disclosure_blocks()[1:])
                result = self.check(mode="ADAPTIVE", inventory=inventory)
                self.assertEqual(result.status, "UNVERIFIED")
                self.assertFalse(result.dispatch_blocks)

    def test_cross_deal_revision_subject_facility_basis_and_source_are_denied(self):
        original = disclosure_blocks()[0]
        scopes = [replace(SCOPE, **{field: value}) for field, value in (
            ("deal_id", "other"), ("revision", 2), ("subject_id", "other"),
            ("facility_id", "other"), ("basis_digest", "changed"))]
        variants = [replace(original, scope=scope) for scope in scopes]
        variants += [replace(original, source=replace(SOURCE, **{field: "changed"}))
                     for field in ("source_id", "version", "content_digest")]
        for changed in variants:
            with self.subTest(changed=changed):
                result = self.check(mode="ADAPTIVE", inventory=(changed, *disclosure_blocks()[1:]))
                self.assertEqual(result.status, "UNVERIFIED")
                self.assertFalse(result.dispatch_blocks)

    def test_byte_equality_accepts_overflow_never_truncates(self):
        measured = self.check(mode="ADAPTIVE")
        self.assertEqual(self.check(mode="ADAPTIVE", max_context_bytes=measured.context_bytes).status, "COMPLETE")
        over = self.check(mode="ADAPTIVE", max_context_bytes=measured.context_bytes - 1)
        self.assertEqual(over.status, "UNVERIFIED")
        self.assertIn("CONTEXT_BYTE_LIMIT", over.reasons)
        self.assertFalse(over.dispatch_blocks)
        self.assertEqual(over.context_bytes, measured.context_bytes)

    def test_full_extraction_requires_inventory_not_only_discovered_field(self):
        extra = block("unselected-amendment", "Material covenant amendment.", role="QUALIFIER")
        inventory = (*disclosure_blocks(), extra)
        checked = self.check(inventory=inventory, purpose="FULL_EXTRACTION",
                             selected=tuple(b.block_id for b in disclosure_blocks()))
        self.assertEqual(checked.status, "INCOMPLETE")
        self.assertIn("unselected-amendment", checked.missing)
        self.assertEqual(self.check(inventory=inventory, purpose="FULL_EXTRACTION", mode="ADAPTIVE").status,
                         "COMPLETE")
        missing_selection = self.check(purpose="FULL_EXTRACTION", mode="ADAPTIVE", selected=("not-in-inventory",))
        self.assertEqual(missing_selection.status, "INCOMPLETE")
        self.assertFalse(missing_selection.dispatch_blocks)

    def test_cycles_deduplicate_and_work_limits_fail_closed(self):
        inventory = (block("a", "A", dependencies=("b",)), block("b", "B", dependencies=("a",)))
        result = self.check(inventory=inventory, roots=("a",), selected=("a",), mode="ADAPTIVE")
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(len(result.dispatch_blocks), 2)
        oversized = tuple(block(str(i), "Synthetic") for i in range(65))
        stopped = self.check(inventory=oversized, mode="ADAPTIVE")
        self.assertEqual(stopped.status, "UNVERIFIED")
        self.assertFalse(stopped.dispatch_blocks)
        self.assertEqual(self.check(roots=(), selected=()).status, "UNVERIFIED")

    def test_versions_duplicates_and_original_locations_fail_closed(self):
        first, *rest = disclosure_blocks()
        for invalid in ((first, first, *rest), (replace(first, page=0), *rest),
                        (replace(first, start=-1), *rest), (replace(first, text=""), *rest)):
            with self.subTest(inventory=invalid):
                self.assertEqual(self.check(inventory=invalid).status, "UNVERIFIED")
        self.assertEqual(self.check(sources=(SOURCE, SOURCE)).status, "UNVERIFIED")
        with self.assertRaises(InputError):
            replace(first, parser_verified="true")
        with self.assertRaises(InputError):
            self.check(mode="UNSAFE")

    def test_context_and_original_location_changes_invalidate_identity(self):
        original = self.check(mode="ADAPTIVE").packet_digest
        first, *rest = disclosure_blocks()
        for changes in (dict(text=first.text + " Updated."), dict(page=4), dict(start=20)):
            with self.subTest(changes=changes):
                result = self.check(mode="ADAPTIVE", inventory=(replace(first, **changes), *rest))
                self.assertEqual(result.status, "COMPLETE")
                self.assertNotEqual(result.packet_digest, original)
        self.assertEqual(self.check(mode="ADAPTIVE", inventory=tuple(reversed(disclosure_blocks()))).packet_digest,
                         original)

    def test_alignment_uses_requested_period_and_preserves_unscaled_original_value(self):
        result = align_table_value(**table_inputs())
        self.assertEqual(result.status, "KNOWN")
        self.assertEqual(result.value.value, "120")
        self.assertEqual(result.value.scale, "1000")
        self.assertEqual(result.value.required_blocks, ("current-cell", "current-header", "revenue-label", "units"))
        args = table_inputs()
        without_label = tuple(b for b in args["inventory"] if b.block_id != "revenue-label")
        self.assertEqual(align_table_value(**(args | dict(inventory=without_label))).status, "UNVERIFIED")

    def test_alignment_rejects_noncanonical_cell_and_invalid_geometry(self):
        args = table_inputs()
        inventory = tuple(replace(b, text="1.20e2") if b.block_id == "current-cell" else b
                          for b in args["inventory"])
        self.assertEqual(align_table_value(**(args | dict(inventory=inventory))).reason,
                         "NONCANONICAL_NUMERIC_CELL")
        for number in (Decimal("NaN"), Decimal("Infinity"), Decimal(90), 1.5):
            with self.subTest(number=number):
                headers = (args["headers"][0], replace(args["headers"][1], x0=number))
                self.assertEqual(align_table_value(**(args | dict(headers=headers))).status, "UNVERIFIED")

    def test_repeated_header_context_is_not_an_extra_financial_observation(self):
        args = table_inputs()
        repeated = replace(args["headers"][1], layout_id="fragment-2")
        moved = replace(args["cells"][1], layout_id="fragment-2")
        result = align_table_value(**(args | dict(headers=(*args["headers"], repeated),
                                                    cells=(args["cells"][0], moved))))
        self.assertEqual(result.status, "KNOWN")
        self.assertEqual(result.value.value, "120")
