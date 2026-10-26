# Orchestrator Instructions

Instruction ID: ORCH-001  
Version: 1.6  
Execution: Deterministic LangGraph state machine; zero planning LLM calls  
Requirements: FR-008, FR-011, FR-013–015, FR-018–020  
Read with: [Shared contract](shared-contract.md), each dispatched role, [Evaluation](evaluation.md)

## Purpose and rationale

Demonstrate actual delegation, dependency coordination, state handoffs, failure/review routing, and completion for three core agents. Do not spend a model call choosing a known sequence.

Agent 1 = Extractor. Agent 2 = Compliance. Agent 3 Risk & Summary = Risk Quantifier + explicit Synthesizer. Financial, Evidence, and Memo/Report Generator support them.

## Normal workflow

1. Intake validates the package and selected fixture/live/policy configuration.
2. Extractor produces validated current-revision facts: normal LLM call one.
3. Financial computes supported metrics; Compliance evaluates applicable sample rules.
4. Risk Quantifier directly computes supported flags/gaps and the versioned educational score/band when all factor assessments and material source inputs are valid.
5. Check required panels/revision/evidence prerequisites. Missing/invalid mandatory inputs pause dependent work, not force a PanelDecision.
6. Synthesizer reads all three panels once: normal LLM call two.
7. Evidence checks accepted references/numbers/critical support; invalid output follows bounded repair or review-needed stop.
8. Python recomputes the amount/confidence trigger plus SCORE-ROUTING-1.0 and other mandatory referrals. Moderate always requires normal human underwriting; High requires Credit Risk Manager handling then Authorized Approver review; Very High requires that existing Approver persona's SENIOR tier. Low cannot clear independent gates. Insufficient Data pauses dependent synthesis/readiness, never silently takes a no-review branch.
9. Route true to Human Review; route false only when required gates permit.
10. Report Generator assembles the final Markdown from current validated state and any accepted disposition.

The term loan_amount in routing means validated requested amount, not substituted portfolio exposure. Use SAMPLE-LOAN-POLICY-1.0; retired SYN-ESC-003 cannot trigger. Preserve all other mandatory issue reasons and affected dependencies.

Authorized SME fixes: complete reviews require a registered reviewed case/assessment/subject pack; unregistered synthetic Live uploads execute only supported partial work. Check entity/facility coherence and critical Live FACT-SUPPORT-1.0 permissions at existing edges. Pending support pauses affected trusted work before finance; source-quality review is not the later credit-approval interrupt. Saving scoped support invokes nothing; explicit same-input-revision continuation uses a new run/thread at the earliest affected stage and the same ledger, with no extraction replay or stale review reuse. See SPEC-007. Keep source support, numerical exception handling, score handling and final disposition separate. CONDITIONS-1.0 cannot turn a missing prerequisite into an acceptable future condition. No added graph node/model stage or budget.

## Contract and dispatch guards

Apply SPEC-007 EXEC-ADMISSION-1.0 before actual app/notebook/CLI execution against the same database, using the existing durable operations claim rather than only a process-local worker. Busy has no graph/provider/embedding dispatch; uncertain claims require explicit reconciliation, never time/PID-based stealing. REVIEW-BASIS-1.0 separates valid review progress/condition-draft support from changed analytical dependencies; draft metadata alone dispatches nothing. Restore STATE-CODEC-1.0 types before routing/hashing; do not reconstruct confidence through binary floats or revive an explicitly cleared current artifact. The exact Extractor Runtime prompt must match DealTermsWire and its reviewed instruction/schema/fixture identity. Keep these development rules outside model-visible runtime sections.

Validate deal/run/input revision, expected role/schema, source/metric/policy versions, allowed state transition, operation identity, and budgets before dispatch. Record sender/recipient, accepted/rejected handoff, stage outcome, and artifact references. A decorative timeline over a canned answer is insufficient.

