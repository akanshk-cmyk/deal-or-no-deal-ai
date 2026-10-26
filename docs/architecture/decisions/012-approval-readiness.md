# ADR-012: Separate proposal, approval readiness and human decision

Status: user-approved educational MVP control, 2026-10-24.

The saved Standard Deal proposes Approve while its contractual covenant has not
been evaluated. Retain that exact model-shaped response as historical evidence;
do not edit the sample answer to hide the inconsistency.

Evaluate readiness deterministically inside the existing route_review node. Store
ai_proposal, approval_readiness and human_decision separately. Reuse app_records,
SQLite admission, version preconditions and existing reviewer permissions. Enforce
the latest assessment on direct approval and graph resume, not only in the UI.

Readiness has five outcomes: Ready for Human Decision, Pending Review, Additional
Information Required, Exception Review Required, Recovery Required. Only Ready
permits an independently authorized approval. Missing information does not imply
rejection. Future reporting obligations need applicability/timing/evidence review;
they are not automatically breached before their contractual due date.

Rejected alternatives: treating the AI proposal as final authority; modifying the
registered answer; adding another LLM to judge eligibility; blocking every draft
report until credit approval. These either obscure provenance, add cost or prevent
useful review without improving the deterministic controls.

Consequences: historical reports remain original snapshots; current readiness may
differ. Additional reviewer work is explicit. Saved-response matching alone is
not semantic evidence verification. Existing premature approval walkthroughs now
remain blocked until mandatory checks are satisfied. No additional model calls,
dependencies, database or automatic expiry are introduced.

Contract: ../../specs/approval-readiness.md. Test results:
../../evaluation/approval-readiness-results.md.
