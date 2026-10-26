# Independent demo preparation — 2026-10-25

The user deferred interrupted-request reconciliation until provider evidence is
available. This preparation does not waive that step, clear the execution claim,
release its reservation, record human support or advance live inference.

## Read-only application rehearsal

Streamlit AppTest checked the actual local application's six screens under
Analyst, Risk Manager, Compliance Officer, Authorized Approver and Administrator:
**30 checks passed**, no uncaught screen exceptions, no review-mode selector,
zero generation/evaluation transport calls, and identical logical database
contents before and after. Existing recovery notices remained visible.

Evidence: `var/evaluations/demo-readonly-rehearsal.json`.

The initial rehearsal found Streamlit applying an automatic Arrow conversion to
a dashboard column containing exception counts and "Not checked". The display
now uses consistent text values; no count, rule or stored result changed. A fresh
session checked all three recorded deal rows: zero exceptions, zero Arrow
conversion fallbacks, and unchanged database contents.
Evidence: `var/evaluations/dashboard-display-recheck.json`.

These are framework-level checks, not browser screenshot, keyboard, screen-reader
or 200% zoom assessments. No form was submitted and no human decision was made.

## Teaching artifacts

- The existing workflow SVG helper can now render the actual live graph
  definition, including Fact Review, Evidence Review and conditional credit review.
  It still compiles the shared graph builder without invoking it.
- `notebooks/01_workflow.ipynb` now describes unified execution, distinct readiness
  and human decisions, and live verification. It includes a graph-only live SVG
  cell. Code parsing and artifact checks passed; no fresh Jupyter kernel was run
  and no optional notebook tools were installed.
- A versioned `prototype/demo-2026-10-25.html` preserves the original snapshot.
  It displays current readiness above the unchanged historical memo, identifies
  saved-example provenance, and uses the unified Run AI Deal Review label on its
  disabled demonstration action. It makes no live calls or graph invocations.
- The generated live SVG is `var/presentation/live-workflow.svg`.

The updated teaching-artifact checks passed: **2 tests**, 12.23 seconds. They
verify the live graph labels, notebook source parsing, six HTML destinations,
exact recorded source data, current Pending Review notice and no database writes.

The focused command-center and teaching-artifact regression run also passed:
**18 tests**, 257.52 seconds. The separate updated HTML assertion run above
verified the final snapshot presentation after its last changes.

## Follow-up demo checks

The installed headless Edge browser opened a temporary local Streamlit instance
on port 18765; existing services on ports 8501 and 8502 were not stopped or
changed. Browser navigation passed all six screens with no uncaught application
exceptions or browser errors. The New Deal screen had one Run AI Deal Review
action. The Decision History borrower filter accepted and retained typed text;
Tab moved focus to a control. No financial/evidence form was submitted.

External browser requests were blocked and none were observed. The logical
database digest was identical before and after the rehearsal, including persisted
usage and decision records. Evidence: `var/evaluations/browser-demo-rehearsal.json`.
A 200% CSS-zoom screenshot was captured and inspected at
`var/evaluations/demo-history-200pct.png`; this is not a full browser-native zoom,
screen-reader or accessibility conformance assessment. A follow-up browser pass
successfully downloaded the scoped financial-history CSV. The extended pass's
memo selection timed out in its automation selector, so its overall `passed`
field is false despite its six successful navigation checks; this is not evidence
that memo download itself failed. The earlier failed selector attempt is retained
in `var/evaluations/browser-demo-rehearsal-selector-attempt.json`. Actual financial
submissions were not covered by these read-only browser passes.

Added `tools/check_demo_readiness.py`, a standard-library read-only preflight.
It reads configuration and SQLite with read-only/query-only access, never reads
credentials or invokes model code, and reports the active recovery claim,
retained allowance reservation, actual synthesis/report availability and saved
evaluation execution statuses. It distinguishes stale persisted RUNNING progress
from the authoritative RECOVERY_REQUIRED admission claim. No automatic recovery,
configuration change, human support or historical rewrite is performed.

Two new preflight tests passed in 0.15 seconds: an absent database is not created,
and recovery overrides stale progress without modifying database bytes.
The current preflight is recorded in `var/evaluations/demo-preflight.json`.

The full offline regression was rerun with outbound network prohibited:
**319 passed and 269 subtests passed**, seven existing warnings, in 566.38 seconds.
Evidence: `var/evaluations/demo-final-offline.xml`. The two newly added preflight
tests were run separately after full-suite collection; they are additional checks,
not part of the 319-test count. Warnings concern JUnit properties and deprecated
RAGAS ID-metric imports. No paid generation or evaluation was performed.

### Remaining live dependencies

Provider-evidence reconciliation, 36 actual human fact assessments, exact live
synthesis packet verification, actual synthesis and narrative review, live memo
and live-answer RAGAS. The known paid amount and uncertain reservation remain
unchanged. The saved-answer evaluation is not relabeled as live evidence.

The earlier preparation used the previous 315-test suite; the follow-up above
records the new 319-test regression and limited automated browser rehearsal.
Neither substitutes for actual human evidence submissions or a completed live
journey. Follow `docs/demo-runbook.md` for those remaining tasks.
