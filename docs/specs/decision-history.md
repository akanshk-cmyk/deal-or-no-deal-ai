# Decision History — Cross-Deal Review and Audit Export

**Correction events:** SOURCE_CORRECTION_SAVED records original missing fact and
registered reviewer correction, reason/source/UTC and superseded parent. CORRECTION_APPLIED
records the explicit Update request, not an invented completed-analysis event.
READY and UPDATED_FINDINGS_REQUESTED remain distinct from final execution/credit
decision. History filters/timeline/CSV expose old/corrected facts and source refs.
See [CORRECTION-1.0](source-correction-integration.md).

**E-P01:** CONDITION_DRAFT_PREPARED, CONDITION_SUPPORTED and CONDITIONAL_APPROVE
retain comments, role, UTC, original snapshot and evidence/gate binding. Human
CONDITIONALLY_APPROVED differs from COMPLETED execution and OUTSTANDING condition.
Filters/timeline/CSV retain these events and condition record. See
[CONDITIONAL-1.0](conditional-integration.md). No fulfilment action is available.

**Exception events:** financial EXCEPTION_DISPOSITION captures actual RiskManager,
reason, rule/issue, RECOMMEND_REJECT, selected source/calculation/policy refs and
previous gate version without changing credit status. It is filterable and included
in timeline and all-filtered CSV, with explicit handling/rule/issue/ref columns.
Original event snapshots are retained separately from compact graph receipts.

**Current implementation status:** See [../implementation-status.md](../implementation-status.md). Earlier milestone progress paragraphs below are historical and superseded for implemented capabilities; requirements and safety boundaries remain active.


**Authorized completion refinement:** Add financial-history filters and pagination
to the main six-screen app using frozen financial events only. Scope every record
before counting; search deal/borrower/reviewer, action/status and inclusive UTC
dates. Export all filtered rows, not just the page, with a rechecked snapshot digest.
Keep original event details and an independently unfiltered deal timeline.
Use the existing database and CSV format; no new PDF dependency or graph call.
Legacy borrower/amount metadata absent from an event snapshot stays Not captured;
new events may capture actual extracted terms in their original snapshot.

**Financial integration:** FIN-REVIEW-1.0 now reads actual financial comment,
request/response and decision events, with frozen AI/risk/final policy/source
snapshots and status/reviewer/UTC attribution. It excludes illustrative events.
CSV export scopes before content and rechecks snapshot identity, using formula
neutralization and explicit prepare/download. Historical corrections append;
ordinary UI commands cannot edit old events. SQLite is not immutable storage.
Financial search/filter/pagination UI now reads actual scoped financial events;
the independent preview remains separate. CSV covers all filtered pages; PDF stays
deferred. New event borrower/amount metadata comes from the exact pre-action run;
legacy missing metadata is not filled from current analysis.

**Financial execution integration (2026-10-24): [APP-READ-1.0](financial-command-center-integration.md) exposes actual run events in the root app and explicitly reports no human credit decision. Stage completion is not approval. Separate illustrative history retains filters/frozen context/CSV. Financial credit-decision integration/export still requires the financial review adapter; full SPEC-013 acceptance is not claimed.**

Feature ID: SPEC-013  
Contract: DECISION-HISTORY-1.0 / DECISION-SNAPSHOT-1.0  
PRD requirement: FR-021; related FR-010/014/020  
Date: 2026-10-24  
Status: User-authorized implementation specification

## Outcome and boundaries

Add a sixth dedicated Decision History page to the planned Financial Deal Review application. The user's explicit request supersedes the previous five-screen limit for this feature only. Implement the page in the existing local preview first, alongside Human review, with a reusable Streamlit component and read-only service using the same SQLite records/history. No new database, dependency, provider request, inference, source registration, real approval authority or schema migration. The preview remains ILLUSTRATIVE_UI_ONLY; financial pipeline/complete lifecycle-event integration remains pending. Do not fabricate uploads, agent starts, reassessments or historical credit decisions from the user's illustrative timeline.

All five existing simulated roles may inspect/export only their configured workspace/allowed-deal scope. This explicitly authorizes CSV export of the same scoped data visible to that role; it grants no financial action permission. A Risk Manager in the user's illustrative example does not acquire final Reject authority. Reviewer names are trusted demo display labels, not verified identities. Do not add a free-text identity or admin scope-bypass control.

## Page behavior

