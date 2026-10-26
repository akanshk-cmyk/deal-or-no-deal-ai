# Deal or No Deal AI — Domain and Product Review Checklist

Version: 1.1  
Review date: 2026-10-23  
Status: Seven documentation findings resolved by the user's request to fix the identified issues; runtime verification pending  
Initial review baseline: PRD v1.27, HLD v1.20, specification overview v1.9  
Current corrected baseline: PRD v1.28, HLD v1.21, specification overview v1.10  
Purpose: A credible five-day educational loan-review demonstration, not operational banking readiness

## 1. Review method and boundaries

1. Establish the actual scope and distinguish an educational recommendation from an external financial action.
2. Follow one deal from documents to extracted facts, calculations, policy/risk panels, recommendation, human handling and report.
3. At each handoff ask: what is known, what supports it, what is missing, who can act, and what prevents completion?
4. Compare each checklist item with the written contracts. A stated intention without a usable field, service or acceptance check is only partial coverage.
5. Prioritize small specification fixes that prevent a misleading or blocked demonstration. Separate missing requirements from already planned work and deliberately deferred capabilities.

This review uses credit analyst, risk, compliance, approver and engineering perspectives. It does not represent the internal policies of JPMC, Wells Fargo, Citi, Morgan Stanley or NYLife. Insurance underwriting and equity investment analysis are different products and remain outside this MVP.

Confirmed: synthetic USD term loans; same-loan debt-risk perspective; five screens; five simulated personas; Python/LangGraph; two normal inference stages; Nebius access later; fixed cumulative cost/token limits; local persistence without automatic expiry. The current score requires supplied case-author factor assessments, not LLM-generated grades. Repository and implementation gates remain pending.

No new lending thresholds, factor-rating formulas, document-expiry rules, legal interpretations or external actions are assumed. The user subsequently authorized fixing all seven findings; section 6 records the reconciled decisions. The initial checklist/findings below preserve the evidence and reasoning from before the fixes, rather than implying the old gaps remain current. Runtime implementation and later phase gates remain pending.

## 2. Checklist and comparison

Status meanings: **Specified** = adequately described for this educational scope, but unimplemented/unverified. **Partial** = intent exists but the contract or supported workflow needs clarification. **Prerequisite** = already acknowledged work or approval, not an overlooked feature. **Deferred** = an intentional scope boundary.

