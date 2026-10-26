# Latest Sample Deal interrupted extraction

Status: authorized by the user's instruction to remove the stuck execution
block so the workflow can be tested. Activation evidence is recorded separately.
No paid calls made during diagnosis or isolation.

Observed new live review: 51eef80e-e890-4c62-91bb-c25478a5adf1.
Review ID: f72f77dd-6912-5146-aa2b-8a7d4fc7a01e.
Generation time: 2026-10-26T03:23:18.940651+00:00 (October 25 Pacific).
Paid extraction: addc521e-76c9-5858-8abd-d38a92f7bb2b.
Retained unknown reservation: USD0.0007.
The active claim is RECOVERY_REQUIRED; only pdf_input completed, no extractor
result or report was recorded. The underlying network/provider cause is not
retained, so timeout, rejection and provider completion cannot be distinguished.

Proposed recovery after exact approval: extend guarded unknown-extraction
isolation to this exact operation; recheck versions, identity, allowance/ledger,
missing paid result and exclusive recovery claim. Preserve all original
request/source/checkpoint/history records and the unknown USD0.0007 reservation.
Fence replay/late publication and release only this operation's claim.
No automatic paid retry, evidence verification or credit decision.

The previous sizing isolation remains intact; it did not cause or cover this
new failed attempt. AGENTS.md grants exact-request isolation only, not general
authority. A fresh specific approval is required before activation.

UI fix implemented: exceptions from Sample Deal Run now show the attempt
reference and link the retained attempt to Workspace/Activity rather than just
the outer generic error. Two focused offline Streamlit regressions passed.
