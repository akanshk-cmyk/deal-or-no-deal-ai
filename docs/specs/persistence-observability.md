# Local Persistence, Audit, Diagnostics and Evaluation Results

**Upload retention:** UPLOAD_PACKAGE uses existing app_records/global admission;
original PDFs use content-addressed scoped ignored var/uploads paths. Reads check
workspace, package identity/digest, bytes and page hashes/locators. File/DB gaps retain
recovery, never auto-replay/delete. Upload library is separate from financial deal
permissions. See [UPLOAD-1.0](upload-inspection-integration.md).

**Correction persistence:** Existing app_records stores scoped SOURCE_CORRECTION
draft/READY context/outcome and frozen financial-history events atomically with
parent supersession/shared-ledger version update. READY means no execution claim or
checkpoint yet; explicit Update atomically admits one worker. Idempotent duplicates
return the original revision. Unknown dispatch gaps retain recovery state with no
automatic retry. Original checkpoint/artifacts remain historical. See
[CORRECTION-1.0](source-correction-integration.md).

**E-P01 durable events:** Existing app_records/admission transactions retain separate
exception/preparation/support/final events, scope/version/gate/source binding and
frozen original snapshots. Graph checkpoints carry compact snapshot-digested
receipts. Current gates/draft are reconstructed from actual events on reads/resume;
memo independently validates accepted condition targets. No new table/DB, expiry,
reset, immutable-storage claim or paid tracing. See
[CONDITIONAL-1.0](conditional-integration.md).

