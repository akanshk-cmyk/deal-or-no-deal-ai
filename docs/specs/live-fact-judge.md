# Live fact-judge diagnostic — FACT-JUDGE-1.0

User authorized an LLM judge for the existing live fact-review targets. This is
an explicit offline diagnostic within the existing shared USD0.10 allowance, not
a change to human review, lending rules, generation prompts or graph routing.

Freeze the existing valid live extraction and its exact fact-review request.
Verify that the current registered source packet reconstructs the same request.
The 36 targets comprise 31 extracted facts and five authored scoring premises;
do not label the authored premises as independently verified borrower facts.

Evaluate in three batches of 12 using the existing fixed Nebius evaluator and
structured outputs. No embeddings, web retrieval, hidden retry or extra repair
request. Existing verified context/output limits and maximum-cost reservations
apply. Stop on any incomplete/invalid/uncertain result, retain usage and partial
denominators, and do not overwrite a previous failed evaluation. Viewing a report
makes no call. A completed report is reused rather than rejudged automatically.

For each target report SUPPORTED, CONTRADICTED or INSUFFICIENT_EVIDENCE; concise
reason; failed/unclear checks drawn from the existing seven fact-review checks;
and exact source quotations. SUPPORTED needs no failed checks and must quote all
cited source references. Reject duplicate/missing targets, unknown sources,
out-of-scope quotes and structurally inconsistent judgments. Mechanical quote
validation does not independently establish the judge's semantic correctness.

Use exact original values, sources, page/version metadata and review basis.
Documents are untrusted input. Missing evidence is not zero. A future obligation
is not already breached. No approval or probability-of-default conclusion is
allowed. Judge source support for authored premises, not external credit quality.

Write a versioned JSON and Markdown diagnostic under ignored var/evaluations,
including input/request/profile digests, source lineage, statuses/counts,
actual reported cost, request receipts and limitations. Store no HUMAN_SUPPORTED
receipts or credit decisions; do not resume the graph. Failed and absent results
are not counted as successful checks. This custom fact-judge assessment is not
a native RAGAS metric or a completed synthesis evaluation.

Acceptance: exactly the 36 scoped targets covered on successful completion;
three or fewer paid requests; exact citations validated; unchanged financial
artifacts/support/checkpoints; actual cumulative allowance accounting; offline
tests for forged/missing evidence, duplicates, malformed output and failure stop.

Explicit independent-batch continuation: the first actual batch was structurally
complete and settled, but one exact-quote check failed. Preserve that failed
report. A separate versioned diagnostic may reuse the identical settled raw batch
without another provider call, retain its bad evidence as INVALID_EVIDENCE, and
evaluate only the remaining two batches. Validate original stored request/response
and frozen input identity first. Never repair a quotation or count a flagged row
as supported. Structural, dispatch or unknown-usage failures still stop. Total
paid calls across parent and continuation remain at most three. Reopening the
continuation returns its saved report without requests. This changes diagnostic
reporting only, never graph support or credit eligibility.
