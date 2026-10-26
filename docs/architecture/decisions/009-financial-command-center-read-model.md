# ADR-009: Connect the normal fixture UI through a financial read model

Date: 2026-10-24. Status: Implemented for APP-READ-1.0 normal E-N01 only.

Problem: the functioning financial graph and illustrative review preview had
different identities/provenance. Reusing preview requests for financial deals
would falsely attribute human approvals and bypass the real resume contract.

Decision: add one application-owned read service over existing SQLite records.
Reuse the existing worker for explicit Analyst start, with its admission,
idempotency, ledger and checkpoints. Read stored findings and memo; do not rerun
analysis on navigation. Bind source inspection to recorded dependency/input
digests. Inspect execution claims to distinguish uncertain work from completion.
Add UTC timestamps to new stage events, retaining honest gaps in old events.

Trade-off: the six destinations now demonstrate the actual normal path, but
financial approval/information workflows remain visibly unavailable. Keeping the
isolated preview prevents false audit history while that adapter is unfinished.
No new infrastructure or provider calls are needed. Historical source versions
are not archived by this change: unavailable versions withhold citation resolution
rather than using newer documents.

Remaining: registered review/missing/conflict/Reject cases; financial pending
request and transactional receipt/resume; validated evidence fulfilment and
revision invalidation; financial decision history/export; Conditional editor;
notebook/HTML; independently authorized provider verification. None is marked
complete by normal-path UI tests.
