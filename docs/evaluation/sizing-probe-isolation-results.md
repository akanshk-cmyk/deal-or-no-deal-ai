# Approved sizing-request isolation: activation evidence

The user explicitly approved setting aside this exact interrupted sizing
request. Applied using probe_recovery.isolate_probe after checking current
request/allowance versions, workspace/review/purpose, unknown recovery claim,
retained reservation and absence of a settled result.

- Request: fbb6ba9d-ba4b-5c5a-b0b8-11f350b413ea.
- Review: 74985f6f-5825-5e39-9ae9-ceaf13f36e35.
- Result: ISOLATED_NOT_RECONCILED; its claim is RELEASED with no active key.
- Unknown USD0.0262147 allowance reservation retained unchanged.
- Every pre-existing application record and every other execution claim compared
  equal before/after. Only the quarantine audit and target claim were changed.
- Original upload, reporting profile, completed/historical reviews and earlier
  isolation records preserved. No paid calls, SEC requests or credit decisions.
- Evidence: var/evaluations/sizing-probe-isolation-applied.json.

Replay and late publication for the abandoned sizing review remain forbidden.
This releases its execution lock; it neither reconciles billing nor completes
the uploaded deal. A controlled new-attempt mechanism is still needed before
this same packet can undergo another sizing request. Repeated Run on the
original packet is not a recovery mechanism.
