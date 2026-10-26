# Deterministic Credit Memo and Draft Preview

**Correction provenance:** CORRECTION-1.0's corrected-profile memo requires a bound
reviewer correction record. Summary/audit identify original missing CFADS, restored
USD900000, basis/page, reason, reviewer, UTC and event ID. The original model response
is not rewritten or relabeled successful. Seven sections, citations and source-bound
checks remain; Approve recommendation is not human approval. See
[contract](source-correction-integration.md).

**E-P01 report:** [CONDITIONAL-1.0](conditional-integration.md) independently checks
exception/draft/domain-support receipts and accepted targets. Seven sections retain
original Exception and AI, separate human decision and source-backed condition as
OUTSTANDING / Unassigned / EXTRACTED_NOT_EVALUATED. Report completion is not condition
fulfilment or funding readiness. Existing normal/Reject memo records are unchanged.

**Financial reviewed fixture:** FIN-REVIEW-1.0 independently validates the accepted
own receipt and remaining gates before rendering the seven original sections.
E-N01-REVIEW-MEMO-1.0 preserves the original confidence/referral and AI proposal,
adding actual simulated human decision/comments/reviewer/time/event identity.
Normal renderer/old memos remain unchanged. Reviewed generation time is actual
report time, not the pre-human-wait start time. Revision2 creates a new report.

