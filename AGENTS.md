# AGENTS.md â€” Deal or No Deal AI

## Current upload acceptance update - 2026-10-25

User explicitly asked to fill Cedar Vale's remaining items as AI-verified.
Record Codex-assisted source-review metadata separately via ai_evidence_review,
not LIVE_SUPPORT/HUMAN_SUPPORTED and not a paid independent judge or Phase 2 run.
Preserve the existing human assessments and graph pause. Flag unsupported
repayment structure and unknown applicability rather than blanket supporting.
AI evidence records are scoped to current request/target/source digests and
visible to permitted reviewers; they never clear the human continuation gate.

User requests automatic uploaded-data population and calculations on all screens
for all permitted roles. Read-only uploaded_calculations previews may use the
existing Decimal kernel on scoped actual extraction after source/basis checks.
Label them preliminary and not human-verified; never persist a completed graph
stage, clearance, support receipt or decision from rendering. Preserve mandatory
fact/narrative interrupts and actual recorded stage outputs as authoritative.
See docs/specs/general-upload-acceptance.md for the bounded projection contract.

User authorized a narrowly labeled educational human approval override for
completed uploaded live reviews with Pending Review readiness and only PENDING
blockers. Follow docs/specs/uploaded-human-decisions.md. Require AuthorizedApprover
NORMAL tier, comments, current-version/digest checks and explicit acknowledgment.
Keep original readiness/AI proposal and unresolved checks unchanged; mark override
in history/export. No missing/stale evidence, policy exception, recovery, pending
information or graph-resume override. This supersedes unconditional approval
blocking only for that explicit educational human action.

The user's continuing instruction to remove demo execution blocks until they
request re-enabling covers the newly interrupted Sample Deal operation
1d478574-1e3d-426c-bfe5-622b75872e79. Isolate this exact request using guarded
version/identity checks; retain USD0.0007 unknown usage and all original records.
No provider reconciliation, paid replay or credit gate bypass. The local app
must run with network access: sandboxed Nebius GET /models failed, while an
approved unrestricted read-only GET succeeded with HTTP200 and the chosen model.

The user's instruction to remove the stuck execution block authorizes isolating
latest Sample Deal operation 51eef80e-e890-4c62-91bb-c25478a5adf1 under
docs/architecture/decisions/proposed-latest-sample-isolation.md. Preserve its
USD0.0007 unknown reservation and history, fence replay/late publication, and
release its claim after exact identity/version checks. Do not automatically
start a paid review or weaken spending, duplicate-call, or credit controls.

User explicitly approved isolating sizing request
fbb6ba9d-ba4b-5c5a-b0b8-11f350b413ea only, under
docs/architecture/decisions/proposed-sizing-probe-isolation.md. Apply the guarded
probe_recovery.isolate_probe with version checks; retain its USD0.0262147 unknown
reservation, original request, upload/profile and all historical reviews. Fence
replay/late writes and release only its execution claim. No paid retry or general
quarantine authority is granted by this approval.

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

## Approved uploaded single-deal demo - 2026-10-25

User subsequently authorized post-verification uploaded-deal human controls.
Follow docs/specs/uploaded-human-decisions.md: source-validated completed upload
only, required comments and current versions, role/tier checks, readiness-gated
Approve, explicit Reject/Pending/comments and supported information-response
review. Human events are separate from original AI draft/checkpoints. No blanket
verification, invented covenant dates, automatic decisions, provider calls or
new dependencies. Explicit human decisions supersede the earlier no-decision
demo boundary only after these backend checks; automatic draft generation still
does not create a human decision.

Subsequent explicit approval permits exact-ID quarantine also for operation
54b1dd19-7dad-4ead-b297-31aae29a0d86, as specified in
docs/architecture/decisions/proposed-new-demo-quarantine.md. Preserve its unknown
USD0.0007 reservation/history, fence replay and late writes, release only its
claim after version/evidence checks. This is not general quarantine authority.

User explicitly requested implementation of upload -> live review -> workspace,
activity and memo. Follow docs/specs/upload-live-demo.md. The bounded supported
package is the complete exact Standard Deal profile, matched by retained bytes
and parsed pages, with a distinct upload-derived Deal ID. Actual extraction and
synthesis run through the existing live graph; no saved-answer fallback. Reuse
the approved sample policy and authored scoring premises only for this exact
source profile. Preserve the uploaded page citation map, readiness, historical
contexts and existing DEMO_DRAFT/HUMAN_REQUIRED semantics. Other documents remain
inspection-only. This scoped extension supersedes older blanket no-upload-model
statements only for this supported package. No new dependencies or budget change.

## Approved Phase 1 demo policy - 2026-10-25

The user explicitly approved docs/specs/phase1-live-demo.md. New live reviews
use config/app.toml LIVE / DEMO_DRAFT, only after explicit Run. Existing reviews
retain their persisted HUMAN_REQUIRED checkpoints. Demo technical integrity
checks never count as human evidence support. Preserve approval readiness and
backend credit authorization; a draft is not a credit decision. No fabricated
human receipts. This approved exception supersedes older default-FIXTURE and
mandatory pre-draft human-checkpoint instructions for new demo drafts only.
Phase 2 (RAGAS, judges, optimization) is deferred. Validate functional behavior
and one bounded live UI journey within the existing shared USD0.10 allowance.

## Current measured execution â€” 2026-10-25

User authorized an explicit LLM fact judge for the 36 current live fact-review
targets. Follow docs/specs/live-fact-judge.md. tools/judge_live_facts.py uses the
existing evaluation transport, fixed model and shared USD0.10 allowance, with
three total paid batches and no automatic retry. The separately loaded evaluator
instruction is docs/agents/extracted-fact-judge.md, never a graph prompt.
Results are advisory: 31 accepted citation checks and five evidence flags; they
are not native RAGAS or HUMAN_SUPPORTED. Preserve the failed first report and
cached raw response, original sources, human gates and generation prompts. See
docs/evaluation/live-fact-judge-results.md for actual measurements and limitations.

