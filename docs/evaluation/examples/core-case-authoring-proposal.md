# Remaining core cases — concrete authoring proposal

Status: User explicitly APPROVED the fictional factor assessments and cash bridge
in this session. Source candidates are now authored and parser-checked under
fixtures/development/e-p01, e-m01 and e-f03. E-M01 is now a registered/executed
information-pause sample; E-F03 is registered/executed through separate RiskManager
handling, AuthorizedApprover Reject and memo/history. E-P01 remains a source
candidate with supported condition/Conditional integration pending. These are not
new bank policies/rating rules. E-N01, prompts, thresholds and budgets are unchanged.

## Source schedules

Use separate synthetic scenario versions of the existing USD1,200,000,48-month,
6% equipment-loan structure. Preserve the explicitly supplied annual2027 forecast
basis and transaction date2026-10-23; never present projections as actual outcomes.
Each scenario needs its own PDF bytes, original page map, reviewed scope/basis,
source hashes, expected extraction and registration. No source is auto-admitted.

| Scenario | Source change from normal fixture | Required behavior |
| --- | --- | --- |
| E-P01 | Document annual CFADS690,000; annual principal500,000 and interest100,000 | DSCR1.15; policy exception; separate RiskManager handling before package decision |
| E-M01 | CFADS explicitly Not supplied; no alternative source supplies it | Unknown DSCR; no complete score/PanelDecision; request information |
| E-F03 | Net income−300,000; interest100,000; tax0; depreciation500,000; amortization800,000; CFADS−300,000 | EBITDA1,100,000, DSCR−0.50 and interest coverage−2.00; case-specific supported Reject only after required handling |

E-F03's actual cash bridge is not supplied by the approved example. Proposed new
synthetic authoring assumption for approval: EBITDA1,100,000 less cash working-capital
outflow800,000 and cash capital outflow600,000 gives CFADS−300,000. No additional
cash-tax/interest deductions in this authored pre-debt-service bridge; interest
remains separately in the600,000 debt-service denominator. This is an educational
cash schedule, not an accounting-standard CFADS formula. Do not invent the bridge
in an agent response or register it before explicit approval.

## Authored risk assessments for approval

These are illustrative case-author judgments, not a deterministic mapping from
ratios to grades or a trained model. Weights remain30/20/20/20/10%. Keep original
credit-profile/industry supporting premises only if separately stated in each
scenario's source; do not borrow a reference to E-N01's assessment page.

| Factor | E-P01 proposed grade | E-F03 proposed grade | Authored explanation |
| --- | --- | --- | --- |
| Repayment capacity |60|100| E-P01 has a documented annual service shortfall; E-F03 has negative cash available and no supported remedy |
| Financial leverage |25|25| Same documented3.00× debt/EBITDA premise, with EBITDA not substituted for cash |
| Collateral quality |20|20| Same explicitly documented60% equipment LTV and prior liens0 |
| Borrower credit profile |15|15| Separate synthetic assessment must explicitly supply the approved no-delinquency premise |
| Business/industry |30|30| Separate synthetic assessment must explicitly supply the same illustrative operating/concentration premise |
| Weighted total |33/100 Moderate|45/100 Moderate| Proposed values only; neither score implies a lending decision |

Checked against E-N01's actual assessment manuscript: its fictional history says
scheduled payments current with no recorded arrears; business premise says an
equipment-using manufacturer with ordinary cyclical demand. No bureau, market or
concentration check was run. Those premises must be separately authored for each
new scenario; they are not observations about a real borrower. E-M01 has missing
material CFADS: no complete grade total, no reweighting and no placeholder zero.

## Decisions and gates

E-P01's approved design calls for Conditional Approve, but its concrete supported
condition text and RiskManager handling disposition still need authoring/review.
Do not invent a collateral/guarantee cure or treat a future promise as missing-data
fulfilment. E-F03 uses the existing documented Reject rationale with empty conditions;
RiskManager RECOMMEND_REJECT precedes AuthorizedApprover Reject. An exception by
itself is never a universal rejection rule. Moderate scores independently require
normal human underwriting. Technical failure and E-M01 missing evidence are not Reject.

Approval received: proposed cash bridge and synthetic factor assessments.
Implementation still needed for E-P01: evidence-supported condition/handling example,
source registration, synthesis rubric and Conditional/package review integration.
E-M01 new-document continuation remains pending. Older source manuscripts' draft/review wording
is retained; the explicit current user approval is recorded in each manifest.
