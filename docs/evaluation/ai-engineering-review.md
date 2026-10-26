# Deal or No Deal AI — Multi-Agent, Grounding and LangGraph Engineering Review

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.5  
Review date: 2026-10-23  
Status: Historical review refinements adopted; M1 foundation checks passed; full workflow/model/retrieval validation pending  
Original reviewed baseline: PRD v1.30; HLD v1.23; SPEC-005 v1.4; SPEC-006 v1.6; SPEC-007/008/011 v1.4; evaluation plan v1.11  
Scope: A five-day educational local prototype, preserving the agreed architecture and budgets

Current follow-up, 2026-10-23: M1's43 foundation methods/build passed as recorded in the [execution evidence](../execution.md#m1-implementation-evidence); the original review's Not run statements describe that earlier review stage, not current foundation status. Full financial/retrieval/model/UI evaluation remains unrun. The user subsequently adopted the [source-ready/four-baseline/conditional-reranker sequence](hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision): report DIRECT, KEYWORD, VECTOR and HYBRID first, identify actual ranking failures, then consider a separate reranker only if quality benefit justifies added processing. VECTOR-only is the semantic retrieval baseline; RRF is fusion. Keep the capability status/evidence dimensions distinct.

## Current Principal follow-up resolution — 2026-10-23

The user authorized fixing the subsequent Principal review. The current [PRD](../product/prd.md), [HLD](../architecture/hld.md) and canonical feature contracts specify the fixes below. This records DOCUMENTATION_FIXED, not implemented or passing behavior. Historical sections below retain their original review baseline; current linked contracts govern implementation.

