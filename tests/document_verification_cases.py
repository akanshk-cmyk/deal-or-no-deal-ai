"""Synthetic parsed-block cases and gold, never loaded by application code."""

from dataclasses import asdict, dataclass, replace
from datetime import date
from decimal import Decimal
from time import perf_counter

from deal_or_no_deal_ai.context import fingerprint
from deal_or_no_deal_ai.documents import (
    ColumnHeader, NumericCell, OriginalBlock, ReviewScope, SourceVersion,
    StatementPeriod, align_table_value, verify_evidence,
)


SCOPE = ReviewScope("synthetic-deal", 1, "synthetic-borrower", "synthetic-facility", "basis-1")
SOURCE = SourceVersion("synthetic-statements", "1", "synthetic-content-digest-1")
CURRENT = StatementPeriod(date(2025, 12, 31), date(2025, 1, 1))
PRIOR = StatementPeriod(date(2024, 12, 31), date(2024, 1, 1))


def block(key, text, *, page=1, role="BODY", dependencies=(), **changes):
    return OriginalBlock(key, SCOPE, SOURCE, page, 0, text, role, dependencies,
                         parser_verified=True, fit_verified=True, **changes)


def table_inputs():
    """Prior year is left, current year right: first-number heuristics fail."""
    inventory = (
        block("prior-header", "Year ended 31 December 2024", role="PERIOD"),
        block("current-header", "Year ended 31 December 2025", role="PERIOD"),
        block("units", "USD thousands; standalone borrower statements", role="UNIT"),
        block("revenue-label", "Revenue"),
        block("prior-cell", "100"), block("current-cell", "120"),
    )
    return dict(
        scope=SCOPE, source=SOURCE, inventory=inventory,
        headers=(ColumnHeader("prior-header", "fragment-1", PRIOR, Decimal(10), Decimal(40)),
                 ColumnHeader("current-header", "fragment-1", CURRENT, Decimal(50), Decimal(80))),
        cells=(NumericCell("prior-cell", "fragment-1", "revenue", "revenue-label", Decimal(20), Decimal(30)),
               NumericCell("current-cell", "fragment-1", "revenue", "revenue-label", Decimal(60), Decimal(70))),
        metric="revenue", period=CURRENT, currency="USD", scale="1000", basis="standalone",
        units_block_id="units", expected_currency="USD", expected_scale="1000",
        expected_basis="standalone",
    )


def disclosure_blocks():
    return (
        block("disclosure", "The borrower recognizes service revenue on delivery. See Note 2.",
              page=2, dependencies=("note-2",)),
        block("note-2", "Except for bundled contracts, for which recognition follows acceptance; see definition.",
              page=3, role="QUALIFIER", dependencies=("definition",)),
        block("definition", "Acceptance means documented customer sign-off.", page=1, role="FOOTNOTE"),
    )


@dataclass(frozen=True)
class VerificationCase:
    name: str
    question: str
    inventory: tuple[OriginalBlock, ...]
    roots: tuple[str, ...]
    selected: tuple[str, ...]
    table: dict | None
    # Evaluator-only labels below; never passed to application helpers.
    alignment: str | None
    expected_value: str | None
    baseline_status: str
    adaptive_status: str
    required_gold: tuple[str, ...]
    gold_period: StatementPeriod | None = None
    gold_currency: str | None = None
    gold_scale: str | None = None


def cases():
    table = table_inputs()
    all_ids = tuple(b.block_id for b in table["inventory"])
    rows = [VerificationCase(
        "reversed-years", "What was 2025 revenue, in the statement's units?", table["inventory"],
        (), all_ids, table, "KNOWN", "120", "COMPLETE", "COMPLETE",
        ("current-cell", "current-header", "revenue-label", "units"),
        CURRENT, "USD", "1000",
    )]
    prior = dict(table, period=PRIOR)
    rows.append(replace(rows[0], name="prior-year-question", question="What was 2024 revenue?",
                        table=prior, expected_value="100",
                        gold_period=PRIOR,
                        required_gold=("prior-cell", "prior-header", "revenue-label", "units")))
    shifted_inventory = tuple(replace(b, page=3 if b.block_id.endswith("cell") or b.block_id == "revenue-label" else 2)
                              for b in table["inventory"])
    shifted = dict(table, inventory=shifted_inventory,
                   headers=tuple(replace(h, layout_id="mapped-fragment-2", x0=h.x0 + 100, x1=h.x1 + 100)
                                 for h in table["headers"]),
                   cells=tuple(replace(c, layout_id="mapped-fragment-2", x0=c.x0 + 100, x1=c.x1 + 100)
                               for c in table["cells"]))
    rows.append(replace(rows[0], name="mapped-shifted-cross-page-table", table=shifted, inventory=shifted_inventory))
    for name, changed, alignment in (
        ("missing-year-header", dict(table, headers=table["headers"][:1]), "UNVERIFIED"),
        ("unknown-shifted-fragment", dict(table, cells=tuple(
            replace(c, layout_id="unmapped-fragment") for c in table["cells"])), "UNVERIFIED"),
        ("overlapping-year-columns", dict(table, headers=(table["headers"][0],
            replace(table["headers"][1], x0=Decimal(30)))), "UNVERIFIED"),
        ("duplicate-current-year-cell", dict(table, cells=table["cells"] + (table["cells"][1],)), "CONFLICT"),
        ("different-unit-scale", dict(table, expected_scale="1"), "UNVERIFIED"),
        ("different-accounting-basis", dict(table, expected_basis="consolidated"), "UNVERIFIED"),
        ("unsupported-year", dict(table, period=StatementPeriod(date(2023, 12, 31), date(2023, 1, 1))), "MISSING"),
    ):
        rows.append(replace(rows[0], name=name, table=changed, alignment=alignment,
                            expected_value=None, baseline_status="WITHHELD_ALIGNMENT",
                            adaptive_status="WITHHELD_ALIGNMENT", required_gold=()))
    disclosure = disclosure_blocks()
    full = tuple(b.block_id for b in disclosure)
    rows.append(VerificationCase(
        "cross-page-disclosure", "What qualification applies to this borrower's service-revenue disclosure?",
        disclosure, ("disclosure",), ("disclosure",), None, None, None,
        "INCOMPLETE", "COMPLETE", full,
    ))
    rows.append(replace(rows[-1], name="already-complete-disclosure", selected=full,
                        baseline_status="COMPLETE"))
    rows.append(replace(rows[-2], name="physically-missing-qualifier", inventory=disclosure[:1],
                        adaptive_status="INCOMPLETE"))
    rows.append(replace(rows[-3], name="unverified-disclosure-parse", inventory=(
        replace(disclosure[0], parser_verified=False), *disclosure[1:]),
        baseline_status="UNVERIFIED", adaptive_status="UNVERIFIED"))
    return tuple(rows)


