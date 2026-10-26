# Uploaded-deal human review actions

User authorized visible Approve, Reject, Pending and comment controls after live
analysis. Scope: completed uploaded DEMO_DRAFT reviews only; no model rerun or
graph rewrite. The AI draft and original AI proposal remain historical.

Reuse existing readiness evaluation forms in Human Review for the uploaded deal.
Risk Manager and Compliance Officer record evidence verification; Compliance
Officer evaluates covenant applicability/timing with quoted source support.
Do not fabricate a date or waive a requirement to make the sample approvable.

All simulated review roles may add comments; Analyst/Risk Manager/Compliance
Officer/Authorized Approver may request additional information with specific
items. Only Authorized Approver with NORMAL permission may Approve or Reject.
Approve additionally requires current persisted approval readiness, no pending
request and valid unchanged sources. A pending request can be returned to review
by Risk Manager only after explicitly checking every requested item against
quoted current source evidence. This does not onboard replacement documents.

Require comments, exact latest analysis/readiness/decision versions and scoped
UUID operation IDs. Same command is idempotent; conflicting replay/stale versions
fail. Approve/Reject are final for that analysis; later comments remain allowed.
Persist timestamp, simulated reviewer role/name, previous/new status, original
AI proposal, readiness and analysis snapshot in existing SQLite records/history.
Show current human disposition in dashboard/workspace/memo/history without
rewriting the original memo or checkpoints. No paid calls or new dependencies.
Offer a separate memo-with-review-history download; preserve the original memo
download and clearly distinguish later human events from its historical draft.

Tests: role/bypass checks, incomplete readiness, supported approval, Reject,
Pending/response review, comments, duplicate/stale submissions, source changes,
finalization lock, UI controls and cross-screen history. Use offline mocks only.
# Pending Review educational approval override

The user explicitly requested an enabled human Approve action following review
of a Pending Review AI recommendation. In this educational application only,
completed uploaded live reviews may record an explicit demo override when all
readiness blockers have PENDING status and the outcome is Pending Review.
AuthorizedApprover with NORMAL tier, required comments, current version/digest
checks, normal decision confirmation and a separate override acknowledgment
remain required. Missing/stale evidence, policy exceptions, recovery errors,
Pending Information requests and finalized decisions remain blocked.

The command adds demo_override (default false). The human event retains the
unchanged readiness assessment and unresolved requirement IDs, plus reviewer
comments and an EDUCATIONAL APPROVAL OVERRIDE label in displayed/exported
comments. No original AI proposal, readiness eligibility, source support or draft
memo is altered. This is a simulated human decision, not a claim that mandatory
checks passed or real lending authority exists. Ordinary approval still calls
the existing require_approval gate. Graph resume does not gain an override.

