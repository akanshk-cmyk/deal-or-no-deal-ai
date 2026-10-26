# Uploaded workflow acceptance completion

## Shared uploaded-data population

Explicit AI-review request: for Cedar Vale, separately store AI_EVIDENCE_REVIEW
metadata with request/target digests, source quotes, AI provenance, timestamp and
AI_SUPPORTED / AI_FLAGGED / AI_NEEDS_INFORMATION results. These are Codex-assisted
source checks, not human receipts or a paid independent evaluator. They display
beside the selected target and in an AI-review table, without selecting/checking
human inputs or resuming the graph. Existing human events remain unchanged.

Policy/risk follow-up: the preliminary projection now calls the existing sample
policy handler and risk-flag aggregator on the same scoped extracted inputs.
Show all configured rule results with predicate, value, threshold, applicability
and sources. Unknown applicability, unverified financial evidence and absent
synthesis remain Unknown/not evaluated. Do not treat zero numerical exceptions
as completed policy clearance. Preliminary passes are labeled only as no breach
on extracted data. Policy version and formulas are unchanged.

Show numeric exception risk flags and the five missing borrower-factor assessments;
never derive a composite credit score from ratios or copy sample ratings. The
composite remains Insufficient Data for Cedar Vale. These projections populate
every screen/role and the Compliance/Risk tabs before graph verification. Recorded
graph stages, human support and decisions remain untouched. Actual graph-produced
results take precedence after specialist execution.

The user's follow-up explicitly requests calculations from uploads across all
screens and roles. Add a read-only preliminary arithmetic projection using the
existing Decimal kernel on the actual retained extraction. Revalidate source,
borrower, scope and basis bindings first. Display UNVERIFIED extraction-based
results separately from recorded specialist artifacts; do not persist synthetic
stage events, mark fact review complete, execute policies/synthesis or clear
readiness. Unknown policy applicability stays unknown; LTV may display arithmetic
only with that qualification. Missing/invalid operands retain kernel statuses.

The same preview is available on New Deal, Dashboard, Workspace, Agent Activity,
Memo and Decision History to all five permitted roles. Once the financial stage
has executed, its recorded results remain authoritative and the preview is hidden.
Widget data never carries between deal/review digests. Users still explicitly
verify evidence and make credit decisions within their permissions.

Observed validation: one Streamlit integration test checks all 30 screen/role
combinations with a different borrower and DSCR1.75, no extra provider calls,
no changed graph state and rejected out-of-scope access. Thirteen regression tests
and31 subtests pass for finance, evidence feedback and live review UI. Read-only
Cedar Vale calculation produced DSCR1.50, LTV60%, EBITDA800000 and Debt/EBITDA3.00;
these are unverified preliminary arithmetic, not a completed live graph journey.

The user clarified that automatic population applies across screens and roles,
not only the reporting form. Display actual extracted financial inputs, periods
and references in Financial Analysis even while the graph awaits verification.
Keep calculated results explicitly pending until their nodes execute. Saved
reporting declarations are readable by all permitted upload-library roles.
Source-quote boxes prefill with the selected deal's exact cited page text, editable
to a narrower continuous quotation. Widget identity includes the review-request
digest to prevent values/checks carrying between deals or revisions.
Prefill never creates HUMAN_SUPPORTED, checks boxes, selects an assessment,
accepts a condition, approves a deal or resumes a graph. No model call on render.

## Reporting-basis prefill

Evidence form feedback follow-up: before submitting support metadata, identify
missing status/comments, source quotes and required checks. Supported assessments
require a continuous exact quotation from every cited source and all stage checks.
Withheld/unsupported assessments may cite only the relevant nonempty sources and
do not assert that every check passed. Backend scope/version/role/source checks
remain authoritative. Do not save support or resume automatically. Four focused
form/UI regressions passed without provider requests.