User approved the bounded administrative quarantine in
docs/architecture/decisions/proposed-unknown-request-quarantine.md after its impact
explanation. It may abandon only aab508af-564d-461f-a4e7-cf0708ec29b6, retain its
unknown ledger and USD0.0007 shared reservation, block all replay/late publication
for that review, and release only the exclusive local claim. This is not provider
reconciliation or evidence of no charge. All human fact/narrative and credit gates
remain mandatory. Use existing SQLite records; no migration, reset or new runtime
database. See docs/evaluation/quarantine-results.md for actual activation status.

User authorized visible specialist roles/handoffs under
docs/specs/specialist-handoffs.md. Agent Activity uses existing scoped events and
artifacts; never persist synthetic message history or treat projected downstream
results as evidence support. Preserve two generation stages, all prompts and
the existing sequential graph. No third LLM or autonomous-supervisor claim.

User authorized the unified review UI in docs/specs/unified-review-experience.md.
The saved UI is the baseline. No mode radio; config/app.toml mode selects new
FIXTURE or LIVE execution. Preserve disabled flags, separate backend paths and
all human checkpoints. Historical source determines rendering/resume, not the
current configuration. Default remains FIXTURE; never activate paid calls on view.

See docs/evaluation/live-answer-quality-results.md for current evidence, which
supersedes older no-key/no-paid-call status statements below. Actual live
extraction passed and awaits human fact review; saved-synthesis native/custom
RAGAS ran. Do not claim a completed live journey or hosted semantic benchmark.
Preserve all human checkpoints and the cumulative USD0.10 shared allowance.

## Recommendation presentation update - 2026-10-24

Recommendation presentation is governed by docs/specs/recommendation-presentation.md. Reuse the five existing readiness outcomes and shared pure recommendation.py formatter. Do not add thresholds, a High-Risk Review status, agents or paid rephrasing calls. Keep original responses and historical memos intact; structured recommendations belong in the main UI and new reports, with original proposals in audit details.


## READINESS-1.0 current update - 2026-10-24

The approved READINESS-1.0 contract is docs/specs/approval-readiness.md. Deterministic eligibility belongs in route_review, with backend enforcement on direct approval and graph resume. Preserve exact original AI proposals, sources and historical reports. Future reporting is not a breach merely because fulfilment has not occurred. New read-only projections do not write assessments. No new dependencies or paid calls are required. Regression evidence is recorded in docs/evaluation/approval-readiness-results.md.


## LIVE-GRAPH-1.0 implementation update - 2026-10-24

User authorized completing the live graph and evidence checkpoints. Follow
[the live graph contract](docs/specs/live-graph-integration.md). The shared build_graph now has an explicit
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
and evaluation. See [live integration specification](docs/specs/live-synthetic-integration.md)
and [approved fit profile](docs/evaluation/live-fit-proposal.md).

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


**Current UPLOAD-FACT-1.0:** Follow
[docs/specs/upload-fact-review.md](docs/specs/upload-fact-review.md).
Analyst proposes source-bound annual CFADS/principal/interest with quote/token,
units/scale and subject/facility/annual basis. RiskManager alone records exact-version
support/withholding with seven checks and reason. Mechanical reference checks never
set HUMAN_SUPPORTED. Candidates are manual/UPLOAD_CANDIDATE_ONLY, not registered
deal/Live facts. Replacement invalidates support. CALC-004 preview requires three
compatible supported inputs; no score, policy clearance, approval/model/graph.
Complete critical-fact/source registry and financial onboarding remain pending.

**Current UPLOAD-1.0:** Follow
[docs/specs/upload-inspection-integration.md](docs/specs/upload-inspection-integration.md).
New Deal/Upload supports explicit Analyst synthetic-PDF inspection:3 files/10 pages/
10,000,000 bytes combined,45-second parser deadline and120,000 extracted UTF-8 bytes.
Retain originals under scoped ignored var/uploads and metadata/pages in existing
SQLite/admission. All five simulated roles read their local workspace upload library;
this grants no financial deal authority. INSPECTED_NOT_REVIEWED means no fixture
fallback, score, clearance, model, memo or automatic registration. Verify bytes and
citations. Partial persistence gaps retain recovery; no expiry/deletion/retry.
Semantic chunking/provider/index remain pending. This supersedes disabled-upload
observations only for inspection.

**Current CORRECTION-1.0:** Follow
[docs/specs/source-correction-integration.md](docs/specs/source-correction-integration.md).
Separate E-N01/extraction-miss uses unchanged PDFs with deliberately missing CFADS.
Analyst may restore only the registered900000/FY-ASSESS/FIN-P2 fact with reason.
Save atomically supersedes original, creates revision2/new run/thread READY and
retains the same review/ledger; Save dispatches no graph/model work. Explicit
Update affected findings revalidates sources/basis/versions/budget, records reviewer
correction provenance and runs the seven affected nodes. Never label changed
extraction as reused/model output. Preserve original and memo/history/citation trail.
No arbitrary field/value/new-document or completed/interrupted-review correction
in this bounded slice; E-M01 remains missing evidence. All budgets unchanged.

**Current CONDITIONAL-1.0:** Follow
[docs/specs/conditional-integration.md](docs/specs/conditional-integration.md).
E-P01 is registered: one unchanged source-backed annual-statements condition.
Require separate RiskManager exception handling, AuthorizedApprover preparation,
RiskManager FINANCIAL_RISK support, ComplianceOfficer POLICY_CONTROL support and
final AuthorizedApprover Conditional Approve/Reject. Replay actual persisted gates;
retain original Exception/AI and OUTSTANDING condition. No free-text condition edits,
fulfilment/funding, generic waiver or new documents. Preserve compact checkpoint
receipts, full history snapshots and all budgets. This supersedes old pending notes.

**Current EXCEPTION-REJECT-1.0 milestone:** User explicitly authorized RiskManager
exception handling followed by E-F03 supported Reject. Follow
docs/specs/exception-reject-integration.md. E-F03 is now source/rubric registered,
with actual reviewed graph, unsatisfied numerical-exception requirement, scoped
RECOMMEND_REJECT handling, gate-version reconstruction from persisted events and
final AuthorizedApprover Reject. The original policy remains Exception; no generic
Approve bypass. Full event snapshots stay in history; bounded fingerprinted receipts
travel in checkpoints. Preserve all existing depth/token/node/tool/time/cost limits.
E-N01/E-M01 unchanged; E-P01 Conditional, new-document continuation and Live pending.

