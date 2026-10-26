# Educational demo runbook

## Single uploaded-deal live demo — 2026-10-25

For human actions: Review Workspace -> uploaded deal -> Human Review. Enter
required comments. Analyst/reviewers may request specific information with
Mark Pending; simulated Authorized Approver may Reject or Approve when eligible.
Approve stays disabled until every required readiness check is satisfied.
Risk Manager/Compliance Officer use Verify evidence and covenant checks; do not
invent timing or record verification without inspecting evidence. Pending items
require Risk Manager response review before approval. Decision History records
all actions. Credit Memo offers the original draft and a separate download with
subsequent review history. See [details](evaluation/uploaded-human-decisions-results.md).

New Deal → Upload New Deal now supports the complete unchanged three-PDF Standard Deal package. Explicit Run performs fresh Nebius extraction and synthesis on retained uploaded content, with a distinct upload-derived Deal ID, source map, shared workspace/activity/history and draft memo. It does not use saved answers as live results. Other, partial or changed packages remain inspection-only. Approval readiness and unverified-draft safeguards remain; historical human-checkpoint reviews are unchanged. See [scope, steps and evidence](evaluation/upload-live-demo-results.md). This supersedes older blanket inspection-only statements only for that exact supported profile.

Browser-verified completed uploaded deal: `53d8e05e-126a-5c3a-872b-d089fb31bdae`
(dropdown suffix `Uploaded deal 53d8e05e`). To inspect without new spending,
select its retained upload package showing `0726711d` in the displayed package
label, then Open Review Workspace, Agent Activity or Credit Memo. For a new
upload demonstration, use all three PDFs in `fixtures/development/e-n01/sources`,
confirm synthetic data, Validate and inspect uploads, then explicitly Run.


## Approved Phase 1 demo update — 2026-10-25

The user approved the [live demo-draft contract](specs/phase1-live-demo.md). New explicit Run actions use LIVE / DEMO_DRAFT. Extraction and synthesis call Nebius; Python performs calculations, sample policy checks, illustrative scoring, readiness and draft assembly. Technical integrity checks do not record human verification. Drafts cannot authorize credit approval. Existing HUMAN_REQUIRED reviews retain their checkpoints and original records. Saved examples remain available internally. No model calls on screen viewing and no fallback on failure. Phase 2 RAGAS/judge evaluation and optimization are deferred. This update supersedes older default-FIXTURE and pre-draft human-checkpoint statements only for new demo drafts. Functional evidence is recorded in docs/evaluation/phase1-demo-results.md (relative to repository root).


Prepared 2026-10-25. This is a presenter checklist, not a record that every task
below has passed. Use only synthetic documents and simulated roles.

## Present the completed live demo first

1. Open the existing Streamlit app and select Review Workspace.
2. Select Standard Deal / Example Equipment LLC and the latest completed live
   review (2026-10-25 about 5:27 PM Pacific). Technical operation ID:
   `e822bbb5-20d0-438a-a74a-2b4c2c0cd69a`.
3. Show extracted terms, DSCR 1.50x, sample policy checks and illustrative risk
   21/100. Use the Evidence explorer to inspect source pages.
4. Show effective Pending Review, mandatory covenant evaluation incomplete,
   human evidence verification not recorded and no human credit decision.
5. Open Agent Activity for recorded handoffs, Credit Memo for the downloadable
   unverified draft and Decision History for the preserved timeline.
6. To perform a new paid demonstration, choose New Deal, simulated Analyst,
   Standard Deal and explicitly click Run AI Deal Review. Do not click Run merely
   to show an existing result. Failures never substitute saved answers; retain
   the operation ID for diagnosis and do not reset the database or cost ledger.

This successful functional journey is not a quality benchmark or proof that
every future model output will validate. Two earlier actual summary outputs
failed; their records are retained. See [Phase 1 results](evaluation/phase1-demo-results.md).

## Historical preflight and interrupted attempt

Before presenting, run the read-only local preflight:

```powershell
.\.venv\Scripts\python.exe tools/check_demo_readiness.py
```

It reports the configured source, execution lock, retained allowance reservation,
live synthesis/report availability and saved-answer evaluation status. It does
not load credentials, call Nebius, clear recovery or record evidence support.
`NO_ACTIVE_EXECUTION_LOCK` alone is not permission or proof of live readiness.

