# Six-Screen Financial Deal Review Command Center

## Deal-first saved-review navigation

Select Deal lists unique authorized deal IDs using borrower and plain-English scenario labels. Selecting a deal opens its latest recorded review, ordered by generation time and operation identity, consistently with the Dashboard. Earlier attempts appear only inside that deal's collapsed Review History section. Single-review deals do not show a history dropdown. Review labels use an ordinal, input version, UTC time and friendly status instead of opaque run IDs.

An intentionally selected historical review stays selected across Workspace, Memo, Activity and History. Show an earlier-review notice and Open latest review action. Explicit Dashboard links, corrections and reassessment continuations preserve their intended exact review; they are not silently replaced by a newer run. Navigation is read-only: no record deletion, source/model execution, permission changes or database writes. Saved and Live review modes remain separate.

Regression: tests/integration/test_command_center.py::CommandCenterTests::test_deal_selector_scopes_history_defaults_latest_and_preserves_records, plus existing historical-page, citation, correction and reassessment UI tests.

Observed offline validation: 37 tests passed in 107.42 seconds across command-center, source-correction, financial-review, missing-data and recommendation-presentation suites. Evidence: var/evaluations/deal-navigation.xml. The three-deal/four-run test verifies scoped history, latest defaults, historical navigation and unchanged database bytes; no model calls or external requests.


**Upload evidence UI:** Existing Upload page now offers cited manual proposals,
source/basis fields, pending/support table, RiskManager check/reason form, one-click
candidate-source navigation, preserved history and annual DSCR preview/blockers.
Financial Run remains disabled; manual facts are not AI extraction or approval.
See [UPLOAD-FACT-1.0](upload-fact-review.md).

**Upload UI:** New Deal/Upload offers native submission, synthetic attestation,
limits, safe file/page errors and saved inspection feedback. Retained workspace
library shows exact file/page/hash citations, inert text and original downloads.
All simulated roles read; Analyst submits. Show Inspected—not reviewed and keep
financial Run unavailable for unregistered packages. See
[UPLOAD-1.0](upload-inspection-integration.md).

**Correction UI:** New Deal adds E-N01 Extraction miss. Workspace's Source-backed
correction form requires documented CFADS, original basis/page, reason and explicit
verification. Save navigates to revision2 READY; no updated findings yet. Separate
Analyst Update affected findings runs analysis. Dashboard indicates Analyst next
action; Agent Activity labels reviewer-applied extraction separately from reused
intake. Memo/history preserve correction provenance. No extra screen or free-form
financial editor. See [CORRECTION-1.0](source-correction-integration.md).

**E-P01 UI:** New Deal adds the registered Conditional sample. Human Review shows
the unchanged source-backed condition and clickable evidence, current required role,
exception reason, draft preparation, separate specialist support and permitted final
Conditional Approve/Reject with comments/confirmation. Dashboard next-role projection
comes from reconstructed gates. Memo/history show OUTSTANDING, not fulfilled/fundable.
No free-text condition editor. See [CONDITIONAL-1.0](conditional-integration.md).

**Review input correction:** Normal runs without a pending financial review show
an explicit read-only explanation and Prepare a review-required sample action;
do not render an apparently broken disabled comment editor. Preparation selects
the reviewed sample but never starts a graph or changes persona. E-M01 explains
its distinct missing-data stop without suggesting generic approval.

Active financial and RiskManager handling inputs use native forms: current text,
selected evidence and confirmation submit together in one click. Submit does not
depend on an earlier text-area blur. Validate required fields on submit with a
specific no-write error; retain drafts on validation failure and show saved receipt
confirmation on success. Existing service role/scope/version/gate checks remain.

**E-F03:** New Deal offers Supported Reject. Workspace Human Review shows each
unhandled numerical exception, actual policy/calculation/source references and a
RiskManager-only reason/evidence form. All required refs must be explicitly selected.
Before handling no final decision is available; after RECOMMEND_REJECT the permitted
AuthorizedApprover can select/confirm Reject. Dashboard owner follows validated
unhandled requirements; History filter/details/CSV retain the separate handling.

**E-M01 sample:** New Deal adds the registered missing-CFADS scenario. Dashboard
prioritizes its Pending Information state, with simulated Analyst next owner;
Workspace shows missing CFADS and actual partial evidence while final actions are
disabled. Financial-run labels identify scenario; source/deal selection never
borrows E-N01 values. Credit Memo correctly has no completed report for this case.

**Screen 1 redesign:** [Dashboard design and read-model mapping](../design/dashboard-redesign.md)
supersedes the earlier simple deal-list presentation only. Search, KPI/risk filters,
row or selector-based deal selection, next-action guidance, borrower/risk/financial/
policy/workflow/action cards and source-bound navigation use stored latest reviews.
Original run selection on other screens remains unchanged until explicit dashboard
navigation. No task assignment, calibrated PD or trend service is introduced.

**Connected financial controls:** New Deal selects Normal or Human review required
sample. Workspace services enforce role/tier/current basis; comments and requested
items persist. Final Approve/Reject requires comments and explicit UI confirmation,
then consumes the recorded receipt on the paused graph. RiskManager can assess an
exact registered-source response and explicitly start revision2; general/new-fact
uploads stay unsupported. Memo/History show actual decisions and frozen context;
CSV is scoped and snapshot-checked. Normal runs without a review request retain
disabled actions. Conditional editor/reopening remain pending.

**Audit correction:** POLICY-VIEW-1.0 in
[APP-READ-1.0](financial-command-center-integration.md) makes the selected run's
recorded final policy authoritative for Workspace cards/counts/evidence. Before
synthesis, label the available panel preliminary. Preserve original inputs and
historical artifacts; no report regeneration, source substitution or new clearance.

**Current implementation (2026-10-24): [APP-READ-1.0](financial-command-center-integration.md) connects six destinations to actual E-N01 financial records. Normal/review-required fixture navigation, source inspection, activity, role-aware financial decisions, registered-source reassessment, memo and history are implemented. General uploads, arbitrary evidence fulfilment, Conditional editing and full UI acceptance remain pending; illustrative review is a separate preview.**

Authorized addition2026-10-24: [SPEC-013 Decision History](decision-history.md) adds a sixth page, scoped CSV export and event-time context snapshots. This supersedes earlier five-screen/no-history-export limits for that feature only. The current preview has Human review and Decision History navigation; the full six-screen shell and financial lifecycle adapter remain pending. Existing Workspace/Memo review controls and financial permissions are unchanged.

