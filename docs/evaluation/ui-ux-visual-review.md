# Deal or No Deal AI — UI/UX Visual and Interaction Review

Version: 1.5  
Review date: 2026-10-23  
Status: Professional/realistic visual direction confirmed by the user; detailed component tokens remain proposed, not a rendered-app evaluation  
Current baseline: [PRD](../product/prd.md), [SPEC-010](../specs/command-center-ui.md), [SPEC-009](../specs/credit-memo.md), [SPEC-012](../specs/jupyter-html.md); use their current user-authorized revisions  
Scope: Educational five-screen analyst/operator experience, within the approved Streamlit/local-prototype direction

Current phase update, 2026-10-23: the [Phase 5 design-system proposal](../design/design-system.md) now consolidates these tokens and message/action conventions. It is the proposed implementation baseline for review; this document remains supporting rationale. Earlier statements that the file had not been created describe the earlier review stage. Rendered UI, usability and accessibility results remain Not run; M1 execution approval is pending.

## 1. What can be assessed now

The workspace contains documentation only. There is no application, HTML, CSS or current rendered screenshot to inspect. This review assesses planned information architecture, interaction contracts and missing visual decisions. It does not claim observed defects in actual button dimensions/colors, successful user testing or accessibility conformance.

The existing design already specifies five screens, a five-column dashboard, three-step intake, one contextual primary action, finding/evidence pairing, visible mandatory blockers, explicit role/mode and separate credit/policy/evidence assessments. These are useful foundations. Final typography/colors/components are intentionally scheduled for the later design-system phase; their absence is a pending design decision rather than evidence of a poorly rendered application.

Sources of truth: [PRD](../product/prd.md), [Workspace/UI specification](../specs/command-center-ui.md), [Memo specification](../specs/credit-memo.md), [notebook/HTML specification](../specs/jupyter-html.md), [evaluation plan](evaluation-plan.md). Detailed review recommendations remain proposals; the user's subsequent professional/realistic appearance requirement is recorded in the existing PRD and UI/HTML specifications. The Phase 5 design-system document is not created here, and no implementation/phase gate is advanced.

## 2. Review process and rationale

1. Identify the operator's immediate job: understand the case, trust the evidence and perform the permitted next action.
2. Check attention order: current action/blockers, assessment, supporting details. Visual prominence must follow that order.
3. Inspect interaction risks: ambiguous verbs, competing buttons, disabled actions without reasons, lost edits, accidental inference and conflicting status meanings.
4. Propose restrained visual settings with measurable dimensions/contrast. Treat sizes as starting targets until rendered.
5. Check the five screens, narrow layouts, keyboard/focus, loading/error and stale-data behavior against existing tasks, without adding features or evaluation programs.

Each finding below follows observation -> user impact -> recommended adjustment -> verification. This is a design rationale, not an internal reasoning transcript or an empirical usability score.

## 3. Findings and priorities

Priority A: resolve before styling the prototype. Priority B: settle while producing the agreed design system and verify in the rendered demo. These priorities are presentation recommendations, not changes to financial severity, routing or permissions.

