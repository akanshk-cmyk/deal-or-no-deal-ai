# Memo / Report Generator Instructions

Instruction ID: REPORT-001  
Version: 1.3  
Execution: Pure Python; zero LLM calls  
Requirements: FR-009, FR-016–017, FR-019–020  
Read with: [Shared contract](shared-contract.md), [Evaluation](evaluation.md)

## Purpose and rationale

Assemble a readable report from validated state without another model call. This is Memo's implementation responsibility, not another writing/planning agent.

## Inputs

Current deal/run/input revision/mode, validated terms, Financial/Compliance/Risk outputs, accepted Synthesizer summary/PanelDecision, EvidenceReview, conditions/provenance, issue owners/gates, optional HumanDisposition, explicit audit events, template version, and supplied cutoff/generation metadata.

## Seven sections, in order

1. Executive Summary: known borrower/facility facts and supported upstream summary; visible material gaps.
2. Compliance: versioned fictional policy results, exceptions, applicability, and evidence.
3. Financial Analysis: unchanged recorded values, definitions, inputs, periods/units, and citations.
4. Risk Scores: recorded educational credit score/band or Insufficient Data with material missing inputs; separate policy exception and missing evidence assessments; weights/contributions/provenance and factor coverage in explanation. Undefined concentration remains Not assessed. Copy recorded values; do not calculate or merge assessments.
5. Decision: simulated PanelDecision, uncalibrated confidence/rationale, current gates, and separate human disposition or Review not required.
6. Conditions: separate documentary covenants, model-proposed follow-ups, human modifications, owners, and evidence.
7. Audit Log: recorded events and source/reference index through the stated cutoff; disclose gaps and mode.

Never invent connecting facts, scores, decisions, conditions, or completed events. Use existing supported narrative and deterministic template sentences. Required action/owner/review tier comes from routing. AI-proposed action is copied only from accepted current synthesis and labeled separately; otherwise it is unavailable. A preview cannot imply required Moderate/High/senior review has occurred.

Copy CONDITIONS-1.0 provenance/category/owner/status and existing-gate links, with OUTSTANDING proposals separate from prerequisites; completed review/report never means fulfillment or funding. Covenants stay EXTRACTED_NOT_EVALUATED. Disclose the supplied annual period/entity/facility, full-term/balloon/refinancing NOT_EVALUATED and reported-EBITDA reconciliation Deferred. Source-support review is separate from credit disposition; unregistered uploads stay partial without PanelDecision. These markers fit the same seven sections and require no calculations or inference in the renderer.

## Output and purity

Return a Markdown string to state.report_markdown plus report_metadata carrying identity/revision/mode/template/cutoff/source-event references. Exact schemas are later specifications. Identical explicit inputs/template yield identical content; timestamps are supplied inputs, not hidden mutable state.

Do not invoke an LLM, network, checkpointer API, external file write, email, or export from this node. Runtime checkpoints the returned state update after completion. This node still counts toward graph/runtime limits.

## Draft preview and generated report

The same pure renderer may generate an on-demand read-only draft preview before required human review. Label it Preview, not an executed final report artifact, review action, or completed report-node event. It does not overwrite the persisted report for another revision.

The graph's post-review/no-review Report Generator creates the generated artifact. Blocked/partial material remains incomplete with owner/next action. A no-review branch never receives fabricated human approval.

Corrections mark prior report stale/superseded and regenerate only from valid current state. Review-only disposition/conditions changes need no fresh inference. Keep prior artifact references in history.

## UI and audit boundaries

Render Markdown safely; citations open the right source/version in Review Workspace. Generic acceptance never clears a mandatory gate. P0 requires readable inspection and generated sample output linked to an actual run; downloadable packages remain P1.

Audit contains only recorded events through cutoff. A checkpoint/report cannot already include its own future completion or later human actions. MemorySaver/SQLite is not an immutable complete audit guarantee.

Director fixes preserve seven sections and zero inference. NARRATIVE-CHECK-1.0 requires evidence/support coverage for rationale, each condition and action reason alongside observation Claims; rendering cannot invent support or turn REFERENCE_CHECKED into verified meaning. Keep original AI/human-edit targets and disposition separate. SOURCE-TRIAGE-1.0 reasons/owners are independent of true missing-document/policy counts. A CONTINUE-CHECK-1.0 budget stop preserves historical report/partial work without generating a completed current report or credit Reject. Existing citation and safe-rendering controls still apply.

## Required checks

Seven ordered headings; preserved numeric values/citations/exceptions; missing/Not assessed markers; preview versus generated/superseded labels; separate PanelDecision/HumanDisposition; direct-report review label; deterministic rendering; safe content display; cutoff accuracy; zero provider calls and no export side effects.