Feature ID: SPEC-010
Version: 1.21
Status: Approved specification; unified six-screen saved/live interface implemented with role-aware bounded review controls; manual browser/accessibility acceptance pending
PRD requirements: FR-001–003, FR-007, FR-009–012, FR-014–020
Role instructions: [Specialist instruction index](../agents/README.md)

## User-authorized V2 presentation

[Redesign V2](../design/redesign-v2.md) implements the immediate P0 scope from the
user's supplied design: deal-centric dashboard and accurate counts/search; sample
intake checklist separate from unavailable uploads; persistent selected run and
shared context; six workspace tabs and contextual evidence navigation; nine-stage
recorded activity cards; document-framed memo/download; business-decision empty
state separate from recorded run milestones. Human actions stay disabled until
the financial backend is connected. No portfolio figures, decisions, support,
source references, execution results or provider metrics are invented.
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

An operator acting as a simulated Analyst, Risk Manager, Compliance Officer or Authorized Approver can identify current activity, findings, evidence and next owner/action. The interface is Streamlit over shared services. No chat agent, real accounts, external notifications, simultaneous authenticated coediting or second financial engine.

Confirmed visual requirement, 2026-10-23: professional and realistic financial-review software. Use compact navy navigation, white surfaces on a light neutral workspace, restrained blue primary actions, aligned financial tables, consistent type/spacing and unobtrusive status badges. Keep the deal/action/evidence prominent and the product name/tagline compact. Use coherent synthetic case data and actual recorded execution/ownership/source lineage; blank/missing/pending states remain honest. The five-screen experience should resemble a usable analyst workspace while preserving visible educational, simulated-role and Fixture/Live context. No invented institution branding, generated activity, real approval/clearance claim or cosmetic confidence gauge. Detailed color/type/control tokens in the visual review remain proposed for the design-system gate; use the agreed stack and accessible components without a new frontend framework.

## Workflow and rules

Human-review addition authorized2026-10-24: [REVIEW-UI-1.0](human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10) adds a shared panel to Workspace/Memo: deal and current status, simulated reviewer role/tier, unresolved blockers, required comment, explicit unselected action, additional-information item list when selected, and Record review action. Show service-derived permitted actions/reasons, including read-only Administrator and disabled wrong-tier/blocked approval. A success message states the committed action/status and UTC time, not graph/report completion. The expandable chronological history shows role/ID, action/status, exact comment/items and timestamp. No financial outcome is preselected. Preserve drafts on validation errors and selection across refresh; a deal switch cannot submit a previous deal's draft/operation. Pending — additional information requested remains separate from Awaiting review and Processing. The reusable component/local preview are implemented before full screen integration; preview actions are visibly illustrative, isolated from actual deal execution and never resume a graph.

Persistent product name/tagline, EDUCATIONAL DEMO — SYNTHETIC DATA ONLY, role-simulation label and Fixture/Live badge. Sidebar retains Dashboard, New Deal, Workspace, Agent Activity, Credit Memo. Workspace is the main working surface; Agent Activity remains available as an inspection/learning destination. A selected deal/run/revision, selected finding/source and finding-list position persist across navigation where possible. No selected deal gives a selection prompt. Keep the selected demo role visible in a compact session area; changing persona/mode is intentional and never executes analysis, auto-switches authority or changes an existing run.

| Screen | Required content | Actions and limits |
|---|---|---|
| Dashboard | Five default columns: Deal, Request, Review state, Owner, Next action. The review state includes its concise attention reason. Row details retain stage, mode, issue breakdown and last activity; compact stored counts and expandable recent events | Search/filter by status/owner/mode, open/create deal; no inference on reads |
| New Deal | Three visible steps: Choose documents -> Check readiness -> Start review. Source selection/limits, per-file validation and policy/mode/budget prerequisites appear at the relevant step | Validate/commit locally; intentional Run once; explain unmatched uploads/unavailable Live before the Start step |
| Workspace | Default overview: current issue/owner/action, all mandatory blockers, key supported observations, separate AI recommendation/human review. Findings and selected evidence sit together; all terms, six financial metric cards, policies, risks and history remain available in labeled sections | One prominent contextual action; source/formula/rule inspection, correction, issue handling and shared review controls |
| Agent Activity | Current stage, last successful stage, stop/wait reason and next action first. Expandable graph/timeline, handoffs, budgets, usage and context diagnostics retain the full educational trace | Read/filter, permitted explicit retry/continue/cancel; no synthetic animation or invented percentages/time remaining |
| Credit Memo | Above the unchanged seven-section memo, show separate AI recommendation, Human review, Report status and unresolved-condition/action summary. Preserve preview/generated/historical, mode/revision/cutoff labels | Source links and the same guarded review controls; no P0 download/export or generic clearing |
| Decision History | Cross-deal chronological events, current versus event status, deal/reviewer/comments/time, filters/pagination and original-context details; complete recorded per-deal timeline | Read/export within allowed scope; explicit all-filtered CSV; timeline event buttons; no decision edits, invented lifecycle events, new model call or clearance |

Use existing Streamlit primitives first; final typography/colors/components belong to Phase 5 design system. Avoid UI code that duplicates financial comparisons, permissions, cache validity or graph transitions.

### SME review resolutions within the five screens

New Deal distinguishes Prepared case — complete review from Unregistered upload — partial analysis only. Show missing trusted assessment/subject configuration before Start; an unregistered Live run labels its action Run partial analysis and cannot promise a score or committee recommendation. Fixture mismatch remains unavailable with zero provider fallback. Preparation belongs to the trusted offline case-authoring path, not an uploaded policy, score slider or new UI form.

Workspace shows the financial subject and supplied assessment period beside relevant metrics, with source/basis/facility details on demand. For critical Live inputs awaiting FACT-SUPPORT-1.0, the primary action is Review source support with required Risk Manager persona. The existing evidence pane pairs each value with its exact row/label, units, scale, period and subject. Individually checked FACT targets can be submitted together through the existing support service; this is not generic approval. Source-support status is independent of KNOWN/Unknown extraction and of human credit disposition. Save support spends no inference; explicit Continue analysis rechecks readiness and budgets. If the value/source is wrong, use correction and its separate Save/Update flow.

