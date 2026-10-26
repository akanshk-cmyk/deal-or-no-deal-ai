# Deal or No Deal AI — Phase 3 Specification Overview

## Current upload acceptance update - 2026-10-25

The user authorized fixing the upload acceptance gaps. This update supersedes
older exact-Standard-only, inspection-only and sequential-only statements for
**new uploaded synthetic text-PDF reviews**. Historical records are unchanged.
See `docs/specs/general-upload-acceptance.md` for the implementation contract.

New uploads can declare their own borrower, reporting periods, transaction date,
USD whole-unit basis and sample-policy applicability. Declarations are unverified
and must be checked against the retained documents. Unknown inputs/applicability
stay unknown. No sample borrower facts or factor ratings are copied. Existing
parser, token, permission and shared spending limits remain in force.

New uploaded reviews use live extraction -> mandatory fact/profile verification
-> parallel Financial / Compliance / Risk subgraph -> joined synthesis ->
mandatory narrative verification -> readiness routing -> partial or complete memo.
Only the parent persists branch outputs; calculations and policy rules are
unchanged. Missing borrower factor assessments produce Insufficient Data, never
a default Low score. Partial reports do not waive approval blockers. The same
Deal ID and uploaded page map feed Workspace, Agent Activity, Memo and History.
Sample Deal and historical contexts keep their existing execution policies.
No new dependencies, migrations, inference model settings or budget were added.
Phase 2 evaluation remains deferred. Offline provider mocks establish functional
behavior, not fresh Nebius answer quality or genuine human verification.

## Single uploaded-deal live demo — 2026-10-25

Current human-action contract: [uploaded-human-decisions.md](uploaded-human-decisions.md).
Completed uploaded drafts support separately authorized comments, Pending,
response review, Reject and readiness-gated Approve without rerunning AI.

New Deal → Upload New Deal now supports the complete unchanged three-PDF Standard Deal package. Explicit Run performs fresh Nebius extraction and synthesis on retained uploaded content, with a distinct upload-derived Deal ID, source map, shared workspace/activity/history and draft memo. It does not use saved answers as live results. Other, partial or changed packages remain inspection-only. Approval readiness and unverified-draft safeguards remain; historical human-checkpoint reviews are unchanged. See [scope, steps and evidence](upload-live-demo.md). This supersedes older blanket inspection-only statements only for that exact supported profile.


## Approved Phase 1 demo update — 2026-10-25

The user approved the [live demo-draft contract](phase1-live-demo.md). New explicit Run actions use LIVE / DEMO_DRAFT. Extraction and synthesis call Nebius; Python performs calculations, sample policy checks, illustrative scoring, readiness and draft assembly. Technical integrity checks do not record human verification. Drafts cannot authorize credit approval. Existing HUMAN_REQUIRED reviews retain their checkpoints and original records. Saved examples remain available internally. No model calls on screen viewing and no fallback on failure. Phase 2 RAGAS/judge evaluation and optimization are deferred. This update supersedes older default-FIXTURE and pre-draft human-checkpoint statements only for new demo drafts. Functional evidence is recorded in docs/evaluation/phase1-demo-results.md (relative to repository root).


Current specialist presentation: [specialist-handoffs.md](specialist-handoffs.md)
implements the existing FR-008/011/019 orchestration and transparency requirements
within SPEC-007/010/011. Three role groups project scoped artifacts and recorded
events without extra calls, altered prompts, message backfills or graph changes.
See [implementation status](../implementation-status.md) for current execution;
dated milestone paragraphs below describe their own historical scope.

Current unified experience (2026-10-25): [approved contract](unified-review-experience.md).
One Run AI Deal Review action uses config/app.toml mode; saved and live records
share the existing saved UI. Earlier sidebar mode and separate layout descriptions
are historical. Live interrupts, source labels and backend authority remain intact.

Approved interrupted-attempt exception:
[administrative quarantine](../architecture/decisions/proposed-unknown-request-quarantine.md)
adds scoped audit/fencing to existing SPEC-007/011 admission and persistence.
The original review and unknown reservation stay intact; only its exclusive local
claim is released. No other review's verification or approval requirements change.
Execution evidence: [quarantine results](../evaluation/quarantine-results.md).

User-requested [live fact-judge diagnostic](live-fact-judge.md) evaluates the
existing source-bound targets offline; it does not add a graph agent, clear an
interrupt or modify human-support permissions. See
[actual results](../evaluation/live-fact-judge-results.md).

## Recommendation presentation update - 2026-10-24

Recommendation presentation: recommendation-presentation.md defines the shared pure formatter for Dashboard, Workspace and new Credit Memos. It reuses READINESS-1.0 without additional statuses or decision rules. Original proposals remain traceable; historical memos are not rewritten. Tests: tests/unit/test_recommendation.py and tests/integration/test_recommendation_presentation.py.


## READINESS-1.0 current update - 2026-10-24

READINESS-1.0 / FR-READY-001 through FR-READY-005: approval-readiness.md governs the original AI proposal, deterministic current eligibility, and human decision as separate records. An existing normal or conditional approval path remains blocked until all mandatory readiness checks are resolved; condition preparation and supported rejection paths remain available. Earlier successful approval examples do not waive this gate.


## LIVE-GRAPH-1.0 implementation update - 2026-10-24

User authorized completing the live graph and evidence checkpoints. Follow
[the live graph contract](live-graph-integration.md). The shared build_graph now has an explicit
live branch with a pre-calculation fact_review interrupt and a post-synthesis
evidence_review interrupt. live_worker uses the existing SQLite admission/ledger,
checkpointer, strict wire parsers and deterministic finance/policy/risk services.
Actual response text is retained; registered sample answers are never a fallback.
ReviewedLiveCase binds the actual extraction to source/profile validation and
immutable human-support receipts without changing the original registration.

Every present term/financial fact and authored scoring premise needs RiskManager
support. Every observation, rationale, condition and next-action reason has an
exact target; policy/control meaning requires ComplianceOfficer support and mixed
content needs both domains. Source quotations, seven explicit checks, comments,
role, target/source digests and UTC timestamps are recorded. Support is metadata
only. Analyst continuation resumes the same checkpoint and cumulative ledger.
Confidence-only normal credit review has a separate AuthorizedApprover checkpoint.
Missing information stops before dependent work; live exceptions/conditions beyond
this bounded E-N01 example stay blocked, never generically waived.

UI update 2026-10-25: one Run AI Deal Review action follows config/app.toml; there is no sidebar mode selector. Live review start,
evidence forms, recorded activity, source-linked pure-Python memo and scoped local
history are connected. Live setup/readiness remains in the sidebar only.
Provider calls use the worker's existing admission claim, reserve the shared
USD0.10 allowance and record actual reported usage; uncertain usage retains its
reservation and blocks replay. No global enable-flag flip or new database.

This is implemented integration, not evidence of paid model quality. Provider
access, hosted model/schema/current rates and exact whole-request counts still
require verification; each changed synthesis packet needs its own count evidence.
Historical boundary: the 2026-10-24 integration implementation itself made no paid calls. Subsequent actual extraction, fixed embedding probes and saved-answer native/custom RAGAS are recorded in the current implementation status. Full live synthesis/report completion and hosted semantic benchmarking remain pending.


## Live foundation update ? 2026-10-24

User approved LIVE-COMPACT-1.0: extraction 4,000 input/1,000 output;
synthesis 2,500/650. Aggregate 8,000/2,000 and protected correction
1,500/350 remain unchanged; Fixture prompts and stage limits are unchanged.
The shared authorized spending allowance is USD0.10 across generation, embeddings
and evaluation. See [live integration specification](live-synthetic-integration.md)
and [approved fit profile](../evaluation/live-fit-proposal.md).

Implemented: separate live specialist prompts, compact full-source E-N01 offline
packets, explicit credential/readiness checks, guarded transport foundation with
persistent allowance reservation, four-arm retrieval mechanics, and optional
RAGAS 0.4.3/tokenizer dependencies. RAGAS requires the tested
langchain-community 0.3.31 compatibility pin; ID metrics currently use its
available public API with deprecation warnings.

Measured: local packet components 3,699 extraction and 2,282 synthesis tokens;
provider rendering overhead remains unverified. Six actual native RAGAS ID
measurements over three synthetic questions: DIRECT recall 1.0 (precision not
applicable); KEYWORD recall 1.0, precision 0.5. These tiny author-authored cases
are diagnostic, not proof of semantic quality. VECTOR/HYBRID mechanics tests use
synthetic vectors, not hosted embeddings. At that historical milestone no real generation, embedding or judge calls had run; spend was then zero. Subsequent provider execution is recorded in current implementation status, not this earlier measurement. Complete live graph integration, source-backed
critical-fact/narrative review, hosted embeddings/indexing, semantic benchmarks and
LLM-based RAGAS/custom quality scores remain pending. The key was absent at that milestone; subsequent provider access and bounded contracts are verified. Actual changed synthesis packets still need whole-request fit evidence.
An API key alone does not activate Live mode.