| ID | Review question | Initial document status | Initial evidence / finding |
|---|---|---|---|
| C01 | Is there one narrow borrower/product/workflow and a clear educational boundary? | Specified | [PRD](../product/prd.md), [overview](../specs/overview.md); term-loan review, not several financial products |
| C02 | Are success measures defined without claiming observed savings or quality? | Specified | [Evaluation plan](evaluation-plan.md); learning, workflow, quality, cost and latency distinguished |
| C03 | Can a prepared case and an uploaded synthetic deal each reach a supported outcome? | Partial | [Intake](../specs/document-intake.md), [risk](../specs/policy-risk.md); no complete factor-assessment onboarding contract for an unregistered upload — SME-01 |
| C04 | Are format, page/byte limits, unreadable pages and source versions handled? | Specified | Intake; three text PDFs, ten pages, fixed byte cap, explicit failure and passage provenance |
| C05 | Do statements, debt schedules and collateral belong to the reviewed borrower and facility? | Partial | [Extraction](../specs/extraction.md) captures borrower; financial contracts check periods/bases but lack an explicit subject/entity-coherence rule — SME-02 |
| C06 | Are missing, conflicting, invalid and explicit-zero facts distinct? | Specified | Extraction, [shared contract](../agents/shared-contract.md); no invented source precedence |
| C07 | Are definitions, units, periods, liabilities and repayment double-counting controlled? | Specified | [Financial analysis](../specs/financial-analysis.md), [FIN-1.0](../agents/financial-analyst.md); Decimal and source-supported inputs |
| C08 | Is reported/adjusted EBITDA reconciliation actually representable? | Partial | Extraction promises preservation; strict eighteen-field financial wire has no reported-EBITDA slot — SME-06 |
| C09 | Are repayment source, repayment structure and analysis horizon clear? | Partial | Annual DSCR is specified; full-term/balloon repayment coverage is not — SME-07 |
| C10 | Are collateral applicability, valuation basis and prior liens explicit? | Specified | Financial/risk contracts; no invented haircut or expiry, no forced equipment LTV for unsecured cases |
| C11 | Are guarantees preserved without inferring recovery value or enforceability? | Specified | Extraction and [synthesis](../specs/synthesis-evidence.md); documentary facts separate from proposed conditions |
| C12 | Are fictional bank policy rules versioned and distinct from product controls/law? | Specified | Risk/compliance; score, amount and confidence referrals excluded from lending-exception counts |
| C13 | Can a user inspect the executed rule, inputs, formula and consequence? | Specified | RULEVIEW-1.0 in risk/UI contracts; inspection cannot clear a gate |
| C14 | Are contractual covenants distinguished from bank-policy tests? | Partial | Covenants are sourced strings, but evaluation coverage/status is not explicit — SME-05 |
| C15 | Is the educational score transparent, complete and separate from other assessments? | Specified | RISK-EDU-1.0/SCOREVIEW-1.0; five factors, fixed weights, separate policy/evidence cards; Insufficient Data when material inputs are absent |
| C16 | Do unrounded bands and required human routes behave consistently? | Specified | SCORE-BANDS-1.0/SCORE-ROUTING-1.0; Moderate always human; High specialty plus package review; Very High senior tier |
| C17 | Can known source errors be stopped without treating a resolving citation as truth? | Partial | Evidence intent exists; critical extracted Fact support and the claim-only support command need an explicit bridge — SME-03 |
| C18 | Are required evidence, policy handling, score handling and final disposition separate? | Specified | [Human review](../specs/human-review-corrections.md); generic acceptance grants no waiver |
| C19 | Can outstanding conditions be shown without implying missing critical evidence was cleared? | Partial | Memo consumes condition records; precise typed condition category/completion semantics are missing — SME-04 |
| C20 | Are recommendation, human disposition, workflow readiness and report completion separate? | Specified | UI/memo; technical failures and information pauses are not Reject |
| C21 | Are agents' responsibilities and handoffs real, typed and observable? | Specified | [Orchestration](../specs/orchestration-budgets.md); three core roles, seven specialist responsibilities and deterministic coordination |
| C22 | Are prompts, source isolation, context packing and retrieval boundaries controlled? | Specified | [Context contract](../specs/context-optimization.md); DIRECT baseline; optional offline hybrid benchmark, no runtime web agent |
| C23 | Do retry, correction, cancellation and restart preserve one cumulative allowance? | Specified | Orchestration/[persistence](../specs/persistence-observability.md); uncertain requests retain reservations; no paid replay |
| C24 | Do corrections invalidate scores, findings, recommendations and stale review? | Specified | Human review/orchestration; Save does not dispatch; explicit continuation shares review budget |
| C25 | Are audit, retention and simulated-role limitations stated honestly? | Specified | Persistence; explicit events, SQLite profile, RAM saver limitations, no immutable-audit claim or automatic expiry |
| C26 | Are source evidence, blockers, owners and permitted actions easy to find? | Specified | [UI contract](../specs/command-center-ui.md); five screens, progressive detail, keyboard/narrow-layout checks planned |
| C27 | Do evaluations distinguish Approve, Conditional, Reject, missing information and technical failure? | Specified | Evaluation plan; E-N01, E-P01, E-F03, E-M01 and focused technical controls; false-positive counts remain offline |
| C28 | Are source packs, factor assessments and matching fixtures actually authored? | Prerequisite | Evaluation plan acknowledges authoring; no runtime source/fixture artifacts exist yet |
| C29 | Are provider compatibility, structured outputs, tokenizer, prices and full serialized payload fit checked? | Prerequisite | [Repository proposal](../architecture/repository-design.md); no successful Nebius measurement yet |
| C30 | Are repository approval, execution/design planning and first implementation approval complete? | Prerequisite | Repository proposal pending; future execution/design-system documents are expected next-phase work |
| C31 | Are trained PD/LGD/EAD, full portfolio concentration, commercial pricing and operational controls needed now? | Deferred | PRD; none is necessary for this educational demonstration |
| C32 | Is a debt-investment lens kept separate from investment valuation or trade execution? | Specified | PRD scope; same loan's repayment/credit risk, without yield, fair value, portfolio allocation or suitability claims |

The initial checklist had 21 Specified, 7 Partial, 3 Prerequisite and 1 Deferred items. The seven Partial findings are now resolved at specification level by section 6, giving 28 Specified, 3 Prerequisite and 1 Deferred. These are document-review classifications, not a test pass rate. C17 was a support-contract clarification rather than absence of evidence controls. The score formula itself was already specified under C15; its upload-population gap was C03/SME-01.

