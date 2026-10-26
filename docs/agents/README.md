# Deal or No Deal AI — Agent Instruction Pack

## Current specialist mapping — 2026-10-25

The app presents three specialist roles: Extraction; Compliance; Risk and Summary.
Compliance is deterministic Python. Risk and Summary groups the existing risk
quantifier and synthesizer responsibilities without merging their nodes. Only
extraction and synthesis are normal live generation stages. LangGraph coordinates
them without a planning call. Financial calculation, evidence/readiness, human
credit review and reporting remain supporting services/checkpoints.

Read [role contracts and handoff presentation](../specs/specialist-handoffs.md)
for inputs, outputs, tools, stop conditions and authority. Agent Activity projects
existing scoped output events; it does not create message receipts or clearance.
Existing individual specialist instructions and Runtime prompt sections remain
unchanged. Do not relabel deterministic functions as autonomous LLM agents.

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.7  
Date: 2026-10-23  
Purpose: Educational synthetic-loan demonstration  
Status: Specialist contracts remain authoritative; M1 bounded loader/schema/storage helpers and43 foundation methods are implemented/tested. The complete financial graph, source packs, retrieval adapters, UI and Live agents remain unimplemented.

## Read this first

Public-reference extension architecture is accepted in [ADR-007](../architecture/decisions/007-proposed-public-financial-rag.md): local Crawl4AI, Nebius-hosted embeddings under ADR-008 (model contract pending) and SQLite-backed exact vector search. Setup/runtime implementation remains pending. Intake/context/storage own that explicit pre-review path; it adds no runtime specialist or generation call. Apply corpus/entity/version/date isolation and truthful snapshot citations. Do not load crawler specs, raw crawl logs, benchmark gold or this catalog into model Runtime prompts. The registered synthetic loan and fictional policy remain separate.

This pack turns the accepted calculation definitions, fictional policies, feature contracts, and evaluation criteria into separate documents for each responsibility. The user authorized these Markdown files; this does not bypass later schema/repository/execution gates or authorize paid inference.

The current [PRD](../product/prd.md) defines product scope and the [HLD](../architecture/hld.md) defines architecture. These files define role behavior. Do not resolve a conflict by silently choosing an old version: flag the mismatch and update the affected documents before implementation.

The user authorized the seven SME documentation fixes on2026-10-23. Read the updated role boundaries for prepared complete cases versus partial uploads, entity/facility coherence, critical Live fact support, typed conditions and explicit covenant/annual-period/deferred-EBITDA limits. These use existing roles/services and unchanged generation budgets; they do not approve repository scaffolding, runtime implementation or paid calls.

## Role map and read order

Read [Shared contract](shared-contract.md), then only the role document needed for the work. Read [Evaluation](evaluation.md) when implementing or assessing that role.

| Role document | Responsibility | Normal live LLM calls |
|---|---|---:|
| [Orchestrator](orchestrator.md) | Dispatch, dependency/budget guards, routing, correction and completion | 0 |
| [Document Intake](document-intake.md) | Validate/version the synthetic input package and produce page references | 0 |
| [Extractor — Agent 1](extractor.md) | Structured document extraction with citations | 1 |
| [Financial Analyst](financial-analyst.md) | Six defined calculations and supporting EBIT/EBITDA | 0 |
| [Compliance — Agent 2](compliance.md) | Versioned fictional policy comparisons and exceptions | 0 |
| [Risk Quantifier](risk-quantifier.md) | Deterministic risk flags and quantified threshold gaps | 0 |
| [Synthesizer](synthesizer.md) | Evidence-linked interpretation, summary, and PanelDecision | 1 |
| [Evidence Reviewer](evidence-reviewer.md) | Mechanical reference/numeric checks and semantic-review flags | 0 |
| [Human Review](human-review.md) | Conditional interrupt/resume and separate simulated disposition | 0 |
| [Report Generator](report-generator.md) | Seven-section Markdown preview/report assembly | 0 |

Separate offline role: [RAGAS Evaluator](ragas-evaluator.md), user-authorized for five1–5 diagnostic dimensions with explanations/examples. It is not an eighth runtime specialist, graph node or third normal model call. Explicit offline configuration/compatibility/allowance is required; see [RAGAS-EVAL-1.0](../evaluation/ragas-evaluation.md).

