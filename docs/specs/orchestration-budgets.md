# Graph Orchestration, Modes and Cumulative Budgets

**Correction implementation:** CORRECTION-1.0 initial extraction miss executes5 nodes
then stops. Save consumes no graph/model work and reserves the one correction
allowance without resetting ledger. Explicit Update preflights the remaining direct
path, seeds unchanged intake plus reviewer-corrected extractor and executes7 nodes.
Observed fixture totals12 nodes/7 tools/0 provider calls. No old-thread changed-input
resume, hidden node merging or budget increase. See [contract](source-correction-integration.md).

**E-P01 implemented:** [CONDITIONAL-1.0](conditional-integration.md) uses the existing
reviewed graph pause/resume. Handling/preparation/support are durable human commands,
not extra model nodes. Verified final fixture uses11 nodes/4 tools/0 provider calls,
with unchanged cumulative limits and no automatic wait expiry. Missing specialist
receipts block final dispatch; no generation replay to complete a human decision.

**Hosted embedding accounting — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) selects Nebius-hosted embeddings with model/API/allowance unconfigured. Two normal generation tasks do not mean two total provider requests. Account for embedding requests, input tokens, retries, active time and dollars separately; review-time work must fit existing cumulative review caps. Corpus preparation/isolated retrieval benchmarks require an explicit separate REFERENCE_EMBEDDING allowance, and RAGAS keeps its OFFLINE_EVALUATION allowance. No numeric allowance, automatic paid request, fallback or higher cap is approved by provider selection.

