# Agent Evaluation Instructions

Instruction ID: EVAL-001  
Version: 1.11  
Execution: Deterministic checks/human scoring; user-authorized RAGAS judging only in the explicit separately budgeted offline extension  
Requirements: FR-012, FR-019–020  
Read with: [Shared contract](shared-contract.md) and each evaluated role

## Purpose and evidence labels

Assess whether the future implementation meets the educational scope. Separate application tests from model-quality evaluations. Record Not run/Failed/Passed honestly; this document is not a test execution report. Fixture runs do not establish model quality, inference cost, or live latency.

## Authorized RAGAS extension

The user's2026-10-23 request adds [RAGAS-EVAL-1.0](../evaluation/ragas-evaluation.md) and the separate [RAG evaluator prompt](ragas-evaluator.md). It overrides blanket no-judge statements below ONLY for this explicit offline entry point; those earlier regression fixes/core runtime still add no judge. Preserve five custom1–5 dimensions with explanations/examples: Faithfulness, Context Relevance, Answer Completeness, Source Attribution and Response Coherence. Do not call them native RAGAS scores or overwrite the existing human rubric. Original output/actual generation context/cutoff and separate evaluator references are mandatory. The one-shared-request custom adapter, native metric applicability, strict outputs, versions, zero default dispatch and separate evaluation allowance must be verified before execution. A high score cannot grant HUMAN_SUPPORTED, approval or HHH certification. No RAGAS model/package has run; report manual/controlled/native/custom origins honestly.

## Core acceptance and extension

For retrieval, follow the [source-ready/four-baseline/conditional-reranker decision](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision): implement and report DIRECT, KEYWORD, VECTOR and HYBRID before considering a separate reranker. VECTOR-only is the semantic retrieval baseline; DIRECT is unranked coverage; RRF is fusion. Record specified/implemented/tested/measured status, actual candidate ranks, per-query MET-23 counts/coverage and processing work. Diagnose missing-source, candidate-recall and packing problems separately from eligible evidence ranked below the cutoff. A conditional reranker comparison needs the same frozen candidate pool and before/after quality plus incremental work; no presumed uplift or new threshold. Retrieval, native/custom RAGAS and model-generation results stay separately labeled and separately selected. All retrieval measurements remain Not run; M1 tests are foundation evidence only.

Follow the [evaluation plan](../evaluation/evaluation-plan.md): core E-N01/E-P01/E-M01 walkthroughs, E-N01/source-backed correction and E-F03/reject-supported QA variants, focused critical controls and one operator's five tasks/learning checklist. The thirty-case corpus, ten-case batch, held-out model-quality study, three-person usability study and thirty-completion p95 protocol remain optional extensions. Later at least one separately authorized validated Live integration run remains required. No observed result is implied.

## Dataset and split

Thirty designed synthetic scenarios in the extension inventory, with golden facts, formulas, rule versions/outcomes, supported risks/abstentions, evidence labels, expected review branch, and terminal/partial state:

| Category | Development | Held out | Total |
|---|---:|---:|---:|
| Normal supported cases | 3 | 2 | 5 |
| Policy exceptions | 3 | 2 | 5 |
| Financial edge cases | 3 | 2 | 5 |
| Missing information | 2 | 2 | 4 |
| Conflicting documents | 3 | 1 | 4 |
| Invalid documents/tool failures | 2 | 2 | 4 |
| Injection/permission attempts | 2 | 1 | 3 |
| Total | 18 | 12 | 30 |

Do not tune against held-out answers. Exhaustive arithmetic/schema/boundary unit cases can be additional local tests; they are not fabricated extra independent loan scenarios.

## Acceptance metrics and denominators

