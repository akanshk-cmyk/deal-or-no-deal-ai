# Financial Analyst Instructions

Instruction ID: FINANCE-001  
Version: 1.3  
Execution: Pure Python/Decimal; zero LLM calls  
Requirements: FR-004, FR-007, FR-019  
Read with: [Shared contract](shared-contract.md), [Compliance](compliance.md), [Evaluation](evaluation.md)

## Purpose and rationale

Current implementation: services.compute_financials qualifies the exact registered E-N01 default before calling finance.calculate_metrics. Its nine outputs retain eighteen input facts, source references, scope, period/basis and missing dependencies. [Observed application checks](../execution.md#m2-registered-deterministic-panels-evidence) do not establish general Live support or full graph execution. Covenant evaluation and full-term/balloon/refinancing adequacy remain explicitly unevaluated.

Produce reproducible arithmetic with explicit provenance. The model interprets these outputs later; it does not choose new formulas, reclassify debt, or silently recompute numbers.

## Inputs and basis

Use validated source facts/corrections, period/as-of metadata, and the following versioned definitions. All calculations are USD unless explicitly dimensionless. Distinguish annual flow periods from balance-sheet/debt as-of dates; label post-loan figures pro forma. Fixtures must provide a coherent documented assessment basis rather than implicitly mix quarterly, historical, and forecast inputs.

## Calculation definitions — FIN-1.0

| ID | Calculation | Accepted prototype definition |
|---|---|---|
| CALC-001 | EBIT | Net income + interest expense + income-tax expense, matching period |
| CALC-002 | EBITDA | EBIT + depreciation + amortization, matching period; no discretionary addbacks |
| CALC-003 | Funded debt after loan | Documented existing funded interest-bearing debt + proposed funded borrowing - documented debt repaid in this transaction |
| CALC-004 | DSCR | Documented annual cash available for debt service / documented annual principal-plus-interest payments including proposed loan, on the stated assessment basis |
| CALC-005 | Debt/EBITDA | CALC-003 / annual CALC-002 |
| CALC-006 | Equipment LTV percent | (Proposed facility exposure secured by these assets + documented prior-ranking liens) / eligible equipment value * 100 |
| CALC-007 | Revenue growth percent | (Current annual revenue - previous comparable annual revenue) / previous revenue * 100 |
| CALC-008 | Current ratio | Current assets / current liabilities, same reporting date |
| CALC-009 | Interest coverage | CALC-001 / interest expense, same annual period |

The six required ratio definitions are CALC-004–009; CALC-001–003 are supporting arithmetic.

No net-cash deduction or undrawn-commitment substitution in funded debt. Use documented debt classification; do not invent lease reclassification. Eligible equipment value and lien amounts require their source/basis; absent liens are not assumed zero. Do not subtract prior liens from value as well as adding them to exposure. No unstated valuation haircut, collateral aggregation, FX conversion, or repayment projection is performed.

CFADS/cash available is an explicit documented input; do not substitute EBITDA or generate a cash forecast. Proposed debt service must be supplied in a schedule; no amortization/rate-forecast engine is added. A term is taken from documented months or supported maturity data; unspecified date/day-count conversion is not invented.

Follow SPEC-001 subject/facility attribution and SPEC-002 FACT-SUPPORT-1.0 before using required inputs. Live critical facts need current HUMAN_SUPPORTED source evidence; compatible dates or an existing citation alone do not make another entity's figures borrower data. Fixture execution stays labeled demonstration. Expose affected metrics as Unknown when the prerequisite is missing; do not silently use an unreviewed value.

Follow SPEC-003's scope limits: supplied annual assessment-period analysis, with full-term/balloon/refinancing adequacy NOT_EVALUATED. Copy repayment structure, maturity and use of proceeds without asserting lifetime repayment. Contractual covenants are EXTRACTED_NOT_EVALUATED rather than policy Pass. Normalized reported/adjusted-EBITDA extraction/reconciliation is deferred; compute only FIN-1.0 and retain original source access, without a claimed adjusted-EBITDA mismatch assessment.

## Invalid and missing inputs

- Missing/unsupported/conflicting essential inputs return Unknown with affected definition/input references.
- DSCR requires positive debt service; negative supported cash available can yield a meaningful negative ratio.
- Debt/EBITDA requires positive EBITDA; zero/nonpositive EBITDA returns Not meaningful plus a supported concern, never a negative-ratio Pass.
- LTV requires positive supported eligible value and supported nonnegative exposure/liens.
- Revenue growth requires positive prior revenue; no annualization or incompatible-period comparison.
- Current ratio requires positive current liabilities; interest coverage requires positive interest expense.
- Never return infinity, fabricate defaults, or map calculation failure to a credit Reject.

Use SOURCEFIT-1.0-selected exact period/subject/qualifier inputs and INPUT-EDU-1.0's bounded normalized external values. Precision50 must preserve supported sums and policy cross-products without silent arithmetic rounding; threshold comparison uses exact numerator/positive denominator. Repeating division/display remains legitimately approximate and must not be rejected by a blanket inexact-operation trap. Technical/profile overflow is an affected calculation error, not a new lending threshold or loan rejection. Original negative CFADS and zero handling remain unchanged. SOURCE-TRIAGE-1.0 routes unresolved financial context to investigation, never a guessed number/precedence rule.

## Output and display

MetricResult includes definition/version, assessment basis, inputs/provenance, Decimal result/unit, validity/reason, and display value. Policy comparisons use the unrounded value. Display ratios to two decimals and percentages to two decimal percentage points for consistency; do not confuse display with decision precision.

## Fictional golden examples

Cash available 900,000 / debt service 600,000 -> DSCR 1.50x. Funded debt 3,300,000 / EBITDA 1,100,000 -> leverage 3.00x. Secured exposure 1,200,000 with explicitly documented zero prior liens / value 2,000,000 -> LTV 60.00%. Assets 1,500,000 / liabilities 750,000 -> current ratio 2.00x.

## Required checks

Golden results and threshold-adjacent values; missing/zero/nonpositive denominators; negative cash/EBIT; debt repayment and double-count prevention; prior liens; units/periods/entity/facility scope and current critical fact support; no adjusted EBITDA substitution or claimed reconciliation; annual-only and covenant-not-evaluated labels; no silent FX/forecast; unchanged numbers through synthesis/reporting.
