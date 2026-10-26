# Deterministic Financial Analysis

Feature ID: SPEC-003
Version: 1.5
Status: Registered saved finance and bounded correction integrated; live adapter tested with mocks; actual live calculations await fact verification; generic upload admission pending
PRD requirements: FR-004, FR-007, FR-019
Role instructions: [Financial Analyst](../agents/financial-analyst.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

Current financial adapter boundary: registered saved E-N01/E-M01/E-P01/E-F03 cases and the bounded source-backed correction use deterministic FIN-1.0 calculations with source/scope/period checks. Live computation consumes actual source-supported facts through ReviewedLiveCase; that adapter is tested with mocks, while actual live computation awaits human fact support. Arbitrary uploaded-case financial admission remains unsupported. The pure arithmetic kernel is not itself proof of source correctness or human support.

An analyst sees reproducible numbers with their inputs, periods, formulas and uncertainty. Python Decimal performs all arithmetic. No adjusted EBITDA, credit grading, amortization forecast, FX, valuation haircut, or substitute cash-flow model.

## Workflow and rules

Select validated current facts/corrections on a coherent assessment basis. Evaluate CALC-001–009 in FIN-1.0 dependency order. Annual flows must match periods; balance-sheet amounts must share the stated date; post-loan debt and debt service must share the documented transaction basis. Missing D&A/tax/debt components are not zero.

Before trusted use, verify SPEC-001's subject/facility registry and SPEC-002's fact-support permissions for each required dependency. In Live mode reference-only critical facts remain untrusted until current source-backed support is recorded; affected metrics show Unknown and existing scoped information requirements. Registered Fixture execution remains explicitly labeled demonstration, not human verification. A parent's/guarantor's statement is not automatically borrower evidence. Supported consolidated scope must be expressly documented; do not mix subjects even when periods/currencies match.

Definitions are centralized in the [Financial Analyst file](../agents/financial-analyst.md), not duplicated alternatives. CALC-001 EBIT; 002 EBITDA; 003 post-loan funded debt; 004 DSCR; 005 leverage; 006 equipment LTV; 007 revenue growth; 008 current ratio; 009 interest coverage.

Apply P3-07 precision/display. Compare ratio thresholds via numerator/positive denominator cross multiplication before display rounding. Store exact numerator/denominator and computed Decimal representation; repeating quotients need not be mathematically exact decimal expansions.

DSCR denominator is supplied annual principal plus interest INCLUDING proposed borrowing; CFADS must be documented, never EBITDA. LTV adds supported prior-ranking liens once; absent lien amount is not zero. Debt/EBITDA with nonpositive EBITDA is NOT_MEANINGFUL and raises a supported concern, not a negative passing ratio. Optional absent growth/liquidity inputs remain unassessed and do not by themselves create a new lending requirement.

### Covenant and repayment-analysis limits

SME-05: contractual covenants remain extracted documentary clauses, not automatically evaluated obligations. A derived CovenantView copies clause/source/definition/period text and shows EXTRACTED_NOT_EVALUATED, MISSING_SOURCE or CONFLICT; an explicitly documented absence is NO_DOCUMENTED_COVENANTS, never an assumed covenant Pass. Bank-policy results keep their own rule/metric definitions. Even a policy Pass cannot establish agreement-covenant compliance. This status adds no lending threshold or automatic information gate for a requirement not already configured. No covenant engine, future monitoring or legal interpretation is included.

SME-06: FIN-1.0 computes unadjusted EBITDA from its registered components. Reported/adjusted-EBITDA normalization/reconciliation is deferred; do not display a completed reconciliation or mismatch assessment. Original statements remain inspectable and no discretionary addbacks or source adjusted-number substitution is allowed.

SME-07: DSCR is explicitly Analysis of supplied annual assessment period, not a full-term repayment forecast. Preserve source-backed repayment structure, maturity and use of proceeds in the summary. Full-term coverage, future rate scenarios, balloon repayment and refinancing adequacy are NOT_EVALUATED unless separately specified later; do not infer them from one favorable annual ratio. This limitation is disclosure, not an invented breach or automatic Reject. Missing existing required annual debt-service inputs still pauses the dependent result. Maturity alone cannot supply undocumented term-start/day-count assumptions. No amortization/stress/return-valuation model is added.

## Contracts and data changes

### M2 parser-independent arithmetic slice

The user's instruction to move forward authorizes the next local educational slice. Implement `finance.calculate_metrics` as an internal arithmetic kernel over exactly the eighteen FINANCIAL_FIELDS, each a canonical normalized money string or null. It returns all nine FIN-1.0 results with direct input names, numerator/denominator, percent multiplier, Decimal value, display, validity and safe reason. A separate exact threshold helper compares numerator times multiplier with positive denominator times threshold at precision50. Missing is never zero, documented zero is retained, and invalid signs for debt/assets/liens/debt-service operands affect dependent metrics. Repayment above existing funded debt plus proposed funding is invalid without a separately documented reconciliation; that reconciliation adapter is not part of this slice. Optional/inapplicable equipment LTV is explicitly unassessed rather than fabricated.

This kernel is not the public `compute_financials` stage, a financial panel, a source validator or a source-support bypass. Its VALID status means arithmetic validity only. The future stage must first apply current scope/period/currency/source applicability, fact support and case registration and attach full provenance. Candidate-case/application tests may exercise the kernel without claiming trusted Fixture or Live execution. No model, provider, database or financial action is invoked. Source-backed period/support-stage tests remain pending, even when kernel arithmetic tests pass.

Author E-N01 source files and expected numbers as an AUTHORING_DRAFT, not an approved registered fixture. Runtime-candidate extraction/assessment configuration remains separate from evaluator-only gold. New case dates, material assertions and five case-author ratings require review before registration. An author-created text/page map is not PDF-parser output; parser fidelity stays unverified until the licensed/approved parser actually runs. Preserve the user-uploaded `test_deal.pdf`; do not copy it or silently relabel it as synthetic.

compute_financials(FinancialRequest) -> StageEnvelope[FinancialPanel].
FinancialRequest: terms artifact reference, accepted corrections, assessment_basis_id, definition_version FIN-1.0, applicability/subject registry and current fact-support references.
FinancialPanel: metric_results, missing_dependencies, issue_refs, completeness COMPLETE/PARTIAL, assessment_basis_id, subject/facility/support lineage, covenant_views, analysis_scope (supplied period, source repayment/term/use references, full-term/balloon/refinancing NOT_EVALUATED), deferred_reported_ebitda_reconciliation marker.
MetricResult: metric_id/definition_version, input_fact_refs with canonical values, numerator/denominator nullable, Decimal value nullable, unit RATIO/PERCENT/USD, PeriodBasis, validity VALID/UNKNOWN/NOT_MEANINGFUL/INVALID, reason, display_value, source_refs.

Reject nonfinite inputs, incompatible units/bases, invalid signs for debt/assets/liens, and impossible repayment greater than documented available funded debt/transaction proceeds unless an explicit supported reconciliation is supplied. Financial values can legitimately be negative (net income, EBIT, CFADS); sign validation is field-specific.

Require SOURCEFIT-1.0-selected material inputs for the exact ReviewSourceBasis, subject/facility, unit and assessment period, in addition to FACT-SUPPORT-1.0. KNOWN, human-supported or most recently uploaded does not establish temporal/authority applicability. Do not combine older/newer statements into a ratio or substitute one tier/rate type for another; preserve legitimate prior-period inputs only where the formula explicitly requires them (for example comparable revenue growth). An older statement is not automatically expired: its reviewed period/basis must match. Missing material selection/date/authority pauses affected calculations; no invented recency threshold or financial Reject. Use existing TEST-003-04/E-C03 variants.

Use INPUT-EDU-1.0's external normalized-input bounds with precision 50. Verify sums/differences and policy cross-products remain exact at supported digit/scale boundaries. Apply exact numerator/positive-denominator threshold comparisons; do not round inputs, substitute floats or reject legitimate repeating ratios simply because division is inexact. A derived ratio is not an external money string and uses its own MetricResult schema. Arithmetic/resource overflow stops affected calculations with a technical reason, never a new bank-policy breach or automatic Reject. Refine TEST-003-02/03/06, retaining supported negative CFADS and existing FIN-1.0 formulas.

## AI and evidence behavior

Zero provider calls. Every number traces to inputs and FIN-1.0. Reviewer corrections retain REVIEWER provenance. Unsupported inputs cannot become confirmed just because arithmetic succeeds.

## Authorization

Only orchestration schedules the current artifact. Analysts can inspect formulas and propose source-backed corrections through SPEC-008, not directly edit computed values.

## UI states

Empty: inputs not yet extracted. Loading: deterministic calculation stage. Success: metrics, formula/input drawer, units and period. Partial/failure: Unknown/Not meaningful with exact missing/invalid input and next action; never infinity or zero placeholders.

## Reliability and stopping

One scheduled compute_financials tool boundary; ordinary arithmetic helpers are not additional LLM/tool agents. No transient retries for invalid mathematics. A technical execution exception may be retried once intentionally within global tool/node/time limits after a recoverable cause; never repair by changing inputs silently.

## Analytics

financial_panel_computed with valid/unknown/invalid counts, definition version and duration; calculation_issue_created with safe reason and metric ID, no amounts.

## Tests and acceptance

- TEST-003-01: Golden EBIT/EBITDA/post-debt and all six ratios match expected numerator/denominator and display.
- TEST-003-02: Positive/zero/negative denominators and nonpositive EBITDA handled explicitly.
- TEST-003-03: Negative supported CFADS/EBIT retained as negative meaningful ratios where denominators permit.
- TEST-003-04: Period/unit/basis/subject/facility mismatch, missing components or insufficient Live critical-fact support pause dependent results; supported consolidated scope cannot be guessed from a name. Reuse an E-C03 variant. SOURCEFIT-1.0 requires selected applicable inputs; a legitimate comparable prior-period operand is not rejected by an invented age limit.
- TEST-003-05: Prior liens and documented repayments counted once; unknown liens not zero.
- TEST-003-06: Unrounded threshold-adjacent inputs compare correctly despite identical display values. Verify INPUT-EDU-1.0 boundary sums/cross-products under precision50; legitimate repeating division is not a validation error.
- TEST-003-07: No provider request and no fabricated optional/concentration metric. Covenant EXTRACTED_NOT_EVALUATED is not policy Pass; annual DSCR cannot imply full-term/balloon repayment. Reported-EBITDA reconciliation is visibly deferred and cannot substitute a source adjusted value for FIN-1.0.

Target: 100% deterministic golden validity/arithmetic cases. See E-F01–F05 plus policy boundaries; exact examples in the evaluation plan.

## Dependencies and implementation boundary

Requires validated facts from SPEC-002/008; feeds SPEC-004/005/009. No finance library or calculation code is installed/written by this document.
