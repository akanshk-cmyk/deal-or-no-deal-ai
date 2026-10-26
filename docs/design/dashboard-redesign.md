# Deal Dashboard — recorded-data redesign

Scope: Screen 1 only. Preserve the six destinations, financial commands, permissions,
source validation and budgets. Reuse design-system.md; no new UI dependency.

| Reference component | Application mapping | Limitation |
| --- | --- | --- |
| Portfolio summary | Distinct latest deals; decision, risk, exception, information filters | E-N01 only today; runs are not deals |
| Borrower profile | Recorded extracted terms and revision | No assigned owner, industry or existing exposure |
| Risk gauge | Recorded educational 0–100 score and band | Higher is worse; no PD or calibrated prediction |
| Financial extraction | Recorded calculation values, units and calculation links | No invented reporting periods or trends |
| Covenant monitoring | Recorded policy results, exact predicates and evidence links | Not covenant-fulfilment monitoring |
| Workflow | Actual stage events, including synthesis/routing and human interrupt | No estimated completion percentage |
| Alerts | Pending decision/information, recovery and policy findings | Required role is not an assigned individual |

Read-only projection groups by scoped deal ID and selects the greatest recorded
generation time, breaking ties by operation ID. Queue priority: recovery, pending
information, pending decision, policy exceptions, high risk, other recorded reviews.
Execution and human disposition remain separate. Counts of exceptions mean recorded
exceptions, not verified unresolved-resolution state. Missing policy results remain
Not checked and excluded from the known-count subtotal.

Dashboard links bind the selected operation before navigation. Evidence links open
the existing Workspace explorer, which verifies the original source packet before
showing passages. Merely reading the Dashboard starts no graph, provider, retrieval,
embedding, mutation or financial decision. Role availability comes from the existing
financial review service; no new approval controls are added here.

Native controls retain keyboard access and focus styles. Three desktop card columns
collapse on narrow screens; tables scroll. No accessibility certification is claimed.
Trend charts remain unavailable until comparable time-series observations exist.