def run_case(case, mode):
    """Measure deterministic controls only; expected/gold fields stay outside."""
    started = perf_counter()
    alignment = align_table_value(**case.table) if case.table else None
    if alignment and alignment.status != "KNOWN":
        return dict(status="WITHHELD_ALIGNMENT", alignment=alignment.status, reason=alignment.reason,
                    value=None, period=None, currency=None, scale=None, source=None, blocks=[],
                    expanded=[], context_bytes=0, duration_ms=(perf_counter() - started) * 1000)
    roots = alignment.value.required_blocks if alignment else case.roots
    checked = verify_evidence(scope=SCOPE, sources=(SOURCE,), inventory=case.inventory,
                              roots=roots, selected=case.selected, mode=mode, max_context_bytes=20000)
    value = alignment.value if alignment and checked.status == "COMPLETE" else None
    return dict(status=checked.status, alignment=alignment.status if alignment else None,
                reason=list(checked.reasons), value=value.value if value else None,
                period=asdict(value.period) if value else None, currency=value.currency if value else None,
                scale=value.scale if value else None, source=asdict(value.source) if value else None,
                blocks=[dict(block_id=b.block_id, page=b.page, text=b.text) for b in checked.dispatch_blocks],
                expanded=list(checked.expanded), context_bytes=checked.context_bytes,
                duration_ms=(perf_counter() - started) * 1000)


def compare_cases():
    results = []
    for case in cases():
        inputs = dict(question=case.question, inventory=[asdict(b) for b in case.inventory],
                      roots=case.roots, selected=case.selected, table=case.table)
        if case.table:
            inputs["table"] = {k: ([asdict(v) for v in value] if k in ("inventory", "headers", "cells")
                                  else asdict(value) if k in ("scope", "source", "period") else value)
                               for k, value in case.table.items()}
        input_digest = fingerprint("DOCVERIFY-PAIRED-INPUT-1.0", inputs)
        arms = {}
        for mode, expected in (("BASELINE", case.baseline_status), ("ADAPTIVE", case.adaptive_status)):
            actual = run_case(case, mode)
            failures = []
            if actual["status"] != expected:
                failures.append("STATUS")
            if actual["alignment"] != case.alignment:
                failures.append("ALIGNMENT")
            if actual["status"] == "COMPLETE":
                if actual["value"] != case.expected_value:
                    failures.append("VALUE")
                if not set(case.required_gold) <= {b["block_id"] for b in actual["blocks"]}:
                    failures.append("MISSING_GOLD_CONTEXT")
                if case.table and (actual["period"] != asdict(case.gold_period)
                                   or actual["currency"] != case.gold_currency
                                   or actual["scale"] != case.gold_scale
                                   or actual["source"] != asdict(SOURCE)):
                    failures.append("PERIOD_UNITS_OR_SOURCE")
                originals = {b.block_id: b for b in case.inventory}
                if any(b["text"] != originals[b["block_id"]].text or b["page"] != originals[b["block_id"]].page
                       for b in actual["blocks"]):
                    failures.append("ALTERED_ORIGINAL_LOCATION")
            elif actual["value"] is not None or actual["blocks"]:
                failures.append("UNSAFE_OUTPUT")
            arms[mode] = dict(input_digest=input_digest, expected_status=expected,
                              checks_passed=not failures, failures=failures, **actual)
        results.append(dict(case_id=case.name, question=case.question, arms=arms))
    return dict(
        protocol="DOCVERIFY-1.0", evidence_type="APPLICATION_TEST", cases=results,
        unique_case_count=len(results), paired_execution_count=2 * len(results),
        failures=sum(not a["checks_passed"] for r in results for a in r["arms"].values()),
        summary={mode: dict(
            complete_packets=sum(r["arms"][mode]["status"] == "COMPLETE" for r in results),
            withheld=sum(r["arms"][mode]["status"] != "COMPLETE" for r in results),
            blocks_added=sum(len(r["arms"][mode]["expanded"]) for r in results),
            measured_local_duration_ms=sum(r["arms"][mode]["duration_ms"] for r in results),
        ) for mode in ("BASELINE", "ADAPTIVE")},
        default_mode="BASELINE", adaptive_adopted=False,
        model_tokens=None, model_cost_usd=None, provider_latency_ms=None,
        not_run=["PDF parser fidelity", "LLM answer quality", "VECTOR/HYBRID retrieval", "RAGAS"],
    )
