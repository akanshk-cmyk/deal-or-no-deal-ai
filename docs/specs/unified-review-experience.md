# Unified deal review experience

User authorized 2026-10-25: retain the saved-response interface as the baseline,
integrating live functionality without merging execution workflows.

- Keep all six navigation destinations and the existing saved-mode forms,
  workspace tabs, dashboard, citations, memo and history controls.
- Expose exactly one primary sample action: **Run AI Deal Review**. No review-mode
  radio control. Upload inspection remains a separate non-financial action.
- Existing `config/app.toml` `mode` selects new execution: `FIXTURE` calls
  `start_run`; `LIVE` calls `run_live`. Default remains `FIXTURE`. Reject any other
  value. Existing disabled tracing/model flags and limits remain unchanged.
- State the configured response source before Run, including paid-call awareness
  for LIVE. Credentials, rendering and readiness checks never activate execution.
- LIVE currently supports only the registered Standard Deal. Other saved
  scenarios remain supported when configured FIXTURE; arbitrary uploads remain
  inspection-only. There is no silent fallback between paths.
- Combine scope-checked saved/live projections in the existing UI deal selector,
  dashboard and per-deal Review History. Preserve source-specific metadata and
  original historical content. Configuration changes affect new runs, not how
  existing records are interpreted, displayed or resumed.
- Use the same `render_workspace` implementation for both sources. Source-specific
  components only add live evidence status, original source text before synthesis,
  next-role guidance and existing fact/narrative/credit controls in Human Review.
- Preserve all interrupts, exact-version checks, authorization, usage allowance,
  unknown-usage recovery, readiness and financial calculations. Verification does
  not grant credit approval. Display recovery as error rather than success.
- Credit Memo identifies the actual source of the selected review. Decision
  History retains existing saved filters/exports and also shows recorded live
  evidence assessments and credit decisions for that deal, explicitly labeled.
  Existing CSV export remains the existing financial-history scope; live evidence
  receipts are not silently added to that export or converted into credit events.

No model/prompt/policy/scoring change, dependency, migration, live request or
historical rewrite is required. Tests use isolated workspaces, saved examples and
mocked Nebius. Check both configurations, mixed history, failed-live/no-fallback,
explicit start, read-only rendering, human support and completed memo.

## Observed offline validation

Final full suite: **315 passed, 269 subtests passed**, 258.22 seconds. Seven
warnings are existing pytest JUnit-property compatibility and RAGAS ID-metric
deprecations. Evidence: `var/evaluations/unified-review-offline.xml`.

Regression coverage includes configuration validation without activation, a
single primary Run action, saved examples, mocked live extraction/synthesis,
source verification interrupts, mixed-source per-deal history, original saved
record preservation after configuration changes, live failure without saved
fallback, read-only navigation and source-labeled completed memos. No real model,
embedding, evaluator or SEC request was made for this UI change. Personal review
records and historical artifacts were not rewritten. Browser pixel fidelity was
not separately assessed; UI checks used Streamlit AppTest.