| ID | Priority | Observation / risk | Customer-experience impact | Recommendation and verification |
|---|---|---|---|---|
| UXV-01 | A | Risk cards, recommendation and mandatory actions could receive similar emphasis | Operator may act on a favorable score before seeing a blocker | Put the current required action/owner/reason and all mandatory blockers above the three assessment cards. Test whether the operator identifies the next step before opening detail |
| UXV-02 | A | Color meanings have no exact palette yet | Green may imply loan approval; red may conflate a technical stop with a credit recommendation | Use the semantic mapping below with explicit text/icons. Report generation is neutral/blue; green is limited to a specific passed check. Color never changes financial meaning |
| UXV-03 | A | Both source support and credit disposition involve a human | Generic Review/Approve labels could imply the wrong authority or action | Label Source support and Human credit review separately; use scoped verbs such as Record source support and Record simulated credit review. Verify the actor can explain the distinction |
| UXV-04 | A | Prepared versus unregistered upload and Fixture versus Live are separate concepts | A valid upload can be mistaken for a complete review or for a real-data service | Preserve Prepared case — complete review / Upload — partial analysis, plus a concise Fixture — sample AI outputs / Live — connected AI explanation. Both remain synthetic educational data; missing readiness is explained before Start |
| UXV-05 | B | Font hierarchy and numeric presentation are unspecified | Dense financial data can be difficult to scan, compare or interpret | Use the type/number conventions below; keep labels and evidence readable, with tabular numeric alignment and units. Check at normal and enlarged text sizes |
| UXV-06 | B | Button/control dimensions and destructive-action treatment are unspecified | Small targets and equally prominent actions increase misclicks | Target 44 CSS px control height, one primary action per task region and clearly separated Cancel. Inspect actual focus/click area, not icon size alone |
| UXV-07 | B | Long role/control labels and evidence panes can crowd laptop layouts | Owners/actions wrap unpredictably and cited source context becomes unreadable | Start with the responsive layout below; show full labels, stack evidence when necessary and preserve return position. Check representative laptop and narrow widths |
| UXV-08 | B | Role switching and rerendering can interrupt correction/support forms | Operator may lose carefully entered work or believe Save ran analysis | Preserve safe drafts and show exact Save/Continue effects. After a role/context switch, retain or explicitly offer to discard the draft; reject stale submission in the existing service |
| UXV-09 | B | Many chips, metadata fields and caveats are available | The main working surface can become a wall of technical detail | Keep persistent synthetic/mode context compact; put source/config/version/token details in labeled expanders. Never collapse away mandatory blockers or the reason an action is unavailable |
| UXV-10 | B | Loading, validation and stale-state presentation lacks a common visual recipe | A spinner or old result can look like fresh completed analysis | Show actual stage/state, field errors, preserved input and Out of date labels. Never invent progress percentages, time estimates, success or model work |
| UXV-11 | B | Memo could visually resemble a final credit approval | Review completion may be confused with fulfilled conditions/funding | Separate AI proposal, human credit disposition and report status. Show outstanding condition owners/status and covenant/annual-analysis limitations without changing the seven sections |
| UXV-12 | B | Accessibility is specified as intent without a rendered check | A visually tidy layout can still hide focus or fail at zoom | Check keyboard order, labels, status announcements, reflow and contrast on actual components. Contrast calculations alone cannot prove app accessibility |

## 4. Proposed visual direction

User confirmation, 2026-10-23: App should look professional and realistic. Record that as the visual requirement in PRD/SPEC-010/012. The concrete direction is a compact navy sidebar, light neutral page, white surfaces, restrained blue actions, readable aligned tables, consistent type/spacing and quiet status indicators. This confirms the professional appearance goal; it does not approve every suggested token, change a business rule or advance the implementation gate. Realistic synthetic case values, documents, owners, conditions and honest execution states supply credibility without copying bank branding or fabricating real activity.

Use a light neutral workspace, white content surfaces, dark readable text, one blue action color and restrained semantic accents. Keep the brand/tagline in the product identity area without taking the space needed for the current deal/action. Start with a single light theme; a dark theme is optional later work with its own contrast checks.

### Color tokens and meanings

| Purpose | Proposed color / pairing | Use |
|---|---|---|
| Page background | #F8FAFC | Quiet surrounding workspace |
| Surface | #FFFFFF | Forms, evidence pane, assessment cards |
| Navigation | #0F172A with white text | Compact professional sidebar; preserve readable selected/focus states |
| Primary text | #0F172A on #FFFFFF | Headings and financial values |
| Secondary text | #475569 on #FFFFFF | Supporting text; not faint gray for required information |
| Primary action | White on #1D4ED8 | Current permitted action; no implied approval |
| Information | #1E40AF on #EFF6FF | Recorded completion, context or non-adverse information |
| Attention / information needed | #92400E on #FFFBEB | Required action or missing/support-review prerequisite |
| Error / blocked | #B91C1C on #FEF2F2 | Explicit blocked/failed state with its actual meaning in text |
| Individual policy Pass | #166534 on #F0FDF4 | That check passed; never a global loan-approved signal |
| Neutral badge | #475569 on #F1F5F9 | Draft, history or neutral metadata |
| Control boundary | #64748B against white/page background | Authored input/control boundary where needed for recognition |
| Decorative divider | #E2E8F0 | Nonessential separators only, not the only cue identifying a control |

Risk bands retain their exact labels and thresholds. A Low badge can be neutral; Moderate can use the attention treatment. High/Very High may use the same stronger text/icon treatment while remaining separately named. A technical Processing stopped state and an AI-proposed Reject require different words/reasons even if both use red. No color or icon is a new risk rule.