## 3. Findings and smallest useful adjustments

**Priority A** means resolve the specification before implementing that path: otherwise a valid-looking result can be misleading or the supported workflow can dead-end. **Priority B** means bound or clarify behavior before the demo; prefer explicit limitations over a new subsystem. These review priorities are not application risk severities or regulatory classifications.

### SME-01 — Priority A: close the factor-assessment intake gap

Evidence: intake accepts arbitrary synthetic packages in Live mode, while the complete risk score requires five trusted case-author assessments and material-input configuration. The UI has no specified action that creates those trusted assessments. Authoring is already acknowledged as pending; its connection to the upload journey remains incomplete.

Consequence: a well-formed uploaded loan can extract correctly but remain permanently Insufficient Data, even when the user expects a complete review. The displayed five-factor score must also disclose that Python aggregates supplied assessments rather than independently deriving grades.

Recommended five-day boundary: complete decision walkthroughs use prepared, reviewed synthetic case packs. Unregistered uploads clearly support extraction/partial analysis only until an instructor supplies reviewed assessment/configuration through the trusted case-authoring path. This is a proposed scope clarification, not an approved restriction. Do not add a scoring LLM or let an uploaded policy define trusted ratings.

Acceptance: one registered complete pack works; one otherwise complete unregistered upload explains the exact missing assessment prerequisite and available partial outcome; neither copies another case's grades. Preserve the current Insufficient Data and no-reweighting requirements. Existing core fixtures need their authored factor packs before execution.

### SME-02 — Priority A: add borrower/entity and facility coherence

Evidence: source identity/deal/revision and PeriodBasis are specified, but entity attribution is not part of the financial-input acceptance contract. A shared deal ID does not prove that a statement belongs to the borrower rather than a parent, guarantor or unrelated company.

Recommended adjustment: attach a trusted subject/entity scope and statement role to source/basis metadata. Compare borrower, financial subject, debt schedule and collateral ownership/basis before combining affected inputs. Explicitly supported consolidated information must describe its scope; do not assume name similarity proves identity or require a new external identity service.

Acceptance: a package with another entity's financial statements cannot produce a trusted borrower ratio; a supported entity-scope clarification restores only affected work. Add a focused variant of existing E-C03 rather than a new scenario family. Reuse the existing information/conflict mechanism; no automatic Reject or regulatory KYC claim.

### SME-03 — Priority A: make critical fact support an actionable contract

Evidence: extraction explicitly says hydration does not prove semantic accuracy. EvidenceReview checks references and copied values; semantic assessments currently target claim_id, while extracted inputs are Fact records. The intention to stop unsupported critical inputs is present, but the Fact-to-support-review path is not precise enough to implement consistently.

Recommended adjustment: specify a scoped fact-support target, or an explicit Fact-to-Claim linkage, for critical inputs such as amount, CFADS, debt service, debt, valuation, units and entity/period basis. Define mechanical checks versus operator support checks and the status that permits each downstream use. A number occurring in a cited passage is insufficient when it belongs to another row, period or entity. Unknown support must not silently become validated.

Acceptance: a valid passage containing the wrong period/row or a wrong-scale amount cannot acquire a trusted support label; supported correction/review is recorded with current lineage. The Low direct-report path retains its configured underwriting rules but cannot acquire a false claim of semantic verification. Reuse E-C03/C04 and current support tests; no judge-model call or implied universal credit-committee review.

### SME-04 — Priority A: define conditions and completion semantics

Evidence: source covenants, AI-proposed conditions and reviewer edits are distinguished conceptually. However, condition records consumed by the memo have no complete shared contract for category, owner, support, status and whether they represent an existing blocking prerequisite.

Recommended adjustment: define a small ConditionRecord with identity/revision, origin/category, text, supporting refs, owner, status and linked existing issue/gate where applicable. The authoritative prerequisite remains the configured issue/rule, not an LLM-selected blocking flag. Distinguish a missing pre-decision requirement from a proposed condition of a simulated Conditional Approve and from a sourced future covenant. Do not build a funding workflow or covenant-monitoring system.

