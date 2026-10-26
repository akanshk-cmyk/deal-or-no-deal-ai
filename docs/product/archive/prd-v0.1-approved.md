# DealLens — Product Requirements Document

Status: Approved v0.1 — Phase 1 requirements baseline. Implementation remains subject to later phase gates.

Approval record: On 2026-10-22 the user replied “ok” to the request to approve the PRD, including its explicitly proposed choices. This establishes the scope, sample policies, limits, evaluation targets, retention boundaries, and HHH interpretation below as the approved baseline. Descriptions originally labeled proposed record their origin; targets remain unmeasured. This approval authorizes Phase 2 design only, not paid services, model execution, scaffolding, or deployment.

Project: 3B — Multi-Agent Deal Review Pipeline  
Date: 2026-10-21  
Working name: DealLens (proposed)  
Document phase: 1 — Discovery and PRD (approved; Phase 2 design is now authorized)

## Table of Contents

1. [Problem](#1-problem)
2. [User](#2-user)
3. [Core Metrics, Prioritisation & Roadmap](#3-core-metrics-prioritisation--roadmap)
4. [MVP Features](#4-mvp-features)
5. [Constraints](#5-constraints)
6. [Technical Requirements](#6-technical-requirements)
7. [Grounding Strategy](#7-grounding-strategy)
8. [Prompt Strategy](#8-prompt-strategy)
9. [Hallucination Guardrails](#9-hallucination-guardrails)
10. [Evaluation Strategy](#10-evaluation-strategy)
11. [Production Readiness Criteria & Metrics (HHH)](#11-production-readiness-criteria--metrics-hhh)
12. [Pricing](#12-pricing)
13. [Assumptions](#13-assumptions)

## 1. Problem

### 1.1 Confirmed project brief

Build an educational, local multi-agent application for a credit analyst reviewing small-business loans, including the same loan viewed as a debt investment. Assess borrower financials, loan terms, approved sample lending policies, collateral, covenants, and credit risks.

The required roles are an extraction agent, a policy/compliance review agent, a risk-and-summary agent, and an orchestrator. Additional agents are optional when justified. The user approved reviewing the same loan as a debt investment rather than adding a separate equity-review workflow.

### 1.2 Problem and business context

Proposed problem hypothesis: analysts spend substantial effort finding terms across documents, reconciling financial inputs, applying policy, and preparing review notes. Missing evidence and inconsistent interpretation can make findings difficult to verify. No interviews, baseline timings, or customer demand measurements have been collected.

Business objective: reduce time to an evidence-backed, human-reviewed brief while preserving accuracy, visibility of unknowns, and reviewer control. Educational objective: demonstrate agent delegation, structured communication, durable state, bounded retries, human review, and evaluations as code.

### 1.3 Current and proposed workflows

Current workflow is illustrative, awaiting validation: receive documents → read and record terms → calculate ratios → compare with policy → identify exceptions → write a memo → obtain review.

Proposed workflow: select synthetic deal and policy → ingest documents → extract cited facts → resolve material ambiguities → calculate and check policy → identify supported risks → inspect draft loan/debt-investment brief → correct and rerun affected work → acknowledge exceptions and finalize the review.

Finalizing a review means the analyst has reviewed the brief. It does not approve a loan, commit an investment, or certify legal compliance.

### 1.4 Why AI is justified

Use AI to interpret varied document wording, map clauses to defined concepts, and explain supported findings. Use ordinary software for arithmetic, explicit rule comparisons, schema validation, file handling, budgets, and workflow controls. A rules-only approach remains the baseline for structured inputs; the AI must demonstrate added value on unstructured text.

Multi-agent roles provide inspectable responsibilities and handoffs. A simple single-agent baseline will test whether the additional coordination improves quality enough to justify its cost.

## 2. User

### 2.1 Primary user and jobs to be done

Primary user: a credit analyst assessing a small-business loan and its risks as a debt investment.

| Job | Desired outcome |
| --- | --- |
| Understand the borrower and proposed loan | Verify key facts without repeatedly searching documents |
| Assess repayment capacity and security | Inspect calculated ratios, their inputs, and their limitations |
| Check approved sample policy | Distinguish failed checks from missing information |
| Evaluate the same loan as a debt investment | Understand contractual interest, maturity, security, repayment risks, and protections |
| Prepare and review a memo | Produce an editable, evidence-backed brief with outstanding questions |
| Learn how the system works | Inspect agent inputs, outputs, handoffs, and concise explanations |

Secondary user, proposed: an instructor or project evaluator inspecting traces and evaluation reports. A separate manager role and multi-user permissions are deferred.

### 2.2 Smallest useful end-to-end experience

One analyst reviews one synthetic loan package against one approved sample policy version, inspects evidence and policy outcomes, corrects a fact, sees affected results update, and exports a human-reviewed brief. The debt-investment view reuses the same facts and findings.

## 3. Core Metrics, Prioritisation & Roadmap

All targets below are proposed acceptance targets, not observed results. Baselines are unmeasured. Numerical targets require approval with this PRD and feasibility validation after the model and hardware are selected.

### 3.1 Success metrics and measurement

| ID | Metric and calculation | Proposed target | Measurement method |
| --- | --- | --- | --- |
| MET-01 | Review-time reduction: (manual median − assisted median) / manual median | At least 30% on comparable synthetic tasks | At least 6 paired tasks; counterbalance order and use matched cases to limit learning effects; time upload/read through reviewed brief, including corrections |
| MET-02 | End-to-end task completion: completed reviews / attempted valid supported reviews | At least 90% across at least 10 attempts | Scripted task records and observed usability sessions; disclose small sample |
| MET-03 | Critical-field accuracy: correct critical fields / all expected critical fields | At least 95% | Exact normalized match for amounts, units, currency, rate, dates, and agreed identity fields; correct missing status counts only when gold label is missing |
| MET-04 | Policy accuracy: correct rule outcomes / labeled outcomes | 100% for deterministic rule fixtures | Compare Pass, Fail, Unknown, and Not applicable against versioned gold labels, including threshold boundaries |
| MET-05 | Material-risk recall and precision | 100% recall for planted critical risks; at least 90% precision for labeled material findings | Match findings against predefined risk labels; blind rubric review for paraphrases; report false negatives and false positives |
| MET-06 | Evidence quality: supported material factual claims / all material factual claims | 100% citation coverage; at least 95% citation correctness; zero unsupported critical claims | Check that references exist and passages actually support the claims; calculations must link to source inputs and formula |
| MET-07 | Missing/conflicting input handling: correct uncertainty outcomes / labeled cases | 100% on critical missing/conflicting fixtures | Remove or contradict source facts and inspect status, explanation, and escalation |
| MET-08 | Correction integrity: correct refreshed dependent results / correction scenarios | 100%; zero stale final briefs | Change facts, documents, or policy; check invalidation, recalculation, preserved history, and new review acknowledgement |
| MET-09 | Automated processing latency | p95 at or below 120 seconds for the supported package | At least 30 runs on declared machine/model/config; include parsing, retries, and validation; exclude human waiting; publish failed/time-limited runs separately |
| MET-10 | Model usage and estimated cost | At most 20,000 input and 4,000 output tokens per new review; proposed USD 0.10 maximum estimated inference charge | Aggregate all agent calls/retries per review; use dated, approved provider rates; label estimates; local inference reports tokens and elapsed time, with hardware cost unmeasured |
| MET-11 | Avoidable repeat work | Identical finalized input served without new model calls; affected corrections do not trigger unrelated extraction | Instrument call counts, cache hits, and invalidated stages against scripted scenarios |
| MET-12 | Review control and data boundaries | Zero unauthorized finalizations, external actions, cross-deal disclosures, or unapproved network calls in the test suite | Permission, prompt-injection, isolation, and outbound-call checks |

### 3.2 Prioritisation and roadmap

P0: supported ingestion, cited extraction, sample-policy checks, financial calculations, risk brief, same-loan debt-investment view, reviewer corrections, orchestration/persistence, limits, and evaluation visibility.

P1 after MVP acceptance: richer cross-document reconciliation, document-version comparison, and policy-controlled what-if scenarios. These require a later approved scope change.

Deferred: separate equity/investment workflows, live market feeds, OCR, voice, external financial integrations, multi-tenant deployment, and advanced planning agents.

Roadmap follows approval gates: PRD → HLD and decisions → feature specifications and evaluation plan → repository design → execution/design plan → implementation, tests, and clickable HTML prototype. No calendar delivery commitment has been agreed.

## 4. MVP Features

### 4.1 Functional requirements and user acceptance

Every requirement below is part of the proposed PRD; approval of this draft establishes its implementation authority.

| ID | Priority | Requirement and user need | Acceptance criterion |
| --- | --- | --- | --- |
| FR-01 | P0 | Create a deal review with synthetic documents and a selected policy version | Accept supported files within limits; show names and versions; reject invalid inputs with a clear reason before model calls |
| FR-02 | P0 | Extract borrower, loan amount, currency, interest terms, maturity, repayment terms, collateral, guarantee, and covenants | Each present fact has a source reference; absent values remain missing; conflicting values remain unresolved until explicitly addressed |
| FR-03 | P0 | Extract borrower financials and calculate supported ratios | Show period, units, inputs, formula, and result; do not mix periods/currencies or divide by zero; missing inputs yield Unknown |
| FR-04 | P0 | Evaluate the approved sample policy | Show rule ID/version, applicability, inputs, evidence, outcome, and reason; no overall compliance certification |
| FR-05 | P0 | Flag supported credit risks and outstanding questions | Each material finding links to facts/calculations/policy and offers a reviewer action; no invented default probability or fabricated score |
| FR-06 | P0 | Summarize the same loan as a debt investment | Show contractual interest structure, maturity, security, covenant protections, and downside risks using the same dataset; do not equate interest rate with realized return |
| FR-07 | P0 | Navigate sources from extracted facts and findings | A click opens the correct document/page or text section and reveals the supporting passage; changed documents cannot silently reuse old references |
| FR-08 | P0 | Let the analyst correct facts and record dispositions | Preserve original value, new value, author label, reason, time, and evidence basis; invalidate affected results and any prior finalization |
| FR-09 | P0 | Require human acknowledgement before finalization | Block finalization on unresolved conflicting/invalid critical facts or unsupported critical claims; allow missing information or policy failures only with explicit acknowledgement and recorded review disposition; never convert acknowledgement into Pass |
| FR-10 | P0 | Coordinate named agents through inspectable structured handoffs | Display stage status and concise input/output summaries; validate payloads; enforce retries/limits; preserve state for pause/resume |
| FR-11 | P0 | Export the review brief locally | Include review status, policy version, source manifest, terms, ratios, risks, debt view, exceptions, and reviewer disposition; label all synthetic/demo content |
| FR-12 | P0 | Expose quality, usage, and workflow diagnostics | Show run ID, model/prompt/policy versions, time, token usage, estimated cost or unavailable status, and errors without exposing secrets |
| FR-13 | P0 | Keep stored review data isolated and removable | Resume the selected review without mixing another deal's state; delete associated documents, checkpoints, caches, and exports managed by the app under the approved retention policy |

### 4.2 Proposed synthetic document package

Use fictional entities and values, visibly labeled SYNTHETIC. No actual customer documents or real borrower identifiers are needed.

| Document | Information provided |
| --- | --- |
| Loan term sheet | Borrower, amount, currency, purpose, fixed/variable rate, maturity, repayment schedule, annual proposed debt service |
| Borrower financial summary | Annual revenue, EBITDA, total debt, operating cash available for debt service, existing debt service, period and currency |
| Collateral and covenant schedule | Declared eligible collateral value, valuation date, guarantee wording, proposed covenants, reporting obligations |
| Sample policy pack | Policy owner label, version, applicability, required fields, formulas, thresholds, severities, and escalation instructions |

Initial support proposed: text-based PDF and UTF-8 text; maximum 3 deal documents, 20 combined PDF pages or 40,000 combined extracted characters, and 10 MB combined upload size. Apply whichever limit is reached first. Separate approved policy content is not a user document that can redefine rules through prompt text.

### 4.3 Proposed sample policy v0.1 — approval required

These are fictional internal teaching rules, not regulatory requirements or industry-standard underwriting thresholds. Explicit comparison boundaries prevent later business-rule invention.

| ID | Proposed illustrative rule | Outcome semantics |
| --- | --- | --- |
| POL-01 | Loan principal must be greater than zero and no more than USD 750,000 | Boundary of 750,000 passes; non-USD is unsupported; missing/invalid value is Unknown |
| POL-02 | Maturity must be greater than zero and no more than 60 months | 60 passes; unsupported term units must be normalized with visible derivation or flagged |
| POL-03 | DSCR must be at least 1.25× | DSCR = annual operating cash available for debt service / (annual existing debt service + annual proposed loan debt service); all values use the same currency/annual period; zero/negative denominator is Unknown |
| POL-04 | Declared eligible collateral coverage must be at least 1.20× | Coverage = declared eligible collateral value / proposed principal; missing eligibility/value is Unknown; no assumption that declared value proves recoverability |
| POL-05 | A personal guarantee is required for all supported demo deals | Explicit adequate guarantee passes; explicit exclusion fails; absence or ambiguous language is Unknown |
| POL-06 | Total debt / annual EBITDA must be no more than 4.00× | Total debt includes the proposed loan after closing; nonpositive EBITDA yields Unknown plus a material financial-risk finding |
| POL-07 | Proposed covenants must require annual financial reporting and DSCR of at least 1.25× | Both must be explicit and sufficiently strict to pass; explicit weaker terms fail; missing/ambiguous clauses are Unknown |

Policy statuses: Pass, Fail, Unknown, Not applicable. Not applicable requires an explicit approved applicability rule, never missing evidence. All seven initial rules apply to supported deals. A policy failure is a review finding, not an automated rejection.

Annual proposed debt service is an evidenced input for this MVP. Do not infer amortization from rate and maturity alone. Unspecified fees, taxes, prepayments, loss rates, and recovery timing prevent net-return or expected-return calculations.

Example, not an evaluation result: USD 500,000 principal, USD 400,000 eligible collateral, USD 180,000 annual operating cash, USD 60,000 existing annual debt service, and USD 90,000 proposed annual debt service produce coverage of 0.80× and DSCR of 1.20×. Both fail the proposed policies. Missing guarantee text remains Unknown.

### 4.4 Explicit non-goals

- Autonomous loan approvals, investment execution, applicant communications, or adverse-action notices.
- Legal/regulatory compliance certification, KYC/AML/sanctions screening, fraud verification, bureau checks, or collateral appraisal.
- Equity valuation, securities selection, portfolio allocation, investment suitability, market forecasting, and personalized investment advice.
- Predictive credit scoring, default probability, expected-loss estimation, or model-generated ratings.
- OCR/scanned documents, spreadsheets, multi-currency conversion, live market data, and unsupported financial formulas.
- Real-time voice/ElevenLabs, broker integrations, cloud deployment, subscriptions, and production-readiness claims.

## 5. Constraints

### 5.1 Confirmed constraints

Local educational prototype; synthetic data; human financial decisions; no paid services, external actions, or deployment without explicit approval. Preferred stack: Python, LangChain agent/tool primitives, LangGraph stateful flows, Pydantic, and Jupyter learning notebooks. Token and cost optimization are explicit priorities. Explain decisions in plain language so the user can reproduce the work.

### 5.2 Proposed constraints and scope boundaries

One local operator, one active automated run, USD-only synthetic cases, annual financial periods, and bounded document sizes. No account system or multi-tenant authorization in MVP; bind local application access to the local machine. Do not present it as a secure shared financial service.

Deadline, hardware capacity, exact Python/package versions, model provider, real-data permissions, and monetary project budget are not yet agreed. These remain open; model-enabled execution is blocked until the execution mode and any costs are approved. Mock execution must be labeled simulation and cannot establish model-quality acceptance.

## 6. Technical Requirements

### 6.1 Requested technologies and proposed roles

This is a requirements-level direction, not the HLD. Exact components, dependencies, APIs, persistence adapter, UI framework, schemas, and repository layout will be approved in later phases.

| Technology | Purpose and qualification |
| --- | --- |
| Python | Core application and evaluation code; exact supported version deferred |
| LangChain | Model integration, bounded agent behavior, and allowlisted tools |
| LangGraph | Explicit multi-step state, conditional routing, checkpoint persistence, and human-review pauses |
| Pydantic | Validate structured agent handoffs and outputs; schema validity does not prove factual accuracy |
| Jupyter | Short guided learning notebooks that call shared application logic; avoid a duplicate notebook-only implementation |
| LangSmith | Candidate tracing/evaluation integration only; disabled by default; activation requires approval of external data transfer, retention, capabilities, limits, and cost |
| Model/provider | Undecided; compare compatible local inference with an explicitly approved hosted option during HLD |

Verified capabilities: LangGraph supports mixing deterministic and model-driven steps, persisted state, and human interruptions. LangChain supports structured output, including Pydantic schemas, subject to provider/model capabilities. Package compatibility, provider limits, hardware fit, and current prices must be checked before pinning dependencies.

### 6.2 Nonfunctional requirements

| ID | Requirement |
| --- | --- |
| NFR-01 | Reliability: persist stage completion; pause/resume and process restart must preserve a review; duplicate resumes must not duplicate finalization or unboundedly repeat model calls |
| NFR-02 | Performance and budgets: instrument MET-09/10; obey hard call/token/time ceilings even when quality targets are unmet |
| NFR-03 | Privacy: synthetic inputs only; no credentials, source documents, or raw financial text in ordinary analytics; external tracing off by default |
| NFR-04 | Reproducibility: record document hashes/versions, policy version, prompt/schema/model versions, and evaluation configuration; do not promise identical model outputs |
| NFR-05 | Usability/accessibility: keyboard-accessible controls, visible focus, text labels alongside color, readable errors, and distinct loading/empty/paused/failed/completed states |
| NFR-06 | Maintainability: small modules, bounded agent roles, shared logic between app/notebooks, and independent deterministic tests versus AI evaluations |
| NFR-07 | Security: validate file types/sizes; prevent path traversal; allowlist tools and outbound destinations; render document/model content as untrusted text |
| NFR-08 | Learning support: concise task explanations, a reproducible walkthrough, and visible evidence/calculations; no requirement to expose private model reasoning |
| NFR-09 | UI honesty: label synthetic data, mock outputs, estimates, and human review status; keep errors/partial results visibly distinct from completion |

### 6.3 Tool permissions

Agents may read documents for the current review, read the selected approved policy, invoke defined calculations, and submit structured findings. Only application-controlled operations may write checkpoints or a requested local export. The user interface controls corrections, deletion, and finalization.

No agent shell execution, arbitrary filesystem browsing, arbitrary web retrieval, email, payment, trading, account changes, or policy editing. Documents cannot grant permissions. No new paid service, account connection, repository publication, license selection, or external deployment without user approval.

### 6.4 Token, cost, and stopping requirements

Proposed starting limits per new review: 20,000 aggregate input tokens, 4,000 aggregate output tokens, at most 6 total model attempts including errors/retries, 12 total tool invocations, and 180 seconds automated wall time. Target normal completion remains p95 at or below 120 seconds. One model request has a proposed 45-second timeout; enforce the remaining run deadline. Human waiting is excluded from active time and incurs no background model activity.

At most one retry for a failed stage, only within the global limits. Do not retry unchanged valid outputs merely because a result is unfavorable. Cancel, budget exhaustion, repeated schema failure, unsupported critical evidence, or timeout stops automated work and preserves a clearly labeled partial/paused state.

Before a model call, reserve its token/output allowance and, where applicable, conservative estimated cost using approved rates. Do not dispatch if the worst-case reservation exceeds the remaining budget. Unknown price/usage must be marked unavailable; never display zero as a substitute. Hosted execution is disabled without approved pricing/configuration. Local inference still consumes hardware/time and is not claimed to be cost-free.

Cost optimization sequence: parse once → select relevant passages with original source IDs → extract typed facts once → calculate with code → pass concise facts/findings rather than entire documents → cache valid results by document/policy/prompt/model/schema versions → rerun affected stages only → measure quality before reducing model capacity. No stronger-model escalation or additional agent calls without an approved configuration and remaining budget.

Each resumed or corrected attempt has a visible linked run record; cumulative review usage remains visible and cannot be reset silently by resume. Reaching a cumulative approved budget requires an explicit user-authorized new allowance before further inference.

## 7. Grounding Strategy

### 7.1 Approved knowledge sources

Deal facts may come only from the current synthetic package or an explicit, attributed human correction. Rules may come only from the selected approved sample policy version. Calculated facts come from defined formulas and evidenced inputs. General model knowledge cannot supply missing borrower data, missing policy, market prices, or legal requirements.

Use direct evidence selection for the small supported packages. A vector database, embeddings service, external search, and general web browsing are not MVP requirements. If passage selection omits needed context, widen within limits or report Unknown; do not invent a supported answer.

### 7.2 Citation and navigation contract

Each factual output retains document ID/version, page or text-section locator, and source passage. PDF page references are 1-based; text files use stable section/line locators. A calculation references its formula and all input sources. A policy finding references both policy ID/version and underlying evidence. A summary retains finding references rather than citing another unsupported summary.

Validate reference existence separately from whether its passage supports the claim. Contradictory documents remain visible; no automatic latest-document precedence is assumed. Human corrections without document evidence are labeled reviewer-provided, with a reason, rather than given a fabricated citation.

### 7.3 Memory and retention

Required memory is deal-scoped workflow state: document references, normalized facts, findings, corrections, policy/configuration versions, stage status, and human review acknowledgements. It exists to resume work and preserve review history. No cross-borrower conversational memory, autonomous learning, or reuse of borrower facts in unrelated deals.

Proposed retention: store local synthetic review data for 30 days from last activity; purge expired data on application startup and before loading a review. No background purge service is required, so files can remain while the application is closed; disclose that limitation. Manual delete removes managed documents, state/checkpoints, caches, and managed exports immediately. User-copied exports and OS backups are outside application deletion control and must be disclosed. Keep only allowlisted, content-free operational metrics for the same 30-day window. No external retention applies while external services remain disabled.

## 8. Prompt Strategy

Use versioned, role-specific instructions and schema-constrained outputs. The feature-spec phase will define exact prompts, fields, examples, and tool contracts; this PRD sets behavioral requirements only.

| Role | Required behavior |
| --- | --- |
| Extraction agent | Extract facts and original units/periods; attach evidence; preserve missing and conflicting states; do not make an underwriting decision |
| Policy review agent | Map evidence to approved policy concepts and invoke deterministic checks; never invent rules or override calculated outcomes |
| Risk and summary agent | Explain supported material risks, unknowns, and next questions; generate loan and same-debt-investment sections from shared verified records |
| Orchestrator | Delegate within approved roles/tools, inspect handoff validity, select allowed next steps, stop at human checkpoints, and enforce global limits |

Recommendation: implement a deterministic evidence-validation step first. Add a separate evidence agent only if later evaluation demonstrates benefit within budget; it is not a mandatory fourth specialist model call.

Prompt inputs distinguish trusted instructions/policy from untrusted document content. Prompt outputs contain short evidence-based explanations and structured next actions, not private chain-of-thought. Learning material explains each step's purpose, inputs, outputs, and observable result.

## 9. Hallucination Guardrails

| ID | Required behavior |
| --- | --- |
| GR-01 | Missing or unsupported facts remain null/missing with a reason; never default to a favorable value |
| GR-02 | Conflicting material facts pause dependent checks and require an explicit reviewer resolution |
| GR-03 | Unsupported numerical scores, default probabilities, market claims, and legal conclusions are excluded |
| GR-04 | Document instructions to ignore policy, reveal secrets, invoke tools, or approve a deal are treated as untrusted content |
| GR-05 | Arithmetic and explicit thresholds are enforced by code; model wording cannot reverse them |
| GR-06 | Broken or nonsupporting critical citations block finalization; bounded repair or human correction is required |
| GR-07 | Out-of-scope requests receive a short explanation of supported scope; no invented analysis or unapproved tool action |
| GR-08 | A reviewer may acknowledge an exception but cannot silently change its policy outcome; all overrides retain a reason and history |
| GR-09 | Unknown applicability is not Not applicable; lack of guarantee text is not evidence of no guarantee |

Credit-risk severity is a proposed qualitative rubric: Critical = unusable or conflicting decision-critical evidence, or attempted unauthorized action; High = a known failure of DSCR, collateral, leverage, or required guarantee/covenants; Medium = an amount/maturity policy exception or required missing information; Informational = contextual observations. Missing decision-critical financial inputs still block their dependent calculations. Multiple findings may coexist. This is a review-priority rubric, not a calibrated credit rating. Approve or revise it before implementation.

## 10. Evaluation Strategy

### 10.1 Proposed evaluation dataset

Create 12 development cases and 12 held-out synthetic acceptance cases, with distinct borrower values and wording. Do not tune prompts on the acceptance set. Label expected facts, source spans, formulas, policy outcomes, material risks, escalation behavior, and allowed human actions before model runs. Each set includes:

1. Complete case passing sample policy.
2. Values exactly on thresholds and just outside them.
3. Missing guarantee/covenant clauses and missing financial inputs.
4. Conflicting principal or financial period across documents.
5. DSCR and collateral shortfalls.
6. Zero/negative EBITDA or invalid debt-service denominator.
7. Currency/period/unit mismatch and malformed values.
8. Document prompt injection and cross-deal data requests.
9. Out-of-scope equity/market/legal requests.
10. Fact correction that changes a downstream policy outcome.
11. Model/tool failure, timeout, budget stop, restart, and duplicate resume scenarios.
12. Stale policy/document version, broken citation, and finalization-control scenarios.

Some scenarios are direct workflow tests rather than document-only cases; the later evaluation plan will distinguish fixtures, interactive sequences, and model runs. Include paraphrased clauses, financial tables, and extraction difficulty without adding unsupported file formats.

### 10.2 Methods and acceptance

- Application tests establish arithmetic, policy boundaries, validation, permissions, persistence, invalidation, and budget behavior without depending on live model outputs.
- AI evaluations establish extraction, clause interpretation, evidence support, risk coverage, and summary quality using a declared real model configuration.
- Human review rubric scores completeness, evidence support, clarity, and actionable next questions from 0–2 each; proposed acceptance is at least 7/8 for every finalized acceptance brief, with no unsupported critical claim.
- Run each held-out AI case three times; report per-case results, worst run, aggregate denominators, variance, call counts, and actual configuration. Do not hide failed attempts or replace missing observations with demo values.
- Compare multi-agent results with a simple single-agent baseline on the same supported tasks and budgets. Report quality/cost trade-offs honestly; multi-agent complexity alone is not a success metric.
- Require all applicable MET targets plus the control tests before claiming prototype acceptance. Failure of a target leads to a documented fix, scope change, or explicitly approved threshold revision; never silently lower a gate.

### 10.3 Limitations

Synthetic data and small samples cannot establish real-world underwriting performance, fair-lending compliance, production robustness, or institutional acceptance. A single reviewer rubric has subjectivity; use a second reviewer when available and report disagreements. Repeated model runs are not independent borrower samples. Mock evaluations cannot prove AI quality. Time-saving results are exploratory until tested with representative analysts and authentic permitted workflows.

The detailed case definitions, runnable evaluation design, and requirement-to-test mapping belong in Phase 3, after PRD/HLD approval.

## 11. Production Readiness Criteria & Metrics (HHH)

Approved interpretation of HHH: Helpful, Honest, Harmless, accepted with the Phase 1 baseline on 2026-10-22.

| Dimension | Prototype evidence required |
| --- | --- |
| Helpful | MET-01/02 task/time evidence, accepted user flow, and completed review/export walkthrough |
| Honest | MET-03 through MET-08, citations/unknowns preserved, estimates/mock content labeled, and no fabricated observed results |
| Harmless | MET-12 permission/data tests, injection handling, human review controls, no autonomous financial/external actions |

These are educational prototype acceptance criteria, not production certification. A future production release needs an independently approved readiness scope covering real-data permissions and retention, identity/access management, jurisdiction-specific compliance ownership, representative validation and bias assessment, security review, recovery testing, operational ownership, and approved financial-decision boundaries. No such checks have been completed.

Observed evidence at the Phase 1 gate (2026-10-21): the workspace was inspected and contained no existing application or Git repository; this PRD was the only project artifact. No code, tests, evaluations, latency measurements, provider charges, or deployment results existed.

## 12. Pricing

No customer pricing or monetization is approved for this educational project. No license will be selected, account connected, paid service enabled, or repository published during this phase.

Proposed operational objective: local execution without mandatory paid services. A hosted model or hosted tracing option requires explicit approval; framework installation does not include model inference or hosted-service usage. Exact current provider costs, pricing units, retention, limits, and free-tier eligibility must be verified after a provider is proposed.

The proposed USD 0.10 per-review inference ceiling is an unvalidated budget target, not a quoted price or expected result. Monthly model cost, if approved, would be estimated from measured token use × dated input/output rates, aggregated across every attempt. Compute, storage, tracing, and operator time must be reported separately where measured; do not present omitted costs as zero.

Potential future business validation: measured analyst hours saved = reviews per month × measured minutes saved / 60. Compare that benefit with operating and policy-maintenance costs before proposing subscriptions or per-review pricing. No demand, ROI, or willingness-to-pay claim has been established.

## 13. Assumptions

### 13.1 Confirmed requirements and decisions

| ID | Confirmed item |
| --- | --- |
| C-01 | Primary user is a credit analyst reviewing small-business loans |
| C-02 | Investment review covers the same loan as a debt investment; user explicitly selected this boundary |
| C-03 | Cover financials, loan terms, sample lending policies, collateral, covenants, and credit risk |
| C-04 | Define synthetic loan documents and sample policy content for approval |
| C-05 | Local educational prototype, synthetic data, human decisions, no paid services/external actions/deployment without approval |
| C-06 | Python, LangChain/LangGraph agent/tool primitives and stateful flows, Pydantic, Jupyter; consider LangSmith without enabling it |
| C-07 | Optimize tokens/cost and explain steps simply so the user can reproduce the project |
| C-08 | Work phase by phase; approved documents control implementation; request approval at each gate |

### 13.2 Proposed assumptions and recommendations requiring PRD approval

| ID | Proposed choice | Reason |
| --- | --- | --- |
| A-01 | DealLens working name | Provides a consistent name without committing branding |
| A-02 | One local operator, one active run, USD and annual periods, defined small document limits | Keeps the MVP feasible and measurable |
| A-03 | Text PDF/text input and local export; no OCR/spreadsheets | Controls ingestion complexity |
| A-04 | Sample policies POL-01–07 and qualitative severity rubric | Makes the demo explicit and independently testable |
| A-05 | Proposed metric targets, dataset sizes, retry/time/token/tool ceilings, and conditional USD budget | Creates reviewable targets before implementation |
| A-06 | Thirty-day local retention and startup/access expiry checks | Bounds memory without a background service; limitations are disclosed |
| A-07 | Deterministic evidence checks before adding another model agent; compact handoffs and selective reruns | Limits redundant inference |
| A-08 | HHH means Helpful, Honest, Harmless | Supplies a proposed meaning for the requested section |

### 13.3 Dependencies and risks

| Item | Risk or dependency | Planned response |
| --- | --- | --- |
| Model choice/hardware | Local models may not meet quality/latency targets; hosted models may require paid approval | Benchmark compatible choices after HLD approval; disclose trade-offs rather than promise feasibility |
| Policy approval | Fictional thresholds might be mistaken for authoritative requirements | Keep sample labeling visible; no rule implemented before approval |
| Document complexity | Tables, ambiguous units, and varied clauses can break extraction | Evaluate difficult supported examples; retain Unknown and human correction paths |
| Agent coordination | Extra calls can increase cost or propagate errors | Validate handoffs, limit loops, preserve source references, compare baseline |
| Framework compatibility | Package/provider capabilities can change | Verify official documentation and pin compatible versions during implementation planning |
| Financial interpretation | Debt investment view could be mistaken for return prediction or advice | Restrict it to contractual terms, protections, risks, and explicitly unknown quantities |
| Synthetic evaluation | High scores may not transfer to real underwriting | Limit claims and require a separate readiness process for real deployment |

### 13.4 Open questions

1. What deadline and available machine/OS resources should shape the HLD? Workspace OS is Windows; CPU/RAM/GPU availability is not yet established.
2. Is the user comfortable with Python/virtual environments, or should the later walkthrough assume beginner-level setup?
3. Which execution mode should be evaluated: an existing local model, a new local model requiring download approval as applicable, or a separately approved hosted provider? No provider is selected.
4. Are all proposed policies, metric thresholds, severity labels, retention boundaries, and budgets acceptable?
5. Does the proposed HHH interpretation match the intended rubric?

Questions 1–3 remain open for HLD investigation without allowing paid execution. Questions 4–5 were resolved by the Phase 1 approval on 2026-10-22; subsequent changes require an explicit baseline revision.

### 13.5 Source notes and verification

Official documentation checked on 2026-10-21. These sources support framework capability statements only; they do not approve an architecture, establish model quality, or set financial policy.

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): deterministic/model-driven orchestration and stateful workflows.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpoint-scoped state and persistence options.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): pause/resume for external human input.
- [LangChain structured output](https://docs.langchain.com/oss/python/langchain/structured-output): structured response schemas, subject to strategy/provider support.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/): typed output validation; not proof of factual correctness.
- [LangSmith observability](https://docs.langchain.com/langsmith/observability): optional tracing capability; pricing/limits/data retention are not approved or verified here.

### 13.6 Phase 1 gate

Created at the Phase 1 gate: `docs/product/prd.md` only. No architecture, feature specs, execution plan, repository scaffolding, code, tests, notebooks, HTML, Git initialization, external repository, deployment, or paid service activation occurred in Phase 1.

Gate outcome: approved on 2026-10-22. Phase 2 may create `docs/architecture/hld.md` and justified architecture decisions. It may not implement the application. The next approval gate is the HLD and major technology choices.