**E-M01 integration:** User authorized the recommended immediate missing-data step.
Follow docs/specs/missing-data-integration.md. Exact config/registrations/e-m01.json
now binds five authored pages and the missing-CFADS extraction. Reuse existing
graph/worker: five normal nodes then conditional END WAITING_INFORMATION; no
Synthesizer, PanelDecision, complete score or final memo. Partial source inspection
is read-only and cannot become a synthesis task. Analyst may start only permitted
cases; E-N01 remains unchanged. E-M01 response/new-document continuation, E-P01/F03
runtime and specialty/Conditional gates remain pending. No new spend/dependency.

**Latest pending-work milestone:** User approved the synthetic core-case factor
assessments and E-F03 cash bridge in docs/evaluation/examples/core-case-authoring-proposal.md.
tools/prepare_core_case_sources.py now creates separate parsed source candidates;
they are not runtime registrations or completed Reject/Conditional graph evidence.
provider.py is a pure offline request/response boundary with no client/credential
or network dispatch. Main financial History now has scoped filters/pagination,
original event details and all-filtered CSV. Preserve existing prompts, E-N01
registrations, business rules and all budgets. User explicitly deferred optional
notebook dependency installation. Live dispatch/embedding/judge remain disabled.

**Current implementation status:** See [docs/implementation-status.md](docs/implementation-status.md). Earlier milestone progress paragraphs below are historical and superseded for implemented capabilities; requirements and safety boundaries remain active.


**Current financial milestone â€” FIN-REVIEW-1.0 / FIN-REASSESS-1.0:** Follow
docs/specs/financial-review-integration.md, authorized by the implementation-order
request. E-N01/default remains unchanged. E-N01/review is a separately registered
confidence0.65 response using existing SYN-ESC-012. The same graph/worker now has
financial prepare/interrupt, receipt-first Approve/Reject resume, memo and frozen
history/CSV. Request Information blocks final actions. RiskManager may assess
every item against an exact registered PDF and explicitly start revision2, keeping
review_id/ledger but using a new run/thread and staling the old request. Reuse only
identical verified intake/extraction. One registered reassessment uses nineteen
nodes total; never reset budget or accept changed/unknown documents. Preview
remains isolated. Conditional editing, other source cases, general uploads, Live
and RAGAS/hybrid execution remain pending. Notebook/HTML now exist; notebook kernel
is unverified without optional IPython/Jupyter. No new dependency/provider enabled.
This supersedes older pending claims for this bounded financial workflow only.

**Policy-display audit fix â€” POLICY-VIEW-1.0:** command_center.policy_display
projects the selected scoped run's recorded final_policy into Workspace cards,
counts and a copied evidence dictionary. Before synthesis, show the recorded panel
as preliminary. Do not overwrite pre-synthesis inputs/artifacts or regenerate old
memos to fix presentation. Validate run/input/dependency binding; unavailable
verified sources yield no citation buttons. Preserve distinct policy outcomes and
workflow controls (NOT_TRIGGERED is not human approval). Larger financial HITL,
fulfilment and additional-case gaps remain pending; do not report them fixed by
this display correction.

**Authorized UI V2 (2026-10-24):** Follow docs/design/redesign-v2.md and the user's
supplied six-screen design for P0 presentation. ui/command_center.py and
ui/presentation.py reuse existing financial services. .streamlit/config.toml owns
the local light theme; no remote fonts/assets or new framework. Group runs by deal,
retain selected run, separate human decisions from execution, and link finding
references to exact recorded sources. Financial human actions and arbitrary uploads
remain disabled until backend integration. Never seed fake history/owners/metrics
to decorate the UI. Keep screenshots ignored and report actual UI/browser checks.

**Current normal-path integration (2026-10-24): APP-READ-1.0 adds root app.py and ui/command_center.py with six destinations over actual E-N01 financial records. command_center.py enforces scope and Analyst start permission using existing worker admission. Citations require recorded dependency/input digests; uncertain claims override stale RUNNING. New events have UTC timestamps; legacy times remain absent. Illustrative role-action/history preview stays isolated. Financial interrupt/resume, evidence fulfilment, Conditional review, other cases, notebook/HTML and Live remain pending. This supersedes earlier full-shell-pending notes for the bounded normal path only.**

**Decision History addition â€” 2026-10-24:** User explicitly authorized a sixth Decision History page and CSV/PDF audit export, superseding the older five-screen/no-P0-export restrictions for SPEC-013 only. Follow docs/specs/decision-history.md. Use one SQLite database and shared scope guards; all five simulated roles may view/export only their allowed deals. Preserve final-review permissions. Capture original event-time status/context snapshots; never use latest analysis to fill historical gaps or fabricate lifecycle events. CSV is the implemented export format; PDF remains deferred. Implement the current illustrative preview page without pretending it is connected to real financial/HITL records. Full app/financial timeline integration remains pending; no new inference, dependency, schema migration, account system or external publication.

**Authorized Human review UI â€” 2026-10-24:** The user requested role-aware comments, Approve/Reject/Request Additional Information (Pending), and reviewer/status/timestamp history. Follow SPEC-008 REVIEW-UI-1.0. review_actions.py may persist only ILLUSTRATIVE_UI_ONLY records in existing app_records/history; ui/human_review.py and tools/preview_human_review.py are reusable component/local preview, not the whole app. Preserve the core capability matrix, mandatory prerequisites/tier checks and original AI outputs. All submitted actions require comments; information requests remain pending/blocking without a new PanelDecision label or generic clearance. Preview actions never consume real financial requests, create HUMAN_SUPPORTED, dispatch a graph or complete a report. Do not silently seed samples on import/read or alter existing normal records. Record actual tests honestly; financial interrupt/resume wiring, Conditional support/editor, full UI and Live remain pending.

