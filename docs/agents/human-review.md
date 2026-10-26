# Human Review Instructions

Instruction ID: REVIEW-001  
Version: 1.7  
Execution: Python service and LangGraph interrupt/resume; zero LLM calls  
Requirements: FR-010, FR-014, FR-018, FR-020  
Read with: [Shared contract](shared-contract.md), [Policy](compliance.md), [Evaluation](evaluation.md)

## Trigger and pause

Orchestrator computes threshold_escalation as requested loan_amount_usd >=10,000,000 OR validated confidence <0.7, using unrounded validated values. Final escalate_to_human is that trigger OR a SCORE-ROUTING-1.0 referral OR another mandatory referral. Moderate always requires normal human underwriting. High requires the existing Risk Manager persona's separate credit-risk handling then Authorized Approver package review. Very High requires Authorized Approver with SENIOR review tier; independent specialty/policy handling is still required. Missing material score inputs pause dependent synthesis/readiness rather than inventing a PanelDecision.

True routes to interrupt-based review. False with required gates satisfied goes to Report Generator and records Not required by configured demo rules, never Human approved. Invalid/missing trigger inputs cannot silently take the false branch. Retired SYN-ESC-003 does not create an amount-based referral.

Pause with current thread/deal/run/revision, PanelDecision, all panels, evidence references, required owner/gates, and explicit reasons. No paid work inside the interrupted node; pre-interrupt code can run again on resume.

## Simulated persona responsibilities

Authorized REVIEW-UI-1.0: require comments for every submitted review action, with a separate Add comment option. Analyst/Risk Manager/Compliance Officer/Authorized Approver may request additional information with specific items; record Needs information and retain all existing blockers. Only a current permitted Authorized Approver may record Approve/Reject after required tier and prerequisites pass. Administrator is read-only in this panel. Record simulated reviewer ID/role, exact comments, status and application UTC timestamp in versioned local history; never interpret a request/comment as source support, a final decision, graph resume or report completion. The current local preview is explicitly illustrative and cannot consume/approve actual financial workflow records.

| Persona | Intended responsibility | Boundary |
|---|---|---|
| Credit Analyst | Prepare documents, correct facts, request/provide evidence, notes/ownership handoffs | No final review authority |
| Risk Manager | Inspect supported risks and investigate assigned issues/recommend exception handling | No automatic specialty waiver or approval from role name |
| Compliance Officer | Investigate configured sample-policy/control issues and record permitted handling | No real sanctions/KYC/legal clearance; unmapped capability denied |
| Authorized Approver / existing Reviewer | Record the simulated review disposition on the current package | Cannot waive absent evidence, technical integrity, or specialty blocks by generic acceptance |
| Administrator | Local configuration/support | No default credit-review power |

Use SPEC-008's accepted fine-grained capabilities, numerical exception dispositions and separate record_credit_risk_review command. Credit-risk handling cannot waive a policy exception or missing evidence. NORMAL review cannot satisfy a SENIOR requirement; capability comes from trusted demo configuration, not arbitrary submitted text. No sixth persona is added. A permitted exception requires a separate recorded reason/disposition, not deletion of its violation. The operator can switch personas; attribution is unverified simulation.

## Resume contract

Follow SPEC-008 REVIEW-BASIS-1.0: bind the immutable analytical basis separately from current gate progress/version and the accepted receipt's prerequisite snapshot. Permitted exception/High-score handling against unchanged analysis advances readiness, not a model rerun; analytical/support/source changes still stale the old request. The pending package disposition need not already exist to accept itself. Edited conditions requiring domain support are intentionally saved as exact draft targets before final disposition; permitted reviewers assess those targets and acceptance consumes the same identities. No post-approval regeneration, unchecked condition waiver or self-granted support. Use EXEC-ADMISSION-1.0 to acquire the same-workspace execution claim atomically with actual resume acceptance; Busy records no disposition. STATE-CODEC-1.0 preserves exact persisted basis/values and safe restart behavior. These developer/service contracts add no provider prompt or generation call.

Before the credit-review interrupt, a Live run may separately pause for critical FACT support. SPEC-008's typed FACT/CLAIM support command records current source-backed checks without a fact edit or provider call. Explicit continuation follows SPEC-007; it is not Command(resume=...) on an old credit token. Source support does not satisfy score handling, policy exception disposition or package approval. Corrections of values/sources still create a new analytical revision.

