# Live workflow and answer-quality results — 2026-10-25

These are observed results, not production readiness or credit approval.

## Current technical state after approved quarantine

The exact interrupted attempt was administratively quarantined with explicit user
approval. No active shared execution lock remains. Its USD0.0007 reservation,
unknown usage, original records and checkpoints are retained; it cannot restart.
Earlier valid review `46802df1-4f6b-435d-895e-61576fca3d9b` can now accept actual
fact verification. No live synthesis or live RAGAS answer exists yet. Actual UI
navigation to its Risk Manager form passed with no provider calls or database
changes. See [activation and regression evidence](quarantine-results.md).
Earlier completion checks below describe their historical checkpoints, not a
currently active global lock or current full-suite counts.

Subsequent [live fact judging](live-fact-judge-results.md) assessed all 36
targets with three actual paid requests (USD0.0024520): 31 accepted citation
checks and five independent evidence flags. This is a custom fact-level judge,
not native RAGAS synthesis scoring and not human verification. Current known
shared spending is USD0.0091557, plus the retained USD0.0007 unknown reservation.

## Bounded live-generation requests

The user requested a limit in the three-to-five-request range. The implementation
uses three total submitted generation requests per review, not three extra
retries. Two normal generation stages leave room for one explicit correction,
subject to the existing token/time/allowance checks. There is no automatic retry.
The transport counts persisted request records by review, including unknown
outcomes; cached results are returned before the cap check without dispatch.
The verified provider profile and existing request fingerprints were not changed.

Observed regression: **26 tests passed**, four existing RAGAS ID deprecation
warnings, in 53.83 seconds. Command: Python pytest over
`tests/integration/test_live_foundation.py`, `test_live_graph.py` and
`test_evaluation_transport.py`, with network prohibited and pytest cache disabled.
Evidence: `var/evaluations/live-bounded-requests.xml`. New regressions establish
exactly three mocked submissions, no fourth request or database write, cached
result reuse at the limit, and no replay of an uncertain request using either
the same or a different operation ID. No real paid request was made.

At this pre-quarantine checkpoint, the user confirmed the interrupted request's
provider record remained unavailable and its claim/reservation were unchanged.
The later approved quarantine above releases only the shared claim. Request
limits do not resolve absent usage evidence or fulfill human
fact/narrative review. Live synthesis and live-answer RAGAS remain pending.

## Earlier completion check before quarantine — 2026-10-25

The existing completed saved-answer report was resolved again through the
evaluation CLI with its independent Standard Deal reference. It returned COMPLETE
without replaying provider requests. The latest evaluator/transport offline checks
passed: **15 tests**, 41.64 seconds. One warning concerned denied pytest-cache
writing; the tests passed. No additional paid calls were made. This check did
not rerun the full application suite or produce new live-answer scores.

Actual native scores remain Faithfulness 0.8, Response Relevancy
0.5363238990888313, Context Recall 0.8; Context Precision is NOT_APPLICABLE for
unranked DIRECT context. The five validated custom rubric dimensions are each
5/5. The disagreement with independent Pending Review readiness remains visible;
these scores do not clear incomplete covenant checks or grant credit authority.

Live-answer evaluation cannot yet complete: no recorded live review has a
synthesizer output. The earlier valid extraction remains paused at fact_review.
A newer operation, `aab508af-564d-461f-a4e7-cf0708ec29b6`, requires recovery.
Request `59a0ab09-1779-56f3-b0f8-1ecefea14993` has a retained USD0.0007
reservation without a saved provider usage/result record. Known committed spend
remains USD0.0067037, plus that unresolved reservation, within USD0.10.
Absence of a local result does not prove that Nebius processed or billed nothing.
Do not replay, release the reservation or fabricate usage to unblock evaluation.

Remaining sequence: obtain provider evidence and reconcile the interrupted call
through the existing audited recovery process; complete actual fact review;
verify the actual synthesis packet count and explicitly continue; then freeze
and evaluate the actual live synthesis with separate provenance. Narrative
verification is also required before the live journey's final report. Native
and custom offline evaluation scores never substitute for these human actions.

In the unified UI, open Agent Activity and use Review History to select the
original saved Standard Deal review to see its completed evaluation. Selecting
the newer live attempt correctly shows no answer-quality report yet.

## Offline regression

The full offline suite completed with **309 passed and 269 subtests passed** in
244.54 seconds. Seven warnings concern pytest JUnit properties and deprecated
RAGAS ID-metric imports. Evidence: `var/evaluations/agent-ragas-final.xml`.

## Actual provider checks and evaluation

Nebius structured generation and hosted embeddings passed the fixed capability
probes. The verified models are Qwen/Qwen3-30B-A3B-Instruct-2507 and
Qwen/Qwen3-Embedding-8B (4,096 dimensions). No credentials are recorded here.

The original saved Standard Deal synthesis was evaluated using actual RAGAS
0.4.3 and paid Nebius requests. Native Faithfulness: 0.8; Response Relevancy:
0.5363238990888313; Context Recall: 0.8. Context Precision is not applicable to
unranked DIRECT grounding. These are one-example diagnostics, not release gates.

The first custom evaluation failed exact-quotation validation and remains saved.
One explicit corrected evaluation reused cached native results and produced five
validated custom rubric scores of 5/5. These scores do not establish that the
original Approve proposal is appropriate: the independent readiness gate remains
Pending Review. Human adjudication is required when judge scores and substantive
readiness concerns disagree.

Completed report:
`var/evaluations/answer-quality-30326073-31ec-58f9-8036-3870f2e354fb.json`.
This evaluates the saved synthesis, not a completed live-generated deal report.

## Actual live journey

Operation `46802df1-4f6b-435d-895e-61576fca3d9b` passed live extraction using
2,161 input and 890 output tokens, costing USD0.0004831. It is paused at
`fact_review`; no human support, financial decision or completed report has been
fabricated. Two earlier schema-invalid outputs and their known charges remain
preserved. Existing financial-basis constraints were exposed in the live output
schema; no saved response was substituted.

Observed shared committed spending so far: **USD0.0067037 of USD0.10**. No
outstanding allowance reservation remained at this checkpoint. Later execution
must consult the persistent ledger rather than treating this snapshot as current.

## Remaining work

1. RiskManager reviews actual extracted facts against sources; Analyst continues.
2. Verify the exact actual synthesis request token count before paid synthesis.
3. Complete actual narrative evidence review using the applicable simulated roles.
4. Generate the report subject to readiness and authorized human decision rules.
5. Evaluate that actual live synthesis separately; do not relabel saved results.

Hosted embedding capability is verified; VECTOR/HYBRID semantic benchmarks are
not yet measured. Saved and live results now use the unified review interface;
their provenance and required human checkpoints remain distinct. No live SEC
request was made.
