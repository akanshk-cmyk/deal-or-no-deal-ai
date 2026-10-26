# Deal or No Deal AI — Execution and Measurement Plan

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

Human-action extension implemented: [contract](specs/uploaded-human-decisions.md)
and [functional evidence](evaluation/uploaded-human-decisions-results.md).
No paid validation or mutation of actual demo decisions is required.

New Deal → Upload New Deal now supports the complete unchanged three-PDF Standard Deal package. Explicit Run performs fresh Nebius extraction and synthesis on retained uploaded content, with a distinct upload-derived Deal ID, source map, shared workspace/activity/history and draft memo. It does not use saved answers as live results. Other, partial or changed packages remain inspection-only. Approval readiness and unverified-draft safeguards remain; historical human-checkpoint reviews are unchanged. See [scope, steps and evidence](specs/upload-live-demo.md). This supersedes older blanket inspection-only statements only for that exact supported profile.


## Approved Phase 1 demo update — 2026-10-25

The user approved the [live demo-draft contract](specs/phase1-live-demo.md). New explicit Run actions use LIVE / DEMO_DRAFT. Extraction and synthesis call Nebius; Python performs calculations, sample policy checks, illustrative scoring, readiness and draft assembly. Technical integrity checks do not record human verification. Drafts cannot authorize credit approval. Existing HUMAN_REQUIRED reviews retain their checkpoints and original records. Saved examples remain available internally. No model calls on screen viewing and no fallback on failure. Phase 2 RAGAS/judge evaluation and optimization are deferred. This update supersedes older default-FIXTURE and pre-draft human-checkpoint statements only for new demo drafts. Functional evidence is recorded in docs/evaluation/phase1-demo-results.md (relative to repository root).


Documentation authority: requirements and approved feature contracts describe
intended behavior; [current implementation status](implementation-status.md)
records observed completion. Dated implementation/setup/test paragraphs below
are historical evidence for their stated milestone, not current missing-work
claims. See [documentation alignment](evaluation/documentation-alignment.md) for the cross-document review.

## Unified review experience - 2026-10-25

The saved-response UI is the shared baseline. Use one Run AI Deal Review action;
there is no user-facing mode selector. Existing config/app.toml mode selects new
FIXTURE (default, no calls) or LIVE (explicit paid Nebius execution). Both sources
share the six screens and per-deal history. Historical source controls display
and resume; live human verification and all backend rules remain unchanged.
See [the unified review contract](specs/unified-review-experience.md). Earlier sidebar mode instructions
are superseded. This UI change does not authorize a new paid test.

## READINESS-1.0 current update - 2026-10-24

Finish READINESS-1.0 before paid live testing: deterministic schema and route integration; versioned persistence; backend direct/resume guards; shared four-screen presentation; offline regressions and full suite. Existing successful premature-approval tests must assert blocked approval or use explicitly satisfied synthetic prerequisites. Keep original E-N01 sources and saved response untouched. No SEC or model calls during this milestone. Results: evaluation/approval-readiness-results.md.


## LIVE-GRAPH-1.0 implementation update - 2026-10-24

User authorized completing the live graph and evidence checkpoints. Follow
[the live graph contract](specs/live-graph-integration.md). The shared build_graph now has an explicit
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
and evaluation. See [live integration specification](specs/live-synthetic-integration.md)
and [approved fit profile](evaluation/live-fit-proposal.md).

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


