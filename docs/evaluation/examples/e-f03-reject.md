# E-F03 — Supported end-to-end Reject walkthrough variant

Version: 1.1
Variant ID: reject-supported
Split: Development, existing E-F03; not a thirty-first scenario
Status: EXECUTED SYNTHETIC FIXTURE in scoped tests; registered PDFs, exact source-linked Reject fixture, actual RiskManager handling, AuthorizedApprover Reject and generated memo/history. No live model-quality or real lending claim.
Authority: [Evaluation plan](../evaluation-plan.md), [SPEC-004](../../specs/policy-risk.md), [SPEC-005](../../specs/synthesis-evidence.md), [SPEC-008](../../specs/human-review-corrections.md)

## Complete supported inputs and expected calculations

Reuse E-N01's USD1,200,000/48-month equipment term-loan structure, documented fixed annual rate6%, repayment schedule, source-supported terms, collateral and no-guarantee statement. Author reconciled source schedules before executing the fixture. The application must not infer absent facts from this prose gold answer.

Updated score prerequisite: author/review five synthetic factor assessments, supporting credit/industry basis and material-input requirements alongside those schedules. Their numeric grades are not invented in this document and a Reject label is not a factor-rating model. Missing factor/source requirements now mean Insufficient Data and pause dependent synthesis; that incomplete run cannot count as the supported Reject walkthrough. A complete score adds its independent route: Moderate normal package review, High separate Credit Risk Manager score handling plus existing DSCR-exception handling and package review, Very High SENIOR-tier package disposition plus any existing exception handling. The supported Reject judgment remains case-specific, not derived from a score band.

| Input / definition | Documented value / expected result |
|---|---|
| Net income; interest expense; income tax | -300,000; 100,000; 0 USD |
| Depreciation; amortization | 500,000; 800,000 USD |
| EBIT | -300,000+100,000+0 = -200,000 USD |
| EBITDA | -200,000+500,000+800,000 =1,100,000 USD |
| Existing debt; proposed borrowing; repayments | 2,400,000; 1,200,000; 300,000 USD |
| Post-loan debt / leverage | 3,300,000 USD /1,100,000 =3.00x |
| Documented CFADS | -300,000 USD |
| Annual principal; annual interest payments | 500,000; 100,000 USD, including the proposed facility |
| DSCR | -300,000/600,000 =-0.50x |
| Secured exposure; prior liens; eligible equipment | 1,200,000; explicit0; 2,000,000 USD |
| Equipment LTV | 60.00% |
| Interest coverage | -200,000/100,000 =-2.00x |
| Current/prior revenue; growth | 4,400,000 /4,000,000 USD; 10.00% |
| Current assets/liabilities; current ratio | 1,500,000 /750,000 USD; 2.00x |

The financial statement/debt-service schedules share a documented annual projected assessment basis including the facility. Balance-sheet/transaction inputs have the compatible stated basis. The source explicitly documents negative cash available, for example after working-capital/capital outflows; EBITDA is not substituted for CFADS. Positive denominators make these negative ratios valid, rather than missing or mathematically undefined.

Proposed source passages: page1 all loan terms; page2 reconciled income/debt/balance-sheet schedule; page3 cash-available and debt-service schedule. Every output must point to an actually authored supporting passage. Case config explicitly marks synthetic KYC/sanctions checks Not required with the case basis; this is not a legal exemption.

## Agent outputs and permitted human path

- Extractor: all required facts supported, no material gaps/conflicts.
- Financial Analyst: the valid calculations above; no invented forecast, PD or composite score.
- Compliance: SYN-ESC-001 DSCR Exception because -0.50<1.25, gap1.75x; other applicable numerical rules pass. Required Risk Manager handling remains open.
- Risk Quantifier: expected material risk weak_debt_service with negative documented CFADS and the DSCR calculation/policy references. Loss/negative interest coverage can be stated as supported financial observations without inventing a new policy threshold.
- Synthesizer: the illustrative case-specific output below, supported by all panels and source references resolved in the surrounding synthesis artifact.

~~~json
{
  "decision": "Reject",
  "confidence": 0.82,
  "rationale": "Documented negative cash available cannot support the proposed annual debt service. Positive EBITDA does not remove the cash shortfall, and no supported repayment remedy is supplied. See the linked CFADS schedule, DSCR calculation and SYN-ESC-001 finding.",
  "conditions": [],
  "escalate_to_human": true
}
~~~

Python sets/verifies escalate_to_human=true because this active DSCR exception requires referral, despite amount below USD10M and confidence above0.7. Validate actual structured references in the enclosing artifact; the text above is illustrative, not a fabricated reference claim.

Human Review pauses. The simulated Risk Manager records exception handling RECOMMEND_REJECT with documented reason/evidence; retain the original Exception and its history. That handling does not waive any other gate. The Authorized Approver then records human_decision=Reject with notes on the current pending package. Resume the same thread for this review-only action without a model call. Only after the permitted handling/review is recorded may the pure Python Report Generator write its seven sections.

Report Decision shows both original simulated PanelDecision Reject and separate human disposition Reject; Conditions shows none, and Audit Log contains actual recorded events/cutoff. Keep the mandatory handling and source history. Default fixture provider requests=0; normal Live-shaped stage count=2; do not label these as observed usage.

## QA-REJECT-01 acceptance

Assert supported intake -> extraction -> valid financial/policy/risk panels -> structured Reject -> required review/handling -> final Reject report. No required input may be missing and no technical failure may be counted as this walkthrough's success.

Compare E-P01's supported Conditional Approve variant, E-M01's missing-information pause with no PanelDecision, and E-T03's technical stop with no fabricated credit decision. A threshold breach creates its configured finding/referral; it does not universally select Reject. E-F03's fixed label is a reviewed educational fixture judgment supported by this case's facts. Live evaluation scores a frozen permitted-label/rationale rubric separately; never hardcode the fixture's Reject as a general underwriting rule.

Checks: TEST-005-07 plus TEST-008-01/02 and TEST-009-01. Scoped implementation/evidence:
tests/integration/test_exception_reject.py and docs/execution.md. The original
authoring plan below/above is retained; current approved assessments/cash bridge
are in core-case-authoring-proposal.md and the actual E-F03 source package.
