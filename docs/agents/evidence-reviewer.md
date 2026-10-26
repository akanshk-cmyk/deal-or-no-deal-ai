# Evidence Reviewer Instructions

Instruction ID: EVIDENCE-001  
Version: 1.6
Execution: Pure Python plus explicit human semantic-review flags; zero LLM calls  
Requirements: FR-007, FR-014, FR-017, FR-019–020  
Read with: [Shared contract](shared-contract.md), [Evaluation](evaluation.md)

## Purpose and rationale

Prevent a valid-looking response or citation from being mistaken for a supported finding. Mechanical checks are useful but do not independently prove semantic truth.

## Inputs and checks

- Apply [DOCVERIFY-1.0](../specs/context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10) to declared original-block dependencies, including cross-page qualifications. Adaptive expansion may restore only accepted same-scope originals; absent/unverified material remains withheld. COMPLETE coverage and KNOWN column alignment never confer HUMAN_SUPPORTED or prove a parser discovered every dependency.

- Current source/version/page/passage manifest.
- Extracted facts and corrections, recorded calculations, policy/risk results, and Synthesizer claims/PanelDecision.
- Resolve every material citation to the same deal/input revision and available source.
- Verify copied numeric values/units/periods and calculation references against validated results, not a fresh model calculation.
- Check required sections/fields, mandatory issues, contradiction references, and unsupported new numbers.
- Distinguish sourced facts from reviewer-provided corrections and narrative proposals.
- Validate registered fixture scope/reference integrity; evaluator-only golden support annotations are checked offline, never loaded to grant runtime support. Route unresolved semantic support to human review.

## Output

EvidenceReview contains per-claim structural/reference/numeric results, support status, unresolved semantic-review needs, missing/conflicting inputs, required follow-up, and dependency/blocking effects. Preserve original claims and their validation outcomes for audit; do not silently rewrite evidence.

Critical unsupported facts or gate-conflicting claims are withheld/quarantined and cannot become verified merely because the panel confidence is high. Known unverified material must be visible in UI/report. Noncritical uncertainty may remain explicitly partial only when the configured workflow permits.

FACT-SUPPORT-1.0 supplies the missing Fact-to-review contract: records bind the exact current fact/value/source/basis/subject digests and use the typed FACT target in SPEC-008; narrative uses CLAIM. In Live mode required critical facts need source-backed HUMAN_SUPPORTED before trusted dependent use. Check row/label, scale/unit, period/entity/facility, not just numeral presence. Support cannot override a mechanical mismatch, substitute for a missing document or mutate source facts. Replaced sources/values or retracted support invalidate dependent artifacts and stale acknowledgements. Controlled fixture execution is labeled demonstration, not human semantic certification; evaluator gold remains outside runtime prompts/control permissions.

Reject claims that bank-policy Pass proves contractual covenant compliance, that a report means conditions fulfilled/funding, that annual DSCR proves full-term/balloon repayment, or that reported EBITDA reconciliation ran. Confirm CONDITIONS-1.0 retains existing blocking issues and supported condition lineage. These checks add no judge-model call.

## Boundaries

No judge-model call, browsing agent, legal certification, or external fact-checking service. Do not mutate source documents or erase exceptions. An LLM can still be wrong with valid citations; do not equate source existence with entailment.

Provide the current scoped references required by SPEC-010's CITEVIEW-1.0: document/version/page/passage and context for quoted facts; formula and operand sources for computed values; exact policy rule/version plus borrower inputs; attributed case-assessment/rubric or reviewer-correction records when that is the real origin. All supporting/conflicting refs must remain accessible beside the validated detail. Never invent a PDF page, source URL or highlight coordinates. Missing/unavailable/stale references retain explicit states. UI/source inspection reads these artifacts without model/tool dispatch, gate mutation or automatic HUMAN_SUPPORTED status; precise highlighting uses stored source spans only, with a truthful textual-context fallback.

Apply COVERAGE-1.0 inventory and all original page locations, including table headers/units/notes and split-clause qualifiers; a resolving row alone is not complete support. CANON-1.0 maps supplied logical handles only within the exact current request. Model Claims receive Python-owned IDs/criticality and PENDING then mechanically REFERENCE_CHECKED status; only a permitted current human support record can confer HUMAN_SUPPORTED. Preserve original model claims under EVAL-CUTOFF-1.0 even when later human conditions or facts change. Missing related context/source version or unsupported meaning is not repaired by a new guessed citation.

Check SOURCEFIT-1.0 selection/profile/date/qualifier lineage in addition to reference resolution and semantic support. Source availability, effective period and financial period are different tests. Different tiers, APR/APY/annual interest values or statement periods are not automatically equal propositions/conflicts. Human support cannot authorize missing precedence or turn a superseded value into the selected current value. Citations expose actual selection reasons and alternatives; no date or authority is fabricated. Missing material fit blocks dependent conclusions without deleting history or introducing a universal expiry rule.

## Failure and correction behavior

Broken/missing source, stale reference, unsupported new metric, or known contradiction produces a reason-coded result. Mandatory failures pause affected progression. A proposed repair that requires model work is dispatched only by Orchestrator within the same budgets, not by a hidden reviewer-agent loop.

Apply NARRATIVE-CHECK-1.0's fixed target registry to all three observations, the rationale, each condition and optional proposed-action reason. Reuse local Claim/path/text/source/dependency digests; no model-supplied IDs, sentence-splitting engine or judge. Check the whole field for unsupported material assertions; reference resolution/numeric checks do not certify entailment. Keep PENDING/REFERENCE_CHECKED/HUMAN_SUPPORTED separate and use existing role-specific assessments for unresolved material support. Human condition edits have new targets without overwriting original model evaluation. SOURCE-TRIAGE-1.0 identifies missing evidence versus source authority/applicability/configuration; do not count an available uncertain PDF as missing or grant a blanket waiver through support/assignment.

## Required checks

Resolving and broken citations; wrong deal/version/page; copied-number mismatch; incomplete/unsupported rationale; preserved conflicts; reviewer corrections without fabricated citations; unsupported critical claim withheld; known semantic uncertainty routed; source inspection/validation zero inference.
