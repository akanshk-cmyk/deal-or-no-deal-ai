# Phase 1: working live demonstration

Status: approved by the user on 2026-10-25 ("Approve the demo-draft path").
Phase 2 evaluation and optimization are deferred.

## Deliverable and unchanged boundaries

One existing Streamlit interface and one shared LangGraph builder. Extraction
and synthesis use the existing Nebius model; finance, sample compliance, authored
risk scoring, orchestration and report assembly use existing Python nodes.
Preserve source-linked outputs, saved examples, historical review policies,
quarantine, permission checks, cumulative allowance and three generation-request
limit. No new packages, database migrations, vector services, UI redesign or
RAGAS/judge work. Do not claim three autonomous LLM agents or production readiness.

## Approved educational demo-draft policy

To make a Run action produce an end-to-end live draft without 36 manual
per-fact approvals, explicitly configure a DEMO_DRAFT verification policy for
new live reviews only. The user sees a clear warning before starting:
"Live AI demo: generates an unverified draft. No human credit decision."

Flow: intake -> live extraction -> Python source/schema/reference/basis integrity
checks -> financial calculations -> sample compliance -> illustrative risk ->
live synthesis -> Python output/reference integrity checks -> approval-readiness
assessment -> source-linked draft memo. All agents pass scoped artifacts through
the existing state, events and checkpoints; no separate backend pipeline.

These automatic checks do not establish semantic correctness. Record their
provenance as AUTOMATED_DEMO_CHECKS, never HUMAN_SUPPORTED. Financial facts and
memo text must not claim human verification. Approval readiness remains blocked
by missing human evidence and unevaluated covenants. No automatic human credit
decision, waiver, loan approval or rejection. Confidence referral and other review
requirements remain recorded; a draft memo is not final authorization. Preserve
stops for invalid/uncertain provider output, missing material inputs and unhandled
policy exceptions; no saved-answer fallback or hidden retries.

Existing live reviews without the new context policy keep their original human
fact/narrative interrupts. Never modify those historical contexts or synthesize
human-review receipts. The already quarantined attempt stays abandoned. New
demonstrations use the same database and existing execution admission and cost
ledger, with a new actual review identity.

## Phase 1 functional acceptance

Functional correction: the first actual summary exhausted the existing 650-token
cap. New demo requests include concise output guidance in demo context only
(short rationale, three short observations, minimal supporting references).
System instructions, model settings, schema, financial rules and caps stay
unchanged. Preserve the failed response and settled usage; do not repair its
JSON, substitute a saved answer or automatically retry it. Administrators may
close a demo failure only with a stored, settled invalid/truncated response and
no uncertain usage for that review, then explicitly start a separate review.

1. Explicit Run in Streamlit starts actual Nebius extraction. Viewing never calls.
2. Saved and live records retain the same six-screen navigation and correct source.
3. Node handoffs, financial calculations, sample checks and scoring are recorded.
4. Actual synthesis produces a validated original proposal; deterministic readiness
   shows the effective Pending Review or other appropriate blocked status.
5. A downloadable draft memo, citations, activity and history are available with
   human verification and decision explicitly not recorded.
6. Missing data, wrong roles, quarantined attempts, duplicate submissions and
   failed inference do not obtain approval or silently switch to saved data.
7. Offline functional tests pass; one bounded actual live journey is recorded
   with reported usage and a browser/UI walkthrough. No Phase 2 scoring is run.

## Why an explicit choice is needed

Existing AGENTS.md and LIVE-GRAPH-1.0 require human fact and narrative support
before downstream analysis/reporting. DEMO_DRAFT changes that execution policy
only for clearly labeled new educational drafts, preserving final decision
controls. Choose this exception explicitly or retain the existing per-target
human checkpoints. Neither choice authorizes increasing the USD0.10 allowance.