**Authorized quality improvements â€” 2026-10-24:** Follow [QUALITY-REVIEW-1.0](docs/evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10). Add full-source BASELINE extraction preparation, field-level value/basis/reference diagnostics, narrative source-review packets and exact original-response retention through the explicit offline capture CLI. This is read-only deal analysis/evaluation preparation, not Live activation, model-quality evidence, a provider response contract or human support. Preserve original prompts/registrations, two generation stages, all caps, disabled provider/evaluator flags and the sequential graph. Paid/provider/tokenizer, additional case, HITL/UI and optional RAGAS prerequisites remain separate.

**Authorized normal Fixture slice â€” 2026-10-23:** [E-N01-SYNTHESIS-1.0](docs/specs/synthesis-evidence.md#authorized-e-n01-normal-slice--e-n01-synthesis-10) binds the current synthesis request, exact educational stage response and four narrative evidence targets. The normal nine-stage LangGraph/SQLite path, primitive panel handoffs and pure seven-section memo are now implemented; scoped executed checks are recorded in execution.md after verification. Only E-N01/default is supported. Other cases, actual human-review interrupts/corrections, full UI/notebook/HTML and Live remain pending. Fixture expectation checking is not HUMAN_SUPPORTED or a real model-quality result; provider calls remain disabled. Earlier partial/no-graph status notes describe their historical slices.

Generation comparison authorized2026-10-23: follow [GEN-COMPARE-1.0](docs/evaluation/generation-model-comparison.md). Qwen/Qwen3-30B-A3B-Instruct-2507 is the baseline candidate; nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B is the challenger. Prepare identical registered synthetic inputs and local response checks; no automatic application switch, new judge or paid run. The explicit offline preparation CLI reads no secrets and creates no client/database/network operation. E-N01 extraction packet preparation is separate from verified provider token fit; missing/conflict/Reject packs remain unready; both E-N01 task packets are prepared offline, with Live token fit unverified. All real model quality/cost/latency measurements stay null until authorized provider execution. Preserve existing Runtime prompts, source registration, embedding selection, execution admission and allowance gates.

**Current embedding decision â€” 2026-10-23:** [ADR-008](docs/architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Document status: Active for approved M1/M2 and scoped normal M3 Fixture implementation, 2026-10-24
Location: repository-root AGENTS.md
Activation: User instructed applying the reviewed recommendations and moving to next steps after the concrete M1 approval request. This authorizes M1 scaffolding, dependency resolution and offline checks. Later paid/provider/parser/publication gates remain unchanged. Historical draft-only statements below apply to the documentation copy; this root copy is active for M1.
Source proposal: docs/architecture/repository-design.md

## Project purpose and source of truth

Build a local educational financial-deal review demonstration over synthetic USD term-loan documents. The tagline is â€œEvery deal has a story. Our agents find the plot holes.â€ This is not real lending, legal/compliance certification, screening, investment advice, a payment/trading system or production banking software.

Read the current user request and approved documents before changing behavior:
- docs/product/prd.md â€” required product outcomes and boundaries.
- docs/architecture/hld.md and docs/architecture/decisions/ â€” architecture.
- docs/specs/overview.md and the relevant SPEC-001â€“013 file â€” exact contracts, accepted P3 decisions and authorized Decision History extension.
- docs/agents/shared-contract.md and only the relevant specialist file â€” role/calculation/policy behavior.
- docs/evaluation/evaluation-plan.md and docs/traceability.md â€” quality definitions, case split and planned checks.
- docs/execution.md and docs/design/design-system.md â€” milestone/design rules once approved.

Existing user authorization persists. Follow the approved phase sequence and the current milestone; do not ask again for routine implementation choices already authorized. If a material spec conflict or unapproved business rule blocks work, identify the affected requirement/decision and propose a concrete edit for review. Never silently choose an archived or more convenient rule.

Phase 3 was accepted on 2026-10-22. Repository approval does not automatically approve Phase 5's first implementation milestone, paid inference, publication, external deployment or a project license. Check recorded approvals rather than inferring them from installed tools or a present key.

## Architecture and navigation

Accepted public-reference architecture2026-10-23: the user instructed updating the pending crawler/embedding/storage choices and aligning all documents. Read docs/specs/public-financial-sources.md and accepted ADR-007. Local-file intake (Crawl4AI inactive), Nebius-hosted embeddings under ADR-008, and app-owned SQLite vectors with bounded exact cosine search are approved selections. The exact SEC credit-agreement URL is selected. Do not request these architecture/source approvals again. Package/browser/model/tokenizer revisions, licenses, Windows compatibility, additive schema-change safety, network limits and any required identifying contact still need actual verification. The architecture-approval turn changed documentation only; the latest implementation record below supersedes that historical execution status. Public references remain a separate REFERENCE_CORPUS, never E-N01 fixtures, lending policy or Live HUMAN_SUPPORTED. No paid Firecrawl/hosted vector service, deployment, automatic download or automatic runtime strategy switch follows.

One source-checkout Python app: app.py remains the planned full Streamlit shell; tools/preview_human_review.py currently exposes Human review and Decision History. src/deal_or_no_deal_ai contains shared contracts/domain/services; ui/ contains reusable components, with full six-screen integration pending. config/ contains trusted nonsecret versions/policies; docs/agents is the sole role-instruction source. fixtures/development and fixtures/held_out contain reviewed synthetic inputs/model-stage fixture responses/gold labels. tests/ contains application tests; notebooks/ and prototype/ remain planned shared-graph/HTML destinations; var/ is ignored local state/output.

Use one LangGraph definition with explicit typed state and one user-started execution worker. Services enforce persona, scope, revision, idempotency and gates. Keep SQL and checkpointer ownership separate in the same SQLite file. Do not introduce a REST server, second database, ORM/migration framework, queue, distributed agents, vector service, voice SDK or external app connector without a justified approved change.

Node mapping:
- Agent 1: Extractor, first normal model task.
- Agent 2: Compliance, deterministic sample-policy checks.
- Agent 3: Risk & Summary, composed of Python Risk Quantifier plus Synthesizer, second normal model task.
- Supporting specialists: Financial Analyst, Evidence Reviewer, Memo/Report Generator.
- Orchestrator: deterministic delegation, joins, routing, budget and failure guards.
- Intake and Human Review are control responsibilities.

Keep all seven specialist outputs inspectable. Named specialist files/nodes do not justify extra LLM calls.

## Coding and change conventions

Latest public-reference progress2026-10-23: the user supplied a different47-page local PDF, and actual LOCAL_FILE inspection succeeded. The original Downloads source is unchanged, retained artifacts stay ignored, and source instructions remain data. LOCAL-REFERENCE-1.1 fixes source leakage: corpus_id=null, declared_source={}, configured company/URL only under expected_profile_source, origin UNBOUND_LOCAL_UPLOAD, scope NO_CORPUS_ADMISSION and support UNVERIFIED. Never label this upload as the earlier configured company or auto-admit it based on matching words.96 combined methods pass. Earlier95-method setup and package/build evidence is retained; no new dependency or model-prompt hash. No BGE weights, embedding/index, retrieval comparison, credit score or full loan workflow is complete. Actual source/review evidence is in execution.md; prior no-user-file notes describe earlier slices.

Latest authorization: after the explicit next-step/A1-A4 request the user said â€œok move with next steps.â€ Resume development and record A1-A4 as user-approved educational E-N01 assumptions. Implement CASE-REG-1.0 exact source/assessment/default-stage binding and trusted deterministic finance/policy/risk slice; no repeat permission request for these assumptions. Keep draft/history files and original external PDFs unchanged. No generic Six Flags ingestion, Live HUMAN_SUPPORTED, paid call, production claim or new financial rule follows. Existing parser/provider/publication and later readiness boundaries retain their scoped evidence requirements.

Parser authorization2026-10-23 is fulfilled: pypdf6.21.2 is installed/locked and all five E-N01 pages pass known-corpus checks. User subsequently approved A1-A4 by requesting the presented next steps. config/registrations/e-n01.json now binds the source/assessment/default-extraction slice; do not request these same approvals again. Generic upload, other cases/variants, Live fact support, paid calls and full graph/readiness remain separate work.

M2 current scope: services.py loads only the exact approved E-N01 FIXTURE/default, verifies source/profile/schema output hashes and parsed pages, qualifies scope/period/units/authority, then wraps finance.py and pure policy.py/risk.py. tools/run_e_n01_panels.py executes this deterministic slice;85 application methods pass. Authoring snapshots deliberately retain draft flags; current permission comes from the separate trusted CASE-REG-1.0 record. Parse-only verification does not resolve registration and reports approval/registration unknown. Retain history/1-draft and all earlier evidence. No full graph, synthesis, final readiness, Live HUMAN_SUPPORTED or generic real-document processing is implemented by this slice.

Use Python 3.12 only after the approved interpreter/dependency check. Use uv and the committed lockfile rather than unrelated package managers or untracked ad hoc installations. Dependency versions and project-specific CLI commands must match the actual manifest/implementation, not guessed APIs. Use the minimal approved dependency set; document any requested addition and its purpose/license implications.

Make small changes tied to a SPEC/FR and planned TEST ID. Keep graph nodes thin and domain functions independently testable. No speculative framework, duplicate financial engine or parallel infrastructure. Start with ordinary modules; split only for demonstrated size/responsibility reasons. Preserve archives and unrelated user changes.

Pydantic trust boundaries reject extra properties, nonfinite numbers and Boolean/numeric coercion where prohibited. Decimal values serialize canonically. Use FIN-1.0, approved periods/bases, precision/display settings and exact threshold comparisons; never derive missing financial inputs from assumptions. Missing is not zero. Concentration remains Not assessed; no PD or unapproved score. RISK-EDU-1.0 is the sole educational aggregation: five supplied synthetic assessments weighted30/20/20/20/10%, Decimal contributions/total, no reweighting. Missing material factors/inputs yield Insufficient Data with null total/band and pause dependent synthesis/readiness. SCORE-BANDS-1.0 classifies unrounded totals before display. SCORE-ROUTING-1.0 requires Moderate normal human underwriting, High Credit Risk Manager handling then package review, Very High senior-tier Approver review; preserve independent gates and five personas. Compute in the existing Python risk node. Supply a bounded supported score/band/driver projection to the existing Synthesizer call; optional proposed_action belongs outside exact five-field PanelDecision and never authorizes an action. Three read-only assessment cards separate score, policy exceptions and missing evidence; factor coverage is explanation only. Never infer ratings, invent bands, add credit-data APIs or turn41 Moderate into41% PD/approval. Preserve source/configuration/revision lineage and invalidate dependent review on corrections. TEST-004-10/11 and existing UI/HITL tests cover deterministic arithmetic/control/display, not predictive calibration. Viewing performs zero scoring/inference.

Use SAMPLE-LOAN-POLICY-1.0. SYN-ESC-003 is retired and its historical ID reserved. Requested amount >=USD10M OR validated confidence <0.7 OR active score referral OR other mandatory referral controls Python routing. Score referrals are separately versioned DEMO_PRODUCT_CONTROL records, excluded from policy-exception counts. Confidence is uncalibrated; model recommendations cannot waive a gate. Apply P3-01 status aggregation without discarding issue scope/history.

Implement RULEVIEW-1.0 as the policy handler's recorded condition trace plus a scoped read projection into existing UI details. Show exact versioned predicate/applicability/operands/calculation/source and distinct result/workflow consequence, including compound grouping and unevaluated/Unknown/Not applicable/stale states. View rule evaluation performs no financial/policy recomputation, graph/tool/model call or mutation. Never add a UI-side evaluator, editable rule DSL, generic validation stamp or imported screenshot thresholds/integrations. Trace/version mismatch must remain explicitly unverifiable; correction and permitted support/disposition actions stay separate. Preserve source/rule reference navigation in the static HTML using labeled snapshot data.

Apply P3-02 and SPEC-008 capabilities in services and UI. Acknowledge, record a supported sample exception, record High-score credit-risk handling, apply an allowlisted synthetic control fixture, and record final package disposition are different actions. NORMAL cannot satisfy SENIOR review tier; generic Approve cannot clear missing sources or specialty/integrity blocks. Administrator has no automatic financial/compliance approval authority. Preserve original PanelDecision separately from HumanDisposition.

Follow the authorized SME fixes in SPEC-001/002/003/007/008/009: complete walkthroughs use registered reviewed source/assessment/subject packs; unregistered Live uploads are partial with no borrowed scores/PanelDecision. Match borrower/entity/facility and basis before trusted use. Critical Live facts require current source-backed FACT-SUPPORT-1.0 through typed FACT/CLAIM support targets; KNOWN and a resolving citation do not imply HUMAN_SUPPORTED. Support Save invokes no graph/model or fact edit; explicit same-revision continuation uses the same ledger at the earliest affected stage, never extraction replay or stale review tokens. Conditions retain provenance/category/owner/status and existing-issue-derived blocking; outstanding proposals cannot waive current evidence or imply fulfillment/funding. Covenants are extracted, not automatically evaluated; annual-period analysis does not establish full-term/balloon/refinancing adequacy. Reported/adjusted-EBITDA normalization/reconciliation is deferred; keep the eighteen-field wire and FIN-1.0. No extra agent/node/call/database/screen or expiry policy is introduced. Reuse existing focused tests and source-case variants; report document checks separately from runtime evidence.

Fact/source/control corrections create analytical revisions, invalidate affected results and stale acceptance, and rerun only approved dependencies in a new run/thread with the same review_id and cumulative allowance. Do not resume stale interrupts with changed analytical data; only review-only handling uses the same pending thread. Notes/ownership/conditions-only human handling do not silently rerun unchanged model work.

Follow [UX-1.0](docs/specs/command-center-ui.md#simplicity-attention-and-interaction-contract--ux-10): keep five screens, a five-column default Dashboard, three-step intake, Workspace-first issue/owner/action with every mandatory blocker, paired evidence and progressive technical detail. Preserve separate recommendation/review/report labels and seven report sections. Use the existing service-derived action availability; no new permission/policy engine. Read-only correction impact and Save spend no model work: Save prepares READY state and invalidates dependent output, then an explicit permitted continuation queues work. Preserve focus, selected finding and readable field/status errors. Core usability follows UX-T01â€“05 with honest self-assessment; offline QA/benchmark results remain outside the UI. Detailed visual tokens/components belong to the approved Phase5 design-system work, not speculative new dependencies.

No key/provider client/database mutation during import, graph construction, screen reads, source inspection or notebook diagram rendering. Network I/O occurs only inside explicitly invoked, scoped adapters: authorized lazy Nebius inference, the accepted bounded public-source crawler, or separately initiated verified dependency/browser/model setup. Import, refresh, source inspection and notebook rendering never trigger those operations; page/model text cannot initiate them. The one worker invokes plain services, never Streamlit UI functions. Refresh must reuse persisted run/service identities.

## Context, inference and budget controls

The user authorized applying DOCVERIFY-1.0 checks on2026-10-23. Use the bounded parser-independent documents.py helpers and same-input offline comparison. BASELINE keeps every mandatory safeguard; ADAPTIVE remains opt-in and restores only accepted scoped blocks. Do not treat supplied geometry/fidelity flags or passing synthetic block tests as actual PDF/model verification, adopt a parser, activate retrieval or add a model call. Future pipeline wiring must retain full request/token preflight and human source support.

Retrieval implementation order: after reviewed synthetic sources and frozen query annotations are ready, implement and report DIRECT, KEYWORD, VECTOR and HYBRID first. VECTOR-only is the semantic retrieval baseline; DIRECT is the coverage baseline; RRF is rank fusion. Consider a separate reranker only after measured candidate-ranking failures demonstrate a useful quality versus added-processing trade-off. Follow the [canonical sequence, capability status and report decision](docs/evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). Keep specified/implemented/tested/measured states distinct. M1 foundation tests and installed transitive packages are not implemented or measured retrieval. No automatic model download, new runtime call or app-strategy switch is authorized.

Only Extractor and Synthesizer normally invoke models. Read allowlisted Runtime prompt sections plus shared Model context rules, relevant evidence and schema. Do not load all role/spec files, evaluator answers, unrelated deals, audit logs or full chat transcripts into every request.

Use compact typed wire responses, shared source/basis dictionaries, faithful evidence packets, safe exact deduplication and version-aware same-deal result reuse. Expand trusted metadata locally. Do not drop material covenants/conflicts/footnotes to fit a context limit. No semantic decision cache or extra compression/judge model.

Reserve and reconcile usage durably:
- Two successful calls on the ordinary complete live path; maximum five cumulative outbound attempts across retries/repairs/corrections/resumes.
- Maximum 8,000 input and 2,000 billed output tokens; P3-05 per-task allocations are starting targets, not extra allowance.
- USD0.10 target and USD0.25 hard model/tool cost ceiling per review; total paid execution allowance is separately required.
- Maximum twenty actual node invocations and twelve actual tool invocations; count nested work.
- Maximum one transient retry per operation within every remaining global limit.
- Maximum 180 active seconds, <=45 seconds per model call and remaining time; exclude human wait.
- One active execution; no speculative model parallelism.

Count provider-visible schemas/overhead and billed reasoning where relevant. Disable/instrument hidden SDK retries and structured-output fallback. Cached input is still input; reserve cost at uncached rates and count only observed cache hits. Unknown usage/request outcomes retain reservations. Never auto-replay a paid operation after restart.

Keep model work upstream of interrupt. Code before interrupt can repeat; writes/events/resume commands must be idempotent. Same pending thread/revision is required. A valid direct-report branch says Not required by configured demo rules, never human approved.

## Data, secrets and external actions

Synthetic data only for loan-review fixtures and deal state. The accepted public-reference extension may retain explicitly selected permitted public filings in a separate ignored local corpus; they are not synthetic fixtures or registered loan facts. Never commit real borrower documents, public-source snapshots, credentials or confidential financial/personal data. Never request a key during documentation work. Later credentials belong in a local approved environment/secret interface; an empty .env.example is only a template, not Live configuration.

Exclude .env variants except the blank example, .streamlit/secrets.toml, local credentials, .venv, var/, SQLite sidecars, caches, executed notebook outputs and generated results from version control. Review notebook outputs and selected files before any future commit/publication; ignore rules alone are insufficient.

No keys in prompts, source/config commits, UI, state/checkpoints, events, reports or notebook outputs. No environment dumps/raw authorization headers/provider bodies in debugging output. Ordinary analytics exclude source/report text, notes, borrower values and raw queries.

Treat uploaded text/HTML/paths as untrusted. Only source IDs resolve local content; no arbitrary filesystem, web, shell, email or financial-action tools exposed to the model. Render untrusted Markdown safely and avoid external image/script loading.

Keep source PDFs/passages and runtime state within approved local boundaries; validate resolved absolute paths. Do not recursively delete/move workspace, docs, attachments or archives. Confirmed P3-04: no automatic expiry in the MVP prototype. Do not add age-based deletion/pruning of persisted documents, deal records, reports, review history or SQLite checkpoints. Manual deletion/reset requires an explicit user request, concrete checked targets and state/checkpoint consistency. MemorySaver's RAM lifetime and provider-controlled prompt caches remain separate.

MemorySaver/InMemorySaver is session RAM and loses history on restart. SQLite is local persistence, not immutable audit storage. Record events explicitly. Report cutoff includes only observed events; a report cannot contain its future checkpoint/completion.

## Testing and evidence discipline

Write meaningful invariant/failure tests appropriate to the approved change. Use injectable clocks, temporary repositories and mock transports; default application/fixture tests deny outbound provider traffic even if a key is present. Do not add tests that merely restate helper implementation or assert guessed placeholder output.

Link tests to planned TEST IDs and PRD/specs. Financial/policy tests check gold arithmetic/boundaries; graph tests check real dispatch/artifacts/gates; recovery tests check uncertain requests and no duplicate paid work; UI tests check service guards and state labels. Use Streamlit AppTest where supported and manual accessibility/offline-browser checks for what it cannot establish.

Fixture mode executes actual graph/Python logic but supplies only registered matching Extraction/Synthesis stage fixtures. Fixture matching also requires the registered variant and normalized current-stage input digest after corrections. An arbitrary uploaded document or unmatched edit cannot receive a canned success. Failed Live requests never silently switch to Fixture or another provider.

Application tests are not model evaluations. Keep eighteen development and twelve held-out scenarios separate; do not tune prompts on held-out answers or include gold labels in model context. Report author exposure/limited blindness. Actual model accuracy/support/risk recall requires the separately funded evaluation protocol and honest failure denominators.

Plan RET-1.0 from the first context implementation: ordinary Python evidence-selection protocol, injected DIRECT adapter and unchanged ContextPacket for graph/agent consumers. Optional BM25/vector/RRF adapters are confined to retrieval_benchmark.py and the offline evaluation entry point. The app remains DIRECT; no model/index creation or downloads at import/startup/Fixture/notebook time. Do not use top-k search for complete extraction or let reference retrieval override executable policies. Benchmark adapters return the same scoped source-backed result, with no query-rewriting/generation call or automatic provider fallback. Record actual local comparison evidence as EXECUTED_RETRIEVAL_BENCHMARK; fake vectors test contracts only. Follow [the benchmark protocol](docs/evaluation/hybrid-retrieval-benchmark.md); later backend implementation/configuration still needs its scoped tests and approved dependency setup, even though graph/agent code stays isolated.

Report exact commands, scope, pass/fail/not-run, failures and limitations. Distinguish DOCUMENT_REVIEW, APPLICATION_TEST, EXECUTED_FIXTURE, EXECUTED_LIVE and ILLUSTRATIVE. A static link check is not an application test. A fixture run is not live model quality or provider latency evidence. One live smoke test is not p95 validation. Never claim tests or integrations ran when they did not.

## Commands and milestone availability

M1 setup, foundation tests and local build are authorized. On2026-10-23 the user explicitly permitted retrying installation: uv sync succeeded, .venv/uv.lock exist, all43 foundation tests passed and local packaging succeeded. The previous installation rejection is historical, not a current blocker. The optional langsmith_plugin pytest integration is disabled; application imports must not initialize hosted services, even when tracing flags exist. Other commands below remain future milestones until their files and approvals exist. The stdlib-only runner is a subset, not the full required suite. Provider spending remains separate.

| Purpose | Proposed command |
|---|---|
| Foundation setup | uv sync --python 3.12 --group dev |
| Local application | uv run streamlit run app.py --server.address 127.0.0.1 |
| Unit/integration checks | uv run --frozen --python 3.12 pytest tests/unit tests/integration |
| UI/presentation checks | uv run pytest tests/ui tests/presentation |
| Development fixture suite | uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split development --output-dir var/evaluations |
| Full fixture suite | uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split all --output-dir var/evaluations |
| Notebook setup | uv sync --group dev --group notebook |
| Local notebook UI | uv run --group notebook jupyter lab --no-browser --ip 127.0.0.1 |
| Graph-only executed copy | uv run --group notebook jupyter nbconvert --execute --to notebook --output-dir var/notebooks notebooks/01_workflow.ipynb |
| Offline presentation artifact | uv run python -m deal_or_no_deal_ai.presentation --run-id RUN_ID_FROM_ACTIVITY --output-dir var/presentation |
| Local package build | uv build --python 3.12 --no-sources |

RUN_ID_FROM_ACTIVITY is a placeholder for a real executed fixture run. No npm/frontend build is needed. A Python wheel alone is not a self-contained deployed app: prompts/config/fixtures are resolved from the reviewed checkout. Do not publish built artifacts or launch external hosting.

Do not run unavailable suites or quietly skip required checks to report success. After initial setup/lock generation, use the committed lockfile; investigate unexpected dependency changes before accepting them. Do not invent a Live command or run a funded benchmark through normal test discovery.

## Human approval boundaries

Continue autonomously within an approved milestone. Approval is required for a changed business formula/threshold/capability/status rule, material source-of-truth conflict, new provider/model or increased allowance, paid/external service activation, project-license choice, external repository/publication/deployment, destructive reset or new sensitive-data handling. Do not repeatedly ask about an action already explicitly authorized in the session.

ADR-006 records explicit user approval of pypdf under BSD-3-Clause terms and the tested6.21.2 profile. That fulfills the installation/license checkpoint for this selected dependency, not general parser fidelity, case approval or the project's license. PyMuPDF is not selected/installed; its AGPL/commercial choice is not authorized. Other dependency/provider/license changes retain approval gates; educational purpose alone does not settle license suitability.

Before requesting a new decision, finish the authorized reversible work needed to make it concrete and reviewable. State the exact spec/approval condition and practical impact. Do not use a request for permission to leave already authorized work incomplete.

## Definition of completion and reporting

Complete only the approved milestone and its required checks. Explain what changed, linked requirements, actual validation and remaining risks. Report incomplete provider/model/license/dependency decisions explicitly. A screenshot, static graph or prewritten report does not substitute for the working delegated pipeline.

Final educational-demo acceptance requires three core fixture walkthroughs plus E-N01 source-backed correction and E-F03 supported Reject QA variants, the agreed critical application/evaluation checks, shared offline Jupyter graph, clickable HTML walkthrough, actual generated source-linked sample report and later validated Nebius integration with proper usage/evidence. No claim of production readiness, bank compliance or measured business savings follows from this prototype.

## Authorized review-fix instructions

Follow the subsequent Principal fixes in their canonical feature contracts: exact DealTermsWire-only Extractor Runtime prompt (SPEC-002/agents/extractor); REVIEW-BASIS-1.0 and pre-disposition condition drafts (SPEC-008); cross-entry-point EXEC-ADMISSION-1.0 (SPEC-007); and exact STATE-CODEC-1.0 (SPEC-011). Do not copy the full development contracts into a provider prompt. Compare the actual loaded prompt/schema/examples and expected instruction hashes; never allow notes/domain metadata or Unknown strings in place of declared wire fields. Do not mistake valid specialist review progress for changed loan analysis or regenerate unsupported condition targets after accepting the disposition. All execution entry points sharing the local database use the same durable admission claim, not just a per-process lock. Preserve exact checkpoint numbers/types/fingerprints and null-clearing semantics, with no pickle fallback or automatic recovery/migration. Extend the existing first-milestone compatibility/regression families and report actual evidence honestly. These are approved specification fixes, not activation of this draft or approval to scaffold/run paid services.

The user's later RAGAS-EVAL-1.0 request supersedes blanket no-judge wording ONLY for the explicit offline evaluator. Implement the optional lazy dependency/config/custom metric adapter at its approved milestone, with one shared five-dimension1â€“5 bundle, exact examples, separate native metrics and separately approved evaluator allowance. Verify pinned APIs/Nebius/model/token/rate/call behavior; never use a library default OpenAI client or silently invoke a scorer on import, Fixture tests, app refresh, report rendering or graph-only notebook. The application loader retains two prompts; the offline loader alone reads docs/agents/ragas-evaluator.md. Preserve exact original context versus evaluator-reference separation, original-output cutoff, failed denominators and read-only deal-state isolation. No score grants authority/support/approval. Actual RAGAS execution is labeled only when the installed package/adapter ran; no package or evaluator request has run during this documentation task.

Apply the user-authorized Director fixes in existing modules: NARRATIVE-CHECK-1.0 registers targets for all observations/rationale/conditions/action explanations; INPUT-EDU-1.0 rejects nested/escaped duplicate keys and out-of-profile JSON/numbers before hydration, preserving original values and exact routing confidence; SOURCE-TRIAGE-1.0 uses existing owners/services with no new clearance powers; CONTINUE-CHECK-1.0 uses a small path-count table and actual shared ledger, with no double-charged estimates or hidden node merging. Reference checked does not prove semantic truth; support and credit disposition stay separate. Preserve technical-versus-lending-error distinction, node-versus-model-cost distinction, budgets and history. After the relevant gates, prioritize one actual E-N01 fixture slice and expand to the agreed core cases; do not require optional benchmarks or introduce another framework. This root copy is active for M1; later milestone permissions remain scoped.

Apply SPEC-006 SOURCEFIT-1.0 to source applicability: exact deal/subject/period/value type/qualifiers, explicit review date/evidence cutoff and reviewed field-specific authority/supersession. Preserve verified historical capture separately from ingestion and never infer effective/available dates from a filename. Missing material metadata/profile means Unknown or configuration/information pause; newest upload/retrieval rank does not grant authority. No universal hierarchy, recency duration or source-expiry rule is approved. Retain history and no automatic expiry, preserve original conflicts, include date/profile in dependency identity and use existing revision/continue controls. Source-profile configuration requires actual reviewed evidence; no extra LLM/crawler/database or retail-Q&A scope. Apply these instructions within the approved milestone.

Follow the authorized AE-01â€“07 contract refinements: compact SYN-WIRE-1.0 and Python-owned authority; CANON-1.0 exact scoped fixture/dependency identities; COVERAGE-1.0 original-span/multi-page evidence; PROVIDER-1.0 outcome/usage normalization; RESUME-1.0 and RUN-OUTCOME-1.0 receipt/pause/completion handling; STATE-UPDATE-1.0 explicit stale-current clearing; EVAL-CUTOFF-1.0 original model versus reviewed workflow evaluation. Implement in the existing proposed modules after their gate; do not introduce seven new subsystems. Use the existing planned tests and preserve all budgets/history/no-expiry boundaries. No raw graph state streaming is authorized as a substitute for safe event projections.

Before dependent implementation, perform the bounded contract/context-size, dependency and SQLite interrupt/resume compatibility checks in the approved first milestone. Resolve parser licensing before installation; verify selected Nebius model schema/token/rate behavior before authorized Live work. No budget increase, schema weakening or hidden inference is allowed to fit the prototype.

Use updated P3-05 targets and protect one synthesis correction's1,500 input/350 output tokens before optional repairs. A normal path plus that rerun is6,000 input/1,700 output, within aggregate8,000/2,000 ceilings; actual feasibility remains to be measured.

Keep a high-level false-positive count beside recall in offline QA results; do not add excessive-risk-flagging indicators, a new UI workflow or an extra LLM judge. Preserve case-specific supported Reject separately from missing-information/technical stop, with original recommendation and human disposition distinct. The thirty-case/full held-out/timing/batch/multi-person protocols are optional extensions. Core usability uses one operator's five tasks with honest self-assessment. This root copy is active for M1; its source documentation draft remains inactive.

