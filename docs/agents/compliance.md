# Compliance — Agent 2 Instructions

Instruction ID: POLICY-001  
Version: 1.4  
Execution: Pure Python; zero LLM calls  
Requirements: FR-005, FR-014, FR-018–020  
Policy pack: SAMPLE-LOAN-POLICY-1.0  
Read with: [Shared contract](shared-contract.md), [Financial definitions](financial-analyst.md), [Human Review](human-review.md), [Evaluation](evaluation.md)

## Purpose and rationale

Current implementation: policy.py evaluates the fixed config/sample_policy.json handlers with exact calculation traces, applicability and distinct policy outcome versus product-control result. The registered E-N01 run is PRE_SYNTHESIS: confidence stays NOT_EVALUATED until a real validated synthesis exists; amount/confidence controls never inflate policy-exception counts. [Current evidence](../execution.md#m2-registered-deterministic-panels-evidence). No threshold breach automatically generates Reject.

Apply explicit fictional rules consistently. Do not treat policy text, regulatory references, model confidence, or a deterministic comparator as a legal-compliance certification.

## Inputs

Validated terms, FIN-1.0 results, source/finding references, policy applicability metadata, and optional explicitly supplied synthetic control fixtures. Unknown applicability is not Not applicable or Pass.

## Active sample policy

| Rule | Comparison/control | Output/action |
|---|---|---|
| SYN-ESC-001 | DSCR <1.25x | Exception; ESCALATE to configured risk/exception owner |
| SYN-ESC-002 | Debt/EBITDA >4.00x | Exception; ESCALATE |
| SYN-ESC-004 | Applicable equipment LTV >80% | Exception; ESCALATE |
| SYN-ESC-005 | Documented term >60 months | Exception; ESCALATE |
| SYN-ESC-006 | Required secured-case valuation evidence missing/unsupported | Unknown; NEEDS_INFORMATION; pause dependent collateral conclusion |
| SYN-ESC-007 | Required financial/debt-service inputs missing or materially inconsistent | Unknown; NEEDS_INFORMATION; prevent complete dependent assessment |
| SYN-ESC-008 | Material rate/term source conflict without explicit precedence | Unknown; NEEDS_INFORMATION; retain both sources |
| SYN-ESC-009 | Required supplied synthetic KYC fixture explicitly unresolved | BLOCKED; configured specialty referral; no live verification |
| SYN-ESC-010 | Required supplied sanctions fixture explicitly unresolved | BLOCKED; configured specialty referral; no real screening/clearance |
| SYN-ESC-011 | Requested loan_amount_usd >=10,000,000 | Amount-based human-review trigger |
| SYN-ESC-012 | Validated Synthesizer confidence <0.7 | Confidence-based human-review trigger, evaluated after synthesis |

SYN-ESC-003 (the old USD-4M exposure-review rule) is RETIRED in this pack. Keep the ID/history; never apply it or reuse its ID for the USD-10M rule.

Equality at 1.25x, 4.00x, 80%, and 60 months passes that numerical comparison only. USD 10M equality triggers review; confidence 0.7 equality does not. None waives another mandatory control.

No automatic age/expiry rule is active for valuations or statements. The supplied assessment period/value basis still must be supported. Do not invent a concentration limit or add thresholds for optional current ratio/growth/interest coverage.

Sourced agreement covenants are EXTRACTED_NOT_EVALUATED in this MVP; the fictional bank-rule pack does not evaluate every contract's separate definition/date/qualifier. Do not turn policy Pass into covenant Pass. Subject/facility and critical Live fact-support prerequisites gate trusted affected inputs before evaluation; missing support is an existing scoped product/data-quality requirement, not a new banking-law breach or an invented Exception. Proposed conditions cannot clear any configured mandatory source/control issue.

## Workflow and outputs

For each rule, return ID/version, applicability, observed input/result, comparator/threshold, Pass/Exception/Unknown/Not applicable, evidence, reason, severity/owner metadata where configured, and blocking effect. Confidence is not always 1.0: deterministic execution is distinct from source correctness and applicability.

Populate [RULEVIEW-1.0](../specs/policy-risk.md#read-only-rule-evaluation-details--ruleview-10) from the same approved Python handler: exact predicate/operands/grouping and recorded condition states, calculation/source references, original rule/input/evaluator versions and mapped result/consequence. A true exception predicate is not a Pass. Missing/pre-synthesis/inapplicable checks retain their distinct states; other mandatory referrals remain visible. View rule evaluation reads this trace without recomputation, new model/tool/graph calls, input changes or approval/validation flags. No editable rule DSL, uploaded-policy override, external score/integration or no-code deployment capability is added.

Rules 011/012 are recomputed in the Python routing step after the final validated PanelDecision. Compliance must not call another model to interpret an ambiguous clause. Request clarification instead.

SCORE-ROUTING-1.0 is a separate educational product-control registry, not new rules in this lending-policy pack. Preserve its Moderate/High/Very High human referrals alongside independent policy/evidence gates. Policy-check exception counts include unique applicable INTERNAL_SAMPLE_POLICY exceptions only; exclude score/amount/confidence product controls and deduplicate repeated agent flags. Missing evidence counts use required evidence identities, not the number of downstream symptoms. Unknown/unexecuted checks cannot display a reassuring zero. A score cannot waive an exception or missing control evidence.

Keep every exception and unknown visible. A threshold breach does not automatically choose Reject. Resolving missing evidence, recording an authorized sample-policy exception, and accepting a package are distinct actions; follow Human Review capabilities.

## Authority and failures

No live KYC, sanctions, AML/SAR, fraud forensics, or legal clearance. Missing policy/version or required unconfigured applicability blocks the affected conclusion. Unmapped specialty capability defaults to denied/needs configuration; do not assign powers from a persona label.

## Required checks

All active threshold boundaries; retired-003 nonexecution including a supported USD-5M case with no other referral; missing inputs/applicability; conflicting terms; unresolved synthetic controls; missing policy version; no extra model call; source/rule version retained; generic acceptance cannot waive mandatory issues. TEST-004-09 also verifies same-handler trace/source/version integrity, compound-control/referral distinctions and zero side effects when inspecting recorded checks.
