# Exception handling and supported Reject — EXCEPTION-REJECT-1.0

Implementation status: registered E-F03 source/synthesis fixture, actual reviewed
graph, persisted handling, final Reject/memo/history and main-app UI implemented.
Execution evidence is in docs/execution.md. Tests use temporary synthetic workspaces;
no financial test history is auto-seeded into the user's app.

User authorized RiskManager exception handling followed by the prepared E-F03
supported-Reject walkthrough. Reuse current graph, worker, financial review service,
review helpers, memo and SQLite. No new framework/database/model call or policy.

E-F03 has complete authored sources, annual CFADS−300,000, valid DSCR−0.50,
interest coverage−2.00, supplied EBITDA1,100,000 and authored Moderate45/100 score.
Register its exact sources and a source-linked case-specific Reject fixture with
confidence0.82. Python retains SYN-ESC-001 Exception/ESCALATE and Moderate review;
no threshold universally selects Reject. E-M01 still withholds synthesis/score.

Graph runs the existing reviewed path, pausing at human_review before reporting.
PendingReview adds an unsatisfied per-numerical-exception requirement. The only
handling implemented in this slice is RECOMMEND_REJECT, for current supported
SYN-ESC-001/002/004/005 findings. RiskManager supplies nonblank reason and explicit
current source/calculation/policy references. Record a scoped, UTC-stamped immutable-
through-ordinary-commands event and increment gate version; do not change analytical
basis, financial values, original policy findings or AI recommendation. No graph or
generation replay occurs. Conditional exception handling remains unavailable.

Validate actor, run waiting, version/basis/gate, current source hashes and original
finding before durable shared admission. Writes atomically update request and event;
identical command returns its receipt, changed/stale/wrong-scope commands fail.
Reconstruct current gate state from actual original request plus persisted handling
events on every read/accept/resume; do not trust a UI flag or arbitrary receipt.
Full original event snapshots remain in history. Checkpoints carry bounded handling
receipts plus the full-event fingerprint, and recheck them against actual history;
do not duplicate nested snapshots or increase existing byte/depth limits.

Approve and Reject remain blocked before mandatory handling; RiskManager cannot
make a final decision. A recorded RECOMMEND_REJECT enables only a current permitted
AuthorizedApprover Reject (plus comments/information request); it does not enable
Approve. Other unsatisfied gates/information requests still block. Final human
receipt retains exact handling evidence; report node rechecks it before rendering.
Report/history show original Exception, separate handling, original AI Reject and
human Reject with both comments/identities/timestamps. Unfulfilled unrelated gates
cannot be cleared and read/export do no inference. No automatic expiry/deletion.

UI: New Deal adds E-F03; Human Review lists outstanding exception and role, shows
supported evidence selection and reason entry to RiskManager, then explicit final
Reject to AuthorizedApprover. Dashboard next owner follows actual unhandled gates.
History includes exception events/filter/export; no new screen or fake history.

Acceptance: source arithmetic/rubric, premature decisions and wrong roles blocked,
stale/duplicate/concurrent handling, tamper/source mismatch, no model replay, real
interrupt/resume/report/history/CSV and normal/missing-case regressions. Paid Live,
E-P01 Conditional and general document intake remain pending.
