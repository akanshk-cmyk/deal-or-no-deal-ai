# Uploaded single-deal live demo results

Scope: [approved implementation contract](../specs/upload-live-demo.md).
Educational prototype, measured 2026-10-25 Pacific. No RAGAS or Phase 2 quality
evaluation was performed.

## Implementation

New Deal / Upload retains and parses the uploaded PDFs as before. A complete
Standard Deal package is matched by PDF hashes and parsed page text against the
existing educational source profile. File names and order may differ. Matching
does not approve the deal or verify AI claims. Other/partial/changed documents
remain inspection-only; no unknown deal borrows the sample's scoring premises.

An explicit Analyst Run AI Deal Review uses a distinct upload-derived Deal ID,
operation, review and thread. The existing graph receives the retained uploaded
text and calls Nebius for fresh extraction and synthesis. Calculations, sample
policy checks, illustrative scoring, readiness and report assembly reuse the
existing Python services. No saved response worker is called as a fallback.

The context retains upload/package identity, digest and a logical-reference to
uploaded-file/page mapping. Revalidation occurs before execution, continuation
and source navigation. Memo and all screen projections share the same Deal ID.
No migrations, dependencies, formulas, thresholds, model settings or budgets
were changed. Historical contexts and original responses remain untouched.

DEMO_DRAFT remains unverified and cannot authorize credit approval. Historical
HUMAN_REQUIRED reviews retain their human interrupts. Mandatory covenant/evidence
blockers remain separate from the original AI proposal.

## Tests

- New uploaded-deal functional tests: **3 passed**. Actual PDF parsing with mocked
  provider responses; new identity, uploaded citations/memo, shared UI navigation,
  duplicate no-call retrieval, missing package, role/scope and byte replacement.
- Existing upload/live/saved/quarantine regression: **36 passed, 13 subtests**;
  `var/evaluations/upload-live-regression.xml`. An obsolete UI text expectation
  was updated to the new supported-upload message; no financial assertions were
  weakened.
- The real root workspace exposed duplicate Select Deal labels: opening another
  screen could select the original sample instead of the uploaded deal. Uploaded
  labels now include their distinct Deal ID prefix. A test containing both the
  original sample and uploaded deal verifies selection remains on the upload.

## Actual execution evidence

The first uploaded live execution completed ten stages with two actual Nebius
generation calls; root-workspace navigation was then fixed and rechecked without
additional calls. Evidence: `var/evaluations/uploaded-live-ui.json` (original
navigation failure retained) and `var/evaluations/uploaded-pages-check.json`
(successful corrected navigation).

An actual headless Edge browser also submitted the three PDFs through the file
uploader, confirmed synthetic data, parsed five pages and explicitly ran live AI.
Browser-created Deal ID: `53d8e05e-126a-5c3a-872b-d089fb31bdae`.
Operation: `9122dfaf-dcc7-5913-9792-029e11a312fe`.
Detailed browser/download measurements are in
`var/evaluations/browser-uploaded-demo.json`. Browser automation selector timeouts
were investigated separately from application/provider failures; the completed
analysis was preserved and reused for remaining presentation checks.

Final browser result: **completed=true**. Real file upload/parse, explicit live
Run, source explorer, same-deal Agent Activity, memo download and Decision History
passed. A second browser session resumed presentation checks against the same
completed review after correcting automation selectors; it did not rerun AI.
The browser-downloaded memo is retained at
`var/evaluations/browser-uploaded-credit-memo.md` (23,845 bytes); screenshots at
`var/evaluations/uploaded-workspace.png` and `uploaded-credit-memo.png`.

Observed successful browser review: two actual generation requests, 4,018 input
tokens, 1,109 output tokens, generation cost USD0.0007345 at configured rates,
ten completed stages. Approval readiness Pending Review; approval_eligible=false;
human_decision=null; report_kind=UNVERIFIED_DRAFT. All scoped Deal IDs match.
Result navigation left the paid allowance unchanged. Cumulative committed local
cost is USD0.0135178, with the unchanged historical USD0.0007 unknown reservation
retained under the shared USD0.10 ceiling. These are local accounted values, not
a reconciled provider invoice. This exact demo package completed successfully.

### Later runtime blocker found in final preflight

Resolved after explicit user approval: the newer attempt has been isolated,
its unknown reservation retained, and the execution lock released. No active
claim remains; completed uploaded reviews are unchanged. See
[activation and preservation evidence](new-demo-quarantine-results.md).
The following paragraph records the earlier observed blocker, not current state.

After the successful browser demo, a separate newer Standard Deal operation
`54b1dd19-7dad-4ead-b297-31aae29a0d86` appeared in RECOVERY_REQUIRED, started at
18:26:33 Pacific. Its extraction has no stored provider result and retains an
additional USD0.0007 reservation. New execution is currently blocked; the
completed uploaded deal remains available read-only. Do not claim fresh runs
are currently unblocked or clear this by restarting/resetting the app. See
[the concrete proposed isolation](../architecture/decisions/proposed-new-demo-quarantine.md).
The existing exact-ID quarantine authorization does not cover this new attempt.

## Presenter steps

1. New Deal -> Upload New Deal. Use simulated Analyst.
2. Select all three unchanged PDFs under
   `fixtures/development/e-n01/sources/`: agreement.pdf, financials.pdf and
   collateral-and-assessments.pdf. Confirm synthetic educational data.
3. Click Validate and inspect uploads. Inspect the retained source text and pages.
4. Confirm Complete Standard Deal source profile matched, then explicitly click
   Run AI Deal Review. This sends fictional data to Nebius within the existing
   shared allowance. Viewing/inspection alone makes no model calls.
5. Open Review Workspace, inspect findings/citations and the uploaded document
   citation map. Effective readiness remains Pending Review.
6. Open Agent Activity for actual recorded stages, Credit Memo to download the
   unverified draft and Decision History for the same deal's milestones.

To avoid another paid run, select the retained uploaded package or its distinct
Uploaded deal entry and open its completed review instead of clicking Run.

## Remaining boundaries

This completes one supported uploaded source profile, not general underwriting
of arbitrary companies/files or all four example scenarios in live mode. Risk
ratings remain authored educational inputs, not predictive default models. AI
semantic accuracy, general layout fidelity and reliability need the deferred
Phase 2 evaluation. The app does not record human verification or approval merely
because generation completed. Future obligations are not automatically breaches.

Main application changes: upload_live.py; live_context.py; live_worker.py;
live_demo.py; command_center.py; ui/upload_intake.py; ui/command_center.py; memo.py.
Supporting changes: uploaded/live tests and the linked specification/documents.
