# Specialist roles and visible handoffs

Authorized 2026-10-25: make delegation, coordination and communication visible
using existing components. This is a hybrid specialist workflow, not three
autonomous LLM agents. Implements presentation for the existing orchestration,
traceability and explanation requirements; does not replace approved agent specs.

## Role contracts

| Role | Inputs | Permitted implementation/tools | Output | Stop/authority boundary |
| --- | --- | --- | --- | --- |
| Extraction Specialist | Current registered source package | Existing extraction model stage in live execution; preserved responses/source correction in saved workflows | Structured terms/financial facts, basis, references and original output | Schema/source failure stops admission; human fact support required in live flow; no credit authority |
| Compliance Specialist | Supported facts and financial panel | Existing deterministic policy evaluator | Rule results, exceptions, reasons, source/policy references and workflow requirements | Missing/unevaluated is not Pass; no exception waiver or invented policy; no LLM call |
| Risk and Summary Specialist | Financial and compliance panels, authored educational scoring premises and permitted evidence | Existing Python risk quantifier plus existing synthesis model stage | Illustrative factor scores, observations, rationale and original AI proposal | No complete score with material missing factors; no predictive PD claim; no approval authority; synthesis and scoring remain separate nodes |
| Orchestrator | Validated stage outputs, state, receipts and limits | Existing LangGraph/worker coordination | Existing routing, checkpoints, requests and recorded execution status | No planning LLM call; no silent fallback, human-support bypass or uncertain-call replay |

Financial calculation, evidence review, readiness and pure-Python reporting remain
supporting services. This grouping adds no agent framework, prompt, model call,
schema migration, tool permission, threshold or business rule.

## Handoff view

Agent Activity shows the three specialists and a dependency table:

1. Extraction to Financial Calculation Service.
2. Financial Calculation Service to Compliance.
3. Financial Calculation Service and Compliance to risk scoring.
4. Financial, Compliance and Risk outputs to Synthesis.
5. Synthesis plus evidence checks to readiness routing.

The table projects the selected scoped review only. It matches artifacts to
existing output events by current run ID, stage and artifact digest. Completion,
reuse and source-correction events are distinguished in technical references.
Upstream records must precede the destination output event for a downstream
result to be shown. Absent/mismatched output events remain unconfirmed; stage
start events never count as output. Missing timestamps remain Not captured.

Rows show sender, recipient, shared result, review version and recorded progress.
Technical details preserve the original event sequence, digest and timestamp.
They do not claim to be new message receipts, independent proof of semantic input
consumption, human evidence verification or loan approval. No event is persisted
or backfilled by this view. Existing backend handoff validation remains authoritative.

Live fact/narrative pauses and missing-data/recovery states show their required
next action. Completed review is never described as approved credit.

## Validation and delivery boundaries

Test complete and partial saved workflows, missing-information and paused live
records, existing event references, incorrect run/digest, absence of an output
event, sequencing, and unchanged input records. Verify UI navigation makes no
provider call or database change. Preserve existing graph, fixtures, sources,
financial metrics, synthetic policies, score calculations and cumulative limits.

No parallel execution or scale claim is introduced. A batch/load benchmark and
third LLM agent are optional future work requiring a distinct requirement and
specification. Real live completion remains blocked by deferred provider-usage
reconciliation and required human reviews; this UI work does not clear them.

## Observed implementation checks

Four focused projection tests passed: read-only complete dependencies, wrong-run /
wrong-digest / start-only / reversed events, live fact pause, missing information
and technical recovery. Seventeen existing command-center and live evidence UI
checks also passed (208.95 seconds). These verify presentation compatibility,
not a new live journey or scale benchmark. No paid call or personal audit record
was created by these offline checks. Runtime prompts and financial rules were
not modified.
