# Synthesizer — Agent 3 Summary Substep Instructions

Instruction ID: SYNTH-001  
Version: 1.6  
Execution: One normal structured LLM call in Live mode; zero in Fixture mode  
Requirements: FR-006–009, FR-017–019  
Read with: [Shared contract](shared-contract.md), [Policy](compliance.md), [Evaluation](evaluation.md)

## Purpose and rationale

Read all three validated panels together and create an evidence-linked financial/risk interpretation, summary, and simulated credit-committee recommendation. This is the existing second call, not a new narrative/judge agent.

## Inputs

Current-revision Financial, Compliance, and Risk panels; compact verified terms; complete educational score/band and supported drivers; source/finding references; independently computed mandatory gates and known gaps; output schema. Missing/stale/invalid mandatory panels or material scoring inputs prevent dispatch. No entire transcript, unrelated deal history, arbitrary policy corpus, or confidential data.

## Runtime prompt

Read the supplied Financial, Compliance, and Risk panels together. Return only the supplied SYN-WIRE-1.0 SynthesisWire: wire_version, the exact five-field panel_decision, one supported observation per panel, rationale_refs, indexed condition_links and nullable proposed_action. Use only supplied logical reference handles. Weigh all three panels and preserve their exceptions, missing information, and contradictions. Python supplies IDs/provenance and hydrates SynthesisResult; do not emit artifact/Claim IDs, support status, criticality, actor, approval or gate authority.

PanelDecision has exactly these fields: decision (Approve, Conditional Approve, or Reject), confidence (finite 0–1), rationale (substantive source-linked text), conditions (list of nonblank strings), and escalate_to_human (Boolean to be verified by Python). Conditional Approve requires at least one actionable condition grounded in supplied findings. Distinguish proposed review conditions from sourced loan covenants.

All labels are simulated educational recommendations. Confidence is self-reported and uncalibrated, not repayment probability. Do not recalculate metrics, invent scores/default probabilities, manufacture facts/citations/covenants, claim legal clearance, or override mandatory controls. Use references to supplied findings/source IDs. Explain supported uncertainty without revealing hidden chain-of-thought.

Respect each panel's supplied annual period, entity/facility and support scope. Do not claim full-term/balloon/refinancing adequacy, automatically tested contractual covenants or reported/adjusted-EBITDA reconciliation. A sample bank-policy Pass is not covenant compliance. Conditional Approve proposals stay source/finding-linked review conditions, not fulfillment, funding or permission to ignore missing current evidence. Python derives condition categories/gates from existing records; do not invent that authority. Unregistered uploads or unsupported mandatory inputs do not receive a completed recommendation.

The Python router enforces requested amount >=USD 10M or confidence <0.7, SCORE-ROUTING-1.0, and other mandatory referrals. Moderate always requires normal human underwriting; High requires Credit Risk Manager handling then package review; Very High requires senior-tier Authorized Approver review. A Low score or confident Approve cannot clear an independent block. No score band universally selects Approve/Reject. Return only the requested structured output.

Use only SOURCEFIT-1.0-selected material facts for the supplied review date/knowledge cutoff and exact subject/period/qualifiers. Preserve all unresolved material source-fit issues; do not substitute a newer historical value, superseded term, unmatched tier or different rate type. A recent filename or model confidence cannot establish authority. Python's source-selection profile owns applicability; a retained historical source is not automatically valid for the current recommendation. This instruction adds no wire field/call and must be included in instruction-hash/token preflight updates.

## Output and local validation

Follow the exact compact wire and complete ordinary/Conditional examples in SPEC-005 SYN-WIRE-1.0. Python validates the wire/reference dictionary and hydrates the trusted envelope, three Claim observations and condition records. proposed_action remains outside PanelDecision with the exact kind/target/reason/refs shape; it is advice, not an executable action or clearance. Python computes actual permitted action/support/criticality and effective escalation independently. Missing accepted current synthesis means AI-proposed action is unavailable; never fabricate it from a template. Use the existing second call within unchanged budgets. The full schema/output must pass token preflight; 350 output tokens is an unmeasured starting target.

Validate all required fields/types, literal decision values, finite confidence in [0,1], substantive rationale, referenced IDs, and nonempty supported conditional conditions. No guaranteed confidence=1.0 and no unsupported confidence calibration.

Required data absent -> no accepted PanelDecision, with existing needs-information/block state. A parser/schema failure is not Reject. Evidence/gate-conflicting output is quarantined/unverified, not displayed as cleared.

Python sets the final escalate_to_human flag and records trigger/override reasons. Keep raw model-proposed value only as diagnostic provenance; it cannot suppress a required route.

NARRATIVE-CHECK-1.0 in SPEC-005 registers evidence targets locally for all observations, rationale, conditions and optional action reason, using the existing returned references. Python checks every target without adding model-visible IDs/fields or another generation call. Unsupported material assertions anywhere in a field cannot be concealed by a correct cited sentence elsewhere. INPUT-EDU-1.0 rejects duplicate/oversized/invalid wire content before hydration; source-role assignments do not grant authority. Keep five-field PanelDecision unchanged and the exact validated confidence for unrounded routing/canonical identity. A valid citation is not human semantic support; original versus human-edited targets remain separate for evaluation.

## Corrections, human disposition, and limits

A material analytical revision invalidates synthesis and dependent report/disposition. Reuse unaffected upstream outputs. A human-only condition edit or package disposition does not rerun this call. Schema/provider repair counts as another attempt and must fit every cumulative budget.

## Required checks

All three valid labels; confidence 0/1, negative/>1/nonfinite; blank rationale; empty conditional conditions; all three panels represented; source-backed versus unsupported rationale/proposed action; missing/stale panels and material scoring inputs; block-conflicting Approve; amount/confidence and score routing boundaries; exact five-field PanelDecision; original recommendation retained after human override; one normal call.

## Supported rejection and current-input fixtures

[E-F03/reject-supported](../evaluation/examples/e-f03-reject.md) demonstrates a supported case-specific Reject recommendation with required human handling/review. Missing inputs or a technical failure do not become Reject. A policy breach alone does not universally select the label. Stage fixtures must match current normalized panels and revision-scoped evidence, including after correction. This adds no inference stage.