Acceptance: missing current CFADS remains an information pause even if proposed as a condition; a supported Conditional Approve may appear in a completed review report with explicitly outstanding proposed conditions. Report completion never means funded, conditions fulfilled or a mandatory gate waived. Reuse E-M01, E-P01 and existing memo/HITL checks; approval is needed for the exact proposed condition contract.

### SME-05 — Priority B: state what covenant review actually covers

Evidence: covenants are extracted as strings with source references; executable bank-policy thresholds do not represent every agreement's contractual covenant, definition or testing date.

Recommended five-day adjustment: explicitly label contractual clauses Extracted — not automatically evaluated unless a reviewed case supplies a compatible comparison and basis. Keep their exact definition, period and qualifiers accessible. Use manual, attributed review where needed; do not advertise general contractual covenant compliance.

Acceptance example, illustrative only: a supplied agreement's minimum DSCR can differ from the sample bank's policy minimum. A policy Pass must not imply covenant Pass, and the application must not compare incompatible DSCR definitions. A focused existing-case variant is sufficient; no universal new covenant threshold or rule editor.

### SME-06 — Priority B: reconcile the reported-EBITDA contract mismatch

Evidence: [Extractor instructions](../agents/extractor.md) and extraction specifications promise to retain reported EBITDA for reconciliation, but [DealTermsWire](../specs/examples/extraction-wire.md) allows exactly eighteen financial keys, none for reported/adjusted EBITDA. Strict rejection of extra keys makes that promise ambiguous.

Recommended adjustment: choose explicitly between one optional source-linked reported-EBITDA observation, with corresponding schema/fixture/budget updates, and deferring that reconciliation claim. Preserve FIN-1.0's derived unadjusted EBITDA; no discretionary addbacks or automatic substitution. The choice is open, not silently resolved here.

Acceptance: if supported, a documented adjusted number remains distinguishable from computed FIN-1.0 EBITDA and does not overwrite leverage inputs; otherwise the UI/instructions clearly say reconciliation is outside the demo. Reuse existing financial tests, not another financial agent.

### SME-07 — Priority B: bound annual repayment analysis versus full-term risk

Evidence: the calculation contract uses one supplied annual assessment basis and supplied debt service. Repayment structure is text; there is no amortization forecast, rate stress or explicit full-term/balloon repayment assessment.

Recommended five-day adjustment: state in the financial summary and memo that DSCR describes the supplied assessment period. Preserve repayment structure, maturity and use of proceeds from the document; do not let a favorable annual ratio imply demonstrated repayment over the entire facility. Mark unsupported balloon/refinancing or future-period analysis Not evaluated, with its limitation. A richer supplied schedule/stress analysis is an optional future feature requiring definitions.

Acceptance: an illustrative annual interest-only period does not support an invented conclusion about a later principal balloon. There is no new forecast, recovery assumption or automatic Reject. Keep the debt-investment view limited to the same loan's supported credit/repayment observations, not investment return or suitability.

## 4. What is already sound, and what to defer

Keep: deterministic financial/policy/risk/report nodes; two normal generation stages; versioned shared state; exact five-field PanelDecision; separate policy/evidence/credit assessments; mandatory review tiers; complete evidence visibility; current-source correction/invalidation; supported E-F03 Reject distinct from missing data/failure; offline risk false-positive QA; bounded attempts/cost and no silent replay.

The deterministic coordinator is appropriate for a known process. Describe the deliverable honestly as a bounded multi-agent workflow with specialist roles and two model-backed stages, rather than several independent autonomous underwriting agents. LangChain's own documentation distinguishes predetermined workflows from dynamic agents. This is a terminology clarification, not a reason to add calls. [Official LangGraph workflow guidance](https://docs.langchain.com/oss/python/langgraph/workflows-agents).

Do not add for this review: live credit bureaus, actual sanctions/KYC checks, loan origination integrations, trained default prediction, LGD/EAD, valuation/yield/pricing, continuous covenant monitoring, multi-tenant security, distributed workers, more LLM specialists or default vector retrieval. Optional hybrid benchmarking remains isolated from the default DIRECT path.

## 5. Domain references and regulatory comparison

