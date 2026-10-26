# Answer-quality evaluation integration

User requested completing the agent workflow and RAGAS. Reuse the existing live
graph, evidence interrupts, readiness gate and USD0.10 shared allowance. Never
grant human evidence support, approve a deal, or insert saved answers into Live
mode to finish a demonstration automatically.

Freeze the original synthesis, its exact generation context and artifact identity
before offline scoring. LIVE subjects use the recorded paid request; FIXTURE
subjects use their registered validated task and remain labeled saved-response
subjects. Evaluator references stay separate from generation context. No-context
or no-response cases remain non-evaluable rather than receiving invented scores.

Implement actual pinned RAGAS 0.4.3 native Faithfulness, AnswerRelevancy (report
label Response Relevancy), ContextPrecisionWithReference and ContextRecall.
DIRECT has no ranked precision. Missing reference/embeddings are explicit statuses.
Preserve native raw values (including negative cosine relevancy), undefined values
and package/variant provenance. No native metric is inferred from ID overlap or a
custom rubric. Cache embeddings by exact model/text/config identity.

The five 1–5 custom dimensions share one structured judge request, with strict
scores, exact response/evidence quotations and known handles validated locally.
All evaluator, embedding and native subrequests have bounded calls/time/size,
durable reservation against the existing allowance, reported usage and no hidden
retry/default provider. Unknown usage retains the reservation and recovery claim.
Separate evaluation cost from the deal ledger; do not enlarge its 8,000/2,000 caps.

Provider verification remains explicit. An API key alone does not verify schemas,
rates or exact generation token fit. The evaluation transport may use a separately
verified full deployed-context token ceiling as its conservative reservation;
this is not a measured prompt count and never replaces review-stage token checks.
New evaluation configuration stays disabled until verified. No paid run on read.

Expose frozen saved results in Agent Activity, with native scores, custom scores,
examples, limitations, usage and subject mode. Evaluation cannot change approval
readiness or human decisions. Offline tests use controlled adapters; label them
APPLICATION_TEST, not live model-quality measurements.