Use the same thread_id and current pending-review operation. The reviewer command includes human_decision, notes, conditions and supported condition_links as applicable. SPEC-008 RESUME-1.0 commits the validated disposition and accepted receipt first; the worker's Command carries only operation/receipt/request IDs and disposition digest, not unrestricted replacement state:

- Approve: record an affirmative simulated disposition separately from PanelDecision.
- Reject: record the negative simulated disposition; it is not an external loan rejection/notice.
- Conditional Approve: record explicit nonblank modified conditions and preserve original model conditions.
- Factual correction: use the correction/revision path rather than editing source facts through notes.

Before acceptance, validate persona/action/capability, deal/run/input revision, pending state, payload, duplicate identity, and unresolved mandatory gates. An issue remains unresolved until required evidence/authorized handling exists.

Apply RESUME-1.0's same-operation RECORDED exception on re-entry instead of failing an unconditional PENDING guard after accepting this very action. All other scope/dependency/capability/gate checks remain mandatory. Duplicate receipt reads schedule nothing; explicit crash-gap recovery verifies current checkpoint/receipt before reusing the same operation. No second disposition, provider replay or automatic restart. A paused invocation or accepted receipt alone is not COMPLETED; use RUN-OUTCOME-1.0.

Use SOURCE-TRIAGE-1.0 in SPEC-008 for issue owner/action: Risk Manager investigates financial/loan source fit, Compliance policy/control applicability, Analyst supplies missing evidence/authorized corrections, Admin coordinates reviewed offline setup. Assignment/acknowledgement adds no clearance power; existing-source uncertainty is not a missing PDF or banking-policy exception. NARRATIVE-CHECK-1.0 extends existing CLAIM assessments to rationale/individual conditions/action explanations with current path/text/source digests and every applicable domain check. Human edits retain separate targets/original history; no automatic extra underwriting gate. INPUT-EDU-1.0 validates commands first. CONTINUE-CHECK-1.0 checks the remaining human-resume/report suffix; original pause is already counted, no model rerun/budget reset.

## Outputs and next step

Store HumanDisposition, actor attribution, original-versus-modified conditions, notes, timestamps/event IDs, and current gate/status outcome. Then generate the report when progression is permitted. Mere review disposition or condition editing adds no model call. Fact correction invalidates affected analysis and may require bounded dependency reruns.

Use CONDITIONS-1.0 with current condition_links for proposed/modified text, origin, category, owner/status and linked existing gates. A Conditional Approve report can retain outstanding supported proposals after required handling/review; it cannot imply fulfillment, funding, covenant compliance or waiver of missing current evidence. A textual condition cannot downgrade a configured prerequisite. Keep source covenants recorded/not automatically evaluated and preserve the original proposal after edits.

## Persistence and audit

MemorySaver/InMemorySaver pauses can resume only while the same in-memory history survives. SQLite is the persistent local-app profile. Neither is immutable audit storage. Record events explicitly and exclude human waiting from active-processing budgets. Do not auto-resume/replay paid nodes after restart.

## Required checks

All dispositions; confidence/amount boundaries and other mandatory referrals; direct-report label; empty modified conditions; wrong persona/unmapped capability; stale/duplicate resume; same-thread requirements; original recommendation preserved; required block not waived; zero inference on review-only resume.

## Analytical correction versus resume

UX-1.0 uses a read-only correction-impact preview, Save correction, then a distinct explicit Update affected findings command. Saving records provenance/revision/invalidation and prepares a READY run/thread with the same review budget; it dispatches no graph/provider work. Current prerequisites and possible model work are explained before continuation; unavailable estimates remain Unavailable. Preserve the original recommendation/human disposition and actual prior terminal history. Review-only disposition and condition edits keep their existing zero-inference resume semantics.

Follow [SPEC-007](../specs/orchestration-budgets.md): an analytical correction supersedes the old run/review, creates a new revision/run/thread and starts at the earliest affected stage with the same review allowance. Do not resume an old interrupt with changed financial inputs. Only unchanged-analysis review disposition/condition editing resumes that pending thread. Risk Manager handling can record RECOMMEND_REJECT with evidence; it preserves the original Exception and does not waive unrelated gates. See [E-F03](../evaluation/examples/e-f03-reject.md).
