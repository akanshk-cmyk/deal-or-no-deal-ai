# ADR-003: Fixture-first development and later bounded Nebius integration

User-authorized2026-10-23 [GEN-COMPARE-1.0](../../evaluation/generation-model-comparison.md) prepares a same-input Qwen/Nemotron-3-Nano comparison. It changes no application model, generation stage or budget. Offline preparation has no provider adapter/credentials; live comparison remains gated by verified model/request/token/reasoning behavior and a separate concrete allowance. Dated list-rate estimates and harness tests are not measured review savings or a model winner.

Version: 1.10  
Status: Accepted educational architecture baseline through Phase 3; dependency verification and implementation pending  
Date: 2026-10-22  
Reference requirements: FR-008/011–012/015; PRD section 12  
Context: [Current HLD](../hld.md), [Current PRD](../../product/prd.md)

Scope: Working local educational demo required; Nebius access will be supplied later. Preserve phase gates before implementation. No operational banking use, real borrower data, or deployment is included.

## Context

The user confirmed a working demo and will provide Nebius API access later. API availability must not block synthetic fixture development. Live integration is a later required demo milestone.

## Accepted architecture direction

Implement clearly labeled fixture and live adapters behind shared contracts. Fixture mode executes the graph and deterministic tools without inference. It must not be presented as model output. Missing access disables Live mode; failed live requests do not silently fall back to fixtures or another provider.

Accepted allocation: two normal successful live calls, Extraction and explicit Synthesizer. The Synthesizer joins all three deterministic panels and returns PanelDecision plus supported narrative in the existing one-call envelope. Fixture mode has none. Risk quantification and rule checks are direct Python. Count any schema/provider repair, SDK retry, correction, or resumed work as additional attempts, within all cumulative limits. A review-only resume or report rerender must reuse completed model outputs.

Keep the proposed live envelope: USD 0.10 target/USD 0.25 ceiling; 8,000 input/2,000 output tokens; five total model attempts; twelve tools; twenty node invocations; one transient retry per operation; 180 active seconds and at most 45 seconds per model call. Finalize cumulative reservation/accounting before implementation. These values are unmeasured, not provider quotas or spending permission.

Store the later key in local secret/environment configuration, excluded from version control, UI, notebook outputs, state, and traces. Select the model, verify rates/capabilities, and agree an execution allowance before live validation.

Memo's Report Generator is a pure-Python node with zero provider calls/tokens in fixture and live modes. Model work stays upstream. Report replay/rerender remains inside node/runtime limits; executing a graph resume may trigger upstream model work and must honor the same cumulative allowance.

Amount/confidence routing, human wait/resume, condition editing, and report generation add zero model calls. Count active execution separately from human waiting. A valid no-review branch preserves the two-call normal budget. Material factual corrections may consume further attempts within existing ceilings.

Mapping the three core agents to seven supporting responsibility nodes adds no normal model calls. Count nested/composite execution and all provider/tool attempts within existing budgets. Proposed multi-deal evaluation is fixture-only until a separate live-batch allowance exists; no large-scale performance claim follows from the diagram.

The [specialist instruction pack](../../agents/README.md) separates the two application Runtime prompts from Python contracts. The application loader includes only the needed role section, shared Model context rules and task evidence, recording version/hash. No automatic whole-pack prompt or additional planning/judge call is allowed in the deal graph. Deterministic checks/human scoring remain core acceptance. The user's2026-10-23 [RAGAS-EVAL-1.0](../../evaluation/ragas-evaluation.md) request explicitly supersedes blanket no-judge wording for separately invoked offline evaluation only: lazy optional RAGAS dependency, separate allowlisted evaluator prompt, frozen samples, five custom1–5 dimensions with examples and separate optional native metrics. Use one shared routine judging bundle plus local metric projections after compatibility proof; count every real request under an explicitly approved evaluation allowance. No default provider, automatic scoring, deal-state mutation or third normal application call. Library/model/rates/token accounting and paid execution remain unverified/unapproved.

## Trade-offs and validation

Local content-free diagnostics are sufficient; LangSmith remains optional and inactive. Report fixture/live timing and estimated/measured usage separately. Do not claim p95 latency or model quality from a single run.

Verify no outbound inference in fixture or graph-only mode, no automatic refresh calls, visible live failures, bounded retry/cost accounting, and later validated synthetic live execution. No provider request, key file, tracing connection, or evaluation has been performed.

Approval clarification: the user accepted the architecture/specification direction through Phase3; the subsequent issue-fix request authorizes documentary corrections. This does not select a project/parser license, validate dependencies, approve new R4-01–08 choices or authorize paid execution. [Current scope/contracts](../../specs/overview.md) govern the five-day core.
