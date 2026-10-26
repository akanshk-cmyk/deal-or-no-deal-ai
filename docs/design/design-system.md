# Deal or No Deal AI — Design System

Current navigation and review source: use one Run AI Deal Review action, no
review-mode selector, and retain actual saved/Nebius source labels on historical
records. Agent Activity shows three role groups, the deterministic orchestrator
and read-only dependency progress from existing events. Technical node details
remain available; findings recorded never means verified evidence or approved
credit. See [the unified UI contract](../specs/unified-review-experience.md) and
[specialist handoffs](../specs/specialist-handoffs.md).

## Approval readiness presentation

Show current readiness as the main assessment, followed by its reason and permitted next action. Keep the original AI proposal in a secondary expandable explanation and show the human decision separately. Reuse the same assessment on Dashboard, Review Workspace, Credit Memo and Decision History. Hide unavailable approval actions, retain backend enforcement, and explain the required specialist review. Historical memo text and decision-time snapshots retain their original dates and assessment versions. Unknown covenant timing remains Pending Review; avoid red breach styling for future obligations merely not yet due.


**Conditional review controls:** Use existing native forms, citation explorer,
required comments, explicit evidence selection and confirmation for E-P01. Show
next required simulated role and separate specialist statuses. OUTSTANDING condition
and original Exception stay visible after report completion. Do not present support
as condition fulfilment/funding authority. No extra screen or UI dependency.

**Financial workflow update:** The reviewed sample now has actual permitted
actions, required comments, explicit final-decision confirmation and status/history
feedback. Do not show illustrative actions as financial decisions. Information
requests show a blocking notice; RiskManager's bounded response panel maps every
item to an exact registered PDF before reassessment. Reused intake/extraction
stages are labeled Reused, not executed again. Memo displays renderer/time and
actual human disposition. CSV follows explicit Prepare/Download with scope/snapshot
checks. Generic uploads, Conditional editing and broad recovery controls stay
unavailable. Full accessibility and notebook-kernel checks remain separate.

**Integrated shell:** Six native Streamlit destinations display actual execution status, separate risk/policy/evidence indicators, stage expanders, an evidence selector and original source-page text. Empty/error/source-version-unavailable states do not fabricate content. Bounded role-aware financial and evidence review controls are connected; generic new-document workflows remain limited. Framework-level UI checks passed; manual browser/keyboard/contrast/responsive acceptance remains unverified.

Decision History addition2026-10-24: [SPEC-013](../specs/decision-history.md) adds the sixth target page using existing native components: compact UTC chronology table, visible filter/search controls, bounded pagination, Open event details selector, per-deal timeline buttons and an explicit Prepare/Download CSV flow. Distinguish Status at event from Current status. Use Not captured for absent metadata/context and label all simulated reviewer identities. Historical AI/risk/source details use inert text/JSON expanders; timeline coverage is explicit. Show empty/invalid-date/stale-export/permission states without fabricated records or color-only meaning. Existing five-screen rules below remain applicable to their original surfaces.

Version: 1.2
Date: 2026-10-23
Status: User-authorized V2 implemented for the normal saved example shell; headless UI checks executed, manual accessibility acceptance pending
Authority: [PRD](../product/prd.md), [SPEC-010](../specs/command-center-ui.md), [memo contract](../specs/credit-memo.md), [offline presentation](../specs/jupyter-html.md), [execution plan](../execution.md)
Supporting rationale: [visual/interaction review](../evaluation/ui-ux-visual-review.md)

## Scope, approval and implementation

The user's supplied V2 specification authorizes the immediate presentation redesign
in [redesign-v2.md](redesign-v2.md). It supersedes earlier proposed-only visual
status for this bounded implementation. Current tokens use navy #10233F navigation,
slate #F4F7FB canvas, white surfaces, blue #1D4ED8 actions and teal #087E8B accents.
Local .streamlit/config.toml and ui/presentation.py own theme/style; no remote assets.
Deal-centric grouping, shared context, six workspace tabs, contextual evidence
buttons, visual stage cards and memo framing reuse actual recorded outputs.
Decision History distinguishes no recorded human decisions from run milestones.
Upload and human-action controls are visibly unavailable, not simulated as working.
The older five-screen/sixth-screen-unneeded wording below is historical; FR-021
and the V2 six-screen scope take precedence. CSS selectors are presentation hooks
against installed Streamlit; native controls remain keyboard operable, but actual
browser/mobile/focus/contrast checks must still be reported separately.

