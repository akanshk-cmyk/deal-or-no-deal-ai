# Proposed isolation of the newer interrupted attempt

Status: approved by the user on 2026-10-25 ("Approve this narrowly scoped
isolation"). Applied and verified; see [activation evidence](../../evaluation/new-demo-quarantine-results.md).
Separate from the successfully completed browser-uploaded deal. No provider requests.

Final preflight observed a newer Standard Deal review started at
2026-10-25 18:26:33 Pacific (2026-10-26T01:26:33Z), with no stored provider result.
Its active recovery claim currently prevents new execution globally.

- Operation: `54b1dd19-7dad-4ead-b297-31aae29a0d86`
- Review: `8635fc37-d1e8-54dd-ad48-a9d378150f2c`
- Paid extraction request: `84124b6b-9a42-59ec-b3f9-3c6c6ba4b500`
- Retained uncertain allowance reservation: USD0.0007.
- Original uploaded browser demo operation `9122dfaf-dcc7-5913-9792-029e11a312fe`
  remains COMPLETED and its memo can be inspected/downloaded without new calls.

Proposed action, only after approval: extend the existing exact-ID administrative
quarantine mechanism to this one explicitly named operation, after rechecking
context/progress/ledger/allowance/request versions, missing paid result, exact
unknown reservations and exclusive claim. Retain original sources, checkpoints,
request, ledger, unknown cost and a versioned administrative audit record. Fence
replay/late publication for this review and release only its execution lock.
Do not erase, reconcile, assume no charge, retry or turn it into a credit rejection.
Do not alter the earlier quarantined operation or either completed uploaded demo.

AGENTS.md currently authorizes exact-ID quarantine only for the earlier
`aab508af-564d-461f-a4e7-cf0708ec29b6` attempt; that does not authorize this new one.
Required tests before activation: exact scope/version/result/role checks,
reservation retention, replay and late-result fencing, and unrelated completed
review preservation. A restart alone must not clear the uncertain request.
