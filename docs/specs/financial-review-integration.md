# Financial review integration — FIN-REVIEW-1.0

**Separate extraction correction:** [CORRECTION-1.0](source-correction-integration.md)
adds a missing-field repair over existing E-N01 sources. This differs from the
unchanged-evidence response below: actual extractor output changes with reviewer
provenance. Save and Update are separate; old terminal information wait is superseded,
new revision/thread retains review/ledger. Existing reviewed reassessment is unchanged.

**Additive E-P01 implementation:** [CONDITIONAL-1.0](conditional-integration.md)
extends this same service/thread/storage with separate exception handling,
prepared unchanged condition and two specialist support receipts before final
Conditional Approve/Reject. E-N01 continuation remains bounded as specified below;
E-P01 does not gain arbitrary condition editing or new-document continuation.

Status: implemented for the registered E-N01/review and FIN-REASSESS-1.0 paths.
The scope statements below distinguish the original review slice from the later
registered-source fulfilment extension; general/new-fact intake is still unsupported.

Authorization: user requested implementing the findings in the recommended order.
This extends SPEC-007/008/009/010/013 without changing financial rules or budgets.

First registered reviewed fixture: E-N01/review, same verified source package,
financial inputs and authored risk factors as E-N01/default. A separately hashed
synthetic synthesis response has confidence0.65 and escalation true. Existing
SYN-ESC-012 routes it to NORMAL AuthorizedApprover review; it is not a new borrower
case, model-quality observation or automatic credit decision. Original registration,
source files, prompts and normal outputs remain unchanged.

Use the existing graph definition, worker, SQLite file and durable ledger. Extend
the reviewed route with review_prepare -> human_review(interrupt) -> report.
Normal path remains nine nodes; reviewed path budgets eleven logical nodes.
Preparation persists a scoped FINANCIAL_REVIEW request before interrupt, including
analytical dependency digest, gate snapshot, NORMAL tier and registered-fixture
evidence prerequisite. Reserve the human node before pause; human wait is excluded
from active processing. Release the execution claim only after verifying a real
pending checkpoint. Waiting is not Completed and produces no report.

Commands require canonical IDs, expected request version/basis/gate, scoped
simulated role and nonblank comments. Comments/information requests are allowed
to Analyst/RiskManager/ComplianceOfficer/AuthorizedApprover; Administrator is read
only. Final Approve/Reject requires current NORMAL AuthorizedApprover and all
prerequisites. Keep the AI proposal separate; rejection is a human action with
reason, never a universal threshold-breach rule. Conditional editing remains
unavailable until its separate supported-condition contract is integrated.

Persist a frozen event-time snapshot, reviewer role/name, UTC timestamp and status
transition in the same transaction as request/outcome update and execution admission.
Duplicates return the original event; changed payload with reused ID conflicts.
Only an accepted own receipt may supply Command(resume) on the same thread.
Revalidate sources, gate, ledger and checkpoint before dispatch. A record-first
crash must never duplicate the decision; uncertain graph gaps remain explicit
RECOVERY_REQUIRED, never automatically replayed. Approval-only resume performs no
extraction/synthesis call. Recheck the current accepted request inside the node.

Report must validate original evidence and human receipt separately. Render the
same seven sections, preserving AI confidence/escalation, final policy findings,
human action/comments/time and review event references. A handled workflow referral
does not turn its original control into NOT_TRIGGERED. No original memo is replaced.

Workspace exposes permitted actions only for real pending financial requests.
All financial pages use the same outcome/disposition. History shows actual frozen
review events; never import illustrative preview events. Scope checks precede
history/export, and text is inert. Preview continues to reject financial kinds.

Request Information records required items and leaves the graph paused/blocking.
Do not offer generic clearance: source-backed fulfilment/new analytical revision
must be implemented against an exact registered supplement/profile before enabling
it. The initial complete journey is pause -> comment -> Approve/Reject -> memo/history.
General uploads, information fulfilment, Conditional editing, additional source
cases and Live are not completed by this milestone.

## Registered-source fulfilment and reassessment — FIN-REASSESS-1.0

The implementation-order request also authorizes the next bounded step. A pending
information request in E-N01/review can receive an exact registered PDF as a
response. RiskManager must give a nonblank assessment and explicitly map every
requested item to an original page in that PDF. Exact source identity, current
request/version, all independent fixture prerequisites and unchanged registration
are checked; arbitrary documents or a generic checkbox never clear a request.
This is human assessment of already registered evidence, not automatic semantic
entailment or acceptance of new financial values.

Register a distinct E-N01 reassessment input profile at revision2 over the same
verified sources/facts, with its own case and synthesis binding. New evidence not
matching this profile remains unsupported. Atomically retain the response/event,
stale the old request, supersede the old unfinished run and admit a new run/thread
with the same review_id/ledger. Preserve prior events and original AI output.
Set the existing correction-used flag; do not reset budget. Settle the interrupted
logical human node without charging wait time. Reuse only the identical verified
intake/extraction, with explicit artifact_reused events and new scope bindings;
start the same graph at Financial Analysis. Nine remaining reviewed nodes plus
the parent's ten consumed nodes fit the existing twenty-node ceiling. Keep the
new confidence0.65 response and mandatory human review; no inferred improvement.
Explicit final approval/rejection is still required. A second correction that
does not fit the remaining path is denied with the pending state retained.

Acceptance: wrong PDF/item mapping/role/version/basis or Busy writes nothing;
old resume is rejected; new revision/thread shares review_id and ledger; parent
history remains available; current source resolution uses the exact selected
profile; explicit final decision produces a new memo with the actual review.

Acceptance: actual saver reopen/resume; zero provider requests; role/tier/stale/
duplicate/busy protections; preserved original response and source registration;
request info blocks final actions; one disposition/event; same thread and ledger;
memo/history/UI consistency; uncertain outcome is not replayed automatically.