| Measure | Definition | Target |
|---|---|---|
| Financial arithmetic | Golden results/validity outcomes correct divided by agreed deterministic cases | 100% |
| Sample policies | Correct rule outcome/route divided by agreed deterministic cases | 100% |
| Extraction accuracy | Correct normalized extracted field slots divided by annotated available slots; abstention counts incorrect here | >=95% |
| Critical unknown/conflict handling | Required critical cases correctly detected and paused/withheld divided by those cases | 100% |
| Accepted schema validity | Accepted stage outputs conforming to the contract divided by accepted outputs | 100% |
| Material risk recall | Supported expected material risks identified divided by annotated expected material risks | >=90%; no missed critical control exception |
| False-positive risks (MET-22) | Manually count unsupported/irrelevant risk findings against each synthetic case; count duplicates once | High-level offline QA note only; no UI indicators, extra model call or precision threshold |
| Evidence support | Material model claims with resolving, supporting evidence divided by scored material claims | >=95% broader target; zero accepted unsupported critical claims |
| Review/permission gates | Correct required branch, permitted action, no bypass, stale rejection divided by critical controlled cases | 100% |
| Report template | Seven sections, unchanged facts, visible gaps, cutoff and provenance correct divided by template cases | 100% |
| Inference controls | Recorded actual requests/usage versus allowed stages and cumulative ceilings | Two normal successful live calls, max five cumulative attempts; zero fixture/Python/HITL/report inference |
| UI | Screen-specific/cross-screen criteria in PRD 4.3 | All agreed critical checks pass |

Also measure citation coverage independently: every material claim needs a reference or an explicit unsupported/withheld label. Structural citation existence is not semantic support.

## Human narrative rubric

UX-1.0 usability is the five UX-T01–05 tasks in the evaluation plan: locate attention deal, explain issue/owner/action, inspect evidence and return, perform a source-backed correction with impact/staleness understanding, and distinguish memo recommendation/review/completion. Record duration/hesitation/help/errors and author self-assessment honestly. The separate 5/5 learning checklist remains; neither headless UI tests nor document review proves external-user usability or accessibility compliance. Offline QA/benchmark results do not become new dashboard requirements.

Score factual faithfulness, evidence support, material-risk coverage, appropriate conditions, and clarity/uncertainty on a documented 1–5 scale. Proposed accepted target: mean >=4/5 with no critical factual/control error. Use one consistent reviewer rubric; note reviewer qualifications/limitations.

Golden decision evaluation may specify a permitted label set plus required rationale/conditions rather than demand exact narrative wording. Do not reward a technically failed run for inventing Reject. A missing-data scenario passes by reaching the correct pause/partial state, not by fabricating a finished recommendation.

Check reasonable novel risks against evidence rather than automatically calling them false. Keep the two QA checks high level and offline. Detailed precision/adjudication tooling is deferred; unsupported critical allegations still fail existing evidence controls. Use deterministic/human checking only.

## Original model quality and engineering regressions

Follow EVAL-CUTOFF-1.0 in the evaluation plan. Freeze original wires/attempt lineage and the first accepted model artifact before human fact/condition/disposition edits. MET-03 counts an E-N01 documented CFADS omission even after the corrected workflow passes; genuine E-M01 absence is missing-data handling, not invented available-slot success. Score original Synthesizer conditions/rationale separately from human-edited reviewed reports. Include stopped/refused/invalid cases, accepted-output conditional denominators and repair counts; no empty or unavailable-output pass. Runtime support never reads evaluator gold. Cache reuse is not a new inference sample.

Use the plan's AE-01–07 regression table and existing ninety TEST IDs for compact wire/authority, exact fingerprints, receipt-based resume/lifecycle, multi-page coverage, provider refusal/usage, explicit state clears and evaluation cutoffs. Document checks and controlled responses do not prove pinned LangGraph/Nebius compatibility, actual token fit or Live quality. Keep all unexecuted checks Not run; no extra paid batch/judge/dashboard.

## Source relevance and historical correctness

Apply the evaluation plan's SOURCEFIT-1.0 focused variants using existing cases/test IDs/metrics. Cover governing-source versus newer secondary upload; historical cutoff with later knowledge excluded; verified earlier capture versus actual ingestion; rate/APR/APY and tier/period noncomparability; ended/future applicability; partial amendment scope; unknown authority/dates; policy-purpose applicability; cache invalidation on date/profile change; and source-selection reasons visible in existing citations/memo. An older but explicitly applicable historical-period input is not automatically stale. Keep current application revision separate from business validity and preserve no-automatic-expiry. Do not turn user-supplied retail examples into observed market values, a crawler, extra scenario inventory or a paid benchmark. No evaluator gold supplies runtime authority.

Use the plan's authorized Director-fix table within existing test IDs: NARRATIVE-CHECK-1.0 all-field target coverage and per-field unsupported assertions; INPUT-EDU-1.0 duplicate/escaped keys and exact resource/numeric boundaries without clamping or false rejection; SOURCE-TRIAGE-1.0 owner/action and honest source/policy counts; CONTINUE-CHECK-1.0 planned versus actual9/11 and7/9 counts, pending resume2, reviewed11+9=20 and safe overrun without double charging. The original normal example has four narrative targets; a one-condition response with proposed action has six. Valid negative/zero/repeating values remain valid under their existing field/formula rules. No new case inventory, paid judge, metric or automatic benchmarking. Core implementation begins with E-N01's actual fixture graph, then the existing pause/review/correction/Reject variants; report all runtime checks Not run until executed.

