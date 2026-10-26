# Accepted: abandon an uncertain live attempt without claiming usage is reconciled

Status: ACCEPTED — user approved after the impact explanation on 2026-10-25.
Implementation and activation evidence is recorded separately in
`docs/evaluation/quarantine-results.md`. The filename is retained for existing links.

## Problem and evidence

The user wants to continue the educational demo without further billing work.
The supplied aggregate charges total USD0.0067037, matching known local spending,
but do not establish the interrupted request's processing status or final usage.
An administrative abandonment must not be labeled provider reconciliation.

Interrupted operation: `aab508af-564d-461f-a4e7-cf0708ec29b6`.
Uncertain paid request: `59a0ab09-1779-56f3-b0f8-1ecefea14993`.
Retained allowance reservation: USD0.0007; actual cost remains unknown.
Earlier successful extraction: `46802df1-4f6b-435d-895e-61576fca3d9b`.

## Approved bounded exception

1. Add an explicit Administrator-only abandonment command for this exact
   interrupted attempt. Require a reason, expected record versions, matching
   workspace/review identity and an existing RECOVERY_REQUIRED claim.
2. Verify the known response is absent and the exact unknown reservation is
   present. Do not infer zero usage, settle unknown ledger entries, manufacture
   a paid response or relabel the aggregate bill as request-level evidence.
3. Preserve the original progress, checkpoint, events, unknown ledger and shared
   USD0.0007 reservation. Append a separate versioned administrative quarantine
   record identifying the reviewer, UTC timestamp, reason and request identities.
4. Atomically quarantine the interrupted review and release only its exclusive
   local execution claim. Do not use the existing reconciliation record to
   misrepresent this action as confirmed provider idleness or settled usage.
5. Deny start, continuation, new child request IDs and direct generation for
   the quarantined review. Views remain available and clearly explain that its
   outcome and cost are unknown. A new ID cannot restart that abandoned review.
6. Fence late results and stale writers against the current execution claim and
   quarantine record before publishing results or modifying accounting. Do not
   let a late callback silently settle an abandoned request or release another
   review's claim. A later provider record requires a separate guarded process.
7. Resume only the earlier successfully extracted review after its actual
   Risk Manager fact verification. Maintain all narrative, readiness and credit
   decision gates. Three generation requests per review and the shared USD0.10
   allowance still apply; the uncertain reserve continues to reduce headroom.

## Required regression evidence before local activation

- Non-administrator and wrong workspace/review cannot abandon an attempt.
- Missing or changed reservation, changed version or known result rejects it.
- Abandonment is atomic and duplicate submissions do not create duplicate events.
- Original outputs, checkpoint and unknown reservations remain unchanged.
- Quarantined review cannot resume or dispatch under the same or new request ID.
- Late results cannot publish or release a different operation's admission claim.
- Earlier unrelated review can record genuine fact support and resume using
  existing checkpoints; no reviewer support is automatically created.
- All future spending includes the retained unknown maximum.

## Approval boundary

Root AGENTS.md says approval is required for a "material source-of-truth conflict"
and instructs that "uncertain usage retains its reservation and blocks replay."
The current demo runbook requires evidence-backed reconciliation before clearing
the claim. This proposal deliberately preserves uncertainty and replay denial,
but changes the shared-lock policy to allow unrelated work. It therefore needs
explicit architecture approval before implementation or execution.

Approval granted: implement and test this administrative quarantine, then
abandon only the exact interrupted attempt above while retaining its reservation.
Approval does not authorize new provider models, a higher allowance, fabricated
human verification, lending approval or an automatic inference retry.
