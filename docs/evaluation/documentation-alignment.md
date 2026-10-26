# Documentation alignment review — 2026-10-25

Scope: README, active AGENTS instructions, PRD, HLD, feature specifications,
design/repository guidance, agent instruction pack, evaluation plans/results,
traceability, execution plan and demo materials. Archived versions remain
historical evidence rather than the current specification.

## Current agreement

| Topic | Aligned interpretation | Main authority |
| --- | --- | --- |
| Product | Local educational small-business loan review; simulated roles; no production or bank-compliance claim | [PRD](../product/prd.md) |
| Core agents | Agent 1 Extraction; Agent 2 Compliance; Agent 3 Risk & Summary; deterministic LangGraph Orchestrator Agent | [Specialist contracts](../specs/specialist-handoffs.md) |
| Execution types | Compliance, finance, risk scoring and reporting use Python. Risk & Summary groups existing risk and synthesis responsibilities, not a merged node or extra LLM | [HLD](../architecture/hld.md) |
| Model calls | Two normal live generation stages: extraction and synthesis. Token probes, embeddings and offline judging are additional accounted requests | [Live profile](../specs/live-synthetic-integration.md) |
| Execution order | Sequential dependencies; live fact verification before calculations, conclusion verification after synthesis, readiness and credit review where routed | [Live graph](../specs/live-graph-integration.md) |
| Handoffs | Structured state and scoped recorded artifacts/events; UI rows are derived views, not newly backfilled messages, evidence support or scale proof | [Handoff presentation](../specs/specialist-handoffs.md) |
| User experience | Six screens, one Run AI Deal Review action, no mode radio. Existing config/app.toml selects new FIXTURE or LIVE execution; historical source governs display/resume | [Unified review](../specs/unified-review-experience.md) |
| Decision authority | Original AI proposal, five-outcome approval readiness and authorized human decision remain separate; future obligations are not automatically breached | [Readiness](../specs/approval-readiness.md) |
| Financial controls | Existing Decimal arithmetic, synthetic policies, five-factor illustrative score and boundaries unchanged; no calibrated PD or invented portfolio concentration | [Financial analysis](../specs/financial-analysis.md), [policy/risk](../specs/policy-risk.md) |
| Persistence | SQLite-backed local state/checkpoints; explicit recorded history; no automatic expiry, implicit reset or immutable-audit guarantee | [Persistence](../specs/persistence-observability.md) |
| Grounding | Runtime DIRECT; source/period/authority restrictions retained; hosted embedding capability verified but no measured hosted VECTOR/HYBRID semantic benchmark | [Grounding/contexts](../specs/context-optimization.md), [benchmark](hybrid-retrieval-benchmark.md) |
| Evaluation | Actual native/custom RAGAS on a saved answer; precision N/A for unranked DIRECT; live answer evaluation still pending; scores grant no approval authority | [Observed results](live-answer-quality-results.md) |
| Demo evidence | Saved examples, framework-level UI checks, graph-only notebook and versioned HTML exist; actual live completion and manual browser/fresh-kernel evidence remain incomplete | [Current status](../implementation-status.md), [runbook](../demo-runbook.md) |

## Corrections made

- Reconciled copied current-status claims about missing credentials, zero paid
  execution and no RAGAS with the later observed evidence. Earlier zero-call
  observations retain their historical milestone scope rather than being used
  as current facts.
- Removed outdated sidebar review-mode directions and obsolete user-facing
  fixture-specific Run labels. Clarified six-screen scope and the existing
  Decision History page; preserved historical version/change records.
- Updated stale feature implementation metadata for extraction, finance,
  policy/risk, orchestration, human review, memo, persistence and teaching artifacts.
- Updated HLD source/verification/readiness flow and its six-screen table. Added
  consistent specialist contracts, UI presentation guidance and test traceability.
- Distinguished actual saved-answer RAGAS, fixed embedding capability probes,
  retrieval mechanics/ID diagnostics and unexecuted semantic/live evaluations.
- Repaired 26 relative links in the archived README copy. Historical measurement
  text was not rewritten. The old HLD five-screen section anchor is retained as
  a compatibility alias for the updated six-screen section.

The externally supplied V2 reference document is not the approved architecture.
Its six-call ReAct design, unmeasured speed assertions, conflicting thresholds and
immutable MemorySaver claim have not been adopted into the current contracts.

## Validation

Final scan: **95 Markdown files reviewed** (90 active and 5 archived/inactive);
**905 local file links checked**, zero missing targets. Selected obsolete-current
status patterns had zero remaining active matches. The README/PRD examiner flow
matches. All **83 protected code/config/model-instruction files** are unchanged;
runtime instruction hashes and live packet identities match their pre-audit
values. All four registered source cases validate.

The audit checks local Markdown target files, selected obsolete-current-status
patterns, README/PRD examiner-flow agreement, runtime instruction hashes and live
packet identities. It separately records protected application/configuration and
model-instruction files, which must remain unchanged by documentation edits.

Focused verification: **15 tests and 30 subtests passed**, 5.77 seconds, using:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider tests/unit/test_context_identity.py tests/integration/test_normal_fixture_graph.py --tb=short
```

Measured audit counts and identities are retained in
`var/evaluations/document-alignment/final-report.json`. Original edited text and
earlier scans are retained under the same ignored audit directory.

This is a documentation consistency check, not fresh model-quality evidence or
proof every planned feature exists. File-link checks do not validate external
websites or every browser-generated heading anchor. The complete offline suite
was not rerun for these documentation-only changes; its previous recorded result
remains distinct from the focused checks above.

## Outstanding implementation work remains explicit

The interrupted request retains its unknown-usage reservation and recovery claim;
the user deferred reconciliation. Actual fact verification, live synthesis,
narrative review, final live memo and live RAGAS remain unfinished. Generic
uploaded-case financial admission, measured semantic retrieval, fresh-kernel
execution and manual browser acceptance are not marked complete by this review.
