# Document Intake Instructions

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Instruction ID: INTAKE-001  
Version: 1.7
Execution: Pure Python control service; zero LLM calls  
Requirements: FR-001–003, FR-015, FR-019–020  
Read with: [Shared contract](shared-contract.md), [Evaluation](evaluation.md)

## Engineering coverage contract

Current LOCAL_FILE implementation is public_sources.py plus trusted config/source_ingestion.toml and explicit inspection/setup tools. User chose to download/upload the document; do not request SEC contact or start a crawler. Read bytes only after explicit input, enforce type/size/reference-page/encoding stops, preserve original bytes/observation identity and keep inspection origin/support UNVERIFIED.95 combined methods pass. No unseen user upload, model artifact, index, reviewed factual support or full loan admission is established. Use current execution evidence; prior setup-only notes below describe their original slices.

Accepted public-reference direction: [ADR-007](../architecture/decisions/007-proposed-public-financial-rag.md) and [source contract](../specs/public-financial-sources.md) select local-file intake, Nebius-hosted embeddings under ADR-008 and SQLite-vector search. Architecture and the SEC agreement URL are approved; actual setup/adapters remain pending. Apply the separate corpus scope and retained snapshot/section locators; never register public text as E-N01, borrower support, executable policy or an authored factor assessment. Keep the existing PDF/deal limits separate. Model-visible extraction/synthesis prompts are unchanged; do not append this engineering prose to their context.

Current E-N01 admission: the user approved A1-A4; services.py resolves the separate trusted config/registrations/e-n01.json under CASE-REG-1.0. It rechecks exact source bytes, real parsed page hashes, case/extraction/policy/instruction versions and approved subject/period/units/authority. Authoring snapshots keep their original draft flags; the parse-only utility reports registration unknown rather than granting it. This exact FIXTURE/default admission is tested, not generic upload or Live HUMAN_SUPPORTED. See [current evidence](../execution.md#m2-registered-deterministic-panels-evidence).

Current parser profile: user-approved pypdf6.21.2 (ADR-006), installed/locked. The E-N01 known-corpus utility actually verifies five parsed pages against manuscripts, separately from authoring maps. Technical draft2 fixes font encoding; original draft and failure evidence remain. Parser text fidelity does not approve A1-A4 or source applicability. This fixed utility rejects changed bytes before parsing; general upload/resource/scanned/layout checks remain future intake work. Preserve truthful page/text fallback; no glyph-box or general table-extraction guarantee.

Apply [DOCVERIFY-1.0](../specs/context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10): bind cells to explicit period headers within the same layout fragment, preserve source units/basis, and retain original blocks for all qualifications. Missing/ambiguous metadata withholds affected use. The parser-independent helper is not an adopted PDF parser or evidence of parsing accuracy. Neither baseline nor optional adaptive restoration may dispatch incomplete/unverified evidence.

Follow SPEC-001/006 COVERAGE-1.0: inventory original parsed blocks/spans, preserve parser warnings/fidelity separately from context coverage, and map each segmented passage to every contributing original page location. Retain cross-page headers, units, periods, footnotes and clause qualifications. COMPLETE packed coverage is not proof of parser or model correctness. Missing material context stops complete dispatch; use the existing citation pane/text fallback without invented highlights or a new dependency.

## Purpose and rationale

Prepare a small, traceable synthetic package before spending model tokens. Parsing, file validation, and source-version assignment do not need model interpretation.

## Inputs and limits

- Synthetic English text-based PDFs for one USD business term-loan case.
- At most three PDFs, ten pages combined, and 10 MB combined. MB means 1,000,000 bytes for this prototype limit.
- The selected sample-policy version and Fixture/Live mode.
- Optional human-entered deal metadata, labeled reviewer-provided rather than documentary.
- Financial statements/debt-service schedules may share a PDF. Equipment valuation is required only for the configured secured case.

Policy configuration is not counted as an uploaded PDF. No arbitrary public/real customer data is authorized.

SME fixes in SPEC-001: complete review requires a registered reviewed synthetic source/assessment/subject pack. Unregistered Fixture is unavailable without inference; unregistered Live explicitly offers extraction/safe partial analysis only, with no borrowed factors or PanelDecision. Explain instructor preparation as the missing prerequisite rather than promising a score-input screen. Only trusted reviewed configuration registers a case; uploaded text/JSON and matching filenames cannot do so.

Source/basis metadata binds the actual entity/financial subject, source role and facility to the reviewed borrower, with passage-level attribution for mixed-entity documents. Parent/consolidated or guarantor data needs explicit supported scope, not a name heuristic. Unknown/conflicting scope pauses affected trusted calculations. Parsing/registration never confers HUMAN_SUPPORTED on Live critical extracted facts; use FACT-SUPPORT-1.0. No extra model, external identity service or node.

## Workflow

1. Assign/resolve deal and operation identity without starting inference.
2. Check supported PDF format, readability, encryption, cumulative byte/page limits, and available text.
3. Produce versioned source IDs, page-aware text blocks, and immutable source references; flag unreadable content.
4. Retain validation results per file. Do not claim scans were extracted; no OCR is included.
5. Verify a fixture package matches its scenario/source versions before providing fixture-stage outputs.
6. Live mode must remain unavailable until provider/model/rates/allowance are configured.
7. Dispatch an intentional single review only after required validation/policy/mode checks pass.

Do not silently truncate material pages to fit the context budget. If the package cannot fit a faithful bounded extraction task, stop with a specific input/context message.

Follow [SEG-1.0 in SPEC-006](../specs/context-optimization.md#document-specific-segmentation-and-overlap--seg-10): agreement prose 350–450 tokens/40–60 within-section overlap; term-sheet sections intact or 200–350/up to 30 within-section overlap; financial table groups approximately 200–400 with repeated necessary headers/notes but no duplicate rows; complete policy rules approximately 150–400 with no overlap between independent rules. These are proposed starting targets, not measured optima or active configuration. Preserve complete parents, definitions, source/page spans and period/currency/scale. A mixed-content PDF uses the appropriate profile per block. Classification/segmentation add no model call. Keep direct grounding, deterministic approved-policy lookup and the three-PDF limit; reference policies do not become user-editable executable rules.

## Output

DocumentManifest with source ID/version/content identity, filename, bytes/pages, format/readability result, page-block references, validation errors, fixture-match status, and current deal/revision. The parser does not assign creditworthiness or an approval result.

## Failure/UI behavior

Unsupported, empty, corrupt, scanned-only, encrypted, or oversize packages show actionable errors and no inference. Preserve useful safe draft inputs after recoverable failures. Existing documents replaced later require a new input revision and dependency invalidation. Duplicate Run actions reuse the operation identity.

## Required checks

Three-file/ten-page/10-MB equality and over-limit cases; corrupt/encrypted/scanned/empty text; per-file source/version assignment; recognized versus unmatched fixtures; missing Live configuration; validation/refresh zero provider calls; duplicate dispatch; no secrets in manifest/events.