The user confirmed professional, realistic financial-review software. This document consolidates the earlier proposed tokens and approved UX-1.0/CX-1.0/CITEVIEW-1.0 behavior for the existing six screens. Exact visual tokens below remain proposed until reviewed; M1's backend-only approval need not imply a rendered-design acceptance. Once accepted, use this document for styling rather than a second competing palette in review notes.

Implement with accessible Streamlit primitives/theme and lightweight local HTML/CSS for the later offline walkthrough. Keep one shared semantic view/service model; do not duplicate calculations, policy evaluation, permission logic, source selection or graph transitions in UI/HTML. No new frontend/charting framework, remote font/icon service, dark theme or additional navigation screen is required. Prefer labeled text controls and familiar local icons where available; never require an icon to convey a financial outcome.

## Product identity and information hierarchy

Name: Deal or No Deal AI. Tagline: Every deal has a story. Our agents find the plot holes. Keep both compact in the identity/navigation area. A persistent EDUCATIONAL DEMO notice and task-specific data label distinguish SYNTHETIC LOAN DATA from PUBLIC FILING REFERENCE under accepted ADR-007. Show simulated role and actual task/mode/corpus without implying public statements are synthetic or a real-company loan is approved. Avoid repeating large notice blocks beside every field; no new color system or screen is added.

Reading order: selected deal/request/context -> required action, reason, owner and every mandatory blocker -> three independent credit/policy/evidence assessments -> selected finding and cited evidence -> optional terms/metrics/history/technical detail. A favorable number never displaces an unresolved blocker. Workspace is the principal working surface; Activity explains execution and teaching detail on demand.

## Color tokens and semantic meaning

Single light theme, proposed opaque sRGB values:

| Token | Value / foreground pairing | Purpose |
|---|---|---|
| page | #F8FAFC | Neutral workspace background |
| surface | #FFFFFF | Cards/forms/evidence |
| navigation | #0F172A with #FFFFFF text | Compact sidebar and selected-location context |
| text-primary | #0F172A | Headings/body/financial values on white |
| text-secondary | #475569 | Readable supplementary metadata |
| action-primary | #1D4ED8 with #FFFFFF text | Current permitted task; blue does not mean loan approval |
| information | #1E40AF on #EFF6FF | Recorded completion/context without credit endorsement |
| attention | #92400E on #FFFBEB | Required action, information/support prerequisite |
| error-blocked | #B91C1C on #FEF2F2 | Actual failure/block with specific text/reason |
| check-pass | #166534 on #F0FDF4 | A particular recorded check passed, not general approval |
| neutral-badge | #475569 on #F1F5F9 | Draft, historical, pending metadata as explicitly labeled |
| control-boundary | #64748B | Meaningful authored input/control edge on page/white surface |
| divider | #E2E8F0 | Decoration only; not the sole control boundary/state cue |

Text/icons accompany color. Report generated and review recorded use neutral/information treatment. Low/Moderate/High/Very High retain exact names/boundaries and their actual required action; color is not another severity/decision model. Technical failure and simulated Reject require distinct text even if both use an adverse accent. Model confidence is uncalibrated detail, never a green correctness gauge.

