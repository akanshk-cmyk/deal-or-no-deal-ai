# Qwen versus Nemotron generation comparison

Contract: GEN-COMPARE-1.0  
Date: 2026-10-23  
Status: User-authorized comparison preparation; paid model execution not enabled

## Decision and scope

The user approved comparing Qwen/Qwen3-30B-A3B-Instruct-2507 with nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B on the same synthetic extraction and synthesis tasks. Qwen remains the baseline candidate; Nano is a challenger, not an automatic fallback or replacement. The selected Qwen3-Embedding-8B model and DIRECT/KEYWORD/VECTOR/HYBRID retrieval comparison are separate. No new agent, judge, generation stage, provider, dependency, UI screen or financial rule follows.

The [Nebius catalog](https://tokenfactory.nebius.com/api/public/models_info) was checked on2026-10-23: Qwen input/output USD0.10/0.30 and Nano USD0.06/0.24 per million tokens. These dated list rates support estimates, not measured review savings or a paid allowance. [Nano's upstream card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) supports reasoning/non-reasoning configurations; the deployed Nebius schema, reasoning controls and billing behavior remain to be verified. Do not assume an upstream flag works on the hosted endpoint or exclude reasoning tokens from billing.

## Paired inputs and scenario readiness

Freeze the same source passages, basis registry, approved role instructions, output schema, reference dictionary, policy/panel versions and original-output cutoff for both models. Record hashes of the exact shared task packet and instruction/schema/source/config identities. Do not put gold answers, reviewer corrections, previous model answers or evaluation notes in either request. Model ID is the intended difference; record identical requested sampling/output limits and actual accepted provider parameters. The current preparation freezes source-grounded E-N01 extraction and synthesis tasks; UTF-8 size is not tokenizer evidence or permission to dispatch.

| Existing development case / task | Current preparation boundary |
|---|---|
| E-N01 default extraction | Verify the registered five-page source pack and construct a shared instruction/schema/source/basis packet; provider/token preflight still pending |
| E-N01 default synthesis | Compact current panel/reference request and exact AI-authored educational fixture rubric are bound; provider/token preflight remains pending |
| E-M01 missing-information path | Source pack/registration pending; no dependent synthesis or invented PanelDecision |
| E-C01 conflicting amounts | Source pack/registration pending; retain both values and withhold unresolved conclusions |
| E-F03 reject-supported | Source pack/assessments and case-specific rubric pending; reject rationale must differ from a missing-information or technical stop |

These reuse existing scenario designs, not newly approved loan fixtures. Do not tune on held-out cases. Missing source/configuration is NOT_READY, never a skipped success. A normal case alone cannot establish risk recall, supported Reject quality or general model superiority. Keep false-positive risk counts beside recall in offline results when the relevant cases are actually executed; do not add a UI indicator.

## Implementation and execution boundary

config/generation_comparison.toml pins the two candidates and dated rate observations, with paid_execution_enabled=false, allowance_status=NOT_APPROVED and provider_contract_status=UNVERIFIED. The offline model_comparison.py helper reads this configuration and the registered source pack, creates two shared task packets (extraction and synthesis), exposes null measurement cells for both arms and blocks unfinished cases explicitly. It constructs no provider client, reads no credentials, performs no network/database operation, and cannot dispatch paid requests. The explicit tools/prepare_model_comparison.py command writes a content-addressed plan under ignored var/evaluations/generation-comparison; stdout contains only status/path/counts. Identical existing artifacts are reused; changed files are never overwritten silently. Read-only source/preflight inspection does not invoke the graph or occupy an application execution claim. Later actual preparation/model/evaluation work sharing app state must use EXEC-ADMISSION-1.0 and a durable usage ledger.

The application Runtime prompts, config/model.toml disabled Live/evaluation flags, E-N01 registration and per-review caps remain unchanged. The command is an offline preparation tool, not a Live runner. Do not add an SDK or run a request just because the key is present. A separately invoked live comparison later needs verified request/schema/tokenizer/reasoning/usage contracts, explicit total requests/tokens/time/USD allowance, safe persisted reservations/outcomes and no automatic retry after uncertain dispatch. Each model receives its own equivalent allowance; running two arms is not one review's two-call budget. Verify P3-05's1000 extraction/350 synthesis starting output targets and all unchanged8000/2000 cumulative review limits; model-specific tokenizers may count the same text differently. Do not truncate evidence or enlarge limits to make a candidate pass.

## Measurements and acceptance

### Authorized quality preparation and response review — QUALITY-REVIEW-1.0

On 2026-10-24 the user authorized the recommended document-understanding and synthesis-quality improvements within the existing architecture. Implement this bounded offline prerequisite before Live activation. Keep two generation stages, Runtime prompt hashes, financial/policy rules, registered Fixture responses, DIRECT grounding and all allowances unchanged. No paid execution, provider client, dependency, automatic repair, judge or application-model switch is authorized by this slice.

1. Prepare extraction through a shared builder that revalidates current registered scope/source/parsed-page identity and full-inventory BASELINE DOCVERIFY coverage. Preserve every original page verbatim, basis metadata, location, source hash and explicit review basis. Byte size is a resource diagnostic, never tokenizer evidence. Do not apply ADAPTIVE globally or use top-k extraction.
2. Extend local extraction review with per-field exact value/basis/reference comparisons, available-slot numerators/denominators, missing/conflict counts and unresolved-reference diagnostics. An existing but wrong-page citation must be visible even when the value matches. Failed outputs retain all available slots in the denominator. These are comparisons to an authored example, not semantic approval or calibrated accuracy.
3. Add synthesis review against the exact current packet. Validate schema and transitive references for every observation, rationale, condition and action reason. Export every narrative target with the full local supporting reference closure, recorded limitations and structured control results for manual review. Re-evaluate amount/confidence/score gates in Python; report unresolved/mismatched routing, never grant clearance. Valid structure/references cannot establish factual support, omission detection or recommendation correctness. Leave narrative scores, risk recall/false positives, grounding and RAGAS null until separately assessed.
4. An explicit offline CLI accepts a bounded local QUALITY-CAPTURE-1.0 record containing canonical attempt UUID, attempt number, selected model ID, stage, exact current task digest, output text, origin FIXTURE_TEST or UNVERIFIED_CAPTURE and completion status COMPLETE/TRUNCATED/REFUSED/ERROR/UNKNOWN. These are local declarations, not a verified Nebius response contract. Only COMPLETE is eligible for structured review; all other outcomes retain failure denominators. Preserve exact original capture bytes and output text before scoring under ignored var/evaluations/response-review/<attempt_id>. Reject changed capture reuse rather than overwrite the original; repairs use distinct attempts. No automatic model attribution, usage/cost estimate, app database mutation or graph execution follows. Store current task input alongside the capture so later source/prompt changes cannot relabel historical results. Normal stdout contains only safe status/path/counts.

Required checks extend existing TEST-002/005/006/007 and MET-03/04/05/07/08/09/16: missing/current-year/basis/reference mistakes; full-source coverage and unverified parser rejection; all narrative paths/unknown or cyclic references; low confidence independently requiring review; schema-valid but false narrative remaining MANUAL_REVIEW_REQUIRED; refusal/truncation/unknown completion; byte-exact first response/history retention; no secrets/network/client/database activity. Run the existing same-input BASELINE/ADAPTIVE layout/disclosure checks and the normal E-N01 regression. Evidence is APPLICATION_TEST or LOCAL_RESPONSE_CHECK_ONLY, never EXECUTED_LIVE. Final provider/tokenizer integration, human support, additional registered cases and optional funded RAGAS remain pending.

Report original first-attempt results separately from repairs/human corrections. Keep every planned eligible attempt in denominators; refusals, malformed/empty/truncated output and timeouts are failures or explicit unresolved outcomes, never credit Reject. Record model/deployment identity, exact input/config hash, valid structured output count, field-value/basis accuracy, unresolved source/basis references, source-grounding review, risk false positives/recall when applicable, total billed input/output/reasoning, requests/repairs, active latency and cost. Unknown usage/cost stays null/unresolved, not zero. Compare paired per-case outcomes and totals; tiny samples cannot establish p95 or statistical superiority.

The local extraction helper reuses parse_extraction and reports conservative exact field-value/basis matches over all31 registered fields, including failed outputs in the denominator, plus unresolved source/basis references. It does not certify that an existing citation supports a claim, and matching the authored answer is not human factual support. Narrative, omission/conflict fidelity and source meaning need the existing manual rubric; no added LLM judge. Its results are LOCAL_RESPONSE_CHECK_ONLY unless linked to verified provider records by a later evaluator. Test-double scores remain APPLICATION_TEST evidence, not measured model performance.

Adopt Nano only after both complete the same ready workload and Nano passes existing critical schema, grounding, missing-data/conflict, routing and supported-Reject checks, without a critical regression, while actual total cost/latency is acceptable within the same caps. Do not introduce a new universal acceptance percentage or decide from model names, upstream benchmarks, confidence or token price alone. Retain Qwen on ties, missing evidence or unclear benefit; a permanent application change requires an evidence-backed selection decision. RAGAS remains optional, separately budgeted, and is not run by this comparison.

## Implementation checks and reporting

Extend existing TEST-002/005/007 and MET-03/04/07/08/09/10/11/15/18 coverage: exact candidate/config tamper rejection; byte-identical shared packet identity for both arms; unchanged instruction hashes; no gold in requests; explicit unready cases; deterministic cost estimates with Boolean/negative token rejection; valid/invalid/duplicate-key/unknown-reference response checks; and no imports/inspection causing network, secrets, database or provider work. Report those as harness correctness, not an executed model comparison.

Current model quality, latency, billed usage and measured savings: NOT_RUN/null. The offline readiness plan contains both E-N01 tasks; the executed normal Fixture path is separate application/workflow evidence; real comparison follows the remaining source/provider/allowance prerequisites.
# Offline provider compatibility implementation — 2026-10-24

User authorized implementation of the pending-work review. Implement PROVIDER-1.0
as pure request preparation and response normalization, tested with injected saved
responses. No SDK, credential read, network dispatch, paid allowance or Live graph
activation follows. Reuse exact DealTermsWire/SynthesisWire parsers and existing
task preparation. Keep raw output for explicit offline capture; never log provider
envelopes or infer semantic support from JSON validity. Only one assistant choice,
expected model, stop completion and complete nonnegative integer usage can be
accepted. Refusal, length/content-filter/tool output, malformed JSON and missing
usage remain explicit non-success states. Completion tokens already include any
billed reasoning tokens; do not add them twice. Rates are dated estimates only.
Configured task token ceilings and protected correction reserve stay unchanged.
Actual model schema compatibility, tokenizer fit and durable funded dispatch remain
pending before a real provider can be wired into the graph.

