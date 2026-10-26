# ADR-002: Source evidence, sample rules, and one SQLite boundary

**Current embedding decision — 2026-10-23:** [ADR-008](008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.10  
Status: Accepted educational architecture baseline through Phase 3; dependency verification and implementation pending  
Date: 2026-10-23  
Reference requirements: FR-002–007/009–010  
Context: [Current HLD](../hld.md), [Current PRD](../../product/prd.md)

Scope: Working local educational demo required; Nebius access will be supplied later. Preserve phase gates before implementation. No operational banking use, real borrower data, or deployment is included.

## Context

The prototype must support source-linked synthetic examples, deterministic arithmetic, corrections, and simulated review. Real borrower records are excluded.

## Accepted architecture direction

Later accepted [ADR-007](007-proposed-public-financial-rag.md) extends this boundary with dated public-source observations, citation-bearing parent/child passages, Nebius-hosted embeddings under ADR-008 and app-owned SQLite vectors/build records. Use bounded exact cosine search after source/corpus/date eligibility, not a second database or automatic policy source. Source and architecture approval are resolved; schema changes/setup/tests remain pending. An additive versioned schema change must preserve existing records/checkpoints/history, and incomplete/mismatched builds cannot become active. Public-reference corpus data is separate from synthetic case fixtures and loan support.

Use page-aware source references, explicit formulas, versioned fictional policies, and separate extracted facts, reviewer corrections, calculations, policy outcomes, risk inferences, and evidence status. Undefined inputs/formulas remain Unknown. The accepted [Financial Analyst contract](../../agents/financial-analyst.md) defines FIN-1.0 arithmetic and [Compliance](../../agents/compliance.md) defines SAMPLE-LOAN-POLICY-1.0; retired SYN-ESC-003 must not execute. Intake uses three text PDFs, ten total pages, and 10 MB combined, as specified in [Document Intake](../../agents/document-intake.md).

Parser choice superseded by [ADR-006](006-proposed-pdf-parser.md): user approved pypdf installation/known-corpus verification; PyMuPDF is not selected. Use one SQLite database with distinct application/checkpointer ownership. Specify operation IDs, revisions, interruption/restart, and affected-stage invalidation before implementation. Both fixture and live modes follow the same provenance rules.

The Report Generator reads recorded audit events, not an assumed complete trace. Its state update is checkpointed after the node returns. MemorySaver/InMemorySaver is an optional in-process notebook/test saver; its RAM-backed history is lost on restart. Keep SQLite for persistent app state. Neither backend guarantees immutable audit storage; inspection and executing replay/resume are separate operations. See [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).

Persist validated PanelDecision and synthesis mode/revision/evidence metadata separately from workflow gates, effective escalation, and reviewer disposition. The deterministic report copies accepted recommendations/conditions with a simulation label; corrections invalidate stale decisions and reports.

The new conditional review uses same-thread interrupt/resume. In-memory MemorySaver is a session-only classroom profile; SQLite remains the persistent local-app profile. Serialize defined graph state and record review/tool events explicitly. Generate the final report after valid resume or the no-review branch; its own checkpoint follows generation, not precedes it.

Core-agent handoff records must include sender/recipient, deal/run/revision/task identity, schema and artifact references, and validation/outcome. Link at least one generated sample report to its executed run. Multi-deal fixture evaluation must keep state/outputs separate and retain honest checkpoint/audit limits.

## Trade-offs and validation

A separate vector database/service adds no demonstrated benefit for the small loan package. The accepted public-reference extension uses SQLite-backed vector rows and exact local search; no measured retrieval benefit or ANN capability is claimed. Reference existence does not establish semantic support; include human inspection and later model-backed checks.

Confirmed P3-04: no automatic expiry in the MVP prototype. Persisted synthetic documents, deal records, reports, review history and SQLite checkpoints have no age-based deletion/pruning. A manual deletion/reset needs an explicit user request and reviewed consistent targets; attachments/archives are not implicit cleanup targets. Test citation resolution, arithmetic boundaries, incompatible periods, stale results, time advancement and restart persistence. MemorySaver remains RAM-only. No parser, database, migration or cleanup job has been created.

Approval clarification: the user accepted the architecture/specification direction through Phase3; the subsequent issue-fix request authorizes documentary corrections. This does not select a project/parser license, validate dependencies, approve new R4-01–08 choices or authorize paid execution. [Current scope/contracts](../../specs/overview.md) govern the five-day core.

Analytical corrections use a new revision/run/thread with the original review budget; only review-only handling uses same-thread resume. Old pending requests become stale. [SPEC-007 transition table](../../specs/orchestration-budgets.md) defines the exact entry/reuse rules.
