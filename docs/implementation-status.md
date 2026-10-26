# Current implementation status

## Current upload acceptance update - 2026-10-25

The user authorized fixing the upload acceptance gaps. This update supersedes
older exact-Standard-only, inspection-only and sequential-only statements for
**new uploaded synthetic text-PDF reviews**. Historical records are unchanged.
See `docs/specs/general-upload-acceptance.md` for the implementation contract.

New uploads can declare their own borrower, reporting periods, transaction date,
USD whole-unit basis and sample-policy applicability. Declarations are unverified
and must be checked against the retained documents. Unknown inputs/applicability
stay unknown. No sample borrower facts or factor ratings are copied. Existing
parser, token, permission and shared spending limits remain in force.

New uploaded reviews use live extraction -> mandatory fact/profile verification
-> parallel Financial / Compliance / Risk subgraph -> joined synthesis ->
mandatory narrative verification -> readiness routing -> partial or complete memo.
Only the parent persists branch outputs; calculations and policy rules are
unchanged. Missing borrower factor assessments produce Insufficient Data, never
a default Low score. Partial reports do not waive approval blockers. The same
Deal ID and uploaded page map feed Workspace, Agent Activity, Memo and History.
Sample Deal and historical contexts keep their existing execution policies.
No new dependencies, migrations, inference model settings or budget were added.
Phase 2 evaluation remains deferred. Offline provider mocks establish functional
behavior, not fresh Nebius answer quality or genuine human verification.

## Single uploaded-deal live demo — 2026-10-25

Human Review now exposes role-controlled comments, Pending, Reject and
readiness-gated Approve on completed uploaded deals. No actual demo approvals
or evidence receipts were created by implementation tests. See
[results and limits](evaluation/uploaded-human-decisions-results.md).

Subsequent approved isolation of the newer interrupted attempt is applied.
No active execution lock remains; both unknown USD0.0007 reservations and
completed upload histories are preserved. [Verification](evaluation/new-demo-quarantine-results.md).

New Deal → Upload New Deal now supports the complete unchanged three-PDF Standard Deal package. Explicit Run performs fresh Nebius extraction and synthesis on retained uploaded content, with a distinct upload-derived Deal ID, source map, shared workspace/activity/history and draft memo. It does not use saved answers as live results. Other, partial or changed packages remain inspection-only. Approval readiness and unverified-draft safeguards remain; historical human-checkpoint reviews are unchanged. See [scope, steps and evidence](evaluation/upload-live-demo-results.md). This supersedes older blanket inspection-only statements only for that exact supported profile.


## Approved Phase 1 demo update — 2026-10-25

The user approved the [live demo-draft contract](specs/phase1-live-demo.md). New explicit Run actions use LIVE / DEMO_DRAFT. Extraction and synthesis call Nebius; Python performs calculations, sample policy checks, illustrative scoring, readiness and draft assembly. Technical integrity checks do not record human verification. Drafts cannot authorize credit approval. Existing HUMAN_REQUIRED reviews retain their checkpoints and original records. Saved examples remain available internally. No model calls on screen viewing and no fallback on failure. Phase 2 RAGAS/judge evaluation and optimization are deferred. This update supersedes older default-FIXTURE and pre-draft human-checkpoint statements only for new demo drafts. Functional evidence is recorded in docs/evaluation/phase1-demo-results.md (relative to repository root).


Reviewed 2026-10-25. This page summarizes current observed evidence. Earlier
milestone notes are preserved in
[historical status text](history/implementation-status-before-demo-cleanup.txt);
they do not override the current contracts or authorize paid calls.

## Measured Phase 1 completion

Actual Nebius extraction and synthesis completed through the Streamlit Run
action on the registered Standard Deal. Ten stages, twelve checkpoints, draft
memo download and source navigation were verified. Effective readiness remains
Pending Review; no human evidence support or credit approval was recorded.
Generation cost was USD0.0007312 for the successful review, excluding its
separate request-size probe. See [functional evidence and limitations](evaluation/phase1-demo-results.md).
Older no-live-synthesis/no-live-memo notes below are historical and superseded
by this measured result. Phase 2 quality evaluation remains deferred.

## Working implementation

Agent Activity now explains three specialist roles and shows read-only handoff
progress derived from current-run artifacts and recorded events. This makes
delegation visible without introducing extra calls, changing graph dependencies
or backfilling messages. See [specialist contracts](specs/specialist-handoffs.md).

