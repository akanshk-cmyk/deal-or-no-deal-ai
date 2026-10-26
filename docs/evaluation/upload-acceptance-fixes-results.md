# Upload acceptance fixes and regression results

## Upload form usability follow-up

Moved optional manual evidence entry below the live workflow, collapsed long
parsed page text, added numbered steps and a disabled Run button with its
prerequisite explained. Missing required profile fields are named on save.
Streamlit regression verifies an unmatched retained PDF package can save its
profile with no manual financial entries, enable Run, and dispatch the existing
handler once. No paid call occurs in this test.

Observed: 7 tests and 10 subtests passed in 22.65s; evidence:
var/evaluations/upload-intake-usability.xml. This is a separate focused run,
not an additional distinct-case total for the earlier suites.

Date: 2026-10-25. Scope: functional Phase 1 demo; Phase 2 remains deferred.

## Changes

1. Added a reviewer-declared profile for new synthetic text-PDF packages, rather
   than requiring exact Standard Deal bytes. It binds borrower, periods, USD
   whole-unit basis and policy applicability to the retained upload digest.
   Declarations remain unverified until explicit specialist review. Missing
   comparative data stays missing. Unsupported currency/basis is stopped.
2. New uploaded reviews run the Financial, Compliance and Risk specialists in
   an actual LangGraph fan-out/join subgraph. Branches have disjoint outputs and
   no concurrent store writes. The parent records their outputs and usage.
3. New uploads require fact/profile and narrative evidence checkpoints before
   the report. A real source-binding defect in the verifier was fixed: it now
   checks the uploaded case, not the original sample identity.
4. Partial reviews can produce a memo without approving a deal. Missing factor
   assessments display Insufficient Data and keep approval ineligible. No sample
   Low score is inherited. Existing roles, latest-version approval checks,
   comments, Pending/Reject controls, citations and history remain separate.
5. Existing sample/historical contexts keep their original recorded policy and
   artifacts. No migration, new package, model configuration or budget change.

Main implementation files: upload_profile.py (new), upload_live.py,
live_context.py, services.py, synthesis.py, graph.py, live_worker.py,
live_demo.py, live_review.py, memo.py, readiness_service.py,
uploaded_decisions.py and UI upload_intake.py / command_center.py / specialists.py.
All paths above are under src/deal_or_no_deal_ai/.

## Observed offline results

| Test run | Observed result | Evidence |
|---|---|---|
| Same previous acceptance suite | 57 passed; 55 subtests passed; 225.30s | var/evaluations/upload-acceptance-audit-after.xml |
| General upload module, selected test_general names | 11 passed; 150.09s | var/evaluations/general-upload-tests.xml |
| Changed Python modules compile | Exit 0 | compileall |

The second run includes inherited compatibility tests; these counts are not
distinct cases to add together. Provider responses were mocked. Reviewer
support actions were created only in isolated test databases, never in the
actual application's audit store.

The different-borrower test parses an actual generated PDF for fictional
Northstar Widgets LLC: requested amount USD800,000 and calculated DSCR1.75.
It verifies its own source references and identity, two model-generation
dispatches, genuine graph checkpoint stops/resumes with test reviewers,
unscored risk, blocked approval readiness, a partial memo, and rendering of
Workspace, Agent Activity, Credit Memo, Decision History and Dashboard without
additional inference. A threading barrier verifies actual three-branch fan-out.
Other regressions cover unchanged sample calculations, upload tamper detection,
duplicate requests, authorization, pending/comments/rejection, controlled ready
approval and same-deal navigation.

## Acceptance assessment

The requested functional checks pass within the bounded educational upload
scope. This does not establish universal document support, live answer quality,
or production readiness. No paid calls or SEC requests ran during these tests.
A fresh end-to-end Nebius journey for the newly generalized profile still needs
the user's genuine fact/profile and narrative verification in the application.
No test-only reviewer actions may be copied into that live journey.

Existing limits remain: up to three synthetic text PDFs, ten pages and 10MB,
USD whole units, annual analysis, and approved token/spending caps. Scanned,
encrypted, oversized, mixed-subject or incompatible-basis documents can stop.
No new approved factor-scoring rubric was invented; absent factors stay unknown.
Runtime grounding uses cited uploaded pages, not a newly added vector database.

## Demo navigation

New Deal -> Upload New Deal -> Validate and inspect uploads -> declare the
documented reporting basis if no exact registered profile matches -> Save
reporting basis -> Run AI Deal Review -> Review Workspace. Complete the explicit
fact/profile checks in the indicated simulated reviewer roles, then continue as
Analyst. Review narrative evidence and continue. Agent Activity shows recorded
branches and handoffs; Credit Memo provides the same deal's downloadable report.
Human credit actions remain separate and authorization/readiness gated.