The Evidence card keeps unique missing-required-source counts distinct from pending semantic support or subject conflicts. If documents exist but critical support is pending, show Support review required with the unmet requirement and owner; do not fabricate a missing document or imply complete evidence from0 Missing. No fourth default card or extra screen. Activity records the actual support pause/continuation, excluding human wait from active latency without hiding elapsed wait.

Where existing summaries say Human review, clarify Human credit review (the package disposition). Source-support review has its own status/detail; a Not required credit-review branch must not claim that no human source checking occurred. The actual simulated actor and evidence-support result remain visible without another default dashboard column or screen.

Financial/Terms details and Memo label covenants Extracted — not automatically evaluated, and state that sample-policy Pass does not establish agreement compliance. Preserve source terms/maturity/use of proceeds and disclose Annual-period analysis; full-term/balloon/refinancing adequacy not evaluated. Reported/adjusted EBITDA reconciliation is Deferred, never a completed comparison. Conditions display origin/category, owner or Unassigned, supporting refs and OUTSTANDING/recorded/handled status from CONDITIONS-1.0. A completed simulated Conditional review report is not evidence that conditions were fulfilled; unresolved mandatory prerequisites remain blocking.

### Engineering outcome and citation presentation

Use RUN-OUTCOME-1.0 and RESUME-1.0: show Review recorded; completing report only after the accepted receipt, and Report generated only after its actual current artifact/gates. A returned interrupt remains Awaiting human review; information END remains Needs information. A crash gap shows Recovery required with the guarded existing recovery action; duplicate clicks/refresh never schedule another task. STATE-UPDATE-1.0 removes stale current recommendation/report after corrections or support/source changes, retaining visibly historical versions. COVERAGE-1.0 opens all real pages for a table or qualified clause, including headers/notes, with honest text fallback. Keep all five screens/25 criteria; refine TEST-010-03/04/06 and existing UX tasks, without another control dashboard.

### Source date, authority and excluded alternatives

SOURCEFIT-1.0 uses the existing Workspace/evidence pane, not a new history screen or free-form historical chatbot. Show the selected review-as-of date and knowledge cutoff in review details and the recorded memo basis. Beside a validated value, expose its actual source/version, effective-date evidence, financial period/value kind/qualifiers and concise selection reason. View other sources shows relevant alternatives as Selected, Superseded for this field, Outside selected date, Different basis/tier or Unresolved, preserving all source links; an unknown reason cannot masquerade as verified authority. Older evidence remains inspectable without appearing as a competing current value. Missing temporal/authority support shows the affected requirement/owner and permitted next action, not a confident current fact. Changing the analytical basis uses the guarded revision/impact/Save/explicit-continue path; opening evidence changes nothing and invokes no inference. A frozen-as-of demonstration is visibly labeled and never presented as current lending information. Refine existing TEST-010-03/05/06 and UX-T03/05 only.

### Director review fixes in existing controls

NARRATIVE-CHECK-1.0 makes rationale, each condition and the proposed-action explanation inspectable support targets alongside observations. Reuse the existing citation/evidence pane and typed support controls; distinguish Reference checked, Human supported and unsupported/withheld content. A resolving source link cannot display verified meaning. Original AI text, human edits and credit disposition remain distinct; no extra screen or mandatory underwriting approval for every otherwise valid Low case.

SOURCE-TRIAGE-1.0 supplies the reason/owner/repair action for missing documents, unresolved financial/policy applicability or authority, true conflicts and missing reviewed configuration. An existing PDF with unresolved authority can show 0 Missing while a prominent Source authority unresolved blocker names the required action. Product-control source issues do not count as bank-policy exceptions. Admin coordinates reviewed offline setup, with no profile editor or financial clearance button. Assignment/acknowledgement changes no gate.

INPUT-EDU-1.0 validation displays a specific safe field/format/technical-limit error before a command mutation, preserving the draft and original source. Do not truncate the user's value silently or label a technical parse error Reject. CONTINUE-CHECK-1.0 appears in existing correction impact/readiness details: estimate remaining supported work, show the exact limiting allowance, and explain zero retry headroom without promising completion. A saved correction remains recorded if continuation cannot fit; historical recommendations stay Out of date. Citation inspection remains available after a budget stop and performs zero graph/tool/model work. Refine existing TEST-010-03/04/05/06 and UX-T03/04/05; no new UI IDs/metrics, cost dashboard or simulated execution.

## Simplicity, attention and interaction contract — UX-1.0

The user authorized these review fixes on2026-10-23. They refine defaults/presentation within the five screens, not scope, banking rules or an implemented design system. Prioritize current attention -> reason -> supporting evidence -> permitted next action.

| Area | Initial presentation | Available on request |
|---|---|---|
| Shared header | Deal name/request, current demo role and mode, plain-language current state | Run/revision IDs, policy/source versions and technical metadata in a labeled Details expander |
| Dashboard | Attention-first five-column list; concise reason/owner/action visible together. Search/attention filter stays easy to reach | Detailed stage, exception/gap/conflict counts, mode, last activity and recent events. A filter showing mixed modes says All modes; a selected run always shows its actual mode |
| New Deal | Supported synthetic boundary/limits, sample versus upload choice, local readiness, one mode-labeled Start action | Source IDs/hashes/versions and budget/configuration details; selected policy name/version and Fixture/Live availability remain visible before execution |
| Workspace | Overview and attention area, key findings, selected evidence; preserve a compact list of every unresolved mandatory blocker | Terms, Financial Analysis, Policies, Risks, Decision details and issue/history sections. Existing fields/metrics remain accessible; no critical issue hidden by disclosure |
| Activity | Current stage/last success, actual wait/stop reason, link to required action | Actual graph, stage/handoff IDs, event timeline, attempts/tokens/cost/context/cache diagnostics; exhausted-budget reason remains prominent |
| Memo | Separate recommendation/review/report labels plus unresolved conditions and next action | Seven ordered report sections, source/condition detail and historical/cutoff metadata |

Use one prominent action for the current task, derived from existing service permissions and unmet prerequisites; secondary navigation has lower visual emphasis. Ready intake uses Run AI Deal Review or Start live review. Missing information uses Add evidence, a supported correction uses Correct documented value, saved analytical changes use Update affected findings, permitted package review uses Record review decision, and completed runs use View credit memo. Never replace a required specialty action with generic approval. If the next owner is another demo role, explain the required role and permit intentional role selection rather than switching it automatically.