1. Show a chronological decision/status-change dashboard, newest first by default, including comments as unchanged-status audit actions. Columns expose exact UTC time, deal ID, borrower, amount/currency, deal type, reviewer name/role, previous/new status, current deal status, action and reason/comments. Missing captured fields display Not captured, never invented amounts, zero risks or a fabricated identity.
2. Filters: deal ID substring, borrower, reviewer name/ID/role, action type, event status and optional inclusive UTC date range. Show active filters, total matched records and page size/page navigation. Filter before counting/pagination and never reveal excluded deals' counts. Stable timestamp/sequence/event-ID ordering. Invalid/reversed date ranges show a clear error and no export.
3. Selecting an event opens its original comments/requested items, transition, reviewer identity/tier, analysis revision/basis, AI recommendation/version, risk assessment, compliance findings, policy exceptions and captured supporting-document details. Render untrusted text inertly; never interpret arbitrary paths/URLs or call an agent to reconstruct history.
4. Selecting a deal opens its complete recorded review timeline, oldest first, independently of dashboard filters. Every event has a clickable View event details action. A pagination/size limit must be explicit; no silently incomplete 'complete' timeline. Show the current adapter's review-action-only coverage; submission/AI-execution events are not connected yet.
5. CSV audit export includes all matched authorized events across pages, not just the visible page. Bound a single export to5000 events and require narrower filters above that limit rather than truncate. Prepare bytes only on explicit request; browser download is local, with no email/upload or paid service. Recheck permissions and the exact filtered dataset digest before preparing; changed results require refresh. Include provenance, historical versus current statuses, source/context snapshots and export UTC time. Quote CSV fields and neutralize spreadsheet-formula prefixes without modifying stored comments. PDF is deferred; CSV satisfies the requested 'CSV or PDF'.

## Historical snapshot contract

Extend newly recorded review events atomically with previous_status, a monotonic per-request event_sequence, trusted simulated reviewer_name and DECISION-SNAPSHOT-1.0. Snapshot the event deal ID, borrower_name, loan_amount/currency, deal_type; AI recommendation/analysis version; risk assessment; compliance findings/policy exceptions; supporting documents; and existing revision/basis lineage. Source these from the trusted pre-action record, not the command/form or latest analysis. Unknown values remain null. New UI samples may have clearly illustrative borrower labels/type but no invented financial amount, AI recommendation or risk finding. Original PanelDecision is never changed by a human action.

Existing events are not rewritten. For legacy records, read the exact expected_record_version from app_record_history to recover the actual pre-action status/context where retained; otherwise mark Not captured with source LEGACY_NOT_CAPTURED. A later record/title/context update must not alter historical event snapshots. Current deal status is a separate explicitly labeled read-time projection. Reviewer names not captured historically stay null; a role is not silently converted into a person's name.

## Service and data contracts

- query_decision_history(Store, Actor, HistoryFilters, offset, limit) -> snapshot digest, authorized match count, page rows, scoped deal list. Use a read transaction for one consistent request/event/history snapshot. No initialize/write on read, import, filter, timeline or export; a missing database returns empty.
- get_deal_timeline(Store, Actor, exact_deal_id) -> complete authorized saved review events, ascending. Wrong workspace/deal/unknown role denied; above5000 events explicitly blocked for bounded educational review.
- export_decision_history_csv(Store, Actor, HistoryFilters, expected_digest, clock) -> UTF-8 CSV bytes and safe metadata. Requery/recheck scope and digest; no arbitrary row payload supplied by UI. No automatic export cache across actors/scopes/filter changes.
- HistoryFilters strictly validates bounded text, known actions/statuses, date types/order and sort direction. Page size1–100 and nonnegative offset; resource limits are explicit, not semantic filtering.

Use existing app_records/app_record_history. New event snapshot keys are application metadata, not an expanded model wire. Read transactions perform SELECT only and preserve checkpoint ownership. The global active execution guard still protects review writes; history stays readable without spending model budget. Local records are versioned history, not cryptographically immutable audit storage. No expiry/reset/delete.

## Acceptance and evaluation

TEST-013-01: all roles/scopes, denied cross-deal/workspace reads/exports and no count leakage.  
TEST-013-02: exact previous/new/current status, reviewer name/role, UTC time, original context retained across later changes; faithful legacy handling.  
TEST-013-03: all filters/date boundaries/order/pagination, empty/invalid states and no hidden truncation.  
TEST-013-04: complete deal timeline and selected event details with unknown versus captured risk/AI/source context.  
TEST-013-05: scoped all-page CSV, exact dataset identity, stale export rejection, missing-field representation, formula neutralization and no writes.  
TEST-013-06: Streamlit page navigation, filters, timeline clicks/details, permission-scope changes and explicit export preparation.  
TEST-013-07: unchanged original case/prompts/budgets/checkpoints and existing human-review regression.  
Application/UI tests are not model evaluation, manual accessibility verification or financial lifecycle completion. Reuse MET-09/15/19 reporting with raw results; no financial-quality threshold is changed.
