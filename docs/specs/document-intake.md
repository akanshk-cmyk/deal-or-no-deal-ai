# Deal Creation and Document Intake

**Next implemented upload stage:** [UPLOAD-FACT-1.0](upload-fact-review.md) binds
manual annual CFADS/principal/interest proposals to original page spans, subject,
facility, period and units. RiskManager reviews semantic support. It does not certify
source origin/current authority, register a complete case or infer missing facts.

**Current upload inspection:** [UPLOAD-1.0](upload-inspection-integration.md) enables
New Deal uploads: Analyst attestation, bounded PDF validation, retained originals,
page/hash citations and workspace library. This is INSPECTED_NOT_REVIEWED, not
general financial admission/registration. Limits remain3 PDFs/10 pages/10,000,000
bytes, plus45-second parse/120,000 UTF-8 text ceiling; never truncate. Semantic
chunking/index/provider remain pending. Earlier upload-pending notes are superseded
only for inspection.

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Feature ID: SPEC-001
Version: 1.9
Status: Registered cases and bounded uploaded-PDF inspection implemented; general financial onboarding pending
PRD requirements: FR-001–003, FR-015, FR-019–020
Role instructions: [Document Intake](../agents/document-intake.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

Latest LOCAL_FILE slice: public_sources.py/config/source_ingestion.toml inspect supplied HTML/text-PDF bytes without browser/network/database work; exact content/observation identity, static text/rows, PDF page locators and unverified origin/support are recorded. The explicit CLI retains local bytes/report.95 combined methods pass; actual user upload and full semantic/layout support remain untested. This reference inspection does not broaden the core loan admission or certify generic PDF parsing. User will upload the file, so a SEC contact and remote crawl are not prerequisites now. [Evidence](../execution.md#local-reference-setup-and-inspection-evidence).

Accepted ADR-007 adds a separate explicitly invoked REFERENCE_CORPUS ingestion path using local-file intake, Nebius-hosted embeddings under ADR-008 and SQLite-vector storage; [public-source contract](public-financial-sources.md) owns its exact URL/HTML/snapshot/segmentation limits. Source and architecture approval are resolved; setup/implementation checks remain pending. The selected SEC source is a credit agreement, so use clause/definition/pricing dependencies. Existing three-PDF/ten-page/10MB loan intake and E-N01 registration are unchanged. A public-source crawl is not a complete loan package or trusted policy onboarding. No import or source view starts fetching.

A simulated Credit Analyst creates a synthetic deal, sees supported input limits, validates sources, and starts one intentional review. Include text-based English PDFs for one USD term loan. Exclude OCR, spreadsheets, password recovery, arbitrary real customer data, runtime web search, and file execution.

## Workflow and rules

Create a DRAFT workspace, then select a prepared scenario or upload a package. Enforce <=3 PDFs, <=10 combined pages and <=10,000,000 combined bytes; equality is permitted. Check actual format/readability, not extension alone. Reject encrypted, corrupt, zero-page, scanned-only, or essential unreadable pages with file/page-specific messages. Preserve page text/table layout and numeric footnotes; do not silently ignore unusable essential content.

Assign source/version/content digest, page numbers starting at one, and stable passage identifiers. Replace a source through a new analytical revision, retaining the original. A supported package too large for faithful model context still fails SPEC-006 preflight despite passing PDF limits.

Apply [SEG-1.0 document-specific segmentation](context-optimization.md#document-specific-segmentation-and-overlap--seg-10): agreement clauses, term-sheet sections and financial table/row groups retain their original source spans and parent/related-passage links. A single PDF can contain multiple content profiles. Type/profile comes from trusted scenario metadata or operator selection, not another model call. Preserve required definitions, headers, currency/scale, statement periods and footnotes; do not treat repeated headers/overlap as new data. The Banking Policies profile covers trusted reference content; arbitrary uploaded policy-to-rule conversion is outside scope and cannot modify executable sample rules.

Fixture mode requires an exact registered package digest and scenario version; formatting changes do not inherit canned results by filename. Live mode accepts only synthetic packages and requires readiness/configuration in SPEC-007. A synthetic-data declaration is an operator attestation, not an automated privacy classifier.

### Supported completion and assessment onboarding

### Approved E-N01 deterministic slice — CASE-REG-1.0

After the concrete A1-A4 approval/next-steps request, the user replied “ok move with next steps.” This resumes development and approves the presented educational E-N01 dates, loan details, fictional premises and factor ratings20/25/20/15/30. Record attribution as user-approved educational assumptions, not independent banking validation or Live HUMAN_SUPPORTED. No additional approval of these same assumptions is required.

Keep draft source/candidate files unchanged. Add a trusted config/registrations/e-n01.json approval record binding exact current manifest, source package, case metadata, extraction-candidate, policy-pack and Runtime instruction hashes. Store actual UTC observation/cutoff separately from the explicitly approved2026-10-23 business review date; never infer historical availability from authored dates. The fixed source profile approves only the registered synthetic borrower/facility and supplied periods/units, with field-specific page authority and no blanket external-source hierarchy or expiry rule. Approval of a fixture is not real-world fact verification.

Implement the small registered-case loader/adapters in services.py, and pure policy.py/risk.py handlers. The M2 loader accepts only FIXTURE/E-N01/default and requires the exact registered extraction-stage candidate; changed/unregistered sources/configuration/outputs stop before trusted calculation. Actual pypdf text/page hashes must match the approved known-corpus fidelity profile. Build real parsed-page OriginalBlocks with registered dependency closure and scoped source-fit; preserve all five pages. Full request/model-token preflight remains mandatory before later Live dispatch; the offline byte diagnostic is not token accounting. No generic upload, new model call, graph, database or automatic registration of another deal is introduced.

Before compute_financials, validate every known financial operand's exact approved basis ID, scope, USD/scale, selected source/page and current fixture permission. Reject cross-subject/facility/revision, incompatible periods/units/bases, unknown refs or missing current Live support; this slice explicitly rejects Live mode rather than faking support. Genuine prior-period revenue is allowed only through FIN-1.0's comparable prior basis. Output source-linked FinancialPanel data and limitations, then deterministic compliance/risk artifacts. Missing material input or invalid metric cannot produce a full score. This is an APPLICATION_TEST deterministic slice, not yet an EXECUTED_FIXTURE full graph, final recommendation or human disposition. The approved source/assessment registration remains separate from later synthesis and correction-stage variant registration.

Extend existing TEST-001-05/06, TEST-002-06/07, TEST-003-04 and TEST-006-03/05 with exact source/config/stage binding, scope/period/source checks, full-coverage inclusion and no gold import. Preserve earlier draft/source/parser evidence and no automatic expiry.

Current M2 progress2026-10-23: the user approved A1-A4 and source/assessment/default-stage binding through CASE-REG-1.0 above. [E-N01 pack](../../fixtures/development/e-n01/README.md) retains its three synthetic PDFs/five pages and original authoring snapshots. [ADR-006](../architecture/decisions/006-proposed-pdf-parser.md) pypdf6.21.2 is installed/tested; services.py now resolves current registered source fit and real parsed inventory separately from authoring flags/maps. Scope/period/units/authority and exact default extraction are qualified before deterministic panels. Generic uploads, Live support and full graph/correction/synthesis variants remain pending. External test_deal/Six Flags documents remain outside the registered synthetic case; original drafts/failure evidence are retained.

Authorized SME-01 fix, 2026-10-23: the five-day MVP offers complete review walkthroughs for registered, reviewed synthetic case packs only. A pack binds source/package digests, policy/applicability configuration, subject/basis registry, all five case-author factor assessments and their material-input requirements, and matching current-input fixture variants. Ratings remain explicitly authored educational assessments, not autonomous grades. Runtime assessment/configuration records are separate from evaluator-only gold results. Source registration is not semantic verification of a Live model's extraction.

Unregistered synthetic uploads are supported for extraction and safe partial analysis in explicitly available Live mode; Fixture mode still rejects an unmatched package without inference. Before Start, state Partial analysis only — reviewed case assessments/configuration unavailable. After extraction, absent assessment/material/subject prerequisites remain explicit; credit score is Insufficient Data, dependent synthesis/PanelDecision is unset, and no final decision-ready report is claimed. Do not promise that uploading more of the same financial document supplies missing case-author ratings. The next action explains instructor case preparation, not a nonexistent score-entry form or automatic completion.

Case preparation is an offline, reviewed developer/instructor task using trusted repository configuration after the implementation gate. It includes actual supporting synthetic sources, applicability/rubric, current dependency digests, and fixture authoring/evaluation. Uploaded JSON, PDF instructions, persona switching and a filename cannot register a pack or modify weights/ratings. Changed material inputs invalidate assessments; reuse requires matching reviewed dependencies, never another deal's grades. No new scoring LLM, UI editor, node or external service.

### Subject and facility coherence

Authorized SME-02 fix: trusted source/basis metadata contains subject_id, subject_label, role, facility_scope_id, applicable source/passage references, subject_match MATCH/UNKNOWN/CONFLICT, and review attribution/basis. Roles distinguish BORROWER_TERMS, BORROWER_FINANCIALS, DEBT_SCHEDULE, COLLATERAL_SUPPORT, GUARANTOR and PARENT_CONSOLIDATED. A document with several entities needs passage-specific attribution; do not default all pages to the borrower. The one-loan facility scope must match the reviewed deal.

The case-author registry explains the connection between the contractual borrower and financial subject/debt/collateral scope using actual supporting passages. A supported consolidated basis explicitly names the included entities and justified assessment scope; no universal permission to use a parent's statement is inferred. Equal display names, a selected deal ID, matched dates or an operator-selected label alone do not prove a match. Unresolved subject/facility attribution is UNKNOWN/CONFLICT and pauses affected trusted metrics and downstream conclusions through existing scoped information issues, not a credit Reject or real KYC result. Unregistered uploads cannot silently inherit a case's subject registry. No entity-resolution model or external identity service is added.

## Contracts and data changes

| Proposed service | Input | Output/validation |
|---|---|---|
| create_deal | CreateDealCommand: operation_id, workspace_id, actor, display_name, optional owner/purpose | DealRecord with generated deal_id, input_revision=1, record_version=1, lifecycle DRAFT; no findings |
| validate_package | CommandMeta; candidate PDF bytes/names; selected mode/scenario; policy version | PackageValidation with per-file outcomes, totals, issues, accepted manifest nullable |
| commit_package | CommandMeta; validated candidate identity/digest | DocumentManifest; increments revision for replacement, marks dependent artifacts stale |
| get_source_passage | scoped deal/source/version/page/passage | SourcePassage with source text, page context, original location; never arbitrary filesystem path |

DocumentManifest fields: manifest_id, deal_id, input_revision, source entries, totals, package_digest, scenario match, validation status, completion_scope REGISTERED_COMPLETE_REVIEW/UNREGISTERED_PARTIAL, assessment_config_ref nullable, subject_registry_ref/version. Source entry: source_id/version, display_filename, byte_count/page_count, content_digest, media_type, page block references, parsing outcome, subject/facility/passage-scope references with attribution status. Internal storage locations are generated locally, never derived from uploaded path components. Policy pack is configuration, outside uploaded-PDF totals. Missing trusted configuration is a visible analysis prerequisite, not a fabricated source fact.

## Source authority and business-date applicability

SPEC-006 [SOURCEFIT-1.0](context-optimization.md#source-relevance-authority-and-temporal-fit--sourcefit-10) adds reviewed ReviewSourceBasis/profile and per-candidate date/qualifier/authority/supersession metadata to the existing manifest/case configuration. Local ingestion time, evidenced historical observation time, publication/effective dates and financial periods are distinct; never infer an old capture from filename. Registered packs need authored review date, evidence cutoff and supported field-level authority/applicability, including the selected policy version. A newly uploaded document is not automatically the governing source. Missing metadata leaves affected use unresolved/partial; uploaded instructions cannot register a profile. Frozen historical demonstration uses retained registered versions only. SOURCEFIT-1.0 itself adds no crawling; the separately accepted ADR-007 extension permits only its exact public-reference URL scope. No additional loan PDFs, automatic expiry or new authority hierarchy is added. Changed source/basis/profile follows revision and dependent-artifact invalidation; source reads remain zero inference.

## Parsed inventory and citation locations

### Approved known-corpus parser verification slice

User instruction2026-10-23: install the proposed parser and verify these PDFs. This approves installing/testing pypdf for the three E-N01 draft source PDFs, not A1-A4, case registration, general upload intake or paid inference. Preserve the authored files/manifest as a historical draft; write measured parser artifacts separately under ignored var/evaluations. Record the resolved package/license/API profile and actual source digests. No adopted PyMuPDF dependency or project license is implied.

The explicit offline utility tools/verify_e_n01_pdfs.py must check all expected generated bytes/manuscript hashes before parsing. Limit this entry point to the known deterministic E-N01 writer output; it is not a generic untrusted-PDF parser. For each actual page, save plain and layout extraction separately and compare the complete ordered nonblank lines against its authoring manuscript. Ignore blank-line/trailing-space differences only; preserve inner spacing, characters, order, table values and qualifications. Record mismatches as failures, with no silent truncation or repair. Verify actual page count/encryption/readability plus the existing package limits.

Focused diagnostics verify both explicit year columns, revenue-to-year alignment using layout character positions, whole-USD units, annual projection context, cross-page debt-service qualification and documented zero liens. These are PDF extraction/layout checks, not automatic general-purpose financial extraction, actual glyph-box measurements or approval of source assertions. Never derive an accounting/risk conclusion from this verification. Ambiguous/missing headers or straddling values fail the diagnostic instead of guessing a year. Save exact source/version/page and character offsets, with a clear layout-character coordinate label.

Construct actual parsed page blocks for DOCVERIFY from parser output, never reuse manuscript offsets as parsed offsets. Successful full-page comparison can establish measured parser fidelity for these five simple authored pages only. Source-fit flags remain false: both baseline/adaptive must still withhold trusted dispatch while the case/source profile is unapproved. Report parser fidelity separately from SOURCEFIT, semantic HUMAN_SUPPORTED, review readiness and fixture registration. Additional malformed/scanned/resource tests remain prerequisites for later generic upload support. Extend existing TEST-001-02/03/04 and TEST-006-02/03 integrity families with known-source mismatch and absent/ambiguous-column cases; do not add a new TEST/MET ID or broaden application scope.

Apply SPEC-006's COVERAGE-1.0: preserve the original per-source/version/page block/row/span inventory and parser fidelity/warnings separately from segmented passages. Each passage maps to an ordered list of original page locations, including required headers, units, periods, qualifiers and notes. FULL_EXTRACTION coverage must account for the whole accepted parsed package, not just discovered field hits. A single source reference represents one location; cross-page evidence expands to every location, with truthful text fallback where bounding boxes/preview are unavailable. Extend TEST-001-04 with the two-page table and qualified clause examples; missing material parse context cannot become COMPLETE. No parser or chunk-target change is authorized.

## AI and evidence behavior

The user-authorized [DOCVERIFY-1.0](context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10) adds offline checks over supplied original blocks and table geometry/period metadata. Preserve named layout fragments so a shifted or reversed year column cannot inherit a different fragment's coordinates. Missing headers/units/periods and unavailable qualifications withhold affected values. Parser selection/licensing and actual PDF-to-block fidelity remain separate unresolved prerequisites; synthetic parsed-block tests cannot establish them.

No model call in creation, parsing, validation, or navigation. Preserve original bytes and extracted page blocks as separate artifacts. Header/footer deduplication follows SPEC-006 and never rewrites originals. Terms are not inferred by the parser; typed extraction belongs to SPEC-002.

## Authorization

Credit Analyst creates/commits packages under P3-02; all permitted personas can inspect their local workspace sources. Wrong workspace/deal/reference requests are denied. Do not claim authenticated isolation: the operator can switch personas.

## UI states

Empty: synthetic boundary, supported limits, scenario/upload choice. Loading: per-file validation progress. Success: source IDs, pages/bytes, policy/mode readiness and Run availability. Failure: actionable per-file error, preserved safe draft, no dispatched run. Stale: replaced manifest clearly supersedes previous sources.

## Reliability and stopping

Read source bytes once per digest. No model repair/OCR fallback. Parsing failure is explicit and ends intake; a recoverable local read may be retried intentionally within run limits if part of a running graph. Duplicate commands use receipts. Run remains disabled until all required intake checks pass.

## Analytics

deal_created; package_validation_completed with file/page/byte counts, outcome/reason; source_committed with revision/digest reference. Exclude filenames, raw source text, borrower names, credentials, and raw bytes from ordinary analytics.

## Tests and acceptance

- TEST-001-01: Create empty workspace; duplicate operation returns one deal; altered duplicate payload rejected.
- TEST-001-02: File/page/byte equality accepted and each over-limit rejected before inference.
- TEST-001-03: Corrupt, encrypted, scanned, empty and spoofed formats produce explicit safe errors.
- TEST-001-04: Exact source locators, contributing pages and parent/related references survive SEG-1.0 segmentation/extraction; mixed-content PDFs retain correct profiles; repeated table context creates no duplicate financial observation; path-like filenames cannot escape storage boundary. COVERAGE-1.0 verifies the original-span inventory and two-page table/qualified-clause locations, including missing material parse context.
- TEST-001-05: Unmatched fixture and unavailable Live cannot dispatch; matched fixtures remain usable without credentials. Complete reviews require registered reviewed assessment/config packs. Unregistered Live upload clearly starts partial analysis only, with no borrowed ratings/subject metadata, accepted PanelDecision or final-ready report; uploaded instructions cannot register a case.
- TEST-001-06: Source replacement increments revision and invalidates dependent results; reads/refresh add zero calls. SOURCEFIT-1.0 also invalidates affected source selection after review-date/cutoff/profile changes; evidenced historical observation stays distinct from local ingestion.

All agreed intake cases must pass. Related scenarios: E-T01/T02 and E-M04; quality denominators are in the evaluation plan.

## Dependencies and implementation boundary

Requires SPEC-011 repository interface and parser compatibility/licensing review. Provides manifest/passages to SPEC-002/006. No source files, parser, uploads directory, or database are created by this specification.
