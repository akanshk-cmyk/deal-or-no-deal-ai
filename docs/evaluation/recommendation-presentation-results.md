# Recommendation presentation — implementation results

Measured 2026-10-24. Educational prototype; no paid model, embedding, judge,
SEC or other external requests. No additional dependency or database.

## Improvement

One pure formatter, recommendation.py, explains the existing ApprovalReadiness
and recorded financial/risk outputs. It creates an outcome, recommendation,
two-to-four-sentence rationale, recorded outstanding issues, next action and
independent human decision. Unknown readiness remains qualified Pending Review.

The formatter does not use the original model's prose as verified evidence.
An illustrative Low score cannot determine the effective outcome. Ready means
ready for human assessment; an unfavorable existing proposal is not converted
into favorable advice. Future obligations keep their existing evaluated status.
No High-Risk Review status, underwriting thresholds or approval rules were added.

Dashboard uses a compact explanation. Workspace uses the full explanation and
existing citation explorer. New saved-response and live Memos use the same
formatter. Original proposals remain in expandable/audit details; their exact
stored responses and historical memo bytes are preserved. New report renderer
versions include /RECOMMENDATION-1.0 to identify the changed presentation.

## Standard Deal before and after

Before: Approve — Supported annual repayment metrics and the supplied Low
assessment support this simulated recommendation; contractual covenants remain
unevaluated.

After:

- Recommended AI Outcome: Pending Review.
- Recommendation: Defer approval pending additional validation.
- Supporting Rationale: The calculated annual debt-service coverage ratio is
  1.50x; current evidence verification is not complete. The supplied illustrative
  risk assessment is Low (21.00/100); this score does not establish approval
  eligibility. Mandatory covenant evaluation incomplete. Unconditional approval
  is not supported while the recorded mandatory blockers remain unresolved.
- Required Next Action: Evaluate the annual financial-statement reporting covenant,
  including its contractual timing and requirements. Verify the current critical
  facts and conclusions against their source evidence.
- Human Decision: Not recorded.

Observed structured example: var/evaluations/recommendation-e-n01.json.
These statements describe the actual registered synthetic case, not a universal
loan assessment or verified real borrower. No nonexistent policy exception is
added to this case's outstanding issues.

## Files added or modified for this change

Application:

- src/deal_or_no_deal_ai/recommendation.py — new shared pure formatter and Markdown renderer.
- src/deal_or_no_deal_ai/ui/readiness.py — full recommendation, independent human
  decision and citation controls; original proposal in expandable details.
- src/deal_or_no_deal_ai/ui/dashboard.py — compact recommendation.
- src/deal_or_no_deal_ai/ui/command_center.py — pass existing source availability
  to recommendation citation controls.
- src/deal_or_no_deal_ai/memo.py — same full narrative in new saved/live Memos;
  original proposal retained in labeled audit details.

Tests:

- tests/unit/test_recommendation.py — new pure presentation safeguards.
- tests/integration/test_recommendation_presentation.py — new actual Standard Deal,
  memo consistency, unchanged results, UI and citation navigation tests.
- tests/integration/test_financial_review.py — expected new report renderer suffix.

Documentation:

- docs/specs/recommendation-presentation.md — new minimal implementation contract.
- docs/specs/overview.md, docs/product/prd.md, AGENTS.md — current scope references.
- docs/evaluation/recommendation-presentation-results.md — this evidence report.

## Verification

Focused suite: **12 passed in 12.04 seconds**. This includes eight formatter
checks, two new integration tests, the existing conditional-review record check
and the existing source-mismatch citation check.

Full offline suite: **292 passed and 269 subtests passed, zero failures, in
187.04 seconds**. Seven existing warnings remain: three JUnit record_property
compatibility warnings and four RAGAS deprecated-public-import warnings.

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=short --junitxml=var/evaluations/recommendation-final.xml
```

Focused XML: var/evaluations/recommendation-focused.xml.
Full XML: var/evaluations/recommendation-final.xml.

The initial regression pass caught citation buttons being exposed after source
validation failure and an oversized conditional-review record caused by repeated
policy references. Both were corrected in presentation code. References now
point to the relevant exception evidence rather than every passing policy; source
failure withholds recommendation links. Existing size limits were not increased.

The unchanged Standard Deal still executes nine graph nodes with zero model
attempts in saved-response mode. Tests verify formatter reads do not mutate its
financial/policy/risk artifacts, original proposal, human status or database.
Existing graph, authorization, correction, history, saved-response and mocked-live
regressions pass. Live-provider correctness is not established by mocked tests.

## Scope and future limitations

Financial formulas, policy rules/thresholds, risk weights/bands, readiness
eligibility, role permissions, LangGraph nodes/routing and registered sample/live
response formats remain unchanged. No extra LLM call formats the narrative.

This feature explains recorded results; it does not fill missing evidence,
evaluate an unreviewed covenant or establish model accuracy. Historical reports
remain historical; their current UI recommendation can differ from the stored
snapshot. Existing bounded local record/document limits remain. Normalizing large
review histories or building broader financial interpretation would be separate
backend work, not part of this minimal presentation change.
