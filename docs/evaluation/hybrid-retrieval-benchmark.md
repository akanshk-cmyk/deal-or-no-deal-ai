# Optional Hybrid Retrieval Benchmark

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Version: 1.5
Date: 2026-10-23
Status: Four-arm mechanics implemented; DIRECT/KEYWORD source-ID diagnostics executed; hosted VECTOR/HYBRID semantic comparison pending
Authority: [PRD](../product/prd.md), [RET-1.0 / SPEC-006](../specs/context-optimization.md#shared-evidence-selection-interface-and-optional-benchmark--ret-10), [evaluation plan](evaluation-plan.md)

## Purpose and boundary

Accepted public-source extension: [contract](../specs/public-financial-sources.md) and ADR-007 select local Crawl4AI ingestion, Nebius-hosted embeddings under ADR-008 (model contract pending), and SQLite-backed exact vector search. Optional packages are installed and local-file inspection/CPU import are tested, but the hosted model contract and all retrieval adapters remain unverified/unimplemented/unmeasured; the capability table is unchanged. Freeze a separate public-report corpus/query set and report it apart from the synthetic ten-query workload. Use the same four-arm protocol; no reranker before measured ranking-error evidence. Public references cannot substitute for synthetic annotations or establish a completed loan review.

Compare direct evidence selection, keyword-only search, vector-only search and hybrid keyword/vector retrieval on the same synthetic evidence. Determine whether a later retrieval option preserves required evidence at acceptable context size, latency and total processing/API cost. Do not assume hybrid wins or activate it in the MVP application based on its name.

This is an optional offline extension, not a five-day core acceptance gate, a new user-facing feature or an executed result. The initial implementation plans RET-1.0 and DIRECT; the optional adapters/runner are implemented at a selected later milestone. Graph nodes, agent prompts, calculations, policy gates and UI use the shared evidence contract. No runtime files, dependencies, downloads, indexes, provider calls or measured baseline are created by this document.

## Implementation order and conditional reranker decision

User-authorized recommendation, 2026-10-23: implement and report DIRECT, KEYWORD, VECTOR and HYBRID first, after their reviewed synthetic source documents are ready. Add a separate reranker only if measured results show a ranking problem worth its additional processing. This sets the implementation sequence; it does not execute the benchmark, choose a model, enable downloads or change the five-day core scope.

1. Prepare the reviewed development sources, faithful SEG-1.0 passages, exact source/date/authority scope and ten query annotations. Missing source text or relevance annotations means Not ready; evaluator gold never substitutes for a source passage. M2 starts source authoring, but its first E-N01 pack alone does not establish that all ten benchmark questions are ready.
2. Implement the shared RET-1.0 adapter and DIRECT coverage baseline. Preserve complete required evidence, independent policy authority and the application's planned DIRECT default. M1's context/contract helpers are not an implemented evidence-selection adapter.
3. Implement KEYWORD and VECTOR, then HYBRID over those same candidate lists. VECTOR-only is the semantic retrieval baseline. DIRECT is the unranked coverage baseline. HYBRID's RRF combines ranks; it is not a separate semantic/cross-encoder reranking model. ADR-008 selects Qwen/Qwen3-Embedding-8B on Nebius with dated catalog dimensions/rates; deployed tokenizer/API/limits/usage and an explicit allowance remain pending. No reranker is selected.
4. Execute and save the four-arm comparison using the frozen corpus/questions/configuration and existing cold/warm workload. Inspect per-query failures as well as aggregates. Report relevant improvement, tie or regression against both the coverage baseline and the semantic baseline without assuming a winner.
5. Diagnose a missed-evidence result before proposing a reranker. A useful ranking-error example is eligible required evidence present in the recorded candidate pool but below the final selection cutoff. Evidence absent from that pool, missing source documents, wrong chunks, unsupported annotations, unresolved authority or lost context during packing require their corresponding fixes; reranking does not establish a cure for those failures.
6. If the measured ranking errors justify a follow-up, document affected query/passages, baseline results and the expected benefit versus added setup, compute, latency and any billable work. Define the selected model/revision, compatible dependencies, candidate-pool bound, work/allowance limits and comparison objective before that separately selected experiment under the existing scope/model/setup/spending rules. No universal uplift or latency threshold is invented here.
7. Compare the unchanged HYBRID baseline with the candidate reranked variant on the same frozen eligible candidate pool. Record before/after order, required-evidence ranks, the existing MET-23 recall/precision/packed-coverage outcomes and extra processing. Retain ties, regressions, failures and source/citation violations. Keep the simpler baseline when benefit is not demonstrated or does not justify added work. Application adoption remains a separate evidence-backed decision; benchmark selection never switches the app automatically.

### Capability status and comparison report

Keep specification, implementation, executed testing and measurement separate for each capability:

| Capability | Specified | Implemented | Executed adapter tests | Measured retrieval quality |
|---|---|---|---|---|
| DIRECT coverage baseline | Yes | No | Not run | Not run |
| KEYWORD / BM25 | Yes | No | Not run | Not run |
| VECTOR semantic baseline | Yes; Qwen/Qwen3-Embedding-8B on Nebius selected; runtime/allowance pending | No | Not run | Not run |
| HYBRID / RRF | Yes | No | Not run | Not run |
| Separate reranker | Conditional follow-up only; no model/configuration selected | No | Not run | Not run |

These statuses describe RET-1.0 retrieval components, not M1's passing foundation tests. Update a status only with its actual code/test/result evidence and versions; a design, installed transitive package or test double is not a measured retrieval baseline.

The four-arm report must retain query/corpus/source/config versions; actual candidate passage IDs, component/fused ranks and available raw scores; source-navigation references; required-evidence judgments and exclusion reasons; top-five selection; separately packed context/coverage; existing MET-23 raw counts/denominators; cold/warm/initialization/packing work; measured context size and method; and actual embedding/cache/compute observations. Label DIRECT ranking metrics Not applicable and unavailable/failed results honestly. Do not combine incomparable BM25, cosine or RRF scores or present them as probabilities. Keep source/currentness checks mandatory regardless of average relevance.

If the conditional reranker experiment is selected later, add its exact model/configuration, original candidate-pool identity, before/after ranks, separately labeled model scores and incremental work to that report. Do not silently replace the original four-arm results or present a reranker result when only RRF ran. Results remain local under the existing var/evaluations boundary; no extra dashboard, core metric, TEST ID or automatic model/judge request is introduced. RAGAS answer evaluation remains separately selected work, distinct from a VECTOR semantic retrieval baseline.

## Source applicability shared by every arm

Apply SPEC-006 SOURCEFIT-1.0 before treating any ranked item as applicable support. Each EvidenceRequest/selection records the same ReviewSourceBasis (review date, knowledge cutoff, source profile/policy versions) and exact field/subject/period/qualifier scope; candidate exclusion reasons remain inspectable. Similarity, BM25 or RRF cannot make an expired, later-known, superseded-for-field or unrelated candidate authoritative. Use focused stale/period/authority variants within the existing ten development questions rather than expanding the workload. Unknown material applicability remains unresolved; include date/profile metadata in benchmark cache/config identity and disclose this versioned setup. Same eligibility rules apply to DIRECT and all ranked arms; no source-type precedence or new embedding model is invented, and the planned application default remains DIRECT.

## Controlled comparison

| Arm | Behavior | Setup |
|---|---|---|
| DIRECT | Planned faithful bounded package/direct required-reference lookup | Coverage baseline; no embeddings |
| KEYWORD | BM25 ranking over scoped SEG-1.0 passages | Local benchmark adapter; library/version selected during implementation |
| VECTOR | Dense embeddings and cosine-similarity ranking over those same passages | Semantic retrieval baseline; local model/revision must be configured; exact local search suffices for this tiny corpus |
| HYBRID | Combine KEYWORD and VECTOR ranked candidates with reciprocal rank fusion (RRF) | Same model/chunks/query/scope as the two component arms |

Starting benchmark configuration: each ranked arm supplies at most 10 candidates; HYBRID unions the two top 10 lists, deduplicates passage identity and ranks by sum(1/(60+rank)), with one-based component ranks and zero contribution when absent. Return top 5; ties break by stable scoped passage ID. These are explicit retrieval-experiment defaults, not business rules or proven optima. RRF merges ranks, not incomparable raw BM25/cosine scores. [RRF explanation](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking).

DIRECT is an unranked coverage/context baseline: report its complete evidence/context size, and label ranking-only metrics Not applicable. Do not truncate it to five arbitrary passages to manufacture a comparison. For KEYWORD/VECTOR/HYBRID report top 5 candidates, then separately assemble evidence with necessary parent/definition/table/policy context through the same Python packing rules and request-size preflight. A candidate list that fits does not prove that its complete supporting context fits.

Use the same frozen corpus, source/policy versions, SEG-1.0 profile settings, query text and scope across arms. Restrict sources by trusted deal/revision/selected policy pack before ranking. Do not choose precedence by recency or suppress conflicting clauses. The initial four-arm comparison has no automatic query expansion, extra LLM judge, separate reranker or tool loop. A later reranker follows the measured decision above. This protocol requires no new backend service. A BM25 implementation/package and the selected Nebius embedding model/API/tokenizer/rate contract remains a verification checkpoint; no installed APIs or measured performance are asserted here.

Bound the initial workload to one cold-start pass and one warm repeat over the same ten queries/four arms, at most 80 arm selections; these are still ten unique questions, not twenty quality samples. Reuse corpus/query embeddings between VECTOR and HYBRID and report cache state, initialization and query time separately. No automatic parameter sweep/retry loop. Stop on cancellation, unready model/artifacts or a configured resource/allowance limit; record failed/partial arms independently. A larger corpus/model comparison or a generation-backed experiment is separately scoped work.

## Small representative workload

Author ten retrieval questions over the existing development scenarios/variants. They are question annotations, not ten new loan scenarios or ten generation requests. The frozen workload must cover all four document profiles using reviewed synthetic agreement/term-sheet sections, financial schedules and the selected sample-policy reference text. If necessary source passages are not yet authored, mark the query Not ready; never treat a canned gold answer as a source document.

| Query group | Count | Required evidence |
|---|---:|---|
| Loan agreement | 2 | Repayment/covenant clauses and linked definitions or qualifications |
| Term sheet | 2 | Amount/term and pricing/collateral sections with source identity |
| Financial statements | 2 | CFADS/debt-service inputs and income-statement inputs, with labels, periods, currency/scale and notes |
| Banking-policy references | 2 | Applicable rule text, exceptions/handling and configured version; reference retrieval never executes or rewrites policy |
| Missing evidence, E-M01 | 1 | No supplied passage supports the absent required CFADS; unrelated high-ranking text cannot establish that fact |
| Conflicting clauses, E-C02 | 1 | Both conflicting rate clauses and original/amendment references; no invented precedence |

Query annotation: query_id, case/split/variant, question, allowed source/policy scope/version, required evidence groups expressed as original passage spans, relevant/irrelevant judgments, missing/conflict expectations and reviewer/date. Keep annotations out of prompts, indexes and embedding input. Use development data only; held-out answers remain excluded from tuning. Freeze ambiguous or novel relevance judgments with a versioned reason before reporting scores.

## Measurements — MET-23

- Evidence recall@5: required gold evidence groups fully supported by the top 5 candidates / required groups. A group counts once, despite overlapping chunks; score every required member for linked/multi-span evidence. Report per query, document type and aggregate numerator/denominator.
- Precision@5: relevant returned passages / actual returned passages, at most 5. Human-check relevance against the frozen annotation. Empty returns give Not applicable precision and still fail positive-evidence recall as appropriate; do not label them 100%.
- Complete evidence coverage after packing: queries whose required clauses/definitions/headers/notes/conflicting sources are all present / applicable queries. Report this separately from candidate recall. The packing stage can add related passages but must not conceal poor candidate recall.
- Missing-evidence query: manually check that returned text is not treated as support for absent CFADS. It has no positive gold groups, so recall is Not applicable. Empty search alone cannot prove documentary absence; only the full bounded source review/case annotation establishes that fixture expectation. No unsupported value or decision may be generated.
- Source isolation/citation validity: count wrong-deal/revision/policy/source references, broken locations and lost conflict candidates. Expected zero accepted scope/citation failures; controls remain mandatory regardless of ranking average.
- Efficiency: index/model initialization time, cold and warm query time, packing time, source/chunk/vector counts, index size where measurable, complete packed-context tokens and overflow/stopped cases. Report median and observed maximum for this ten-query workload; no p95 or broad speed claim.
- Cost/work: generation_calls=0 for retrieval-only execution; record embedding operations/input tokens/cache reuse separately, model artifact setup and local resource observations when measurable. Local embedding compute is not free work or observed provider savings. Monetary cost is Not applicable/unavailable where no verified billable service applies, never a fabricated zero-total-cost claim.

A full-context baseline that cannot fit is Not comparable for end-to-end generation, not grounds to raise hard limits. Log failed/partial/not-ready queries and denominators rather than reporting only successful searches. A future paired Nebius generation experiment is separate: it needs approved model/rates/total allowance, the unchanged per-review ceilings and actual model-quality scoring. Reusing fixture responses cannot prove retrieval-conditioned model quality.

## Separately selected RAGAS diagnostics

The user's subsequent [RAGAS-EVAL-1.0](ragas-evaluation.md) addition may consume saved benchmark contexts/IDs, never automatically execute this benchmark or the deal graph. ID-based native Context Precision/Recall0–1 are separately labeled definition/versioned diagnostics over frozen scoped annotations; they are not automatically identical to MET-23 precision/recall@5. DIRECT remains unranked with ranking-only metrics Not applicable; do not invent a top-five order or prune required evidence to improve scores. Custom Context Relevance1–5 examines the actual packed task evidence, including qualifications/conflicts. Native Faithfulness/custom semantic rubric calls run only under an explicitly selected offline evaluation manifest/allowance, separate from the no-generation retrieval workload. No hidden scorer, embedding download or automatic all-case evaluation is introduced. Earlier no-judge wording describes this retrieval-only runner, not a prohibition on the user-authorized separate offline scorer.

## Acceptance and result record

The interface acceptance check is planned TEST-006-09. All comparisons must preserve source scope, source navigation, complete required qualifications and deterministic policy authority. Do not accept an apparent token reduction obtained by missing a critical definition/exception or hiding one side of a conflict.

Report whether hybrid improves, ties or worsens recall/coverage/precision/context size relative to the relevant baselines, with raw counts. No numerical uplift, latency improvement or winning strategy is assumed. A later application-adoption decision requires no critical evidence/control regression and a documented useful trade-off; it is not automatic benchmark behavior. This small author-reviewed set cannot establish general retrieval quality.

BenchmarkResult: evidence_label, benchmark/config/query/corpus/segmentation versions, source scope/digests, embedding model/revision/tokenizer/dimension or Not applicable, arm, candidate/source-span IDs and ranks, group-level judgments and metric counts, packing coverage/token estimate method, timing/cache/embedding observations, errors/stops, reviewer/date and known limitations. Detailed results stay local under ignored var/evaluations; no new dashboard or risk-flagging indicator is required. Persisted artifacts follow the existing no-automatic-expiry rule.

Fixture vectors/test doubles are APPLICATION_TEST evidence only. Actual hosted embedding/retrieval measurements are labeled EXECUTED_RETRIEVAL_BENCHMARK, not EXECUTED_LIVE or a successful end-to-end loan review. All result fields currently remain Not run/Not measured.
