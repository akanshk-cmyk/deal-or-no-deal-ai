# AGENTS.md — Deal or No Deal AI

**Current embedding decision — 2026-10-23:** [ADR-008](decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. The deployed API/tokenizer/input limits and paid allowance remain unverified; execution/indexing stay disabled. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

Document status: Source draft preserved; root copy activated for approved M1 on2026-10-23; this documentation copy remains inactive
Intended destination: repository-root AGENTS.md
Activation: copy to the root only in an approved scaffolding milestone; replace this draft status with the recorded approval date. This documentation copy is not active workspace policy.
Source proposal: docs/architecture/repository-design.md

## Project purpose and source of truth

Build a local educational financial-deal review demonstration over synthetic USD term-loan documents. The tagline is “Every deal has a story. Our agents find the plot holes.” This is not real lending, legal/compliance certification, screening, investment advice, a payment/trading system or production banking software.

Read the current user request and approved documents before changing behavior:
- docs/product/prd.md — required product outcomes and boundaries.
- docs/architecture/hld.md and docs/architecture/decisions/ — architecture.
- docs/specs/overview.md and the relevant SPEC-001–012 file — exact contracts and accepted P3 decisions.
- docs/agents/shared-contract.md and only the relevant specialist file — role/calculation/policy behavior.
- docs/evaluation/evaluation-plan.md and docs/traceability.md — quality definitions, case split and planned checks.
- docs/execution.md and docs/design/design-system.md — milestone/design rules once approved.

Existing user authorization persists. Follow the approved phase sequence and the current milestone; do not ask again for routine implementation choices already authorized. If a material spec conflict or unapproved business rule blocks work, identify the affected requirement/decision and propose a concrete edit for review. Never silently choose an archived or more convenient rule.

Phase 3 was accepted on 2026-10-22. Repository approval does not automatically approve Phase 5's first implementation milestone, paid inference, publication, external deployment or a project license. Check recorded approvals rather than inferring them from installed tools or a present key.

## Architecture and navigation

Current public-reference decision: active root AGENTS.md and accepted ADR-007 as amended by ADR-008 select local-file intake, Nebius-hosted embeddings under ADR-008 and SQLite-backed exact vector search. Source and architecture approval are resolved; setup/runtime checks remain pending. This copy stays inactive, and its older synthetic-only/network-only-Nebius wording must not override the scoped public-reference exception in root policy. No automatic downloads, paid service or loan strategy change.

One source-checkout Python app: app.py is a thin Streamlit entry point; src/deal_or_no_deal_ai contains shared contracts/domain/services; ui/ has five screen modules. config/ contains trusted nonsecret versions/policies; docs/agents is the sole role-instruction source. fixtures/development and fixtures/held_out contain reviewed synthetic inputs/model-stage fixture responses/gold labels. tests/ contains application tests; notebooks/ renders the shared graph; prototype/ contains the offline walkthrough template/assets; var/ is ignored local state/output.

Use one LangGraph definition with explicit typed state and one user-started execution worker. Services enforce persona, scope, revision, idempotency and gates. Keep SQL and checkpointer ownership separate in the same SQLite file. Do not introduce a REST server, second database, ORM/migration framework, queue, distributed agents, vector service, voice SDK or external app connector without a justified approved change.

Node mapping:
- Agent 1: Extractor, first normal model task.
- Agent 2: Compliance, deterministic sample-policy checks.
- Agent 3: Risk & Summary, composed of Python Risk Quantifier plus Synthesizer, second normal model task.
- Supporting specialists: Financial Analyst, Evidence Reviewer, Memo/Report Generator.
- Orchestrator: deterministic delegation, joins, routing, budget and failure guards.
- Intake and Human Review are control responsibilities.

Keep all seven specialist outputs inspectable. Named specialist files/nodes do not justify extra LLM calls.

## Coding and change conventions

Historical draft gates below are superseded by the active root AGENTS.md: pypdf6.21.2 is installed/locked; the user approved A1-A4 and E-N01's exact default source/assessment slice is registered under CASE-REG-1.0. Qualified finance/policy/risk handlers and85 combined application methods pass. Do not repeat fulfilled approvals. Generic uploads, full graph/synthesis/UI and paid-model work remain pending. This documentation copy remains inactive.

Use Python 3.12 only after the approved interpreter/dependency check. Use uv and the committed lockfile rather than unrelated package managers or untracked ad hoc installations. Dependency versions and project-specific CLI commands must match the actual manifest/implementation, not guessed APIs. Use the minimal approved dependency set; document any requested addition and its purpose/license implications.

Make small changes tied to a SPEC/FR and planned TEST ID. Keep graph nodes thin and domain functions independently testable. No speculative framework, duplicate financial engine or parallel infrastructure. Start with ordinary modules; split only for demonstrated size/responsibility reasons. Preserve archives and unrelated user changes.

Pydantic trust boundaries reject extra properties, nonfinite numbers and Boolean/numeric coercion where prohibited. Decimal values serialize canonically. Use FIN-1.0, approved periods/bases, precision/display settings and exact threshold comparisons; never derive missing financial inputs from assumptions. Missing is not zero. Concentration remains Not assessed; no PD or unapproved score. RISK-EDU-1.0 is the sole educational aggregation: five supplied synthetic assessments weighted30/20/20/20/10%, Decimal contributions/total, no reweighting. Missing material factors/inputs yield Insufficient Data with null total/band and pause dependent synthesis/readiness. SCORE-BANDS-1.0 classifies unrounded totals before display. SCORE-ROUTING-1.0 requires Moderate normal human underwriting, High Credit Risk Manager handling then package review, Very High senior-tier Approver review; preserve independent gates and five personas. Compute in the existing Python risk node. Supply a bounded supported score/band/driver projection to the existing Synthesizer call; optional proposed_action belongs outside exact five-field PanelDecision and never authorizes an action. Three read-only assessment cards separate score, policy exceptions and missing evidence; factor coverage is explanation only. Never infer ratings, invent bands, add credit-data APIs or turn41 Moderate into41% PD/approval. Preserve source/configuration/revision lineage and invalidate dependent review on corrections. TEST-004-10/11 and existing UI/HITL tests cover deterministic arithmetic/control/display, not predictive calibration. Viewing performs zero scoring/inference.

Use SAMPLE-LOAN-POLICY-1.0. SYN-ESC-003 is retired and its historical ID reserved. Requested amount >=USD10M OR validated confidence <0.7 OR active score referral OR other mandatory referral controls Python routing. Score referrals are separately versioned DEMO_PRODUCT_CONTROL records, excluded from policy-exception counts. Confidence is uncalibrated; model recommendations cannot waive a gate. Apply P3-01 status aggregation without discarding issue scope/history.

Implement RULEVIEW-1.0 as the policy handler's recorded condition trace plus a scoped read projection into existing UI details. Show exact versioned predicate/applicability/operands/calculation/source and distinct result/workflow consequence, including compound grouping and unevaluated/Unknown/Not applicable/stale states. View rule evaluation performs no financial/policy recomputation, graph/tool/model call or mutation. Never add a UI-side evaluator, editable rule DSL, generic validation stamp or imported screenshot thresholds/integrations. Trace/version mismatch must remain explicitly unverifiable; correction and permitted support/disposition actions stay separate. Preserve source/rule reference navigation in the static HTML using labeled snapshot data.

Apply P3-02 and SPEC-008 capabilities in services and UI. Acknowledge, record a supported sample exception, record High-score credit-risk handling, apply an allowlisted synthetic control fixture, and record final package disposition are different actions. NORMAL cannot satisfy SENIOR review tier; generic Approve cannot clear missing sources or specialty/integrity blocks. Administrator has no automatic financial/compliance approval authority. Preserve original PanelDecision separately from HumanDisposition.

Follow the authorized SME fixes in SPEC-001/002/003/007/008/009: complete walkthroughs use registered reviewed source/assessment/subject packs; unregistered Live uploads are partial with no borrowed scores/PanelDecision. Match borrower/entity/facility and basis before trusted use. Critical Live facts require current source-backed FACT-SUPPORT-1.0 through typed FACT/CLAIM support targets; KNOWN and a resolving citation do not imply HUMAN_SUPPORTED. Support Save invokes no graph/model or fact edit; explicit same-revision continuation uses the same ledger at the earliest affected stage, never extraction replay or stale review tokens. Conditions retain provenance/category/owner/status and existing-issue-derived blocking; outstanding proposals cannot waive current evidence or imply fulfillment/funding. Covenants are extracted, not automatically evaluated; annual-period analysis does not establish full-term/balloon/refinancing adequacy. Reported/adjusted-EBITDA normalization/reconciliation is deferred; keep the eighteen-field wire and FIN-1.0. No extra agent/node/call/database/screen or expiry policy is introduced. Reuse existing focused tests and source-case variants; report document checks separately from runtime evidence.

Fact/source/control corrections create analytical revisions, invalidate affected results and stale acceptance, and rerun only approved dependencies in a new run/thread with the same review_id and cumulative allowance. Do not resume stale interrupts with changed analytical data; only review-only handling uses the same pending thread. Notes/ownership/conditions-only human handling do not silently rerun unchanged model work.

Follow [UX-1.0](../specs/command-center-ui.md#simplicity-attention-and-interaction-contract--ux-10): keep five screens, a five-column default Dashboard, three-step intake, Workspace-first issue/owner/action with every mandatory blocker, paired evidence and progressive technical detail. Preserve separate recommendation/review/report labels and seven report sections. Use the existing service-derived action availability; no new permission/policy engine. Read-only correction impact and Save spend no model work: Save prepares READY state and invalidates dependent output, then an explicit permitted continuation queues work. Preserve focus, selected finding and readable field/status errors. Core usability follows UX-T01–05 with honest self-assessment; offline QA/benchmark results remain outside the UI. Detailed visual tokens/components belong to the approved Phase5 design-system work, not speculative new dependencies.

No key/provider client/database mutation during import, graph construction, screen reads, source inspection or notebook diagram rendering. Network I/O occurs only inside the authorized lazy Nebius adapter. The one worker invokes plain services, never Streamlit UI functions. Refresh must reuse persisted run/service identities.

## Context, inference and budget controls

Retrieval implementation order: after reviewed synthetic sources and frozen query annotations are ready, implement and report DIRECT, KEYWORD, VECTOR and HYBRID first. VECTOR-only is the semantic retrieval baseline; DIRECT is the coverage baseline; RRF is rank fusion. Consider a separate reranker only after measured candidate-ranking failures demonstrate a useful quality versus added-processing trade-off. Follow the [canonical sequence, capability status and report decision](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). Keep specified/implemented/tested/measured states distinct. M1 foundation tests and installed transitive packages are not implemented or measured retrieval. No automatic model download, new runtime call or app-strategy switch is authorized. This documentation copy remains inactive; the root AGENTS.md is the active implementation instruction.

Only Extractor and Synthesizer normally invoke models. Read allowlisted Runtime prompt sections plus shared Model context rules, relevant evidence and schema. Do not load all role/spec files, evaluator answers, unrelated deals, audit logs or full chat transcripts into every request.

Use compact typed wire responses, shared source/basis dictionaries, faithful evidence packets, safe exact deduplication and version-aware same-deal result reuse. Expand trusted metadata locally. Do not drop material covenants/conflicts/footnotes to fit a context limit. No semantic decision cache or extra compression/judge model.

Reserve and reconcile usage durably:
- Two successful calls on the ordinary complete live path; maximum five cumulative outbound attempts across retries/repairs/corrections/resumes.
- Maximum 8,000 input and 2,000 billed output tokens; P3-05 per-task allocations are starting targets, not extra allowance.
- USD0.10 target and USD0.25 hard model/tool cost ceiling per review; total paid execution allowance is separately required.
- Maximum twenty actual node invocations and twelve actual tool invocations; count nested work.
- Maximum one transient retry per operation within every remaining global limit.
- Maximum 180 active seconds, <=45 seconds per model call and remaining time; exclude human wait.
- One active execution; no speculative model parallelism.

Count provider-visible schemas/overhead and billed reasoning where relevant. Disable/instrument hidden SDK retries and structured-output fallback. Cached input is still input; reserve cost at uncached rates and count only observed cache hits. Unknown usage/request outcomes retain reservations. Never auto-replay a paid operation after restart.

Keep model work upstream of interrupt. Code before interrupt can repeat; writes/events/resume commands must be idempotent. Same pending thread/revision is required. A valid direct-report branch says Not required by configured demo rules, never human approved.

## Data, secrets and external actions

Synthetic data only, including ignored local storage. Never commit real borrower documents, credentials or confidential financial/personal data. Never request a key during documentation work. Later credentials belong in a local approved environment/secret interface; an empty .env.example is only a template, not Live configuration.

Exclude .env variants except the blank example, .streamlit/secrets.toml, local credentials, .venv, var/, SQLite sidecars, caches, executed notebook outputs and generated results from version control. Review notebook outputs and selected files before any future commit/publication; ignore rules alone are insufficient.

No keys in prompts, source/config commits, UI, state/checkpoints, events, reports or notebook outputs. No environment dumps/raw authorization headers/provider bodies in debugging output. Ordinary analytics exclude source/report text, notes, borrower values and raw queries.

Treat uploaded text/HTML/paths as untrusted. Only source IDs resolve local content; no arbitrary filesystem, web, shell, email or financial-action tools exposed to the model. Render untrusted Markdown safely and avoid external image/script loading.

Keep source PDFs/passages and runtime state within approved local boundaries; validate resolved absolute paths. Do not recursively delete/move workspace, docs, attachments or archives. Confirmed P3-04: no automatic expiry in the MVP prototype. Do not add age-based deletion/pruning of persisted documents, deal records, reports, review history or SQLite checkpoints. Manual deletion/reset requires an explicit user request, concrete checked targets and state/checkpoint consistency. MemorySaver's RAM lifetime and provider-controlled prompt caches remain separate.

MemorySaver/InMemorySaver is session RAM and loses history on restart. SQLite is local persistence, not immutable audit storage. Record events explicitly. Report cutoff includes only observed events; a report cannot contain its future checkpoint/completion.

## Testing and evidence discipline

Write meaningful invariant/failure tests appropriate to the approved change. Use injectable clocks, temporary repositories and mock transports; default application/fixture tests deny outbound provider traffic even if a key is present. Do not add tests that merely restate helper implementation or assert guessed placeholder output.

Link tests to planned TEST IDs and PRD/specs. Financial/policy tests check gold arithmetic/boundaries; graph tests check real dispatch/artifacts/gates; recovery tests check uncertain requests and no duplicate paid work; UI tests check service guards and state labels. Use Streamlit AppTest where supported and manual accessibility/offline-browser checks for what it cannot establish.

Fixture mode executes actual graph/Python logic but supplies only registered matching Extraction/Synthesis stage fixtures. Fixture matching also requires the registered variant and normalized current-stage input digest after corrections. An arbitrary uploaded document or unmatched edit cannot receive a canned success. Failed Live requests never silently switch to Fixture or another provider.

Application tests are not model evaluations. Keep eighteen development and twelve held-out scenarios separate; do not tune prompts on held-out answers or include gold labels in model context. Report author exposure/limited blindness. Actual model accuracy/support/risk recall requires the separately funded evaluation protocol and honest failure denominators.

Plan RET-1.0 from the first context implementation: ordinary Python evidence-selection protocol, injected DIRECT adapter and unchanged ContextPacket for graph/agent consumers. Optional BM25/vector/RRF adapters are confined to retrieval_benchmark.py and the offline evaluation entry point. The app remains DIRECT; no model/index creation or downloads at import/startup/Fixture/notebook time. Do not use top-k search for complete extraction or let reference retrieval override executable policies. Benchmark adapters return the same scoped source-backed result, with no query-rewriting/generation call or automatic provider fallback. Record actual local comparison evidence as EXECUTED_RETRIEVAL_BENCHMARK; fake vectors test contracts only. Follow [the benchmark protocol](../evaluation/hybrid-retrieval-benchmark.md); later backend implementation/configuration still needs its scoped tests and approved dependency setup, even though graph/agent code stays isolated.

Report exact commands, scope, pass/fail/not-run, failures and limitations. Distinguish DOCUMENT_REVIEW, APPLICATION_TEST, EXECUTED_FIXTURE, EXECUTED_LIVE and ILLUSTRATIVE. A static link check is not an application test. A fixture run is not live model quality or provider latency evidence. One live smoke test is not p95 validation. Never claim tests or integrations ran when they did not.

## Commands proposed for approval

These commands become approved conventions only after the repository proposal and relevant milestone are accepted and target files exist. During draft review, do not run them or infer setup/build success. Package downloads may require environment approval; provider spending remains separate.

| Purpose | Proposed command |
|---|---|
| Foundation setup | uv sync --group dev |
| Local application | uv run streamlit run app.py --server.address 127.0.0.1 |
| Unit/integration checks | uv run pytest tests/unit tests/integration |
| UI/presentation checks | uv run pytest tests/ui tests/presentation |
| Development fixture suite | uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split development --output-dir var/evaluations |
| Full fixture suite | uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split all --output-dir var/evaluations |
| Notebook setup | uv sync --group dev --group notebook |
| Local notebook UI | uv run --group notebook jupyter lab --no-browser --ip 127.0.0.1 |
| Graph-only executed copy | uv run --group notebook jupyter nbconvert --execute --to notebook --output-dir var/notebooks notebooks/01_workflow.ipynb |
| Offline presentation artifact | uv run python -m deal_or_no_deal_ai.presentation --run-id RUN_ID_FROM_ACTIVITY --output-dir var/presentation |
| Local package build | uv build |

RUN_ID_FROM_ACTIVITY is a placeholder for a real executed fixture run. No npm/frontend build is needed. A Python wheel alone is not a self-contained deployed app: prompts/config/fixtures are resolved from the reviewed checkout. Do not publish built artifacts or launch external hosting.

Do not run unavailable suites or quietly skip required checks to report success. After initial setup/lock generation, use the committed lockfile; investigate unexpected dependency changes before accepting them. Do not invent a Live command or run a funded benchmark through normal test discovery.

## Human approval boundaries

Continue autonomously within an approved milestone. Approval is required for a changed business formula/threshold/capability/status rule, material source-of-truth conflict, new provider/model or increased allowance, paid/external service activation, project-license choice, external repository/publication/deployment, destructive reset or new sensitive-data handling. Do not repeatedly ask about an action already explicitly authorized in the session.

The parser-license/API checkpoint remains unresolved until recorded: existing PyMuPDF candidate is dual AGPL/commercial, and no license path/purchase or replacement is silently selected. Do not install/adopt it before that checkpoint. No other dependency license is assumed acceptable solely because the project is educational.

Before requesting a new decision, finish the authorized reversible work needed to make it concrete and reviewable. State the exact spec/approval condition and practical impact. Do not use a request for permission to leave already authorized work incomplete.

## Definition of completion and reporting

Complete only the approved milestone and its required checks. Explain what changed, linked requirements, actual validation and remaining risks. Report incomplete provider/model/license/dependency decisions explicitly. A screenshot, static graph or prewritten report does not substitute for the working delegated pipeline.

Final educational-demo acceptance requires three core fixture walkthroughs plus E-N01 source-backed correction and E-F03 supported Reject QA variants, the agreed critical application/evaluation checks, shared offline Jupyter graph, clickable HTML walkthrough, actual generated source-linked sample report and later validated Nebius integration with proper usage/evidence. No claim of production readiness, bank compliance or measured business savings follows from this prototype.

## Authorized review-fix instructions

Follow the subsequent Principal fixes in their canonical feature contracts: exact DealTermsWire-only Extractor Runtime prompt (SPEC-002/agents/extractor); REVIEW-BASIS-1.0 and pre-disposition condition drafts (SPEC-008); cross-entry-point EXEC-ADMISSION-1.0 (SPEC-007); and exact STATE-CODEC-1.0 (SPEC-011). Do not copy the full development contracts into a provider prompt. Compare the actual loaded prompt/schema/examples and expected instruction hashes; never allow notes/domain metadata or Unknown strings in place of declared wire fields. Do not mistake valid specialist review progress for changed loan analysis or regenerate unsupported condition targets after accepting the disposition. All execution entry points sharing the local database use the same durable admission claim, not just a per-process lock. Preserve exact checkpoint numbers/types/fingerprints and null-clearing semantics, with no pickle fallback or automatic recovery/migration. Extend the existing first-milestone compatibility/regression families and report actual evidence honestly. These are approved specification fixes, not activation of this draft or approval to scaffold/run paid services.

The user's later RAGAS-EVAL-1.0 request supersedes blanket no-judge wording ONLY for the explicit offline evaluator. Implement the optional lazy dependency/config/custom metric adapter at its approved milestone, with one shared five-dimension1–5 bundle, exact examples, separate native metrics and separately approved evaluator allowance. Verify pinned APIs/Nebius/model/token/rate/call behavior; never use a library default OpenAI client or silently invoke a scorer on import, Fixture tests, app refresh, report rendering or graph-only notebook. The application loader retains two prompts; the offline loader alone reads docs/agents/ragas-evaluator.md. Preserve exact original context versus evaluator-reference separation, original-output cutoff, failed denominators and read-only deal-state isolation. No score grants authority/support/approval. Actual RAGAS execution is labeled only when the installed package/adapter ran; no package or evaluator request has run during this documentation task.

Apply the user-authorized Director fixes in existing modules: NARRATIVE-CHECK-1.0 registers targets for all observations/rationale/conditions/action explanations; INPUT-EDU-1.0 rejects nested/escaped duplicate keys and out-of-profile JSON/numbers before hydration, preserving original values and exact routing confidence; SOURCE-TRIAGE-1.0 uses existing owners/services with no new clearance powers; CONTINUE-CHECK-1.0 uses a small path-count table and actual shared ledger, with no double-charged estimates or hidden node merging. Reference checked does not prove semantic truth; support and credit disposition stay separate. Preserve technical-versus-lending-error distinction, node-versus-model-cost distinction, budgets and history. After the relevant gates, prioritize one actual E-N01 fixture slice and expand to the agreed core cases; do not require optional benchmarks or introduce another framework. This draft remains inactive until approved scaffolding.

Apply SPEC-006 SOURCEFIT-1.0 to source applicability: exact deal/subject/period/value type/qualifiers, explicit review date/evidence cutoff and reviewed field-specific authority/supersession. Preserve verified historical capture separately from ingestion and never infer effective/available dates from a filename. Missing material metadata/profile means Unknown or configuration/information pause; newest upload/retrieval rank does not grant authority. No universal hierarchy, recency duration or source-expiry rule is approved. Retain history and no automatic expiry, preserve original conflicts, include date/profile in dependency identity and use existing revision/continue controls. Source-profile configuration requires actual reviewed evidence; no extra LLM/crawler/database or retail-Q&A scope. These are draft instructions until the repository gate.

Follow the authorized AE-01–07 contract refinements: compact SYN-WIRE-1.0 and Python-owned authority; CANON-1.0 exact scoped fixture/dependency identities; COVERAGE-1.0 original-span/multi-page evidence; PROVIDER-1.0 outcome/usage normalization; RESUME-1.0 and RUN-OUTCOME-1.0 receipt/pause/completion handling; STATE-UPDATE-1.0 explicit stale-current clearing; EVAL-CUTOFF-1.0 original model versus reviewed workflow evaluation. Implement in the existing proposed modules after their gate; do not introduce seven new subsystems. Use the existing planned tests and preserve all budgets/history/no-expiry boundaries. No raw graph state streaming is authorized as a substitute for safe event projections.

Before dependent implementation, perform the bounded contract/context-size, dependency and SQLite interrupt/resume compatibility checks in the approved first milestone. Resolve parser licensing before installation; verify selected Nebius model schema/token/rate behavior before authorized Live work. No budget increase, schema weakening or hidden inference is allowed to fit the prototype.

Use updated P3-05 targets and protect one synthesis correction's1,500 input/350 output tokens before optional repairs. A normal path plus that rerun is6,000 input/1,700 output, within aggregate8,000/2,000 ceilings; actual feasibility remains to be measured.

Keep a high-level false-positive count beside recall in offline QA results; do not add excessive-risk-flagging indicators, a new UI workflow or an extra LLM judge. Preserve case-specific supported Reject separately from missing-information/technical stop, with original recommendation and human disposition distinct. The thirty-case/full held-out/timing/batch/multi-person protocols are optional extensions. Core usability uses one operator's five tasks with honest self-assessment. This draft is not active root AGENTS.md and does not approve repository scaffolding.