**Current embedding decision — 2026-10-23:** [ADR-008](architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.26
Date: 2026-10-24
Status: Registered saved cases/correction, upload inspection and candidate DSCR preview implemented; bounded live integration and extraction verified; full live completion and generic uploaded-case financial onboarding pending

## Uploaded financial evidence review — 2026-10-24

Authority: user requested the next implementation step after upload inspection.
Contract: [UPLOAD-FACT-1.0](specs/upload-fact-review.md), based on existing
FACT-SUPPORT-1.0 and FIN-1.0. No new lending rule, provider, dependency or table.

Analyst manually proposes existing annual DSCR inputs: CFADS, principal, interest.
Bind exact retained page/quote/start, raw label/numeric token/unit label, explicit
USD/scale, subject/facility and annual actual/projection dates. Normalize with Decimal;
source match does not certify semantics. RiskManager records exact-current-target
HUMAN_SUPPORTED/UNSUPPORTED/WITHHELD, seven explicit checks and reason. All identities
are simulated. Candidates are REVIEWER_PROVIDED / UPLOAD_CANDIDATE_ONLY and confer
no registered-deal/Live authority. Append versioned scoped events through existing
admission; reconstruct/revalidate originals on reads. Duplicate commands retain
receipts, competing/stale/changed targets fail. New proposal invalidates support.

Only three compatible current supported candidates enable existing CALC-004 annual
DSCR preview. Missing/withheld or differing subject/facility/period/basis blocks it.
Preview does not expose other kernel metrics, infer collateral classification, assess
full-term repayment, clear policy, produce a score or approve a deal. Source origin/
current authority, all other critical facts, full registry and graph admission remain
pending. No model/embedding/evaluator or expiry/reset/deletion.

UI reuses Upload: manual proposal form, support-state table, RiskManager assessment
form and one-click exact candidate source navigation; preserve complete local evidence
history. Native forms submit current inputs atomically. Old sample workflows/Runtime
prompts/registrations and budget limits remain unchanged.

Initial4 integration checks passed in13.01s. An added concurrency/source-change test
initially misplaced remaining assertions from its neighboring test; corrected the
test boundary. Source guard itself correctly rejected the changed bytes. Final:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/upload-facts-final.xml
```

Result: **242 tests and269 subtests passed in211.39s**, zero failures/skips. Five
new integration methods cover exact source/normalization/annual guards, roles,
missing checks, stale/duplicate/concurrent support, replacement invalidation,
incompatible subject/withholding, changed retained source, supported1.50x preview
with no financial runs, and actual Streamlit AppTest proposal→RiskManager support→
citation navigation. No separate real-browser submission run this milestone;
previous upload browser evidence remains at its original scope. No paid calls or
user-data seeding; tests use temporary synthetic workspaces.

## Local uploaded-PDF inspection — 2026-10-24

Authority: user requested the next recommended uploaded-document intake step.
Contract: [UPLOAD-1.0](specs/upload-inspection-integration.md). Connect New Deal/Upload
to bounded synthetic-PDF inspection with existing pypdf and SQLite/admission, no new
dependency/framework/schema or model. Analyst confirms synthetic educational data;
all five simulated roles may read the local workspace upload library, which grants
no registered financial-deal access or authority.

Enforce1–3 PDFs/10 pages/10,000,000 bytes combined; reject invalid names/type/bytes,
duplicate content, corrupt/encrypted/blank/scanned-only pages. Separate short-lived
parser processes share a45-second deadline, with120,000 extracted UTF-8 bytes and
bounded response/record envelopes; no truncation. This is not an OS memory sandbox
or universal table/year-layout guarantee. Preserve exact original page text, SHA256
and locators. Invalid validation writes nothing. Global admission guards raw-byte
retention in scoped ignored var/uploads and metadata in app_records; partial file/
DB gaps become RECOVERY_REQUIRED, no automatic replay/deletion/expiry. Identical
successful operations read retained receipts without reparsing; changed reuse fails.

Upload UI has native form, explicit validation, file/page error attribution, retained
library, source/page citation explorer, inert text and original download. Status:
INSPECTED_NOT_REVIEWED. No score, clearance, verified entity/period/authority, fixture
fallback, model, memo, embedding, token chunking or index. Unregistered financial Run
remains disabled. Source/profile/fact onboarding, provider and E-M01 new-document
continuation are explicitly separate pending work.

Focused checks: **6 tests/10 subtests passed in47.90s**. Final command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/upload-intake-final.xml
```

Result: **237 tests and269 subtests passed in151.17s**, zero failures/skips. New
checks cover retained parsing/citations/reopen/idempotency, no financial records,
roles/workspace, invalid inputs, encryption/blank/corrupt/page/time limits, changed
source and partial-save recovery, plus UI library/error/read-only roles.

Actual headless Edge used a separate ignored synthetic workspace on localhost8526:
uploaded all three E-N01 PDFs, inspected cited text, then downloaded the retained
original and verified SHA256. One upload record, zero financial runs, zero exception
boxes/external requests; root user DB SHA256 unchanged. First browser assertion ran
before the streamed download control appeared; replace immediate count with explicit
wait and verify the actual download. Reopen succeeded, no duplicate upload needed.
Evidence under var/evaluations/upload-browser; this is real browser upload/download
evidence, not live model or parser semantic-fidelity evidence.

## Source-backed extraction correction — 2026-10-24

Authority: user accepted the recommended next correction step. Contract:
[CORRECTION-1.0](specs/source-correction-integration.md), based on the existing
E-N01 correction example. Reuse unchanged source PDFs, approved factor assessments
and documented annual CFADS900000/FY-ASSESS/FIN-P2; no new financial premise.
Separate extraction-miss registration deliberately omits that value and stops the
actual graph after5 nodes, with no complete score, Synthesizer or report.

Analyst Save requires exact supported fact/basis/page/reason, verified source and
current scope/version/basis. In one existing SQLite/admission transaction it retains
the original extraction/event, supersedes parent and creates revision2/new run/thread
READY, retaining review_id/shared ledger and one correction allowance. Save runs no
graph/model. Explicit Update revalidates sources/draft/original event/budget and
starts the existing graph at Financial Analysis. Unchanged intake is reused;
changed extractor is labeled REVIEWER_SOURCE_CORRECTION, never reused/model output.
Seven affected nodes recompute all downstream findings. Corrected synthesis has its
own input/profile registration. Memo independently binds correction fact/source/scope
and retains reviewer/reason/UTC/original missing value/event. History/filter/timeline/
CSV preserve both Save and Update-request events; no fabricated human credit decision.

UI adds Extraction miss sample, original-source citation, required correction form,
READY warning and separate Analyst Update button. Dashboard shows the correct next
role/action; activity separates reused intake and reviewer-applied extraction.
General field/value/new-document edits and completed/interrupted-review correction
remain unsupported. Original E-M01 missing source cannot borrow this repair.
No expiry/reset/deletion, new table/framework/dependency, paid call or deployment.

Initial focused failures caught a missing profile marker and two test assumptions
(source number formatting and PDF subdirectory path). Fixed the profile binding and
tests without weakening guards. Initial2 backend checks passed in4.98s; later5/6
checks passed before correcting the test-only PDF path. Focused correction/financial/
missing-data suite: **19 passed in29.15s**. Final command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/source-correction-final.xml
```

Result: **231 tests and259 subtests passed in101.34s**, zero failures/skips. Six new
methods cover actual Save/no-dispatch→READY→explicit Update→memo, exact value/basis/
page/role/scope, stale/duplicate commands, concurrent Save/Update one revision,
changed source/tampered saved fact no dispatch, original artifacts/shared budget,
correction provenance/history/CSV and actual Streamlit AppTest form/citation flow.
Observed cumulative12 nodes/7 tools/0 provider requests; restored DSCR1.50x.
This is fixture workflow evidence, not live extraction quality, cost/latency or RAGAS.

Refreshed owned Streamlit on127.0.0.1:8523. Real headless Edge read-only smoke
selected Extraction miss and verified its explanation/Run control, zero exception
boxes and zero external requests. No Run click and root user database SHA256
unchanged. Ignored evidence: var/evaluations/source-correction-browser-smoke.py
and source-correction-intake.png. Full correction submission was exercised by
AppTest, not claimed as a separate real-browser submission test.

## Source-backed Conditional review — 2026-10-24

Authority: user requested implementing the recommended E-P01 step. Contract:
[CONDITIONAL-1.0](specs/conditional-integration.md). Register the approved separate
five-page package and score33/DSCR1.15 premises. Reuse the agreement's actual
“Supply annual financial statements” covenant; no invented repayment cure/policy.

Existing reviewed graph/worker/SQLite now supports separate RiskManager
ACCEPT_FOR_CONDITIONAL_REVIEW handling, AuthorizedApprover condition preparation,
RiskManager FINANCIAL_RISK and ComplianceOfficer POLICY_CONTROL support, then
AuthorizedApprover Conditional Approve or Reject. Current record/basis/gate/source,
role/tier and exact draft/evidence are checked. Reconstruct actual persisted events
on reads/resume and independently in memo acceptance. No generic Approve bypass.
Idempotent identical commands retain receipts; changed/stale/concurrent commands
cannot silently replace them. Full snapshots remain in history, bounded receipts
in checkpoints; depth/byte/token/call/node/tool/time/cost ceilings unchanged.

UI adds E-P01 sample, required-role prompts, native atomic forms, evidence links,
separate specialist statuses, conditional final confirmation and history filters.
Final history/CSV retain condition provenance and unchanged original Exception/AI.
The condition stays OUTSTANDING / owner Unassigned / EXTRACTED_NOT_EVALUATED;
report completion is not fulfilment, a DSCR cure or funding permission. No arbitrary
wording/owner edits or new-document continuation.

Validation: initial backend4 passed in10.14s; focused normal/Reject/conditional
services18 passed in34.59s. First isolated UI attempt hit test-only Windows
socketpair import ordering; move the shared fixture import before network guards.
Next attempt caught a formatted-label assertion mismatch; corrected the test.
Actual role-handoff AppTest then passed1 in9.20s, including memo/history/citations.
Final complete offline command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/conditional-review-final.xml
```

Result: **225 tests and259 subtests passed in93.54s**, zero failures/skips. Seven
new checks include source change, wrong role/condition/digest, stale/duplicate,
concurrent preparation, missing support, tampered draft/receipt, information blocks,
conditional and separate human Reject, actual graph and UI. Conditional final run
uses11 nodes,4 tools and0 provider requests; original generation does not rerun.
These are executed fixture checks, not live model/RAGAS/cost/latency evidence.
No dependency, paid service, deployment, expiry/reset/deletion or user-deal seeding.

Refreshed the owned local Streamlit process on127.0.0.1:8523. A real headless
Edge read-only smoke selected E-P01, verified its Run button/explanation and zero
exception boxes/external requests. No Run click: root user database SHA256 stayed
identical. Ignored evidence: var/evaluations/conditional-browser-smoke.py and
conditional-intake.png. Browser smoke is intake availability; full role handoff
was verified by AppTest, not claimed as a separate real-browser submission test.

## Review typing/submission correction — 2026-10-24

User reported inability to type/submit. Read-only inspection found the user's app
had two completed E-N01/default runs and no pending human-review requests. Removed
the misleading disabled comment editor there; explain read-only scope and offer
explicit Prepare a review-required sample navigation. It selects the review variant
without running, writing records or changing role. E-M01 has its own missing-data
explanation; no gate is waived to make a field editable.

Active financial and exception forms now submit current values atomically through
native Streamlit forms. Buttons no longer depend on text-area blur to become enabled.
On-submit validation handles missing action/comments/evidence/items/confirmation
without writes; success displays a saved confirmation. Backend permissions and
receipt/idempotency/financial authority are unchanged.

Updated AppTest workflows to submit form values in one batch, matching real browser
behavior; intermediate reruns intentionally do not commit unsubmitted form fields.
New regressions cover read-only-to-reviewed preparation with byte-identical database,
blank-submit no write and one-batch persisted comment. Focused command-center,
exception and missing-data suites: **24 passed in39.80s**; earlier isolated updated
Approve/Reject UI checks2 passed in9.40s.

Actual local Edge typing test used a separate ignored temporary synthetic workspace
on localhost8525, leaving user database unchanged: typed a comment then clicked
Submit once without prior blur; saved confirmation appeared and zero exception
boxes. A second actual browser check clicked the visible confirmation label,
typed final comments and submitted once; approval reached the generated memo with
zero exception boxes. A direct automated click on the hidden native checkbox input
was intercepted by its styled label; using the visible label succeeded. No paid calls,
new dependencies, policy changes or deployment. User app restarted on localhost8523.

## RiskManager handling and supported Reject — 2026-10-24

Authority: user accepted the recommended RiskManager handling step followed by
E-F03. Contract: specs/exception-reject-integration.md. Existing approved fictional
assessments/cash bridge retained; no new lending policy/rating conversion rule.

Implemented exact E-F03 source/synthesis/rubric registration and reviewed graph.
Annual CFADS−300,000, DSCR−0.50, interest coverage−2.00, EBITDA1,100,000 and
Moderate45/100 remain separate from the case-specific Reject judgment. No model
or source can waive handling. PendingReview adds an unsatisfied numerical-exception
requirement. RiskManager records RECOMMEND_REJECT with exact source/calculation/
policy refs and reason; shared durable admission atomically records event and new
gate version without changing analytical basis, original Exception or AI output.
Reads reconstruct current gate state from actual history. Identical/concurrent
handling is idempotent; stale/wrong-role/wrong-scope/changed-source actions fail.

Before handling both final decisions are blocked; afterward only permitted
AuthorizedApprover Reject can complete this fixture. RiskManager cannot make the
final decision, generic Approve cannot bypass handling, and information requests
still block. Same thread resumes without generation replay. Report independently
checks original findings/accepted handling and human receipts. History/CSV include
both actions and handling/rule/issue/ref/gate fields. UI exposes New Deal sample,
Human Review role handoff, explicit evidence/reason controls and Dashboard next owner.

Context testing caught an over-nested full history snapshot inside the graph's
human artifact. Kept full original snapshot once in history; checkpoint carries a
compact fingerprinted receipt, rechecked against persisted events. Depth12/byte
limits and all budgets remain unchanged. Direct memo test rejects removed handling.

Executed:

```powershell
.\.venv\Scripts\python.exe -B tools/prepare_e_f03_review.py
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/exception-reject-final.xml
```

Observed full regression: **216 passed, 259 subtests passed in70.62s**. Five new
integration tests cover complete supported Reject, roles/scope/refs/source changes,
stale/duplicate/conflicting commands, concurrent identical handling, no generation
replay, original analysis preservation, forged map/information blocking and real
UI handoff→Reject→memo/history. Path: eleven nodes/four tools/zero provider calls.

After final snapshot validation and CSV/UI detail refinements, targeted
test_exception_reject.py + test_financial_review.py + test_command_center.py:
**27 passed in49.41s**. Additional direct missing-receipt memo check:1 passed in3.92s.
After final next-action/unavailable-memo controls, connected UI test:1 passed in6.50s.
Test-suite durations are not model latency or app p95 measurements.

Actual Edge browser: New Deal E-F03 option and explicit Run control visible, zero
exception boxes. Browser did not click Run or seed user records. Existing local
server restarted at localhost8523; mutation tests use temporary synthetic workspaces.
No dependency install, paid inference/embedding/judge, crawl, hosted tracing, external
repository or deployment. Notebook installation remains deferred.

Remaining: E-P01 supported Conditional/editor, missing/new-document continuation,
actual extraction-miss correction, guarded funded Nebius Live, operator usability
and optional retrieval/RAGAS. No general underwriting/production-readiness claim.

## E-M01 missing-data integration — 2026-10-24

Authority: user accepted implementing the recommended immediate E-M01 step.
Contract: [MISSING-DATA-1.0](specs/missing-data-integration.md).

- Explicit tools/register_e_m01.py binds the previously authored five source pages
  with their actual parsed-text/byte hashes, separate deal/subject/facility IDs,
  source authority/assessment basis, current evidence cutoff and missing-CFADS wire.
  Existing E-N01 registration bytes and prompts were not changed. Registration is
  an explicit authoring command, never a side effect of app refresh or intake.
- Same graph/worker/SQLite handles E-M01. After five actual stages it ends with
  WAITING_INFORMATION; preserves artifacts/checkpoints/missing items and releases
  the admission claim as a confirmed information stop. No model-stage synthesis,
  PanelDecision, package approval request or final memo is created. Actual fixture
  usage is five nodes/three deterministic tools/zero provider calls.
- Partial source inspection retains exact case/input/dependency binding and full
  original passages/formulas/policy results. prepare_synthesis and synthesis_task
  still reject incomplete prerequisites. No source inspection bypasses readiness.
- New Deal scenario, per-scenario Financial run labels, context cards and distinct-
  deal Dashboard counts support E-M01. Pending Information points to the simulated
  Analyst to obtain the2027 CFADS schedule. Workspace explains the missing field,
  score/band absent, cited available facts and disabled final controls. Replacement
  upload/continuation remains explicitly unsupported. No expiry/reset/recovery hack.

Executed:

```powershell
.\.venv\Scripts\python.exe -B tools/register_e_m01.py
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/e-m01-integration-final.xml
```

Observed full suite: **211 passed, 259 subtests passed in240.57s**. Time is whole-suite
duration, not app/model latency. New checks cover actual information terminal state,
zero synthesis/report dispatch, exact missing field, score abstention, source packet,
partial-to-synthesis refusal, duplicate no replay/no writes, cross-case operation
conflict, unauthorized start/source tamper, separate normal/missing deal counts and
Streamlit intake→sources→blocked approval→no memo→Dashboard. Existing E-N01 reviewed
approval/Reject/information response/reassessment tests remain passing.

After the final admission action label was corrected to RUN_E_M01_MISSING_FIXTURE,
the four focused missing-data tests were rerun: **4 passed in20.97s**.

Actual Edge browser check after restarting localhost8523: E-M01 Missing CFADS option
and Run registered E-M01 review control visible, zero exception boxes; no Run click
or new deal record was created by this read-only check. An initial text-only locator
failed; using the actual combobox/option succeeded. User server remains running.

No new dependency, model call, paid service, crawler, deployment or notebook install.
E-P01/F03 runtime/exception handling/Conditional, E-M01 new-document continuation,
actual extraction correction and funded Live/optional evaluations remain pending.

## Pending-work implementation — 2026-10-24

User authorized implementing the audit recommendations, then explicitly approved
the fictional assessments/cash bridge in evaluation/examples/core-case-authoring-proposal.md.
User explicitly deferred optional notebook dependencies. Current capability index:
[implementation-status.md](implementation-status.md).

1. Reconciled README, root instructions, HLD and spec status; retained original
   README under docs/history. Historical milestone claims no longer take priority.
2. Added provider.py pure offline request/response boundary: model/stage allowlist,
   original text, P3-05 caps, strict wires, refusal/truncation/error distinction,
   usage validation and dated cost estimates. Reasoning tokens are not counted
   twice. No client, credential read, transport, automatic retry or Live activation.
3. Financial History now scopes before counting, captures original borrower metadata
   for new events, filters deal/borrower/reviewer/action/status/inclusive UTC dates,
   paginates, shows original AI/risk details, exposes an independent deal timeline
   and exports all filtered pages with snapshot revalidation. Legacy fields stay
   Not captured. A UI test caught local-date versus UTC defaults; fixed to UTC today.
4. Core case kernel tests record risk recall and false-positive counts in offline
   JUnit properties. These are arithmetic-only evidence, not model/source quality.
5. Prepared E-P01/E-M01/E-F03 separate candidates: nine PDFs, fifteen parser-checked
   pages, manuscripts, extraction candidates and distinct source manifests. User
   approved fictional totals33/45 and E-F03's cash bridge; E-M01 score stays null.
   Existing E-N01 registrations/prompts and all budgets remain unchanged. No candidate
   is admitted to the runtime or labeled a completed supported Reject/Conditional.

Source preparation command:

```powershell
.\.venv\Scripts\python.exe -B tools/prepare_core_case_sources.py
```

Observed: three packages, each10 generated files before adding README; status
SOURCE_PREPARED_NOT_RUNTIME_REGISTERED. Actual PDF text is compared with all visible
manuscript lines (the parser omits blank lines). An overlong manuscript was caught
by the existing fixed-layout guard and explicitly wrapped before successful output.
Reruns preserve bytes and refuse mismatched existing artifacts. No source cropping
or changed financial thresholds. Source tests also check isolation/no original edits.

Final regression command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider -o junit_family=xunit1 --junitxml=var/evaluations/pending-work-offline-final.xml
```

Observed: **207 passed, 259 subtests passed in191.53s**, no warnings. Earlier206-pass
run had3 JUnit-family warnings; xunit1 retains the requested scenario properties
without that reporting incompatibility. New focused tests also passed: provider12,
core-kernel3, source-package1, scoped history/export1 and the expanded approve→memo→
history→filter/date→CSV UI journey1. Full-suite time is not application/model latency.

Actual local Edge inspection after restarting Streamlit on localhost8523: updated
History caption present and zero application exception boxes; Dashboard loaded.
Browser requests were limited to localhost. Mutation tests used temporary synthetic
workspaces. User's current app remains running at the same address.

Verified package presence without installation: OpenAI SDK present transitively;
IPython/ipykernel/nbclient/ragas absent. Presence grants no execution permission.
Nebius official quickstart and structured-output documentation were reviewed:
https://docs.tokenfactory.nebius.com/quickstart and
https://docs.tokenfactory.nebius.com/ai-models-inference/json . Exact chosen-model
capability, tokenizer fit, current prices and actual response accounting remain
unverified; stored cost estimates are dated2026-10-23, not invoice measurements.

Remaining: runtime adapters/registration for new cases, independent exception
receipts and supported Conditional review, extraction-miss correction, guarded
funded transport/Live graph, operator UX acceptance and optional retrieval/RAGAS.
No dependency install, paid call, crawler, hosted tracing or deployment occurred.

## Dashboard presentation milestone — 2026-10-24

Implemented the user-supplied screenshot/prompt within Screen 1: five distinct-deal
KPI filters, searchable attention queue, selected-deal cards, financial/policy
evidence navigation and recorded workflow/action guidance. Existing backend,
permissions, budgets and other five screens retained. See
[implementation matrix and mappings](design/dashboard-implementation-review.md).

Validation: full offline suite190 passed +259 subtests in67.35s; after final queue/table
refinements, focused command-center suite13 passed in28.57s. Local Edge checks at
1600/900/390px had zero exception boxes/JS page errors and no document overflow.
Read-only test compared database bytes before/after filters and citation navigation;
no graph replay allowed. No paid/external service, model call or dependency added.
Screenshot paths and honest partial/unavailable features are in the review document.

## Financial workflow and teaching milestone

Authority: user requested fixing the pending work in the recommended order.
Contracts: FIN-REVIEW-1.0 / FIN-REASSESS-1.0; architecture ADR-010.

1. Reconciled canonical prerequisite rows: normal pipeline/UI are no longer labeled
   not started; broader incomplete families retain Partial status.
2. Registered E-N01/review over the unchanged approved sources. Confidence0.65 is
   an explicitly authored fixture testing existing SYN-ESC-012, not model quality.
   Registered revision2 has its own case/input/synthesis digests; no new financial
   values, policy threshold, scoring premise or Runtime prompt was introduced.
3. Extended the same graph/worker with review_prepare and actual human interrupt.
   Scoped receipt-first actions persist comments, requests and Approve/Reject;
   NORMAL AuthorizedApprover and current gates are checked before resume and in
   the node. Same thread/ledger, no generation replay; paused is not completed.
   Confirmed reviewed journey consumes eleven nodes and four tools, zero providers.
4. Memo uses a reviewed renderer with real report-generation time, preserves AI
   confidence/referral, and adds simulated human decision/reason/reviewer/time.
   Financial history has frozen AI/risk/final-policy/source snapshots and scoped,
   snapshot-checked CSV. Preview records remain excluded. Comments after completion
   append history without changing disposition or regenerating the memo.
5. RiskManager can explicitly assess every request item against an exact registered
   PDF. Admission atomically stales the old request/supersedes the old unfinished
   run, retains the response and starts revision2/new thread on the same ledger.
   Reuse only identical verified intake/extraction; rerun downstream analysis and
   require final human review. Full path uses nineteen nodes and eight tools;
   original history remains. Unknown PDFs, stale approvals and further unsupported
   corrections fail instead of borrowing sample facts or resetting allowance.
6. Created notebooks/01_workflow.ipynb (same compiled graph, local SVG/Mermaid) and
   prototype/index.html (clickable six-page recorded fixture snapshot). Notebook
   cells are syntax-checked; IPython/Jupyter is absent and kernel execution is not
   claimed. Exporter uses scoped reads and does not overwrite existing snapshots.
7. Provider, embedding, index, paid evaluation and tracing remain disabled. No new
   dependency was installed and no key, paid call, crawler or deployment was used.

Verification observed so far: focused financial tests and UI-to-decision/memo/history
passed. The first broad regression attempt had185 passes and one worker timeout,
reporting an anomalous total10344.30 seconds. The same affected test then passed
in9.09 seconds, and the next complete suite passed186 methods plus259 subtests in
57.10 seconds. The180-second guard was not weakened. A subsequent concurrency test
passed: two identical responses admitted one reassessment/event. Final complete
suite result is recorded below after execution.

Final complete command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

Observed final complete suite: **188 passed, 259 subtests passed in116.73 seconds**.
This includes concurrent identical-response admission and the UI registered-source
response -> selected revision2 path (AppTest injects widget bytes; actual source
validation and graph/persistence execute). Whole-suite duration is not model or
application p95 latency. No general browser upload-transport acceptance is claimed.
The optional notebook kernel remains Not run; notebook code syntax and graph SVG
generation are tested. A final focused reassessment UI check after adding verified
sample-PDF download controls is recorded separately below.

Final focused command after verified source-download controls:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests/integration/test_command_center.py::CommandCenterTests::test_registered_response_ui_opens_revision2_after_risk_manager_assessment
```

Observed: **1 passed in56.71 seconds**. It exercises the actual scoped response
validation, current request, original ledger and selected new revision through
Streamlit AppTest with injected registered-upload bytes. Source-download reads
check the trusted manifest path and SHA before exposing a sample PDF. This timing
is a test-harness observation, not an application latency acceptance result.

Fresh local headless Edge checks: all six Streamlit pages loaded with zero exception
boxes; all six offline HTML destinations were clickable with zero script errors
and zero external requests. Existing application database file hash was unchanged.
Browser reads used existing data; mutation tests used temporary synthetic workspaces.
Manual WCAG/screen-reader/zoom acceptance and a live model-quality run remain unverified.

Remaining scope: general/new-fact uploads and source-profile registrations, Conditional
editing/support, broader missing/conflict/exception/E-F03 source cases, financial
history filter UI/PDF, explicit technical recovery UX, optional notebook environment,
Live Nebius adapter/token accounting and separately authorized retrieval/RAGAS runs.
This is an educational working fixture workflow, not production lending software.

## Compliance presentation audit fix — POLICY-VIEW-1.0

User authorization: "fix it" after the major-issue audit and recommendation to
correct the Workspace/memo compliance mismatch. Implemented a bounded read-model
correction; this does not claim completion of the larger missing workflows.

command_center.policy_display uses the selected run's recorded post-synthesis
final_policy for Workspace policy rows, exception count and policy evidence.
SYN-ESC-012 now shows EVALUATED, confidence0.85 and NOT_TRIGGERED, matching the
memo, instead of the earlier pending check. Workflow controls are distinguished
from policy outcomes. Before synthesis, checks stay preliminary/Pending. The view
checks scope, dependency and input identity and patches only copied references.
Unavailable source verification still removes citation buttons. Developer details
explicitly retain the original pre-synthesis stage; persisted artifacts and old
memos are never rewritten or regenerated by viewing this correction.

Actual final command:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

Observed: **176 passed, 259 subtests passed in 58.77 seconds**. Two new regression
methods exercise real temporary E-N01 runs and Streamlit UI: final rule/card/source
agreement with the memo, preserved original packet/records, preliminary state,
scope/input mismatch rejection, and withheld links on source failure. Initial
regression assertions exposed Markdown escaping and the preliminary control label;
the assertion and Pending display were corrected before the passing final run.
These are application checks, not new provider-quality or real lending evidence.

No rule, source registration, prompt, budget, model/provider setting, database schema
or dependency changed. No paid call or deployment occurred. Existing application
data were not migrated or rerun. Financial approval/resume, information fulfilment,
financial decision-history integration and additional registered end-to-end cases
remain pending. Restart Streamlit to load the corrected UI/service modules.

## User-authorized UI redesign V2 — 2026-10-24

The supplied V2 redesign is implemented for its immediate P0 scope under
[redesign-v2.md](design/redesign-v2.md). ui/command_center.py now renders a
borrower-centric dashboard with accurate counts/search/run grouping; sample intake
checklist and a disabled upload mode; shared deal/run context and persistent run
selection; six Workspace tabs with human-readable terms, financial definitions,
policy predicates, authored factor contributions and contextual evidence buttons;
nine recorded stage cards and output inspector; document-framed stored memo; and
a business-decision empty state separate from technical activity. Local theme/CSS
live in .streamlit/config.toml and ui/presentation.py. Dynamic authored HTML values
are escaped. Human actions remain disabled, and illustrative records stay separate.

Executed full suite: **174 passed, 259 subtests passed in 52.62 seconds** using
`.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`.
After final presentation adjustments the targeted seven command-center integration
methods passed again in **13.46 seconds**. Existing graph, admission, source and
memo tests remain part of the full suite. New checks cover two runs grouped into
one deal, older-run selection across screens, contextual factor-to-source buttons,
disabled decisions under Analyst/Approver, and upload-mode reads without DB writes.

Local headless Edge/Playwright captured all six desktop screens and a 390px mobile
Workspace under ignored var/evaluations/redesign-v2. The final browser run confirmed
the latest risk display, reported **no horizontal document overflow** and **zero
external requests**, and only read existing financial records. Screenshot review
led to extra header padding and removal of the risk-band trend arrow. Browser
harness attempts initially targeted native radio inputs/sidebar collapse elements;
the final check uses visible labels and a fresh mobile viewport. Screenshot review
and these narrow checks do not establish WCAG compliance, complete keyboard testing
or comprehensive responsive acceptance. No production/immutable audit claim.

No additional dependency, paid service, model call, document upload, financial
decision, budget change, schema change, deployment or case registration occurred.
Financial HITL/fulfilment, actual uploads, PDF export and future P1/P2 behaviors
remain pending. Restart a running Streamlit process to load the updated modules
and theme; preserve its existing SQLite data.

## Financial command-center alignment — executed 2026-10-24

Authority: user's instruction to fix the frontend/backend review findings.
Contract: [APP-READ-1.0](specs/financial-command-center-integration.md).
Decision: [ADR-009](architecture/decisions/009-financial-command-center-read-model.md).

Implemented root app.py, ui/command_center.py and command_center.py. Six destinations
now show actual registered E-N01 financial runs through the existing Store/worker.
The Analyst start service checks scope before dispatch. Navigation is read-only;
repeated submission of the same operation reads the prior result. Scope-filtered
projections join context/outcome/progress/claim/artifacts/events in one SQLite read
transaction. Unknown execution remains RECOVERY_REQUIRED. Stored reports are
checked against the report-generator artifact before display. Citation resolution
requires recorded source/packet identities; unavailable versions are withheld.
New stage events record real UTC timestamps; old timestamps are not backfilled.

Actual final command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Observed: **171 passed, 259 subtests passed in 21.24 seconds**, with outbound
network denied by the test harness. Four new integration methods cover the actual
Streamlit UI-to-worker flow, source/scope failures, denied starts, uncertain runs,
no replay and replaced-report detection. These are application test results,
not live-model quality, browser/accessibility acceptance or end-user latency.
The initial new read-model test exposed inappropriate use of provider-wire string
limits for persisted reports; it was corrected to the existing bounded envelope
decoder. Initial documentation edit attempts failed without writing; corrected
edits now record current status while retaining historical evidence.

No dependencies, schema, provider settings, prompts, case registrations or budget
limits changed. No real credentials, paid calls, deployment or original production
database run occurred. Tests use temporary workspaces; existing demo history is
preserved. No refreshed package build or manual browser review is claimed.

### Outstanding implementation, in dependency order

1. Prepare/register the already-designed review/missing/conflict/Reject source
   variants with exact approved premises and fixture output bindings. Do not
   invent a rule that any threshold breach causes rejection.
2. Add actual financial PendingReview registration and receipt-first transactional
   actions using RESUME-1.0, then same-thread graph interrupt/resume. Preserve
   simulated role/tier/prerequisite gates and retry/recovery protections. Current
   illustrative commands must never accept financial requests.
3. Wire information fulfilment to validated sources and analytical revision/new
   run/thread, staling dependent reviews/reports while retaining history. A note
   or generic checkbox must never clear missing evidence.
4. Connect actual financial human decisions, frozen analysis context, Conditional
   controls and financial history/export; validate approve/reject/pending flows
   end to end. The root history currently exposes execution events only; the
   separate illustrative history has decision filters/CSV.
5. Complete teaching notebook/HTML and focused manual usability/accessibility
   checks. Six navigable destinations do not mean every screen contract is done.
6. Separately verify Nebius adapter/schema/tokenizer/accounting and approved
   spending before any Live execution. DIRECT remains the grounding approach;
   embeddings/four-arm retrieval/RAGAS execution remain separate pending work.

No claim that all audit findings are fixed or the complete application is ready.
Authority: [PRD](product/prd.md), [HLD](architecture/hld.md), [repository design](architecture/repository-design.md), [feature contracts](specs/overview.md), [prerequisites](specs/overview.md#implementation-prerequisites-and-required-evidence), [evaluation plan](evaluation/evaluation-plan.md), [traceability](traceability.md)
Visual baseline: [design system](design/design-system.md)

## Authorization and scope

### Executed Decision History page and CSV audit export — 2026-10-24

The user explicitly requested a dedicated Decision History page across deals, historical comments/status transitions/reviewer/context, filters, clickable timelines and CSV/PDF audit export. [SPEC-013](specs/decision-history.md) / FR-021 was written before implementation and authorizes a sixth target screen plus scoped CSV export, superseding older five-screen/export-deferral limits for this feature only. Existing final-review permissions remain unchanged; the user's illustrative Risk Manager rejection/example timeline is not imported as authoritative permission or fabricated executed events.

Implemented decision_history.py, ui/decision_history.py and Page navigation in the existing tools/preview_human_review.py. The current preview exposes Human review and Decision History; the full six-screen financial app remains pending. History reads only saved ILLUSTRATIVE_UI_ONLY records, filters by actor workspace/allowed deals before counts/details, and uses one consistent SQLite read transaction with no initialize/write/schema migration. All five explicitly configured simulated roles can view/export the same allowed scope; no admin/global-scope bypass or authenticated identity is claimed. A missing database remains missing; an empty page never seeds decisions.

New review events atomically retain previous status, per-request sequence, trusted simulated reviewer name and DECISION-SNAPSHOT-1.0 containing available pre-action deal/AI/risk/compliance/policy/document context. Unknown values remain null. UI examples receive only clearly illustrative borrower labels/type, without invented loan amounts, AI recommendations, risk scores or source findings. Current deal status is a separate read-time projection. Legacy events are not rewritten; their exact expected_record_version in app_record_history may recover the real pre-action status/context, with missing historical names/context explicitly Not captured. No later borrower/context change fills or replaces old snapshots. Original financial records/prompts/rules/budgets/checkpoints remain unchanged.

The dashboard supports deal-ID/borrower/reviewer name-ID-role/action/event-status/inclusive-UTC-date filters, newest/oldest sorting, 25-row UI pagination and explicit matched counts. Selected event details expose exact original comments/request items, reviewer/tier, previous/new/current statuses, original revision/basis and captured AI/risk/policy/source context. Deal timeline events are clickable and ascending, independent of dashboard filters, with explicit review-action-only coverage. No upload, agent-start, reassessment or financial approval event is invented to fill the user's example. Absent data says Not captured rather than zero or latest values.

Explicit CSV preparation re-queries/re-authorizes the exact scoped filtered dataset digest and exports all matches across pages. Permission/scope/filter/data changes invalidate prepared bytes; stale digests are rejected. Exports include exact UTC event times, historical context, export time/digest and provenance. Quoted UTF-8 CSV neutralizes common spreadsheet-formula prefixes without modifying original comments. Above5000 events, narrow-filter/limit errors replace silent truncation; full timelines have the same explicit bounded-review limit. No PDF dependency was added; PDF is deferred because CSV satisfies 'CSV or PDF'. Export performs no write, provider request or external transmission.

Actual full command `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` passed **167 tests and 259 subtests in16.76 seconds**, zero failures/skips. Ten new service and five new Streamlit AppTest methods cover scopes/count leakage, frozen snapshots, faithful legacy recovery, filters/date boundaries, stable order/pages, timeline/detail navigation, scoped all-page CSV, stale/other-actor export denial, formula neutralization, explicit limits, read-only/missing-database behavior, corrupt cross-deal snapshots and Administrator read/export without credit powers. Existing human-review, normal graph/report, arithmetic, provider-disable and quality checks still pass. Focused runs passed20 service methods/37 subtests, then22 history/UI/regression methods/13 subtests. Tests used temporary synthetic UI records, not the user's illustrative names/decisions or real borrower data.

Offline package command `uv build --python .venv\Scripts\python.exe --no-build-isolation --no-sources --offline --no-cache --out-dir var/evaluations/decision-history-2026-10-24/build` succeeded for sdist/wheel, including the new history service/page. PRD/HLD/spec overview/UI/review/persistence/design/repository/evaluation/traceability/AGENTS/README are aligned with the explicit sixth-screen scope. No sample decisions were seeded into the working database, no browser/server was launched, no dependency installed, no model/API call or charge incurred. Manual browser/mobile/accessibility, actual financial lifecycle adapter, full app shell and Live remain pending. Local history/export does not constitute immutable production audit storage.

### Executed role-aware Human review panel — 2026-10-24

The user authorized comments, Approve, Reject and Request Additional Information (Pending), controlled by user-role permissions and recorded with reviewer/comments/status/timestamp. [REVIEW-UI-1.0](specs/human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10) was specified before coding and is linked from PRD/HLD/specs/design/evaluation/traceability/AGENTS/README. It preserves P3-02: Analyst/RiskManager/ComplianceOfficer/AuthorizedApprover may add comments/request information, only a correctly tiered AuthorizedApprover may record final Approve/Reject, and Administrator is read-only. Every submitted action requires comments; information requests also require specific items. Required source/specialty/tier gates remain mandatory and information requests cannot be cleared by a comment or role switch.

Implemented review_action_availability in existing review.py, review_actions.py as the isolated persisted preview adapter, ui/human_review.py as the reusable Streamlit panel and tools/preview_human_review.py as the local entry point. Opening/refreshing reads only; intentional Prepare UI review samples creates three clearly labeled UI-only examples (ready, blocked, senior) in existing app_records/history within the same configured SQLite database. Examples have no loan analysis/source pack/risk grade/AI recommendation or real paused checkpoint. They never modify the registered E-N01 records, become a financial fixture or create a real HumanDisposition. Preview records carry ILLUSTRATIVE_UI_ONLY and graph_progress=NOT_CONNECTED; financial pending-request registration and RESUME-1.0 dispatch remain pending.

Each service command revalidates strict input, scope/role/tier/current record/basis/gate and active-execution state in a short serialized transaction. The event and updated review projection commit together. Events retain exact comments, request items, simulated reviewer ID/role/tier, deal/thread/revision/basis, action/status and application-generated UTC time. Duplicate identical operations return the original event/time; changed reuse conflicts; failed writes roll back. A final decision cannot be replaced by another action, while later comments preserve its status. Information requests retain a pending review and explicit NEEDS_INFORMATION state, with no preview clearance/reset shortcut. Local history is retained, not immutable audit storage.

The panel uses an initially unselected permitted action, required comment, conditional requested-item field, one explicit Record review action button, service-derived unavailable-action reasons, UTC-stamped plain-text history and separate report status. It preserves per-deal session drafts across errors/deal switching, detects changed records and requires Refresh review before another submission, and renders HTML/Markdown-like comments as inert text. Role selection is visibly simulated; no authentication, remote notification, provider/model request, graph resume or report completion is claimed. Conditional Approve's existing supported-condition contract is retained; its editor/financial adapter are outside this bounded preview.

Actual final validation: `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` passed **152 tests and 246 subtests in 14.11 seconds**, zero failures/skips, after adding immediate committed-status feedback. The preceding pass took14.82 seconds and is retained as historical verification. This includes10 new service tests and7 Streamlit AppTest methods, alongside all existing normal graph/quality/arithmetic checks. Coverage includes five roles, both tiers, wrong scope, mandatory comments/items, pending versus final states, exact UTC/duplicate timestamps, stale/busy denial, transaction rollback, original-record preservation, explicit preparation, inert text, no preselected decision and retained drafts. The first focused attempt passed backend guards but failed6 UI methods because the universal network guard blocked Windows asyncio's internal socketpair. A test-only wrapper now permits only the owning thread's internal loopback pair creation, while external/provider traffic remains denied. The focused rerun passed22 methods/27 subtests before full regression. No application schema or financial rule was weakened to pass.

Offline local sdist/wheel build succeeded with `uv build --python .venv\Scripts\python.exe --no-build-isolation --no-sources --offline --no-cache --out-dir var/evaluations/review-ui-2026-10-24/build-final`; the final wheel contains the new review adapter and UI package. The earlier build is retained separately. Run the local preview from the source checkout with `.\.venv\Scripts\python.exe -m streamlit run tools/preview_human_review.py --server.address 127.0.0.1`; the command is documented, not launched as a browser/server during this turn. Actual tests used temporary databases; no illustrative samples were seeded into the user's working database. Manual browser, keyboard/screen-reader/mobile usability, full five-screen integration and actual financial interrupt/resume remain Not run/pending. No dependencies were installed, no API key requested and no paid service or deployment activated.

### Executed offline document and synthesis quality prerequisites — 2026-10-24

The user authorized implementing the recommended document-understanding and summary-quality improvements. [QUALITY-REVIEW-1.0](evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) was added to the existing specification before implementation. model_comparison.py now builds extraction tasks through current registered-case validation and full-inventory BASELINE DOCVERIFY coverage. All five original pages remain verbatim, with source hashes/locations/dependencies, basis metadata and explicit scope/review date/cutoff. The runtime prompts, source/case/synthesis registrations, financial formulas, sample policy, sequential nine-stage graph and two normal generation stages are unchanged.

Extraction review now reports every field's supplied versus authored expected value/basis/reference set, available-slot denominators, missing/conflicting fields and unresolved references. A correct value cited to the wrong existing page is visible without pretending that an exact reference set is the only possible semantic support. Synthesis review validates structure and transitive references for every observation, rationale, condition and proposed-action reason, retains original text plus full local supporting context, and recomputes routing diagnostics through existing Python rules. Original pre-synthesis evidence is labeled separately from final confidence-policy evaluations. All arbitrary prose remains MANUAL_REVIEW_REQUIRED; there is no automatic semantic approval, recommendation acceptance or human disposition.

quality_review.py and tools/review_model_response.py accept an explicit bounded local capture, bind its task digest to the current source/prompt/schema request, and retain exact original capture bytes, output text and task snapshot before scoring. Changed attempt reuse fails rather than overwriting history; declared repairs are separate attempts. Truncated/refused/error/unknown outcomes are not parsed as successful outputs even when the text is valid JSON. These statuses/model IDs/origins are local declarations, not verified provider records. All observed provider usage/cost/latency and real model-quality/RAGAS cells remain null. No application database mutation, graph execution, secret read, provider SDK, automatic repair, dependency installation or paid request is introduced.

Actual final regression command `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` passed **135 tests and 222 subtests in 25.64 seconds**, zero failures/skips. This includes the existing normal graph/report tests and 15 new quality methods covering full source/basis preservation, missing/wrong-period/conflicting values, existing-but-wrong citations, arbitrary unsupported narrative remaining unverified, all narrative paths, stale packets, low-confidence routing, response cutoff/history, completion statuses, no side effects and sanitized CLI output. The first focused run found three invalid test response encodings/owner examples; tests were corrected to use the existing numeric-confidence wire serializer and allowlisted Analyst target, without weakening schemas or changing Runtime prompts. The final focused run passed25 methods/29 subtests before the full regression.

The explicit local check driver succeeded after correcting its standalone test-helper import path. It recorded three FIXTURE_TEST captures (complete extraction, complete synthesis, parseable-but-declared-truncated extraction) at var/evaluations/quality-review-2026-10-24/checks-68f0caa25051c6bf.json. The original complete example has31/31 exact available value/basis matches and four narrative review targets; these are authored Fixture comparisons, not live accuracy. The truncated response retains31 available slots and zero correct slots. The paired parser-independent layout/disclosure comparison exercised **14 unique cases / 28 BASELINE–ADAPTIVE executions, zero controlled-check failures**; BASELINE remains default and ADAPTIVE is not adopted. These flags/geometries are supplied synthetic block inputs, not evidence of generic PDF-layout fidelity.

Actual CLI `.\.venv\Scripts\python.exe tools/review_model_response.py var/evaluations/quality-review-2026-10-24/synthesizer-complete.capture.json` safely reused the recorded original at var/evaluations/response-review/bd348a6b-c546-5912-8fca-0d6dded623f1/review.json. The explicit preparation CLI created the new content-addressed two-task plan f7b5d32d5ede6c330ff7e547e5d9bb86bfa3fcf25c23be035de6f49d04a76bbd; older plans/reports remain unchanged. Current serialized task sizes are22,847 extraction and23,875 synthesis UTF-8 bytes, not tokens or proof of fitting8000/2000 caps. Actual deployed tokenizer/full-request/schema/usage checks remain required; no evidence is truncated or allowance increased.

Offline source/wheel build succeeded with `uv build --python .venv\Scripts\python.exe --no-build-isolation --no-sources --offline --no-cache --out-dir var/evaluations/quality-review-2026-10-24/build`. The app still requires its reviewed source checkout assets; this is not a standalone deployed demo. PRD, HLD, repository/spec overview, relevant extraction/synthesis/context specs, evaluation/traceability, README and AGENTS now link the bounded implementation. Remaining work: verified Nebius adapter and token preflight, explicit funded access, Live source-support handling, additional registered scenarios/HITL/UI and separately budgeted optional RAGAS. No measured live quality improvement, model winner, latency saving or production readiness is claimed.

### Executed normal E-N01 graph, synthesis and memo — 2026-10-24

The user accepted the recommended next step: complete the E-N01 synthesis packet and offline validation, then connect the normal Fixture path to report generation. E-N01-SYNTHESIS-1.0 now separately pins the existing case/package, semantic request, ordinary canned response and AI-authored educational rubric. Original source PDFs, case/extraction registration, policy, instruction hashes and financial formulas remain unchanged. The request explicitly carries the existing 2027 annual projection and transaction basis, separate from the review date/cutoff. Four narrative targets are checked; no HUMAN_SUPPORTED record or real model result is invented.

Actual implementation: services.py now exposes separate financial/compliance/risk handoffs; panel_codec.py restores only known primitive panel shapes and exact Decimal strings. synthesis.py constructs the current three-panel/reference packet and rejects changed input, scope, response, rubric or unresolved references. graph.py is the shared nine-stage normal definition; worker.py uses the existing SQLite admission slot, durable per-node reservations/artifacts/events, pickle-disabled SqliteSaver and terminal-report checks. Duplicate completed commands read the recorded result; uncertain failures retain reservations/RECOVERY_REQUIRED with no automatic replay. memo.py renders the seven sections in pure Python, with explicit source/period/support limitations, raw versus Python-owned routing, separate human disposition and internal citation navigation. Post-synthesis confidence-rule citations use the actual final evaluation while the pre-synthesis request remains unchanged. Renderer version E-N01-MEMO-1.1 is distinct from template MEMO-1.0.

Final application validation: **120 tests and 206 subtests passed in 8.36 seconds**, zero failures/skips. New checks cover same-input synthesis binding, four narrative targets, exact primitive panel round trips, foreign/stale/changed handoffs, schema/source guards, deterministic inert memo rendering, cutoff/future-event protection, actual graph/checkpoint completion, duplicate non-replay, Busy, retained uncertain reservations and hosted-tracing rejection. The first focused run exposed an open SQLite handle on Windows; explicit connection closing fixed it before the final pass. These tests are not model-quality or business-performance measurements.

Actual local demo: operation bc2d14d0-7f97-4c49-a749-fba8919889d0 completed run700a2944-849d-5f0b-b311-d99a5d44e19d with **9 nodes, 4 Python tools, 0 provider requests**, 18 recorded stage events and 11 SQLite checkpoints. Report cutoff17 excludes its own later completion event. Repeating the same operation returned duplicate=true without another graph execution. The sample memo is retained at var/demos/e-n01/700a2944-849d-5f0b-b311-d99a5d44e19d/credit-memo.md with run.json; the prior local renderer artifact remains history. Observed source-backed fixture values are DSCR1.50, leverage3.00, equipment LTV60.00% and authored21.00 Low; the original simulated recommendation is Approve with fixture confidence0.85, while human disposition is null and credit review is Not required by configured demo rules. No real credit approval is asserted.

The offline Qwen/Nano preparation command now records **two shared task packets**, extraction and synthesis, under var/evaluations/generation-comparison/b44eef7fa0faa6e0dc0fef97e68e3b6826bfafa538c29dd7ab15999678c6c92a/readiness.json. Both model arms remain NOT_RUN with null quality/latency/billed usage/cost/winner. Serialized request sizes are21,818 and23,875 UTF-8 bytes respectively; these are not token counts or proof of fitting the unchanged aggregate8,000/2,000 ceilings. Actual provider-tokenizer/full-request preflight and any permitted lossless context optimization remain necessary before Live dispatch; no budget is increased.

Offline local sdist/wheel build succeeded with the existing approved command and no dependency downloads. Completion evidence under var/evaluations/e-n01-synthesis/completion.json verifies the original case registration and instruction hashes, released execution claim, final checkpoint, 96 internal citation links to33 targets, and698 existing local Markdown link targets with no missing files. The check is target-existence validation, not a full heading/browser/UI audit. Wheel evidence includes all five new runtime modules; this remains a source-checkout application, not a standalone packaged demo or deployment.

Remaining M3 scope: other registered cases, actual human-review interrupts/handling, analytical corrections, full cancellation/recovery services and Live support flows. Five-screen UI, Jupyter/HTML, generic uploaded-reference chunking/embeddings/retrieval, funded model comparison and optional RAGAS remain pending. This completes one actual normal Fixture slice, not all M3 or the five-day deliverable. No API key, paid request, tracing connection, external service, project license, deployment or original-source modification occurred.

### Qwen versus Nemotron comparison preparation

The user accepted the recommended same-input Qwen/Nano comparison. [GEN-COMPARE-1.0](evaluation/generation-model-comparison.md) now defines the exact scope, unready cases, measurement/acceptance boundaries and later paid-run prerequisites. config/generation_comparison.toml pins Qwen/Qwen3-30B-A3B-Instruct-2507 as the baseline candidate and nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B as challenger, with dated list rates and disabled paid execution. model_comparison.py reuses approved role instructions, strict extraction schema and the verified registered E-N01 source pages; no reference answer/gold is placed in its task packet. It adds conservative local field/reference checks and Decimal price estimates without a provider client, new dependency, graph task or app-model switch.

Actual evidence: 108 application tests and 203 subtests passed in 22.79 seconds. Ten new unit/CLI methods cover exact configuration/activation guards, paired packet identity, null/unready states, estimate validation, response parsing/field/ref checks, no secret/network/client/database operations and history-safe CLI behavior. These are harness/application checks, not model quality, retrieval/RAGAS results or deal latency. Existing source registrations, Runtime hashes, model.toml disabled flags, policies, generation budgets and embedding choice remain unchanged.

The explicit tools/prepare_model_comparison.py command succeeded with status PREPARED_OFFLINE_NOT_RUN, one shared extraction task packet, two comparison arms, zero provider requests and winner=null. It retained the exact content-addressed plan under ignored var/evaluations/generation-comparison/1e4c70c07ad20b5fffb62450668aa89702d10ef7c9d86cb79dad6164659c6751/readiness.json. Neither tokens, billed cost, latency nor quality is fabricated; those measurements remain null. E-N01 synthesis needs its compact panel/reference packet and rubric; E-M01/E-C01/E-F03 need registered source packs and rubrics. Provider schema/tokenizer/reasoning/usage verification, local credentials and a concrete comparison allowance precede live work. No paid request, model download, automatic selection, deployment or app database mutation occurred.

### Qwen3-Embedding-8B selection and offline checks

The user approved the recommended Qwen/Qwen3-Embedding-8B after the available-model/pricing review. [ADR-008](architecture/decisions/008-nebius-hosted-embeddings.md), PRD/HLD/specifications/evaluation guidance and configuration now record this exact model. The dated public catalog observation lists active status,4096 dimensions, USD0.01 per million input tokens and zero output-token charge; the selected-entry evidence is retained under ignored var/evaluations/nebius-selection/qwen-catalog-observation.json. These observations are not a request/response smoke test or future price guarantee.

The strict NEBIUS-EMBEDDING-1.1 configuration pins this model and catalog metadata, with enabled=false, no paid allowance, UNCONFIGURED deployment revision/token-count method, null max_input_tokens and disabled indexing. Catalog40960 versus upstream32K limits remain unresolved for the deployed service. No local weights or arbitrary replacement model are introduced. Older inspection hashes and observations retain their original configurations.

Actual validation:98 application tests and190 subtests passed in5.19 seconds. The existing configuration guard now checks the chosen model/catalog metadata while rejecting premature activation, arbitrary dimensions, unverified token ceilings, modified rates and false verification status. Import/source-isolation and retired-download checks still pass. No dependency change, paid request, embedding/index build, retrieval benchmark, RAGAS score or deployment occurred. Remaining: deployed API/tokenizer/batch/normalization/usage/data-handling verification, later local credentials, a concrete paid allowance and subsequent small synthetic smoke test. Model selection needs no repeat approval.

### Earlier provider-only selection and offline checks

The user selected hosted embeddings to avoid running an embedding model locally. [ADR-008](architecture/decisions/008-nebius-hosted-embeddings.md) supersedes ADR-007's local BGE choice. PRD/HLD/specs, agent engineering guidance, repository plan, evaluation/report/traceability documents and root AGENTS.md now identify this override. Historical installation and inspection evidence is retained. The retired tools/setup_reference_model.py stops before download/import/filesystem work; no local weights are required. Existing optional packages/lockfile are retained without reinstalling or removing unrelated dependencies.

config/source_ingestion.toml and its strict inspection profile select NEBIUS-EMBEDDING-1.0 with enabled=false, model/revision/counting method UNCONFIGURED, null dimensions/input ceiling and no approved allowance. Indexing remains false. The metadata check reports those exact states with zero requests/model loads. Changing the configuration changes its inspection profile digest: preserve older reports and their original digest; never relabel or rewrite prior evidence as hosted-model verification or source admission.

Actual validation for this change:98 application tests and186 subtests passed in6.43 seconds. Two new checks reject inherited BGE dimensions/token limits/local device or premature activation, and prove the retired download command stops without network, optional-model imports or directory creation. The existing no-side-effect import/inspection and source-isolation checks still pass. This timing is test execution, not application/model latency. No dependency install, model request, index build, benchmark, RAGAS score, deployment or charge occurred. A selected available Nebius model/API/tokenizer/limits/rate/data-handling contract, later local credentials and an explicit paid allowance are still required before actual embeddings.

Current uploaded-source result: the newly supplied PDF was inspected locally and retained with its exact hash. LOCAL-REFERENCE-1.1 prevents inheriting the earlier configured source identity;96 combined methods pass. [Evidence](#uploaded-reference-inspection-and-source-binding-correction) supersedes prior no-user-file statements only for this source. Actual source origin/support remain unverified; no index/model/crawler or loan decision was produced.

Latest execution authorization2026-10-23: the user instructed now move with next steps, authorizing the accepted optional setup/local foundation. They then chose to download/upload the document rather than provide an SEC contact: LOCAL_FILE is the active route; no SEC contact/request or browser setup is required now. Optional packages are installed and the local inspection slice is implemented/tested. Earlier no-install/no-code statements apply to their historical stages. [Current evidence](#local-reference-setup-and-inspection-evidence) supersedes them for this scoped slice only.

Selected public source and approved stack: the exact SEC exhibit URL and local-file intake (Crawl4AI inactive) + Nebius-hosted embeddings under ADR-008 + SQLite-backed exact vector search are accepted. [Source classification](specs/public-financial-sources.md#selected-sec-source-and-suitability) records a credit agreement, not a statement corpus. Read-only web inspection succeeded; crawler/snapshot/index/retrieval execution has not occurred. Do not repeat source or architecture approval. Preserve SEG-1.0 agreement handling; statement-specific tests need an actual statement source. Remaining prerequisites are verified versions/licenses/setup and implementation tests.

Accepted public-source extension: [contract](specs/public-financial-sources.md) and [ADR-007](architecture/decisions/007-proposed-public-financial-rag.md) govern the selected public-reference path. Ordered tasks are setup/license/package/model verification -> mocked ingestion/provenance and access limits -> faithful parent/child segmentation -> Nebius-hosted embeddings and additive SQLite schema/storage -> paired DIRECT/KEYWORD/VECTOR/HYBRID comparison -> citation integration. Local architecture approval is fulfilled; environment permissions and verified prerequisites still apply to actual setup. Optional package installation and local-file inspection have now run; no browser setup, content crawl, BGE-weight download, vector schema/index or retrieval benchmark has run. This does not replace the pending core LangGraph/synthesis/HITL/report milestone or silently extend the five-day delivery target.

Current authorization2026-10-23: after the explicit A1-A4/next-steps request, the user said “ok move with next steps.” This resumes development and approves the presented E-N01 educational premises, ratings and deterministic integration. CASE-REG-1.0 records the exact current source/metadata/default extraction/policy/instruction binding; no repeated case/parser approval is needed. It is not independent banking validation, Live semantic support, generic Six Flags ingestion, a paid allowance or a completed full graph.

Latest parser authorization2026-10-23: user explicitly requested installing the proposed parser and verifying the PDFs. This approves pypdf installation and known-corpus checks; it does not approve A1-A4, source authority/risk assessments, fixture registration, generic uploads or paid inference. Earlier parser-pending statements in historical evidence below are superseded by the current parser section.

Latest scoped authorization2026-10-23: following the uploaded-document review, the user instructed moving to the next steps. This authorizes M2's local source-pack preparation and already specified arithmetic. The actual uploaded PDF remains unchanged/outside fixtures. New case assumptions and the unresolved parser license/dependency selection are presented concretely below; neither is silently approved. No paid service, parser install or complete fixture registration is included.

Current authorization, 2026-10-23: after approving the local M1 direction, the user explicitly permitted dependency installation and requested simple explanations. Setup succeeded with Python3.12.15; .venv/uv.lock exist,43 foundation methods and the refreshed local build passed. Root AGENTS.md is active. The earlier rejected install is historical; no rejection was bypassed. M1's scoped foundation checks are complete. The earlier planning/no-code paragraphs below describe prior phase edits. Later source-pack, financial graph, UI, provider, paid evaluation and deployment boundaries remain unchanged.

The user instructed: use the findings and apply them to move forward with the next implementation steps. Treat this as authorization to advance the existing Phase 4 repository direction into concrete Phase 5 execution/design planning. R4-01–08 remain the implementation direction. This records progression to planning, not an invented completed runtime check, blanket paid permission or approval of an unseen build milestone.

The original Phase 5 gate requires approval of the first implementation milestone. This document makes M1 concrete for that approval. No source package, root AGENTS.md, environment, lockfile, database, synthetic PDF, UI, notebook or HTML is created here. M1 approval would authorize its listed local files, dependency resolution/downloads and offline tests, subject to actual environment permissions. It would not authorize a parser/project-license choice, Git/remote publication, Nebius/evaluator calls, hosted tracing or deployment. Later milestones remain the ordered delivery plan; this request seeks M1 execution approval specifically.

Keep the five-day educational target, one graph/shared service layer, five screens, synthetic USD term loans, DIRECT grounding, two normal successful Live generation tasks and all existing cumulative limits. No automatic expiry or cleanup. Real borrower data and operational financial decisions are outside scope.

## Public-reference implementation tasks after accepted ADR-007

Documentation alignment evidence2026-10-23:24 related Markdown documents now record the accepted crawler/embedding/storage choices and separate pending setup/runtime work. Static validation resolved661 local links across55 active Markdown files with zero missing targets/headings. Both Runtime instruction hashes still match E-N01 registration, and all13 runtime/configuration/dependency files bound by the earlier M2 completion evidence are unchanged. No application tests, crawler, embedding job or benchmark were rerun for this documentation-only change; prior85-method evidence is retained at its original scope.

The following are planned extension tasks, not executed results or new loan business rules. Runtime/source artifacts stay under ignored var/; pyproject.toml/uv.lock change only during the later verified setup task.

| Order | Task and planned ownership | Required evidence / done condition |
|---|---|---|
| PUB-01 | Verify optional crawler compatibility and Nebius embedding model/API/tokenizer/limits/rates/data handling and explicit allowance; config/source_ingestion.toml and optional dependency groups | Python3.12/Windows compatibility, licenses, resource needs and controlled download/cache paths documented; no import-time work; no invented contact identity |
| PUB-02 | public_sources.py and source config; mocked transports | Exact selected URL, robots/redirect/subresource/rate/resource controls, snapshots/provenance, idempotent observations and explicit partial/error states tested before a live fetch |
| PUB-03 | public_sources.py/context helpers; faithful segmentation | Clause/definition/qualifier and table-period links retained; full embedding input counted with pinned tokenizer; no truncation; original spans navigate |
| PUB-04 | embeddings.py and existing storage.py application-owned records | Finite typed vectors, model/dimension/build validation; versioned additive schema change preserves application history and checkpointer ownership; interrupted build not active |
| PUB-05 | retrieval.py/retrieval_benchmark.py and frozen annotations | Same-corpus DIRECT/KEYWORD/VECTOR/HYBRID results, actual ranks/coverage/exclusions and cold/warm work reported; no gold input or automatic reranker/default switch |
| PUB-06 | Existing Workspace/Activity read projections, UI and evidence tests | Distinct public-reference label, retained-snapshot/section citations, no fake PDF pages/loan score, no fetching or embedding on view |

Tests use synthetic HTML and fake embeddings first; they establish control behavior, not real model retrieval quality. Later approved-source execution must record actual fidelity, embeddings and retrieval outcomes. Initial whole-agreement indexing still obeys size/chunk limits; overflow preserves partial evidence and stops. Existing no-automatic-expiry, exact source scope and separate paid-inference gates remain. Do not reset a database to roll back an index change: leave the last valid complete build active, preserve failed-build history and use a tested schema rollback/recovery plan.

## Uploaded-reference inspection and source-binding correction

Observed2026-10-23: the user supplied a different PDF from the earlier selected source. Actual local inspection passed for812,132 bytes/47 physical pages, SHA256 e0920b4305d4eceafd2f9ec1b0e1ca34315b04ccf6bef0112e80e75996c22f4b. Text extraction produced186,694 characters; physical pages2/12/14/23/29/34/38 yielded only header/footer text, not substantive financial evidence. This is text review, not visual/table fidelity certification.

LOCAL-REFERENCE-1.1 fixes the observed scope-label gap before retaining this source: arbitrary uploads now have corpus_id=null, declared_source={}, origin_status=UNBOUND_LOCAL_UPLOAD and scope_status=NO_CORPUS_ADMISSION. The configured source is preserved only as expected_profile_source. Matching company text or uploaded instructions cannot bind a document. Prior1.0 reports/configuration remain retained; the configuration was not silently replaced with a new case. The inspection/schema digest changes with the output contract.

The actual CLI retained source/inspection.json under ignored var/reference-inspections/d40201181140170e6c19cfd974e0be5d5c583a340c5d96a5605840235e1ff671; review.json records manual text findings and PDF page references separately. The original Downloads file is unchanged. No public source bodies are committed as fixtures or model context. The reference fits the local250-page limit but exceeds core10-page loan intake; no complete financial review or score is claimed.

Eleven local-source tests passed first, then96 combined application methods passed with zero failures/errors/skips (console5.72 seconds; test duration is not deal latency). The added regression extends existing source-isolation checks: a matching company name and a command embedded in source text cannot grant corpus membership or support. No new library, download, provider/crawler call, BGE model, embedding, index, benchmark or financial policy rule. Earlier95-method/build evidence remains historical; the package build was not rerun for this source-label-only change.

Commands: python tools/inspect_local_reference.py with the explicitly supplied Downloads path, and .venv/Scripts/python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/public-source-setup/source-binding-pytest.xml. User-provided bytes are not included in ordinary diagnostics. Next remains faithful source-aware segmentation and model/vector/retrieval implementation with explicit source/corpus admission; do not index the new file under the earlier selected company automatically.

## Local-reference setup and inspection evidence

Observed2026-10-23 local date. This is APPLICATION_TEST/setup evidence, not a completed crawl, model/index evaluation, public-company financial analysis or the full loan graph.

- Python3.12.15/Windows: official PyPI metadata verified crawl4ai0.9.5 and sentence-transformers6.2.0; uv resolved149 packages and installed the optional groups. CPU torch2.14.1+cpu, transformers5.20.2 and playwright1.64.1 are present. Prior package constraints are retained except xxhash4.0.2 ->3.8.2 required by Crawl4AI. The old manifest/lock and metadata/license observations are retained under ignored var/evaluations/public-source-setup.
- Installed license metadata/files were inspected, including Crawl4AI's additional attribution requirement; README credits preserve its required statement. This does not select a project license or claim a complete distribution license audit.
- Explicit offline torch/sentence-transformers import and a CPU tensor calculation passed with zero socket/DNS attempts. Cold import took77.530 seconds; no weights were loaded, so this is neither embedding-query latency nor model readiness. Browser/model caches were directed into ignored local setup paths; no browser was installed/launched.
- config/source_ingestion.toml declares LOCAL_FILE, the expected SEC source/company and10MiB/250-reference-page bounds. crawler_enabled=false, embedding artifact_revision=UNCONFIGURED and index_enabled=false are deliberate. No contact email is required or stored.
- public_sources.py implements supplied-byte inspection, exact file/text/profile/observation identity, inactive HTML and table-row context, actual PDF-page locators, explicit missing/unsupported/encoding stops and unverified origin/support. This is inspection-only, not financial extraction or layout/semantic certification. Unrelated input cannot become a registered synthetic loan by carrying the expected declared URL.
- tools/inspect_local_reference.py reads an explicit local path bounded before parsing, retains original bytes and a separate observation report, and never fetches links. tools/check_public_source_setup.py reads metadata only. No database/vector schema change is made by this slice.
-95 combined methods passed, zero failures/errors/skips; eight new source unit methods and two CLI integration methods cover active-resource isolation, table/year/unit context, invalid bytes/type/name/encoding, malformed/blank/encrypted/over-limit files, profile/timestamp tampering, import-side-effect denial and retained observations/stopped-command behavior. The full original85-method suite remains passing. JUnit suite time4.389 seconds (console total4.49 seconds) is test duration, not deal latency.
- Re-running E-N01 panels still gives21 Low,0 policy exceptions/0 missing material inputs, final_ready=false and zero model calls. No original source/configuration/prompt identity changed.
- The first offline packaging attempt could not replace an older dist artifact under sandbox permissions. An approved retry to a fresh ignored evidence build directory produced source and wheel packages successfully without network. The wheel includes public_sources.py; this source-checkout package is not a deployed app and does not bundle source/config/model artifacts.

Actual commands:

```powershell
uv lock --python 3.12
uv sync --frozen --python 3.12 --group dev --extra crawl --extra embeddings
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/public-source-setup/pytest.xml
.\.venv\Scripts\python.exe tools/check_public_source_setup.py
.\.venv\Scripts\python.exe tools/run_e_n01_panels.py
uv build --python .venv\Scripts\python.exe --no-build-isolation --no-sources --offline --no-cache --out-dir var/evaluations/public-source-setup/build
```

The initial sandbox metadata/cache access failed; approved escalated commands performed actual resolution/installation. No environment rejection was bypassed. Detailed ignored evidence: var/evaluations/public-source-setup/{pypi-metadata.json,installed-package-licenses.json,offline-import-check.json,pytest.xml,completion.json}. Existing earlier records and source drafts remain.

Historical remaining-work snapshot from the earlier local-library setup: the upload was subsequently inspected and ADR-008 replaced BGE artifact setup with hosted model/API/tokenizer/rate/allowance verification. Source-profile preparation, faithful segmentation, hosted embedding/vector-storage implementation and the four-arm benchmark remain pending. PUB-01 has package/import evidence but model artifact readiness is incomplete; PUB-02 has local-file inspection, not a verified remote crawler. PUB-03-06 remain pending. Keep the core graph/UI milestones visible; no paid service, remote content fetch, deployment or full RAG result occurred.

## Observed environment and remaining uncertainty

Historical pre-installation observations on2026-10-23. They describe the initial inspection; current installed versions and compatibility results are in the M1 evidence section below:

| Item | Observed result | Implication |
|---|---|---|
| Workspace | Only docs/ existed before these Phase 5 documents | Application implementation has not started |
| Default shell Python | 3.14.8 | Do not silently use the default for a Python3.12 project |
| Installed project-target interpreter | uv-managed CPython3.12.15 | Request3.12 explicitly when creating the project environment; no interpreter download is currently needed |
| uv | 0.12.23 | Available; dependency resolution/sync still untested for this project |
| sqlite3 library exposed by installed3.12 | 3.53.1 | Observed library version only; not proof that the selected LangGraph saver works |
| Target3.12 packages | Pydantic, LangGraph, langchain-core, SQLite saver, Streamlit, pytest and HTTPX were not installed there | Resolve into an isolated project environment after approval; do not rely on packages in another interpreter |
| uv cache access | Restricted execution initially denied cache access; approved read-only interpreter listing succeeded | Actual environment setup may require managed permission; listing approval is not package-installation approval |
| Provider/model/tokenizer/rates | Not configured or verified | Live and paid scoring remain unavailable |

No package pins are guessed here. Generate uv.lock through actual successful resolution, review the resolved dependencies/terms and record the tested combination. An available interpreter alone does not complete PREREQ-02.

## Ordered milestones and planning allocation

Day labels are planning allocations, not observed effort or guaranteed dates. The five-day clock begins after required approvals/access to the chosen local setup. A failed compatibility/license/evidence check causes a scoped replan; it never authorizes weaker controls or fabricated results.

| Milestone | Planning allocation | Prerequisites / specs | Demonstrable result |
|---|---|---|---|
| M1 Contracts and persistent foundation | Day1 starting slice | PREREQ-01/02 and local part of03; SPEC-002/005/006/007/008/011 | Offline contract/codec/admission/review-basis compatibility harness; no full deal demo yet |
| M2 Reviewed E-N01 source pack and Python panels | Day2 | M1; PREREQ-04; SPEC-001/003/004/006 | Actual synthetic source package, reviewed registrations and correct deterministic calculations/policy/risk artifacts |
| M3 Real fixture graph and necessary branches | Day3 | M1/M2; PREREQ-05; SPEC-002/005/007/008/009/011 | Executed normal, information, Conditional, correction and supported Reject paths with actual reports/history |
| M4 Six-screen command center | Day4 | M3; PREREQ-06; SPEC-010 and shared services | Usable source-linked Streamlit workflow with guarded actions and actual recorded status |
| M5 Notebook, local HTML and demo acceptance evidence | Day5 | M3/M4; PREREQ-06; SPEC-009/010/012 | Shared graph visualization, clickable offline walkthrough, source-linked sample memo and honest core QA/usability record |
| M6 Nebius Live integration | After relevant core proofs and explicit access/allowance; may fall outside five days | PREREQ-07; SPEC-006/007/011 | At least one authorized validated synthetic Live end-to-end review and actual usage evidence |
| M7 Selected RAGAS/hybrid experiments | Separate extension | PREREQ-08 and relevant verified core | Actual separately labeled evaluation/retrieval results; app remains DIRECT until an adoption decision |

Use E-N01 first, then the three core walkthroughs and existing correction/E-F03 variants. Authoring/executing all30 scenario designs, held-out quality, ten-case throughput and30-completion timing studies is not a prerequisite for M1–M5. A fixture cannot establish Live extraction/narrative accuracy or provider latency.

## M1 — Concrete first implementation milestone for approval

Outcome: a small importable, isolated Python foundation with real offline tests of the most failure-prone boundaries. It deliberately precedes a complete financial workflow; compatibility test graphs/records are APPLICATION_TEST evidence, not a second financial engine or an executed deal.

### M1 files and dependencies

Create only files needed by the tasks below, incrementally:

~~~text
README.md
AGENTS.md                          # reviewed draft activated with the actual M1 approval reference
pyproject.toml / uv.lock / .python-version
.gitignore / .env.example           # no populated key file or project LICENSE
config/app.toml / config/model.toml  # Fixture; Live/tracing disabled; model/rates unset
src/deal_or_no_deal_ai/
  __init__.py / configuration.py
  contracts.py / context.py / budgets.py / storage.py / review.py
tests/
  conftest.py
  unit/test_wire_contracts.py
  unit/test_context_identity.py
  unit/test_state_codec.py
  unit/test_review_basis.py
  unit/test_budget_boundaries.py
  integration/test_admission.py
  integration/test_checkpoint_compatibility.py
~~~

These names are planned implementation paths, not files already created. Add helpers only where needed; do not create the full proposed repository as empty placeholders. M1 does not create app.py, a full production graph/nodes/worker, PDF parser, registered case corpus, report/UI, providers/nebius.py, notebook or HTML. Existing docs/agents remains the only instruction source.

Approved-stack candidates for actual resolution: Pydantic, LangGraph, selected langchain-core, langgraph-checkpoint-sqlite and Streamlit; pytest in the development group, minimal setuptools build backend and Python standard-library JSON/Decimal/hashlib/sqlite3/concurrency helpers. Streamlit is resolved with the core foundation but screens/AppTest behavior is M4 work. HTTPX is added when its actual provider adapter is implemented; notebook/RAGAS/retrieval extras remain separate. Check compatibility and dependency terms at resolution; unresolved terms or incompatible APIs stop the affected task rather than select an unapproved alternative.

### M1 small tasks and verification

| Task | Dependencies / files | Behavior and meaningful checks | Linked coverage |
|---|---|---|---|
| M1-01 Establish the isolated foundation | M1 approval; root/configuration files above | Select installed3.12, resolve/lock dependencies, import package without provider/database/startup work; Fixture and tracing-off defaults; secrets ignored; no model auto-selection. Record actual setup result/version set | PREREQ-01/02; TEST-007-05, TEST-011-06 |
| M1-02 Implement strict external and wire/domain boundaries | M1-01; contracts.py, tests/unit/test_wire_contracts.py | INPUT-EDU-1.0 parsing before hydration; full extraction and synthesis wire shapes, strict types/extra keys, null/zero/conflict handling, exact confidence and logical refs. Reject injected raw_text/status/authority and nested duplicate keys. Hydrate synthetic test registries without claiming authored PDF provenance | SPEC-002/005/overview; TEST-002-04/07, TEST-005-01/03/06 |
| M1-03 Load bounded instructions and canonical identities | M1-02; context.py, test_context_identity.py | Exact allowlisted Runtime/shared sections and expected hashes; missing/ambiguous section fails. CANON-1.0 stable field/set/order/Decimal identity, scope checks, noncircular parent-content hashes; all-field narrative target identity. Serialize complete illustrative requests/schema/output and record actual UTF-8 component sizes. No token-fit claim without selected tokenizer/template | SPEC-006/005; TEST-006-01/04/05/08, TEST-005-03/04 |
| M1-04 Define exact primitive codec and application-owned storage | M1-02/03; contracts.py/storage.py, test_state_codec.py | STATE-CODEC-1.0 typed save/restore, exact confidence below0.7, score boundary, negative values, missing versus0, Unicode/refs and explicit null/[] clears. Reject unknown versions without pickle/downgrade/migration. Store operation identities/receipts and codec/schema version using temporary databases in tests | SPEC-011/overview; TEST-011-01/03, TEST-006-05, TEST-003-06, TEST-004-11 |
| M1-05 Prove shared execution admission | M1-04; storage.py, test_admission.py | Atomic single active key across two independent processes/connections using one resolved temporary DB. Exactly one contender starts a controlled operation; Busy rolls back acceptance/reservations and cannot record a disposition. Test duplicate reads, safe release, saved pause/reacquisition and explicit uncertain-claim recovery with no PID/time stealing | SPEC-007/011; TEST-007-05/06/07, TEST-011-02/03/04 |
| M1-06 Verify the actual saver/interrupt boundary | M1-04/05; test_checkpoint_compatibility.py | A minimal test-only LangGraph using the same primitive codec and SQLite file/table ownership: persist interrupt, close/reopen, resume same thread, preserve exact values. Exercise app receipt versus checkpoint gaps and idempotent own-operation recovery without a provider. Verify the pinned API; do not claim a transaction spanning app/saver commits | SPEC-008/011; TEST-008-04/07, TEST-011-03/04, TEST-007-02/06 |
| M1-07 Prove review-basis and condition-draft guards | M1-02/03/04; review.py, test_review_basis.py | Pure review snapshot/draft helpers plus scoped persistence tests: unchanged analysis with permitted handling advances gates; real source/support change invalidates; stale gate versions fail. Draft targets exist before required domain support, wrong-domain/unchecked edits fail, final prepared snapshot preserves target identity. This is contract/guard evidence, not the full E-P01 UI workflow | SPEC-008/005; TEST-008-02/03/06/07, TEST-006-05 |
| M1-08 Verify the correction allowance locally | M1-02/04; budgets.py, test_budget_boundaries.py | Same review ledger through simulated original/correction lineage; equality/overrun, one protected synthesis reserve and unknown usage never resets. Check current required-path tables and conservative reservations locally. Actual nine/eleven/seven/nine production-node instrumentation awaits M3; no provider-cost/timing claim from this trace | SPEC-006/007/011; TEST-007-03/06/08, TEST-006-08 |
| M1-09 Record results and unresolved decisions | M1-01–08; existing evaluation/PREREQ notes and relevant docs | Exact commands, dependency versions, test outcomes, scope/limits and failed attempts. Update only proven parts of prerequisites; leave parser, case packs, UI, exact provider tokens, Live and optional evaluations pending. A failing required check is not silently skipped | SPEC-011; TEST-011-07; PREREQ evidence record |

The test files may contain multiple parameterized cases under the existing90 planned TEST families. A subset passing in M1 does not mark a whole family complete when its production-graph/UI/provider assertions belong to later milestones. Use standard test data builders/temporary registries; do not copy evaluator gold into runtime context or create duplicate source packs under tests/.

### M1 setup and check commands

These authorized setup/test/build commands have now run successfully; exact results and scoped limits are recorded below:

~~~powershell
uv sync --python 3.12 --group dev
uv run --frozen --python 3.12 pytest tests/unit tests/integration
uv build --python 3.12 --no-sources
~~~

uv 0.12.23 supports the listed options; the local source/wheel build passed. Use Python3.12 explicitly and reuse the generated lockfile/frozen checks. Resolve/build only the local package; never publish it. Package downloads/cache access may require managed environment permission. No command may initialize a provider or use a present key as spending approval.

### M1 definition of done and checkpoint

- The listed foundation imports and builds under the resolved Python3.12 environment; actual versions/commands are recorded.
- The required scoped contract, codec, admission, real saver/interrupt, review-basis and budget tests execute successfully without provider/network work or hidden hosted tracing. The test harness intercepts outbound attempts even if provider/tracing environment variables exist; do not log their values.
- There is no unapproved schema weakening, silent skipped compatibility check, default provider, second database, duplicate instruction pack, pickle workaround, automatic claim expiry or budget reset.
- Root AGENTS.md truthfully records its activation and actual commands; no license, Git remote, paid service or external deployment is created. No claim of complete deal/Live/UI success is made from M1.
- Present a concise evidence-backed M1 result and any compatibility blocker before the next slice. License, model, paid allowance, scope/threshold and destructive-action decisions retain their explicit approval boundaries; do not repeatedly ask about routine choices within an approved milestone.

If compatibility fails, preserve the result and local files for inspection, leave affected paths unavailable and propose the smallest justified change. Rollback means returning to the prior document/config/source version or using disposable test databases—not deleting retained runtime sources/history/checkpoints. No recursive workspace reset is authorized.

## Later milestone implementation boundaries

| Milestone / small task group | Expected modules/files | Required tests/evaluations and checkpoint |
|---|---|---|
| M2-01 Resolve parser; M2-02 author/review E-N01; M2-03 implement FIN/policy/risk; M2-04 faithful segmentation/selection | documents.py, finance.py, policy.py, risk.py, retrieval.py DIRECT, context.py; config/sample_policy.json; fixtures/development/e-n01 sources/case/model-stage fixtures/gold | Parser-license/API decision before installation; TEST-001–004 and TEST-006-02/03; complete source/factor/date/authority registrations and golden arithmetic. Author numeric assumptions explicitly; no inferred factor grades or PD. Missing-data/conflict branches stay distinguishable |
| M3-01 Real graph/nodes/worker; M3-02 guarded commands/review; M3-03 correction/report; M3-04 core variants | graph.py/nodes.py/worker.py/services.py; extend budgets/storage/review/evidence/synthesis/extraction; memo.py and fixture provider; core case packages/variants | Actual graph count/handoff/receipt/stop invariants; TEST-005/007/008/009/011; E-N01, E-M01, E-P01, correction and E-F03 QA; high-level false-positive count offline. Current source/support/handling projections feed the report; no fake execution timeline |
| M4-01 Shell/read models; M4-02 intake/Workspace; M4-03 review/evidence/corrections; M4-04 Activity/Memo | app.py; ui/shell.py/dashboard.py/new_deal.py/workspace.py/activity.py/credit_memo.py; shared service projections; local theme config if needed | TEST-010-01–07 and source-safe rendering; all25 UI criteria plus current PREREQ conditions. Streamlit AppTest for interactions, separate manual keyboard/status/zoom checks. No duplicated financial/policy logic or ordinary risk-QA dashboard |
| M5-01 Shared graph notebook; M5-02 snapshot HTML; M5-03 core demo evidence | notebooks/01_workflow.ipynb, presentation.py, prototype/template.html/local assets; generated artifacts only under ignored var/ | TEST-012-01–06, actual fixture snapshot/memo lineage, UX-T01–05/MET-20 checklist. No remote renderer/assets, live upload simulation, second pipeline or deployment. Author self-assessment is labeled; optional unfamiliar-person feedback is separate |
| M6-01 Profile/readiness; M6-02 controlled adapter tests; M6-03 authorized Live smoke/workflow | providers/contract.py/nebius.py, HTTPX dependency when needed; model config/usage mapping; registered source support flows | Exact model/schema/tokenizer/rates and explicit allowance before dispatch. PROVIDER-1.0 mocks before funded work; full-context/ordinary/Conditional/correction fit; at least one actually validated synthetic Live run, with all attempts/usage and required human checks recorded. No automatic full-corpus/timing/held-out workload |
| M7-01 selected RAGAS adapter; M7-02 native/report projections; M7-03 selected retrieval experiment | lazy ragas_evaluation.py, evaluation.py/config/evaluation.toml; optional retrieval_benchmark.py/config/annotations/dependency groups | Existing protocols and TEST-006-09/011-07/007-05–07; one shared custom bundle versus separately counted native work, frozen actual context and gold separation. No package/model default or download at startup; no universal aggregate or automatic app retrieval adoption |

M7-03's user-authorized implementation sequence is now explicit: wait for reviewed source documents and the ten frozen development queries, implement/report DIRECT coverage and KEYWORD/VECTOR/HYBRID comparisons, then inspect actual ranking failures before considering a separate reranker. VECTOR-only is the semantic retrieval baseline and RRF is rank fusion. Record each component's specified/implemented/tested/measured status and the existing MET-23 results before any conditional follow-up. Use [the benchmark decision](evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision) for candidate-pool diagnosis and quality versus added-processing evidence. A later reranker is not a fifth initial arm or part of the existing80-selection workload; its bounded experiment/model/setup/work must be selected separately. No new execution-task/TEST/MET ID, core day allocation, automatic download, paid call or app-strategy switch follows from this planning addition. RAGAS remains an independent optional evaluator, not the semantic retrieval baseline.

Module names follow the repository proposal; split only when a real responsibility/size requires it. M2–M7 task IDs are execution-plan IDs, not new TEST/MET definitions. Review the produced artifacts at each checkpoint; new business rules, dependencies/providers/licenses, paid runs, publication and destructive changes require their existing decisions rather than being inferred from this roadmap.

## Measurement implementation

### Event ownership and safe properties

Use SPEC-011's common envelope: event ID/name, scoped workspace/deal/review/run refs where applicable, input revision, operation/stage/task, mode, schema/config versions, UTC timestamp and per-run sequence. Events come from the service that commits the actual effect, with append-once identities. A widget rerender/duplicate receipt is not another execution. Ordered sequence defines report cutoff; the report-generated event cannot be inserted into its own earlier audit snapshot.

Use the canonical event names below instead of emitting older PRD proposal aliases such as document_validation_completed or evidence_opened alongside their accepted equivalents. This chooses consistent instrumentation, not new product behavior:

| Event(s) | Trigger / owner | Additional safe properties |
|---|---|---|
| deal_created; package_validation_completed; source_committed | Intake service commits the respective effect | Completion scope, file/page/byte counts, validation/reason code, source/digest refs; no filenames/text/borrower name |
| review_started; stage_started/completed/failed | Worker/node boundary actually begins/ends | Stage status, duration, controlled error code, artifact refs; no invented progress |
| handoff_dispatched/accepted/rejected | Actual typed stage artifact handoff | Sender/recipient, contract version, artifact/dependency refs and outcome |
| provider_attempt_reserved/completed/unknown | Budget/provider boundary records reservation and actual outcome | Attempt/request refs, certainty, finish classification, actual/estimated/unavailable usage, input/cached/billed-output counts, dated rate ref and conservative cost/reservation |
| decision_route_computed; review_requested; review_paused/resumed/skipped | Routing/review service records actual route, pause or permitted resume | Control/referral refs, required owner/tier, gate version, pause kind data-quality/information/credit and reason category; no score/condition text |
| exception_disposition_recorded; credit_risk_review_recorded; semantic_assessment_recorded; disposition_recorded | Respective guarded command commits once | Scoped issue/target/receipt/draft refs, target kind, permitted outcome/category/tier and record version; no free-text explanation |
| correction_recorded; artifacts_invalidated; issue_metadata_updated | Corrected revision or metadata command commits | Revision/affected artifact refs and category; no before/after financial values or notes in ordinary telemetry |
| report_generated; report_superseded | Actual artifact persistence/supersession | Template/input/cutoff refs, render kind, completeness; no report content |
| budget_stop; review_cancelled/completed; recovery_required; operation_reconciled; storage_error | Actual confirmed stop/end/recovery/storage outcome | Safe reason, limit/counter/receipt refs; cancellation request cannot pretend remote work stopped |
| screen_viewed; deal_opened; source_opened; action_requested; action_denied | Intentional UI navigation/inspection/command request or service denial | Screen/action/source IDs, current revision/mode and safe denied reason. Do not count every Streamlit rerender as an intentional view |
| usability_task_completed | End of an explicitly observed task attempt, including failure | UX task ID, outcome, duration, help/error categories and screen only. Manual click/role/repeated-open counts and categorical friction remain local QA notes, not a new telemetry stream |
| evaluation_result_recorded | Explicit evaluation run persists a result | Evaluation kind/origin/config/sample refs, scored/attempted/excluded/failed counts and status; full quotes/scores/examples remain in scoped results, not routine events |

Condition-draft/support mutations use existing operation/target records and semantic-assessment/command events; no new high-cardinality text event is introduced. All new event/property implementation must match the accepted feature contract; an alias is mapped deliberately rather than double-counted. The definition of action_requested is intent, not command acceptance, paid dispatch, approval or completion.

### Metrics, calculations and honest baselines

The [evaluation plan](evaluation/evaluation-plan.md#metrics-and-release-acceptance) remains the source for all23 MET definitions/targets/denominators. Implement the following calculations from actual artifacts/events or explicit human scoring; never infer success from a populated card or empty result set:

| Metric group | Implementation / observation | Baseline and target treatment |
|---|---|---|
| MET-01/02/05 arithmetic, policies, typed validity | Deterministic harness and accepted/raw-invalid attempt records | Proposed100% controlled correctness/accepted validity; current application result Not run. Invalid attempts remain visible |
| MET-03/04/06/07/08 extraction, missing/conflict, risks and evidence | Freeze original outputs; score against reviewed independent source labels with field/claim/issue denominators and support review | Retain existing thresholds and demo critical gates; Fixture proves controlled workflow only. No baseline or measured Live percentage yet |
| MET-09/10/13/14 routes, reports, core outcomes and isolation | Guard/report assertions and actual run/receipt lineage; expected information pause counts as correct behavior | Existing100% relevant controls and3/3 core plus both QA variants; two-deal isolation core. Unrun30-case/ten-case extensions are not Passed |
| MET-11/18 work and cost | Sum every actual attempt and durable reservation across review/correction lineage; cost = uncached_input*dated_input_rate + observed_cached_input*dated_cached_rate + billed_output*dated_output_rate, divided by the rate unit | Existing8,000/2,000 cumulative tokens, five attempts,20 nodes/12 tools, USD0.10 target/0.25 hard and time caps. Missing/contradictory usage retains conservative reservations; no fabricated zero or guaranteed cache discount |
| MET-12/17 validated Live and latency | Count actual validated Live completions. Sum active processing intervals separately from human waiting; use prescribed nearest-rank p95 only when the existing30-completion protocol is actually selected/met | At least one authorized Live demonstration;90s p95 is a proposed extension target,180s active hard limit. No timing or model-quality claim from installed versions, Fixture timing or one smoke run |
| MET-15/19/20 interface, task success and learning | Actual notebook/HTML/UI checks, five explicit task attempts and separate learning checklist | Core25 UI criteria and5/5 tasks/learning with stated limitations. Preserve failures/help; no task-time saving claim. Self-assessment is not external-user validation |
| MET-16/21/22 narrative, context optimization and false positives | Human original-output rubric; actual context size/profile feasibility; high-level deduplicated false-positive count | Existing mean4/5/no critical-error narrative target where scorable; no observed savings; false positives reported offline with recall, not another UI card |
| MET-23 and separate RAG-R/native scores | Only explicitly selected retrieval/RAGAS runners over frozen inputs | Not run until enabled and executed; native scales/variants/statuses remain distinct from custom1–5 and financial scores. No universal blended score or assumed hybrid winner |

A zero denominator is Not measured/Not applicable with a reason; it is never100%. Separate dev/held-out, original/reviewed, Fixture/Live and actual/estimated/demo values. Numerical sample values in docs are illustrative until tied to actual scoped artifacts. Current business baseline, analyst time saved, adoption, revenue and real loan-outcome benefit are unknown; educational proxies remain task/learning/workflow evidence.

### Results and dashboard boundaries

- Dashboard: stored five-column deal list and compact status counts, scoped to the current filter/revision. No fabricated activity or new product-QA dashboard.
- Workspace/Memo: current financial assessments, every mandatory blocker, source/calculation/rule drill-down and guarded next action. Quantitative risk, policy exceptions, missing evidence, AI confidence and completion remain separate.
- Activity: actual current/last stage and wait/stop/recovery first; expanded counters/context/cache and existing instructor/developer evaluation expander. Show four native RAGAS rows plus five custom dimensions/status/examples when inspecting saved quality results; opening it dispatches no scorer.
- Prerequisite/evaluation record: local scoped notes/results under the existing ignored var/evaluations boundary when implementation exists. Record actual procedure, versions, attempted time, result/limitations, evidence refs and reviewer. No event page is proof that a pending check passed.

### Privacy and retention

Ordinary logs/events never include credentials, raw prompts/responses/source/report text, borrower fields, factor ratings, conditions, operator notes/search text, request headers or provider error bodies. Synthetic source/quote/model artifacts remain separately scoped inspectable content; do not dump full graph state into logs. Hosted tracing remains disabled until explicitly approved, including when environment flags happen to exist. Persisted data/history/checkpoints have no automatic expiry; test data uses isolated temporary storage. Manual deletion/reset requires an explicit request and reviewed targets. Notebook/HTML contains no keys or remote analytics/assets; executed notebook outputs stay local/ignored.

## Risks, stop conditions and rollback

| Risk | Stop / response |
|---|---|
| Dependency/saver/codec behavior differs from assumptions | Preserve failed compatibility evidence, keep dependent features unavailable and propose the smallest version/adapter change; no pickle or weaker schema workaround |
| Parser license/API remains unresolved or loses essential layout | Stop before parser adoption/trusted complete extraction; retain originals and missing-context reasons. M1 pure-contract work does not require a parser choice |
| Source/factor/date/authority configuration incomplete | Keep the case unregistered/partial; no borrowed grades, fabricated citations or final-ready report |
| Faithful request/correction cannot fit verified profile | Stop before dispatch; improve lossless representation/reallocate within current caps or narrow supported source package. No hidden truncation or budget increase |
| Busy, duplicate, stale or uncertain execution | Use atomic admission/receipts, preserve reservations/history and explicit recovery. No background replay, claim stealing, invoice assumption or reset |
| Edited conditions/review support mismatched | Keep the request pending with exact owner/action; prepare/support the actual targets before disposition. Do not create a self-approval loop |
| UI/framework does not implement proposed styling/accessibility behavior reliably | Prefer accessible native controls and readable flow, retain critical meaning and record limitations; avoid fragile internal DOM overrides or a new frontend framework |
| Five-day target becomes unrealistic | Report remaining scope honestly and replan the smallest slice; retain critical controls and separate optional/Live work. No production-readiness or broad savings claim |

## First milestone approval gate

Historical pre-scaffold documentation verification on 2026-10-23: 49 active Markdown documents, 535 local links and 109 anchor links checked with no missing targets; all four illustrative JSON blocks parsed. The inventory remains 90 unique planned TEST IDs, 23 core MET IDs, 25 UI criteria, five UX tasks and eight prerequisites; M1 contains nine tasks. These are static documentation checks only. At that earlier check the root contained only docs/; this historical observation is superseded by the current M1 evidence.

M1 authorization and its scoped successful setup/tests/build are recorded; do not request that authorization again. M2 is the next planned slice: reviewed synthetic sources, calculations, sample policy/risk panels and faithful selection. Parser licensing and reviewed case configuration must be settled before their affected implementation. Paid calls, optional services, publication/deployment and destructive changes retain their existing boundaries. A foundation pass does not establish a complete deal workflow.

## M2 registered deterministic panels evidence

Evidence date2026-10-23. Type APPLICATION_TEST; actual pypdf/source checks and Python panels, with a registered authored default extraction fixture. This is not yet EXECUTED_FIXTURE full-graph or Live/model-quality evidence.

Implemented config/registrations/e-n01.json and config/sample_policy.json; services.py exact-case loader, current parsed inventory and trusted fixture qualification; finance adapter with input values/bases/source refs and limitations; policy.py fixed handlers/traces/three-state review-trigger group; risk.py approved factor aggregation, band/referral and linked numerical flags. Actual UTC observation/cutoff is recorded separately from the approved2026-10-23 business review date, without backdating availability from manuscript dates. Source-fit approval is scoped to this exact fictional case/profile, not an external authority hierarchy.

The offline entry point tools/run_e_n01_panels.py now reads the three actual registered PDFs/five pages and validates current page/source hashes, instruction versions, exact metadata/output/default variant and scope/period/units/field authority before dependent arithmetic. It reads no gold or authoring manuscripts. Changed source/policy/basis/scope/unregistered extraction or Live mode is rejected; it never borrows an answer or falls back to another provider.

Observed results: EBIT900,000; EBITDA1,100,000; post-loan debt3,300,000; DSCR1.50x; leverage3.00x; equipment LTV60%; projected growth10%; current ratio2.00x; interest coverage9.00x. The authored ratings20/25/20/15/30 contribute6/5/4/3/3 for21/100, Low. Four numerical sample checks pass; required source prerequisites are satisfied; KYC/sanctions are explicitly Not applicable under the fictional config. Policy exceptions0, missing material evidence0, false-positive risk flags0 for this normal case; risk recall is N/A because there are no positive labels. These are exact-case diagnostics, not population performance or a grade inferred from ratios.

Confidence remains NOT_EVALUATED/AWAITING_VALIDATED_SYNTHESIS; its control is distinct from policy outcomes. Amount/confidence OR grouping is three-state and independent score/policy/evidence gates remain intact. Policy completeness is PRE_SYNTHESIS; final_ready=false and final_decision=null. Covenants remain EXTRACTED_NOT_EVALUATED; concentration NOT_ASSESSED; full-term/balloon/refinancing and reported-EBITDA reconciliation remain unassessed/deferred. All facts are registered Fixture provenance, not Live HUMAN_SUPPORTED.

Ten new policy/risk unit methods and six registered-panel integration methods passed with the previous suites: **85 methods passed**, zero failures/errors/skips, final headline2.54 seconds. Tests cover numerical equalities/adjacent breaches, inclusive amount/exclusive exact confidence, retired003 absence, required/unresolved controls, invalid/missing factor/material inputs, continuous unrounded score bands, correct owner/tier, exact gaps, scope/date/unit/source/policy/stage tampering, no gold/manuscript reads and complete dependency closure. Unit-modified inputs are APPLICATION_TEST probes, not registered alternate loan scenarios or correction variants. No whole planned TEST family is certified complete.

Executed commands:

~~~powershell
.\.venv\Scripts\python.exe tools/run_e_n01_panels.py
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/m2-registered-panels-pytest.xml
~~~

Ignored reports: var/evaluations/e-n01-deterministic-panels.json, m2-registered-panels-pytest.xml and m2-registered-panels-completion.json. Earlier43/55/66/69-method reports and source drafts remain retained. No new dependency, runtime prompt/hash, model call, UI, full graph, memo, external repository, deployment or project license. Parser-only QA deliberately leaves approval/registration unknown; use CASE-REG-1.0 resolution for current source/assessment permission.

Remaining M2/M3 boundary: the registered exact case and deterministic panels work; RET-1.0 ContextPacket/provider-token preflight integration, synthesis-stage/current-input registration, persisted graph/worker/gates/receipt/correction/report flows and other core cases remain. Generic upload/source selection and Live human support remain unimplemented. Next implement the shared E-N01 fixture graph and source-linked report with actual node/tool/usage instrumentation, then the required information/Conditional/correction/Reject branches. No fresh approval of unchanged A1-A4 or pypdf is required.

## M2 parser installation and PDF verification

Evidence date2026-10-23. Type APPLICATION_TEST, actual local pypdf extraction over the E-N01 draft. User-approved [ADR-006](architecture/decisions/006-proposed-pdf-parser.md) is accepted for this scoped parser choice. `uv add pypdf --python 3.12` resolved/installed6.21.2 and updated pyproject.toml/uv.lock. Installed metadata states BSD-3-Clause; the installed license digest is recorded. The initial sandbox cache denial was resolved through the permitted escalated install, not bypassed.

Actual `tools/verify_e_n01_pdfs.py` results: three PDFs/five actual pages, all PASS for complete ordered nonblank-line comparisons in both plain/layout modes. Only blank lines/trailing spaces are ignored; inner spacing and every character/value remain checked. Six focused diagnostics PASS: year columns/revenue mapping2026=4,000,000 and2027=4,400,000; whole-USD units; explicit annual projections; cross-page continuation; full debt-service qualification; documented zero liens. Layout positions are character offsets, not invented glyph boxes. Raw plain/layout outputs and real parsed-page inventory are saved separately from source authoring maps.

The first run correctly failed: two pages had apostrophe differences because the fixed PDF writer omitted explicit font encoding. A diagnostic also matched the later Revenue growth prose as a table row. The writer now declares WinAnsi encoding; the diagnostic uses the actual table section and rejects ambiguous/straddling columns. Technical draft2 changes only binary font encoding and source/version hashes, not financial text/assumptions. The thirteen original draft files remain under fixtures/development/e-n01/history/1-draft; initial failed report and ten raw outputs remain under var/evaluations/e-n01-pdf-verification-v1. No deletion or automatic expiry occurred.

Three new parser integration methods check real extraction/punctuation/qualifications, rejection of changed bytes before parser execution, and header-based column assignment with missing/duplicate/straddling negative cases. Combined suite: **69 methods passed**, zero failures/errors/skips, final headline9.20 seconds. This is test duration, not app/provider latency. Draft source-fit flags stay false: both BASELINE/ADAPTIVE have measured parser fidelity but retain UNVERIFIED/no dispatch due to SOURCE_FIT_UNVERIFIED. A1-A4, semantic HUMAN_SUPPORTED, registry and final decision remain unset/unapproved.

Executed successful commands:

~~~powershell
uv add pypdf --python 3.12
.\.venv\Scripts\python.exe tools/prepare_e_n01.py --check
.\.venv\Scripts\python.exe tools/verify_e_n01_pdfs.py
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/m2-parser-pytest.xml
~~~

Ignored evidence: var/evaluations/e-n01-pdf-verification/report.json and its ten raw text outputs; m2-parser-pytest.xml; m2-parser-completion.json. Verification is restricted to exact known writer-generated bytes; altered files stop before parsing. It is not arbitrary upload acceptance or a generic financial table extractor. Scanned/malformed/decompression/time/resource controls and representative unfamiliar real layouts still need their intake slice. No visual PDF rendering, generalized parser-fidelity claim, approved bank assessment, complete graph, UI, model call, RAGAS or retrieval benchmark is implied. Earlier43/55/66-method evidence and uncorrected sources remain retained.

Next: obtain the case-assumption review/approved source profile, bind the exact current source/config digests, implement trusted context/financial/policy/risk service integration, then the M3 fixture graph. Parser installation permission need not be requested again. Generic upload and provider paths retain their separate prerequisite checks.

## M2 source candidate and arithmetic evidence

Evidence date2026-10-23; type APPLICATION_TEST / AUTHORING_DRAFT. The first bounded M2 slice is implemented, not the full milestone.

| Work | Actual artifact/result | Remaining boundary |
|---|---|---|
| Prepare E-N01 | [Candidate and A1-A4 assumptions](../fixtures/development/e-n01/README.md); five manuscripts, three deterministic PDFs/five authored pages, byte digests, page/paragraph authoring maps, draft case metadata and schema-valid extraction candidate | Source/manuscript authoring is not PDF parsing, professional review, source-fit verification or registration. Flags remain false; no final PanelDecision |
| FIN-1.0 arithmetic | src/deal_or_no_deal_ai/finance.py: all nine calculations, exact threshold helper, precision50 and ROUND_HALF_UP display; no provider calls | Internal kernel only. Public trusted compute_financials, source/period/support integration and FinancialPanel remain pending |
| Regression checks | Nine finance methods plus two candidate-integrity/nonapproval methods; combined suite66 methods passed, zero failures/errors/skips in13.20 seconds | TEST-003 arithmetic subsets, TEST-001-04/005-03/006-03/05 integrity subsets; whole test families not complete. Duration is not app latency |
| Parser choice | [ADR-006 proposal](architecture/decisions/006-proposed-pdf-parser.md) records official sources, recommendation and trade-offs | pypdf proposed under BSD-3-Clause terms; no package added, version selected, parser run or automatic PyMuPDF replacement |

Executed commands:

~~~powershell
.\.venv\Scripts\python.exe tools/prepare_e_n01.py --write
.\.venv\Scripts\python.exe tools/prepare_e_n01.py --check
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/m2-candidate-pytest.xml
~~~

Independent authored gold reproduces EBIT900,000; EBITDA1,100,000; funded debt3,300,000; DSCR1.50x; leverage3.00x; equipment LTV60%; projected revenue growth10%; current ratio2.00x; interest coverage9.00x. These are deterministic results from the candidate's supplied normalized inputs, not values extracted by a parser/LLM or a verified borrower assessment. Tests also cover exact threshold-adjacent comparisons despite identical rounded display, missing versus explicit zero, negative CFADS/EBIT, nonpositive denominators, liens/repayment once, invalid signs and bounded maximum precision/repeating division.

The candidate's A1-A4 add proposed dates/bases, use-of-proceeds/detail, fictional assessment premises and individually authored ratings20/25/20/15/30. They are not new bank rules, automatic ratio-to-score mappings or approved usable assessments. Evaluator-only gold is separate; no runtime handler imports it. An integration check supplies all authoring blocks to DOCVERIFY and confirms UNVERIFIED/no dispatch in both modes while fidelity/source-fit are unverified.

Ignored evidence: var/evaluations/m2-candidate-pytest.xml and m2-candidate-completion.json. Prior43/55-method reports remain retained. No lockfile/dependency, runtime prompt/hash, source-policy threshold, provider allowance or application retrieval mode changed. No full parser/loan graph, report, UI, notebook, HTML, live model, RAGAS/hybrid benchmark or refreshed package build is claimed.

Next checkpoint: user approval of the concrete parser proposal and A1-A4. Then install/verify the selected parser, parse and compare the actual five source pages, complete reviewed source/basis/factor registrations and trusted finance/policy/risk/context integration, before the M3 fixture graph. Keep review/case approval attributable and exact-digest-bound; a positive reply is not a claim of professional financial validation.

## Document verification extension evidence

Authorization and evidence date: 2026-10-23. The user requested applying the unfamiliar-layout/year-column/cut-off-context checks. [DOCVERIFY-1.0](specs/context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10) was specified before implementing the bounded parser-independent portion. This does not complete M2, select a parser or change the graph/default retrieval/model allowance.

| Step | Implemented files / existing contracts | Observed outcome and remaining boundary |
|---|---|---|
| Define checks | SPEC-001/006, PRD grounding, HLD data flow, intake/evidence instructions | Explicit scope, geometry/period, original-location and dependency rules; no new business formula or threshold |
| Implement checks | src/deal_or_no_deal_ai/documents.py | Typed parsed-block/table helpers, source allowlist, row-label/year/unit/cell references, dependency closure, safe BASELINE and opt-in ADAPTIVE, byte/work stops and packet identities. No PDF parser, semantic support or provider dispatch |
| Test controls | tests/unit/test_document_verification.py; tests/integration/test_document_verification.py | Eleven unit methods and one paired integration method extend TEST-001-04 and TEST-006-02/03/05/07. Combined suite:55 methods passed, zero failures/errors/skips; final run2.87 seconds, not app latency |
| Compare fixed inputs | tests/document_verification_cases.py; tests/compare_document_verification.py | Fourteen synthetic parsed cases,28 paired executions, zero check failures. Gold labels are outside helper inputs. BASELINE4 complete/10 withheld; ADAPTIVE5 complete/9 withheld. One disclosure restores its existing qualification/definition; absent or unverified context remains withheld |

In that disclosure case the measured packet sizes were675 BASELINE bytes and1315 ADAPTIVE bytes. This is added source context, not a claim of token savings. Per-case report records actual local duration, input identity, value/period/units/source, original pages/text, status, expansion and failures. It is APPLICATION_TEST evidence, not model accuracy, RAGAS, vector/hybrid retrieval, PDF parsing or a new registered loan scenario. Durations are single local observations, not p95/provider latency.

Actual successful commands:

~~~powershell
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/unit tests/integration --junitxml var/evaluations/document-verification-pytest.xml
.\.venv\Scripts\python.exe -m tests.compare_document_verification
~~~

The first run passed with a sandbox pytest-cache write warning; the final run disabled that optional cache and passed without warnings. Existing M1 evidence remains retained. New ignored reports: var/evaluations/document-verification-pytest.xml, document-verification-paired.json and document-verification-completion.json. The prior package build predates this helper; no refreshed package build is claimed by this extension.

Remaining order: resolve the existing parser-license/API checkpoint; author/review the actual E-N01 sources and source/factor/subject registrations; adapt parser outputs into the original-block inventory; integrate DOCVERIFY with faithful DIRECT ContextPacket/full-request preflight; test real parser layouts and later authorized Nebius outputs on identical questions. Numeric formatting normalization and undeclared-dependency discovery remain adapter/review responsibilities. Neither synthetic control success nor a supplied fidelity flag establishes those checks. Keep adaptive opt-in until that representative paired comparison supports adoption. No installation, model download, LLM call or paid service occurred in this extension.

## M1 implementation evidence

Evidence date: 2026-10-23. Origin: APPLICATION_TEST, scoped M1 foundation. Dependency installation succeeded after the user explicitly permitted retrying it. The prior34-method stdlib result and earlier rejected-install record remain preserved in var/evaluations/m1-foundation.json; they are historical, not the current blocker.

Current result: **43 pytest-collected methods passed, zero failures/errors/skips**. These include eight wire/schema/hydration methods and the actual LangGraph SQLite saver method with normal and committed-receipt/pre-resume recovery variants. JUnit expands unittest subtests into101 reported cases; this is the same suite, not101 new feature tests. The final pytest headline was3.13 seconds; test duration is not application latency. The90 planned TEST IDs and all product-quality targets are unchanged; a passing scoped method does not complete its whole feature family.

| Task | Executed M1 evidence | Later work deliberately outside this proof |
|---|---|---|
| M1-01 environment/configuration | uv resolved the approved dependencies into .venv and wrote uv.lock; current configuration and a fresh import check passed with network/database blocked and synthetic tracing flags enabled | Provider/parser/notebook/evaluator configuration; no hosted service is connected |
| M1-02 strict wires/domain | All eight Pydantic methods passed: complete examples, exact numeric confidence, missing/conflict handling, scoped references, unauthorized fields and all narrative fields. Positive requested amount is now enforced and zero/negative cases are covered | Complete registered source manifests and production stage/artifact integration are later; hydration does not confer semantic support |
| M1-03 bounded context/identity | Fixed instruction hashes, allowlisted Runtime/shared sections, canonical identity and actual schema/response byte measurements passed | Synthesis measurement uses illustrative handles, not a complete grounded case packet. Actual complete-case/tokenizer/template/token-budget fit remains pending; no bytes-to-tokens claim |
| M1-04 codec/storage | Exact confidence/Decimal/null/negative/Unicode round trips, reopen, explicit stale clears, version rejection and retained record history passed | This snapshot is the M1 typed compatibility record, not the full future deal state |
| M1-05 admission | Actual two-process contention admits exactly one; Busy/stale transaction rolls back writes/reservations; duplicate receipts cannot dispatch; unknown claims/reservations survive | App/notebook/evaluation entry-point wiring and production worker dispatch belong to later slices |
| M1-06 actual saver/interrupt | Real installed saver paused, closed/reopened, resumed its own accepted record and preserved exact state. Recovery variant retained one disposition | This is APPLICATION_TEST graph evidence, not an executed financial workflow or immutable audit storage |
| M1-07 review basis/conditions | Pure guard tests passed for valid handling progress, stale analysis/gate, tier, mixed-domain draft support and own-receipt consumption | Complete transactional domain commands, final condition semantics and screens are later |
| M1-08 cumulative allowance | Reserve/settle/restart, exact equality/overrun, protected correction, unknown usage, stored-spend integrity and bounded path previews passed | Actual production-node counting, provider timeout/retry behavior and real billed usage remain pending |
| M1-09 evidence/build | Exact versions/commands/results saved; local source and wheel build succeeded after the final source/README change | No license/publication/deployment, full deal, UI, model-quality, RAGAS or hybrid result is implied |

Actual successful commands:

~~~powershell
uv sync --python 3.12 --group dev
uv run --frozen --python 3.12 pytest tests/unit tests/integration --junitxml var/evaluations/m1-foundation-final-pytest.xml
uv build --python 3.12 --no-sources
~~~

| Component | Actual tested version | Declared package license metadata inspected |
|---|---|---|
| Python / sqlite3 library | 3.12.15 / 3.53.1 | Interpreter/library observations, not a project license |
| Pydantic | 2.14.1 | MIT |
| LangGraph | 1.2.16 | MIT |
| langchain-core | 1.7.0 | MIT |
| LangGraph checkpoint / SQLite saver | 4.3.0 / 3.1.2 | MIT |
| Streamlit | 1.66.1 | Apache-2.0 |
| pytest | 9.1.1 | MIT |
| Isolated wheel build generator | setuptools84.2.1 | Build metadata version recorded; no project license selected |

uv.lock contains the resolved package graph; use frozen runs rather than independently reinstalling versions. LangSmith's SDK and sqlite-vec are transitive dependencies of selected packages; their presence does not enable hosted tracing, a vector index or an embedding/model service. The optional langsmith_plugin pytest integration is explicitly disabled. The separate import check found zero network/database attempts with synthetic enabled tracing flags. No real credentials were requested/read into reports.

Ignored local evidence: var/evaluations/m1-foundation-completion.json, m1-foundation-final-pytest.xml and m1-context-bytes.json. Earlier evidence/XML remains retained. These record actual versions, source/lock hashes, commands, raw JUnit counts and limitations. Local artifacts: dist/deal_or_no_deal_ai-0.1.0.tar.gz and dist/deal_or_no_deal_ai-0.1.0-py3-none-any.whl. They require the reviewed checkout for prompts/configuration; no self-contained app or external deployment is claimed.

Context byte observations: extraction instructions4724/schema9585/illustrative source registry1567/response2641; synthesis instructions5470/schema2800 with illustrative responses794 or1039. These are measured UTF-8 component sizes, not token counts, verified provider requests or full grounded synthesis packs. Real tokenizer/template and complete-case fit remain required before Live use.

Preserved failures/limitations: the sandboxed uv test invocation needed cache permission; a build-artifact read needed permission; the evidence-authoring script initially called SQLite's version string as a function and was corrected. None changed the passing application results. Package installation/tests/build were explicitly authorized. No complete loan graph, PDF parser, reviewed case pack, UI/notebook/HTML, actual model call, paid evaluation, external repository or deployment ran. M1 foundation checks are complete; subsequent prerequisite scopes remain pending.

## Executed LIVE-GRAPH-1.0 verification - 2026-10-24

- Full regression: 261 tests and 269 subtests passed in 148.98 seconds;
  report: var/evaluations/live-graph-final.xml.
- Following the final fact-versus-narrative check refinements and durable exact
  paid-request snapshots: 13 focused live graph/transport/readiness/native-ID
  checks passed in 31.58 seconds; report:
  var/evaluations/live-transport-checkpoints-final.xml.
- Four known pinned-RAGAS public-API deprecation warnings remain; no skipped
  or silently substituted provider results were used as model-quality evidence.
- Actual shared LangGraph/SQLite checkpoint tests use mocked Nebius transport.
  They cover fact/narrative pauses, domain/role/source/target/check rejection,
  missing material data, separate low-confidence credit approval, duplicate
  read without new calls, no fallback on timeout, retained uncertain spending,
  setup-verification pause without spending and explicit UI metadata-only review.
- Explicit local readiness check: key absent; provider model/schema/current rates
  and whole-request fit unverified. Local components still 3699/2282 tokens.
  No actual Nebius generation/embedding/judge request or paid cost occurred.
- Existing saved-response paths remain available. Arbitrary-upload financial
  onboarding, live source correction/exception conditions and LLM-based RAGAS
  are not represented as completed by these checks.
