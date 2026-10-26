# READINESS-1.0 implementation and offline results

Measured locally on 2026-10-24. Educational prototype, simulated reviewer roles.
No paid provider calls, SEC requests, dependency installs or real-deal decisions.

## Result

The deterministic gate runs inside the existing route_review node. It preserves
the exact saved/live proposal, records versioned eligibility separately, and
requires current eligibility plus existing permissions for human approval.
Low risk and an AI Approve proposal cannot override mandatory blockers.

Existing E-N01 registration, saved response, source files, financial calculations,
references and previously stored reports/events were not edited. Tests use isolated
temporary workspaces; the user's local deal database was not reset or migrated.

## Observed E-N01 output

| Field | Observed result |
|---|---|
| Original AI proposal | Approve, unchanged saved response |
| Approval readiness | Pending Review, version 1 |
| Primary reason | Mandatory covenant evaluation incomplete |
| Additional blocker | Current evidence verification pending |
| Human decision | Not recorded |
| Next action | Evaluate the annual financial-statement reporting covenant, including its contractual timing and requirements |
| Report | Generated, with readiness and original proposal distinguished |
| Graph nodes / audit events | 9 / 18 |
| Model attempts | 0 |

Reproduction evidence: var/evaluations/readiness-e-n01.json. A saved answer's
reference matching does not replace a human semantic evidence review. The annual
covenant is not automatically classified as breached and no due date is invented.

## Schema

Three independent fields: ai_proposal, approval_readiness, human_decision.
ai_proposal retains original_wire_json, decision, rationale, mode and parent_digest.

ApprovalReadiness contains:

- schema_version READINESS-1.0; assessment_id; version; previous_assessment_id.
- scope and review_version; exact analysis_digest; evaluated_at_utc; review_as_of.
- outcome; approval_eligible; reason; evaluated_requirements; covenants.
- blockers; evidence_refs; permitted_next_actions; assessment_digest.

Each requirement has an ID, label, mandatory flag, status, reason, evidence refs
and next action. Each covenant records applicability, timing, explicit due date,
evaluation status, compliance status, evidence status, refs and reason.

Five outcomes: Ready for Human Decision, Pending Review, Additional Information
Required, Exception Review Required, Recovery Required. Only the first permits
approval. Unknown timing remains pending. A reviewed future obligation with a
verified source-backed future due date may be Not yet due without being breached.
There is no automatic expiry or host-clock-based deadline creation.

## Backend and UI behavior

Versioned snapshots and the current pointer reuse SQLite app_records. Mutations
require existing admission and optimistic record preconditions. Read projections
do not write; legacy/stale projections are marked unrecorded version 0 rather
than rewriting history. Reviewer comments, role, target/source binding and UTC
timestamps are retained. Evidence evaluation alone is not a credit decision.

Direct approvals and conditional approvals require the latest readiness version
and digest, unchanged sources, and existing role/tier/review gates. Resume paths
recheck the recorded approval's readiness. New decisions capture their assessment
and original proposal; history CSV includes these separate fields. Identical
commands return the original event; changed or stale commands are refused.

Dashboard, Workspace, Memo and History use the same current assessment. Original
proposal reasoning is secondary to current eligibility. Historical memo text is
preserved with a snapshot explanation. Pending readiness alone does not prevent
the normal draft report. Independently supported Reject and information-request
flows retain their existing guards; pending readiness never implies Reject.

Earlier tests that approved the incomplete Standard Deal now verify that approval
is blocked and exercise history/resume through a separate human rejection. The
conditional example retains preparation, specialist support and original findings,
but final conditional approval also requires the new mandatory readiness checks.
This is the intended approved restriction, not a waiver of existing policy.

## Verification

Full offline command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=short --junitxml=var/evaluations/readiness-final.xml
```

Observed: **281 passed, 269 subtests passed, zero failures; 242.84 seconds**.
Seven warnings: three existing JUnit record_property compatibility warnings and
four existing RAGAS public-import deprecations. No cache-permission suppression
was needed beyond disabling pytest's optional cache provider.

One additional regression added after full-suite collection exercised the actual
resume receipt loader against a real persisted pending assessment:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider tests/integration/test_approval_readiness.py::test_resume_credit_receipt_cannot_bypass_pending_readiness --tb=short --junitxml=var/evaluations/readiness-resume.xml
```

Observed: **1 passed; 4.63 seconds**. Thus 282 distinct tests and 269 subtests were
verified across the full-suite run and this additional focused run. The full XML
alone contains 281 tests, not 282.

New tests cover incomplete covenants, future and overdue obligations, stale and
missing evidence, unresolved policy exceptions, recovery precedence, missing
mandatory checks, unauthorized approval, stale versions, source changes, duplicate
commands, one-decision enforcement, report preservation and blocked resume.

Fully compliant calculations/covenant eligibility are tested with explicit
synthetic requirements. The backend positive approval test injects those pure
eligibility inputs to isolate role/version/idempotency behavior; it does not claim
that unchanged E-N01 contains enough contractual evidence to become compliant.

## Files added or updated

Application:

- src/deal_or_no_deal_ai/readiness.py (new schemas and pure evaluator).
- src/deal_or_no_deal_ai/readiness_service.py (new versioned assessment/review/decision services).
- src/deal_or_no_deal_ai/graph.py, worker.py, live_worker.py.
- src/deal_or_no_deal_ai/storage.py, command_center.py, financial_review.py, memo.py.
- src/deal_or_no_deal_ai/ui/readiness.py (new), command_center.py, dashboard.py,
  presentation.py, live_workflow.py.

Tests:

- tests/unit/test_readiness.py and tests/integration/test_approval_readiness.py (new).
- tests/integration/test_financial_review.py, test_conditional_review.py,
  test_command_center.py, test_live_graph.py.

Specifications and documentation:

- docs/specs/approval-readiness.md (new), docs/specs/overview.md.
- docs/architecture/decisions/012-approval-readiness.md (new), docs/architecture/hld.md.
- docs/product/prd.md, docs/design/design-system.md, docs/evaluation/evaluation-plan.md.
- docs/traceability.md, docs/execution.md, README.md, AGENTS.md and this results file.

## Remaining boundary

These results verify offline controls, not hosted model accuracy or complete
arbitrary-upload underwriting. Paid live extraction/synthesis, hosted semantic
retrieval and answer-quality RAGAS still require their separately verified setup
and budget controls. SQLite history and simulated roles are educational controls,
not tamperproof auditing or production authentication. No architecture replacement
or parallel/ReAct expansion was performed in this milestone.