Color-pair calculations performed for this proposal, using opaque sRGB values: white/primary blue 6.70:1; primary text/white 17.85:1; secondary text/white 7.58:1; warning 6.84:1; error 5.91:1; Pass 6.81:1; info 8.01:1; neutral badge 6.92:1. Proposed control boundary is 4.76:1 on white and 4.55:1 on the page background. These are calculated pair ratios, rounded for reporting; they are not measurements of a rendered UI. Hover/focus/disabled/opacity states still need checking.

WCAG 2.2 contrast guidance uses 4.5:1 for ordinary text, with 3:1 for qualifying large text; meaningful authored control/state cues generally need 3:1 against adjacent colors. A pale decorative separator is not a substitute for an identifiable input boundary. [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

### Typography, spacing and size targets

These are proposed CSS-pixel starting targets, not observed sizes or new business rules. Prefer existing accessible Streamlit controls/theme capabilities and local system fonts; verify framework constraints in implementation rather than adding a frontend library or relying on fragile internal-DOM overrides.

| Element | Starting target | Reason |
|---|---|---|
| Font | system-ui / Segoe UI / sans-serif | Familiar, readable and local; no remote font request required |
| Page title | 28 px, semibold | Clear location without overwhelming the deal/action |
| Section title | 20 px, semibold | Distinct from both page title and data labels |
| Body / form values | 16 px, line-height about 1.5 | Comfortable evidence and decision reading |
| Labels / secondary metadata | 14 px or larger | Keep required context readable; avoid tiny important text |
| Assessment values | 28–32 px, same scale across all three cards | Score does not visually dominate exceptions/evidence |
| Spacing scale | 4 / 8 / 12 / 16 / 24 / 32 px | Predictable alignment and grouping |
| Main/card padding | 24 px / 16–24 px | Separate information without excessive whitespace |
| Button / input height | Target 44 px; allow wrapped/zoomed text to increase height | Easier activation; do not clip long labels to enforce a fixed height |
| Button separation | About8–12 px | Reduce accidental activation and distinguish actions |
| Table rows | About48–56 px initially; grow for full content | Financial scanning and readable ownership/action labels |
| Assessment cards | Consistent internal rhythm; roughly128–160 px starting minimum | Alignment without truncating Insufficient Data or other statuses |
| Focus | Visible outline, proposed 2 px with 2 px offset | Preserve location around controls; do not rely on color alone |

The 44 px recommendation is a comfort target. WCAG 2.2 AA's target-size criterion starts at 24 by 24 CSS px, with specified exceptions/spacing alternatives; it does not require every button to be 44 px. [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

### Number and content formatting

- Label amounts with USD and thousands separators. On the dashboard, omit zero cents when appropriate; reveal full exact source/normalized values in detail. Never use an abbreviated rounded value to determine a route.
- Use 1.15× for a ratio and 60.00% for LTV consistently with FIN-1.0. Align numeric columns right and use tabular figures where supported. Keep units next to values.
- The educational score is not probability; preserve its direction, band and explanation. At rounding boundaries show the exact total in detail, for example 50.004 classified High even when displayed 50.00.
- Use Insufficient Data / Pending / Not evaluated with a reason; do not use 0 or a bare dash for missing facts. Pending support is different from an absent document.
- In prose, state one finding per paragraph with its implication and source link. Source labels identify the document/page or policy rule rather than repeating View for unrelated targets.
- Keep the action/reason/owner visible. Explain terms such as DSCR on first use or through an accessible help control; do not require hover to discover a blocker or action prerequisite.

## 5. Buttons and forms

| Action type | Presentation | Example / boundary |
|---|---|---|
| Current permitted task | Filled blue, clear verb/object | Run AI Deal Review, Run partial analysis, Review source support; choose the actual available action, not all at once |
| Source-support submission | Same primary treatment within the support form | Record source support for selected facts; submit only individually checked targets, no generic Mark validated |
| Correction Save | Primary within the correction form | Save correction; adjacent copy states results become out of date and no analysis is dispatched |
| Explicit continuation | Primary when saved prerequisites permit it | Update affected findings or Continue analysis, according to the existing service/state; explain possible model work/remaining allowance |
| Credit disposition | Explicit outcome selection plus submit | Record simulated credit review; original AI proposal remains separate, not a universal green Approve button |
| Read-only inspection | Secondary/outlined or descriptive link | View source, View rule evaluation, View calculation; same scope and return position |
| Cancel / abandon | Separated secondary or danger treatment according to actual effect | Cancel processing with safe-boundary explanation. Do not invent a delete/reset action or extra confirmation for ordinary read-only navigation |
| Unavailable relevant action | Visible reason next to the action | Risk Manager source support required first; service still enforces permissions |

Button width should fit the label with comfortable horizontal padding, rather than giving every action the same large width. Main mobile/form actions may fill their container. Keep loading/disabled labels readable. A successful Save displays exactly what changed; it does not use Done when analysis is still pending. Prevent duplicates through existing idempotency, not merely a spinner.

No additional confirmation screen is proposed for everyday inspection, correction Save or ordinary navigation. If an unsaved draft would be lost, offer Keep editing / Discard draft at that point. No new deletion or external-action workflow is introduced.

## 6. Layout and the five screens

Proposed Workspace reading order, shown as a structural sketch rather than a rendered prototype:

~~~text
Deal / request / educational mode / current state
Required action + reason + owner + all mandatory blockers
Credit risk          Policy checks          Evidence
Selected finding and analysis  |  Exact cited source / rule / calculation
Detailed terms, financials, conditions and history on request
~~~

Use a laptop-first content width up to approximately 1440 px, with a roughly 240 px sidebar where space permits. Source/finding panels may start around 55/45 width, but only stay side by side when each remains about 420 px wide or more. Otherwise stack the selected evidence below its finding with a clear return control. Sidebar collapses on narrower views. These are layout targets to verify in Streamlit, not promises of arbitrary CSS control. Avoid fixed-height nested evidence scroll regions where normal page flow works better; PDF/table viewers can have their own intentional navigation.

| Screen | Main experience | Specific review recommendation |
|---|---|---|
| Dashboard | Find the case needing attention | Retain five default columns. Use full deal/request values, concise state/owner and one row navigation affordance. Preserve explicit reason-based attention ordering from the service rather than inventing a new financial priority score; stable ordering avoids jumps during refresh |
| New Deal | Understand what can be reviewed before spending time or tokens | Put prepared versus partial-upload choice early. Keep limits, per-file validation and readiness at their relevant step. Persist drafts/back navigation; explain unavailable actions in plain language |
| Workspace | Understand a finding and act using evidence | Required action and all blockers first; three equal-emphasis assessments second; finding/source pairing third. Group source-support checks without preselecting unverified facts or presenting them as underwriting approval |
| Agent Activity | Explain actual progress or a stop | Current stage, last successful stage, waiting reason and next action first. Graph, node IDs, tokens and technical handoffs remain available below; show no decorative fake progress |
| Credit Memo | Read the recommendation and its limits | Compact AI proposal / Human credit review / Report status summary. Show source-support detail, outstanding conditions and existing blockers; retain seven report sections and no active unsupported export button |

Responsive verification should include a common laptop viewport, a narrower tablet layout and approximately 390 px mobile width. Also test content reflow at 320 CSS px equivalent/400% zoom where applicable. Genuine data tables/PDFs can require two-dimensional navigation; ordinary forms, action text and individual cells should remain readable without a page-wide horizontal scroll. [W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

Prefer inline action areas initially. A later sticky action bar must never cover focused fields/buttons or essential evidence; native focus should stay visible during refresh/navigation. [W3C focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

## 7. Verify customer experience without expanding the project

Reuse the existing five UX tasks and TEST-010/012 checks. Do not add a new user-study program, additional navigation screen, false-positive-risk dashboard or frontend framework. The following are proposed refinements to carry into the approved design/evaluation phase, not claims that current tests were run:

1. UX-T01: the operator identifies the attention case and its reason without scanning every technical field; color-only interpretation is unnecessary.
2. UX-T02: the operator names the required action/owner and distinguishes partial upload, source support and human credit review. A favorable score cannot hide a blocker.
3. UX-T03: the operator opens the exact source/rule/calculation, reads its labels/units/period and returns without losing place using keyboard as well as pointer navigation.
4. UX-T04: correction preserves the draft on a recoverable error, shows old/new/source impact, saves without model dispatch and makes explicit continuation/staleness understandable. A role/context change cannot silently submit stale work.
5. UX-T05: the operator distinguishes AI proposal, recorded credit review, generated report and outstanding conditions; completion never implies funding or fulfilled covenants.

For each task record observed completion, duration, hesitation/help and errors, labeling author self-assessment honestly. Use the already agreed five-task target and critical-control gates; do not invent a faster task-time threshold. Rendered checks should include text/control contrast in all states, keyboard order/focus, status announcements, narrow/zoomed layouts and long/wrapped labels. Proposed sizes/palette do not establish success or accessibility compliance.

## 8. Decision record and next phase

### Product Designer integration and rationale — 2026-10-23

The user requested reviewing and updating the PRD for the best educational product experience. Review the initial task/decision, path to evidence, interruption/recovery and end state; then reconcile existing screen requirements against CX-1.0. This is a specification review, not an observation of a rendered defect or a claim that the product is best-in-class. The following documentary inconsistencies are corrected in PRD v1.37 and SPEC-010:

| Prior wording / gap | Adopted refinement | Reason and trade-off |
|---|---|---|
| New experience rules were concentrated in an opening change note, while individual screens retained older labels | Integrate sample/scope/help/handoff/recovery/finish behavior and verifiable expectations into the existing screen sections and UI IDs | A builder/reviewer reading a single screen sees the current requirement. Reuse IDs and link CX-1.0 rather than creating another screen or duplicate specification |
| Load sample scenario and only two Run labels left scope/start behavior ambiguous | Start with a sample deal prepares readiness; the explicit Run label matches Fixture, prepared Live or partial Live scope | Prevent surprise execution and overpromised uploaded-document outcomes. Keep first-use guidance optional and existing attention work prominent |
| Approve demo recommendation and separate memo action labels could anchor the reviewer to an AI result | Shared explicit disposition selection with no preselected outcome, followed by Record simulated credit review | Preserve deliberate human action and consistent effects. Keep the approved schema/condition/permission guards rather than introducing new decision rules |
| Disable stale report/review actions could be read as blocking history inspection | Keep historical artifacts readable with truthful revision labels; block only stale state-changing actions | Users can understand what changed after a correction without accidentally accepting obsolete findings. This is not automatic comparison, recomputation or reuse of old support |
| Generic cancellation and completion labels could blur draft loss, execution stop, saved receipt and finished report | Separate Cancel editing from Cancel processing; use actual receipt/artifact/uncertainty feedback and a conditional end-of-task recap | Reduce accidental loss and false reassurance while preserving safe stopping, budgets and all unresolved issues. No new auto-retry or confirmation for ordinary reading |

The interaction rationale follows visibility, consistency, recognition and recovery principles in [Nielsen Norman Group's usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) and concise, actionable submission feedback in [W3C's form-notification guidance](https://www.w3.org/WAI/tutorials/forms/notifications/). These sources inform the design; they do not certify this implementation or its financial conclusions. Verify the refinements with the existing five user tasks and keyboard/focus/narrow/zoom checks after a prototype exists. Exact palette/type/spacing/control tokens still await their existing design-system gate.

The user subsequently authorized the product-experience fixes in [CX-1.0](../specs/command-center-ui.md#first-use-review-effort-and-completion-experience--cx-10). The sample introduction, fixed inline help, scoped evidence-selection behavior, explicit local handoff, receipt-based recovery copy and outcome/conditions/action recap now have specification contracts. Existing five-task checks include manual interaction counts and optional unfamiliar-person feedback; they have not executed. This resolves the documentary gaps and establishes what to implement/test. Actual review effort, comprehension, rendered appearance and accessibility remain unmeasured. Exact visual tokens still require the planned design-system consolidation; this review remains supporting rationale rather than a competing source of implementation rules.

Recommended next visual decisions: restrained light palette; consistent type/spacing/control targets; explicit button/action semantics; a responsive finding/evidence workspace; concise role/mode and completion labels. Keep existing financial rules, score bands, permissions, two normal model calls, token/cost caps and no automatic expiry unchanged.

The professional/realistic direction is now recorded in the PRD and UI/HTML specifications. Exact component values remain recommendations; the pending Phase 5 design-system deliverable is not created or approved here. Once the relevant phase is approved, consolidate agreed values into that single design-system source and verify them in actual Streamlit and HTML implementations. This review must not become a second competing implementation authority.

The initial review added this Markdown; the subsequent confirmed visual preference updates existing PRD/HLD/UI/HTML documentation. Calculated proposed color-pair contrast and static document links can be checked now; actual rendering, component dimensions, user tasks, keyboard/screen-reader behavior, model calls and accessibility conformance remain untested. No code, deployment, paid service or runtime prototype was created.