Save-lock correction: saving a declaration is an atomic metadata transaction,
not a model/graph execution admission. It may proceed while an unrelated AI
attempt requires recovery, without changing that attempt's lock or allowance.
Recheck profile version and started-review binding inside the transaction;
record a scoped timestamped UPLOAD_PROFILE_DECLARATION audit entry. Unchanged
duplicate saves are read-only. Analyst/upload access checks remain required.
The separate Run action continues to enforce the global execution lock.
Observed validation: six focused tests passed, including saving during an
unrelated recovery lock, duplicate saves, role checks and frozen started profiles.

Stale-session follow-up: initialize previously blank upload-scoped form fields
once per prefill version, preserving existing nonblank edits. Provide an explicit
Refill from uploaded documents action to restore this package's cited suggestions;
reset confirmation, do not save or call a model. Unrecognized/conflicting values
remain blank. A fresh Streamlit session must display the current compact form.

Compact UI follow-up: retain the backend-used identity, review date, current
annual dates/type, transaction date and three policy-applicability settings.
Group related inputs in columns. Collapse optional comparative annual dates
(used for revenue growth) and source-suggestion details. Prefill remains local,
editable and upload-specific; saving still requires explicit confirmation.
No backend field, policy requirement, existing declaration or checkpoint is
removed by this layout change. Unknown applicability is never guessed.

The user authorized auto-filling Step 2 to reduce typing. Local, conservative
text matching suggests explicitly labeled borrower, ISO transaction/review dates,
annual projection spans and comparative calendar-year projection periods only
when those boundaries are explicit. Each document-derived suggestion retains
its uploaded page reference and quote. Conflicting values remain blank. Missing
values are never copied from a saved example or another deal.

Review date defaults to the UTC upload date only when no explicit review date
is present; the UI labels this as a default, not a documented date. The reviewer
can choose a historical date. Saved declarations take precedence over suggestions.
Policy applicability stays Unknown unless explicitly saved by the reviewer.
All fields remain editable; confirmation and Save are still required. Existing
started-review profile locking and evidence checkpoints remain enforced.
Prefill performs no paid/model call and is not verified extraction or approval.
Implementation: profile_suggestions.py and ui/upload_intake.py. Validation:
tests/unit/test_profile_suggestions.py and the existing Streamlit form test.

User authorized fixing the three acceptance gaps. Preserve historical exact-
profile/saved paths and their immutable-in-application snapshots. No new
dependencies, business thresholds, factor-to-score rules or budget increase.

New synthetic text-PDF packages use their own page inventory, Deal ID and
reviewer-declared borrower, review date, annual/comparative periods, transaction
date, USD whole-unit basis and sample-policy applicability. These declarations
are unverified, not institution-approved metadata. Unknown applicability remains
Unknown. Do not borrow registered facts, factor ratings, dates or scores.
Existing parser limits, direct full-page grounding and model caps still apply.

Extraction is live with the existing strict schema. Source/basis integrity is
checked and fact/profile verification pauses using LangGraph interrupt/resume.
Financial, compliance and risk specialists fan out in a subgraph and join before
synthesis. Each pure branch may recompute inexpensive deterministic inputs to
avoid cross-branch dependencies or concurrent SQLite/state/ledger mutation.
Only the joined parent persists the three outputs and settles their node/tool
usage. Risk flags use existing sample rules; missing authored factor assessments
mean no composite score, never the sample's Low rating.

Permit a clearly partial review memo despite missing score/policy information;
this does not permit approval. Synthesis references current panels/sources and
is followed by mandatory narrative evidence interrupt. Unsupported claims stay
paused/withheld. Effective readiness remains authoritative; no auto approval.
Missing inputs are null, never zero. Conditions/findings/evidence are preserved.

Explicit Run may use existing bounded one-output-token input sizing probes for
new packets, charged to the same USD0.10 allowance. No retries, paid calls on
render, hidden source truncation, saved-response fallback or default OpenAI API.
Large/unsupported/encrypted/scanned/mixed-subject inputs stop with a reason.

Tests: same previous acceptance suite plus new/re-exported/renamed/partial PDF
profiles, actual fan-out/join, strict human pause/resume, no inherited scores,
source/schema/basis checks, blocked readiness and same-ID memo/navigation.
