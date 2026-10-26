# Newer interrupted attempt isolated

Applied 2026-10-25 after explicit user approval of the narrowly scoped isolation.
Operation: `54b1dd19-7dad-4ead-b297-31aae29a0d86`.
Design: [approved exact-ID scope](../architecture/decisions/proposed-new-demo-quarantine.md).

Observed result: **new execution unblocked**, no active execution claims.
Replay of the isolated operation is rejected. This is administrative abandonment,
not a credit rejection or reconciliation of provider usage.

- Its USD0.0007 unknown reservation remains; earlier USD0.0007 remains too.
- Committed cost remains USD0.0135178 under the shared USD0.10 allowance.
- Context, progress, ledger, original paid request, all graph checkpoints,
  earlier quarantine and both completed uploaded reviews are unchanged.
- Only the approved operation's exclusive claim was released; a new versioned
  audit record fences replay and late publication through existing storage guards.
- No paid/provider/SEC calls, retries, database reset or fabricated human support.

Tests: `python -m pytest tests/integration/test_live_quarantine.py -q -p no:cacheprovider`
completed **8 passed**, including second exact-ID authorization, refusal of an
unapproved ID, stale versions, wrong roles/scopes, missing reservation/known result,
transaction rollback, reservation preservation, replay/late response fences and
unrelated workflow preservation.

Actual local evidence (ignored): `var/evaluations/quarantine-preview-new-demo.json`,
`quarantine-applied-new-demo.json`, `new-quarantine-preservation.json`,
`new-demo-quarantine-verification.json`, `new-demo-quarantine-tests.xml`.
Pre/post digests confirm retained records and checkpoints were not rewritten.

Fresh execution is no longer blocked by this attempt. The completed browser
demo remains `Uploaded deal 53d8e05e`; it can be inspected/downloaded without
spending. Further live runs still require explicit Run and the existing source,
configuration, role, token and shared-cost checks. Unknown billing remains a
later reconciliation task and is not assumed free.
