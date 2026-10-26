# E-N01 source pack and registered deterministic slice

Normal synthesis extension: config/registrations/e-n01-synthesis.json separately binds synthesis.default.json and synthesis.rubric.json to the existing registered case and exact semantic request. The response copies the approved ordinary SYN-WIRE-1.0 example, with explicit existing annual projection/transaction basis. It is AI-authored educational fixture data, not an observed model output, human semantic review or general lending rule. Original source files/manifest/case/extraction registration remain unchanged.

Current status: A1-A4 approved for educational use; source/assessment/default-extraction slice registered under CASE-REG-1.0. Full graph/synthesis/correction variants are not registered or executed. Synthetic material only.
User requested the next implementation step after the uploaded-document review.
This pack is newly authored; it does not copy or certify `test_deal.pdf`.

Current technical version:2-draft. The user approved installing pypdf and verifying
these PDFs; pypdf6.21.2 is installed/locked. All five current pages pass full
plain/layout text comparison and focused year/unit/qualification/zero-lien checks.
[Measured evidence](../../../docs/execution.md#m2-parser-installation-and-pdf-verification)
is separate from the authoring manifest. The user subsequently said “ok move with next steps” after the concrete A1-A4 request. [Registration](../../../config/registrations/e-n01.json) binds the exact current source/case/extraction/policy/instruction hashes. This is permission for the deterministic fixture slice, not real lending or a full graph result.

The original `history/1-draft/` is retained. Its first verification found two
apostrophe differences caused by omitted font encoding. Technical draft2 adds
explicit WinAnsi encoding without changing the financial text/assumptions. Printed
source-content version1 remains the same;2-draft identifies the corrected binary
edition and has new source/package hashes. Do not use history as current context.

## What is ready for review

The `authoring/` manuscripts produce three text PDFs, five pages in total:

1. [agreement.pdf](sources/agreement.pdf): one-page equipment term-loan summary.
2. [financials.pdf](sources/financials.pdf): two-page supplied annual projections and transaction schedule.
3. [collateral-and-assessments.pdf](sources/collateral-and-assessments.pdf): equipment evidence and explicitly authored assessment premises.

The financial amounts reuse the approved E-N01 worked example. All pages identify
the same fictional borrower/facility, state units and distinguish supplied annual
projections from actual results. The financial table deliberately puts the earlier
year first. Required debt-service qualifications continue on page2.

## Explicit assumptions approved by the user

| ID | Proposed case-specific detail | Boundary |
|---|---|---|
| A1 | Prepared2026-10-22; review/transaction2026-10-23; annual forecast2027 with comparable annual forecast2026; pro-forma balance/debt/collateral date2026-10-23 | These are authored dates/bases, not dates inferred from file metadata. Growth is between supplied forecasts, not historical performance |
| A2 | USD900,000 equipment purchase plus USD300,000 debt refinancing; stated maturity2030-10-23; no guarantees; annual statements covenant | Allocations/details complete the existing USD1.2M/48-month/fixed6% example; not a general lending rule |
| A3 | Fictional payment-current history and ordinary manufacturing cyclicality; explicit zero prior-ranking equipment liens | Newly authored scenario premises, not bureau, market, valuation or lien verification |
| A4 | Five authored factor ratings20/25/20/15/30, using the already approved30/20/20/20/10 weights | Python totals21, Low. User approved these fictional ratings; no ratio-to-grade mapping, PD or bank validation is implied |

KYC/sanctions fixtures are configured not required solely for this fictional case,
as the existing E-N01 design specifies; this is not a real-law applicability claim.
No generic credit approval or real financial decision follows from any value here.
There is no authored final PanelDecision in this candidate.

Author: AI-assisted fixture preparation. User approved the presented assumptions
for the educational example; reviewer qualifications/independent financial
validation were not established and are not asserted.

## Reproduce and inspect

From the repository root, using the approved local environment:

```powershell
.\.venv\Scripts\python.exe tools/prepare_e_n01.py --write
.\.venv\Scripts\python.exe tools/prepare_e_n01.py --check
.\.venv\Scripts\python.exe tools/verify_e_n01_pdfs.py
.\.venv\Scripts\python.exe tools/run_e_n01_panels.py
```

The standard-library writer emits only this fixed synthetic package. It is not a
PDF parser, upload handler, general PDF toolkit or runtime document service.
Authoring maps describe lines placed by the writer, not parser-discovered text or
measured glyph boxes. `manifest.json` records actual generated byte digests and
retains `parser_verified=false`, `case_approved=false` and `registered=false`.
These preserve the authoring snapshot, not current application permission;
actual parsed blocks/fidelity/source hashes are in the separate ignored
var/evaluations/e-n01-pdf-verification/report.json. The parse-only tool does not
resolve registration. services.py resolves the approved fixed synthetic source
profile from config/registrations/e-n01.json; its independent result is in
var/evaluations/e-n01-deterministic-panels.json. No Live support is granted.
The script does not register cases or change approvals. It refuses changed
generated files rather than overwriting an unexpected existing version.

`extraction.candidate.json` is a schema-checked authored stage candidate with
source/basis handles, not a model response or active canned result. `case.json`
contains draft applicability/assessment/source-basis metadata. `gold.json` holds
evaluator-only expected calculations and never enters runtime/model inputs.
Authoring-map offsets are only in the original manuscript line; a future parser
must supply and validate actual parsed-block spans/locations independently.

## Still required before a complete Fixture graph run

The default source/assessment/extraction slice now loads by exact digest and
produces scoped finance/policy/risk panels. Confidence remains NOT_EVALUATED,
PanelDecision is null and final_ready is false. Next implement stage-input-matched
synthesis/correction variants, the shared LangGraph/worker/budget/review/report
flow, and the agreed core branches. Broader malformed/scanned/resource/unfamiliar
layout checks remain prerequisites for generic uploads. Live needs its existing
support/provider/access/allowance prerequisites. Do not reuse this case's answers
for an altered document or another borrower.