| Finding / failure risk | Adopted source of truth | Required evidence still pending |
|---|---|---|
| Extractor Runtime instructions asked for richer domain data/notes than strict wire allows | [Corrected Runtime prompt](../agents/extractor.md#runtime-prompt), SPEC-002 and PRD8.3/8.9 now name DealTermsWire, exact roots/fields, null/conflicts and Python hydration | Actual loaded-prompt/schema/example checks, updated instruction/fixture hashes and selected-provider size/schema proof |
| Legitimate review handling could be confused with analytical dependency changes | [REVIEW-BASIS-1.0](../specs/human-review-corrections.md#analytical-basis-versus-review-progress--review-basis-10): separate analytical basis versus current prerequisite gate version/snapshot, accepted receipt/self-consumption and source-change invalidation | E-P01/E-F03 handling-after-pause, stale gate payload/source change, competing receipt and correct completion tests |
| A process-local worker does not admit separate app/notebook/evaluation processes | [EXEC-ADMISSION-1.0](../specs/orchestration-budgets.md#shared-execution-admission--exec-admission-10): one atomic SQLite-backed active slot in existing operation/run records, Busy rollback, safe release and explicit uncertain recovery | Independent-process contention, pause/reacquire, no disposition on Busy, no claim stealing/default replay tests |
| Exact values/types/fingerprints may drift through artifact/checkpoint serialization | [STATE-CODEC-1.0](../specs/persistence-observability.md#exact-checkpoint-and-artifact-representation--state-codec-10): schema-known primitive encoding, exact Decimal/confidence restoration, explicit clear semantics, noncircular parent-content projection | Pinned saver/restart/codec round trips,0.7/score boundaries, fingerprint equality, wrong-version rejection and null-versus-zero/clears |

The targeted follow-up also found and resolved an edited-condition sequencing ambiguity: required semantic-support targets must exist before the package disposition is accepted. SPEC-008's existing editor saves an exact condition draft, existing role-specific CLAIM support binds that draft, and final acceptance consumes the same reviewed identities. This prevents a condition-support/approval loop without another screen, table family, model call or banking rule. It remains a planned test path under TEST-008-03/06/07 and TEST-010-03/05, not an observed failure or executed fix.

Consolidation rule: canonical schemas live in the relevant feature contracts; only allowlisted Runtime sections/shared rules reach a provider. Update the dependent prompt/example/hash/profile and focused tests together; do not append every historical correction to model context. Existing90 TEST IDs/30 case designs/23 metrics/25 UI criteria and all token/cost/node limits remain. Repository/first-milestone approvals, package/parser/SQLite compatibility, reviewed synthetic source/factor/authority/fixture authoring, and later Nebius model/token/rate/access/allowance proof remain pending. No additional confirmed critical specification conflict was found in this targeted follow-up; that is a bounded document-review conclusion, not proof that the unimplemented application is defect-free or ready to demo.

### Critical evidence still pending

The user requested adding these remaining prerequisites in simple ordered steps. Use the single [PREREQ-01–08 checklist and evidence record](../specs/overview.md#implementation-prerequisites-and-required-evidence) instead of duplicating a second readiness table here. It covers existing approvals; compatible exact persistence/admission; prompt/context/wire agreement; reviewed synthetic source/case preparation; actual core fixture branches; user-facing citations/notebook/HTML/usability; separately funded Nebius verification; and separately selected optional RAGAS/hybrid execution. Each item states dependencies, suggested owner, required proof, existing test families and the reason for its order.

All runtime results remain Not run. Approval is pending at the existing gates; local implementation/case authoring is not started, Live is not configured, and optional execution is disabled/planned. A VERIFIED mark requires actual scoped evidence, not this documentation update. The later Phase 5 plan will translate prerequisites into approved small implementation tasks; it is not created or approved here.

No other confirmed critical specification defect was identified in this focused reconciliation. Implementation compatibility and end-to-end evidence above remain material blockers to claiming a working demo, not reasons to add more agents or production infrastructure. Unknown dependency/provider behavior must be measured and reported at its actual milestone.

## Resolution status — authorized fixes, 2026-10-23

The user requested fixing the Principal AI Engineer's recommendations. All seven findings are now DOCUMENTATION_FIXED in PRD v1.31, HLD v1.24 and dependent feature/agent/evaluation contracts. This means the missing implementation contracts are specified, not that an application was built or tested. Sections 1–4 preserve the original review evidence/gaps as of the historical baseline above; use the canonical contracts below for current behavior.

| Finding | Adopted contract / source of truth | Verification status |
|---|---|---|
| AE-01 | [SYN-WIRE-1.0](../specs/synthesis-evidence.md#compact-synthesis-wire-and-trusted-hydration--syn-wire-10): complete ordinary/Conditional examples; Python-owned metadata/support/authority; exact five-field domain decision | Document/JSON checks only; runtime schema/token fit pending |
| AE-02 | [CANON-1.0](../specs/context-optimization.md#canonical-identities-and-fixture-references--canon-10): exact typed fingerprints, ordered/set semantics and current logical reference mapping, no approval rebinding | Contract specified; fixture/cache implementation pending |
| AE-03 | [RESUME-1.0](../specs/human-review-corrections.md#review-acceptance-and-graph-resumption--resume-10) and [RUN-OUTCOME-1.0](../specs/orchestration-budgets.md#invocation-result-and-lifecycle--run-outcome-10): accepted receipt versus graph completion, own-operation replay and explicit lifecycle | Contract specified; pinned SQLite/interrupt recovery checks pending |
| AE-04 | [COVERAGE-1.0](../specs/context-optimization.md#coverage-inventory-and-multi-page-evidence--coverage-10): original-span inventory, parser/packing/meaning separation, two-page table and qualified clause examples | Contract specified; parsed sources/navigation checks pending |
| AE-05 | [PROVIDER-1.0](../specs/orchestration-budgets.md#normalized-provider-outcomes--provider-10): refusal/truncation/transport/usage normalization and conservative uncertain-call handling | Controlled response and selected-model verification pending |
| AE-06 | [STATE-UPDATE-1.0](../specs/overview.md#current-state-replacement-and-invalidation--state-update-10): explicit replace/clear/preserve table, stale current outputs cleared, history/spend retained | Contract specified; graph/state regression checks pending |
| AE-07 | [EVAL-CUTOFF-1.0](evaluation-plan.md#original-ai-output-versus-reviewed-workflow--eval-cutoff-10): original AI output versus human-corrected workflow and honest attempted/accepted denominators | Evaluation design updated; all model-quality results Not run |

The [evaluation regression table](evaluation-plan.md#authorized-engineering-regressions-and-evaluation-cutoff) and [traceability](../traceability.md#principal-engineering-fix-coverage) map these to existing TEST families/metrics. No additional test IDs or independent case inventory were introduced. Remaining prerequisites are actual case/source/factor/fixture authoring, repository/execution approval, parser/license/dependency compatibility and verified selected Nebius model/tokenizer/rates plus later local key/explicit allowance. Two normal calls, unchanged cumulative budgets, DIRECT grounding, optional offline retrieval benchmark and no automatic expiry remain.

## 1. Assessment and review method

The architecture is suitable for the agreed demonstration: one bounded LangGraph workflow, typed specialist handoffs, two normal model-backed stages, deterministic calculations/policy/risk/reporting, explicit source support and credit review, and local persistence. The remaining technical risks are contract precision at boundaries. They do not justify more agents, a different framework or default vector retrieval.

The workspace contains documentation only. No source package, application, LangGraph execution, installed dependency set or provider integration is available to test. Findings below describe specification ambiguities and plausible failure modes, not observed runtime defects. No general production-readiness assessment or firm-specific banking policy is implied.

Review steps:

1. Establish the current product/data/permission/cost boundaries, including the recently authorized SME and citation refinements.
2. Trace ingestion -> passage selection -> Extraction -> support/financial/policy/risk panels -> Synthesis -> Evidence -> routing -> human review -> report.
3. Follow the alternative paths: missing input, source-support continuation, correction, stale action, interrupted review, provider failure and restart.
4. Inspect each boundary for exact schema, authority, identity, provenance, state-update and stopping behavior.
5. Compare framework/provider behavior with primary documentation and recommend the smallest useful clarification plus an observable acceptance check.

Reviewed sources include [PRD](../product/prd.md), [HLD](../architecture/hld.md), [shared contracts](../specs/overview.md), [Extraction](../specs/extraction.md), [Synthesis/Evidence](../specs/synthesis-evidence.md), [context/grounding](../specs/context-optimization.md), [orchestration](../specs/orchestration-budgets.md), [review/corrections](../specs/human-review-corrections.md), [persistence](../specs/persistence-observability.md), [repository proposal](../architecture/repository-design.md), [evaluation plan](evaluation-plan.md), specialist instructions and the [hybrid benchmark](hybrid-retrieval-benchmark.md).

## 2. Confirmed design versus unresolved work

| Area | Confirmed / already covered | Review conclusion |
|---|---|---|
| Delegation | Extraction, Compliance and composite Risk/Summary core roles; seven specialist responsibilities | Retain the explicit workflow; three roles do not require three independent LLM loops |
| Inference | Extraction plus Synthesizer normally; no planning/judge/report model | Appropriate cost control; complete Synthesizer wire needs precision under AE-01 |
| Financial and policy logic | FIN-1.0 Decimal calculations, synthetic rules, missing/conflict controls and approved human routes | No new financial thresholds or predictive credit model needed |
| Grounding | DIRECT full bounded source selection and deterministic policy/reference lookup | Evidence-grounded generation without a vector retriever; do not imply deployed semantic search |
| Chunking | SEG-1.0 structure-aware clauses/sections/table groups/rules with context-preserving overlap | Retain proposed sizes; define coverage and multi-page location mechanics under AE-04 rather than changing numbers without evidence |
| Retrieval extension | Offline BM25, vector and RRF-hybrid comparison through RET-1.0; later ADR-007 selects local-file/Nebius-hosted-embedding/SQLite vectors under ADR-008 | Keep isolated from startup and full extraction; architecture selected, setup unverified and adapters/results pending |
| Trust | Critical Live Fact support, separate credit disposition, typed conditions and CITEVIEW-1.0 | Important controls already exist; model-output trust boundary still needs AE-01 precision |
| Persistence and recovery | SQLite app/saver boundary, idempotency intent, explicit events, uncertain-call reservation, no silent paid replay | Sound direction; define resume ordering and exact field updates under AE-03/06 |
| Privacy | Synthetic data, scoped sources, no secrets in state/logs, disabled hosted tracing by default | Preserve safe event/read projections; no raw state streaming is required |
| Evaluation | Fixture/Live distinction, core versus extension, risk recall plus offline false positives, supported Reject | Preserve this scope; explicitly score original AI output separately from corrected state under AE-07 |

Already acknowledged prerequisites are not newly discovered gaps: case/source/factor/fixture authoring; repository approval; execution/design-system planning; parser licensing; compatible pinned packages; chosen Nebius model, schema/tokenizer/rates; later local credentials and funded Live allowance. Their current status is Pending, not Failed or verified.

## 3. Prioritized findings

Priority A means settle the contract before implementing that path, because normal demo behavior can become inconsistent or misleading. Priority B means make the adapter/state/evaluation detail explicit before its relevant demo milestone. These priorities are engineering review recommendations, not application risk severities.

| Finding | Priority | Boundary gap | Smallest useful adjustment |
|---|---|---|---|
| AE-01 | A | Synthesizer output has no complete compact wire/trusted-hydration contract | Define the provider-facing fields versus Python-owned claim IDs, support status, criticality and metadata; measure the complete payload within existing caps |
| AE-02 | A | Semantic digest and fixture reference binding are described but not fully canonicalized | Define stable semantic projection/serialization and deterministic fixture reference rebinding |
| AE-03 | A | Credit-review commit/resume ordering and worker pause classification remain implicit | Specify the local operation sequence, allowed same-operation recovery and terminal/pause outcome mapping |
| AE-04 | A | Coverage COMPLETE and multi-page passage resolution lack a precise shared meaning | Define source-span coverage separately from interpretation quality and expand passage references to every contributing location |
| AE-05 | B | Nebius adapter response/error classification lacks a field-level contract | Normalize completion/refusal/truncation/transport/usage outcomes before accepting domain JSON |
| AE-06 | B | State ownership is defined but per-key update/clear rules are not | Write a replacement/reset table for existing channels; avoid unnecessary merging reducers |
| AE-07 | B | Extraction/narrative quality measurement stage is not explicit enough after human edits | Score immutable model outputs before correction separately from final reviewed workflow correctness |

### AE-01 — Compact Synthesizer wire and server-owned authority

Evidence: SPEC-002 provides a complete DealTermsWire example and Python hydration. SPEC-005 names SynthesisResult with executive_summary, financial_interpretation and risk_summary as lists of the shared Claim type, alongside PanelDecision, condition links and optional proposed_action. Claim includes generated IDs, criticality and support_state, including HUMAN_SUPPORTED. A corresponding complete SynthesisWire/provider-field allowlist is absent. Existing rules say Python derives criticality and human support is separately recorded, but the exact nested schema ownership is still ambiguous.

Impact: one implementation could ask the model to generate trusted metadata/statuses; another could reject legitimate responses because required generated fields are missing. Repeated claim objects can also make the proposed 350-output-token synthesis target unrealistic. This is an unmeasured feasibility risk, not a measured overflow or a reason to increase budgets now.

Recommended fix: define a compact SynthesisWire with only decision/narrative/reference/proposal content needed from the existing call. Python generates identity/provenance, derives criticality, initializes permitted support state and verifies effective escalation. A model-proposed HUMAN_SUPPORTED/actor/permission field must be rejected or excluded, never accepted as authority. Preserve the exact five-field domain PanelDecision, with any envelope outside it. Use current allowed evidence handles and specify local expansion into full domain records. Do not add a third call.

Acceptance: complete ordinary and Conditional payload examples hydrate correctly; model-supplied support/identity/permission fields cannot grant authority; all three panels remain represented; the exact request/schema/output and protected correction path fit the selected tokenizer/profile or Live remains unavailable. Extend existing TEST-005-01–06 and TEST-006-04/08, not the scenario count.

### AE-02 — Canonical semantic identity and fixture binding

Evidence: fixture keys use normalized current-stage input digests excluding generated run/artifact IDs, and caches use dependency versions. The contracts do not enumerate the stable projection, canonical Decimal/text/list serialization, or treatment of generated fact/claim/correction/support IDs and their internal references. Synthesis fixtures must reference findings that may receive fresh runtime IDs.

Impact: identical semantics may fail fixture matching after a restart/correction because fresh UUIDs differ. Removing too many fields could instead reuse a stale result after a meaningful source/support/policy change. A cached/fixture payload can pass its input key yet retain references to another run's generated objects.

Recommended fix: define one canonicalization contract used by fixture keys, dependency checks and payload hashing, with clearly distinct scope/semantic identities where needed. Specify canonical Decimal representation, object-key ordering, semantic versus ordered-list treatment, relevant null/status values, and the exact source/policy/basis/subject/support/instruction/schema/model dependencies. Preserve meaning-bearing source text; do not normalize away conflicting numbers or qualifiers. Stage fixtures use stable logical evidence handles that Python resolves into current scoped references, without consuming evaluator gold. Never rebind an old human disposition or silently broaden deal scope.

Acceptance: a replay with new incidental UUIDs but identical permitted semantics matches and binds only current refs; changes to material value, source, support status, subject scope, policy or instructions invalidate/reject as appropriate. Unknown/stale fixture handles fail closed. Extend TEST-002-06/07, TEST-006-05 and TEST-007-08.

### AE-03 — Resume transaction sequence and actual outcome mapping

Evidence: SPEC-008 validates before resume and inside the resumed service; resume_review produces HumanDisposition plus a receipt and Command(resume=...). SPEC-011 correctly states app/checkpointer commits are separate. The exact ordering of intent, disposition commit, graph resume, current-pending checks and same-operation receipt reuse is not defined.

Impact: if the app marks a review RECORDED before invoking the graph, the rerun human node could fail its own pending-state guard. If it commits after resume without a durable operation identity, a crash gap can produce duplicate or lost disposition effects. A worker can also wrongly label a returned interrupted invocation as completed if its state mapping is implicit.

Recommended fix: specify a short local sequence for validation/reservation, execution, accepted disposition and receipt/checkpoint reconciliation using existing tables/services. Distinguish the pending review's ownership from the same reserved/committed operation's legitimate replay, while rejecting every other stale/duplicate-changed request. Map graph interrupt, explicit information stop, failure/cancel and final validated report to their application lifecycle states. Define human-node reentry, serializable interrupt payloads and exception boundaries; generic error handling must not swallow the graph's interrupt signal.

Acceptance: normal pause/resume; an interruption is WAITING_REVIEW, not COMPLETED; support/data pause is WAITING_INFORMATION; crash before/after disposition commit and before checkpoint; same-operation recovery produces one disposition/report and zero new model calls. No remote or multi-service transaction system is needed. Extend TEST-007-02/06/07, TEST-008-04/07 and TEST-011-02–04.

Framework basis: LangGraph documents node reentry on resume, idempotent pre-interrupt side effects, JSON-serializable interrupt payloads and an interrupt result from invoke. Its guidance warns against broad exception handling around interrupt. The proposed local sequence is an engineering recommendation for this app, not a transaction API supplied by LangGraph. [Official interrupt guidance](https://docs.langchain.com/oss/python/langgraph/interrupts).

### AE-04 — Coverage semantics and multi-page citation expansion

Evidence: ContextPacket requires mandatory_evidence_coverage and EvidenceSelection can be COMPLETE/INCOMPLETE/UNVERIFIED. SEG-1.0 requires linked definitions, table headers/notes, conflicts and all contributing page locations. SourceRef's DOCUMENT form describes a page_number and passage_id, while the model returns passage IDs. A precise coverage algorithm and one-passage-to-many-page hydration contract are not yet specified.

Impact: COMPLETE could mean all known required references, all parsed source content or semantic correctness, which are different claims. A correctly retrieved row may lose a header/qualifier from the preceding page. Showing only the first location can undermine the newly required citation-validation experience.

Recommended fix: define coverage against a versioned source-span/block inventory and reviewed required/related passage sets. FULL_EXTRACTION must preserve the faithful bounded package; checking only fields the model already extracted is not enough. Treat parser/source fidelity, packed-context coverage and model interpretation as separate statuses. Represent contributing page/offset/row locations explicitly and expand one selected passage handle to all required locations/context. Existing CITEVIEW highlighting fallback remains truthful. A larger parent context that exceeds the hard allowance stops rather than being silently dropped; no vector migration is implied.

Acceptance: a two-page table whose header/units/period are on page one and a value/footnote on page two; a split clause with its qualification on the next page; an omitted required span/definition; preserved conflicting sources; source/version mismatch; packed evidence overflow. All locations survive context packing, hydration and click-through. Extend TEST-001-04, TEST-006-02/03/09 and TEST-010-03; use focused variants, not another independent loan corpus.

### AE-05 — Provider completion and error normalization

Evidence: the repository proposes HTTPX and strict schemas; retry/timeout/usage budgets are already explicit. There is no complete field-level provider adapter result specifying how finish reason, refusal, empty/malformed choices/content, unsolicited tool calls, missing usage and transport uncertainty become accepted, paused or stopped stage results.

Impact: valid-looking JSON may be accepted without checking completion state, or a legitimate refusal could be treated as repairable JSON and spend another attempt. Accounting can become inconsistent if usage reconciliation depends on successful domain parsing.

Recommended fix: define a small normalized provider response/error contract carrying request identity, completion/refusal/truncation outcome, structured content, safe provider status, independently reconciled usage and transport certainty. Default to non-streaming single completion for this bounded prototype. Validate actual selected-model capabilities and schema behavior; no hidden SDK retry or fallback to weaker JSON mode. Process usage/reservations even when content fails. Pin limits/deadline/error mapping at the adapter boundary, retaining existing caps and deliberate retry policy.

Acceptance: controlled success, refusal, empty response, valid JSON with non-successful termination, truncation, invalid schema, unsupported tool response, bounded rate-limit handling and uncertain timeout. None becomes a financial Reject; every actual attempt and known/unknown usage is accounted for. Extend existing TEST-002-06, TEST-005-06 and TEST-007-03/05/06 with controlled transports before any funded Live smoke test.

Nebius documents schema-following and arbitrary-JSON modes as different choices, model-dependent structured-output capability and explicit refusal handling. This confirms the need to verify the selected profile; it does not verify any model for this application. [Official structured-output guidance](https://docs.tokenfactory.nebius.com/ai-models-inference/json).

### AE-06 — State update and clearing semantics

Evidence: the shared state names owners and says nodes replace current artifact references through validated patches. This is a useful principle, but no per-key replace/clear/preserve contract describes issues, errors, routing, pending review, PanelDecision and report fields across retries and new-run snapshots.

Impact: a merging list can duplicate issues during reentry; an empty update may fail to clear old errors or routing. A broadly copied snapshot could leave an invalidated decision/report visible as current despite the intended revision rules.

Recommended fix: add a small update/reset table for existing state keys and use default replacement for single-owner current references wherever possible. Explicitly clear invalidated fields, preserve immutable artifact history through references and leave durable events/budgets in their existing repositories. Do not add append-only conversation state or a custom reducer framework for this sequential graph. Test actual pinned LangGraph behavior before choosing implementation-specific reset helpers.

Acceptance: two repeated updates produce no duplicate current issues; clearing a stop/error/decision/report really clears it; changed support/source/policy removes dependent current views while history and spent allowance remain. Extend existing TEST-007-07/08 and TEST-011-01/02. Official documentation distinguishes default replacement from merging reducers and explains that an empty update need not clear a merged field. [Official graph-state guidance](https://docs.langchain.com/oss/python/langgraph/graph-api).

### AE-07 — AI quality before human correction

Evidence: the evaluation plan says to score actual model outputs and preserve correction history, but MET-03's extraction population and narrative-evaluation cutoff are not explicitly tied to immutable pre-correction artifacts versus final corrected state. Critical Live inputs now receive human source support before trusted downstream use.

Impact: scoring the final corrected Fact set can overstate extraction accuracy; omitting stopped/refused cases can hide model failures. A reviewed report's correctness and the original model's quality answer different questions.

Recommended fix: bind extraction scoring to the accepted original extractor artifact and annotated field slots before reviewer correction. Score the original accepted Synthesizer proposal separately from any human-edited conditions/disposition. Keep final reviewed workflow correctness, support quality and correction outcomes as separate existing evaluation dimensions. Include missing/refused/stopped attempts and disclose conditional denominators; do not give a rejected/unavailable artifact a successful score. Runtime source-support records and evaluator gold remain separate.

Acceptance: an extractor omits documented CFADS in E-N01/extraction-miss, the original extraction metric counts the miss, and the corrected workflow can still succeed. E-M01 genuinely missing CFADS is scored according to missing-data handling, not fabricated extraction success. A human-edited condition does not overwrite the model proposal's evaluation. Use existing TEST-011-07, E-N01 correction, E-M01 and evaluation rubrics; no new dashboard, model judge or paid batch.

## 4. RAG and orchestration recommendations

Keep the current default:

~~~text
Synthetic documents + trusted policy/case configuration
  -> parse/segment with preserved source locations
  -> DIRECT faithful evidence packet
  -> Extraction (model call 1)
  -> required source support / deterministic finance-policy-risk
  -> Synthesis (model call 2)
  -> evidence checks / conditional credit review
  -> pure Python report
~~~

This is evidence-grounded generation with direct source selection; it is not a deployed vector-search RAG application. The optional benchmark already has keyword, vector and hybrid arms, scope filtering, deterministic RRF, separate packing coverage and embedding/generation token accounting. Those are sound boundaries. No change to the approved chunk targets/overlaps or embedding selection is warranted from document review alone.

Keep custom deterministic StateGraph coordination. The initial core and four-arm retrieval comparison need no supervisor planning call, ReAct risk loop, swarm, extra financial narrative model, separate reranker or tool broker. The later conditional reranker experiment follows the measured decision above; this is not a permanent ban or a selected runtime model. LangGraph nodes can be ordinary Python or model-backed functions; clear contracts and observed handoffs matter more here than autonomy. [Official graph guidance](https://docs.langchain.com/oss/python/langgraph/graph-api).

Keep safe persisted event/read projections for Activity. Do not assume that a private graph channel is automatically redacted if a later developer adds raw state streaming; select safe fields explicitly. Current docs already keep secrets out of graph state and hosted tracing inactive. This is implementation guidance, not a new tracing feature. [Official graph schema/streaming discussion](https://docs.langchain.com/oss/python/langgraph/graph-api).

Keep SQLite for the local app and an in-memory saver only for the stated notebook/test profile. Checkpoints are thread-scoped state, not an immutable complete audit; this is already correctly documented. Preserve the user's no-automatic-expiry rule; no cleanup schedule is recommended by this review. [Official persistence guidance](https://docs.langchain.com/oss/python/langgraph/persistence).

## 5. Smallest useful next work

Original sequencing recommendation; steps 1–4 are now specified by the authorized fix above, with runtime work still gated:

1. Specify AE-01/02 together: compact SynthesisWire, trusted hydration, stable logical references and canonical dependency/fixture identity.
2. Specify AE-03/06 together: one concrete pause/resume/receipt sequence and current-state replacement/reset table.
3. Specify AE-04: deterministic coverage/location contract and two focused cross-page examples.
4. Specify AE-05/07: normalized provider outcomes and pre-correction AI-evaluation cutoff/denominators.
5. Carry those refinements into the already pending repository/execution gates and first compatibility/budget-feasibility milestone. Author core source/factor/fixture packs, then implement focused controlled tests; only later perform the explicitly funded Nebius smoke run.

Use existing planned test families and cases. The review has seven findings, four Priority A and three Priority B; it does not create new runtime tests, change the existing ninety planned IDs, extend the thirty-case inventory, mandate full optional benchmarks or increase budgets. Two normal model calls, five total attempts, 8,000 input/2,000 billed output, USD0.10 target/USD0.25 hard ceiling and the five-day educational scope remain the baseline.

The compact synthesis fields, canonical identity rules, resume/disposition ordering, coverage inventory/location structure, provider normalization contract and evaluation cutoff are now specified in the resolution table. Exact third-party model/API response mapping, pinned framework/checkpointer behavior, parser fidelity and complete payload token feasibility still require implementation-stage evidence. Unknown provider capabilities are not invented or claimed verified.

Version 1.0 created only the original review. Version 1.1 records the user's authorized fixes across active PRD/HLD/specifications/agent instructions/evaluation/traceability and pending repository guidance. Primary framework/provider documentation informed the review; static document/illustrative JSON checks do not establish compatibility, token fit, financial output, runtime recovery, latency/cost or AI quality. No package installation, paid API call, source fixture, application, notebook, HTML, deployment or external repository was created by these refinements.