The OCC identifies business cash flow as the usual primary repayment source for small-business loans and discusses current/expected cash-flow analysis. That supports emphasizing repayment evidence and disclosing the educational demo's limited assessment horizon; it does not establish this project's DSCR thresholds or require adding a forecasting system. [OCC small-business lending](https://www.occ.treas.gov/topics/supervision-and-examination/credit/commercial-credit/small-business-lending.html).

The existing PRD already records the April 17, 2026 replacement of SR 11-7/SR 21-8 by SR 26-2 and the attachment's exclusion of generative/agentic AI from its scope. This review verified that correction; it is not a missing requirement. The attachment still points to institution-appropriate governance for tools outside that guidance. Do not present this educational system as regulator-validated or imply that guidance exclusion removes other applicable obligations. [Federal Reserve replacement notice](https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm), [scope attachment](https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf).

No firm's internal policy, legal applicability determination or operational banking certification is inferred from these public sources. Existing fictional rules remain unchanged.

## 6. Authorized resolutions and remaining gates

Authorization: the user requested Fix issues identified on2026-10-23. The following decisions are now reflected in the PRD, HLD, shared/feature contracts, affected specialist instructions, evaluation plan and traceability. Status means DOCUMENTATION_FIXED, not application tests passed.

| Finding | Resolution | Canonical contract / planned verification |
|---|---|---|
| SME-01 | Registered reviewed source/factor/subject packs support complete walkthroughs; unregistered Live uploads explicitly remain partial, without borrowed grades or PanelDecision. Case preparation is trusted offline authoring, not a new score-entry UI | [SPEC-001](../specs/document-intake.md); TEST-001-05/004-10/010-02 |
| SME-02 | Subject/facility/passage-role registry with documented consolidated scope; unknown/conflicting attribution pauses affected trusted use | [SPEC-001](../specs/document-intake.md), [SPEC-003](../specs/financial-analysis.md); TEST-002-03/003-04, E-C03 variant |
| SME-03 | FACT-SUPPORT-1.0 and typed FACT/CLAIM review bind exact current evidence. Critical Live facts require HUMAN_SUPPORTED before trusted dependent use; Fixture execution is demonstration-only. Support Save invokes nothing; explicit same-revision continuation preserves ledger, avoiding extraction replay | [SPEC-002](../specs/extraction.md), [SPEC-007](../specs/orchestration-budgets.md), [SPEC-008](../specs/human-review-corrections.md); existing support/routing/evidence tests |
| SME-04 | CONDITIONS-1.0 records origin/category/owner/status/refs and derive blocking from existing issues. Outstanding supported proposals can remain in a completed simulated Conditional review; current missing evidence cannot be waived or called fulfilled/funded | [SPEC-008](../specs/human-review-corrections.md), [SPEC-009](../specs/credit-memo.md); E-P01/E-M01 and existing HITL/memo tests |
| SME-05 | Contract clauses show EXTRACTED_NOT_EVALUATED; fictional bank-policy Pass is not covenant compliance | [SPEC-003](../specs/financial-analysis.md), [SPEC-005](../specs/synthesis-evidence.md); TEST-003-07/005-03/010-03 |
| SME-06 | Defer reported/adjusted-EBITDA normalization and automated reconciliation. Preserve source inspection, strict eighteen financial keys and FIN-1.0; no invented retained observation or mismatch alert | [SPEC-002](../specs/extraction.md), [wire example](../specs/examples/extraction-wire.md); TEST-002-07/003-07 |
| SME-07 | Disclose supplied annual-period/subject scope; full-term/balloon/refinancing adequacy NOT_EVALUATED. Preserve source repayment/maturity/use facts without new forecasts or automatic Reject | [SPEC-003](../specs/financial-analysis.md), [SPEC-009](../specs/credit-memo.md); TEST-003-07/005-03/009-02 |

The previous four open specification choices are resolved by these decisions. Remaining prerequisites are actual reviewed source/factor/configuration and fixture authoring, dependency/parser/saver/license and serialized-payload feasibility checks, and later authorized Nebius model/rate/token verification. No need for additional model agents, thresholds, vector infrastructure, production controls or a full covenant/conditions engine follows from the fixes.

Next sequence remains the pending repository-design approval, execution/design-system planning, first implementation milestone approval, implementation and focused core verification. Preserve five screens/personas, two normal generation stages, current cumulative limits, thirty scenario designs, ninety planned TEST IDs, existing metrics/tasks and no automatic expiry. The five-day implementation target still starts after prerequisite approvals; it is not a measured delivery result.

Only documentation was changed for these fixes. No runtime source packs, factor fixtures, application code/tests, notebook, HTML, paid model call or deployment was produced. Static link/contract checks are document review only; application and AI-quality results remain Not run.
