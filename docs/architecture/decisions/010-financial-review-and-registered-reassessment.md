# ADR-010: Financial fixture review and registered-source reassessment

Status: Implemented bounded extension, user-authorized implementation-order request.

Use the existing StateGraph with two reviewed nodes, not a second pipeline.
E-N01/review changes only its separately registered synthetic synthesis confidence
to0.65 and escalation true. It uses the existing confidence rule and unchanged
financial documents, policy, formulas, authored score and Runtime prompts.

Financial requests/events are distinct from illustrative preview kinds. Receipt
acceptance and application state commit atomically with existing execution
admission, before same-thread Command(resume). On resume consume only that own
recorded request/receipt. Preserve AI proposal and original referral separately
from human disposition. Unknown commit/checkpoint gaps keep recovery required,
with no automatic replay or duplicated decision. Reports recheck accepted gates.

Information fulfilment is deliberately profile-limited: exact registered PDF,
RiskManager assessment, reference for every request item. It does not certify new
facts or accept arbitrary uploads. A separately registered revision2 reuses only
identical verified intake/extraction, then invokes the same graph from financial
analysis. New run/thread, same review_id and cumulative ledger; stale old request
and superseded run retain history. Parent consumes ten logical nodes; nine-node
remaining reviewed path totals nineteen, within twenty. No budget reset, expiry,
additional LLM stage, schema migration or new paid infrastructure.

Financial history reads frozen event-time analysis/source snapshots in one scoped
read transaction. CSV rechecks dataset identity and neutralizes formula cells.
SQLite retained records are not immutable/tamper-proof storage. Teaching notebook
and static HTML reuse graph/read services and execute no provider calls.

Trade-offs: this proves financial coordination and controlled reassessment with
fixture responses, not live extraction quality or general document intake.
Conditional editing, other source/Reject/conflict cases, automatic technical
recovery UX, full accessibility and paid provider/retrieval/evaluator runs remain
separate work. Do not represent these as completed by this extension.