Feature ID: SPEC-007
Version: 1.8
Status: Registered saved paths and live checkpoint/allowance integration implemented; actual live extraction verified; full live journey blocked by deferred recovery and human review
PRD requirements: FR-008, FR-011, FR-014–015, FR-018–020
Role instructions: [Orchestrator](../agents/orchestrator.md), [Shared contract](../agents/shared-contract.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

A learner runs a real bounded graph, sees delegated work and failure reasons, and can distinguish Fixture from Live. No planning LLM, autonomous loops, distributed queue, background paid replay, or provider fallback.

## Workflow and rules

The implemented live path inserts fact_review after extraction and requires
actual narrative evidence review after synthesis, using existing interrupts and
SqliteSaver checkpoints. The saved and live paths retain their separate services
under the shared graph builder. The one UI Run action uses config/app.toml mode;
historical source controls display/resume. Named specialist groups and derived
handoffs are specified in [specialist-handoffs.md](specialist-handoffs.md).
Do not apply saved-path node-count examples below to the live path without its
actual cumulative ledger; no graph node, cap or reserved budget is merged away.

Proposed scheduled nodes: pdf_input -> extractor -> financial_analyst -> compliance_check -> risk_quantifier -> synthesizer -> evidence_review -> route_review -> [human_review OR report_generator]. Human review resumes to report_generator when permitted. Each edge checks current prerequisites; missing mandatory data ends the current invocation with an information/blocked state and safe partial artifacts. It does not fabricate a complete PanelDecision.

SME fixes add prerequisite checks within existing services/edges, not graph nodes. A registered reviewed case pack is required for complete review; unregistered synthetic Live uploads run only supported partial work and cannot acquire a PanelDecision without trusted assessments/configuration. After Live extraction, unresolved subject/basis or FACT-SUPPORT-1.0 requirements pause affected trusted calculations through the existing information state. Required factual support is a data-quality step distinct from the later credit-review interrupt. A known critical fact awaiting support creates a DEMO_PRODUCT_CONTROL requirement (HIGH, Risk Manager, NEEDS_INFORMATION for affected dependencies), excluded from policy exceptions and from missing-document counts when the document exists. UI shows Support review required rather than pretending the source is absent or verified.

Seven specialists remain inspectable; Agent 3 composes risk_quantifier and synthesizer. route_review is deterministic Orchestrator work, not an eighth model agent. A valid direct path executes nine nodes. Required human review invokes its node once to pause and again on resume, so the ordinary reviewed path executes eleven actual invocations. Count retries, repairs and reruns too; these counts are planned examples, not measurements.

Named scheduled tool boundaries: compute_financials, evaluate_policy, calc_credit_risk, calc_concentration_risk. Ordinary arithmetic helpers are not independently registered tools. If implementation adds actual child tools/nodes, count each; wrappers cannot conceal work.

run_review(RunCommand) -> RunReceipt; continue_review(ContinueCommand) -> RunReceipt; cancel_review(CommandMeta) -> receipt; get_run/GetEvents are read-only. RunCommand identifies committed manifest, mode, policy/scenario/config version, expected revision and operation. ContinueCommand identifies stopped/pending run and affected rerun plan. Commands cannot reset the review allowance by refreshing, changing operation ID or creating another run on the same review.

Fixture adapters return registered model-stage artifacts while the graph/Python panels execute. Responses must match scenario+variant+stage+package_digest+normalized current input_digest; package match alone cannot authorize a corrected synthesis. A mismatch stops with FIXTURE_VARIANT_UNAVAILABLE. No arbitrary upload/edit gets fixture responses. Live needs selected model, verified structured output/token accounting/rates, later local credential, explicit mode, and per-run plus total execution allowance. A key alone is not spending authorization.

P3-03 uses one process-wide standard-library worker with maximum one active execution, launched only by an accepted user command. Streamlit reads persisted progress and can request cancellation while the worker awaits a provider; only the main UI thread calls Streamlit. Services/graph run in the worker without UI objects. Refresh reuses the same service/worker/run identity, never starts another task. Waiting human nodes release active execution; resume schedules one permitted task. A process restart creates no automatic replay. No distributed worker, message broker or continuously running paid agent is introduced.

## Shared execution admission — EXEC-ADMISSION-1.0

A process-wide worker alone does not coordinate separate Python entry points. Every execution using the same resolved local SQLite workspace must first acquire the same database-backed admission claim: app start/continue/resume/recovery, optional notebook fixture execution, evaluation CLI and optional retrieval/RAGAS work. A separate process is not a separate allowance or execution slot. Pure graph-only notebook rendering, static HTML, ordinary reads/help/citations and permitted metadata/support recording perform no graph/scoring work and need no execution claim.

Use existing SPEC-011 operations/run records, short atomic application transactions and an SQLite uniqueness constraint for one non-null active_execution_key per database. The shared key is a trusted singleton local-execution slot, not a submitted deal/operation ID. Store owner execution identity/session, associated operation/purpose, claim state HELD/RECOVERY_REQUIRED/RELEASED and admitted scope. No new database, queue, server, worker framework or long transaction around provider/model work. SQLite guards cross-process admission; the existing worker controls in-process scheduling. Exact DDL and connection behavior must be verified in the approved milestone.

1. Resolve the approved absolute database/workspace identity and validate the command, scope, duplicate receipt and budgets. An identical accepted-operation receipt read never starts or reacquires execution. An explicit recovery command remains distinct.
2. In one application transaction, claim the unique slot together with applicable operation/budget reservations and command acceptance. Competing starts return RUN_BUSY (display Busy) before graph/provider/embedding work; failed admission cannot persist a newly accepted human disposition. Local metadata commands retain their short guarded transactions without occupying the execution slot.
3. Schedule only the admitted worker/explicit CLI operation. It verifies its exact claim/operation before each actual dispatch. All native metric child requests still use the admitted evaluation scope and its own counted allowance; they do not create hidden workers or claims.
4. Release once only after a confirmed invocation end, durable information/review pause with no in-flight work, completion or acknowledged safe stop. Atomically clear the non-null active_execution_key and mark RELEASED while retaining owner/operation/claim history in existing records/events. Release is not approval, usage forgiveness or budget reset; unresolved usage remains reserved independently.
5. If process/dispatch/checkpoint outcome is uncertain, retain a RECOVERY_REQUIRED claim until explicit reconciliation proves safe completion/termination or permits the same existing operation to recover. A dead PID, old timestamp, UI refresh, new process or new operation ID cannot steal it, clear paid reservations or replay work. A controlled proved-NOT_DISPATCHED recovery may release it; no timer/automatic expiry or destructive cleanup is added.

The admitted operation may reuse its own verified claim during explicit receipt recovery, never another operation's claim. Waiting for a user releases the slot only after the actual pause is saved; resume must reacquire it within its accepted command transaction. Default offline tests use isolated temporary databases. If a notebook/CLI intentionally selects the app database, it obeys the same rule; an accidental alternative runtime path cannot silently create a second workspace database to bypass Busy.

Extend TEST-007-05/06/07 and TEST-011-02/03/04 with two independent process/connection contenders, app-versus-evaluation admission, duplicate reads, a saved pause/reacquisition, atomic Busy rollback and crash recovery without automatic claim expiry. Exactly one contender may start work. Graph-only rendering remains zero-write/zero-claim under TEST-012-01/03. These are local test plans, not executed distributed-scale evidence.

## Correction and continuation state transitions

Use one graph definition with a service-controlled conditional START edge; start_stage is chosen from a validated rerun plan, never from uploaded/model text. The edge function is routing, not an uncounted wrapper that executes hidden work. All actual nodes/tools are counted.

| Action | Input revision / run / thread | Entry and behavior |
|---|---|---|
| Initial review | Current revision; new run_id/thread_id; existing review_id ledger | START -> pdf_input and normal chain |
| Review-only disposition / modified conditions | Same revision, pending run_id/thread_id | Command(resume=validated_payload); only interrupted human_review repeats, then report; no model rerun |
| Source-support assessment only, unchanged fact/source/basis | Same input revision; new run/thread with prior_run_id after the explicit information pause; SAME ledger | Save support dispatches nothing. Explicit continue enters earliest affected stage (Financial for pre-calculation fact support; Evidence/routing for later claim-only support), validates support/dependency digests and reuses unchanged artifacts in fresh scoped envelopes. Never replay extraction or reuse an old pending credit-review token |
| Source-backed analytical fact correction after a pause/completion | input_revision+1; new run_id/thread_id; SAME review_id ledger | Validate correction; build current terms with correction provenance; promote unchanged source evidence explicitly; START -> financial_analyst -> compliance_check -> risk_quantifier -> synthesizer -> evidence_review -> route_review -> permitted review/report |
| Source addition/replacement that changes extracted information | input_revision+1; new run_id/thread_id; SAME review_id ledger | START -> pdf_input -> extractor; reuse parse blocks only for unchanged source digests; normal downstream chain |
| Explicit schema/technical retry after a stopped invocation | Same analytical revision; new run/thread with prior_run_id; SAME ledger | Start only at the failed validated stage; permitted bounded retry/repair and dependency checks, never automatic replay |

For analytical corrections/source replacement, the entry column names the planned continuation, not automatic dispatch on Save. The impact preview is read-only. Save records the revision/invalidation and prepares the new run/thread with lifecycle READY and the same review ledger. Only an explicit permitted Update affected findings/continue_review command schedules the worker and invokes START at the planned entry after rechecking revision/dependencies/mode/budgets. Saving, reading the impact or refreshing cannot spend model allowance or count as an executed graph node. No new planning model/node or budget reset is introduced.

Correction is allowed only at a safe paused/completed/stopped boundary; a running/uncertain provider operation must finish or be reconciled first. A paused old run becomes STOPPED with reason SUPERSEDED_BY_REVISION; an already completed/stopped run retains its historical terminal outcome and gains a supersession link. Old pending review is STALE, and checkpoints/artifacts remain history with no automatic expiry. Never resume that stale interrupt to process new facts. Reject old-thread/current-revision mismatches. Rebind reused evidence to a new envelope only after dependency equality; do not copy old PanelDecision/review/report as current.

If replacement/current synthesis cannot fit the remaining cumulative allowance, stop with partial state and BUDGET_EXHAUSTED; do not start a fresh budget. Pending approval-only resume uses the original thread precisely because no analytical revision changed. A new correction thread starts with an explicit validated state snapshot; it does not inherit old memory automatically.

Support-only continuation also uses an explicit validated snapshot and fresh artifact identity. Mark the prior information-paused invocation STOPPED/SUPERSEDED_BY_SUPPORT_CONTINUATION; preserve input revision and prior history. Stale dependent pending credit review even without a fact-value change if support status/lineage changes. If a negative support result is corrected by changing a value/source/basis, use analytical revision+1 instead. Source review waiting is excluded from active processing like other human waiting. All actual node/tool/model invocations across these runs remain charged to the same allowance; the complete path still has two normal model calls, and a partial path may have fewer.

Sources for framework semantics: [LangGraph conditional entry](https://docs.langchain.com/oss/python/langgraph/graph-api), [interrupt resume](https://docs.langchain.com/oss/python/langgraph/interrupts). Exact pinned package behavior is checked in the first approved compatibility task, not claimed executed here.

## Contracts and data changes

RunRecord: run_id, review_id, deal_id, input_revision, thread_id, prior_run_id nullable, superseded_by_run_id nullable, fixture_variant_id nullable, start_stage, rerun_reason, mode, lifecycle, node cursor, config digest, issue/review/report refs, stop reason, start/end/wait timing. review_id scopes cumulative allowances across run/revision corrections and resumes; a distinct educational assessment needs an explicit new-review action, not automatic budget renewal.

RoutingResult: amount_trigger, confidence_trigger, other_referral_ids, effective_escalate, route HUMAN_REVIEW/REPORT/WAIT_INFORMATION/BLOCKED, reasons. Valid amount/confidence prerequisites precede the false branch. Individual Issue records survive summary precedence P3-01.
RoutingResult additionally records exact score/band/config/status refs, score_referral_ids, required_owner_categories, review_tier NORMAL/SENIOR, credit_risk_handling_status and independent evidence/policy readiness reasons. Include SCORE-ROUTING-1.0 referrals in the Python OR alongside amount/confidence/other mandatory referrals. A complete Moderate score always requires NORMAL Authorized Approver review; High requires Risk Manager credit-risk handling then package review; VeryHigh requires SENIOR Authorized Approver disposition. Low retains existing conditional routes. Missing/invalid/stale material score prerequisites cannot select the false/no-review branch: pause dependent synthesis/final readiness using the scoped information/configuration issue. No extra planning/model call or graph node is introduced.

Score-referral issues with fully supported inputs block final completion/review satisfaction, not preparation of a supported Synthesizer recommendation; SCORE-DATA-MISSING blocks dependent synthesis as a missing material input. Existing missing policy/control/evidence gates retain their current scopes and precedence. Waiting for Risk Manager handling uses the current human-review request/issue service, not another model cycle; only the final permitted approver resumes graph completion after all prerequisites. Recorded handling/tier must match the same revision/band/method. Once fulfilled, original true predicates do not cause an endless second interrupt. Corrections invalidate those acknowledgements and share the same cumulative ledger.

BudgetLedger: review_id, attempts/tools/nodes committed and reserved, input/output committed and reserved, conservative cost committed/reserved, active_ms, pending provider request IDs/status, batch_allowance_id. State contains a reference/snapshot; the durable ledger is authoritative.

| Boundary | Required check before dispatch |
|---|---|
| Model | Two normal successes; <=5 cumulative outbound attempts, <=8,000 input /2,000 billed output; <=USD0.25 model/tool cost |
| Time | <=180 active seconds total; each model timeout <=45 seconds and remaining active time |
| Graph/tools | <=20 actual node invocations, <=12 actual tool invocations |
| Retry/load | <=1 transient retry per operation; one active review; retries consume the same ledger |
| Target only | <=USD0.10 and p95 <=90 seconds remain measured goals, not proven limits |

## Bounded continuation feasibility — CONTINUE-CHECK-1.0

The authorized Director recommendation uses a small deterministic path-count table in the existing orchestration service, not a planning agent or general workflow optimizer. Correction impact preview reads this table/ledger; it changes no state and reserves no usage. Before explicit run/continue/resume scheduling, recheck current prerequisites and whether the required no-retry completion path can fit remaining nodes/tools/attempts/tokens/cost/active time. This is a bounded feasibility check, not a guarantee that future model output will validate or meet the proposed token target.

| Supported path | Planned actual node invocations, including human pause and resume |
|---|---:|
| Initial direct report | 9 |
| Initial reviewed report | 11 |
| Correction entering Financial, direct report | 7 |
| Correction entering Financial, reviewed report | 9 |
| Already pending review: resumed human node then report | 2 additional; the first pause invocation is already charged |

Derive tools/model work from the same actual start stage and configured stages: a full initial path schedules four registered tools and two normal model stages; an analytical correction entering Financial schedules four tools and one synthesis rerun. Fixture mode dispatches zero real provider requests and model tokens/cost remain Not applicable, while actual nodes/tools still count. Source replacement/extraction retry, source-support continuation or claim-only continuation uses its existing start-stage suffix; enumerate its possible edges from the shared graph metadata rather than inventing hidden work. Before confidence/other dynamic routing is known, use the longer applicable supported branch for this check. A known partial/information outcome uses only its permitted prefix, not a hypothetical complete decision path; missing-data outcomes may legitimately pause earlier. Correctly handled current review predicates must not cause another interrupt loop. Any added node/tool requires updating this table and planned counts before implementation.

An ordinary reviewed completion (11) followed by a reviewed Financial correction (9) reaches the unchanged 20-node ceiling. This exact path is permitted if EVERY other allowance/prerequisite fits, with no node recovery headroom. It is not an assurance that another retry can finish. If the required path already exceeds remaining allowance, decline execution before provider dispatch with the specific BUDGET_EXHAUSTED reason, preserving the saved correction/partial state. If an unexpected retry/recovery consumes the remaining allowance during execution, stop at the boundary, retain recorded work/history and disclose the unfinished report. Never hide node executions, merge nodes solely to evade counts, reset the review allowance or map a budget stop to Reject. Read-only citations, diagnosis and historical inspection remain available.

Only the imminent actual dispatch is durably reserved/count-reconciled under SPEC-011; the completion-path estimate itself is not a second reservation. Do not double-charge estimated future work, the original pause or a duplicate receipt. Recheck the remaining suffix at each dispatch/resume boundary, convert each reservation to actual work once, and preserve unresolved provider reservations. Provider calls still require full conservative input/output/cost reservation. UI details may show Fits required path; no retry headroom, but must not claim guaranteed completion, observed timing or zero future cost. Source-support/human waiting is excluded from active processing under the existing rule, not erased from elapsed waiting history.

Node limits protect bounded execution; they are not a measure of model cost. Actual billable provider usage determines model cost, and Python/report/review work remains zero inference. The <=20 nodes, <=12 tools, <=5 outbound attempts, 8,000 input/2,000 billed output, USD0.25 hard cost and active-time caps do not change. Existing TEST-007-02/03/06/08, TEST-006-08 and TEST-008-04/07 cover direct/reviewed counts, 11+9 equality, overrun/recovery stop, no-double-reservation, saved correction without dispatch and original-ledger preservation. Counts are specification arithmetic until the pinned graph is instrumented.

## Normalized provider outcomes — PROVIDER-1.0

AE-05 defines one small application adapter contract, independent of the eventual verified Nebius model. A configured HTTPX transport is proposed, not installed. Use nonstreaming, one completion, explicitly bounded output and no model-accessible tools. Verify native schema-constrained JSON support for the exact selected model; JSON-object mode alone is not the same guarantee. If an explicitly reviewed profile uses JSON-object mode, strict local schema validation and identical safeguards remain mandatory. No silent mode/model/provider fallback, function-tool fallback or SDK repair/retry loop. Check model parameters, billed reasoning/output bounds, tokenizer/template and dated rates before enabling Live.

ProviderRequest binds the scoped operation/attempt and review ledger, canonical request digest, instruction/schema/model/config versions, input reservation, capped billable output, conservative monetary reservation and remaining deadline. ProviderOutcome contains that local request identity; safe provider request ID if supplied; transport certainty NOT_DISPATCHED/RESPONSE_RECEIVED/OUTCOME_UNKNOWN; outcome SUCCESS/REFUSAL/INVALID_OUTPUT/TRUNCATED/TRANSIENT_ERROR/PERMANENT_ERROR/OUTCOME_UNKNOWN; HTTP status and allowlisted finish reason nullable; structured payload nullable; refusal flag; independent UsageObservation and safe error code. These are application fields, not assertions about Nebius response property names. Keep raw output only as scoped synthetic quarantined content where needed, never routine telemetry/hidden reasoning.

| Response/transport condition | Required handling |
|---|---|
| Complete success | Require the verified profile's success status/finish reason, exactly one nonempty content result, no refusal or unsolicited tool calls, strict JSON plus full local wire/reference validation. Only then hydrate an accepted stage artifact |
| Refusal, empty choices/content, malformed structure, unexpected tools or non-success finish reason | No accepted stage/PanelDecision. Classify REFUSAL or INVALID_OUTPUT with a safe reason. A schema-looking JSON object does not override refusal/finish metadata |
| Truncation/output limit | TRUNCATED even if the prefix happens to parse. No accepted recommendation, hidden continuation or silent token increase |
| Confirmed failure before outbound dispatch | No billed request is assumed dispatched; retain the operation audit and release only its proven unused reservations. At most one permitted transient retry if all remaining caps/deadlines allow. Count every actual outbound attempt, including failures |
| Timeout/disconnect/crash after possible dispatch | OUTCOME_UNKNOWN; keep conservative reservations and stop. No automatic paid retry or provider replay. Local cancellation cannot undo remote processing |
| Rate limit or transient server response | Retry at most once only if the verified profile establishes a safe retry/no-execution outcome and all reservations fit. Bound Retry-After/backoff inside remaining 45-second operation and 180-second active deadline; otherwise stop. An error response alone is not proof of zero billable usage |
| Authentication, unavailable model/capability or permanent request error | Stop with safe configuration/provider error; no alternative paid service or fixture success |

UsageObservation is independent of content acceptance: actual/estimated/unavailable input, cached-input subset, billed output including reasoning where relevant, rates/version and reconciliation status. Reconcile known usage even on refusal/invalid output. Missing, contradictory or unverified usage retains the conservative unresolved portion; never record zero by default or free that budget for another call. A known response with unknown usage is not the same as a successfully reconciled bill. Reject output/usage outside the verified bounded profile and stop further paid dispatch. INPUT-EDU-1.0 bounds raw transport/content parsing and rejects duplicate JSON names before domain validation. Oversized/malformed post-dispatch envelopes cannot establish zero billed usage; retain unresolved reservations and a safe technical reason rather than accepting a truncated subset.

Controlled response fixtures in TEST-002-06, TEST-005-06 and TEST-007-03/05/06 cover every row before funded Live validation. They validate the adapter contract only. Refusal/transport/schema failure never maps to the financial decision Reject. Nebius documents model-specific [structured JSON support](https://docs.tokenfactory.nebius.com/ai-models-inference/json); exact response mappings and capabilities remain a later compatibility check, not presumed implemented APIs.

## Invocation result and lifecycle — RUN-OUTCOME-1.0

Authorized normal E-N01 slice, 2026-10-23: the shared graph.py definition initially implements pdf_input -> extractor -> financial_analyst -> compliance_check -> risk_quantifier -> synthesizer -> evidence_review -> route_review -> report_generator. Only the exact registered default Fixture entry is admitted. Actual stage completion creates source-bound primitive artifacts/events; the four Python finance/policy/risk/evidence tools and all nine nodes count. Fixture lookups are not provider attempts and their billed tokens/cost are Not applicable. No unimplemented human/recovery/other-case path is simulated as successful. Unexpected review needs stop before report; this does not complete the eventual human-interrupt workflow.

worker.py uses the existing Store admission slot and versioned application records, the configured single SQLite database and SqliteSaver with pickle fallback disabled. Compilation/import/render-only inspection creates no database or provider work. An explicit command supplies or records operation/run/thread identity and UTC generation time. Before each dispatch, durably reserve its bounded active time/node/tool usage; after a confirmed local result, atomically persist the primitive artifact/event and reconciled ledger before the graph checkpoint. Persist one immutable report artifact per operation. Duplicate commands read the prior result without replay. Any interrupted/uncertain app-record/checkpoint gap retains RECOVERY_REQUIRED and reservations for explicit later recovery; restart/time/PID cannot auto-clear or re-invoke nodes. Terminal completion requires the actual accepted report and a terminal graph checkpoint. History and original registrations remain unchanged; no schema migration or second database is added. Guard all shared execution entry points and reject incompatible state/digests instead of mixing revisions. These are scoped normal-path guarantees; full cancellation, human resume and analytical correction remain later M3 work.

AE-03 requires the worker to inspect graph outcome and current persisted artifacts, not just that invoke returned without an exception. A returned interrupt maps to WAITING_REVIEW with its current request and releases the worker. An information/support prerequisite reached through END maps to WAITING_INFORMATION, not COMPLETED. Only a current accepted report plus all applicable current completion/review gates satisfied maps to COMPLETED. Confirmed cancellation maps to CANCELLED; budget, technical, invalid-state or uncertain-operation stops map to STOPPED with the actual reason and preserved partial artifacts. A checkpoint/operation contradiction is RECOVERY_REQUIRED under STOPPED. No accepted loan decision is fabricated for these outcomes. Graph return shapes must be verified with the pinned version; do not infer completion from an empty update or from a receipt that only accepted a command. TEST-007-02/06/07 and TEST-011-03/04 cover paused return, information END and real final-report completion.

Current-state replacement/clearing follows STATE-UPDATE-1.0 in the overview. Human resumption follows RESUME-1.0 in SPEC-008; technical recovery cannot bypass its own-receipt checks.

## AI and evidence behavior

No orchestration-model call. Reserve full conservative uncached input and capped billable output before provider dispatch. Include reasoning tokens if billed; a model whose output/usage cannot be conservatively bounded fails the Live gate. Reconcile actual usage atomically; cached tokens are an input subset, not negative input. Missing usage retains reservations, never assumed zero.

At most one transient retry; schema/semantic repair is a separately counted intentional attempt, not a transient retry exemption. Disable or instrument SDK retries/structured-output fallback so every outbound request is counted. No hidden call to “fix JSON”.

## Authorization

Run/correction requests use SPEC-008 persona/capability guards. Batch execution is fixture-only until separately funded. Cancel is local safe-boundary control, not a promise that remote processing/billing is undone.

## UI states

Ready: validated mode/config and remaining limits. Running: real current/last successful node. Wait: human versus missing information distinct. Stopped/cancelled: safe reason, partial artifacts and allowed action. Duplicate command returns existing run. Busy rejects another active review with RUN_BUSY, no queue/paid side effect.

## Reliability and stopping

Reserve attempt+cost+tokens durably before network I/O. A crash/timeout with unknown remote outcome marks OUTCOME_UNKNOWN and retains reservations; no automatic retry/replay after restart. Reconciliation can confirm usage/outcome or leave stopped. A receipt from a completed operation is reusable, not a reason to dispatch again.

Count active time for local/model processing intervals; exclude human wait and explicit paused periods. Persist elapsed/reserved durations; after crash conservatively charge an unresolved call's reserved timeout until reconciled. Boundary checks stop further work; diagnostics/partial read-only rendering remain possible outside further scheduled dispatch. A budget stop is not a loan Reject.

## Analytics

review_started; stage_started/completed/failed; handoff_dispatched/accepted/rejected; review_paused/resumed/skipped; provider_attempt_reserved/completed/unknown; budget_stop; review_cancelled/completed. All carry common identity/version/mode, safe reason, counters and timing, no source text.

## Tests and acceptance

- TEST-007-01: Actual three-core/seven-specialist dispatch/artifacts and dependency checks, not canned timeline.
- TEST-007-02: True/false amount/confidence branches plus SCORE-ROUTING-1.0; Moderate always human, High specialty handling then package review, Very High senior tier. Low cannot waive other gates or critical Live factual support; invalid/missing/stale material score or trigger cannot skip. Fulfilled current referrals resume once without looping; corrections stale dependent handling. Support-only continuation preserves revision/ledger, starts at the earliest affected stage without extraction replay, and cannot reuse stale review tokens or reset active/usage totals.
- TEST-007-03: All cumulative ceilings at equality/overrun, SDK retry accounting, no reset after correction/resume. CONTINUE-CHECK-1.0 verifies planned9/11 and7/9 paths, reviewed11+9=20 equality and safe overrun, with estimates never double-reserved or treated as model cost.
- TEST-007-04: Core fixture runs isolated; a confirmed finished failure releases its execution claim and does not leak state or block the next independent case. An uncertain remote/checkpoint outcome instead remains Recovery required under EXEC-ADMISSION-1.0 until explicit reconciliation; it cannot be treated as a confirmed released failure. The ten-deal workload remains an extension.
- TEST-007-05: Live readiness/failure explicit; fixture/graph-only/inspection zero provider calls. RAGAS judging is disabled by default and absent from app/Fixture/notebook/read paths; explicit offline scoring requires its own compatible adapter/allowance and counted requests, with no hidden five-call projection/default provider.
- TEST-007-06: Unknown paid outcome reserves budget; restart cannot duplicate; active time excludes human wait. PROVIDER-1.0 distinguishes known pre-dispatch failure from possible remote execution; RUN-OUTCOME-1.0 never completes a paused invoke or information END.
- TEST-007-07: Cancel/duplicate/busy/stale commands preserve coherent state and permitted next action. STATE-UPDATE-1.0 clears invalidated current outputs with explicit null/empty lists and preserves durable history/spend; repeated updates cannot duplicate issues.
- TEST-007-08: Correction while awaiting review retires the old pending request, preserves checkpoints/review_id budget and prepares a READY new run/thread with zero graph/provider dispatch on impact preview or Save. Only explicit revalidated continuation starts the allowed stage; old resume is rejected. Approval-only resume keeps its thread and invokes zero model stages. Before explicit continuation, required-path feasibility uses the SAME ledger; insufficient allowance preserves the saved correction/history with no paid dispatch.

Targets: 100% critical routes/control cases, zero unintended inference. Related E-N04, E-P05, E-T03/T04, E-A02/A03.

## Dependencies and implementation boundary

All specialized nodes use shared contracts; persistence/idempotency in SPEC-011; review in SPEC-008. Verify pinned LangGraph interrupt/checkpointer behavior during implementation. No graph, worker, provider or ledger is implemented by this specification.
