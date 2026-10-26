# Administrative quarantine — execution evidence

Approved by the user on 2026-10-25 after the impact explanation. This is a
local educational administrative action, not a lending decision or provider
billing reconciliation. See the accepted
[bounded design](../architecture/decisions/proposed-unknown-request-quarantine.md).

## Implementation

- `live_recovery.quarantine_unknown_extraction` is Administrator-only and
  restricted to the exact approved interrupted operation. It validates scope,
  five record versions, the admission claim, absent paid result, exact unknown
  ledger reservations and the retained shared USD0.0007 reservation.
- The command atomically appends one versioned LIVE_QUARANTINE record and
  releases only the local exclusive claim. It does not rewrite original progress,
  checkpoints, usage, output, ledger, or allowance. Duplicate identical commands
  return the same receipt; conflicting commands fail.
- Store admission and protected progress/ledger writes reject quarantined reviews.
  Generation and LangGraph continuation also reject them. Settlement verifies
  current claim ownership inside its transaction; late responses cannot publish
  or release another review's claim.
- Live projections retain Recovery Required for the abandoned attempt and attach
  the explicit administrative record. UI copy says it was set aside, not rejected
  or reconciled, and offers navigation to the earlier live fact-review pause.
- `tools/quarantine_interrupted_review.py` previews expected versions by default;
  explicit `--apply --expected-versions PATH` performs the approved command.
  `tools/check_demo_readiness.py` distinguishes quarantined reviews from an
  active application-wide execution lock.

## Offline verification

Six dedicated tests passed in 22.40 seconds. They cover unauthorized/wrong-scope
requests, stale versions, missing reservation/known result, transaction rollback,
unchanged history/checkpoints/reservations, duplicate requests, replay prevention,
late response fencing, and an unrelated mocked end-to-end live journey that still
requires genuine test-simulated fact and narrative support. These tests make no
provider calls and never write human support to the actual local demo records.
Evidence: `var/evaluations/quarantine-focused.xml`.

After adding UI navigation/history coverage, all **seven** dedicated tests passed
in 318.78 seconds. This supersedes the six-test run above for the final feature.
The existing independent admission family also passed: **nine tests**, 6.62
seconds (`var/evaluations/quarantine-admission.xml`). UI navigation and read-only
history do not dispatch, record human support or release the uncertain reserve.

The initial test run exposed an invalid reuse of another unittest class's setup;
the new test setup was corrected and the six tests rerun successfully. The earlier
mixed-order run also encountered a multiprocessing spawn failure after Streamlit
testing; it is not reported as a passed regression. Earlier artifacts remain retained.

The fresh complete offline run finished with **327 passed, two failed, 269 subtests
passed**, seven existing warnings, in 1005.02 seconds. Both failures were Streamlit
AppTest 30-second timeouts, not a reported failed business assertion. An initial
concurrent recheck also timed out. After competing test runs finished, both exact
affected tests passed unchanged at the same timeout: **two passed in 14.14
seconds**. This is not reported as a clean full-suite pass or proof of UI latency.
Evidence: `quarantine-full-offline.xml`, `quarantine-ui-recheck.xml` and
`quarantine-ui-isolated.xml` under `var/evaluations`.

## Local activation

Applied to the exact approved attempt using the versioned preview manifest.
Receipt: `var/evaluations/quarantine-applied.json`. Read-only preflight now
reports **NO_ACTIVE_EXECUTION_LOCK**; the abandoned review remains quarantined
and not replayable. Actual cost is unknown; USD0.0007 remains reserved against
the unchanged shared USD0.10 allowance. Known spending remains USD0.0067037.

Post-action comparison passed (`var/evaluations/quarantine-integrity.json`):
all original app records unchanged, all original history unchanged, all graph
checkpoints and checkpoint writes unchanged. Exactly one LIVE_QUARANTINE record
was added; only the abandoned operation's state/active-execution fields changed.
A local ignored SQLite backup and before snapshot were retained. No model API,
provider usage reconciliation, credit decision or actual human support was made.

Actual root UI verification also passed: set-aside message visible; navigation
selected the existing valid review; Risk Manager verification form visible; no
uncaught exceptions, provider calls, support records, credit decisions or database
changes. Evidence: `var/evaluations/quarantine-root-ui.json`.

## Remaining gates

The earlier valid live extraction still needs actual Risk Manager fact review,
exact synthesis request verification, actual synthesis, narrative review and
live-answer RAGAS. Quarantine does not authorize human support, credit approval,
an allowance increase or another inference request on the abandoned review.
