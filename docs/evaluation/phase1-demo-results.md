# Phase 1 live demo functional results

Measured 2026-10-25 Pacific (successful report UTC 2026-10-26T00:27:20Z).
Phase 2 RAGAS, semantic accuracy evaluation and optimization were not run.

## Outcome

The approved registered Standard Deal completed through the actual Streamlit
Run AI Deal Review action with actual Nebius extraction and synthesis. The
existing LangGraph executed ten stages and retained twelve checkpoints. All
six screens were exercised using Streamlit AppTest, not a visual browser audit.

Successful operation: `e822bbb5-20d0-438a-a74a-2b4c2c0cd69a`.
Local evidence (ignored by version control):
`var/evaluations/phase1-live-ui.json` and
`var/evaluations/phase1-completed-verification.json`.

| Observed result | Value |
| --- | --- |
| Execution status | COMPLETED |
| Actual generation requests | 2: extraction and synthesis |
| Financial debt-service coverage | 1.50x |
| Illustrative risk | 21.00/100 |
| Original AI proposal | Approve, confidence 0.85 (uncalibrated) |
| Effective approval readiness | Pending Review |
| Approval eligible | False |
| Human credit decision / evidence support | Not recorded |
| Draft memo | Generated, downloadable, marked UNVERIFIED_DRAFT |
| Source navigation | Evidence explorer available; source identities validated |
| Duplicate result retrieval / page navigation | No additional provider requests |
| Generation cost at configured verified rates | USD0.0007312 for successful review |

The synthesis input used a separate one-output-token request-size setup probe.
That probe is not RAGAS or a judge and is accounted separately in the shared
allowance. Cumulative local committed cost after all historical work and these
functional attempts: USD0.0120521. The earlier unknown USD0.0007 reservation
remains untouched. These are local ledger values, not a reconciled provider bill.

## Functional corrections and preserved failures

The first actual summary was truncated at the existing 650-token cap. The
second fit the cap but repeated FINANCIAL instead of covering all three panels.
Both were rejected; neither produced a memo or approval. Their actual responses,
reported usage, failed checkpoints and administrative closure events remain.
Only proven settled invalid responses can use the new administrator-only demo
closure. Unknown calls cannot be closed through it. No automatic retries were
introduced. A separate explicit attempt succeeded after demo-context guidance
specified concise output and exactly one observation per panel. Model settings,
system instructions, wire schema, caps, calculations and lending rules stay
unchanged. No saved answer was used as a live fallback.

Post-run inspection also found the source explorer did not recognize the new
demo policy in the source-binding fingerprint. The resolver now uses the same
persisted policy as the worker, preserving historical HUMAN_REQUIRED bindings.
The completed actual review was rechecked without paid calls: download and
source explorer are available, and duplicate retrieval preserves its memo.

## Test evidence

- Broader functional regression: **67 passed, 63 subtests passed**;
  `var/evaluations/phase1-regression.xml` (live graph, readiness, quarantine,
  finance, policies, risk and registered panels).
- Focused final demo and quarantine regression: **12 passed**;
  `var/evaluations/phase1-demo-final.xml`. This overlaps the broader quarantine
  suite; do not sum the counts as unique tests.
- The new UI Run test uses a 180-second action deadline instead of the previous
  30-second timeout. Failed model responses are still failures, not test passes.
- After adding the source-explorer assertion, the complete six-screen UI test
  passed again: **1 passed**, `var/evaluations/phase1-citation-ui.xml`.
- Existing saved workflow compatibility: **4 passed, 3 subtests passed**;
  `var/evaluations/phase1-saved-compatibility.xml`. Saved reviews still run with
  zero model calls and preserved registered results.
- No full-suite claim: only the listed functional suites were run in this phase.

## Demo scope and limitations

Ready for a supervised educational demonstration of the registered Standard
Deal and its live draft. This is not verified underwriting or permission to
approve a loan. Covenant evaluation and human evidence verification remain
Pending; future reporting obligations are not marked breached merely for being
future obligations. The original AI proposal is retained separately.

Live generation remains nondeterministic: two earlier outputs failed. One
successful journey establishes functional execution, not a reliability or
semantic-quality guarantee. Arbitrary uploaded PDF-to-live-analysis is not
connected; uploads remain inspection/manual-review only. Runtime grounding is
DIRECT, not a completed VECTOR/HYBRID benchmark. Role simulation, local audit
history and saved examples remain educational features. Phase 2 evaluation is
explicitly deferred.

## Main changed files

- `config/app.toml`: explicit LIVE / DEMO_DRAFT selection for new reviews.
- `live_worker.py`, `services.py`: scoped demo provenance, integrity checks,
  retained historical interrupts and draft-only routing.
- `live_demo.py`: explicit Run/Continue coordination and bounded input probe.
- `memo.py`: unverified draft rendering with preserved readiness and sources.
- `live_recovery.py`: evidence-guarded closure of settled invalid demo outputs.
- `command_center.py`: resolve demo source bindings without changing old ones.
- `ui/command_center.py`, `ui/live_workflow.py`: reuse shared UI and backend.
- `test_live_demo.py`, `test_normal_fixture_graph.py`: functional regression
  and explicit saved-mode isolation in copied test workspaces.
- PRD, HLD, specifications, execution plan, runbook, README and AGENTS.md:
  approved Phase 1 scope and provenance boundaries.
