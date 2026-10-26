# Deal or No Deal AI — RAGAS Evaluation Report Template

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.2
Specification date: 2026-10-23
Status: TEMPLATE / NOT RUN — no evaluation or model request has executed
Contract: [RAGAS-EVAL-1.0 / NATIVE-REPORT-1.0](ragas-evaluation.md#standard-native-ragas-report-panel--native-report-10)

This is the required layout for future actual evaluation reports, not measured output. Replace unavailable fields only from validated saved results. Rendering this report reads results; it does not run metrics or the deal graph.

## Evaluation provenance

ADR-007 selects local-file intake, Nebius-hosted embeddings under ADR-008 and SQLite-vector exact search for public references. A future public-corpus report must identify that separate corpus, actual snapshot/query/build/segmentation/model/tokenizer revisions and retrieval arm; the architecture selection is not an executed result. Keep synthetic/public corpus outcomes and retrieval-only versus answer-quality/RAGAS results separate. The selected SEC agreement alone supplies no statement-year test or complete loan result. Until actual artifacts exist, preserve Not run/null values; report display starts no retrieval, embedding or judging work.

| Field | Value |
|---|---|
| Evaluation run / sample | Not run / not selected |
| Evaluated subject and original artifact | Not selected — original AI output or separately labeled reviewed workflow |
| Original application mode | Not selected — Fixture and Live must remain distinct |
| Task/query and response reference | Unavailable |
| Actual context origin / digest | Unavailable |
| Review-as-of / evidence cutoff / source profile | Unavailable |
| RAGAS package / metric variants / configuration | Not configured |
| Judge / embedding model configuration | Not configured |

## Retrieval benchmark linkage

Retrieval lineage, when an actual saved comparison is available: reference its run, source/query/configuration versions and DIRECT/KEYWORD/VECTOR/HYBRID arm. VECTOR-only is the semantic retrieval baseline; RRF is fusion, not proof that a separate reranker ran. The [benchmark capability/status and reporting requirements](hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision) own the four-arm comparison, per-query ranks/coverage/work and any conditional before/after reranker experiment. Show Not run/unavailable until those artifacts exist; do not manufacture baseline scores or duplicate ranking results as native RAGAS metrics. A future reranked subject must identify its actual variant/model lineage separately. Reading either report executes zero retrieval, embedding, reranking or judging work.

## Native RAGAS scores

| Native metric | Raw score | Native scale | Status | Explanation |
|---|---|---|---|---|
| Faithfulness | — | 0–1 | Not run | No native scoring has executed |
| Response Relevancy / Answer Relevancy | — | Usually0–1; preserve the selected cosine variant's valid[-1,1] raw range | Not run | No native scoring or required evaluator/embedding configuration |
| Context Precision | — | 0–1 | Not run | No evaluated retrieval scope. For an actual unranked DIRECT run, display Not applicable with that reason |
| Context Recall | — | 0–1 | Not run | No evaluated context/reference pair |

Each actual row also exposes the exact native implementation/variant, package version, sample/input hashes and its missing-input/applicability reason. There is no fabricated overall RAGAS score. A measured zero is a score; — means no score. Failed, unselected, missing-input and inapplicable results remain separately labeled. Never convert the custom1–5 ratings below into these native values.

## Custom five-dimension rubric

| Dimension | Score /5 | Status | Explanation and traceable examples |
|---|---|---|---|
| Faithfulness | — | Not run | Required after scoring; quote actual response/evidence and scoped handles |
| Context Relevance | — | Not run | Required after scoring; identify relevant, missing or distracting context |
| Answer Completeness | — | Not run | Required after scoring; identify covered or missing in-scope task points |
| Source Attribution | — | Not run | Required after scoring; show claim-to-source/calculation/policy attribution |
| Response Coherence | — | Not run | Required after scoring; cite actual structure/readability examples |

These are USER-RUBRIC-1.0 scores, not native RAGAS metric values. Preserve evaluator explanations/examples and separately attributed human disagreements. No empty row implies a pass.

## Optional ID-based diagnostics

| Diagnostic | Raw score | Scale | Status |
|---|---|---|---|
| IDBasedContextPrecision | — | 0–1 | Not selected |
| IDBasedContextRecall | — | 0–1 | Not selected |

Populate only from the exact native ID implementation over recorded scoped IDs. These diagnostics are distinct from rank-aware precision, reference-based recall and MET-23 precision/recall@5.

## Independent checks and limitations

Source authority/currentness, exact tier/period/subject, citation resolution, arithmetic, unsupported critical claims, permissions and safe-abstention checks: Not run. An evaluation score cannot waive any failed check or approve a loan. HHH, fairness and compliance certification are not established by this report. For a batch, record each metric's selected/attempted/scored/inapplicable/missing/failed counts instead of hiding absent values in an average.

## Evaluator usage and review

| Work | Observed usage / cost |
|---|---|
| Shared custom-rubric request | Not run / unavailable |
| Native judging requests | Not run / unavailable |
| Native embedding requests / local operations | Not run / unavailable |
| Total evaluator active time and approved allowance | Not run / not configured |
| Human adjudication | Not performed |

Separate evaluator usage from the application's two normal generation calls and preserve all attempts/reservations. Do not print a measured USD0 or zero-token result for work that has not run. No charges were incurred by creating this documentation template.