## Essential cases

The authorized SME regression table in the [evaluation plan](../evaluation/evaluation-plan.md) adds focused variants to existing checks, not another scenario count or judge agent. Cover registered-complete versus unregistered-partial intake, borrower/entity/facility coherence, current critical Live FACT support versus claim review, support-only same-revision continuation without extraction replay, CONDITIONS-1.0 with outstanding proposals versus mandatory prerequisites, covenant EXTRACTED_NOT_EVALUATED, deferred reported-EBITDA normalization/reconciliation and annual-only analysis without balloon/full-term inference. Keep90 existing planned test IDs, thirty scenario designs and five UX tasks; new executions remain Not run. A fixture or document check cannot supply observed Live support/quality.

- Optional [hybrid retrieval benchmark](../evaluation/hybrid-retrieval-benchmark.md): compare DIRECT/KEYWORD/VECTOR/HYBRID through RET-1.0 on the same ten development-source questions; preserve scope, policy authority, complete supporting context and source references. Actual local retrieval measurements are EXECUTED_RETRIEVAL_BENCHMARK, not Live generation/model-quality evidence. No additional runtime prompt, risk-flagging UI or automatic model download is introduced.
- [E-F03/reject-supported](../evaluation/examples/e-f03-reject.md): valid negative CFADS/DSCR with positive EBITDA, supported case-specific Reject, mandatory handling and Approver review, final report; distinguish E-M01 pause/E-T03 fault and never make every breach Reject.
- [E-N01/extraction-miss](../evaluation/examples/e-n01-correction.md): original evidence supports correction; E-M01 genuinely absent input stays paused; adapter matches current stage inputs.
- DSCR 1.25 and just below; leverage 4.00 and above; equipment LTV 80% and above; term 60 months and above.
- Requested amount below/exactly/above USD 10M and confidence below/exactly/above 0.7, before display rounding.
- RISK-EDU-1.0 exact aggregation and material-source prerequisites; SCORE-BANDS-1.0 classifies unrounded totals, including25.5 Moderate and50.004 High despite50.00 display. Missing material factor/input is Insufficient Data, null total/band, no reweighting or dependent synthesis.
- SCORE-ROUTING-1.0: Moderate always normal human review; High separate Credit Risk Manager handling then package review; Very High senior-tier Approver; Low never clears independent policy/evidence gates. Tier/capability/current-lineage guards and no repeated resume loop.
- Three independent cards with deduplicated exception/missing-requirement counts, explicit unknown/not-run and factor coverage as detail.41 Moderate/two exceptions/one missing is coherent only for a non-score-material evidence gap. Required action is Python output; optional AI proposal needs accepted current synthesis. No additional stage/call or fake score for a walkthrough whose factor pack is not yet authored.
- Retired USD-4M trigger does not execute; other mandatory referrals still can.
- Zero/nonpositive denominators, incompatible periods/units, unknown liens/value/methods, and conflicting amount/rate.
- Unsupported citations, injected instructions, invalid schema, duplicate/stale operations, wrong persona/unmapped capability.
- Original model recommendation versus human conditions/disposition; unresolved block cannot be generically waived.
- Fixture versus live failure, budget/timeout/cancel, uncertain requests, graph-only mode, independent deal state.
- PRD UI-DASH/NEW/WORK/ACT/MEMO checks, generated report/sample lineage, and actual handoff events.

## Latency, cost, and stopping

Measure on a defined workload/model/prompt/version and report run count, fixture/live mode, concurrency, failures, retries, cache status where known, active time, and human wait separately. The p95 <=90-second processing goal remains unmeasured until a sufficient agreed timed protocol is funded/executed. A single live smoke test cannot establish it.

USD 0.10 is a target and USD 0.25 the configured per-review hard ceiling, not provider price quotes. Verify dated model/tool rates before paid work. A paid evaluation batch requires its own total allowance; do not assume all thirty scenarios or repeated timings are authorized.

Development/acceptance split, thresholds, and tests are specified here; no cases, fixtures, test code, measurements, paid calls, or reviewer scores are created by this document.