Dashboard row actions use links or secondary styling so the attention list does not become a grid of equally prominent buttons; New Deal remains its principal creation action. Workspace/Memo emphasize the selected case's current permitted action, with View Activity/View Memo/source navigation as secondary links. Existing service priority/status/capabilities determine action availability; this introduces no new severity or lending policy.

Keep the relevant unavailable action and a specific reason, such as Risk Manager handling required first, alongside the issue. Do not display every irrelevant role action as a disabled button. All mandatory blockers, stale-state notices and current-action prerequisites remain visible before submission. Notes/acknowledgements cannot resolve analytical/control gates.

Plain-language labels are deterministic presentation mappings over existing internal states, not new enums or financial decisions:
- NEEDS_INFORMATION: Needs information, followed by the missing/conflicting item.
- REVIEW_REQUIRED: Reviewer action required, with owner/reason; other mandatory escalation/block states retain their specific reasons and handling requirements.
- STALE: Out of date after correction, with affected sections/revision.
- Review NOT_REQUIRED: Human review not required by demo rules, never Human approved.
- A technical stop says Review stopped with its technical reason; Reject remains only a simulated recommendation/disposition.

AI recommendation, human disposition, policy outcomes, issue severity, execution state and report completeness remain separate. Use restrained color plus text/icon labels; completion is not a green credit-approval signal. Model confidence is available in Decision details as Model-reported, uncalibrated, with an explanation that it is not repayment probability. A low-confidence review trigger stays visible in the required-action reason even when the numeric field is collapsed. No confidence gauge, invented aggregate risk score or verified badge based solely on citation existence.

Finding/evidence interaction: selecting a finding opens its source/version/page/passage, formula or rule beside it; preserve selection/list position on return. On narrow layouts, show the evidence directly below the selected finding with a clear Back to finding action. Labels name the source/page or formula instead of repeated generic Click here links. Show both sides of conflicts and explicit missing/unavailable/unsupported-source states. Financial cards show value/unit and relevant sample-policy meaning first; View calculation and sources reveals inputs, periods, units, thresholds and references. Interpretation is reused from recorded artifacts; inspection adds no reasoning call.

### Citation discovery and source navigation — CITEVIEW-1.0

User requirement, 2026-10-23: reviewers must be able to find citations while validating details. Show visible, descriptive, keyboard-accessible citation links beside each material extracted fact, risk finding, rationale/condition and policy check; metric cards expose View calculation and sources beside the value. Citations cannot exist only in a final bibliography, hidden technical Details or hover tooltip. Example labels are Financial statements · p.2, Loan agreement · clause 4.1 · p.3, and Policy SYN-ESC-001 · version 1.0; actual labels/locators come from recorded artifacts, never invented illustrative references in an executed view.

Selecting a citation opens the existing Workspace evidence pane with its original document/version/page/passage or policy rule/version. Show the exact recorded source excerpt, surrounding context and available heading/table/row/units/period/subject metadata. Emphasize the referenced passage using stored spans where available; if precise highlighting/page positioning is unavailable, say so and show the identified passage/context without inventing a highlight or silently opening a different version. An original-page preview uses an already supported local renderer when available; a focused textual passage remains the required fallback. No new PDF-viewer dependency or model-based source lookup is required by this change. On narrow layouts, place evidence below the selected detail with Back to finding; preserve selected row, form draft and return position.

Calculated results link to the recorded formula, exact operands/units/basis and a citation for every required source input. A computed DSCR is labeled Calculated · FIN-1.0; never imply its numeric result appears verbatim in a document unless it does. Policy results link separately to the executed rule/version and supporting borrower inputs. Authored factor ratings link to their attributed synthetic assessment/rubric and material input sources; reviewer corrections link to the correction record and any documentary support. These are explicit calculation/policy/assessment/reviewer origins, not fabricated PDF pages or extra SourceRef kinds.

Keep all supporting references accessible. A compact multi-source link may show View all N sources, with full source labels in the evidence pane; conflicting sources must be explicitly identified and both available, without a silently preferred citation. Missing, unavailable, stale/version-mismatched or not-yet-supported evidence has a visible reason and permitted next action instead of a broken/decorative citation. Source existence/reference checked and HUMAN_SUPPORTED remain separate; opening a citation never marks a fact validated or satisfies a review gate.

Citation presentation is a scoped read projection over existing source/fact/metric/rule/assessment records: display label, origin kind, target artifact/source/version/locator, exact excerpt/context, optional stored focus span, support/status reason and return-to-finding reference. Do not add model-generated URLs, new wire fields, a separate evidence database or arbitrary filesystem navigation. Current/historical state must match the target's actual revision. Navigation invokes no graph/provider/LLM work, re-extraction, rule reevaluation or business-state mutation; existing source_opened analytics may record safe scoped reference IDs only.

New Deal keeps one ordinary form with a three-step indicator, not a new wizard framework. Persist safe draft data when moving back to replace a file. Explain fixture matching and missing Live configuration immediately after source/mode selection. An arbitrary unmatched upload cannot appear ready merely because parsing succeeded. The final readiness step shows exact failed prerequisites and the permitted way forward, not a generic disabled Run button. Service checks, not visual steps, determine readiness.

Correction form: show original/new value, source and reason, plus a read-only impact preview identifying affected analysis/recommendation/memo and possible model work. Revalidate preview/save against the current revision. Save correction records provenance/new revision and marks affected outputs out of date without running the graph. Show Correction saved; affected findings need updating and a separate intentional Update affected findings action only when service/budget/mode prerequisites permit. Preserve same-review cumulative limits and new-run/thread correction rules in SPEC-007/008. Usage/cost is estimated only when a verified estimate exists; otherwise say unavailable. Notes and review-only condition edits remain separate zero-inference actions.

