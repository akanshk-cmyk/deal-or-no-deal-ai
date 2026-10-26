# Isolate the interrupted document-sizing request

Status: user explicitly approved isolation ("ok Approve isolating this stuck request."). Activation verification follows in docs/evaluation/sizing-probe-isolation-results.md.

Request: fbb6ba9d-ba4b-5c5a-b0b8-11f350b413ea.
Review: 74985f6f-5825-5e39-9ae9-ceaf13f36e35.
Retained maximum reservation: USD0.0262147, not a measured charge.

Proposal: apply probe_recovery.isolate_probe as a simulated Administrator,
rechecking request and allowance versions, exact workspace/review/purpose,
recovery claim, retained reservation, and absence of a settled result. Append a
versioned quarantine audit and release only this request's execution claim.
Keep the original request, unknown cost reservation, upload, saved profile,
earlier quarantines and completed reviews. Fence replay and late publication.
Do not reconcile provider billing or automatically send another request.

The aggregate billing screenshot does not identify this specific request or
prove that it completed. Its provider usage remains UNKNOWN. Removing the local
execution lock enables independent future operations; it does not make replay
of this same sizing task safe. A fresh attempt requires a separately bounded,
explicit recovery step; it is not performed by this proposal.

Implementation: src/deal_or_no_deal_ai/probe_recovery.py. Evaluation transport
checks quarantine before reading cached results and validates the execution
claim transactionally before committing late responses.

Observed validation: 7 tests passed in 1.41s across test_evaluation_transport.py
and test_probe_recovery.py. No paid calls; actual application state unchanged.

Approval boundary: AGENTS.md says the earlier quarantine action is "not general
quarantine authority". This is a new exact request, so those approvals cannot be
reused to activate this action.