Shared typed state is the local communication mechanism. No message broker, arbitrary planner, swarm, or independent framework is needed. SPEC-007 defines scheduled node IDs and routing; executable schemas remain implementation work. Apply STATE-UPDATE-1.0 replacement/clearing, CANON-1.0 scoped dependencies and PROVIDER-1.0 normalized outcomes. Model output never owns authority or current-state identity.

Apply CONTINUE-CHECK-1.0's small supported-path table, not a planner: initial direct/reviewed9/11, Financial correction7/9, already paused review2 more nodes. Use the current ledger/entry and longer applicable branch before routing is known; actual dispatch counts remain authoritative. Check required-path feasibility before explicit continuation/resume; estimates reserve nothing and imminent node/tool/provider work is counted/reserved once. Reviewed11 plus correction9 reaches20 with no retry headroom; recovery overrun stops truthfully with saved partial/history, not hidden nodes/new allowance/financial Reject. Two normal model stages do not imply two requests in Fixture mode; Fixture makes zero requests, while actual graph work still counts. Apply INPUT-EDU-1.0 before trusting external JSON and SOURCE-TRIAGE-1.0 ownership without creating clearance capabilities. NARRATIVE-CHECK-1.0 covers every model narrative field before final acceptance.

## Boundaries and failures

- One active review initially; bounded independent fixture batches use distinct thread/run/deal identities.
- Graph construction, Jupyter display, UI refresh/filter/navigation, owner/note changes, and report preview do not invoke models.
- Fixture outputs require a matching scenario/source lineage; live errors never silently become fixture success.
- Count actual child nodes/tools and every model attempt. A wrapper or resume cannot reset/hide usage.
- Stop dispatch on timeout/budget/cancel/integrity failure and preserve validated partial artifacts with a reason.
- Cancellation is acknowledged at a safe boundary; do not claim a running remote request has vanished.
- Uncertain paid calls retain reservations; no silent crash replay.

## Review and correction

Keep paid work upstream of interrupt. Validate current pending thread/revision/persona, required review tier, score/configuration lineage and idempotency on resume. Credit Risk Manager handling satisfies only its current High-score referral; numerical policy exceptions and final package disposition remain separate. Use the existing pending-review service, not an additional graph/model stage. Once all current requirements are satisfied, resume without creating an endless review loop. Review-only disposition/condition edits proceed to Python reporting without unchanged model reruns.

Fact/source/policy changes invalidate affected metrics, findings, synthesis, reports, and stale review acknowledgement. Rerun only dependencies within cumulative budgets; if insufficient, stop rather than silently start a new allowance.

## Resume and lifecycle interpretation

Follow SPEC-008 RESUME-1.0: durable disposition/receipt acceptance precedes worker resume, and the repeated human node can reuse only its own exact accepted receipt after all current checks. A changed/competing/stale operation is denied. Preserve the stable interrupt position and JSON payload, no paid work before it and no broad exception catch that swallows the pause. Graph return is interpreted under RUN-OUTCOME-1.0: interrupt means WAITING_REVIEW, information END means WAITING_INFORMATION, and only a current report with satisfied gates means COMPLETED. Explicit reconciled recovery never replays a model or resets spend.

## Persistence and observations

Choose configured MemorySaver in-process profile or SQLite persistent-app profile per run. Neither promises immutable/full external traces. Record actual events explicitly. Do not include secrets or raw sensitive payloads.

## Required checks

Three core-agent contracts and seven responsibility outputs; actual handoffs; normal/exception/missing/conflict paths; graph-only zero calls; two normal live calls; five-attempt ceiling; amount/confidence routing; correction invalidation; no-review label; duplicate/stale actions; invalid gates; independent fixture runs; sample report linked to executed state.

## Review-fix continuation and budget contract

Use the service-controlled START routing and correction transition table in [SPEC-007](../specs/orchestration-budgets.md). New analytical revisions use a new run/thread but the original review ledger; old review tokens become stale. Review-only resumes stay on the pending thread. Protect the [SPEC-006](../specs/context-optimization.md) one-synthesis correction reserve before optional repairs. An unavailable registered current-input fixture is an explicit stop, never canned success or automatic Live fallback.
