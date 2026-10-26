# Dashboard implementation review — 2026-10-24

## Delivery matrix

| Feature | Result |
| --- | --- |
| Five distinct-deal KPI filters, search and risk filters | Implemented |
| Attention queue, row selection and accessible selected-deal selector | Implemented |
| Borrower, educational risk, financial, policy, workflow and action cards | Implemented |
| Selected operation retained on Workspace/Memo/Activity/History navigation | Implemented |
| Financial calculation and policy links | Implemented through existing verified Workspace explorer |
| Current role's permitted human-review actions | Implemented as guidance; commands remain in Workspace |
| Original review history | Implemented as recorded table; existing Financial run selector opens older runs |
| Responsive layout | Desktop three columns; mobile stacked; tablet native reflow, not custom two-column grid |
| Assigned staff, industry, existing exposure, calibrated PD | Unavailable; no invented data |
| Trend charts, task assignment and processing-time analytics | Unavailable; no sufficient observations/service |
| Inline reporting-period labels and policy-cell highlights | Partial: exact bases/periods/predicates remain in linked evidence; no inferred trends |
| Direct activation of a particular Workspace tab | Partial: opens Workspace and exact reference; tabs remain native user controls |

## Data mappings and boundaries

`ui/dashboard.py::project_deals` groups scoped runs, explicitly sorts by generation
time/operation ID and projects latest recorded extractor, calculation, risk and final
policy artifacts. Policy display retains existing dependency checks and separates
policy exceptions from workflow gates. Workflow labels derive only from actual
events; original timestamps absent in older stored events remain Not recorded.
Human decision comes from the existing verified run projection; review permissions
come from `get_financial_review`. A role category is not an assigned individual.
The projection writes no financial records and invokes no graph/model/embedding.

Changed components: `ui/dashboard.py` (new), `ui/command_center.py` (dispatch/removal
of old list), `tests/integration/test_command_center.py`, PRD, command-center spec,
design-system, dashboard design/review, execution plan and traceability.
No backend command, schema, source fixture, scoring rule, model or budget changed.

## Verification

- Full offline suite: **190 passed, 259 subtests passed in 67.35s**. Final table/row
  interaction refinements additionally receive the focused command-center rerun
  recorded in execution.md.
- Actual AppTest checks cover distinct-deal counts, older-run selection across
  screens, filters, calculation evidence navigation, mandatory review despite low
  risk, and unchanged database bytes for read-only navigation. Existing tests cover
  role-aware decisions and registered-source reassessment.
- Local Edge inspection at 1600, 900 and 390px: zero application exception boxes,
  zero JavaScript page errors; tablet/mobile document widths matched viewport.
  Network routing allowed localhost only. No provider calls or new dependencies.
- Ignored local screenshots: `var/evaluations/dashboard-redesign/desktop.png`,
  `detail-desktop.png`, `workflow-desktop.png`, `tablet.png`, `mobile.png`.
  These are local observations, not external-user testing or WCAG certification.

Remaining improvements require new scope/data: actual multi-deal intake, assigned
tasks, comparable time-series trends and validated Live model quality. Current
dashboard remains a single synthetic-case educational demonstration.
