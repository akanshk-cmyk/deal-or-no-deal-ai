# E-N01 — Source-backed correction variant

Version: 1.3
Status: Executed bounded extraction-miss correction under CORRECTION-1.0; broader completed/interrupted-review corrections remain planned
Authority: [Evaluation plan](../evaluation-plan.md), [SPEC-002](../../specs/extraction.md), [SPEC-007](../../specs/orchestration-budgets.md), [SPEC-008](../../specs/human-review-corrections.md)

## Input and expected sequence

Reuse E-N01's complete original package and documented CFADS USD900,000 for its assessment year. No source is added or rewritten. The default variant extracts it correctly; extraction-miss deliberately returns cash_available_for_debt_service missing despite the original cited page containing it.

E-N01's registered authored factor assessments already support21/100 Low; this
variant invents no new factor grades. Missing validated CFADS yields Insufficient
Data even while those authored assessments exist. The source-backed correction
restores that prerequisite. Current bounded implementation/evidence:
[CORRECTION-1.0](../../specs/source-correction-integration.md) and
[execution record](../../execution.md). Original model quality remains an extraction
miss; corrected workflow success must not replace that original evaluation result.

1. Intake and fixture Extraction execute. DSCR is Unknown, the relevant information issue pauses dependent completion, and no Synthesizer call is dispatched.
2. The Analyst opens the existing page, supplies the documented USD900,000 and basis/reference with a correction reason. Store reviewer-provided correction provenance and original extraction; do not represent it as the original model's result.
3. Mark the terminal missing-information run superseded. It has no Synthesizer or
pending human review. Create revision+1, new run/thread, same review_id/ledger.
General correction of a pending human review remains outside this implemented slice.
4. Save ends with the corrected revision/new run in READY state and affected outputs visibly out of date; it dispatches no graph/model work. The Analyst explicitly selects Update affected findings after readiness/budget revalidation. Enter financial_analyst, then compliance_check, risk_quantifier, synthesizer, evidence and the permitted report route. Reuse unchanged parsed sources/extracted facts. Registered corrected-from-extraction-miss synthesis input must match the recomputed panels.
5. Expected DSCR =900,000/600,000=1.50x, leverage3.00x, LTV60.00%; the illustrative recommendation is Approve, confidence0.85, conditions[], escalate_to_human=false when no other referral applies. Produce the seven-section report and source/correction history.

This path uses one Extraction and one Synthesizer fixture stage, no provider request.
Observed cumulative count12 nodes/7 deterministic tools. A completed-run financial
correction remains planned; its budget arithmetic is not runtime implementation.
Five attempts are a ceiling, not an entitlement.

## Adapter matching and negative checks

Fixture response lookup requires scenario_id, fixture_variant_id, stage, package_digest and input_digest (the normalized current-stage semantic input digest). Normalize semantic current facts, panel values/gaps/issues, source/policy/formula versions and relevant configuration. Exclude generated IDs/timestamps from that digest, but validate their deal/revision scope separately. Never match a corrected synthesis using the unchanged PDF hash alone.

A change to USD910,000 is not silently mapped to the USD900,000 answer. If no reviewed variant matches, return FIXTURE_VARIANT_UNAVAILABLE and require a registered fixture or later explicitly enabled Live mode. No provider fallback.

E-M01 is different: CFADS genuinely does not exist in the source. Typing an unsupported number cannot clear its required-evidence gate. It remains NEEDS_INFORMATION with PanelDecision unset and an incomplete preview. Adding valid new evidence creates a new package/revision and uses the source-change entry path; it cannot reuse an unrelated canned response.

For a correction while a human interrupt is pending, never resume the old thread with changed analytical inputs. The original interrupt remains historical/stale, and a stale resume must fail. Review-only decisions/condition edits continue the same pending thread without inference.

Checks: TEST-002-06/07, TEST-006-08, TEST-007-08, TEST-008-05/08;
tests/integration/test_source_correction.py covers the implemented bounded path.
Live-model accuracy/cost/latency remain unmeasured.
