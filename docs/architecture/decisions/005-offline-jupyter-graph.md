# ADR-005: Runnable offline visualization of the shared graph

Version: 1.8  
Status: Accepted educational architecture baseline through Phase 3; dependency verification and implementation pending  
Date: 2026-10-22  
Reference requirements: FR-008/011/013; F-017  
Context: [Current HLD](../hld.md), [Current PRD](../../product/prd.md)

Scope: Working local educational demo required; Nebius access will be supplied later. Preserve phase gates before implementation. No operational banking use, real borrower data, or deployment is included.

## Context

The user requested Jupyter to show the graph and clarified that a working educational demo is required. Restore an executable shared-graph notebook as a required deliverable after the implementation gates.

## Accepted architecture direction

Separate graph construction from inference. The notebook imports the application's graph factory/metadata, renders its real nodes/edges locally, and explains orchestrator coordination, seven specialists, conditional routes, and human-review pauses.

Show the deterministic Report Generator under Memo, direct Python Risk Quantifier, and one explicit Synthesizer task reading the three panel outputs. Show all seven responsibilities while keeping only Extraction and Synthesizer model-backed. Label the two normal model calls; do not imply each specialist invokes a model. An optional MemorySaver/InMemorySaver checkpoint walkthrough must disclose session-only RAM retention and distinguish reading saved state from executing replay; it cannot claim an immutable or automatically complete audit trail.

Distinguish deterministic/model-backed work and possible routes versus completed runs. Proposed NetworkX/Matplotlib rendering remains subject to dependency compatibility review. Graph-only cells need no Nebius key, model request, paid service, remote renderer, or mutable application state.

Show the amount/confidence conditional edge, mandatory-referral aggregation, interrupt/resume review branch, direct no-review branch, and merge into the deterministic final Report Generator. Do not depict skipped review as human approval. MemorySaver-based session history and SQLite restart behavior are distinct teaching examples.

Label the three core agents plus Orchestrator and the seven responsibility nodes. Show Agent 3's Risk Quantifier/Synthesizer composition. Diagrammed delegation is not execution evidence; pair the later notebook presentation with real run/handoff records and a generated sample report.

## Trade-offs and validation

A shared graph reduces diagram drift; an independent notebook pipeline would duplicate logic. Keep any optional fixture execution walkthrough separate and mode-labeled.

Verify fresh-kernel execution without credentials, graph/diagram consistency, readable labels, zero provider/remote-renderer calls, and no app-state modification. No notebook, renderer, dependency, or execution result is created by this edit.

Approval clarification: the user accepted the architecture/specification direction through Phase3; the subsequent issue-fix request authorizes documentary corrections. This does not select a project/parser license, validate dependencies, approve new R4-01–08 choices or authorize paid execution. [Current scope/contracts](../../specs/overview.md) govern the five-day core.
