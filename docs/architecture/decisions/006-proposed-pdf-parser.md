# ADR-006 — Proposed text-PDF parser for the educational MVP

Status: ACCEPTED for local installation/known-corpus verification; pypdf6.21.2 installed and tested.
Date: 2026-10-23
Scope: SPEC-001/006 and the first E-N01 source pack. No project license selected.

## Approved decision and boundary

The user explicitly instructed: install the parser and verify these PDFs.
This accepts the proposed pypdf BSD-3-Clause dependency for the local E-N01
compatibility check. uv resolved/installed6.21.2 and updated pyproject/uv.lock;
installed license metadata and license-file digest were inspected. It replaces
the earlier unselected PyMuPDF candidate. No project license, general-upload
acceptance, A1-A4 assumption approval or fixture registration follows.

The earlier [AGENTS.md](../../../AGENTS.md) parser-license checkpoint required a
recorded choice. This explicit user instruction fulfills it for pypdf; do not
ask for installation approval again. Other case/provider/license gates remain.

## Options and evidence checked

| Option | Officially documented facts | Implication for this project |
|---|---|---|
| pypdf | BSD-3-Clause-style license; documented PdfReader and layout-mode text extraction | Recommend a compatibility trial over the small text PDFs. Retain applicable notices/terms; a dependency does not choose the project's license |
| PyMuPDF | Official documentation lists AGPL and commercial license paths, plus extraction/rendering capabilities | Keep as an alternative pending an explicit license-path decision; no purchase or installation is authorized |

Sources checked2026-10-23: [pypdf upstream license](https://github.com/py-pdf/pypdf/blob/main/LICENSE),
[pypdf text extraction and limitations](https://pypdf.readthedocs.io/en/stable/user/extract-text.html),
[PyMuPDF documentation](https://pymupdf.readthedocs.io/en/latest/about.html).
These verify documented capabilities/terms, not this project's compatibility or
legal compliance. No dependency version is pinned from a webpage alone.

## Trade-offs and failure behavior

pypdf's layout text is not a verified financial-table parser or a PDF-page image
renderer. Its documentation warns about difficult/incorrect coordinates on
complex pages and extraction resource use. Do not promise accurate glyph boxes,
merged-cell interpretation or automatic semantic header/footnote discovery.
Use exact source/page/text fallback where highlights are unavailable. Unknown
columns, units, qualifiers or essential parse fidelity remain UNVERIFIED.

Keep OCR, new parsing services and document-model downloads outside scope.
Scanned/essentially unreadable sources stop explicitly. Existing file/page
limits alone do not prove bounded decompression or parser execution; verify
the existing active-time/resource stopping behavior and malformed-file tests
before accepting arbitrary uploads. No new banking threshold follows.

## Observed compatibility result

All three current source PDFs/five pages passed complete ordered nonblank-line
comparison in plain/layout modes. Six focused checks passed: explicit year-column
alignment, whole-USD units, annual projections, cross-page continuation, full
debt-service qualification and explicit zero liens. Both DOCVERIFY modes still
withhold trusted dispatch because SOURCEFIT is unapproved. Combined69 methods
passed. [Evidence](../../execution.md#m2-parser-installation-and-pdf-verification).

The first draft failed exact punctuation comparison on two pages because the
writer omitted WinAnsi font encoding. Technical draft2 adds that encoding;
financial content/assumptions are unchanged. Original files and failed evidence
are retained. The diagnostic was also corrected to scope Revenue to its table,
excluding later explanatory prose. No relaxed content comparison was used.

## Remaining integration work

1. Retain the resolved dependency/profile and actual raw parse evidence. No gold
   enters runtime parsing and a text match never grants HUMAN_SUPPORTED.
2. Extend malformed/scanned/resource and representative unfamiliar-layout
   checks before enabling general upload intake.
3. Adapt actual parsed inventory into DOCVERIFY/faithful DIRECT preparation;
   retain full request/token preflight and source-fit checks.
4. Resolve material loss explicitly; do not silently switch parser. Review
   exact case/config/source digests before registration and synthesis authoring.

Current progression,2026-10-23: the user subsequently approved A1-A4 and the exact
[E-N01 default slice](../../../fixtures/development/e-n01/README.md) is now bound
by separate CASE-REG-1.0 registration. Actual page checks feed qualified financial,
policy and risk panels;85 combined application methods pass. Original authoring
snapshots/history remain unchanged. [Current evidence](../../execution.md#m2-registered-deterministic-panels-evidence).
This supersedes the earlier source-fit/registration prerequisite only for that
fixed slice. General uploads, faithful model-context/token preflight, synthesis
fixtures, the full graph and final PanelDecision remain integration work.
