# Sample Policy Checks and Risk Quantification

Feature ID: SPEC-004
Version: 1.9
Status: Registered saved policy/risk, exception handling, graph and UI integrated; live deterministic adapters tested; actual live panels await supported facts
PRD requirements: FR-005–006, FR-007, FR-014, FR-018–020
Role instructions: [Compliance](../agents/compliance.md), [Risk Quantifier](../agents/risk-quantifier.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

An analyst sees which fictional rules apply, their outcomes, supported risk gaps, and who must act. These two independently testable panels use Python, not ReAct or policy-interpretation model calls. The user's supplied five-factor educational score is defined below; no live KYC/sanctions, legal clearance, SAR filing, PD, calibrated credit rating or portfolio-concentration inference is introduced.

## Workflow and rules

M2 implementation boundary: CASE-REG-1.0 in SPEC-001 binds approved E-N01 inputs before pure policy/risk evaluation. Implement sample-policy JSON plus fixed Python handlers (no editable DSL); handler traces retain exact metric operands, comparator/threshold, source/policy refs, authority, separate outcome/workflow/severity/owner. Confidence remains NOT_EVALUATED until synthesis, not a false zero or premature information failure. Score aggregation uses only the now user-approved authored ratings and current material sources/metrics; preserve exact bands and independent gates. Missing/invalid factors or material prerequisites yield null score without reweighting. Aggregate policy/evidence/risk findings by stable underlying identity; no threshold-to-Reject rule, grade inference, PD or concentration calculation. The M2 report has no PanelDecision and cannot claim final readiness. Focused application tests cover existing TEST-004-01/02/03/04/05/07/09/10/11; later persistent handling/graph/UI tests remain pending.

For the existing amount/confidence DEMO_PRODUCT_CONTROL records, keep policy outcome null and record control_result TRIGGERED/NOT_TRIGGERED/UNKNOWN/NOT_EVALUATED separately. Capture the actual three-state amount OR confidence grouping: any true yields true; both false yields false; otherwise unknown. Internal sample-policy outcomes retain Pass/Exception/Unknown/Not applicable. This avoids presenting a mandatory review trigger as a bank-policy breach and adds no new threshold or authority.

Load SAMPLE-LOAN-POLICY-1.0 and CasePolicyConfig. Evaluate applicable rules over current validated facts/metrics. Unknown applicability/input is Unknown, never Not applicable. Retired SYN-ESC-003 is never evaluated. Rules 011/012 are threshold routing controls finalized after synthesis, not a prerequisite requiring confidence before synthesis.

Use active comparisons from [Compliance](../agents/compliance.md): DSCR <1.25, leverage >4, equipment LTV >80%, term >60 months. Missing required valuation/financials/conflicting terms pause affected work; explicitly unresolved REQUIRED synthetic KYC/sanctions controls block completion. Missing required fixture status also remains Unknown/blocked for that conclusion.

CasePolicyConfig fields: version, facility_kind TERM_LOAN, secured_equipment Boolean with documentary basis, required_fields/metrics, assessment_basis_id, KYC/sanctions_required flags, authoritative_source_precedence nullable, conflict/materiality definitions nullable, severity_owner_map, permitted_exception_rule_ids, configured control-fixture digests. This is trusted developer/instructor configuration, not uploaded instructions. A fixture explicitly marks inconsistent rate/principal/period facts material; do not invent percentage tolerances or a universal rule for document recency.

Risk flags reuse the same underlying issue IDs. Calculate exact DSCR shortfall and LTV/leverage/term excess where supported. Optional growth/current ratio/interest coverage are informational unless a separately approved threshold exists. Concentration always Not assessed in P0 because no approved method/data base exists.

SME resolutions preserve the rule pack/thresholds. Complete review requires SPEC-001's registered assessment/subject configuration and SPEC-002's applicable critical-fact support. A known Live value without required semantic support cannot enter a trusted comparison; subject/basis mismatch or absent assessments pause affected work with the existing scoped prerequisite, not an invented banking Exception. A bank-policy Pass does not evaluate sourced contractual covenants, which remain EXTRACTED_NOT_EVALUATED. CONDITIONS-1.0 records cannot waive missing source/control requirements or imply fulfillment. Annual-ratio flags cannot assert full-term/balloon repayment or reported-EBITDA reconciliation. None introduces an automatic Reject or additional LLM call.

## Fixture severity and owner mapping — accepted P3-02

| Rule/control | Severity | Simulated owner | Gate |
|---|---|---|---|
| 001/002/004/005 supported numerical exception | HIGH | Risk Manager | ESCALATE; separate sample-exception handling then final package review |
| 006/007/008 required evidence/conflict | HIGH | Credit Analyst | NEEDS_INFORMATION; affected dependent conclusions/completion paused |
| 009/010 required unresolved control fixture | CRITICAL | Compliance Officer | BLOCKED; only registered synthetic evidence update, never real clearance |
| 011 requested amount trigger | HIGH | Authorized Approver | Required package review; no implied adverse credit finding |
| 012 confidence trigger | MEDIUM | Authorized Approver | REVIEW_REQUIRED with mandatory package review; confidence is not calibrated risk |
| Explicit supported nonblocking observation | INFO | Credit Analyst | CONTINUE; do not invent an observation solely to populate a severity |
| Known noncritical semantic uncertainty | MEDIUM | Configured Risk Manager/Compliance Officer by claim type | REVIEW_REQUIRED; unsupported statement visibly unverified |
| Technical integrity/unavailable required configuration | CRITICAL | Administrator / Technical Review queue | BLOCKED for affected dispatch; no financial clearing power |

These demo mappings were accepted with P3-02 on 2026-10-22. Required controls remain mandatory regardless of severity. Additional ambiguous cases return CONFIGURATION_REQUIRED rather than guessing a financial/specialty authority.

The later SCORE-ROUTING-1.0 addition uses explicit educational display mappings: SCORE-REVIEW-MODERATE MEDIUM/Authorized Approver; SCORE-REVIEW-HIGH HIGH/Risk Manager; SCORE-REVIEW-VERY-HIGH HIGH/Authorized Approver with SENIOR tier; SCORE-DATA-MISSING HIGH/Credit Analyst or the existing configured evidence owner. Risk-band names and issue severity are separate fields: Very High credit risk does not itself assert a CRITICAL compliance violation. Existing CRITICAL control/integrity blocks keep their precedence. These are demo presentation/ownership mappings, not regulatory classifications or new powers.

## Read-only rule evaluation details — RULEVIEW-1.0

User-authorized attachment review on2026-10-23: adopt the compact condition/outcome pattern as an inspectable rule summary within existing Review Workspace details. Users can validate how a recorded check follows from its exact condition, inputs, calculation and source policy. This is inspection of a recorded Python evaluation, not a no-code policy editor, a new validation agent or an independent approval/clearance action. The attachment's Bank Risk Score, Plaid connections, balance thresholds and ACCEPT/REROUTE labels are reference visuals only; they add no fields, integrations, scores or business rules to this project.

| Detail | Required information |
|---|---|
| Rule identity and authority | Rule ID/title, exact sample-policy version/pack digest, INTERNAL_SAMPLE_POLICY or DEMO_PRODUCT_CONTROL, original policy/reference locator and source text |
| Applicability | Applies/Not applicable/Unknown with configured case basis/reason; Unknown must not become Not applicable or Pass |
| Exact condition | The predicate actually evaluated by the approved Python handler, with explicit comparator, threshold and unit; explain whether true means an exception, a trigger or another configured result |
| Observed inputs | Current values/provenance, source/version/page/passage, currency/scale, assessment period/basis and missing/conflict/invalid markers |
| Calculation | FIN-1.0 definition/version, input references, exact numerator/denominator where applicable, display value and sufficient unrounded detail to verify a boundary comparison |
| Condition results | Recorded true/false/unknown state for each evaluated condition; distinguish Not evaluated yet from a completed Unknown result; show AND/OR grouping only where actually used |
| Result and consequence | Recorded policy outcome, distinct workflow/referral/block, severity/owner and permitted next action; a Pass is not credit approval and a breach is not universally Reject |
| Execution context | Deal/run/input revision, evaluator/rule version, input dependency digest and evaluation timestamp from the recorded artifact; historical/out-of-date status is explicit |

Example from existing E-P01, illustrative until fixture execution:

~~~text
SYN-ESC-001 · Minimum DSCR · SAMPLE-LOAN-POLICY-1.0
Applies: Yes, using the documented assessment basis
Calculated DSCR: USD690,000 / USD600,000 = 1.15x
Executed condition: DSCR < 1.25x
Condition result: True
Policy outcome: Exception
Workflow: Escalate · Owner: Risk Manager
Next step: Record supported sample-exception handling, then package review
Links: Policy rule · CFADS source · Debt-service sources · FIN-1.0 calculation
~~~

This is an exception predicate: true means the minimum is breached, not Pass. At DSCR exactly1.25, the predicate is false and that numerical comparison passes. Threshold predicates still use the approved exact arithmetic, not rounded display strings. For amount>=USD10M and confidence<0.7, show the correct inclusive/exclusive operators: USD10M equality triggers; confidence0.7 equality does not. Confidence routing is finalized only after validated synthesis; before then show Not evaluated yet. The amount/confidence OR group and other mandatory referrals remain distinguishable; a false base threshold group cannot suppress an active separate referral or block. Render the recorded grouping/result, not independently invented UI Boolean logic.

Missing/conflicting financial inputs show the missing operands and reason why the comparison is Unknown/not evaluated, not a fabricated observed value or false comparison. An inapplicable rule shows its applicability basis without pretending a comparison ran. A retired rule appears only as historical/Retired, never an active Pass. Historical evaluations remain tied to their original policy/source/input versions; viewing them cannot reevaluate current inputs or adopt a newer policy silently.

Selecting View rule evaluation or a policy/source/calculation link reads the existing artifact and trusted registry/reference content. It invokes no graph node, registered tool, provider call or financial/policy recomputation and changes no review/gate state. No generic Mark validated or Accept rule button is introduced. Existing permitted semantic-support assessment or issue-disposition actions remain separate and cannot turn an inspection into legal clearance. If a user disputes an input, link to SPEC-008's correction/impact flow; if the reference or recorded trace is inconsistent/unavailable, say Cannot verify recorded evaluation and surface the existing issue/technical prerequisite instead of claiming validation or silently fixing the result.

## Contracts and data changes

### Educational weighted risk score — RISK-EDU-1.0

The user supplied this educational scoring framework on2026-10-23 in response to the score-source question. Use the five named factors/weights below and higher values=more modeled risk,0 lowest/100 highest. This supersedes the earlier unconfigured score-source choice and provisional separate Borrower/Deal score labels. It does not define a factor-rating model or probability of default. Product name remains Deal or No Deal AI; pasted DealPilot references do not rename the project.

| Factor ID | Factor | Weight | MVP factor-rating source |
|---|---|---:|---|
| repayment_capacity | Repayment capacity | 0.30 | Explicit synthetic case assessment with rationale/references; DSCR/cash-flow evidence can support it but no DSCR-to-score mapping is inferred |
| financial_leverage | Financial leverage | 0.20 | Explicit synthetic case assessment; no invented debt/EBITDA score bands |
| collateral_quality | Collateral quality | 0.20 | Explicit synthetic case assessment; no invented LTV score bands, valuation haircut or lien assumptions |
| borrower_credit_profile | Borrower credit profile | 0.20 | Supplied synthetic assessment/history only; no credit-bureau integration or inferred repayment history |
| business_industry_risk | Business and industry risk | 0.10 | Supplied synthetic assessment only; no web research, industry model or new concentration calculation |

All factor risk values are explicitly supplied assessments on0–100. Python computes RiskScore=sum(weight_i*factor_risk_i); it does not invent the five ratings or derive them with an LLM. This supplies a transparent aggregation method, not a statistical model or a documented numeric conversion from raw financial ratios. Future automatic factor-rating mappings require separately approved definitions/evidence/evaluation. Synthetic authored assumptions are labeled as assessments, never fabricated documentary facts.

Store runtime factor assessments in trusted case/variant metadata with assessment/source digests/current revision; evaluator-only expected contributions/totals remain in gold.json and never become node inputs. The user's later three-assessment requirement makes a complete material-input-backed score a prerequisite for a final decision-ready assessment: absent factor ratings or their material source inputs produce Insufficient Data and an information pause, never a low score or a no-referral default. Synthetic source/assessment authoring must cover the five factors; neither the LLM nor a case-author numeric rating can cure a known missing/conflicting material source. Trusted configuration defines method/material-input requirements, not uploaded instructions. No actual case/source file is authored by this edit.

Worked arithmetic supplied by the user (illustrative, not a completed application run or a score assigned to an existing loan):

| Factor | Supplied rating | Weight | Contribution |
|---|---:|---:|---:|
| Repayment capacity | 60 | 0.30 | 18 |
| Financial leverage | 40 | 0.20 | 8 |
| Collateral quality | 30 | 0.20 | 6 |
| Borrower credit profile | 20 | 0.20 | 4 |
| Business and industry risk | 50 | 0.10 | 5 |
| Total | | 1.00 | 41/100 |

Validation and absence behavior:
- Exactly the five fixed factor IDs are required once; no extras/duplicates, inferred ratings or implicit zeros. Factor values are finite Decimal0–100 and serialize as canonical Decimal strings; reject Boolean, NaN/infinity, out-of-range and noncanonical/coerced inputs. Preserve explicit valid0 and100.
- Method weights are the fixed versioned decimals above, finite/nonnegative and sum exactly1.00. A changed weight is a new reviewed method version, not an ordinary UI edit. Use Decimal precision50; store unrounded contributions/total and display two decimals with ROUND_HALF_UP (trailing display zeros may be omitted). No silent clamping or score rounding before validation.
- Runtime FactorRiskAssessment carries factor ID/rating, assessment ID/version, reason/rubric reference, material-input requirement IDs and supporting source/assessment references, validation status, CASE_AUTHOR_ASSESSED attribution, as-of/basis and matching deal/input revision. Reference a synthetic statement/history/industry note where required; assessment references are not fake PDF citations. Repayment depends on valid financial inputs/basis; financial leverage and collateral depend on their material calculation inputs; credit profile/business risk need their supplied synthetic assessment basis. A scenario's explicit material-input registry is reviewed with its sources, never guessed at runtime. Missing/conflicting/invalid material input makes the affected factor unusable even if a numeric rating is present. Automatic ratio-to-factor scoring remains undefined; an approved authored rubric/assessment is required before a factor rating is used.
- Material-input authoring minimums: repayment references CFADS and annual principal/interest on the documented compatible basis; leverage references supported funded debt/EBITDA inputs; secured-equipment collateral references eligible valuation, secured exposure and lien basis. Unsecured applicability follows CasePolicyConfig: do not force an equipment valuation/LTV requirement or silently set collateral risk to zero; the authored collateral-factor rubric must explicitly describe that unsecured case. Credit profile and industry reference the supplied synthetic history/assessment basis. The case-author record is attributed assessment evidence, not an invented PDF or actual bureau verification. A method/configuration without the needed applicability/rubric is not ready for scoring.
- Missing/unusable factors or material inputs return status INSUFFICIENT_DATA, null total/band and a specific missing/conflict list. Invalid configuration/trace remains INVALID or NOT_ASSESSED, never a numeric value. Do not renormalize or calculate a partial composite as complete. Factor coverage remains secondary detail, not document completeness. A missing evidence requirement unrelated to the five score inputs may coexist with a valid numeric score, but its separate workflow gate still prevents readiness.
- The user supplied bands and confirmed continuous decimal boundaries/unrounded classification: SCORE-BANDS-1.0 is Low0–25 inclusive; Moderate>25–50 inclusive; High>50–75 inclusive; Very High>75–100 inclusive. Classify the exact Decimal total before two-decimal display;25.5 is Moderate and50.004 is High even if displayed50.00.41/100 is Moderate, not41% PD. Bands are illustrative project configuration, not industry standards, calibrated grades or automatic loan decisions. SCORE-ROUTING-1.0 below adds mandatory human routes while preserving every independent policy/evidence/control gate. PD/LGD/EAD/expected loss and concentration inference remain outside scope.
- Compute only as a deterministic helper inside the existing risk_quantifier invocation from versioned case assessments. No additional registered tool/graph node/model call. Opening a card or memo reads the recorded artifact and never recomputes it. A dependent assessment/fact/source/method revision invalidates the prior artifact and requires the existing explicit continuation path to produce a current score. Preserve historical artifacts/no automatic expiry.

RiskScoreResult: method_id RISK-EDU-1.0, band_config_version SCORE-BANDS-1.0, material_input_config_version, scope/revision/as-of, assessment/source refs/digest, factor ratings/weights/contributions, exact total/display nullable, HIGHER_MORE_RISK direction, coverage/5, missing/conflicting material requirements, completeness/limitations, status COMPUTED_FROM_SYNTHETIC_ASSESSMENTS/INSUFFICIENT_DATA/NOT_ASSESSED/STALE/INVALID, reason and band LOW/MODERATE/HIGH/VERY_HIGH nullable. The original five-factor arithmetic is unchanged; versioned band/material-input config changes invalidate dependent output. Inputs/results use Decimal strings. The bounded risk-panel projection can now include a complete score/band/method and supported driver references for synthesis; it remains read-only input, never permission to alter the five-field PanelDecision schema, replace gates or fabricate factors.

### Independent score referral controls — SCORE-ROUTING-1.0

These are DEMO_PRODUCT_CONTROL records, separate from SAMPLE-LOAN-POLICY-1.0 lending-rule outcomes and excluded from the Policy exceptions count. The user confirmed Moderate always requires human underwriting, using existing personas/worker/HITL flow:

| Score/data state | Control ID | Required simulated owner/action | Completion behavior |
|---|---|---|---|
| Low0–25 | No new score referral | Continue standard review | Existing amount/confidence/policy/evidence/control rules still decide required review |
| Moderate>25–50 | SCORE-REVIEW-MODERATE | Authorized Approver, NORMAL package review | REVIEW_REQUIRED; no direct report completion before recorded human disposition |
| High>50–75 | SCORE-REVIEW-HIGH | Credit Risk Manager (existing RiskManager persona) records credit-risk assessment handling; then Authorized Approver package review | ESCALATE; specialty handling and final package review are separate prerequisites |
| Very High>75–100 | SCORE-REVIEW-VERY-HIGH | Senior credit authority (existing AuthorizedApprover persona, SENIOR review tier) | ESCALATE; required senior-tier disposition; any independent Risk Manager/compliance prerequisites remain |
| Missing/unusable material scoring input | SCORE-DATA-MISSING | Credit Analyst or existing configured evidence owner supplies/corrects the named source/assessment | NEEDS_INFORMATION; score Insufficient Data, dependent synthesis/final-decision readiness paused |

No sixth persona, extra agent/node, external notification, legal-clearing authority, automatic Reject or weighted merge with policy/evidence is added. UI owner categories explain the mapping to the existing simulated personas. SENIOR is a required ReviewRequest tier/capability within the demo, not verified identity or a real bank delegation. Original numeric exceptions retain their existing four-rule Risk Manager dispositions. High-score credit-risk handling is a distinct new capability limited to SCORE-REVIEW-HIGH; it cannot waive policy/control/evidence gates. Generic acknowledgement cannot satisfy it.

Effective human referral is amount trigger OR confidence trigger OR active score referral OR any other mandatory referral, but missing/blocked prerequisites take their existing dispatch precedence. Unknown/invalid/stale score never yields false/no-review. Once the current required handling and review tier are recorded, unchanged score predicates must not create an endless referral/resume loop. Corrections invalidate all dependent band/referral/review artefacts, and analytical reruns share the original budgets. Low scores and fulfilled score referrals never clear independent exceptions/evidence.

Case-level assessment summary is a derived read model: Credit risk=value/band or Insufficient Data; Policy checks=count unique current applicable INTERNAL_SAMPLE_POLICY rules with outcome Exception (deduplicate underlying rule/revision, not repeated agent flags); Evidence=count unique unresolved required missing-evidence requirement IDs from issues/material-input registry. Keep Unknown/not-checked controls and conflicting evidence separately labeled in details; pending/incomplete checks are not zero exceptions. Exclude score/amount/confidence product-referral controls from the exception count and do not treat a valid factor coverage5/5 as evidence completeness.

The illustrative41/Moderate +2 Exceptions +1 Missing layout is valid only when the missing requirement is outside the material score inputs. A missing CFADS/valuation/other material factor input must instead show Insufficient Data, not41. Missing mandatory control evidence can leave a numeric score valid while blocking readiness; retain its actual Compliance owner/action. Referral suggestions can coexist with that blocker but cannot become the primary permitted action if its prerequisites are unmet. Counts and all cards share the same input revision/source policy scope; historical score plus new evidence is not a current assessment.

evaluate_policy(PolicyRequest) -> StageEnvelope[CompliancePanel].
calc_credit_risk(RiskRequest) -> RiskFlags; calc_concentration_risk(RiskRequest) -> NotAssessedResult; compose RiskPanel without inference.

RuleResult: rule_id/version, authority INTERNAL_SAMPLE_POLICY or DEMO_PRODUCT_CONTROL, applicability APPLIES/NOT_APPLICABLE/UNKNOWN with reason/basis, observed/comparator/threshold/unit nullable, outcome Pass/Exception/Unknown/Not applicable, source/metric refs, issue_id nullable.
RuleResult additionally carries an evaluation_trace reference or compact typed trace: approved predicate/handler version, ordered condition operands/operators/grouping, recorded condition states, mapped outcome/consequence and original input/calculation/source references. This is an arithmetic/control execution explanation, not LLM chain-of-thought. The same Python handlers that produce results populate the trace; no expression parser, eval(), generic rule-engine dependency or user-editable rule DSL is added.
get_rule_evaluation_details(ScopedRuleResultRef) -> RuleEvaluationDetails is a scoped read service joining that trace with existing current/historical artifact, source registry, financial calculation and permitted-action projections. Return explicit missing/stale/mismatch diagnostics rather than manufacturing an explanation. No new database, endpoint, model response schema or audit event is required. Details are read-only and use the exact recorded policy/input version, not whichever config is newest.
CompliancePanel: policy_version, rule_results, issue_refs, completeness.
RiskFlag: flag_id, category, supporting_issue_ids, observed/threshold/gap/direction/unit nullable, metric/rule/source refs, evidence status, severity/owner from config.
RiskPanel: risk_flags, risk_score_result (the versioned RISK-EDU-1.0 result or explicit incomplete/invalid status), concentration status/reason, issue_refs, completeness. No other aggregate is inferred. Score referrals are produced by the Python router from this artifact and its configuration, rather than multiplying policy exceptions.

The [SCOREVIEW-1.0 presentation](command-center-ui.md#risk-score-cards--scoreview-10) now shows three independent Credit risk, Policy checks and Evidence cards; factor coverage is secondary score detail. It creates no bank/customer risk model or merged credit/compliance/evidence number. Missing material scoring data is Insufficient Data. No case score is presumed until its five assessments and supporting material inputs are authored/validated; existing flags and independent gates remain authoritative alongside the added score referrals.

P3-01 aggregates unresolved issues as BLOCKED > NEEDS_INFORMATION > ESCALATE > REVIEW_REQUIRED > CONTINUE for summary only. All underlying issues/scopes remain. Nodes are gated by dependencies and blocks_completion, not by sorting severity. Dispositioned exceptions retain their original numerical Exception; history and effective gate state are separate.

SOURCEFIT-1.0 requires trusted policy-version applicability for the selected review date/purpose/product and current eligible input lineage. A later policy upload or version number is not automatic authority or retroactive applicability. Unsupported effective dates, authority or tiers return Unknown/configuration/information gates, never silent Pass/Not applicable or credit Reject. No sample threshold, executable policy precedence, recency duration or blanket expiry is added. View rule evaluation shows the actual selected policy version/basis and operand sources; existing TEST-004-02/09 verify this with focused E-C variants.

## AI and evidence behavior

Zero model calls. Policy references navigate to rule/version content and authority label. A deterministic comparison does not imply confidence=1 or legal compliance. Unsupported ambiguity raises CONFIGURATION_REQUIRED and pauses affected conclusions.

## Authorization

Only orchestration evaluates panels. Owner assignment never grants resolution rights. P3-02 mapping in SPEC-008 governs separate sample-exception/control dispositions. Unconfigured owner/capability is denied, not granted to Administrator.

## UI states

Empty: panels not run/policy unavailable. Loading: actual Python stage. Success: Pass/Exception/Not applicable by rule, risk gaps and sources. Partial: Unknown with missing fields. Blocked: explicit control/configuration issue, owner and permitted action; no automatic credit Reject.

## Reliability and stopping

Three scheduled boundaries here: evaluate_policy, calc_credit_risk, calc_concentration_risk. No agent loops. Missing rule pack is POLICY_UNAVAILABLE; invalid version/config is CONFIGURATION_REQUIRED. Tool exceptions follow SPEC-007 limits; contradictory input cannot be retried into a favorable result.

## Analytics

policy_panel_computed; risk_panel_computed; issue_created/status_changed with rule/category/severity/owner/scope; control_fixture_applied only through SPEC-008. No borrower data or quoted policy/source payloads.

## Tests and acceptance

- TEST-004-01: All numerical equalities/adjacent violations; USD-5M nonexecution of retired 003; RULEVIEW-1.0 displays the same exact comparator/value/outcome as the Python predicate, including inclusive amount and exclusive confidence boundaries.
- TEST-004-02: Required versus Not applicable controls, missing status, unknown applicability/policy. SOURCEFIT-1.0 validates selected policy date/purpose/product applicability without automatic retroactivity or silent precedence.
- TEST-004-03: Synthetic unresolved KYC/sanctions blocked; no actual screening claims.
- TEST-004-04: All five workflow statuses and four severity categories; aggregation preserves every issue and gate.
- TEST-004-05: Exact gaps/units, issue deduplication, no unapproved composite score or concentration method. Only the explicitly versioned RISK-EDU-1.0 aggregation below is permitted.
- TEST-004-06: Sample-exception handling preserves original Exception; source/case changes invalidate stale dispositions.
- TEST-004-07: Policy/manual injections cannot alter trusted configuration; zero inference.
- TEST-004-08: QA-RISK-FP-01 records an offline false-positive risk count against synthetic expected findings, counts a repeated underlying risk once, and preserves the existing unsupported-critical-claim gate. No new UI or precision threshold is required.
- TEST-004-09: Rule details match original handler/trace/input/policy versions, sources, calculation and consequence; preserve recorded compound grouping/other referrals, pre-synthesis Not evaluated, missing/Unknown/Not applicable and historical/retired distinctions. Unknown refs/version/trace mismatch cannot display a verified check. Opening details performs zero graph/tool/provider calls or mutations; source correction and authorized disposition remain separate actions.
- TEST-004-10: Fixed weights and supplied60/40/30/20/50 yield41/Moderate; valid0/100, invalid/missing/duplicate/nonfinite/Boolean/out-of-range ratings, material-input/rubric/provenance/version failures and Decimal arithmetic behave as defined. Missing material data yields null score/band and Insufficient Data without reweighting or invented sources; current/stale and factor-versus-document coverage remain distinct. No PD, predictive calibration claim, added model/tool or recomputation-on-view.
- TEST-004-11: SCORE-BANDS-1.0 classifies exact0/25/25.0001/25.5/50/50.004/75/75.0001/100 before rounding; SCORE-ROUTING-1.0 applies confirmed Moderate/High/VeryHigh tiers plus independent gates. Three summary counts deduplicate policy rules and required evidence roots, exclude product referrals, preserve Unknown/not-run states and cannot mix revisions.41 with a non-score-material gap may remain valid/blocked;41 with missing CFADS is prohibited.

Targets: 100% controlled policy/routing cases; no missed critical control exception. Representative E-P01–P05, E-C01–C04, E-M01–M03, E-A01/A03.

## Dependencies and implementation boundary

Consumes SPEC-002/003, feeds SPEC-005/007/008/009. Rule JSON/YAML, capabilities and config are proposed contracts; actual files await the repository/implementation gates.
