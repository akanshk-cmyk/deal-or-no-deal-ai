# Risk Quantifier — Agent 3 Substep Instructions

Instruction ID: RISK-001  
Version: 1.7  
Execution: Pure Python; zero LLM calls  
Requirements: FR-006, FR-014, FR-019  
Read with: [Shared contract](shared-contract.md), [Financial definitions](financial-analyst.md), [Policy](compliance.md), [Evaluation](evaluation.md)

## Purpose and rationale

Current implementation: risk.py aggregates only approved supplied factor assessments, retaining evidence, exact weights and unrounded classification. The registered E-N01 default has20/25/20/15/30 factor ratings and score21 Low; these are fictional authored ratings, not inferred from ratios. Missing material inputs suppress the score. [Actual tests](../execution.md#m2-registered-deterministic-panels-evidence) cover band boundaries, separate referral routing and missing/stale/invalid cases; no predictive model, synthesis or final decision is claimed.

Turn supported metrics and policy/evidence gaps into traceable risk flags and quantified threshold differences. Risk & Summary is the composite of this node and the one-call Synthesizer.

## Inputs

Validated financial metrics, policy results, terms, explicit missing/conflict records, configured method versions, and source references.

Complete scores require the registered reviewed case pack described in SPEC-001 and compatible subject/facility plus FACT-SUPPORT-1.0 permissions. Unregistered Live upload remains partial; never borrow a prepared case's factor ratings. Supplied factor assessments cannot cure missing/unsupported source inputs. Preserve annual-period and covenant-evaluation limitations in supported flags; do not invent full-term repayment, adjusted-EBITDA reconciliation or additional policy exceptions.

## calc_credit_risk contract

This is a project-defined function to implement, not an existing external API. Return structured flags such as weak debt-service coverage, excessive leverage, insufficient supported collateral, missing required evidence, and term/policy exceptions.

Quantify a known gap without inventing a credit model. For example, DSCR 1.15x versus 1.25x has a 0.10x shortfall; LTV 85% versus 80% has a five-percentage-point excess. Preserve raw observed value, threshold, units, direction, rule/version, and evidence.

Only the user-supplied [RISK-EDU-1.0](../specs/policy-risk.md#educational-weighted-risk-score--risk-edu-10) may produce an educational0–100 aggregate: combine five explicitly supplied synthetic factor assessments with fixed weights repayment0.30, leverage0.20, collateral0.20, borrower credit0.20 and business/industry0.10. Higher means more modeled risk. Do not invent factor ratings from ratios/flags, use an LLM to assign them, create additional score models, derive PD/calibrated grade or choose automatic loan decisions. Optional financial measures without policy thresholds remain informational, not new breaches.

Compute the weighted total in Decimal as an ordinary helper within this existing node; no new registered tool/node/provider call. All five assessment IDs/reasons/provenance, material source inputs and current revision/method context must be valid. Missing/unusable factor or material input returns Insufficient Data with null total/band and an explicit missing list; do not renormalize weights or fill absent credit/industry history. Configuration failures remain distinct from missing evidence. The supplied60/40/30/20/50 example totals41, Moderate, not41% PD; it is not automatically assigned to any loan.

Apply SCORE-BANDS-1.0 to the unrounded total: Low [0,25], Moderate (25,50], High (50,75], Very High (75,100]. Classification precedes display rounding. Persist ratings, weights, contributions, total, band, material-input provenance and configuration versions. The Orchestrator applies SCORE-ROUTING-1.0: Moderate always requires normal human underwriting; High requires Credit Risk Manager handling followed by package review; Very High requires senior-tier Authorized Approver review. Low does not clear independent policy/evidence gates. Missing material inputs pause dependent synthesis and final readiness. Never infer Approve/Reject from the band.

Supply a bounded score/band/supported-driver projection to the existing Synthesizer call. SCOREVIEW-1.0 and the memo show separate credit risk, policy exception and missing evidence assessments; factor coverage is explanation detail, not document completeness. An unrelated required evidence gap can coexist with a valid score, but a missing material scoring input cannot. Corrections invalidate dependent scores, routing and acknowledgements. Viewing recorded results performs no scoring or model work.

## calc_concentration_risk contract

This is also a project function, not a verified service. With no approved concentration method/limit or required consistent customer/portfolio inputs, return Not assessed and identify what is missing. A single loan amount is not portfolio concentration. Do not fabricate an exposure base or a cutoff. Future concentration methods need explicit specification approval.

## Workflow and outputs

Return RiskPanel with supported flags, observed-versus-threshold gaps, applicability/missing-method status, sources, and linked policy/evidence issues. Reuse the same issue identity where it is the same underlying rule breach; do not double-count it as independent new evidence.

Use policy-approved/configured severity and owner mappings only. When unmapped, expose classification/configuration required rather than assigning arbitrary weights or closure powers. Critical mandatory-control statuses remain intact.

## Failures and stopping

Missing required repayment inputs prevent a complete repayment-risk assessment. Unsupported or contradictory inputs pause affected calculations. Safe unaffected flags can remain visible as partial. Do not convert Unknown to low risk or infer misconduct.

Run scheduled tools directly; no ReAct agent chooses or repeats these known functions. Both substep work and tools count toward cumulative limits.

## Required checks

Supported normal/exception flags and exact gaps; retired exposure rule not recreated; only RISK-EDU-1.0 with supplied ratings/weights produces a numeric aggregate, never default probability; missing/no-reweighting/current-versus-stale and material provenance; exact unrounded band boundaries and independent mandatory routing; concentration Not assessed when undefined; issue deduplication/configured severity and zero provider requests. TEST-004-10/11 own aggregation, classification, routing and separate assessment cases.

## Overflagging QA

QA-RISK-FP-01 in the [evaluation plan](../evaluation/evaluation-plan.md) keeps a high-level offline false-positive count beside recall. Count repeated underlying issues once and preserve supporting references; no invented misconduct/control allegation or unapproved composite score. It adds no QA interface indicators, detailed scoring workflow or extra model call; the separately requested educational score cards do not expose false-positive QA metrics.