Rule inspection follows [RULEVIEW-1.0](policy-risk.md#read-only-rule-evaluation-details--ruleview-10), inspired by the attached condition/outcome list. In the existing Policies section, each row shows rule name/ID, observed-versus-required summary, recorded outcome and View rule evaluation. One expanded row/evidence pane reveals exact versioned predicate/applicability, input values and sources, formula/unrounded comparison, recorded condition/group results, separate workflow consequence, owner and permitted action. Preserve table/finding selection on return. Scope the compact summary first; keep full mandatory blockers visible in the shared attention area. No new screen or default wall of policy metadata.

Use actual labels such as Pass, Exception, Unknown or Not applicable alongside explicit Human review required/Needs information/Blocked where applicable, rather than borrowing ACCEPT/REROUTE as deal decisions. A true predicate is not always a passing condition: E-P01's DSCR1.15<1.25 is true and produces Exception. Display AND/OR grouping only for recorded compound controls and retain other mandatory referrals; before synthesis the confidence check is Not evaluated yet. Pass is not a credit approval, and a source link is not proof of semantic correctness. Stale/unavailable/mismatched references show Cannot verify recorded evaluation with the relevant next action. View rule evaluation is read-only; no rule editing, Apply/Deploy/Mark validated button, live threshold slider, extra model work or automatic gate clearing is introduced. Numeric claims are available with exact calculation/source context, not a new risk-score gauge.

## Risk-score cards — SCOREVIEW-1.0

The user refined the case-level risk dashboard on2026-10-23 to three separate assessments: Credit risk, Policy checks and Evidence. Place this compact strip in the existing Workspace overview/Risks section below the current required action/all mandatory blockers; retain five screens and reuse the same current-revision summary in Memo. Credit risk is the RISK-EDU-1.0 value/band or Insufficient Data; Policy checks shows the deduplicated exception count; Evidence shows unresolved required missing items. Never merge them into one number or use a low credit score as a compliance/evidence clearance. Factor assessment coverage moves into View score explanation, not a fourth default card.

Credit risk shows e.g.41/100, Moderate, Higher means more modeled risk and Educational synthetic assessment. View score explanation shows the five ratings, rubric/source basis, weights/contributions, exact total, band configuration/boundaries, factor coverage and current input/method versions. The user confirmed classification before display rounding: Low0–25, Moderate>25–50, High>50–75, VeryHigh>75–100. Policy checks shows e.g.2 Exceptions with View policy checks opening RULEVIEW-1.0; Evidence shows e.g.1 Missing with View missing evidence naming the requirement/owner/action. Show incomplete/Unknown/conflicting/not-run findings explicitly in card detail; pending checks are Pending, not0. All three cards use the same deal/revision/policy scope. This index is not PD, model confidence or a calibrated bank rating.

Factor ratings still require explicit synthetic authored rubric/assessments and material source inputs; no automatic financial-to-factor mapping or LLM-assigned score is defined. Missing/conflicting material factor evidence or an unusable required assessment shows Insufficient Data with the affected factors/requirements, no numeric score/band and no weight renormalization. Optional unconfigured display metadata remains Not assessed; processing before the risk stage says Pending, not Insufficient Data by default. The60/40/30/20/50 arithmetic sample yields41/Moderate but is not an executed loan result.41 with2 exceptions/1 missing is a labeled illustrative layout only if that missing requirement is unrelated to material score inputs; missing CFADS cannot coexist with a completed41 score. No screenshot8/14 values, what-if sliders, real credit-data API or PD/expected-loss view is introduced.

Presentation reads recorded score/policy/evidence artifacts; it executes no scoring. SCORE-ROUTING-1.0 independently requires normal Authorized Approver review for every Moderate case, Risk Manager credit-risk handling then package review for High, and senior-tier Authorized Approver review for VeryHigh. Low follows existing conditional rules; policy/evidence/control blocks apply to every band. Show the authoritative Required action/owner from Orchestrator. AI-proposed action appears separately only when accepted current-revision SynthesisResult actually contains one; it cannot enable a blocked action or supersede the required owner. When synthesis is paused, say AI proposal unavailable pending required evidence and use the actual required-action label, not fabricated AI prose. Changed source/assessment/band/method revisions mark old cards/referrals/reviews Out of date. Valid zero stays0; missing is never0.

Use three equal-weight, clearly titled cards with existing Streamlit primitives; stack on narrow screens and use keyboard-accessible drill-down links. Show numeric score/band, policy exceptions and evidence gaps with text/icons; none looks like a final approval badge. A nearby summary explains e.g. Moderate modeled credit risk;2 policy exceptions and1 missing requirement prevent final-decision readiness, but only for actual consistent records or a clearly labeled illustration. Retain every mandatory issue/owner/action. Original product-level offline false-positive QA/benchmark metrics remain outside this strip. No new charting framework or additional navigation screen.

Keyboard/focus and update behavior: label controls and links, preserve readable contrast and visible focus, retain form values after recoverable errors, and show field-specific error text. Make processing/status changes available to assistive technology without stealing focus or auto-scrolling an evidence reader. Collapse noncritical technical details; blocking messages remain visible. Use accessible Streamlit primitives first and verify actual keyboard/status behavior during implementation rather than claiming accessibility compliance from a headless test. No extra confirmation step for read-only inspection; state-changing action labels and inline summaries explain their consequence.

No new dashboard, benchmark controls, false-positive-risk indicators, chat agent, remote notification, custom frontend framework, additional model call or additional navigation screen is introduced. HTML snapshots follow the same hierarchy but cannot mutate records or imply real processing.

## First-use, review effort and completion experience — CX-1.0

User-authorized product review fixes, 2026-10-23. This section refines the existing six screens and UX-T01–05; it introduces no new lending rules, screen, model request or required study. Use the existing shared view/service contracts. The Analyst is the default task perspective; specialist personas remain explicit simulated responsibilities, not separate authenticated users.

### First useful review

On an empty Dashboard and at New Deal's document-choice step, offer Start with a sample deal beside the existing synthetic-upload option. The sample introduction fits inline and can be skipped; it is not a compulsory tour or additional navigation screen. Explain: Inspect a synthetic loan, follow a finding to its source, and see the recorded review outcome and next action. Show the selected case name, Fixture mode, prepared-case scope and whether its registered files/configuration are available. E-N01 is the introductory case; E-P01, E-M01 and the existing correction/Reject variants remain subsequent walkthrough choices, not extra scenarios.

Selecting a sample only prepares the registered local source selection and displays readiness; it must not start a graph, create duplicate runs, spend inference or present prewritten results as executed. If the sample is unavailable, explain the missing setup rather than silently substituting another case. Keep the existing explicit Run AI Deal Review action after readiness. Explain Fixture as Recorded model-stage responses with real local workflow execution, not live AI output. A prepared complete case can reach its configured review outcome; an unregistered upload remains partial with its actual limitations shown before Start. Neither choice promises approval or a risk score without its prerequisites. Existing nonempty Dashboards retain attention-first ordering; a compact sample/help link does not displace actual blockers.

### Plain-language help in context

Provide short, keyboard-accessible What does this mean? help next to unfamiliar labels, available on activation rather than hover alone. Use trusted fixed copy and links to the existing calculation/rule details, never another LLM call or a second financial engine. Suggested copy:

| Label | Explanation / route to detail |
|---|---|
| DSCR | Cash available for debt service relative to required debt service. View this case's adopted formula, inputs and period; use FIN-1.0, not an alternative definition |
| Equipment LTV | The defined equipment-loan exposure relative to eligible equipment collateral value. Open the recorded formula, valuation and sources |
| Model confidence | The model's self-reported certainty. It is uncalibrated and is not the probability of repayment |
| Source support | A recorded check that the identified value or claim is supported by its exact evidence. Opening a citation alone does not perform this check |
| Policy exception | A recorded exception against a versioned fictional lending rule. It is distinct from missing information and technical failure |
| Simulated credit review | A demo-role disposition of this review package. It does not authorize real lending or establish that outstanding conditions were fulfilled |
| Report generated | The current review report was assembled. Read its decision, unresolved conditions and limitations separately |

Keep the existing three assessments, visible mandatory issues and primary action prominent. Financial explanations reuse FIN-1.0 and recorded rule versions; do not add a glossary screen or put RAGAS diagnostics into ordinary risk cards.

### Evidence review and local handoffs

Within the existing support form, related targets may share a visible evidence context and one submission only when the service already permits those individually identified checks. Every target retains its own explicit selection, outcome, scope and recorded evidence checks. No preselected or unchecked acceptance, one-click blanket verification, automatic support carried across changed revisions, hidden domain check or bypass of the capability matrix. Preserve draft checks during supported navigation within the current scope; on a target/revision change, explain invalidation and require revalidation. Source support, specialty handling and credit disposition remain separate actions.

A handoff names its actual recorded issue, required role/tier, reason and permitted action. Example presentation, only when the current request requires that role: Risk Manager review required. Select that demo role to continue. State Local demo handoff; no notification sent. Do not imply another person is online, auto-switch persona or change the request by assigning an owner. Intentional role selection preserves case/finding/navigation context and safe drafts where their scope remains valid, and it causes no inference. Service guards still decide whether the next action is permitted.

### Saved work, recovery and finish

Use receipt/current-artifact state to explain what is saved, what is incomplete and what may happen next. Never infer success merely because a button was clicked. Examples are conditional copy, not fixture outcomes to manufacture:

| Actual recorded state | Customer-facing message / action |
|---|---|
| Correction committed; downstream outputs invalidated; no continuation dispatched | Correction saved. Findings are out of date. Analysis has not restarted. Show affected sections and the permitted explicit continuation |
| Credit disposition receipt committed; report not yet generated | Review recorded; report completion pending. If recovery is needed, expose the guarded recovery action rather than another review submission |
| Saved work; remaining continuation fails the budget check | Your saved changes are retained. Analysis cannot continue within this review's remaining allowance. Keep evidence/history inspectable; no automatic reset or paid retry |
| Provider dispatch or usage uncertain | Request outcome could not be confirmed. Show retained reservations and the recorded technical stop/recovery reason; do not claim no charge, no request or safe replay |
| Current report artifact actually generated | Report generated. Present its recorded recommendation, separate human credit review and unresolved conditions; technical completion is not loan approval |

After refresh or reopening the same run, recover the latest persisted status/receipt and selected context where supported; do not start or repeat work. If storage failed before a receipt exists, state that the action could not be confirmed/saved and retain a safe draft where possible. Distinguish a receipt from an uncommitted draft and from a completed downstream artifact.

Use the existing Workspace/Memo summary area for a concise end-of-task recap: recorded review outcome; outstanding mandatory blockers/conditions and owner; permitted next action. Link to all unresolved items without hiding mandatory blockers. A valid no-action state says No further step is required by this demo workflow, with its scope/limitations; do not invent a follow-up or imply funding. Missing, partial, historical and unregistered-upload outcomes cannot display a completed final review. This recap is a deterministic projection of current artifacts and remains outside the unchanged seven-section report_markdown.

### Consistent controls and access to history

The Principal follow-up fixes use the same interface: valid specialist handling refreshes current gate readiness without presenting an analytical rerun; a real source/fact/config change still invalidates the pending review. If edited human conditions need support, the existing condition editor offers Save conditions for review, then names the required domain owner/action. This saves an exact draft/targets, not a disposition or graph resume. Record simulated credit review is available only when that exact current draft/original condition set and all other prerequisites are supported; no circular requirement for an assessment of targets that do not exist until after approval. Preserve original model conditions, drafts and actual outcome labels. EXEC-ADMISSION-1.0 returns Busy consistently when the same workspace is executing through the app/notebook/evaluation CLI; it never records an approval on failed admission. A retained uncertain claim shows Recovery required with the guarded permitted action, not an unrestricted Run/Reset. Existing TEST-010-03/04/05/06 and TEST-008-03/06/07 cover these states without a new screen, automatic clearance or model call.

The user-authorized Product Designer refinement integrates CX-1.0 directly into PRD section4.3 and its existing UI criteria. Keep the initial reading order action/reason/owner and every mandatory blocker -> three assessments -> finding/evidence -> optional diagnostics. The active task/form has one prominent action; do not emphasize a page-level submit and an unrelated form submit at once. Fixed help, visible citations and inspection links remain secondary and keyboard accessible. Long action/owner/status text wraps without clipping; preserve readable flow and focus at narrow widths/zoom. Exact component values remain subject to the design-system gate.

Use one shared explicit human-disposition selector with no preselected Approve/Conditional Approve/Reject value, supported condition controls and Record simulated credit review submission in Workspace and Memo. This changes presentation/defaults, not the approved disposition schema or lending criteria. A shown AI recommendation is read-only context until the operator intentionally selects a human disposition. Existing condition/reason/capability guards still apply. Draft controls use Cancel editing; the existing stop action uses Cancel processing and retains its acknowledged safe-boundary/in-flight meaning. If a navigation change would lose an unsaved draft, offer Keep editing / Discard draft before that loss, with no change to retained deal/source history and no extra confirmation for read-only inspection.

Out-of-date reports/evidence remain inspectable as historical artifacts; disable only stale state-changing actions, not history access. A storage failure, confirmed correction, accepted review receipt, pending report and uncertain provider dispatch each use the exact status/next-action rules above. Shared copy must never imply that a saved credit disposition proves report completion or that an uncertain provider request was uncharged. Existing TEST-010-03/05/06 verify these refinements; no new scenario, test ID, automatic review outcome or model call is introduced.

### Usability evidence and later visual consolidation

During existing UX-T01–05, record task success, help/errors and manual counts of clicks, intentional role changes and repeated evidence openings. Record short categorical friction notes such as unclear term, duplicate inspection or uncertain saved state; do not collect borrower text, source excerpts or draft notes in ordinary analytics. These counts are descriptive observations, not new pass thresholds or new telemetry events. Preserve current critical controls and the existing5/5 core task target. A self-check is labeled self-assessment. If feasible, one unfamiliar participant may repeat the same five tasks as an optional formative check; it is not an additional release gate, representative user study or proof of customer adoption.

The [Phase 5 design-system proposal](../design/design-system.md) now consolidates the visual tokens and message/action patterns. Rendered UI and keyboard/focus/status/zoom validation remain Not run; M1 execution approval is pending. Documentation does not establish rendered usability or activate application behavior.

## Contracts and data changes

Proposed reads: list_deals(DealFilter, ActorContext) -> DealRow list; get_workspace(ScopedDealRef) -> WorkspaceView; get_activity(RunRef, after_sequence) -> EventPage; get_memo(ScopedRevisionRef, kind) -> MemoView; get_evaluation_summary(EvaluationFilter) -> EvaluationSummary. The two small QA checks remain offline evaluation records, with no new dashboard, badges, charts or excessive-risk-flagging indicators in the MVP interface. Normal decision, missing-information and technical-failure states remain distinct. Evaluation controls do not invoke a model.
DealRow: identity/mode/revision, lifecycle/stage, owner, open issue counts by status/severity, primary_block_reason, next_permitted_action, updated_at.
WorkspaceView composes current typed artifacts and ActionAvailability entries: action_id, enabled, denied_reason, required_capability, expected_revision/record_version. No key/provider-client serialized to UI.
AttentionSummary is a derived view projection, not a new table: current state/reason, all mandatory blocker summaries, owner, primary permitted action/ref or denied reason, secondary navigation and separate recommendation/review/report labels. Use existing issue/routing/action data; UI code does not recompute permission or severity. Correction impact is a scoped read-only projection defined in SPEC-008. The memo summary sits outside report_markdown and cannot add an eighth report section or change recorded values.
AssessmentSummary is a derived current-revision projection: credit_risk(value/exact band/method+band versions/status/reasons/driver refs); policy_checks(unique applicable lending-rule exception IDs/count, evaluated coverage/Unknown/not-run state); evidence(unique unresolved required missing-item IDs/count, conflict refs and missing-material-factor refs); score-detail factor coverage; independent blocker/referral list; actual next action/owner/review tier/readiness; accepted AI proposal ref nullable with source/validation status. Count logic comes from Python artifact/issue projections, not duplicated UI policy or an LLM. Same input/source/config scope is required across all cards; mismatched/stale artifacts are explicitly unavailable/historical. No extra database or generation task; the five-field PanelDecision remains unchanged, while SynthesisResult may contain the separately specified nullable proposed_action outside it.
SelectionState: workspace/deal/run/revision, active screen, persona, filters, selected finding/evidence reference and list position where supported; mode change applies to a deliberate new authorized run, never silently rewrites an existing run.
Notes/owners are persisted metadata through SPEC-008, not fields in model prompts.

The explicit RAGAS-EVAL-1.0 addition uses the existing Activity instructor/developer evaluation expander and [evaluation report layout](../evaluation/evaluation-report-template.md). Show four native rows—Faithfulness, Response Relevancy, Context Precision and Context Recall—followed by five individually labeled custom1–5 score/status objects with explanations/examples. Expose exact native variant/version/scale, evaluated artifact/context/cutoff, manual/controlled/RAGAS and FIXTURE/LIVE subject labels, independent critical flags and separate evaluator usage. Preserve valid negative cosine relevance values; distinguish Not run, Not selected, Not applicable, Input unavailable, Failed and Stopped from a measured zero. DIRECT ranked precision is Not applicable. Optional ID diagnostics stay separately named; no invented overall score. Read/filter/open examples triggers zero scoring/embedding/model work; no routine deal-page score button, additional navigation screen, critical-gate override or automatic per-deal evaluation. Execution belongs to the explicitly configured offline service and allowance. Existing TEST-010-04/06 and TEST-011-07 own display/isolation checks.

## AI and evidence behavior

Accepted ADR-007 reference integration stays inside the existing six screens; [source contract](public-financial-sources.md) owns ingestion and retrieval behavior. A reference task is visibly labeled EDUCATIONAL DEMO - PUBLIC FILING REFERENCE, while the loan walkthrough retains its synthetic-data label. Show corpus/company/document type, agreement date or fiscal period, snapshot/fetch time and indexing status separately from a deal review. Do not show a public agreement as a completed loan score or approval. Workspace citations use retained HTML heading/clause/table/span locations and an explicitly labeled original URL; never fabricate PDF page numbers or reload the live page to recreate a snapshot. Source views, refreshes and role changes do not crawl, embed, reindex or invoke models. Activity distinguishes fetching/segmentation/embedding/indexing/searching and their actual failures/partial state. No sixth screen or default HYBRID activation is required; UI implementation/usability checks remain Not run.

Read/refresh/navigation/source views/preview/notes/review disposition invoke zero models. Show model narrative as interpretation with machine-reference versus human-support labels; never imply semantic verification solely from citation presence. Unknown, conflict, reviewer-provided, partial and stale badges are explicit text, not color alone.

## Authorization

All commands use service guards even if UI buttons disabled. Two screens invoking review share one pending operation/receipt. Wrong persona/stale record displays a concise reason and reloads current state without automatic replay. Local role switching is unverified.

## UI states

Every screen supports loading, empty, success, failure and stale states:
- Dashboard empty invites synthetic deal creation; failed query preserves navigation.
- New Deal shows file-level errors and keeps safe draft data.
- Workspace lists missing inputs/blocked actions without empty “approved” cards.
- Activity distinguishes waiting for human, information pause, retryable error, stopped/cancelled/completed.
- Memo uses explicit draft/partial/generated/historical labels, not just a spinner or checkmark.

Keyboard-accessible navigation/forms, labeled controls, focus-visible interaction and readable contrast. Narrow layouts stack evidence/panel content without hiding status or actions. Loading UI is driven by recorded service state, not invented timings. Streamlit reruns reuse persisted run identity.

## Reliability and stopping

Presentation reads do not restart the graph. Storage/provider failures show safe messages; live failures cannot become fixture success. Source navigation resolves within scoped manifest, never arbitrary file paths. Disabled action includes explanation, not a silent nonresponsive button.

## Analytics

screen_viewed; deal_opened; source_opened; action_requested/denied; usability_task_completed with screen/task ID, outcome, duration, help and error categories only, consistent with the existing evaluation plan; context/cache details through SPEC-006 events. Attempt completion includes unsuccessful attempts. Click/role-change/repeated-evidence counts remain descriptive manual QA observations. Avoid recording search queries, notes, source/report text or personal identifiers. See the [execution measurement plan](../execution.md) for trigger/owner/property mapping; do not double-emit older event aliases.

## Tests and acceptance

- TEST-010-01: UI-DASH-01–04: five default columns with visible reason/owner/action; additional fields remain available; stored counts, mixed-mode clarity, zero read inference and no duplicate runs.
- TEST-010-02: UI-NEW-01–05: three-step hierarchy, preserved draft/back navigation, source validation/exact fixture matching, early unavailable-Live/unmatched-file explanation, readiness reasons and one mode-labeled Run. Prepared complete cases versus unregistered partial uploads are explicit before Start; no promised rating-entry form or copied case configuration, and no score/PanelDecision when required trusted assessments are absent.
- TEST-010-03: UI-WORK-01–06: default overview/all mandatory blockers, contextual action/denied reason, finding/evidence and rule-evaluation detail/return position, exact predicate/input/formula/source/outcome alignment, separate status/confidence details, correction-impact/save/continue separation, service permissions and two-call allocation. Verify critical FACT support with source row/scale/period/subject, individual targets, intentional role and explicit continuation; source support is not credit approval or missing-document evidence. Covenant/annual-scope/deferred-EBITDA/condition labels remain accurate. Missing/stale/version-mismatched checks cannot look verified; rule inspection mutates nothing and adds no graph/tool/provider calls. SOURCE-TRIAGE-1.0 displays existing-document uncertainty as a scoped blocker with owner/action, without false missing-document or banking-exception counts.
- SCOREVIEW-1.0 extends existing TEST-010-03/05/06: three separate current-revision cards and drill-downs; source/band/method/driver explanation, exact classification versus rounded value, deduplicated exception/missing counts, pending/Unknown/conflict/Insufficient Data/stale states and accessible narrow layout.41/Moderate with unrelated missing control evidence can remain numerically valid/blocked; missing material score input cannot show41. AI-proposed versus required action remains distinct; no accepted current synthesis means no AI-labeled proposal. Factor coverage is secondary detail; no merged score, PD or fabricated approval. TEST-004-10/11 cover aggregation, bands and routing.

CITEVIEW-1.0 refines existing TEST-010-03/05/06: visible inline citations, exact current/historical target, quoted passage/context and truthful highlight fallback; computed-value formula plus operand citations; policy versus document versus authored-assessment/correction origins; all/conflicting sources reachable; missing/version failures explicit. Keyboard/narrow-layout navigation preserves finding/draft/return position. Opening evidence changes no fact/review/gate and invokes zero graph/tool/provider calls. Reuse SPEC-005 reference checks and TEST-009-05; no new test ID or scenario family.
- TEST-010-04: UI-ACT-01–05: current/last/stop/action first, full recorded graph/handoffs/usage available on request, no fake percentages or focus-stealing updates, zero read inference and actual nested work counts. The existing evaluation expander displays four native RAGAS rows and five custom dimensions/examples with distinct scales/statuses, exact versions, critical flags and original subject/cutoff. Verify Not run/null versus measured zero, DIRECT precision Not applicable, missing-reference status and legitimate negative relevance. Reading it dispatches no evaluator or embedding request.
- TEST-010-05: UI-MEMO-01–05: separate recommendation/review/report summary, unchanged seven sections, explicit incomplete/historical states, same guarded controls and zero writing/inspection inference.
- TEST-010-06: Cross-screen selection/revision and list position, duplicate review, keyboard/focus/field-error/status-update/narrow-layout behavior and safe content; no confidence gauge or offline-QA/benchmark UI. Headless checks do not replace the scoped manual keyboard/status review. INPUT-EDU-1.0 preserves invalid drafts with safe errors; CONTINUE-CHECK-1.0 explains exact limiting allowance and no-retry headroom without claiming completion.
- TEST-010-07: One operator/instructor completes the five tasks in the evaluation plan: locate attention deal; explain issue/owner/action; inspect evidence; source-backed correction with stale-impact understanding; distinguish memo recommendation, human review and completion. Record completion, duration, hesitation, help/errors and self-assessment. CX-1.0 extends the same tasks with sample discovery/readiness/explicit Run, accessible fixed definitions, scoped individual evidence checks, honest local role handoffs, saved-versus-pending recovery and final recap. Manually record clicks/role changes/repeated evidence openings with categorical friction notes; no new telemetry event or efficiency cutoff. Optional unfamiliar-participant feedback and the existing three-person/fifteen-attempt120-second study remain extensions, not new core time gates. TEST-010-02/03/04/05/06 own the corresponding no-dispatch, scope, state, permission and keyboard assertions.

All 25 PRD screen criteria plus controlled cross-screen checks must pass. No usability success is observed yet.

## Dependencies and implementation boundary

Uses SPEC-001–009/011. HTML remains a separate static walkthrough under SPEC-012, not Streamlit hosting. No frontend, assets, dependency or screenshots are created in Phase 3.