**Uploaded facts:** [UPLOAD-FACT-1.0](upload-fact-review.md) adds manual cited DSCR
input proposals, exact-target RiskManager support, replacement invalidation, history
and guarded annual preview. Full critical-fact/subject registry, financial case
onboarding and model integration remain pending.

**Current upload stage:** [UPLOAD-1.0](upload-inspection-integration.md) implements
synthetic PDF validation, retention, workspace library and page citation/download.
No financial onboarding, fixture fallback, model or semantic chunking/index implied.
This replaces disabled-upload notes for inspection only.

**Current extraction correction:** [CORRECTION-1.0](source-correction-integration.md)
implements the existing E-N01 deliberate extraction-miss example: source-backed
Analyst Save→READY then explicit Update, new revision/thread/shared ledger, changed
extraction provenance and dependent memo/history. General edits/new documents and
completed/interrupted-review correction remain unsupported. Earlier extraction-miss
pending observations are superseded only for this bounded path.

**Current E-P01:** [CONDITIONAL-1.0](conditional-integration.md) implements one
registered condition, distinct specialist supports, final Conditional Approve/Reject,
source-linked memo and history. Original Exception remains; condition OUTSTANDING.
Arbitrary edits, fulfilment and new documents remain unavailable. This supersedes
E-P01-pending observations in historical milestones below.

**E-F03 current integration:** [EXCEPTION-REJECT-1.0](exception-reject-integration.md)
implements source-backed Reject, separate numerical-exception handling, actual
reviewed graph, final-role decision and memo/history/export. Review handling changes
gate version, never original policy results or analytical basis. E-P01 Conditional
and new-document continuation remain pending.

**E-M01 current integration:** [MISSING-DATA-1.0](missing-data-integration.md)
implements exact-source registration, five-stage partial execution, confirmed
WAITING_INFORMATION and partial source inspection with blocked final actions.
E-N01 normal/review/reassessment remain supported. E-P01/F03 runtime, Conditional
and missing-document replacement/continuation remain pending.

**Current implementation status:** See [../implementation-status.md](../implementation-status.md). Earlier milestone progress paragraphs below are historical and superseded for implemented capabilities; requirements and safety boundaries remain active.


**Current implemented milestone:**
[FIN-REVIEW-1.0 / FIN-REASSESS-1.0](financial-review-integration.md) adds a separately
registered review-required E-N01 response, actual financial interrupt/resume,
role-aware decisions/comments, frozen history/CSV and exact registered-evidence
reassessment. Revision2 uses a new run/thread and original ledger; old review is
stale. Notebook and offline clickable HTML now exist. These bounded paths supersede
older financial-HITL/teaching-artifact pending notes; other source cases, Conditional,
general uploads, optional notebook kernel, Live and retrieval/evaluator runs remain
pending. Normal fixture and original source/prompt registrations are preserved.

**Current normal-path integration (2026-10-24): [APP-READ-1.0](financial-command-center-integration.md) implements the root six-destination fixture shell and source-bound financial read model. Earlier full-shell-pending statements describe prior slices. SPEC-010/013 remain partial: actual financial review actions/resume and human credit-decision history are pending; execution history is labeled separately. Live, additional cases and notebook/HTML remain pending.**

**Decision History scope addition — 2026-10-24:** User-authorized FR-021 / [SPEC-013](decision-history.md) adds a sixth page, read-only scope-filtered timelines and all-filtered CSV export. Existing event-time versus current status/context is preserved; legacy gaps remain explicit. The current illustrative preview now exposes two pages; the full six-screen shell and financial lifecycle integration remain pending. This explicitly supersedes older five-screen and decision-history export deferrals without changing other feature/financial boundaries.

**Human-review UI implementation — 2026-10-24:** [REVIEW-UI-1.0](human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10) extends SPEC-008/010/011 with comments, simulated role-aware Approve/Reject/information requests, actual UTC timestamps, atomic local history and duplicate/stale guards. The implemented preview is illustrative and isolated from normal source/loan records; the complete five-screen/financial interrupt adapter is still pending. No source support, additional inference, new database or financial clearance follows.

**Quality prerequisites implemented — 2026-10-24:** [QUALITY-REVIEW-1.0](../evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) adds complete registered extraction context, field-level diagnostics, original-response retention and source-review packets for arbitrary supplied synthesis text. This extends existing SPEC-002/005/006/007 without activating Live, changing the graph or granting semantic support. The current execution record distinguishes actual offline tests from pending model/schema/tokenizer, manual-review and funded evaluation work.