Existing review calculated selected opaque-pair contrast, not rendered-state accessibility. Verify ordinary text4.5:1, qualifying large text3:1 and meaningful control/state cues3:1 as applicable, including actual hover/focus/disabled/opacity states. Do not claim WCAG conformance from palette math or a headless test. [W3C contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Typography, spacing and control targets

| Element | Proposed starting token | Behavior |
|---|---|---|
| Font | system-ui / Segoe UI / sans-serif | Local fallback; no external font request |
| Page/section title | 28px /20px, semibold | Clear hierarchy without oversized branding |
| Body/form values | 16px, line-height about1.5 | Comfortable evidence reading |
| Secondary labels | 14px or larger | Never tiny important warnings/owner/action text |
| Assessment values | 28–32px, equal visual scale across three cards | Credit score does not overpower policy/evidence |
| Spacing | 4/8/12/16/24/32px scale | Consistent grouping/alignment |
| Main/card padding | 24px /16–24px | Readable density, not excessive empty space |
| Inputs/buttons | Target44px minimum comfort height; grow for content | Wrap long/zoomed text; never clip an action to enforce a fixed height |
| Button separation | About8–12px | Separate actions and reduce accidental activation |
| Table row | Start48–56px, grow as needed | Full borrower/owner/status/action labels remain available |
| Focus | Visible outline, starting2px plus2px offset where authored | Must remain visible around controls and after navigation |

The44px target is a comfort recommendation; WCAG2.2 AA target-size guidance starts at24 by24 CSS pixels with specified alternatives/exceptions. Preserve usable targets and actual keyboard behavior, without forcing fragile Streamlit internal-DOM CSS. [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

## Layout and responsive behavior

Laptop-first content up to about1440px, sidebar around240px when space permits. Finding/evidence columns may start55/45 while both remain approximately420px wide; otherwise stack evidence directly below its selected finding with Back to finding. Collapse sidebar navigation where necessary. These are layout starting points to verify with actual components, not a guarantee of arbitrary CSS control.

Use normal document flow initially. Avoid a fixed-height maze of nested scroll regions; PDF/table viewing may have intentional internal navigation. A sticky control, if later used, cannot cover focus, essential evidence or errors. On ordinary narrow/zoomed forms, page-wide horizontal scrolling must not be necessary to find the next action. Genuine two-dimensional tables/PDFs retain their disclosed navigation. Check representative laptop, narrower tablet/mobile and320-CSS-pixel-equivalent reflow/zoom behavior. [W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

## Shared components and screen composition

| Component / screen | Default content | Interaction boundary |
|---|---|---|
| Context header | Deal/request, current plain-language state, role/mode and current/historical marker | IDs/versions/cutoff in labeled detail; no automatic mode/role changes |
| Attention area | Required action/reason/owner and all mandatory blockers | One prominent actual task; irrelevant disabled controls omitted, relevant prerequisites explained |
| Dashboard | Five columns: Deal, Request, Review state, Owner, Next action; local search/filter | Actual stored attention work first; stable selection/filters and no automatic analysis |
| Sample introduction | Start with a sample deal and prepared scope/availability; short expected outcome | Selecting E-N01 prepares readiness only; optional help can be skipped. On nonempty Dashboard, sample help stays secondary |
| New Deal | Choose documents -> Check readiness -> Start review | Distinguish prepared complete from partial synthetic upload before the actual Run; retain drafts/errors/back navigation |
| Assessment strip | Credit risk; Policy checks; Evidence | Three separate measures with explicit Pending/Unknown/Insufficient Data; recorded source/method/scope details on request |
| Findings/evidence | Selected observation/value next to actual source, rule or formula | Visible inline references; preserve selection/return position; no inference on inspection |
| Individual support form | Identified targets with their exact evidence/domain checks | No preselected blanket validation; related targets may share context but only individually selected/outcome-checked targets submit |
| Condition editor/review | Original model conditions distinct from exact human draft and support status | Save conditions for review when needed; final Record simulated credit review consumes reviewed targets. No default credit selection or self-granted support |
| Activity | Current/last stage, actual wait/stop reason and next action | Graph/handoffs/counters/evaluation detail expanded on demand; no fake animation, percentage or remaining time |
| Memo summary | Separate AI recommendation, human credit review and report status; outcome/conditions/owner/next action | Seven-section report remains unchanged; summary reads records and adds no generated conclusion or clearance |

Ordinary labels use plain language; raw enum values are optional diagnostics. Human credit review is distinct from source support. A citation can be Reference checked without being Human supported. No false online collaborator/avatar, generated event timestamp or bank logo is used to manufacture realism.

## Actions, forms and state feedback

[REVIEW-UI-1.0](../specs/human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10) uses an unselected action control plus one Record review action button, a labeled required Review comments field and a conditional Requested information field (one item per line). Use visible service-derived permission/block reasons and plain-text status labels; color alone never distinguishes Approve, Reject or Pending. Show the selected deal and simulated role before submission. Render comments/history as inert text, show actual UTC timestamps and preserve the form draft on denied/stale submissions. Do not auto-select Approve, change personas automatically, claim real authentication or show report completion after a UI-only decision.

One prominent action within the active task/form, with secondary navigation and inspection links. Default actions come from shared service permissions and prerequisites, not a UI-side Boolean rule. Proposed labels reuse the accepted behavior:

| Action | Label / feedback |
|---|---|
| Registered saved example / complete Live / permitted partial upload | Run saved example review / Start live review / Run partial analysis |
| Source check | Review source support; then Record source support for selected facts |
| Documented correction | Save correction; show affected outputs become out of date and that analysis has not restarted when confirmed |
| Permitted continuation | Update affected findings / Continue analysis with actual remaining allowance/prerequisites |
| Changed conditions needing support | Save conditions for review; show actual required domain owner/next action |
| Final package disposition | Explicit Approve/Conditional Approve/Reject selection with no preselected outcome, then Record simulated credit review |
| Edit cancellation | Cancel editing; if unsaved work would be lost, Keep editing / Discard draft choice |
| Execution cancellation | Cancel processing with safe-boundary/in-flight explanation; Stopped only after acknowledgement |
| Inspection | Descriptive document/page, View calculation and sources, View rule evaluation; no new confirmation or model call |

Use labeled fields, actionable field-specific errors and safe draft preservation. For multiple submission errors, provide a concise summary linked to affected controls where supported. Success feedback describes what actually committed rather than showing a generic Done. Do not steal focus or auto-scroll away from an evidence reader during updates. Use accessible native status/notification mechanisms and verify their rendered behavior. [W3C form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/).

## Loading, empty, partial, stale and failure states

| State | Required presentation |
|---|---|
| Loading | Actual scope/stage or placeholders; unavailable counts remain unknown, not fabricated0 |
| Empty Dashboard | Sample introduction plus supported synthetic-upload choice; no fake live deals |
| No filter matches | Preserve filters and offer Clear filters |
| No selected deal/run | Useful selection prompt and navigation, not empty approval cards |
| Missing/unsupported evidence | Named requirement, current owner and permitted repair; an existing PDF awaiting support is not a missing document |
| Saved correction | Confirmed saved state, affected outputs Out of date and separate explicit continuation |
| Review accepted/report pending | Review recorded; report completion pending, with receipt-based recovery if required |
| Busy | Explain another same-workspace execution is active; preserve safe draft and current status, never queue hidden work |
| Uncertain save/provider outcome | Explain what cannot be confirmed and the guarded next step; never promise no charge or safe replay |
| Historical/out of date | Original revision/source/cutoff visibly labeled and still readable; stale state-changing actions blocked |
| Report generated | Actual current artifact and distinct recorded decision/conditions; no implied real approval, fulfillment or funding |
| Technical failure/budget stop | Specific safe reason, saved partial work and permitted next action; no credit Reject label |

Partial/unregistered uploads cannot display a complete score or PanelDecision without the agreed prerequisites. Native RAGAS results use their metric status/scale; an unrun score is absent with a reason, not a measured zero. These quality diagnostics live in the existing Activity instructor/developer expander, not ordinary financial risk cards.

## Dashboard layout

Screen 1 uses [dashboard-redesign.md](dashboard-redesign.md): five KPI controls,
attention queue, then two rows of three bordered native cards on desktop. Reuse
navy, blue, slate, focus styling and typography. Mobile stacks columns; wide tables
scroll within their panel. Tablet uses native Streamlit reflow rather than a custom
two-column component. Status text always accompanies color. Missing values and
AI recommendations stay distinct from recorded financial decisions.

## Financial content, citations and explanations

Public references follow accepted ADR-007 and the source contract: label company/document type, agreement date or reporting period and retained snapshot identity. Use real HTML heading/clause/table/row/span locators rather than invented page numbers; distinguish retained snapshot from the original URL, whose current content may differ. Public-source ingestion/index status and retrieval relevance are not credit-risk or approval status. Source inspection runs no crawl, embedding or model. Existing citation controls/state tokens apply; implementation and rendered checks remain pending.

Amounts identify USD and use thousands separators. Ratios show units such as1.15× and percentages such as60.00%; numeric columns align and use tabular figures where available. Display rounding follows FIN-1.0 and never controls policy/band decisions. Exact operands/unrounded boundary context remain reachable. Missing/Not assessed/Insufficient Data includes a reason; it cannot look like0 or a low-risk result.

Every material fact/finding/rationale/condition/policy detail has a visible descriptive reference. Source details show actual document/version/page(s)/passage and qualifications; computed numbers show formula plus operand sources; policies show exact version/predicate/applicability and borrower input refs; authored assessments/corrections show their real attributed origin. Conflicts expose both sides and selected/excluded reasons. A missing highlight uses truthful text/location fallback, never invented coordinates or a decorative link. Inspection does not mark support complete or clear a gate.

What does this mean? help is fixed trusted copy available by keyboard/activation, not hover only or a new LLM. Use the definitions in SPEC-010/FIN-1.0: DSCR, equipment LTV, model confidence, policy exception, source support, simulated review and report completion. Narrative describes supported findings/uncertainty and next action; no hidden chain-of-thought or unsupported connecting facts. Source period/subject and review-as-of/cutoff remain distinguishable. Annual-only, covenant-not-evaluated and deferred EBITDA reconciliation limitations appear in relevant details/report.

## Accessibility and verification

Verify labels, keyboard order/activation, visible focus/return, clear status announcements, non-color cues, long labels/content, supported reflow/zoom and contrast on actual components. Safe fields remain after recoverable errors and scope changes explain draft invalidation. Do not claim compliance or external-user validation from proposed tokens, color calculations or AppTest.

Use existing TEST-010/012 checks and UX-T01–05 with outcome/duration/help/error records. M4 implements the actual component behavior, M5 verifies local teaching artifacts; M1 approval starts only the foundation. A design deviation caused by a real framework limitation is documented with its user impact; retain the approved hierarchy/meaning and avoid introducing another UI framework without a justified scope decision.

All actual rendered/usability/accessibility results remain Not run. Proposed token values and illustrations are not observed application output.

## Plain-language interface labels

Use Demo mode - saved AI responses, review attempt, review history, and required checks and approvals. Internal status, role, evidence, annual-basis and check codes remain unchanged; translate presentation only through ui/labels.py. Evidence verified by reviewer refers to evidence support, never credit approval. Keep source citations and rule predicates available. Hide hashes, raw records, calculation versions and report-format diagnostics in collapsed Technical details. Explain DSCR, EBITDA, collateral, covenants and LTV in Financial terms explained. Preserve simulated-role disclosures, independent blockers and exact stored history.

## Educational demo and execution mode

Educational describes intended use, not whether a model is called. Label current saved-response reviews separately from planned live Nebius testing. The global shell currently shows Current mode: saved AI responses and Live AI testing: setup pending. Current review activity reports zero calls only for that saved-response review. Live mode must not be displayed until actual provider-backed graph execution and per-run provenance/usage are connected. The live demo has two model stages (extraction and synthesis); deterministic policy, scoring, routing and report assembly remain Python. Credentials alone never select a live mode or authorize a dispatch.

Live AI setup and its explicit readiness check belong only in a collapsed sidebar section, accessible across pages. Do not duplicate setup controls in the dashboard, New Deal or other main-screen content. Readiness remains an explicit non-dispatch action.

Live AI reviews use a separate sidebar Review mode selection. The mode banner must match the selection. New Deal explicitly starts the bounded live example; Review Workspace separates evidence verification from credit decisions and explicit Analyst continuation. Quotes and all checks begin empty. Source versions/pages remain inspectable. Live and saved-response histories are labeled separately; do not fill one with the other.

Use plain-English sample names in scenario menus, headers, dashboard/run selectors, action buttons and citation labels: Standard Deal, Missing Information, Policy Exception and Rejection Example. Map labels only through ui.labels.case_label; preserve the original scenario IDs, evidence handles, saved reports and source documents for provenance and callbacks.

The saved AI recommendation card displays the selected response's existing concise rationale beneath its decision. Keep the saved-response/not-human-decision disclosure and a collapsible source-check section with exact existing rationale references. A recorded confidence-triggered review explains the configured 0.70 threshold; never imply the numeric confidence is calibrated or a human approval. Do not generate new reasoning, truncate material qualifications, change the original AI response or relax review gates for this presentation change.