Feature ID: SPEC-009
Version: 1.11
Status: Registered saved paths and live report integration implemented; saved memos executed; actual complete live memo pending human review and deferred recovery
PRD requirements: FR-009, FR-016–020
Role instructions: [Memo / Report Generator](../agents/report-generator.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

A reviewer reads one consistent seven-section report, with facts, gaps, original recommendation, review disposition and audit cutoff. Rendering is pure Python; no report-writing LLM, external write, email, automatic export or new inference.

The [RAGAS evaluation report](../evaluation/evaluation-report-template.md) is a separate quality artifact. Its four native metrics and five custom ratings are not financial risk scores and add no credit-memo section or inference to this renderer.

The existing screen-level summary follows [CX-1.0](command-center-ui.md#first-use-review-effort-and-completion-experience--cx-10): show the recorded outcome, unresolved blockers/conditions with owner, and the permitted next action. Review recorded and Report generated require their respective actual receipt/artifact; completion cannot imply funding or fulfilled conditions. The recap reads current records, remains outside report_markdown, and adds neither an eighth section nor new narrative generation. Existing TEST-009-03 and TEST-010-05 cover this refinement.

## Workflow and rules

Use a single pure renderer over a validated snapshot. Before required review is satisfied, a read-only on-demand preview may show known supported content and missing/blocked markers. It is not an executed final-report node or persisted current report. When valid review/no-review routing permits, report_generator returns report_markdown and report_metadata to graph state.

Sections in exact order: Executive Summary; Compliance; Financial Analysis; Risk Scores; Decision; Conditions; Audit Log. Copy validated upstream narrative/facts; deterministic linking sentences cannot introduce new conclusions. No aggregate risk score/PD is invented. Missing methods/values show Not assessed/Unknown.

Decision separates simulated PanelDecision, uncalibrated confidence, effective gates, and HumanDisposition when present. Direct branch states Not required by configured demo rules; never human approved. Conditions distinguishes contractual covenants, proposed follow-ups, exception handling and human changes. Preserve owner/next action and every unresolved mandatory issue.

SME resolutions: Conditions renders CONDITIONS-1.0's origin/category, owner or Unassigned, status, supporting references and linked existing-gate state. A completed simulated Conditional Approve review report may retain OUTSTANDING supported proposals; it cannot imply fulfillment or funding. Missing current CFADS or another mandatory source requirement remains a blocker, not a future condition that allows final completion. Preserve source clauses as EXTRACTED_NOT_EVALUATED, not covenant Pass. Human edits retain original text/history and supported links.

Financial Analysis names the supplied assessment period/subject/facility basis and fact-support mode. State Annual-period analysis; full-term/balloon/refinancing adequacy not evaluated and Reported/adjusted EBITDA reconciliation deferred. Preserve source repayment structure, maturity and use of proceeds without inventing forecasts or lifetime repayment conclusions. Data-quality support and actual underwriting disposition are separate recorded events; a Low/no-underwriting branch cannot claim no source review occurred. An unregistered upload's partial preview has no accepted PanelDecision and never a final decision-ready label. Keep exactly seven sections, reusing existing render inputs and scope markers.

The existing Human review summary line explicitly means Human credit review; source-support status/attribution remains separately available. Not required applies only to the configured credit-review route, never to all human work or semantic verification.

The existing Risk Scores section copies three independent current-revision assessments: RISK-EDU-1.0 credit score and SCORE-BANDS-1.0 band, policy exception count/status, and missing required evidence count/status. Show five supplied ratings/weights/contributions, material inputs, configuration/source versions, coverage and limitations in explanation; no calculation occurs in the renderer. Missing material factors/inputs give Insufficient Data with no total/band or reweighting. Configuration failures and undefined concentration remain distinct Not assessed states. The41 Moderate example is illustrative until backed by a scoped executed assessment, never PD or an automatic factor mapping. Coverage5/5 is not document completeness; score referrals cannot clear independent gates. Decision shows Python's required action/owner/review tier separately from any accepted current AI proposal and actual human disposition. Preserve current/incomplete/stale/history states, exactly seven sections and zero added inference.

Engineering refinements: an accepted review receipt is not a generated memo. RESUME-1.0/RUN-OUTCOME-1.0 require current permitted completion and the actual report artifact; stable report-operation identity prevents a second report/event on crash re-entry. STATE-UPDATE-1.0 explicitly clears affected current Markdown/metadata while retaining historical copies. COVERAGE-1.0 links every contributing source page and condition/qualifier; no fabricated single-page target. Original model proposal and human edits remain distinguishable for EVAL-CUTOFF-1.0. Keep the same seven sections and zero inference; refine existing report/recovery tests.

SOURCEFIT-1.0 adds the recorded review-as-of date, knowledge cutoff and source-selection/policy versions to existing report metadata/basis text, keeping seven sections. Material values cite selected applicable evidence; source details retain the scoped alternative/exclusion reason. A frozen historical report cannot be labeled current, and an unknown material date/authority cannot produce a completed recommendation. Updated review basis/profile/source selection invalidates the current report under the existing correction flow; retained historical reports remain clearly labeled. No eighth section, new inference, export or automatic expiry.

Director refinements preserve seven sections and zero model calls. NARRATIVE-CHECK-1.0 checks targets for rationale, conditions and action explanations as well as observation Claims; rendering cannot turn REFERENCE_CHECKED into semantic verification or hide an unsupported critical target. Supported human edits retain their own provenance/targets without rewriting the original model evaluation. SOURCE-TRIAGE-1.0 unresolved source reasons/owners remain visible independently from true missing-document/policy counts. A CONTINUE-CHECK-1.0 budget stop preserves the saved correction and historical report, but cannot publish a new completed report or financial Reject. Existing TEST-009-02/03/05 verify these states; no new section, field-specific report agent or universal credit-review gate.

## Contracts and data changes

Authorized E-N01 normal implementation slice, 2026-10-23: memo.py implements the pure seven-section renderer over the exact registered default inputs, fixture-checked synthesis/evidence, Python-owned no-review route and explicit recorded event cutoff. It exposes inline internal citation anchors and an exact source/calculation/policy/assessment index inside Audit Log. No external links/images/HTML from source text are executable. Values/conditions/routing are copied, not recalculated. Fixture semantics stay visibly educational; human credit review is Not required by configured demo rules and human disposition remains null. The report excludes its own later completion/checkpoint event. Different/unverified/currently blocked inputs are rejected; other scenarios/previews/UI actions remain future work. The orchestrated node returns Markdown/metadata; the explicit worker owns persistence/export of the local demo artifact.

render_memo(ReportInput) -> RenderedMemo, no I/O.
ReportInput: identity/mode/revision, validated terms/panels/synthesis/evidence references, issues/routing/review, condition records, explicit audit events <=cutoff, generation_time, template_version MEMO-1.0, render_kind PREVIEW/GENERATED/HISTORICAL.
RenderedMemo: markdown, section_index, citation_index, unresolved_issue_ids, metadata.

CITEVIEW-1.0 applies to every material memo claim/value/condition: show a descriptive inline reference from citation_index, not only an end-of-report bibliography. It opens the exact recorded source/rule/calculation/assessment/correction in Workspace and preserves the memo section/claim for return. A calculation exposes operand citations rather than pretending a derived number is quoted source text. A grouped source index may remain inside the existing Audit Log section; it does not add an eighth section or replace inline discoverability. Missing or historical/stale reference state is explicit. Rendering/navigation performs no inference or review-state change.
ReportMetadata: report_id, deal/run/revision, mode, source/artifact/template versions, audit_cutoff_sequence, generation_time, input_digest, render_kind, completeness COMPLETE/PARTIAL, supersedes_report_id nullable. Derive report_id deterministically from supplied identity/input digest/template/cutoff/kind, rather than creating a random identifier inside the pure renderer.

The node consumes explicit time/cutoff metadata, not hidden current time. Identical normalized inputs/template/kind produce identical content/digest. Repository projection persists the returned artifact after graph state update; renderer/node itself never calls a checkpointer or writes files/database directly.

Preview of a partial/blocked state is allowed if clearly incomplete. It cannot create a completed run, erase a block, invent a decision, or overwrite a generated artifact. Corrections mark old reports historical/stale; preserve lineage.

## AI and evidence behavior

Zero calls/tokens in both modes. Include references that navigate to exact source version/passage, formula and rule. Audit includes recorded upstream events only through cutoff; it cannot claim its own future checkpoint/completion or later review event.

## Authorization

Scoped read/preview for permitted personas; any review button calls the same SPEC-008 service. Generic acceptance is never a report-side bypass. Download/export remains P1 and must not have a misleading active button.

## UI states

Empty: no accepted state, show prerequisite/action. Loading: local rendering, not AI writing. Preview: conspicuous draft/partial label. Generated: mode/revision/cutoff and review status. Failure: safe missing-artifact/rendering error, preserve prior report as historical. Stale: visible superseded revision, no current-action controls.

Follow UX-1.0 in SPEC-010: the interface places three separate summary lines above report_markdown: AI recommendation (or Not generated with its reason), Human review (Pending/recorded disposition/Not required by demo rules), and Report status (Draft preview/Generated/Incomplete/Out of date). Show unresolved conditions/mandatory blockers, owner and the contextual permitted action. Source/version/cutoff metadata remains available in labeled Details. This is a view projection from existing records, not an eighth report section, a new conclusion, a renamed seven-section template or a claim that a completed report approves credit. Model confidence remains uncalibrated detail, not a gauge. Both Workspace and Memo call the same guarded action service.

## Reliability and stopping

Rendering errors preserve validated inputs and are technical stops, never Reject. No hidden retry/model fallback. Graph node and active time still count. Refresh/preview is read-only application rendering; it does not execute graph nodes or renew budgets. Renderer must reject incompatible snapshots rather than mix old/new values.

Treat embedded Markdown/HTML/URLs as untrusted: escape fields, do not enable arbitrary HTML, permit only internal source navigation and explicitly approved reference links. Do not render executable remote images/scripts from uploaded content.

## Analytics

memo_preview_viewed; report_generated with template/version/cutoff and completeness; report_superseded; source_opened. No report text in ordinary analytics. Report generation event is after the snapshot cutoff and may appear only in a later report version.

## Tests and acceptance

- TEST-009-01: Seven headings/order and required source/rule/formula/gap/owner markers.
- TEST-009-02: All numeric values/conditions/exceptions preserved; missing scores not zero. ConditionRecord provenance/owner/status and existing gates persist; outstanding proposals do not imply fulfilled covenants/funding. Annual-only scope and deferred reported-EBITDA reconciliation remain explicit; policy Pass cannot become covenant Pass. NARRATIVE-CHECK-1.0 covers rationale, individual conditions and proposed-action text; original AI versus edited targets remain distinguishable.
- TEST-009-03: Preview/generated/historical states and both review-route labels; UI summary separately represents recommendation, factual source support, credit review and report completeness. Unregistered upload stays partial with no PanelDecision; E-P01 may complete its simulated review with outstanding proposals, E-M01 cannot clear missing CFADS. Keep seven sections and never present a technical stop as Reject or source-support review as credit approval.
- TEST-009-04: Deterministic output from explicit inputs, accurate cutoff and supersession.
- TEST-009-05: Unsafe HTML/links rendered inert; cross-deal/stale source reference rejected. Material claims expose descriptive inline citation_index links to the exact recorded target and allow return to the memo claim; missing/highlight-unavailable states are honest. Formula/operand, policy, authored-assessment and correction references do not fabricate PDF citations; inspection has zero model/gate side effects.
- TEST-009-06: No provider/network/file/checkpointer side effects and no generic acceptance bypass.

Target: 100% template cases, zero report inference. At least one generated sample links to an executed run. Scenarios E-N01/N04, E-P01 and E-M01 as incomplete preview.

## Dependencies and implementation boundary

Consumes SPEC-003–005/008/011; used by SPEC-010/012. No report file, template implementation or sample executed output exists from this specification.