**Authorized normal Fixture slice — 2026-10-23:** [E-N01-SYNTHESIS-1.0](synthesis-evidence.md#authorized-e-n01-normal-slice--e-n01-synthesis-10) binds the current synthesis request, exact educational stage response and four narrative evidence targets. The normal nine-stage LangGraph/SQLite path, primitive panel handoffs and pure seven-section memo are now implemented; scoped executed checks are recorded in execution.md after verification. Only E-N01/default is supported. Other cases, actual human-review interrupts/corrections, full UI/notebook/HTML and Live remain pending. Fixture expectation checking is not HUMAN_SUPPORTED or a real model-quality result; provider calls remain disabled. Earlier partial/no-graph status notes describe their historical slices.

**Generation comparison preparation — 2026-10-23:** [GEN-COMPARE-1.0](../evaluation/generation-model-comparison.md) is the authorized narrow implementation contract for paired Qwen/Nano inputs, strict disabled configuration, exact reference-field checks, dated cost estimates and explicit unready/null report states. It extends SPEC-002/005/007 evaluation without changing Runtime prompts, wire contracts, case registration or budgets. No real comparison result or paid activation is inferred.

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

**Current implementation status, 2026-10-23:** M1 dependency installation,43 scoped tests and local build succeeded; [M1 evidence](../execution.md#m1-implementation-evidence) is current. PREREQ-02 is verified for the M1 foundation; PREREQ-03 remains IN_PROGRESS because complete case/source and provider-tokenizer fit belong to later milestones. Do not promote these checks to completed deal/Live/UI evaluations. Prior pending-approval/setup-blocked notes are historical.

Version: 1.28
Date: 2026-10-23
Status: Approved baseline with tested normal/reviewed E-N01, bounded registered-source reassessment and teaching artifacts; remaining broader prerequisites below
Approval record: The user accepted the specifications/evaluation plan and P3-01–09 by requesting the next phase. Repository design and implementation remain separate gates.
Sources: [PRD](../product/prd.md), [HLD](../architecture/hld.md), [specialist instructions](../agents/README.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)
Coverage: [Traceability](../traceability.md)

## Scope and authority

Latest source check: actual inspection of the newly supplied47-page PDF succeeded, with96 combined tests after the LOCAL-REFERENCE-1.1 binding fix. The configured target source stays separate from observed file identity: no admitted corpus/declared source, support UNVERIFIED, no score/index. [Evidence](../execution.md#uploaded-reference-inspection-and-source-binding-correction). Earlier no-user-file/setup notes remain historical; model/vector/graph work is still pending.

Historical local-reference setup progression (superseded by uploaded-source evidence and ADR-008): user authorized next implementation, then selected download/upload instead of SEC crawling. Optional packages/CPU import and LOCAL-REFERENCE-1.0 supplied-byte HTML/PDF inspection are implemented;95 combined methods pass. [Actual evidence](../execution.md#local-reference-setup-and-inspection-evidence). No actual user file has arrived; crawling/browser setup is inactive, BGE weights/revision unconfigured, and embedding/index/retrieval components remain unimplemented. Prior architecture-only/no-install notes describe earlier records. No repeated architecture/source/contact approval is needed for LOCAL_FILE.

Accepted public-source extension2026-10-23: [source contract](public-financial-sources.md) refines SPEC-001/006/011 for the selected SEC credit-agreement reference corpus; [accepted ADR-007](../architecture/decisions/007-proposed-public-financial-rag.md) records local Crawl4AI, Nebius-hosted embeddings under ADR-008 (model contract pending) and SQLite-backed exact vector search. Source and architecture approval are resolved; versions/licenses/setup, schema implementation and runtime tests remain pending. REFERENCE_CORPUS cannot inherit E-N01 registration, policy authority or Live support. Preserve the core loan DIRECT default and scope outside this bounded extension; do not request the same architecture/source approval again.

Latest approved progression2026-10-23: “ok move with next steps” followed the explicit A1-A4 checkpoint and resumes development. [CASE-REG-1.0](document-intake.md#approved-e-n01-deterministic-slice--case-reg-10) now binds the exact E-N01 source/assessment/default extraction profile. services.py qualifies current scope/period/units/source authority, then executes financial/policy/risk handlers. [Actual evidence](../execution.md#m2-registered-deterministic-panels-evidence):85 combined methods pass; score21 Low,0 policy exceptions/0 missing material inputs, confidence not evaluated and no final decision/readiness. These are APPLICATION_TEST results; full graph, correction/synthesis variants, UI, Live support and model-token fit remain pending. Earlier pending A1-A4/source-registration notes below describe prior slices and are superseded for E-N01/default only.

Current parser progress2026-10-23 supersedes earlier parser-pending notes: user approved installation and PDF verification; pypdf6.21.2 is installed/locked and all five E-N01 technical-draft2 pages passed actual plain/layout extraction comparisons. [Evidence](../execution.md#m2-parser-installation-and-pdf-verification):69 combined methods passed, original font-encoding failure/source draft retained. Case A1-A4, source authority/support, full stage integration and registration remain pending. No general upload or financial approval is inferred.

M2 partial implementation2026-10-23: [source candidate and arithmetic evidence](../execution.md#m2-source-candidate-and-arithmetic-evidence) records three synthetic PDFs/five authored pages, draft configuration and nine calculation helpers, with66 combined passing methods. [E-N01 A1-A4](../../fixtures/development/e-n01/README.md) and [parser ADR-006](../architecture/decisions/006-proposed-pdf-parser.md) await approval. No actual PDF parse, registered fixture or trusted complete FinancialPanel is claimed; existing55-method extension evidence is retained.

Subsequent user authorization,2026-10-23: [DOCVERIFY-1.0](context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10) adds parser-independent table/context helpers and paired offline checks. [Observed extension evidence](../execution.md#document-verification-extension-evidence):55 combined methods passed;14 parsed synthetic cases/28 executions with no check failures. This is partial SPEC-001/006 control implementation, not completed M2 intake/retrieval/financial graph or a passed parser/Live prerequisite. Baseline keeps all safeguards; adaptive is opt-in. Existing43-method M1 evidence remains historical and retained.

This phase converts the established educational scope into implementation contracts. It does not authorize code, repository scaffolding, dependency installation, paid inference, publishing, or deployment. The five-day implementation target starts after prerequisite approvals. Existing formulas and thresholds remain fictional demo policy, not regulatory requirements. No real borrower data is permitted.

Confirmed direction: one local Python/Streamlit app; LangGraph plus selected LangChain primitives; Pydantic; Decimal; one SQLite boundary; Jupyter; fixture-first development; later Nebius integration. Two normal live calls are Extraction and Synthesizer. Other responsibilities execute in Python. No REST server, broker, vector database, autonomous planner, voice integration, or cross-deal personal memory is required.

The PRD defines outcomes, HLD defines structure, agent files define role boundaries, and these approved specs define implementation contracts. A mismatch must be resolved in documentation rather than silently interpreted in code. P3-01–09 below were accepted with Phase 3 approval on 2026-10-22; provider spending, dependency compatibility/licensing and later gates remain separate.

## Feature index and dependencies

| Feature | Specification | Dependencies | Primary responsibility |
|---|---|---|---|
| SPEC-001 | [Deal and document intake](document-intake.md) | Shared contracts; SPEC-011 storage | Create/validate/version synthetic packages |
| SPEC-002 | [Structured extraction](extraction.md) | SPEC-001, 006, 007 | Agent 1 |
| SPEC-003 | [Financial analysis](financial-analysis.md) | SPEC-002 | FIN-1.0 arithmetic |
| SPEC-004 | [Policy and risk panels](policy-risk.md) | SPEC-003 | Agent 2; Agent 3 quantifier |
| SPEC-005 | [Synthesis and evidence](synthesis-evidence.md) | SPEC-002–004, 006 | Agent 3 synthesis; Evidence |
| SPEC-006 | [Context optimization](context-optimization.md) | Source/artifact contracts; SPEC-011 | Context selection, exact reuse, token preflight |
| SPEC-007 | [Orchestration and budgets](orchestration-budgets.md) | Shared contracts; SPEC-011 | Graph, modes, guards, scheduling |
| SPEC-008 | [Human review and corrections](human-review-corrections.md) | SPEC-004, 005, 007, 011 | Gates, simulated capabilities, revisions |
| SPEC-009 | [Credit memo](credit-memo.md) | SPEC-003–005, 008 | Pure renderer/report node |
| SPEC-010 | [Command-center UI](command-center-ui.md) | Services SPEC-001–009, 011, 013 | Six-screen target; Human review/History preview implemented |
| SPEC-011 | [Persistence and observability](persistence-observability.md) | Shared contracts | State, idempotency, diagnostics/evaluation viewer; explicit offline RAGAS boundary |
| SPEC-012 | [Jupyter and HTML presentation](jupyter-html.md) | Shared graph metadata; SPEC-007, 009 | Offline diagram and visual walkthrough |
| SPEC-013 | [Decision History](decision-history.md) | SPEC-008, 010, 011 | Scoped event-time snapshots, filters, timelines and CSV export |

Dependency cycles in this table are contract dependencies, not an instruction to implement all services simultaneously. Establish shared types/storage interfaces first; use injected fake adapters and repositories for independent tests. Module paths and commands are proposed only during Phase 4/5.

## Accepted decisions — Phase 3 approval and authorized review fixes on 2026-10-22

| ID | Accepted decision | Reason and boundary |
|---|---|---|
| P3-01 | Summary workflow precedence: BLOCKED > NEEDS_INFORMATION > ESCALATE > REVIEW_REQUIRED > CONTINUE; actual dispatch uses explicit per-issue scope/gates | Gives one dashboard status without erasing underlying issues |
| P3-02 | Capability/exception matrix in SPEC-008; Risk Manager handles four sample numerical policy exceptions and, separately, SCORE-REVIEW-HIGH credit-risk handling; Compliance handles only allowlisted synthetic control fixtures; package Approver must meet required NORMAL/SENIOR tier | Enables a meaningful demo without blanket approval authority |
| P3-03 | One local process, one user-started standard-library execution worker, serialized storage mutations and durable operation/budget reservations; uncertain paid operations require reconciliation, never automatic replay | Keeps Streamlit responsive without a broker or duplicate requests across refresh/restart |
| P3-04 | Confirmed: no automatic expiry in the MVP prototype; no age-based deletion/pruning of persisted synthetic documents, records, reports, review history or SQLite checkpoints | Explicitly reaffirmed by the user on 2026-10-22; manual reset/deletion requires an explicit request and reviewed targets; RAM lifetime/provider caches are separate |
| P3-05 | Starting targets: Extraction 3,000 input/1,000 output; Synthesis 1,500 input/350 output; reserve 3,500 input/650 output within unchanged 8,000/2,000 hard limits | Reserve an additional 1,500 input/350 output for one synthesis rerun before spending optional repair allowance; actual feasibility must pass the early size/model checks, not assumed |
| P3-06 | Five-day core: E-N01 normal and source-backed correction variant, E-P01 Conditional Approve, E-M01 genuine missing-data pause, and E-F03 supported Reject QA path; retain thirty-case/ten-deal/live benchmark design as an extension | User authorized the educational-scope review fixes; no distributed throughput claim or paid batch required for the core demo |
| P3-07 | Decimal precision 50; ratio/percentage display two places using ROUND_HALF_UP; threshold predicates compare exact signed numerator/positive denominator by cross multiplication where applicable | Display never changes policy outcomes; overflow/invalid arithmetic stops affected calculation |
| P3-08 | One operator/instructor completes five UI tasks and the 5/5 learning checklist; label self-assessment if applicable and record duration/help/errors | Three-person/120-second study remains an optional extension; no external-user study or user-time saving is claimed |
| P3-09 | Local offline NetworkX/Matplotlib graph rendering candidate, subject to compatibility/license check at repository gate | No remote Mermaid/image-rendering request or extra graph implementation |

Changes to an accepted decision require review and revision of dependent specs/evaluation rows before implementation. Unmapped actions remain denied. No interest-rate materiality tolerance, statement-recency duration, collateral haircut, credit score, concentration method, or legal applicability is invented.

Authorized SME fixes, 2026-10-23: complete walkthroughs require registered reviewed synthetic source/assessment/subject packs; unregistered Live uploads remain partial. SPEC-001 defines borrower/entity/facility coherence; SPEC-002 defines critical Live FACT support separate from KNOWN; SPEC-008 defines typed FACT/CLAIM support and CONDITIONS-1.0 without extra provider fields. SPEC-007 defines explicit same-revision support-only continuation without extraction replay/budget reset. Source support is data-quality review, not credit approval. SPEC-003/009 disclose covenant extraction without automated evaluation, deferred reported-EBITDA normalization/reconciliation, and annual-period rather than full-term/balloon analysis. The user requested these documentation fixes; they do not approve the pending repository/execution/implementation/spending phases or change thresholds/call limits.

Authorized Principal engineering fixes, 2026-10-23: SYN-WIRE-1.0 in SPEC-005, CANON-1.0/COVERAGE-1.0 in SPEC-006, PROVIDER-1.0/RUN-OUTCOME-1.0 in SPEC-007, RESUME-1.0 in SPEC-008, STATE-UPDATE-1.0 below and EVAL-CUTOFF-1.0 in the evaluation plan resolve AE-01–07 at documentation level. These versioned refinements are part of the source of truth, not additional runtime prompt packs. Existing TEST families are refined; ninety test IDs, thirty scenario designs, five UX tasks, two normal calls and unchanged cumulative limits remain. Compatibility/token fit/provider/source-pack authoring and repository/implementation approvals are still pending.

Authorized source-relevance refinement: [SOURCEFIT-1.0](context-optimization.md#source-relevance-authority-and-temporal-fit--sourcefit-10) distinguishes business-effective date, evidenced observation/knowledge cutoff, financial period, exact qualifiers and field-level authority. Retain source history but do not promote superseded/ineligible material to a current review. Unknown metadata/authority pauses affected use; newest upload and semantic similarity are not precedence. That SOURCEFIT refinement alone introduced no crawler; ADR-007 subsequently accepts the bounded public-reference crawler path. No retail-Q&A feature, universal recency threshold, automatic expiry, wire expansion, generation stage or core metric is introduced. Complete packs require reviewed basis/profile metadata, still to be authored.

Authorized Director recommendations are now incorporated as NARRATIVE-CHECK-1.0 (SPEC-005), INPUT-EDU-1.0 below, SOURCE-TRIAGE-1.0 (SPEC-008) and CONTINUE-CHECK-1.0 (SPEC-007). Use fixed field targets, one shared strict parser/validator, existing issue/capability records and a small path-count table; no new agent/framework/judge, screen, metric or model-wire field. Node counts and model cost are separate. Preserve no automatic expiry, two normal calls, all cumulative limits and the existing core/extension boundary. The next delivery work is the existing repository gate, then a concrete first-milestone execution/design-system plan and approved fixture implementation, not another broad architecture review or implicit scaffolding.

Subsequent user-authorized addition: [RAGAS-EVAL-1.0](../evaluation/ragas-evaluation.md) adds an explicit offline evaluator with five custom1–5 rubric dimensions, explanations/examples and separately labeled optional native metrics. It supersedes blanket no-judge wording only for offline evaluation, not the two-call deal graph or Evidence service. Implement within SPEC-011 evaluation boundaries with disabled-by-default lazy dependencies, frozen actual context/original response, strict results and separate approved evaluator allowance. Package/adapter/model compatibility and all runs remain Not run; no extra graph node, business threshold, screen, automatic scoring or hidden application request. The23 core MET IDs remain plus five RAG-R dimensions;90 TEST IDs and30 case designs are retained.

## Shared schema conventions — CONTRACT-1.0

Follow-up Principal fixes, authorized2026-10-23: the Extractor Runtime prompt names its exact DealTermsWire and forbids notes/domain metadata; REVIEW-BASIS-1.0 (SPEC-008) separates immutable analysis from current permitted review progress and prepares edited-condition targets before disposition; EXEC-ADMISSION-1.0 (SPEC-007) atomically admits one execution across same-database app/notebook/CLI entry points; STATE-CODEC-1.0 (SPEC-011) defines exact primitive storage/rehydration and noncircular narrative-content identity. Keep these canonical details in their feature specs rather than copying them into model prompts. Existing case/test/metric families own verification; all runtime behavior remains Not run, and repository/execution gates remain pending.

The following are field-level contracts for later Pydantic models, not executable code. Unknown properties are rejected on trust-boundary models. Required fields are not silently defaulted. IDs are generated UUID strings; revisions are positive integers; versions are nonempty strings; timestamps are timezone-aware UTC. Text is trimmed for validation without altering source text. Confidence accepts a finite JSON number, not a string/Boolean. Decimal financial values serialize as canonical decimal strings; reject NaN/infinity, ambiguous units, and Boolean-as-number coercion.

| Type | Required fields and validation |
|---|---|
| ActorContext | persona: Analyst/RiskManager/ComplianceOfficer/AuthorizedApprover/Administrator; workspace_id; service-resolved allowed_deal_ids/capabilities/allowed_review_tiers; attribution: SIMULATED. Submitted role/tier text cannot grant a capability |
| CommandMeta | operation_id; deal_id; expected_input_revision; actor; payload_digest. Mutations also compare expected_record_version for metadata lost-update protection |
| SourceRef | Discriminated by source_kind: DOCUMENT requires source_id/version, page_number >=1 and passage_id resolving through the manifest; POLICY requires rule_id/version and registry locator; REVIEWER requires correction/assessment ID and attribution reference, including CASE_AUTHOR_ASSESSED for a supplied synthetic case assessment, not falsely attributed human approval. No fabricated PDF page for a policy or assessment record |
| PeriodBasis | period_start/end ISO dates or as_of date as appropriate; assessment_basis_id; basis_label HISTORICAL/PRO_FORMA/DOCUMENTED_PROJECTION; trusted subject/facility registry refs and scope status. Projection is supplied evidence, never generated; compatible dates alone do not prove borrower identity |
| ReviewSourceBasis / SourceSelectionRecord | SOURCEFIT-1.0 defines review_as_of, evidence_cutoff_at, purpose, source-profile/policy versions, selected candidate references and scoped alternatives/reasons. This is distinct from financial PeriodBasis and application input revision; Python/configuration owned, not extra provider-wire fields |
| Fact | fact_id; field_name; raw_text; field-registered normalized value: strict string, strict integer, Decimal-string, ISO-date string, typed list or typed InterestTerms object, nullable when absent/conflicting/invalid; unit/currency/basis nullable only where specified; provenance DOCUMENT/REVIEWER/NONE; source_refs; status KNOWN/MISSING/CONFLICT/INVALID; separate fact_support_refs. KNOWN is not semantically verified. Booleans are never integers. Provider wire remains unchanged; support contract is in SPEC-002 |
| FactSupportRecord (FACT-SUPPORT-1.0) | Current scoped fact/value/source/basis/subject digests; mechanical checks; PENDING/REFERENCE_CHECKED/HUMAN_SUPPORTED/UNSUPPORTED/WITHHELD; actor/method/reason/time/operation. SPEC-002 defines Live critical-fact permission and explicitly labeled Fixture execution |
| ConditionRecord | Scoped derived condition identity/origin/category/text/refs/owner/status/linked issue; SPEC-008 defines provenance, existing-gate-derived blocking and report completion versus outstanding conditions. No extra PanelDecision fields or model call |
| StageEnvelope[T] | artifact_id; schema_version; deal_id/run_id/input_revision/task_id; sender/recipient; mode FIXTURE/LIVE; instruction_version/hash where used; dependency_digest; result T; validation VALID/PARTIAL/INVALID; references; started_at/finished_at; error nullable |
| ServiceResult[T] | status OK/PAUSED/REJECTED/STOPPED; value nullable; errors list; current_record_version; operation_id |
| ErrorRecord | code; stage; safe_message; retryable; affected_scope; reference_ids. Never credentials, hidden reasoning, raw provider body, or full prompt |
| Issue | issue_id; detection/current revision; rule/control ID/version; agent; sources/metrics/findings; observed/threshold/unit; reason; policy_outcome nullable; workflow_status; severity INFO/MEDIUM/HIGH/CRITICAL; owner_category; affected_nodes; blocks_completion; required_action; resolution_state OPEN/ACKNOWLEDGED/RESOLVED/DISPOSITIONED/SUPERSEDED; history IDs |
| Claim | claim_id; text; kind FACT/CALCULATION/INTERPRETATION/PROPOSED_CONDITION; critical Boolean; source/finding/calculation refs; support_state PENDING/REFERENCE_CHECKED/HUMAN_SUPPORTED/UNSUPPORTED/WITHHELD |
| ReviewRequest | pending_review_id; same thread/deal/run/revision; panel/artifact refs; analytical_basis_digest; review_gate_version/snapshot digest; trigger reason codes; score/configuration/referral refs; required owner categories and NORMAL/SENIOR review tier; current gates; permitted actions; created_at. SPEC-008 distinguishes analysis invalidation from valid handling progress and exact condition drafts |
| ReviewState | NOT_EVALUATED/NOT_REQUIRED/PENDING/RECORDED/STALE; disposition_id nullable. NOT_REQUIRED is never Human approved |

Absent values remain explicit, never replaced by zero. Source facts, corrections, calculated facts, model interpretations, human decisions, and collaboration notes are separate types. Exact per-feature result schemas extend this common envelope.

## Strict external input limits — INPUT-EDU-1.0

The Director-recommended fixes are authorized for this educational prototype. This versioned technical profile applies to externally submitted command JSON and provider structured payloads, not the original PDF bytes, complete source inventories, saved event histories or report length. Existing intake/token/cost limits remain separate and authoritative. Limits below are explicit implementation choices for the supported synthetic cases, not bank lending thresholds, rate restrictions or permission to truncate data.

| Boundary | Technical limit / behavior |
|---|---|
| Structured command/model-content JSON | At most 65,536 UTF-8 bytes, nesting depth 12 (root depth 1), 64 members per object or items per array, and 4,096 Unicode code points per decoded string; narrower existing wire/field constraints still apply |
| JSON interpretation | Exactly one complete root object for these contracts; no trailing document/text, duplicate decoded member names at ANY nesting level, NaN/Infinity or invalid Unicode scalar values. Reject duplicates before converting to a dictionary/Pydantic model, including names made identical by JSON escapes. No last-value-wins behavior |
| Normalized financial inputs | Canonical finite plain Decimal strings, at most 18 integer digits and 6 fractional digits, excluding sign/decimal point from digit counts; at most 26 characters including optional minus sign. No scientific notation, commas, currency symbols, leading plus or silently removed precision. Zero is canonical 0. Normalize documented units exactly before checking this bound; preserve original source text/units |
| Integer input fields | Strict JSON integers, no Boolean/string/float coercion; at most 18 digits before applying existing field-specific positivity/range rules. A term remains documented months, not a guessed date conversion |
| Confidence JSON number | Parse exactly without an intermediate binary float; finite 0..1, at most 24 significant digits and 24 fractional digits after exact expansion, raw literal at most 32 characters. A bounded exponent is allowed only if those expanded limits hold; never round to pass validation or change the 0.7 comparison |
| Provider HTTP response envelope | Read at most 262,144 bytes before full envelope parsing. Reject duplicate keys/invalid constants and enforce bounded parser nesting. Apply the model-content limits separately after the verified PROVIDER-1.0 envelope mapping. An oversized/unreadable post-dispatch response retains unresolved usage reservations; it is not free or financial Reject |

For financial strings, use the existing canonical format with no redundant leading integer or trailing fractional zeros; preserve supported negative CFADS/EBIT values. A normalized value outside the technical profile returns INVALID_INPUT/INVALID_SCHEMA with a safe field/limit reason and pauses affected use; do not clip, round, cast or present a loan-policy failure. Raw JSON numeric literals are length-checked before Decimal/int construction; depth/size guards must act before unbounded recursion/expansion. Apply duplicate checking to both the provider envelope and any embedded JSON content. Narrow shape/type validation then runs under existing CONTRACT/SYN-WIRE/ExtractionWire schemas. Retain the exact validated confidence through hydration, routing and canonical identity; a float conversion/display must not move a value across 0.7. The illustrative PRD float-style class does not authorize precision loss in these comparisons.

The profile belongs in existing trusted configuration and its version enters schema/config/cache/fixture dependencies. Within the supported FIN-1.0 formulas and current thresholds, bounded inputs plus precision 50 must preserve exact addition/subtraction and threshold cross-products; the first compatibility task verifies this at boundaries. Repeating ratio division is legitimately rounded at the calculation/display layer and must not be rejected merely for being inexact. Compare threshold numerators/positive denominators exactly; do not round input values to display precision. If arithmetic exceeds its supported exact bounds, stop the affected calculation rather than accepting silent rounding. Derived metrics keep their formula-specific result schema; do not apply the external money-string bound blindly to a repeating ratio/result.

Enforce with a small shared parser/field validator and standard-library JSON/Decimal plus existing Pydantic validation, not another framework. The actual selected provider profile must fit the transport bound; incompatibility requires a reviewed profile revision, never silent fallback. TEST-002-04/07, TEST-003-06, TEST-005-01/06, TEST-006-04/05 and TEST-007-03/06 cover nested/escaped duplicate keys, resource limits, exact boundary values, negative/zero/repeating valid values, ambiguous output rejection and independent usage retention. These are planned checks, not an implemented parser or measured compatibility result.

Sources: Python documents [duplicate-name/default JSON behavior](https://docs.python.org/3.12/library/json.html#repeated-names-within-an-object) and [Decimal precision/signals](https://docs.python.org/3.12/library/decimal.html). Use the project-pinned runtime behavior at implementation; this documentation adds no package installation or provider request.

## Shared graph state and ownership

| State key | Type/owner |
|---|---|
| identity | deal_id, review_id, run_id, thread_id, input_revision, mode, scenario_id and fixture_variant_id nullable, start_stage, policy_version, schema_version |
| manifest / terms | DocumentManifest / DealTerms; SPEC-001/002 |
| financial_panel / compliance_panel / risk_panel | Versioned stage artifacts; SPEC-003/004 |
| synthesis / panel_decision / evidence_review | SynthesisResult; five-field PanelDecision; EvidenceReview; SPEC-005 |
| issues / routing / review | Issue references; RoutingResult; ReviewState/HumanDisposition; SPEC-004/007/008 |
| budget | Durable ledger reference plus current conservative totals; SPEC-007/011 |
| report_markdown / report_metadata | Current generated artifact only; SPEC-009 |
| artifact_refs / event_cursor / stop_reason | Structured references; ordered event sequence; safe error/control reason |

State is not automatically serialized into an LLM prompt. Node owners replace their current artifact references through validated patches, not whole-state overwrites. Events/usage use repository writes with operation identities; do not append uncontrolled chat transcripts. No secrets or live client objects in serializable state. Actor/runtime services are injected, not model-controlled fields. The state-key table names logical domain types; STATE-CODEC-1.0 defines their JSON-compatible checkpoint representation and strict rehydration. In particular, internal stored confidence strings are not permission to accept string confidence from a model, and omitted patches remain distinct from explicit null clears.

Lifecycle is separately DRAFT/READY/RUNNING/WAITING_INFORMATION/WAITING_REVIEW/COMPLETED/STOPPED/CANCELLED. A technical stop is not Reject. COMPLETED may retain properly dispositioned sample exceptions and an explicit simulated recommendation; it never means approved funding or verified law. Superseded artifacts remain history.

## Current-state replacement and invalidation — STATE-UPDATE-1.0

AE-06 uses ordinary default replacement for the sequential current-state channels; no append reducer or chat history. Each owner writes a validated patch. Omitted keys mean preserve; explicit null clears nullable current artifacts, [] clears a reference list, and an empty object is not a substitute for null. Required identity fields cannot be cleared. Lifecycle is the persisted RunRecord outcome, not an inference from a stale PanelDecision/report in state.

| State key/group | Replace, clear or preserve rule |
|---|---|
| identity | Immutable per run/thread. A correction/support continuation creates a new validated identity snapshot; never patch an existing thread to a different revision |
| manifest / terms | Replace only by their owner with scoped current artifacts; clear terms on affected source replacement before extraction. Source-backed corrections create derived current terms; original extraction remains historical |
| financial_panel / compliance_panel / risk_panel | Replace current artifact refs on accepted owner output. Explicitly null every affected panel on value/source/basis/subject/support/configuration invalidation; do not retain a prior successful panel after a failed recomputation |
| synthesis / panel_decision / evidence_review | Clear affected downstream artifacts to null before continuation/recompute. Publish only current validated results. A failed or absent synthesis cannot leave its old decision current |
| issues | Replace the complete current scoped issue-reference set after each accepted evaluation, deduplicated by configured issue/root identity. No append-on-every-node behavior. Preserve unaffected current issues explicitly through the service projection; historical issue events stay outside this list |
| routing / review | Reset affected routing to null and review to NOT_EVALUATED with disposition_id=null; mark prior pending requests/handling STALE in storage. NOT_EVALUATED cannot mean NOT_REQUIRED or carry an old accepted disposition |
| report_markdown / report_metadata | Clear both to null whenever report dependencies change, including support-only changes. Prior reports remain historical and visibly out of date; no current download/completion label for them |
| artifact_refs / event_cursor | Replace current artifact index, with invalidated refs removed and verified reused refs explicitly re-enveloped. History is read from durable artifacts/events, not accumulated in this key. Cursor advances from persisted ordered events only |
| budget | Preserve the SAME durable review_id ledger and all committed/unresolved reservations. Refresh its snapshot from the repository; a graph patch cannot reset counters or grant allowance |
| stop_reason | Clear to null only on an explicitly authorized validated continuation becoming READY/RUNNING. On stop replace with the new actual reason; preserve the previous reason in run/event history |

Construct a new-run snapshot by clearing the full affected dependency closure FIRST, then inserting only independently verified unaffected artifacts with fresh current envelopes. Support-only continuation keeps input revision but changes relevant dependency lineage and clears downstream results just as a source/value change does. Read-only previews and citation inspection do not apply patches. Saving an authorized correction/support change updates invalidation without executing graph/model work. A repeated operation reuses its committed patch/receipt without duplicate issue/condition/history entries; it never applies an older patch over a newer record version.

Existing TEST-007-07/08 and TEST-011-01/02 cover repeated node updates, empty-list/null clearing, source/policy/support-only invalidation, stopped synthesis after prior success and preserved history/budget. Verify the pinned LangGraph default overwrite semantics during compatibility testing; if a channel later gains a reducer, its explicit reset behavior needs revised specs/tests first. No custom reducer framework is required.

## Shared service and error conventions

Streamlit calls ordinary Python application services; names in each spec are proposed internal contracts, not deployed REST endpoints or third-party APIs. Read services require selected workspace/deal scope. Commands validate current identity, persona/capability, revision, operation identity, and gates in services as well as UI.

Same operation ID plus same normalized payload returns its original receipt. Same ID with a different payload yields OPERATION_CONFLICT. A stale expected revision/record version yields STALE_REVISION/STALE_RECORD. No command may create a duplicate paid action while returning a duplicate receipt.

Shared errors include INVALID_INPUT, UNSUPPORTED_DOCUMENT, LIMIT_EXCEEDED, FIXTURE_MISMATCH, FIXTURE_VARIANT_UNAVAILABLE, MODE_UNAVAILABLE, MISSING_DATA, SOURCE_CONFLICT, INVALID_SCHEMA, INVALID_REFERENCE, UNSUPPORTED_CLAIM, POLICY_UNAVAILABLE, CONFIGURATION_REQUIRED, PERMISSION_DENIED, BUDGET_EXHAUSTED, TIMEOUT, PROVIDER_ERROR, OUTCOME_UNKNOWN, CANCELLED, STORAGE_ERROR. Error-to-issue/lifecycle effects are specified by the affected feature.

All mutation tests include wrong deal/workspace, stale revision, repeated operation, and wrong persona where relevant. Fixture adapters return only registered matching scenario artifacts; real deterministic nodes still execute.

## Core educational acceptance and deferred extension

The user's issue-fix instruction authorizes this refinement of the previously broader acceptance workload. Keep all six target screens at basic functional fidelity, one shared graph, source/formula navigation, the pure seven-section memo, one-worker/one-SQLite design, focused critical tests, graph-only Jupyter, lightweight HTML and no automatic expiry. Do not introduce production infrastructure.

Core fixture acceptance uses three walkthrough cases (E-N01, E-P01, E-M01), the source-backed E-N01/extraction-miss correction variant, and the E-F03/reject-supported QA variant. E-M01 stays paused while CFADS is genuinely undocumented; never clear it with an uncited number. A four-outcome fixture demonstration covers Approve, Conditional Approve, Reject and no decision/information pause. Examples are [wire mapping](examples/extraction-wire.md), [correction flow](../evaluation/examples/e-n01-correction.md) and [Reject QA](../evaluation/examples/e-f03-reject.md).

User clarification: both QA checks stay high level in offline evaluation notes. False-positive counting adds no new interface indicators, dashboard or scoring workflow. E-F03 retains its documented Reject path. Detailed precision tooling is deferred. Direct page/passage selection remains the core loan grounding approach; ADR-007 separately selects Nebius-hosted embeddings under ADR-008 for the public-reference extension, pending setup and implementation. The subsequently approved proposed [SEG-1.0 document-specific size/overlap profiles](context-optimization.md#document-specific-segmentation-and-overlap--seg-10) guide implementation; there is no active runtime configuration or universal fixed window. Financial tables, complete rule qualifications and source provenance take priority over numeric targets.

Authorized extension on2026-10-23: [RET-1.0](context-optimization.md#shared-evidence-selection-interface-and-optional-benchmark--ret-10) plans a shared evidence-selection adapter from initial implementation and an [optional DIRECT/keyword/vector/hybrid benchmark](../evaluation/hybrid-retrieval-benchmark.md). Initial core uses DIRECT only; benchmark backends/dependencies are lazy, local and confined to an offline entry point. Graph nodes/agent prompts consume the same ContextPacket, avoiding a later pipeline rewrite. Backend implementation and optional setup are still real future tasks; no zero-code-change guarantee, extra model stage, benchmark UI, paid invocation or five-day core requirement is introduced.

Authorized UX review fixes on2026-10-23: [UX-1.0 in SPEC-010](command-center-ui.md#simplicity-attention-and-interaction-contract--ux-10) defines five-column default scanning, three-step intake, Workspace-first issue/owner/action and all mandatory blockers, paired evidence, progressive detail, correction impact/Save/explicit continuation and separate memo recommendation/review/report labels. Preserve all five screens and25 existing UI IDs. Numeric confidence is uncalibrated detail, not a gauge; critical review reasons remain visible. SPEC-007/008 make correction Save prepare READY state with no dispatch; explicit continuation remains required. SPEC-009/012 retain the seven-section report and offline HTML boundaries. Existing tests are refined, not executed or multiplied into a production usability program. Core measurement uses UX-T01–05 and the separate learning checklist.

Keep all thirty case designs and the 18/12 split. Authoring/executing the full corpus, ten-deal coordination run, three-person usability study, held-out model-quality benchmark and thirty-run p95 workload are follow-up educational exercises, not five-day core gates. Do not label unexecuted extensions Passed. The later API-backed prototype still requires at least one validated authorized Nebius run; fixture completion is reported separately.

First approved implementation milestone must include a bounded compatibility/feasibility check: strict wire-to-domain round trip; source-layout parser selection/licensing before parser installation; Python/dependency and SQLite interrupt/resume checks; serialized context/output size; one correction budget trace. Provider/model-specific structured-output/token accounting awaits access and separate execution allowance. Stop or revise the representation if essential evidence cannot fit; no automatic budget increase or schema weakening.

## Implementation prerequisites and required evidence

User-authorized addition, 2026-10-23. This is the canonical remaining-prerequisites checklist, not the gated Phase 5 execution plan or permission to install dependencies, scaffold, run paid services or deploy. It organizes the already agreed controls and deliverables; it adds no feature, banking rule, test family, metric, budget or production-readiness program. The five-day target begins after prerequisite approvals. Prepare and verify the smallest useful local path first; connect the paid provider only after its own prerequisites are satisfied.

Suggested owners below describe delivery responsibilities, not new application personas or financial authority. No named person, completion date or execution result is assumed. Current statuses describe work readiness, not loan decisions. Writing this checklist does not make an item VERIFIED.

| ID / prerequisite | Required before | Dependencies | Current status |
|---|---|---|---|
| PREREQ-01 Approved repository and first build milestone | Any application scaffolding/implementation | Existing Phase 4 and Phase 5 approval gates | VERIFIED for M1 scope on2026-10-23: user instructed applying the reviewed recommendations and moving forward after the concrete M1 request; later gates unchanged |
| PREREQ-02 Compatible local foundation and persistence harness | Dependent persistent workflow features | PREREQ-01 | VERIFIED for M1 foundation: resolved environment/uv.lock, exact codec, real saver/restart/resume and cross-process admission passed; full deal integration still needs its own checks |
| PREREQ-03 Exact prompt/schema/context contracts | Accepted model-stage artifacts and subsequent provider integration | PREREQ-01; use PREREQ-02 environment for execution | IN_PROGRESS; raw parser/canonical/runtime hashes and Pydantic wire/schema tests passed; complete case contexts and provider tokenizer/template fit remain pending |
| PREREQ-04 Reviewed synthetic sources and case configuration | A complete fixture review | PREREQ-01; approved parser/environment before parsing | IN_PROGRESS overall; E-N01 extraction and synthesis registered and normal graph/memo tested. Other source packs/variants and broader intake/Live support remain pending |
| PREREQ-05 Executed core fixture workflow and critical controls | Claiming the fixture pipeline works | PREREQ-02/03/04 | PARTIAL overall; normal and reviewed E-N01, same-thread human resume, registered-response reassessment and memo/history tested; other core source scenarios remain pending |
| PREREQ-06 Usable six-screen and offline teaching artifacts | Claiming the user-facing fixture demo is complete | PREREQ-05; existing approved design-system/milestone gates | PARTIAL overall; six-screen normal/review UI, graph notebook and clickable HTML created; notebook kernel and full accessibility acceptance pending |
| PREREQ-07 Verified, authorized Nebius integration | Any paid Live dispatch; validated run before Live-demo acceptance | PREREQ-02/03/04/05 and explicit access/allowance; final user-facing demo also needs PREREQ-06 | NOT_CONFIGURED; Live unavailable and execution Not run |
| PREREQ-08 Configured optional RAGAS/hybrid execution | Enabling that selected extension | Relevant verified core contracts/admission; separate optional milestone/dependencies and allowance where paid | PLANNED_EXTENSION; execution disabled/not configured, results Not run |

### PREREQ-01 — Confirm exactly what may be built

- Suggested owner: user for approval; builder for concrete review material.
- Current progress: the user's 2026-10-23 instruction advances the existing repository direction into Phase 5 planning. [Execution plan](../execution.md) and [design-system proposal](../design/design-system.md) now exist, with M1-01–09 files, checks, definition of done and rollback/stop conditions. M1 approval and the later explicit installation permission are recorded; root AGENTS.md is active. Setup,43 scoped tests and local build passed. Later source/parser/model/paid decisions remain separate; do not request the same M1 approval again.
- Required evidence: explicit approval references bound to the reviewed content/revisions. Record which decision is still pending; installed tools, an API key or a general documentation-fix request cannot stand in for these approvals. Parser/project licensing, publication/deployment and paid execution keep their separate boundaries.
- Why first: a builder needs a concrete agreed target; this prevents implementing an older design or treating a planning update as permission to spend.

### PREREQ-02 — Prove the local foundation can save and continue safely

- Suggested owner: builder, with a technical reviewer when available.
- Resolve/pin the approved Python/Pydantic/LangGraph/SQLite/Streamlit foundation for the actual Windows environment after the milestone gate. Record dependency/lockfile provenance rather than guessing supported versions. Keep optional notebook, retrieval and RAGAS dependencies lazy and out of the first setup unless needed by that milestone.
- Required evidence: actual controlled checks of STATE-CODEC-1.0 exact save/checkpoint/restart/restore, explicit null clears and stable fingerprints; persistent interrupt/resume; accepted-receipt/checkpoint crash gaps; and EXEC-ADMISSION-1.0 contention from two independent processes/connections. Only one contender may execute; Busy cannot record a disposition, and an uncertain claim cannot be stolen or automatically replayed. Use isolated temporary databases, injected clocks/controlled transports and denied provider network traffic. No secrets or live client objects enter saved state/logs.
- Existing verification: TEST-011-01/02/03/04, TEST-007-02/05/06/07, TEST-006-05 and the exact arithmetic boundaries in the evaluation plan. A mocked saver alone cannot prove restart behavior. Stop dependent work if compatible versions or exact restoration cannot be demonstrated.
- Why first: reopening a review must retain its meaning, and two Start buttons must not launch conflicting work.

### PREREQ-03 — Prove agents receive and return the intended information

- Suggested owner: builder with fixture/evaluation reviewer.
- Load only the allowlisted Runtime sections/shared rules with their expected hashes. Verify the Extractor's three-root DealTermsWire and Synthesizer's SYN-WIRE-1.0, Python hydration, unknown-field rejection, explicit missing/conflict handling, all-field evidence targets and exact current logical reference dictionaries. Keep evaluator gold, full role documents, unrelated deals, operator notes and audit histories out of model context.
- Required evidence: executed local prompt/schema/example/domain round trips and negative cases for extra notes/raw_text/status, fabricated references, duplicate keys, invalid types, unauthorized authority fields and wrong instruction/profile identity. Preserve complete COVERAGE-1.0 source spans, qualifier/table context and SOURCEFIT-1.0 selection basis through DIRECT packing. Serialize ordinary and Conditional synthesis examples plus a protected correction path; record actual serialized bytes/components locally. A character-based or unverified token estimate is labeled an estimate and cannot establish provider fit.
- Existing verification: TEST-002-07, TEST-005-01/03/06, TEST-006-01/03/04/05/08. Exact selected-model tokenizer/template/schema accounting is completed under PREREQ-07; local contract success does not enable Live or require an API key. If material evidence/output cannot fit, retain the stop behavior and review lossless representation/allocation within existing ceilings.
- Why first: correct instructions and complete evidence are needed before an agent's answer can be trusted or economically tested.

### PREREQ-04 — Prepare believable, fully supported synthetic deals

- Suggested owner: builder/case author, with an instructor or reviewer checking the case.
- Resolve the candidate parser's licensing/compatibility before installing it or committing to its API. Author the initial E-N01 text-PDF package and then the existing E-P01/E-M01 plus correction/E-F03 variants as required by the approved slice. Keep the intake limit of three PDFs, ten combined pages and10MB; trusted policy configuration is separate. All values are synthetic.
- Each complete pack needs actual source bytes/content digests and original page/span maps, coherent borrower/facility and period/subject registries, review-as-of/knowledge-cutoff and field-authority basis, the versioned sample policy/applicability, five explicitly authored factor assessments with material source requirements, and matching current-input fixture variants. Runtime assessments are separated from evaluator-only gold. Do not substitute this document's prose for a PDF or invent a factor grade at runtime. Retain a supported Low assessment if demonstrating E-N01's direct route; otherwise author its matching required-review variant. E-F03's Reject remains case-specific; a threshold breach is not a universal Reject rule.
- Required evidence: reviewed package/config/fixture digests; reconciled FIN-1.0 expected arithmetic; real original source locations and all required qualifiers; scope/currentness and missing-versus-zero checks; correct missing evidence in E-M01. Author/evaluate first-attempt extraction/synthesis expectations separately from later human corrections. No real borrower data is committed or ingested.
- Existing verification: TEST-001-02/03/04/05/06, TEST-002-03/04/07, TEST-004-10/11 and case-specific evaluation references. Unregistered uploads stay partial; missing reviewed configuration cannot be filled from another case.
- Why first: a convincing demo requires documents and evidence that actually support its numbers and outcomes.

### PREREQ-05 — Demonstrate one real fixture pipeline, then its necessary branches

- Suggested owner: builder and reviewer/operator.
- First execute E-N01 through actual parsing/registered extraction response -> deterministic financial/policy/risk work -> registered synthesis response -> evidence/routing -> permitted pure-Python report. Then exercise E-M01's information pause, E-P01's specialist/package review, E-N01's documented-value correction and E-F03's supported Reject path. They remain three core walkthroughs plus existing-case variants, not a requirement to author/run all30 designs first.
- Required evidence: recorded actual dispatch/handoffs, typed current artifacts, source-linked calculations/policy/risk results and a seven-section generated report tied to its real run/cutoff. Verify REVIEW-BASIS-1.0's handling-versus-analysis distinction, edited-condition draft/support before disposition, duplicate/stale/wrong-role/tier rejection, original AI versus human edits, same ledger after corrections, exact node/tool/attempt accounting and all applicable critical controls. Confirm two-deal isolation with existing scenarios. Default Fixture makes zero provider requests; do not present its canned model stages as actual model-quality evidence.
- Test controlled refusals/truncation/invalid output/uncertain dispatch and budget stops without deliberately spending on failures. Retain partial work and explicit unknown states; technical failure or missing information cannot count as a Reject. Record the agreed high-level risk false-positive count alongside recall offline, without adding a QA dashboard. Preserve no automatic expiry across restart/time advancement.
- Existing verification: the core/QA protocol and TEST-007/008/009/011 families. Require actual per-check evidence and failure reasons, not a green summary inferred from planned TEST IDs. One successful E-N01 run enables the next slice, not a claim that every branch passes.
- Why first: an executed narrow example exposes integration problems faster than building every screen around untested outputs.

### PREREQ-06 — Make the result understandable and inspectable

- Suggested owner: builder/designer and the operator/instructor; unfamiliar-person feedback remains optional.
- Build the five existing screens against shared services and the approved design-system/milestone scope. Verify sample preparation versus explicit Run, complete versus partial upload, fixed accessible term help, current owner/next action, separate credit/policy/evidence assessments, exact condition drafts, confirmed save/pending/recovery messages and the outcome/conditions/action recap. Keep every mandatory blocker visible. Render citations beside the detail being checked, opening actual source versions/locations or recorded formulas/policies and preserving return context.
- Required evidence: the existing UX-T01–05 with honest task outcomes/duration/help/errors and descriptive interaction counts, plus actual keyboard/focus/status/narrow/zoom/source-navigation checks. Core target remains5/5 with critical controls intact; an author's self-check is labeled self-assessment. Headless checks and proposed colors alone do not establish accessibility or ease of use.
- Notebook/HTML evidence: a fresh-kernel graph-only notebook uses the same real graph metadata with no key/provider/network/state write; the local five-screen HTML opens offline and labels illustrative versus executed fixture snapshots. Its clicks cannot pretend to persist approvals or process arbitrary uploads. Link any executed sample memo/snapshot to the actual run, not prewritten demo output.
- Existing verification: TEST-010-01–07, TEST-012-01–06, TEST-009-05 and MET-19/20. Keep fixture-demo completion distinct from Live-demo completion.
- Why first: users need to find evidence and finish the permitted task; technically correct results alone do not prove a usable demo.

### PREREQ-07 — Enable Nebius only after compatibility and spending are explicit

- Suggested owner: user supplies access/allowance; builder configures and verifies the adapter/profile.
- Record the exact selected model/provider configuration, supported schema mode and parameters, response/refusal/truncation mapping, tokenizer/template assumptions, dated rates and complete billable output/usage handling. Validate controlled transport fixtures and keep SDK/transport retries, defaults/fallbacks and model-accessible tools disabled unless already explicitly permitted. A key is stored only through the approved local secret path/environment and never in source, checkpoint, notebook, HTML, logs or fixtures.
- Before any paid dispatch, obtain the explicit bounded total execution allowance as well as the existing per-review limits. Verify full request/schema/evidence and maximum output reservations for ordinary and Conditional paths and the protected correction allowance. Preserve cumulative8,000 input/2,000 billed output, five actual attempt ceiling,20 nodes/12 tools, USD0.10 target/USD0.25 hard cap and180 active seconds/45-second operation limit. These are existing caps, not extra funds; lower stage targets remain unmeasured until the selected profile is checked. Unknown accounting/pricing or infeasible faithful context leaves Live unavailable, with no silent truncation, larger ceiling or provider fallback.
- Required evidence after explicit funding/access: at least one validated registered synthetic end-to-end Live run with the required factual/semantic support and any applicable specialist/package review, actual provider attempts/tokens/usage/cost status, grounded output and generated report. Distinguish the two normal successful generation tasks from all actual attempts, cache reuse and human waiting. Observe outcomes; never copy the fixture's recommendation/confidence as though the model produced it. A single run proves the bounded Live walkthrough only, not held-out quality, p95, real lending value or production readiness. Paid judge work is separate.
- Existing verification: PROVIDER-1.0, TEST-007-03/05/06 and the evaluation plan's Live quality/cost protocol. If access arrives after the five-day window, deliver verified fixture evidence and report Live pending rather than declaring final Live acceptance complete.
- Why later: prove the local workflow before spending, then prove that the actual provider fits the same contracts and limits.

### PREREQ-08 — Activate optional evaluation/retrieval work deliberately

- Retrieval order: reviewed synthetic documents and frozen annotations first, then implement/report DIRECT, KEYWORD, VECTOR and HYBRID. VECTOR is the semantic retrieval baseline; RRF is rank fusion. A separately selected reranker follows only if measured ranking failures justify its added processing, using the [canonical benchmark decision/status record](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). Missing source/candidate evidence or packing failures require their own fixes. Keep specified/implemented/tested/measured states distinct; no retrieval result is established by M1 or by installing dependencies. RAGAS remains a separate optional evaluator, not this semantic baseline.

- Suggested owner: builder/evaluator with explicit run selection and allowance where paid.
- The requested RAGAS capability and native-score report are already planned. Their execution, and the hybrid retrieval experiment, remain separate selected extensions rather than prerequisites for the first core fixture slice. Default scoring/retrieval extras stay disabled; saved score reports show Not run or the applicable honest missing/inapplicable status.
- Required evidence before enabling: pinned compatible lazy adapters; frozen saved actual response/context and separately labeled evaluator reference; explicit selected samples/metrics/model artifacts/configuration and bounded work/allowance; EXEC-ADMISSION-1.0 admission before real judge/embedding work; no default provider, regeneration of the loan review or model download at import/startup. Verify the single shared custom-rubric bundle and five local projections, while accounting for additional native judge/embedding requests separately. Keep native scales/statuses separate from the custom1–5 rubric and credit scores; DIRECT ranked precision remains Not applicable. Hybrid uses the existing ten-query protocol and unchanged app DIRECT default until a later adoption decision.
- Existing verification: TEST-006-09, TEST-011-07, TEST-007-05/06/07, the RAGAS protocol and optional hybrid benchmark. No native result, universal aggregate/pass threshold or winning retrieval strategy is invented. Optional package/network setup and paid execution keep their existing gates.
- Why separately: measuring quality is useful, but hidden evaluator calls or a larger retrieval stack must not delay or inflate the first working example.

### How completion will be recorded

Use one local prerequisite evidence record in the existing evaluation/run notes boundary, not a new dashboard/database. Required fields: prerequisite_id; scope CORE_FIXTURE/LIVE/OPTIONAL_EXTENSION; status; relevant spec/config/dependency versions or content digests; responsible reviewer/actor as actually recorded; prerequisite dependencies; exact approved command/manual procedure if executed; attempted time; observed result/limitations; evidence artifact references; and verification date/reviewer. Before execution, command/time/result/evidence are explicitly Not run/unavailable, not fabricated identifiers or zero cost. No secrets, borrower/source text or raw prompts enter ordinary telemetry.

Statuses: PENDING_APPROVAL, NOT_STARTED, NOT_CONFIGURED, IN_PROGRESS, VERIFIED, FAILED and PLANNED_EXTENSION. VERIFIED requires the actual scoped evidence and completed dependencies, not merely authored documentation. Failed or missing evidence stays visible; retries retain prior attempts. A static-doc check, controlled transport test, executed fixture, actual Live run and actual offline evaluation have their existing distinct evidence labels. Never mark a whole prerequisite VERIFIED based on a narrower partial proof. The later approved execution plan may split these checks into small tasks without changing this source of truth or resetting allowances. Unselected extensions remain honestly pending/planned rather than failed core gates.

## Implementation order and next gate

The user supplied [RISK-EDU-1.0](policy-risk.md#educational-weighted-risk-score--risk-edu-10): five explicitly supplied synthetic assessments weighted30/20/20/20/10%, higher=more modeled risk. SCORE-BANDS-1.0 uses confirmed unrounded intervals Low [0,25], Moderate (25,50], High (50,75], Very High (75,100]. SCORE-ROUTING-1.0 requires Moderate normal human underwriting, High Credit Risk Manager handling then package review, and Very High senior-tier Authorized Approver review. Existing independent controls retain precedence; no score automatically chooses Approve/Reject. Missing material factors/source inputs yield Insufficient Data with null total/band and pause dependent synthesis/readiness. Factor-rating generation and calibrated PD remain undefined, not silently inferred.

[SCOREVIEW-1.0](command-center-ui.md#risk-score-cards--scoreview-10) shows three independent current-revision assessments: credit risk, policy exceptions and missing required evidence. Coverage belongs in score explanation, not a substitute for document completeness. The41 Moderate/two exceptions/one missing example requires that missing item not be a material score input. A bounded validated score/band/driver projection enters the existing Synthesizer call; optional proposed_action is outside exact five-field PanelDecision, separately labeled from Python's actual Required action. Source/revision/configuration changes invalidate scores, dependent synthesis/routing and review acknowledgements. TEST-004-10/11 cover aggregation, classification, routing and counts; existing UI/HITL tests cover presentation/permissions. Five screens, five personas, two normal generation calls and unchanged cost/attempt limits remain; no real credit integration, additional predictive model or automatic execution.

User-authorized attachment adaptation on2026-10-23: [RULEVIEW-1.0](policy-risk.md#read-only-rule-evaluation-details--ruleview-10) adds a read-only condition/outcome drill-down in existing policy details. Same-handler traces connect exact rules/applicability/inputs/formulas/sources to recorded outcomes and separate workflow consequences; View rule evaluation adds no inference, recomputation or mutation. Missing/unevaluated/stale states remain explicit. No rule editor, no-code engine, external bank integration, new score, deployment action or generic validation/approval stamp is added. Existing UI-WORK-01/03 and UX-T03 cover the user interaction; planned TEST-004-09 covers trace integrity/boundaries and zero side effects.

Shared contracts/storage interfaces → intake → finance/policy/risk with goldens → graph and fixture adapters → extraction/synthesis validation → context/budgets → human review/corrections → memo/UI → notebook/HTML → evaluation runs. The later execution plan will break this into scoped milestones and exact files.

Phase 3 is approved and the repository direction has advanced into Phase 5 planning. Review [M1 in the execution plan](../execution.md) and the [design-system proposal](../design/design-system.md) next. No application scaffolding, executable schemas, synthetic source files, tests, notebook or HTML exists; first-milestone execution approval remains pending.