Feature ID: SPEC-011
Version: 1.10
Status: SQLite state, checkpoints, recorded events, scope guards and recovery admission implemented; local history is not tamper-proof; distributed infrastructure out of scope
PRD requirements: FR-001–003, FR-007–012, FR-014–020; PRD memory/privacy and NFRs
Role instructions: [Shared contract](../agents/shared-contract.md), [Orchestrator](../agents/orchestrator.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

The current LOCAL_FILE inspection slice writes explicit source/report observations under ignored var/reference-inspections and creates no database/schema/index. Package installation and95 passing application methods do not complete the planned vector persistence work. Local observation timestamps/content hashes are not an immutable audit store or verified source origin. Keep the future additive schema and complete-build checks pending.

Accepted public-reference extension: [ADR-007](../architecture/decisions/007-proposed-public-financial-rag.md) and the [source/vector contract](public-financial-sources.md) select app-owned source-observation, passage, embedding and index-build records in the same SQLite boundary, with bounded exact cosine ranking. No schema migration/tables/model download are implemented. Implement an additive versioned app-schema change and test existing records/checkpoints/history before enabling the feature; never edit checkpointer-owned tables or reset the database to upgrade. Public snapshots/index artifacts remain ignored local data, distinct from synthetic fixtures. Validate complete builds, dimensions/model/tokenizer revisions and source eligibility; no installed ANN extension or separate service is claimed.

A learner can inspect saved synthetic artifacts, progress and usage; resume a known pending review safely; and distinguish application tests, fixture runs and live evaluations. One SQLite boundary, no hosted tracing dependency or claimed immutable audit.

## Workflow and rules

DECISION-HISTORY-1.0 / [SPEC-013](decision-history.md) reuses existing app_records/history with no schema change. New review events store previous/new status, trusted simulated display name and DECISION-SNAPSHOT-1.0 with pre-action deal/AI/risk/policy/source context. Older events are not rewritten; recover context only from their exact saved expected_record_version when available, otherwise Not captured. Current deal status remains separate. Queries/filter/timeline/export use consistent read snapshots and scoped counts with no writes or initialization. CSV snapshot identity includes actor scope, filters and returned event content; stale views cannot export. Preserve all original artifacts/checkpoints and no-expiry behavior; neither snapshots nor export imply immutable audit storage.

REVIEW-UI-1.0 uses existing app_records/app_record_history in the configured SQLite database for isolated ILLUSTRATIVE_UI_ONLY review requests and immutable-by-command event rows. Each action atomically writes its event and versioned review projection, with role/scope/tier/basis checks, duplicate-operation handling and application UTC time. No tables/schema, financial checkpoint, provider ledger or normal Fixture artifact is changed. This is retained local history, not immutable storage. The preview adapter never creates a real HumanDisposition or resumes a graph. See [the action contract](human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10).

P3-03 proposes one application process, a single user-started execution worker and serialized mutations/single active execution. Streamlit read/command handlers and the worker use shared idempotency/locking services; network I/O holds no database transaction. Application-owned records and compatible LangGraph checkpointer tables use one local SQLite file with separate table ownership/connections. Verify actual adapter/package compatibility before coding; no invented checkpointer transaction API.

Application transactions validate expected revision/record version, reserve operations/budgets, record the command/event, and commit atomically within application tables. Provider I/O is outside the transaction. Graph checkpoints are separate commits: no claim of atomicity across provider, app transaction and checkpointer.

On restart, compare operation receipts, committed artifact lineage, pending requests, budget reservations and checkpoint identity. Resume only a known safe current human pause or an explicitly reconciled operation. A checkpoint behind an accepted operation must reuse its verified receipt/artifact rather than redispatch a model call. Ambiguous state is STOPPED/OUTCOME_UNKNOWN until reconciled; no automatic paid replay.

## Accepted resume receipts and current projections

AE-03/06 adopt [RESUME-1.0](human-review-corrections.md#review-acceptance-and-graph-resumption--resume-10), [RUN-OUTCOME-1.0](orchestration-budgets.md#invocation-result-and-lifecycle--run-outcome-10) and [STATE-UPDATE-1.0](overview.md#current-state-replacement-and-invalidation--state-update-10). Existing operation/run records store the accepted disposition receipt, exact pending-request/dependency digest and graph_progress separately from operation COMMITTED. COMMITTED means the command's application effect was accepted, not that the graph/checkpoint/report finished. Serialize acceptance/claiming of worker tasks; network and graph work hold no long application transaction.

Crash-gap recovery reuses the original operation/receipt and verified artifacts after explicit reconciliation. A duplicate receipt read cannot schedule recovery; a competing operation cannot consume a recorded request. Re-entry accepts its own exact receipt without re-inserting a disposition, while still rejecting changed dependencies. Application code never edits saver internals or asserts a transaction spanning application/checkpointer commits. Keep prior reports/decisions/support/dispositions as history while explicitly clearing affected current projections. Safe Activity events are allowlisted projections; private graph channels are not assumed automatically redacted if streaming is added later.

Refine TEST-011-01–04 and TEST-007-07/08 with before/after acceptance commit, before/after checkpoint, paused invoke versus completion, duplicate reports and support-only invalidation. These are planned local controlled tests, not claims of exactly-once remote execution.

## Contracts and data changes

EXEC-ADMISSION-1.0 adds the shared execution claim to the existing operations/run persistence boundary, not another datastore: trusted active_execution_key, execution owner/session/purpose, claim state and associated operation. A short atomic unique-slot claim precedes actual execution across app/notebook/CLI processes. Acceptance, applicable reservations and claim commit together; Busy rolls back new disposition acceptance. App/checkpointer commits remain separate. Retain uncertain claims for explicit same-operation reconciliation without PID/time-based stealing or automatic replay. Plain reads and metadata recording do not acquire the execution slot. Existing TEST-011-02/03/04 and TEST-007-05/06/07 cover this contract.

REVIEW-BASIS-1.0 persists analytical_basis_digest separately from review_gate_version/snapshot and the accepted receipt's gate snapshot. Current specialist handling changes the latter without rewriting the original analytical finding/model output; actual source/fact/config/support changes follow invalidation. Validate the latest gate state at acceptance and before completion; neither a frozen OPEN status nor the command's own RECORDED state is a reason to rerun models or falsely complete. Existing TEST-011-01/02/04 and TEST-008-02/03/07 cover this distinction.

Prepared human-condition drafts/targets live in the existing artifact/condition records, with exact reviewed identities and later accepted-disposition association; no draft creates a HumanDisposition or edits original model content. The resumed human node/current report projection loads verified authoritative handling/disposition/condition references rather than treating an older checkpoint's gate snapshot as current. Scope/version validation and the accepted prerequisite snapshot still apply; no additional table family or uncommitted state is introduced.

Proposed logical tables; exact DDL and module layout follow approved repository design:

| Record group | Key/content |
|---|---|
| deals/revisions | deal_id, workspace scope, current input revision, record_version, owner/lifecycle; versioned source/fact correction references |
| sources/passages | source_id/version, package digest, PDF bytes as local BLOB, extracted text/page/passage map, synthetic-data declaration |
| runs/artifacts | run/thread/review identity, mode/config, typed JSON artifacts, current/historical flags, dependency/provenance digests |
| issues/dispositions/collaboration | issue history, distinct exception/control/semantic/High-score credit-risk handling/package records; required/recorded NORMAL/SENIOR tier and score/referral lineage; attributed local notes/owners |
| operations | unique workspace+operation_id, payload digest, state RESERVED/DISPATCHED/COMMITTED/FAILED/UNKNOWN, result receipt |
| usage_ledger | review-scoped reservations/actuals, request identity/outcome, counters/timing, dated rates and total allowance references |
| events | event_id, unique run_id+sequence, operation/dedupe identity, typed safe properties and UTC timestamp |
| reports | generated Markdown/metadata/history, input digest and source/review lineage |
| evaluation_runs/results | mode/split/case/model/prompt/formula/policy versions, expected/observed safe outcomes, metrics, run/sample references; no fake pass |
| checkpointer-owned tables | Only managed by the verified compatible saver; application does not edit internals |

Stage data stores synthetic financial text/facts as required; ordinary analytics does not. No credentials, provider client objects, arbitrary pickled uploads or hidden reasoning in any record. Source/report content access is local scoped service access, not telemetry.

SME records fit existing logical groups: versioned subject/facility/basis and case-completion configuration in sources/artifacts; FactSupportRecord/SemanticAssessment with typed FACT/CLAIM target and expected-record-version guards in artifacts/dispositions; CONDITIONS-1.0 records with parent provenance/status/linked-issue IDs in artifacts/dispositions/reports. No second database or new infrastructure. A support-only operation retains input revision but changes support/dependency versions; revoked/replaced support stales dependent current artifacts and pending review, while preserving terminal history. Value/source/basis/subject changes use an analytical revision rather than falsely claiming support-only. Source support and credit disposition cannot share an authority flag.

Proposed repository operations: get/save current artifact with expected revision; get_operation_receipt; reserve/reconcile_usage; append_event_once; list_events(after_sequence); list_evaluation_results. Keep high-level QA false-positive counts and Reject-walkthrough pass/fail in offline evaluation results; no additional app tables, analytics events or UI display are required for these two checks. Store fixture_variant_id, current semantic input digest, prior_run_id/start_stage/rerun_reason and shared review_id lineage for corrections. All mutation calls use CommandMeta or trusted node-operation identity.

Director refinements fit existing tables: NARRATIVE-CHECK-1.0 stores application-owned target Claim/path/text/dependency digests for all AI narrative fields and human condition edits in artifacts/dispositions; no new evidence database. SOURCE-TRIAGE-1.0 stores product-control owner/reason/affected scope and linked existing root without inflating policy or missing-document counts. INPUT-EDU-1.0 version is configuration/schema lineage. CONTINUE-CHECK-1.0 stores a safe path/count/allowance estimate with its basis/config version using current run diagnostics, not a second budget ledger or reservation. Imminent dispatch reservations reconcile once to actual work; estimated future steps are not double-charged. Preserve original model artifacts for EVAL-CUTOFF-1.0, current support scopes, all unresolved paid reservations and historical reports. Raw invalid body content never enters ordinary events; rejected inputs publish only safe field/reason metadata. Use existing TEST-011-01/02/06/07, not new tables or metrics.

## Exact checkpoint and artifact representation — STATE-CODEC-1.0

Use one small versioned conversion/validation boundary for saved application artifacts and serializable graph state. Domain models remain typed and validated in services; the persisted/checkpoint representation is a schema-known JSON-compatible primitive tree, never a live Pydantic/client/connection object or an arbitrary class to reconstruct. Record state_codec_version with saved schema/config metadata and dependency identity. The pinned LangGraph/saver adapter must prove round-trip behavior for this representation before using persistent review flows. Do not invent a saver API or turn on pickle fallback to hide an unsupported type.

| Domain content | Saved representation and restoration |
|---|---|
| Money, financial inputs, factor grades, contributions and exact threshold operands | Canonical Decimal strings under their known field schema; restore exact Decimal values before arithmetic/validation, never binary floats. Derived repeating results retain the existing formula precision and exact operand refs |
| Confidence | Canonical exact Decimal string ONLY in the internal saved representation; restore/validate the bounded exact0..1 number before routing/hashing. The external model wire still requires a JSON number, not a string. Do not use a default dump/load path that changes the0.7 comparison |
| IDs, versions, enums, UTC timestamps, dates and explicit nulls | Schema-validated strings/literals/null, with timezone/date validation on restore. Preserve list order and schema-declared sets through CANON-1.0; malformed/unknown schema/codec/enum values fail explicitly |
| Source text/references and artifact relationships | Preserve exact Unicode/code points, scope and original source digests. Store scoped refs rather than copying PDF bytes, whole event histories or hidden reasoning into each checkpoint; original PDFs stay in source storage |
| State patches | Preserve omitted-key versus explicit null/[] clearing semantics from STATE-UPDATE-1.0. Serialization cannot drop nulls or silently carry an outdated current report through a clear |

After decode, restore the declared trusted field types and validate scope/schema before calculations, routing, canonical fingerprints or a resume action. Never infer a numeric type from arbitrary user text or apply string ordering to numeric thresholds. No automatic migration, rounding, value guessing, schema downgrade or paid recovery follows from an incompatible saved state. Stop with a safe compatibility/recovery reason while retaining original artifacts; fixture/manual tests must demonstrate correctness first.

Canonical identity uses CANON-1.0's typed semantic projection, not incidental serializer object tags, generated UUIDs or display text. For NARRATIVE-CHECK-1.0, parent_digest is the immutable accepted narrative-content projection (wire content plus declared stable logical evidence/basis dependencies), excluding its own digest, generated target IDs, evidence_target_refs and later support/handling records. Compute it before attaching local targets; each target then binds that parent, path and exact text digest. Human condition drafts/edits use their own immutable content parent. Later evidence-target attachment or review progress cannot create a self-referential hash or rewrite the original model content. Changed text/evidence/basis still invalidates its corresponding support; review-gate state is checked separately under REVIEW-BASIS-1.0.

Required controlled round trips include confidence0.699999999999999999999999 (still below0.7 after restart) versus0.7; explicit financial zero versus missing null; supported negative CFADS; unrounded score25.000001 (Moderate despite display25.00); exact document/source text and field refs; ordered conditions; explicit stale-output clears; and unchanged semantic fingerprints before/after storage/checkpoint/rehydration. Wrong codec/schema or altered source changes must fail/invalidates as appropriate, not silently restore. TEST-011-01/03, TEST-003-06, TEST-004-11, TEST-006-05 and TEST-007-02 own these checks. Static examples are not proof that the pinned saver works.

## Offline RAGAS results within the existing evaluation boundary

The user-authorized [RAGAS-EVAL-1.0](../evaluation/ragas-evaluation.md) extends existing evaluation_runs/results, not deal state or another database. Store the frozen sample/original artifact/actual context and reference digests, subject/cutoff, five RAG-R01–05 score/status/explanation/example objects, independent mechanical critical flags, native raw metrics/definitions, package/adapter/judge/prompt versions, result origin, human disagreement and separate evaluator usage. Manual, controlled-adapter, executed native/custom RAGAS and original FIXTURE/LIVE lineage remain distinct. Missing/failed scores are null with reasons, never a fabricated pass.

Render the separate [evaluation report](../evaluation/evaluation-report-template.md) from saved results only. NATIVE-REPORT-1.0 always shows Faithfulness, Response Relevancy, Context Precision and Context Recall, with exact implementation/variant/version, scale, raw_score, status/reason and sample/context/reference digests. Absent results initialize as NOT_RUN with null score; selected definition/input checks distinguish NOT_APPLICABLE, INPUT_UNAVAILABLE, NOT_SELECTED, FAILED and STOPPED. Measured zero remains SCORED. Validate each native range, preserving legitimate negative cosine relevance values; display rounding never changes raw values. DIRECT ranked precision is NOT_APPLICABLE. Optional ID metrics stay distinct. Do not blend native and custom scores, invent an overall score or run any scorer while rendering. This quality report is separate from the seven-section credit memo.

Only the explicit offline evaluation service may dispatch its configured scorer. It uses existing budget/operation helpers under OFFLINE_EVALUATION with a separately approved evaluation-run allowance; it cannot reset/borrow the original deal allowance or mutate support/issues/approvals. Default/import/UI inspection executes zero evaluation calls. One validated shared custom bundle feeds five local metric projections; optional native judging requests need their own declared plan and actual accounting. Cache keys bind exact frozen sample/context/rubric/judge/config/version; duplicates reuse receipts rather than request again. Persist synthetic quotes only in scoped evaluation artifacts, not ordinary telemetry. Existing Activity developer/instructor view exposes the five dimensions/examples/native diagnostics/flags/costs; no additional navigation screen or ordinary risk-QA dashboard. Extend TEST-011-01/06/07 and existing dispatch/privacy checks; runtime compatibility remains unverified.

## Event contract and metric sources

Every event: event_id, event_name, workspace/deal/review/run IDs where applicable, input_revision, mode, operation_id, stage/task, schema/config versions, UTC time and sequence; safe properties only. Required handoff events include sender/recipient/artifact refs and validation outcome. Sequence, not wall-clock equality, defines report cutoff.

Specific properties: stage duration/status; policy/risk counts and rule IDs; issue severity/owner/affected scope; usage actual/estimated/unavailable, input/cached/output counts, reserved and conservative cost; context component counts and cache lineage. No raw prompt/report/source/notes/search-query/borrower values, API keys, request headers or provider error bodies. Debugging synthetic text requires an explicit local source inspector, not broad logging.

Versioned credit-score/band/material-input artifacts and optional supported AI proposal persist within existing runs/artifacts, not an additional database. Store factor ratings/contributions and sources there for scoped inspection, not in routine analytics. Score-route audit events carry control IDs, configuration/artifact references, required/recorded tier and permitted-action outcome without borrower scores or free-text reasons. record_credit_risk_review emits credit_risk_review_recorded once from SPEC-008; existing decision_route_computed/review events retain the independent reasons. Reopen/restart verifies current score/configuration/referral lineage before treating handling as satisfied.

Events are owned by the responsible service from each feature; storage provides append-once behavior. Model context never includes the complete event history. Local evaluation view is a developer/instructor expander in Agent Activity, not a sixth product screen.

Reuse semantic_assessment_recorded with target_kind FACT/CLAIM, scoped target/support/configuration IDs, outcome and record version; record no values, row text, subject labels or free-text reasons. Package-validation events may carry completion_scope and trusted_configuration_available flags. Existing stage/wait/continuation events distinguish data-quality support from credit review and elapsed human wait from active time. Condition provenance/status and sources remain local scoped content; analytics uses IDs/categories, not condition text. No automatic expiry or hidden provider dispatch is introduced.

## AI and evidence behavior

Persistence/inspection has zero inference. A saved checkpoint is state history, not a complete event log or immutable record. MemorySaver/InMemorySaver loses its state on restart and is only a notebook/test profile. SQLite supports local persistence but not tamper-proof records or distributed reliability.
Sources: [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [interrupt semantics](https://docs.langchain.com/oss/python/langgraph/interrupts).

## Authorization

Apply shared local workspace/deal scope and P3-02 mutation permissions in services. Administrator may investigate/reconcile technical operations but cannot fabricate observed usage or clear financial/control issues. LangSmith remains disabled; connecting tracing needs approved fields, retention and any costs.

## UI states

Empty: no runs/events/evaluations, labeled Not run. Loading: read in progress. Success: actual artifacts/event sequence and separate fixture/live results. Failure: safe storage/reconciliation message. Stale/inconsistent: disable affected mutations and expose required recovery without replaying work.

## Reliability, retention and stopping

Unique operation/event identities, expected-version checks, finite transactions and no long transaction around network I/O. Persistence failure stops new paid dispatch. Repeated checkpoint/event writes are idempotent. Unknown usage stays reserved. Test crash gaps rather than asserting exactly-once network execution.

Confirmed P3-04: no automatic expiry in the MVP prototype. Do not configure age-based expiry, a deletion schedule or automatic pruning for persisted synthetic documents, deal records, reports, review history or SQLite checkpoints. Keep synthetic app state locally; any future manual deletion/reset requires an explicit user request, exact reviewed targets, active-review protection and consistent checkpoint/artifact handling. No attachment, archive, source documentation, user file or external record is an implicit cleanup target. MemorySaver's process lifetime and provider-controlled prompt caches are separate; no guarantee against storage failure is implied.

## Analytics

This feature stores common events plus storage_error, operation_reconciled, recovery_required and evaluation_result_recorded. Dashboard/evaluation metrics derive from records, never fabricated counters. Metric calculations and observed/estimated/demo labels are in the evaluation plan; Phase 5 will map events to modules/dashboards.

## Tests and acceptance

- TEST-011-01: Round-trip scoped sources/artifacts, score/material-input/configuration/AI-proposal lineage, subject/facility metadata, typed fact-support targets and ConditionRecords; separate credit-risk handling/review tier. No cross-deal join, fabricated Live support or stale handling after changed fact/source/basis/support dependencies; support-only version change retains analytical revision/history. NARRATIVE-CHECK-1.0 local targets round-trip once per parent/path; original and human-edited text retain separate lineage, and path estimates never reset/double-charge the ledger.
- TEST-011-02: Concurrent duplicate/stale commands cannot create two operations, notes, dispositions or paid requests.
- TEST-011-03: Crash before dispatch/after dispatch/after artifact commit/before checkpoint; no unapproved replay or budget loss. Include RESUME-1.0 disposition acceptance/checkpoint gaps and idempotent report re-entry without model replay.
- TEST-011-04: SQLite pending-review restart versus RAM history loss and correct visible limitations.
- TEST-011-05: Explicit event completeness for required actions, ordered cutoff and no duplicate pause/resume events.
- TEST-011-06: Logs/checkpoints/events contain no configured secrets or hidden reasoning; fixture/live/estimate labels.
- TEST-011-07: Evaluation view shows Not run/Failed/Passed separately, with versions/denominators, no empty-data success. EVAL-CUTOFF-1.0 retains the original E-N01 extraction miss after human correction, distinguishes genuine E-M01 absence, freezes original conditions and reports attempted/accepted/withheld/failed denominators. RAGAS-EVAL-1.0 adds five strict1–5 dimensions/examples, native-scale separation, original-context/reference isolation, invalid score6/fabricated-quote rejection, manual/controlled/package-executed labels and separately recorded human disagreement/usage. NATIVE-REPORT-1.0 checks four visible native rows, null versus measured zero, DIRECT ranked precision Not applicable, missing reference Input unavailable, legitimate negative relevance preserved, exact versions/scales and no blended overall score. Reading/rendering results performs no judging or embedding requests.
- TEST-011-08: Advancing the test clock beyond 30 days and restarting with the same SQLite database does not expire/prune persisted documents, records, reports, review history or checkpoints; no scheduled deletion or implicit destructive reset; hosted tracing inactive. Test MemorySaver's expected RAM loss separately.

Target: 100% controlled integrity/idempotency/privacy checks. Additional recovery/retention tests are local application tests, not extra independent loan scenarios.

## Dependencies and implementation boundary

Defines interfaces for all specs, not a second infrastructure service. No SQLite file, schema migration, tracing connection, cleanup command or measured dashboard exists yet.
