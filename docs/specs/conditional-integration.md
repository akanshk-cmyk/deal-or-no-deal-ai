# E-P01 Conditional approval — CONDITIONAL-1.0

Authorized by the user's request to implement the recommended E-P01 workflow.
Reuse graph/worker/SQLite, condition-draft/review helpers and existing six screens.
No new financial threshold, repayment cure, provider or dependency.

Register the approved separate E-P01 sources: annual CFADS690,000, debt service600,000,
DSCR1.15, shortfall0.10 against1.25, complete authored score33/100 Moderate.
Register a source-linked Conditional Approve fixture. Use the exact existing source
covenant "Supply annual financial statements" as its sole supported condition,
citing E-P01:AGREEMENT-P1. It does not cure the DSCR shortfall or missing evidence.

Human path on the existing paused thread:
1. RiskManager records ACCEPT_FOR_CONDITIONAL_REVIEW with reason, exact DSCR/policy/
   source evidence and the unchanged registered condition. Original Exception stays.
2. AuthorizedApprover explicitly prepares that source-linked condition draft.
3. RiskManager supports its FINANCIAL_RISK target, explicitly acknowledging it is
   not a repayment cure; ComplianceOfficer supports its POLICY_CONTROL target from
   the actual covenant. Use existing prepare_review_conditions/support_draft helpers.
4. AuthorizedApprover records Conditional Approve (or Reject) with comments and
   confirmation, exact draft/version/support receipts and no outstanding other gate.
5. Same graph resumes without model calls; report independently rechecks receipts.

Persist all human actions with original snapshots. Gate version advances separately
from analytical basis; rebuild gate/draft/support state from actual persisted events
on every read/resume. Idempotent identical commands return receipts; stale/cross-scope,
wrong role, changed sources, changed draft and unregistered conditions fail. No
generic Approve bypass. Information requests continue to block. Reject is a human
choice, not an automatic consequence of the DSCR threshold.

ConditionRecord is scoped/stable and links MODEL_PROPOSAL to the actual SOURCE_COVENANT,
parent synthesis/index, source/policy issue and draft. Display exact text, origin,
category, refs, owner Unassigned, status OUTSTANDING and blocks_completion=false only
after mandatory review gates are met. The source covenant remains RECORDED /
EXTRACTED_NOT_EVALUATED. Review support does not mark a condition fulfilled. No
funding, automatic dates or Mark satisfied. Record preparation/support times only.

MVP bounds: one registered source-backed condition, no arbitrary wording changes,
owner edits or replacement documents. General condition editing requires a separately
supported revision and remains unavailable; do not silently accept free-text changes.
Full snapshots remain in history; compact receipts/digests stay in graph checkpoints.
Keep depth/byte/token/call/node/tool/time/cost limits and no automatic expiry.

Tests: actual registered sources/panels; unsupported condition refused; premature
and wrong-role actions blocked; exact draft/domain/gate/source binding; duplicate,
stale/concurrent commands; information blocking; real pause/resume/report/history/
CSV/UI; unchanged original AI/Exception and outstanding condition after completion;
normal/missing/Reject regression. Tests are fixture quality, not live model evidence.
