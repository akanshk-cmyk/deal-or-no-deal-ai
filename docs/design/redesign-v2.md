# Command-center redesign V2 — implementation contract

Audit correction POLICY-VIEW-1.0: compliance cards, exception counts and policy
evidence now use the selected run's recorded post-synthesis final evaluation,
matching the memo. Earlier evaluation remains explicitly preliminary in original
artifacts. Workflow-control results such as NOT_TRIGGERED are not relabeled as
credit approval or policy Pass. Missing verified sources still withhold links.

User-authorized 2026-10-24 from the supplied Redesigned UI/UX Product Specification
V2.0. Implements its immediate P0 presentation improvements on APP-READ-1.0.

- Keep Python/Streamlit, six pages, shared financial read service and existing
  saved example registration/budgets. No external assets, fonts or frontend dependency.
- Apply navy navigation, light slate canvas, white bordered surfaces, blue actions,
  teal informational accents, and restrained amber/red states. Use semantic labels,
  keyboard-native controls and visible focus; never convey status only by color.
- Persist selected run across page navigation using a session-owned value separate
  from widget state. Display consistent borrower/amount/revision/execution/human
  decision context. Never infer human approval from AI recommendation/completion.
- Dashboard groups recorded runs by deal, with accurate counts and expandable run
  history. Search/quick actions are local reads; no invented owners or portfolio.
- New Deal separates registered sample intake from unavailable arbitrary uploads.
  Explain document validation and duplicate-result retrieval. Preserve command IDs.
- Workspace uses six analysis/review tabs, human-readable terms, metric/policy/factor
  tables and a source explorer alongside them. Reference buttons select exact
  registered handles; calculation/policy/assessment dependencies lead to original
  source blocks. Raw artifacts stay under developer details. Missing source versions
  withhold citations; no new semantic-support assertion.
- Activity shows nine visual stage cards using actual start/completion events, with
  ordered logs and artifact inspector. Do not fabricate percent-complete, failures,
  model usage or rerun/recovery controls.
- Memo preserves all seven original sections, download and source identities; adds
  document styling and summary metadata without regenerating report content.
- History shows business-decision empty state separately from recorded run milestones,
  rather than repeating the full technical log. Illustrative review/CSV remains in
  its separate preview; no synthetic human events are seeded.
- Future human-review controls are visibly disabled with an explanation. No new
  financial actions, real uploads, PDF export, reopening, authorization or immutable
  audit claim. Pending backend scope is unchanged.

Checks: actual UI navigation preserves selected run (including an older run), grouped
deal counts, contextual evidence buttons, all six pages, disabled human actions,
duplicate execution, no network/no implicit writes, original graph regressions.
Headless Streamlit checks do not establish browser/mobile/WCAG acceptance.