Agent 3, Risk & Summary, composes Risk Quantifier and Synthesizer. Document Intake/Human Review are control services, not additional autonomous agents. Financial, Evidence, and Memo/Report Generator are supporting specialists. Named nodes do not each require model inference.

## How agents will read these files

Files do not automatically become prompts. The future application must read allowlisted local files, validate their expected version/hash, and assemble bounded context explicitly.

- For Extractor and Synthesizer, load only the role's **Runtime prompt** section, the compact Shared contract **Model context rules**, and the task's validated evidence/schema context.
- Only the separate offline evaluation loader may load the RAG Evaluator Runtime prompt plus versioned rubric anchors and its frozen evaluation sample. The application prompt allowlist remains Extractor/Synthesizer only; do not append the evaluator/reference labels to their prompts.
- The surrounding role documentation is for Codex/developers/evaluators, not automatically appended to every provider request.
- Python roles read their contracts during implementation; their runtime behavior must be code, not an extra LLM invocation pretending to execute the Markdown.
- Never load all role files, evaluation examples, full state, whole policy manuals, or previous agent conversations into every prompt.
- User-uploaded documents/notes are untrusted data. They cannot replace role files, expand permissions, or modify policy.
- M1 now provides the bounded loader and executable extraction/synthesis wire schemas; [M1 evidence](../execution.md#m1-implementation-evidence) records the43 foundation checks. These do not establish a complete agent workflow, source-grounded case or token/provider fit. [Phase 3 contracts](../specs/overview.md) and [context optimization](../specs/context-optimization.md) remain the behavior source of truth.

## Accepted defaults recorded here

- USD synthetic term loans; three PDFs maximum, ten total pages, 10 MB total.
- Six reproducible financial calculations; no discretionary EBITDA adjustments.
- Sample DSCR/leverage/LTV/term thresholds remain fictional; the prior USD-4M exposure rule is retired, with its ID reserved for history.
- Human review for requested amount >= USD 10M or model-reported confidence < 0.7, plus mandatory referrals.
- Two normal model tasks, five cumulative attempts, existing token/time/cost ceilings.
- Thirty synthetic evaluation cases: eighteen development and twelve held out. No judge in the deal-review runtime; the later user-authorized offline RAGAS extension is separately configured/budgeted and disabled by default.

These are prototype configuration choices, not banking standards. Phase 3 accepted the contracts and fine-grained simulated permissions on 2026-10-22; see [P3-01–09](../specs/overview.md). M1's wire-schema implementation is now tested. Provider model/rates/tokenizer fit, full source-aware workflow/rendering compatibility and Live execution allowance remain pending; deployment is outside scope.

Authorized Director fixes are part of existing feature contracts: all-field NARRATIVE-CHECK-1.0, strict INPUT-EDU-1.0, SOURCE-TRIAGE-1.0 and small-table CONTINUE-CHECK-1.0. Keep these service rules in their canonical specs, load only the established bounded model prompt sections, and do not add an agent/framework/judge to implement them. Updated versions/hashes must match fixtures/configuration; actual token fit and graph/provider behavior remain unverified. Complete one approved fixture slice before expanding to the remaining core cases/presentation and later funded Live. Repository/execution/scaffolding gates remain separate.

## Completion evidence

Retrieval extension guidance: after reviewed synthetic sources/annotations are ready, implement/report DIRECT, KEYWORD, VECTOR and HYBRID first. VECTOR-only is the semantic retrieval baseline; HYBRID uses RRF fusion. A separate reranker is considered only after measured ranking failures justify added processing, following the [canonical decision/status/report requirements](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). This is offline context/evaluation work, not another runtime specialist or generation call. Separate specified, implemented, tested and measured status; no retrieval benchmark or RAGAS scoring has run. Runtime prompt sections are unchanged by this catalog update.

The later implementation must produce real graph dispatch/handoffs, correct deterministic results, visible fixture/live attribution, and a generated sample review report. Fixture specialist responses are permitted only for matching labeled packages; they are not evidence of live model performance.