To start a local presentation, use the existing application command:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
```

If its port is occupied, do not stop an unknown existing process. Check whether
the existing app is the intended checkout, or use an explicit available local
port, for example append `--server.port 18765`. The follow-up browser rehearsal
used that port because 8501 and 8502 were occupied. Starting or viewing the app
does not start inference; retain the existing saved-source configuration until
the recovery and live-review prerequisites have actually been resolved.

The interrupted review started at **2026-10-25 00:35:33 America/Los_Angeles**
(07:35:33 UTC). It selected Qwen/Qwen3-30B-A3B-Instruct-2507.

- Local review: `aab508af-564d-461f-a4e7-cf0708ec29b6`.
- Local extraction request: `59a0ab09-1779-56f3-b0f8-1ecefea14993`.
- Reserved maximum: USD0.0007. Actual usage and response are unrecorded.
- The local request reference may not exist in Nebius logs; it is not a verified
  provider request ID. A timestamp/model match alone is not conclusive evidence.

The user-approved administrative quarantine has been applied. The shared local
execution claim is released, but this exact attempt cannot restart or dispatch.
Its original progress, checkpoints, ledger and USD0.0007 uncertain reservation
are unchanged. This is not usage reconciliation, evidence of zero cost or a loan
rejection. Matching provider evidence can be reconciled separately if available
later; do not reset the database, remove the reservation or replay the request.
See [activation and integrity evidence](evaluation/quarantine-results.md).

The user subsequently confirmed that the matching provider record is still
unavailable. The approved quarantine allows other reviews to proceed without
pretending that usage is known. New live generation is limited to three submitted requests per review
(initial calls plus any explicit corrections), with no automatic retries. Cached
results consume no extra request; changing a request ID cannot reset the count.
This is distinct from offline RAGAS's existing judge/embedding call limits and
does not increase the shared USD0.10 allowance. Human fact and narrative support
remain required even after technical recovery. Merely reducing retries cannot
recover an absent response or establish unknown token usage.

Refresh the app, open Review Workspace and click **Open live review awaiting fact
verification** on the set-aside attempt. Select the **Risk Manager** demo role and
open **Human Review**. The actual root UI was checked: this navigation and the
verification form work without provider calls or database changes. It records no
support merely by opening the form. Resume the existing valid review; do not
start a replacement extraction or increase the paid allowance.

## Six-screen presenter walkthrough

| Screen | Show | What to explain |
| --- | --- | --- |
| Deal Dashboard | Actual deal status, exceptions, source label and next action | Execution completion is different from credit approval. Earlier attempts are not extra deals. |
| New Deal | Sample/upload intake, package checklist, one Run AI Deal Review action | Current configuration chooses saved answers or live inference. Browsing makes no call. Uploads are inspection-only. For the live walkthrough, resume the existing valid extraction rather than starting another. |
| Review Workspace | Overview, terms, financial analysis, compliance, risk and Human Review | Open source citations and inspect the calculation basis. A low score cannot override a mandatory blocker. |
| Agent Activity | Recorded stages and scoped evaluation report | Some steps use Python, not LLMs. Saved-answer evaluation is not live-answer evaluation. |
| Credit Memo | Preserved source-linked memo and current readiness | The original AI proposal, effective readiness and human decision are separate. Historical memo text is not silently regenerated. |
| Decision History | Reviewer comments, timestamps, source and prior decisions | Evidence assessments do not approve credit. Simulated role attribution is not real authentication. |

Saved examples available through permitted actions or existing records:
Standard Deal (Pending Review because covenant evaluation is incomplete), Missing
Information (no invented complete score), Policy Exception (specialist/conditional
path), Rejection Example (case-specific supported rejection), and the registered
source-backed CFADS correction. Follow actual role prompts; no generic waiver.

## Complete the actual live journey

1. Administrative quarantine is already applied. Confirm preflight shows no active
   execution lock; retain the unknown reservation and abandonment audit trail.
2. Select earlier live review `46802df1-4f6b-435d-895e-61576fca3d9b` in
   Review Workspace / Review History. Do not start a fresh paid extraction.
3. Simulated Risk Manager reviews all 36 fact targets, exact source quotations,
   reporting basis, units, borrower/facility and required checks. Record comments
   and support or withholding. The prepared guide is
   `var/evaluations/live-fact-review-required.md`; reading it records no support.
   The [actual AI fact-judge diagnostic](evaluation/live-fact-judge-results.md)
   covers all 36 targets and flags five citation issues. Use it as an aid, not
   as human support. The readable local report is
   `var/evaluations/fact-judge-1fb7eaa9-9fef-5454-8617-34778101b82f.md`.
4. Analyst explicitly continues after all required facts are supported. The
   actual prepared synthesis request must have exact token-count evidence before
   dispatch. A configuration pause is not permission to substitute a sample.
5. For that exact prepared packet, the existing technical verification command is:

   ```powershell
   .\.venv\Scripts\python.exe tools/verify_live_input.py --stage synthesizer --operation 46802df1-4f6b-435d-895e-61576fca3d9b
   ```

   This is a paid one-output-token probe, not a free readiness check. Execute only
   after the preceding gates, within the shared USD0.10 allowance and applicable
   environment permissions. Then Analyst explicitly continues the existing run.
6. Required Risk Manager / Compliance Officer reviewers inspect actual narrative
   claims and citations. Unsupported claims stay unresolved. If a separate credit
   gate is routed, only the permitted Authorized Approver may act; readiness must
   permit approval. Never turn fact support into a credit decision.
7. Analyst continues to report generation when permitted. A memo may retain
   Pending Review readiness and unresolved covenants; do not force Approve to
   make the demonstration look complete.

## Evaluate the actual live answer

After actual synthesis exists, prepare its frozen evaluation sample without calls:

```powershell
.\.venv\Scripts\python.exe tools/evaluate_deal.py --operation 46802df1-4f6b-435d-895e-61576fca3d9b --reference docs/evaluation/examples/e-n01-answer-reference.json
```

Check source lineage and reference applicability. The explicit `--run` option
then executes the bounded paid RAGAS evaluation. Preserve original context versus
independent reference, unknown-cost reservations, failures and any explicit single
correction. Do not use another deal's saved answer to fill an absent live answer.

Record native scores, applicable/not-applicable statuses, custom rubric examples,
actual token cost and limitations. DIRECT precision remains not applicable. Judge
disagreement and an unsafe original approval proposal require examination even
when a custom rubric scores highly. COMPLETE means evaluator execution completed;
it does not mean every quality target passed or a loan is approved.

## Operator rehearsal: record observed results

Automated preparation now has [separate evidence](evaluation/demo-preparation-results.md):
30 read-only screen/role checks passed, and the database and provider-call counts
were unchanged. These do not complete the manual keyboard/zoom and submission
tasks below. The versioned offline walkthrough is
`prototype/demo-2026-10-25.html`; the original snapshot remains preserved.

All items below are **not yet recorded as completed** in this runbook.

- [ ] Identify the deal needing attention and explain its next required action.
- [ ] Trace one extracted fact and one calculation to the original source/page.
- [ ] Inspect a policy predicate, observed value, result and outstanding covenant.
- [ ] Record a permitted evidence review; verify an unauthorized action is blocked.
- [ ] Resume the same live review, inspect the memo and trace the decision history.
- [ ] Inspect a saved RAGAS report and distinguish it from a live report.
- [ ] Navigate by keyboard, check focus visibility and inspect at 200% zoom.
- [ ] Download the memo and existing scoped financial CSV; describe export scope.
- [ ] Confirm refreshing/navigation makes no provider call or duplicate decision.

Record operator, date, observed result and problems. Do not invent usability scores,
business savings, real banking compliance or production-readiness claims.

## Demo evidence to retain

One actual live extraction and synthesis, evidence-review receipts, checkpoint
continuation, source-linked memo, applicable human decision or explicit Not
recorded status, live RAGAS report, usage ledger and completed rehearsal notes.
The current saved walkthroughs and offline regression remain separate proof;
see the latest test counts and timeout rechecks in the quarantine results.

Deferred: semantic VECTOR/HYBRID benchmark, generic uploaded-loan analysis,
fresh-kernel notebook execution (installation deferred), PDF audit export,
real identity management, external crawling and deployment.
