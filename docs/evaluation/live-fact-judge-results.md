# Live extracted-fact judge results — 2026-10-25

Observed custom LLM diagnostic, not native RAGAS, human verification, legal
clearance or a credit decision. Scope: original live extraction from review
`46802df1-4f6b-435d-895e-61576fca3d9b` and the same registered source packet.
The 36 targets comprise 31 extracted facts and five authored scoring premises.

## Actual result

| Outcome | Count |
| --- | ---: |
| AI-supported with accepted exact citations | 31 |
| AI contradiction finding | 0 |
| AI insufficient-evidence finding | 0 |
| Independent evidence-validation flags | 5 |
| Not assessed | 0 |

All 36 original AI judgments proposed SUPPORTED. The independent mechanical
validator excluded five from the accepted supported count. This does not prove
the remaining 31 interpretations are correct, nor that a flagged fact is false.

| Flagged target | Independent issue |
| --- | --- |
| Currency | Quoted `Currency: USD whole units.` is not an exact source sentence. |
| Use of proceeds | Quotation flattened a source line break; strict exact-substring validation failed. |
| Authored repayment-capacity premise | Only the assessment page was cited; required financial sources were omitted. |
| Authored financial-leverage premise | Only the assessment page was cited; required financial sources were omitted. |
| Authored collateral-quality premise | Only the assessment page was cited; required collateral sources were omitted. |

No quotation was silently corrected, and no incomplete citation set was promoted
to verified evidence. The same model family generated and judged the extraction;
correlated errors remain possible. Source excerpts and immutable version/page
identifiers in the report support human examination, not independent ground truth.

## Actual calls and cost

Fixed model: Qwen/Qwen3-30B-A3B-Instruct-2507. Three paid requests total, no
embeddings, web fetch, hidden retry or extra repair call. Actual tokens/costs:

| Batch | Input tokens | Output tokens | USD |
| --- | ---: | ---: | ---: |
| First 12 | 4480 | 1100 | 0.0007780 |
| Next 12 | 4533 | 1162 | 0.0008019 |
| Final 12 | 4953 | 1256 | 0.0008721 |
| Total | 13966 | 3518 | 0.0024520 |

The first report failed whole-batch citation validation and remains intact.
Explicit independent continuation reused that settled raw first response locally,
retained its evidence flag, and paid only for the two unjudged batches. The child
report is COMPLETE_WITH_FLAGS; completion describes diagnostic execution, not
unconditional acceptance of the extraction. There were no uncertain new calls.

Current shared committed spending: USD0.0091557, with the earlier USD0.0007
uncertain reservation still held, within the USD0.10 authorized allowance. No
active execution claim remains. Cached report access makes no model call.

## Artifacts and isolation

- Original failed report:
  `var/evaluations/fact-judge-b76516c1-c556-5cb5-81c0-7424c1ffa75d.json`.
- Completed flagged diagnostic:
  `var/evaluations/fact-judge-1fb7eaa9-9fef-5454-8617-34778101b82f.json`
  and the corresponding `.md` report.
- Before/after hashes:
  `var/evaluations/fact-judge-protected-before.json` and
  `var/evaluations/fact-judge-protected-after.json`.

All protected live records, budget ledgers, graph checkpoints and checkpoint
writes are unchanged. Only ordinary paid-evaluation accounting/receipts were
added through the existing transport. No HUMAN_SUPPORTED receipt, lending
decision, updated financial fact or graph continuation was created.

Final offline checks passed: **22 tests**, 9.62 seconds, covering target coverage,
invented/absent quotes, incomplete source coverage, status consistency,
three-request bounds, retained failed denominators, cached first-batch reuse,
parent-report preservation, safe flagged-report rendering and existing
answer/evaluation transport regressions.
Evidence: `var/evaluations/fact-judge-offline.xml`. The full application suite was
not rerun for this separate evaluator. Reopening the completed diagnostic through
the explicit CLI returned COMPLETE_WITH_FLAGS with `replayed=false`; no provider
request was made for that check.

The fact-review interrupt remains open. Actual synthesis and live-synthesis
RAGAS still require the existing human verification and continuation sequence.
