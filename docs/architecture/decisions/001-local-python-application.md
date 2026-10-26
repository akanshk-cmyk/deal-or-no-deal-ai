# ADR-001: One local Python application with shared orchestration

**Current embedding decision — 2026-10-23:** [ADR-008](008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.9  
Status: Accepted educational architecture baseline through Phase 3; dependency verification and implementation pending  
Date: 2026-10-23  
Reference requirements: FR-001–019  
Context: [Current HLD](../hld.md), [Current PRD](../../product/prd.md)

Scope: Working local educational demo required; Nebius access will be supplied later. Preserve phase gates before implementation. No operational banking use, real borrower data, or deployment is included.

## Context

A working local demo is required for education. The user will supply Nebius access later. Keep the five-day scope small and preserve all document/repository/execution approval gates before code.

## Accepted architecture direction

Later accepted [ADR-007](007-proposed-public-financial-rag.md) adds optional Crawl4AI reference ingestion/retrieval, with Nebius-hosted embeddings replacing local BGE under ADR-008 as explicitly invoked shared Python services, with app-owned vector records in the same SQLite boundary. It adds no runtime generation agent, API server, broker or second framework. Source/architecture selection is approved; actual setup, code and tests for that extension remain pending. Synthetic loan graph and public-reference task scopes remain separate.

Use Streamlit, a reusable Python service layer, one LangGraph definition, and typed Pydantic handoffs. Implement seven specialist responsibilities, but do not require seven model calls. Financial and structured Policy work use deterministic tools; Evidence uses reference/numeric checks; Memo owns a pure-Python Report Generator with no LLM calls. It writes the seven-section Markdown report and metadata to state from validated upstream results and explicit audit events.

Provide injected fixture and Nebius adapters for model-backed stages. Both modes execute the graph and deterministic logic; fixture outputs are clearly labeled. The Jupyter notebook imports the same graph. The lightweight HTML artifact is a visual presentation, not a duplicate pipeline.

The user accepted two normal live model calls: Extraction and an explicit Synthesizer reading Compliance, Financial, and Risk panels. Execute configured risk functions directly in Python instead of a ReAct loop. No separate Financial/Policy interpretation call, judge call, or planning-model call is included; policy ambiguity requires clarification. Preserve the seven specialist responsibilities.

Risk is now pure-Python quantification. Synthesizer is a distinct seventh specialist responsibility using the already-budgeted second model call. It returns the five-field PanelDecision from PRD FR-017 and supported narrative in one response. Mandatory gates and separate simulated human disposition remain authoritative for workflow progression.

Compute the new requested-loan-USD-10M OR confidence-below-0.7 trigger in Python and combine it with existing mandatory referrals. Route to interrupt-based review only when required; merge validated resume and no-review branches into Report Generator. Two normal live calls remain unchanged.

The user's primary deliverable is a working 3+ specialist-agent pipeline with orchestration and sample review output. Map core contracts to Extractor, Compliance, and Risk & Summary; Agent 3 composes Risk Quantifier plus the explicit Synthesizer. Financial, Evidence, and Memo/Report Generator support them. Keep all seven responsibilities inspectable and disclose deterministic versus model-backed execution.

Verify actual dispatch/receipt handoffs and generated output, not just a visual timeline. Demonstrate bounded independent fixture runs under the existing active-review ceiling; workload/throughput criteria remain for the evaluation plan. Local tests cannot establish distributed scale.

## Trade-offs and validation

Avoid a separate API, queue, GPU service, or second orchestration framework. A local single-process demo does not establish large-scale reliability.

Later tests must verify actual handoffs, conditional routes, stopping limits, duplicate-action handling, correction invalidation, and shared graph use. Fixture success cannot establish model quality. No code or runtime evidence exists yet.

Approval clarification: the user accepted the architecture/specification direction through Phase3; the subsequent issue-fix request authorizes documentary corrections. This does not select a project/parser license, validate dependencies, approve new R4-01–08 choices or authorize paid execution. [Current scope/contracts](../../specs/overview.md) govern the five-day core.
