# Uploaded-deal human controls

Implemented under [the requested contract](../specs/uploaded-human-decisions.md).

Review Workspace -> select uploaded deal -> Human Review now displays Approve,
Reject, Mark Pending and Add Comment. Comments are mandatory. Final decisions
require simulated Authorized Approver with NORMAL permission; Approve also
requires current recorded readiness and no outstanding information request.
Incomplete covenant/evidence checks cannot be cleared by the AI or a role change.

Evidence and covenant forms are now in Human Review for uploaded deals. Risk
Manager and Compliance Officer verify their respective current targets, including
actual live policy rules. A Risk Manager can return a Pending case to review
only after checking every requested item against quoted current sources. This
does not onboard replacement documents or modify extracted facts. Later requests
preserve previously outstanding items. Final decisions cannot be overwritten;
comments remain available, and further readiness edits are blocked.

Every action stores the same Deal ID, actor/role, UTC timestamp, comments,
previous/new status, AI proposal and readiness/analysis snapshot. Shared history
and CSV accept explicitly labeled LIVE_ANALYSIS_HUMAN_REVIEW events with a scoped
live-context check; they are not mislabeled saved responses. Dashboard, workspace,
memo and Decision History project the latest human disposition. The original
draft and LangGraph checkpoints are unchanged. A separate memo-with-review-history
download appends events without rewriting the original report.

Offline test evidence:
- Three new human-action scenarios passed: blocked/unauthorized approval,
  Pending/comments/response review/Reject, duplicate and stale commands,
  finalization/history/export preservation, controlled approval-ready state and
  actual Streamlit controls/cross-screen navigation.
- Existing readiness/live graph/command-center regression: **37 passed**;
  `var/evaluations/uploaded-human-regression.xml`.
- Final focused rerun after policy-target/export changes: **4 passed**
  (three human-action scenarios and existing evidence-verification regression),
  `var/evaluations/uploaded-human-final.xml`. Counts overlap earlier tests.
- Actual completed uploaded deal was checked read-only in Streamlit AppTest:
  all four controls visible; Authorized Approver's Reject/Pending/Comment enabled,
  Approve disabled for its genuine incomplete readiness; evidence/covenant forms
  available under the correct roles. Original draft and allowance unchanged.
  Evidence: `var/evaluations/uploaded-human-ui-current.json`.

The approval success test uses an explicitly controlled ready-requirements test
double. It does not claim the actual Standard Deal's missing contractual timing
was resolved. Do not invent a due date, classify a covenant as inapplicable just
to enable approval, or treat existing quotes/checkboxes as automatic verification.
The real Standard Deal stays Pending until its required source-supported reviews
are satisfied. No real demo comments, decisions or verification receipts were
fabricated. No paid calls or Phase 2 model-quality evaluation were run.

Main changes: uploaded_decisions.py and ui/uploaded_decisions.py; Human Review
integration; readiness finalization and policy-target checks; scoped live-history
support; dashboard status and optional memo-with-history export.