| Capability | Current scope |
| --- | --- |
| Unified six-screen UI | Existing saved interface is the baseline; one Run AI Deal Review action; config/app.toml selects new FIXTURE or LIVE execution. Both sources share deal selection, workspace and history. |
| Registered examples | Standard Deal, missing information, policy exception/conditional review, supported rejection, and a bounded source-backed extraction correction. |
| Deterministic analysis | Financial calculations, synthetic policy checks, illustrative risk scoring, readiness routing and markdown memo generation. |
| Human review | Simulated role permissions, required comments, exact-version evidence receipts, separate credit decisions and retained history. |
| Citations | Source-bound inspection and original references; missing or unverified evidence is not replaced by newer documents. |
| Uploads | Bounded synthetic PDF inspection and limited manual annual DSCR-input review; no arbitrary upload-to-financial-graph admission. |
| Live integration | Nebius transport, usage reservation, checkpoints, fact/narrative interrupts and report renderer implemented and mocked end-to-end. Actual extraction passed; complete paid journey remains unfinished. |
| Answer evaluation | Native/custom RAGAS actually executed on the original saved Standard Deal synthesis, separately from source-ID retrieval measurements. |
| Live fact judge | Actual three-batch advisory LLM assessment of all 36 targets: 31 accepted citation checks and five evidence flags; no human support or graph continuation. See [measured results](evaluation/live-fact-judge-results.md). |

Latest full offline suite: **327 passed, two UI timeouts, 269 subtests passed**
in 1005.02 seconds, with seven existing warnings. Both exact UI tests passed
unchanged in an isolated recheck (two passed, 14.14 seconds). Seven dedicated
quarantine tests and nine independent admission tests passed separately. See
[quarantine evidence](evaluation/quarantine-results.md) for the full scope and
retained failures. The previous clean full suite was 319 passed/269 subtests.
This is offline evidence, not actual live synthesis quality or UI latency proof.

## Current live blockers

1. Review `aab508af-564d-461f-a4e7-cf0708ec29b6` was administratively quarantined
   with explicit approval; its shared execution claim is now released.
   Its extraction request `59a0ab09-1779-56f3-b0f8-1ecefea14993` has no local
   response/usage result. USD0.0007 remains reserved. This review cannot restart;
   later usage reconciliation remains separate from the approved abandonment.
2. Earlier valid extraction `46802df1-4f6b-435d-895e-61576fca3d9b` is paused for
   human fact verification: 36 required assessments remain unrecorded.
   The new AI judge report can assist that review; its 31 accepted citation
   checks and five flags do not automatically record reviewer support.
3. No actual live synthesis or memo exists. After recovery and fact review, verify
   the actual synthesis packet token count, explicitly continue, review narrative
   evidence, follow any applicable separate credit gate, and generate the memo.
4. Evaluate that actual live answer with its original context. Do not relabel the
   completed saved-answer evaluation as live evidence.

Observed known spend after fact judging: USD0.0091557 plus USD0.0007 reserved/uncertain, under the
shared USD0.10 allowance. Consult the persistent ledger before any future request.
There is now no active application-wide execution lock. Other reviews can submit
permitted evidence assessments. The abandoned review remains visible but cannot
resume or dispatch; its unknown reservation still reduces the shared headroom.

Bounded-request update: live generation now stops before a fourth submitted
request within the same review; cached results remain readable and unknown
outcomes stop without automatic retry. Original verified provider profiles,
prompts, request identities, historical responses and budget ceilings are
unchanged. Provider usage remains unavailable and unreconciled; the separately
approved quarantine releases only the shared local claim, preserving uncertainty.

## Saved-answer RAGAS results

Faithfulness 0.80; Response Relevancy 0.5363238990888313; Context Recall 0.80.
Context Precision is not applicable to unranked DIRECT grounding. Five custom
rubric dimensions scored 5/5, but independent readiness remains Pending Review;
optimistic judge scores do not clear missing covenant evaluation. See
[recorded results and limitations](evaluation/live-answer-quality-results.md).

## Demo completion checklist

Independent preparation continued after the user deferred provider reconciliation:
30 earlier read-only screen/role checks passed with zero provider calls and unchanged
database contents. A dashboard display-type warning was fixed and rechecked;
the graph-only notebook now includes live verification and a versioned HTML
snapshot shows current readiness above historical memo content. See
[demo preparation results](evaluation/demo-preparation-results.md). A follow-up
headless Edge rehearsal checked six-screen navigation, history-filter typing and
CSV download without changing the database. The read-only demo preflight reports
the recovery lock without clearing it. Fresh-kernel and complete manual
accessibility/submission checks remain unverified; no live blocker was bypassed.

Use the [presenter runbook](demo-runbook.md). Required remaining evidence is one
complete live synthetic journey, live-answer RAGAS with limitations, and an honest
operator/browser rehearsal. No production-readiness claim follows from this demo.

Optional or deferred: real hosted VECTOR/HYBRID semantic comparison, arbitrary
uploaded-document financial admission, general new-document continuation,
condition fulfilment, fresh-kernel notebook execution (installation deferred),
PDF audit export, real authentication, crawling and external deployment.

[Unified contract](specs/unified-review-experience.md) |
[Approval readiness](specs/approval-readiness.md) |
[Execution plan](execution.md)
