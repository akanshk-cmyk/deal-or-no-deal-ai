# Deal or No Deal AI — Repository Design

Documentation authority: requirements and approved feature contracts describe
intended behavior; [current implementation status](../implementation-status.md)
records observed completion. Dated implementation/setup/test paragraphs below
are historical evidence for their stated milestone, not current missing-work
claims. See [documentation alignment](../evaluation/documentation-alignment.md) for the cross-document review.

Decision History addition2026-10-24: [SPEC-013](../specs/decision-history.md) places scoped read queries/filter/timeline/CSV in decision_history.py and the dedicated page in ui/decision_history.py, navigable from the existing local preview entry point. New context snapshots are added to existing review event writes; no database/schema/dependency is added. This authorizes a sixth target page; the full shell/financial lifecycle remains pending.

**Human-review component — 2026-10-24:** review_actions.py is the scoped persisted illustrative adapter; ui/human_review.py is the reusable Streamlit panel; tools/preview_human_review.py is an explicit local preview entry point. Existing review.py guards and Store are reused, with no parallel permission engine/database or full app shell. See [REVIEW-UI-1.0](../specs/human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10). Actual financial-review resume/screen integration is pending.

**Quality implementation placement — 2026-10-24:** Existing model_comparison.py now owns full-source extraction task preparation and field/synthesis diagnostics. quality_review.py implements explicit local capture retention; tools/review_model_response.py is the offline entry point. Tests extend the existing unit/integration suites; captures/task snapshots/reports remain under ignored var/evaluations/response-review. [QUALITY-REVIEW-1.0](../evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) introduces no provider client, service, database, agent, dependency or architecture switch. The larger tree below remains a proposed destination where files are still absent.

**Current embedding decision — 2026-10-23:** [ADR-008](decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

**Historical local-library/reference setup snapshot,2026-10-23:** Core E-N01/M1 evidence is retained, and optional Crawl4AI/sentence-transformers/CPU torch installation plus LOCAL-REFERENCE-1.0 file inspection extend the combined suite to95 passing methods. [Current evidence](../execution.md#local-reference-setup-and-inspection-evidence). public_sources.py, config/source_ingestion.toml and explicit inspection/setup tools exist. Browser/model weights, embedding/vector/index/retrieval modules and core graph/UI remain pending. No external repository, project license, paid service or deployment is selected.

Version: 1.21
Date: 2026-10-23
Status: M1 foundation installed/locked;43 scoped checks and local build passed2026-10-23; later modules remain planned
Sources: [PRD](../product/prd.md), [HLD](hld.md), [approved Phase 3 contracts](../specs/overview.md), [evaluation plan](../evaluation/evaluation-plan.md)
Agent-development instructions: [AGENTS.md draft](AGENTS.draft.md)

## Prior approval and current boundary

Accepted ADR-007 extends the planned repository with bounded public-source ingestion, selected local-file intake/Nebius-hosted embeddings and app-owned SQLite vector records. Architecture/source approval is resolved; optional package setup and local inspection are tested; browser/model/index/retrieval modules remain pending. Keep browser/embedding dependencies lazy and optional so the existing fixture environment/imports do not load them. config/source_ingestion.toml now declares LOCAL_FILE and owns the exact URL scope and nonsecret model/segmentation/build versions; raw snapshots, model/browser caches and indexes stay under ignored var/. Public references never enter fixtures/ or evaluator gold.

Current registered M2 slice supersedes earlier A1-A4/policy/risk pending notes: user approved the presented next steps, config/registrations/e-n01.json and config/sample_policy.json now exist, and services.py/policy.py/risk.py execute the exact source-fitted E-N01 default panels. tools/run_e_n01_panels.py is explicit offline QA, not a parallel app/graph. [85-method evidence](../execution.md#m2-registered-deterministic-panels-evidence). Authoring snapshots/history remain; actual parsed sources are rechecked at admission. Only fixed Fixture/default is available; full graph/stage variants/UI/Live remain pending. No new dependency/database/framework.

Current parser update2026-10-23 supersedes earlier no-parser/proposal-only notes: the user approved pypdf installation and verification.6.21.2 is installed/locked; three PDFs/five pages pass actual plain/layout fidelity checks;69 combined methods pass. [ADR-006](decisions/006-proposed-pdf-parser.md) is accepted for this scope. tools/verify_e_n01_pdfs.py is fixed known-corpus QA with ignored raw/report artifacts, not generic upload intake. Technical draft2 repairs font encoding; history/1-draft and initial failure evidence remain. A1-A4/source fit, case registration and complete graph/UI remain pending.

M2 scoped progress2026-10-23: `finance.py` implements the internal FIN-1.0 arithmetic kernel. `fixtures/development/e-n01/` now holds draft source PDFs/manuscripts, metadata, extraction candidate and evaluator-only gold. `tools/prepare_e_n01.py` is one fixed case-authoring utility, not runtime intake or a generic PDF framework; it imports no gold and refuses unexpected generated-file changes. [Evidence](../execution.md#m2-source-candidate-and-arithmetic-evidence):66 combined methods passed. [ADR-006](decisions/006-proposed-pdf-parser.md) is proposed only. No dependency or application architecture change; no parser or registered fixture.

Subsequent scoped extension,2026-10-23: the user authorized [DOCVERIFY-1.0](../specs/context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10). The existing proposed `documents.py` module now contains only parser-independent original-block/table checks. Added test cases/runner live under tests/, not a new application/evaluation framework. [Evidence](../execution.md#document-verification-extension-evidence):55 combined tests and14 paired synthetic cases passed; parser, full intake/ContextPacket, loan graph and retrieval adapters remain pending. No dependency or directory architecture change.

On 2026-10-22, the user approved advancing from Phase 3 with “ok move to next step,” following the explicit request to approve the specifications/evaluation plan and P3-01–09. Record those documents and nine decisions as the accepted specification baseline. No acceptance test, runtime implementation or spending permission follows from document approval.

At the Phase 4 inspection, the workspace contained only docs/, with PRD/HLD, five decision records, thirteen specialist-instruction documents, twelve feature specs plus overview, evaluation plan, traceability and historical archives. There is no .git directory, Python manifest, application package, source fixture, notebook, HTML prototype, root AGENTS.md, environment or database. Preserve these documents and archives.

The user's 2026-10-23 instruction to apply the findings and move forward advances R4-01–08 into Phase 5 planning. The [execution plan](../execution.md) and [design-system proposal](../design/design-system.md) now define the concrete milestones. Application scaffolding, dependency installation and root AGENTS.md activation await M1 approval under the original Phase 5 gate. Project/parser licensing, paid calls, publication and deployment retain their separate boundaries. Earlier phase-completion notes below describe their historical edits rather than the current next step.

## Repository decisions proposed for approval

| ID | Proposed decision | Why |
|---|---|---|
| R4-01 | Use the current workspace as the eventual repository root, distribution name deal-or-no-deal-ai, import package deal_or_no_deal_ai | Avoid an extra nested checkout/project and awkward Python imports |
| R4-02 | One src-layout Python package and a thin root app.py; Python 3.12 as the initial interpreter baseline, subject to actual dependency resolution | Shared code is importable from Streamlit, tests, notebook and CLI |
| R4-03 | Keep docs/agents as the sole instruction source; resolve allowlisted role sections from a trusted source-checkout root | No duplicate prompt directory or divergent notebook prompts |
| R4-04 | Use a small injected model adapter, with HTTPX as the proposed Nebius transport and selected langchain-core primitives; no full LangChain agent runtime required | Explicit request/timeout/retry accounting without an additional planner or provider |
| R4-05 | Commit synthetic case sources/manifests/model-stage fixtures/gold labels under fixtures/, separate development and held_out; keep runtime/output state under ignored var/ | One copy of each scenario, clear evidence labels, no accidental local-data commits |
| R4-06 | Standard-library sqlite3 plus a compatible LangGraph SQLite saver, application table ownership separate in one database | No ORM, second database, migration service or broker |
| R4-07 | Use pytest and Streamlit AppTest; local notebook/HTML checks; Jupyter/NetworkX/Matplotlib in a separate notebook dependency group | Tests exercise shared services and screens without adding browser automation infrastructure initially |
| R4-08 | Draft root AGENTS.md is reviewed here; activate it only in the first approved scaffolding milestone | Unapproved instructions/commands do not become active workspace policy |

Python/package versions, tokenizers and the exact SQLite saver combination are not tested yet. Python 3.12 is a proposed support target, not a claim to be the newest Python or universally compatible. Build tooling is minimal setuptools for the single package; no plugin system or reusable framework is proposed.

## Proposed target tree

ADR-007 adds planned public_sources.py (bounded fetch/snapshot/segmentation) and embeddings.py (lazy Nebius-hosted embedding adapter (disabled until verified)). These are modules in the existing package, not a second service or new implementation framework. storage.py owns the additive app-schema/vector records; retrieval.py owns scoped exact search/adapter selection. No file/dependency/table is created by this tree.

The tree describes files to create incrementally after approvals. Existing docs remain in place. It is not a claim that any non-document path currently exists. Folder names and case names are illustrative planned paths; do not create placeholders for every future module.

~~~text
week_3 project/                         # current workspace; no new nested root
├── README.md                          # purpose, synthetic boundary, setup, demo and honest status
├── AGENTS.md                          # approved copy of the current draft
├── pyproject.toml                     # Python/dependencies, pytest/build settings
├── uv.lock                            # resolved lockfile, generated rather than hand-written
├── .python-version                    # approved interpreter baseline
├── .gitignore                         # local state, keys, caches and generated output exclusions
├── .env.example                       # blank keys only; does not enable Live
├── app.py                             # thin Streamlit entry point
├── docs/                              # existing source-of-truth documents
│   ├── product/                       # PRD and untouched historical archives
│   ├── architecture/                  # HLD, decisions, this proposal and AGENTS draft
│   ├── agents/                        # two application prompts + separate offline evaluator prompt
│   ├── specs/                         # twelve approved feature contracts plus overview
│   ├── evaluation/                    # approved evaluation plan; later honest result notes
│   ├── traceability.md
│   ├── execution.md                   # Phase 5; not created in Phase 4
│   └── design/design-system.md        # Phase 5; not created in Phase 4
├── config/
│   ├── app.toml                       # Fixture default, limits and safe paths
│   ├── model.toml                     # nonsecret provider/model/schema/instruction versions
│   ├── evaluation.toml                # offline RAGAS disabled; rubric/metric/sample versions and explicit allowance refs
│   └── sample_policy.json             # SAMPLE-LOAN-POLICY-1.0 and approved mappings
├── src/deal_or_no_deal_ai/
│   ├── __init__.py                    # no provider/database side effects on import
│   ├── configuration.py               # trusted paths, validated settings, later environment key
│   ├── contracts.py                   # CONTRACT-1.0 and feature-specific Pydantic models
│   ├── documents.py                   # PDF adapter, intake/versioned page references
│   ├── extraction.py                  # extraction request/wire validation and Fact hydration
│   ├── finance.py                     # FIN-1.0 Decimal arithmetic
│   ├── policy.py                      # applicability, active rules, original outcomes
│   ├── risk.py                        # flags/gaps; concentration Not assessed
│   ├── synthesis.py                   # three-panel request / PanelDecision validation
│   ├── model_comparison.py            # implemented offline paired tasks and response diagnostics
│   ├── quality_review.py              # implemented original capture/task retention; no dispatch
│   ├── evidence.py                    # reference/numeric checks and semantic-review labels
│   ├── context.py                     # instruction sections, evidence packets, token preflight
│   ├── retrieval.py                   # RET-1.0 + four scoped adapters; inject lazy embedding interface
│   ├── retrieval_benchmark.py         # optional keyword/vector/hybrid adapters and comparison runner
│   ├── budgets.py                     # reservations/reconciliation, all cumulative limits
│   ├── review.py                      # capabilities, dispositions, corrections/invalidation
│   ├── review_actions.py              # implemented role-aware illustrative review persistence
│   ├── decision_history.py            # scoped read snapshots, filters, timeline and CSV
│   ├── memo.py                        # pure preview/report renderer; no I/O or LLM
│   ├── graph.py                       # shared graph factory and node/edge description
│   ├── nodes.py                       # thin graph adapters around specialist functions
│   ├── services.py                    # scoped application commands and read models
│   ├── worker.py                      # one user-started execution worker; no paid restart replay
│   ├── storage.py                     # SQLite repositories/schema version and operation receipts
│   ├── events.py                      # content-minimized event contract and queries
│   ├── evaluation.py                  # local evaluation CLI/rubrics/result records
│   ├── ragas_evaluation.py            # lazy offline sample/scorer adapter; one shared custom bundle + local metric projections
│   ├── presentation.py                # offline graph/snapshot HTML rendering helpers
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── contract.py                # narrow injected structured-task interface
│   │   ├── fixture.py                 # only matching registered model-stage responses
│   │   └── nebius.py                  # later lazy HTTP transport; one provider
│   └── ui/
│       ├── __init__.py
│       ├── human_review.py            # implemented reusable review panel; full shell pending
│       ├── decision_history.py        # implemented dedicated preview page; full shell pending
│       ├── shell.py                   # navigation, labels, selected deal and service access
│       ├── dashboard.py
│       ├── new_deal.py
│       ├── workspace.py
│       ├── activity.py                # includes local evaluation-results expander
│       └── credit_memo.py
├── fixtures/
│   ├── README.md                      # synthetic-only manifest/lineage/split instructions
│   ├── development/
│   │   └── E-N01/                     # representative of eighteen development cases
│   │       ├── case.json              # hashes/scope/basis; optional synthetic factor assessments, not gold totals
│   │       ├── documents/*.pdf        # up to three synthetic source PDFs
│   │       ├── source_text/*.txt       # authoring text, when needed for reproducibility
│   │       ├── model_outputs/
│   │       │   ├── extraction.json    # fixture for the first model stage
│   │       │   └── synthesis.json     # fixture for the second model stage
│   │       ├── control_dispositions/  # only for cases with approved synthetic fixture updates
│   │       └── gold.json              # evaluator expected facts/metrics/gates; never prompt input
│   └── held_out/                     # twelve held-out packages with the same schema
├── tests/
│   ├── conftest.py                     # deterministic clocks/repos/transports; network denied
│   ├── unit/                          # contracts, arithmetic, policies, gates, context, budgets
│   ├── integration/                   # real graph+SQLite, fixtures, recovery and isolation
│   ├── ui/                            # Streamlit AppTest and service-action consistency
│   └── presentation/                  # offline graph/notebook/HTML and lineage checks
├── notebooks/
│   └── 01_workflow.ipynb               # shared graph, graph-only/no key/no network
├── prototype/
│   ├── template.html                  # lightweight five-screen walkthrough template
│   ├── styles.css
│   └── app.js                         # local navigation only; no financial/policy engine
└── var/                               # created on demand and completely ignored
    ├── deal_review.sqlite3            # app tables + compatible checkpointer; one DB
    ├── evaluations/                   # actual local results, never invented baseline data
    ├── notebooks/                     # executed graph-only notebook artifacts
    └── presentation/                  # generated standalone HTML walkthrough/artifacts
~~~

Use ordinary modules initially. Split contracts.py or storage.py only when growth or independent testing justifies it; do not turn each specialist into its own package/server. Logical record groups in SPEC-011 do not mandate one SQL table/class per record type. app.py and UI modules call services rather than import another graph or reproduce rules.

No Docker, FastAPI, Redis, Node/npm project, hosted CI deployment, vector database, mem0, voice SDK or cloud configuration is planned. No LICENSE file is selected or created.

The user-authorized optional retrieval benchmark adds a local in-memory vector comparison, not a hosted vector database or an active app retrieval mode. DIRECT remains the default. The RET-1.0 interface is planned during initial context implementation; optional keyword/vector/hybrid adapters and model dependencies are added only at their selected implementation milestone. This proposal still does not scaffold any runtime files.

## Directory responsibilities and feature ownership

For the optional retrieval slice, follow [the canonical source-ready/four-baseline/conditional-reranker sequence](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). Implement DIRECT/KEYWORD/VECTOR/HYBRID through the existing planned retrieval.py and retrieval_benchmark.py boundary; record VECTOR as the semantic baseline and HYBRID's RRF as fusion. Add no new directory, package or model for a reranker until measured ranking errors justify the separately selected follow-up and existing dependency/model/setup requirements are met. Report specified/implemented/tested/measured status separately. These retrieval modules remain unimplemented despite M1's passing context helpers; this section allocates future ownership rather than claiming code exists.

| Location | Responsibility | Approved feature references |
|---|---|---|
| docs/ | Product/design/role/evaluation source of truth, with explicit approval history | All; preserve archive content |
| config/ | Trusted versioned demo policies, capability/limit configuration and nonsecret model choices | SPEC-004/006/007/008 |
| src/.../contracts.py | Strict wire/domain types and serialization shared by all entry points | CONTRACT-1.0; SPEC-001–011 |
| documents.py / extraction.py | Validate/parse once, source locators and structured extraction | SPEC-001/002 |
| finance.py / policy.py / risk.py | Deterministic panels; four scheduled tool boundaries | SPEC-003/004 |
| risk.py score helper / existing case metadata | RISK-EDU-1.0 aggregation and SCORE-BANDS-1.0 within existing risk node; material-input-backed case assessments separated from evaluator-only gold totals | SPEC-004 TEST-004-10/11; three independent SCOREVIEW-1.0 projections use recorded output |
| synthesis.py / evidence.py / context.py | Second model task, evidence checks, selective context/exact reuse | SPEC-005/006 |
| retrieval.py / retrieval_benchmark.py | Shared evidence interface/DIRECT and optional offline BM25/vector/RRF comparisons; stable ContextPacket for consumers | RET-1.0 in SPEC-006; MET-23 benchmark protocol |
| graph.py / nodes.py / worker.py / services.py | Shared graph, actual dispatch, one worker and guarded commands | SPEC-007/008 |
| storage.py / budgets.py / events.py | One SQLite boundary, durable ledgers/receipts/history and safe diagnostics | SPEC-007/011 |
| review.py / memo.py | Capability/disposition/revision handling; pure seven-section rendering | SPEC-008/009 |
| ui/ | Five screens; reads do not dispatch model work | SPEC-010 |
| evaluation.py / fixtures/ | Separate deterministic/fixture/live evaluation evidence and fixed gold data | SPEC-011; evaluation plan |
| notebooks/ / presentation.py / prototype/ | Same graph, offline teaching and clickable visual walkthrough | SPEC-012 |
| tests/ | Application invariant tests and controlled adapter checks, not live quality claims | Planned TEST-001–012 families |
| var/ | Untracked runtime state/results and separately scoped permitted public snapshots/model caches/index artifacts; never committed fixtures or evaluator answers | SPEC-009/011/012 |

The current risk refinement fits existing planned modules: trusted application configuration holds band/material-input/referral versions; graph/review services enforce SCORE-ROUTING-1.0 and existing personas' NORMAL/SENIOR capabilities; storage retains distinct score handling and review lineage; synthesis validates optional proposed_action outside five-field PanelDecision. No additional framework, graph node, model stage, database or directory is proposed. Source/assessment authoring remains a prerequisite; no universal financial-to-factor numeric mapping is invented. This repository proposal remains unapproved and unscaffolded.

The authorized SME fixes also fit those modules: configuration/documents hold reviewed case-completion and subject/facility registries; contracts/review/services store scoped FACT/CLAIM support and derived CONDITIONS-1.0; finance/policy/synthesis/memo/UI enforce trusted-use and analysis-scope labels; graph uses existing prerequisite stops and explicit support-only continuation. Complete cases require authored reviewed packs; unregistered Live upload is partial. Reported-EBITDA normalization/reconciliation is deferred, preserving the provider wire. No extra directory, entity-service framework, condition engine or dependency is proposed. Repository/implementation/spending gates remain pending.

## Immediate scaffold versus incremental implementation

The user requested an explicit remaining-prerequisites checklist. [PREREQ-01–08](../specs/overview.md#implementation-prerequisites-and-required-evidence) is the canonical order/status/evidence source: approval -> compatible persistent foundation -> exact prompt/context contracts and reviewed sources -> core fixture workflows -> user-facing artifacts -> separately authorized Nebius integration, with RAGAS/hybrid execution separately selected. This documents dependencies, not a Phase 5 execution-plan approval or a claim that these non-document files exist. Carry the relevant prerequisite IDs/evidence requirements into the later small-task milestone plan; do not scaffold every proposed module to satisfy a checklist.

Nothing in this section is created yet.

First approved milestone must include a bounded compatibility/feasibility check before dependent feature implementation: strict complete wire/domain round trip and serialized size, Python/package resolution, minimal SQLite interrupt/resume and correction budget/entry trace. Resolve parser licensing before parser installation and provider-specific output/token accounting before authorized Live dispatch. Then scaffold only the root README/AGENTS/manifest/interpreter/gitignore/blank env example, minimal package/configuration/contracts and focused tests required by the approved Phase5 plan. These checks are planned; nothing is installed now. Generate uv.lock only through actual resolution; inspect the resulting dependencies and report failures. Do not claim a lockfile is validated from a guessed version list.

Initial configuration remains Fixture. Add only the first milestone's needed config/modules/tests. The public policy JSON is added when policy implementation starts, with explicit exact version/mapping and no legal/regulatory clearance wording.

When context.py is first implemented, inject the RET-1.0 DIRECT adapter instead of hardcoding source selection into graph nodes/prompts. Plan optional benchmark adapters against that same contract. At the explicitly selected benchmark milestone, add config/benchmark.toml, an optional benchmark dependency group and ten query annotations over existing development sources. Default benchmark.enabled=false and app retrieval_mode=DIRECT; absent benchmark dependencies never break the core app/imports/notebook. Leave model IDs/revisions unset until selected and compatibility/licensing checked. An explicit benchmark command requires ready local artifacts; no automatic downloads, cloud fallback or provider calls. No generic plugin framework or additional database is needed.

Add at the relevant later milestone: document/parser implementation and synthetic PDF package; graph/Python panels; review/storage/events; UI modules; remaining cases/evaluation runner; notebook/HTML assets and generated artifacts. Add nebius.py only as a lazy integration adapter after local contracts exist; Live remains unavailable until separately configured/authorized. Notebook dependencies need not slow the first environment setup.

Do not create empty test/module files for all rows now. Do not add a second copy of fixtures under tests/ or prompt files under src/. Tests import the same registered synthetic package helpers with temporary SQLite databases, not a production/local working database.

## Runtime prompts, model configuration and tool definitions

- docs/agents/extractor.md and synthesizer.md Runtime prompt sections and shared-contract.md Model context rules are the only role prose automatically loaded for model calls.
- context.py uses an explicit allowlist, trusted source-checkout root and expected instruction/schema hashes. Uploaded text cannot supply a path. A missing/mismatched file stops, rather than searching arbitrary directories or reading an older copy.
- Full role/spec/evaluation prose is for implementation/review. Do not append it to every request. Do not read fixture gold.json or held_out answers into model context.
- config/model.toml holds provider name, an eventually approved model ID, endpoint/config version, response-schema IDs, prompt hashes, output caps and dated rate/tokenizer references. It has no real key or made-up provider price.
- Provider calls use compact wire schemas and local expansion of trusted identity/reference metadata. Actual model/schema/token accounting must be verified before Live.
- compute_financials and evaluate_policy are defined with their domain logic; calc_credit_risk and calc_concentration_risk live in risk.py. nodes.py schedules them explicitly. Selected LangChain tool/runnable wrappers must not add model loops or conceal child invocations.
- Keep the four scheduled tool boundaries; count any later real child tool/node and all outbound attempts. No tool registry duplication in a separate JSON instruction catalog.

This is a source-checkout local app. A built Python wheel is not a standalone deployed product with source documents/config/fixtures bundled. Run from the reviewed checkout with validated asset root; packaging those assets for distribution would be a separate requirement. Never embed gold answers or credentials to make a wheel self-contained.

## Proposed dependencies and verification checkpoints

| Group | Proposed contents | Verification or open decision |
|---|---|---|
| Runtime foundation | streamlit, langgraph, langchain-core, pydantic, langgraph-checkpoint-sqlite | Resolve compatible versions/Python 3.12/Windows; verify saver connection/transaction behavior and absence of import-time inference |
| Nebius transport | httpx | Native documented request/structured-output shape; explicit timeout and transport retries off; mock tests before any funded live request |
| Standard library | decimal, sqlite3, concurrent.futures, pathlib, hashlib, json, tomllib | No extra ORM, worker framework, YAML parser or dotenv library required initially |
| PDF parser | User-approved pypdf6.21.2 | Installed BSD-3-Clause profile; all five E-N01 pages tested. Generic upload/resource/layout acceptance remains pending; see ADR-006 |
| Development | pytest | Strict fixture-network denial and meaningful invariant/fault tests; no automatic provider-key detection |
| Notebook group | jupyterlab, ipykernel, nbconvert, networkx, matplotlib | Fresh-kernel/local-only renderer checks; exact resolved versions and licenses reviewed later |
| Optional evaluation group | ragas, added only at its approved milestone | Pin Python/Pydantic/provider/custom-metric compatibility; keep imports lazy, default providers/downloads off, and every judging request instrumented; no version or successful Nebius integration assumed |
| Build backend | setuptools | Minimal src-layout build config; local distribution check only, no publication |

No claim that this exact combination has been installed or tested. Full langchain, pandas, Ruff/mypy, browser automation and LangSmith remain unnecessary or optional additions until justified. Existing selected LangChain primitives are retained through langchain-core; this does not introduce a second agent framework.

HTTPX has configurable transports and mock transports, and Nebius documents a compatible HTTP inference endpoint. This supports a small adapter proposal but is not proof that a selected model meets our structured-output and accounting contracts. [HTTPX transports](https://www.python-httpx.org/advanced/transports/), [Nebius quickstart](https://docs.tokenfactory.nebius.com/quickstart).

uv supports dependency groups and project-oriented Jupyter workflows. Streamlit provides AppTest for headless interaction checks. These documented capabilities do not establish full browser accessibility or notebook compatibility. [uv dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/), [uv/Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/), [Streamlit testing](https://docs.streamlit.io/develop/api-reference/app-testing).

### Parser licensing checkpoint and recorded selection

User-approved [ADR-006](decisions/006-proposed-pdf-parser.md) selects pypdf under BSD-3-Clause terms for local installation/known-corpus verification. Installed6.21.2 metadata/license was checked and uv.lock records the actual dependency. PyMuPDF was the previous unselected candidate; neither its AGPL nor commercial path is adopted, and no purchase/project license is selected. [PyMuPDF license statement](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright).

pypdf is now the recorded approved substitution, with actual text/layout tests on E-N01. This does not establish general parser fidelity, visual rendering or legal compliance. Keep applicable dependency notices and verify future changes. [pypdf upstream license](https://github.com/py-pdf/pypdf/blob/main/LICENSE).

This checkpoint must be resolved before the parser/PDF milestone or adding that parser to the manifest. Repository structure and first pure-contract/finance work need not select a parser license. All actual dependency terms remain subject to review; no project LICENSE is inferred from a dependency's license.

## User-authorized RAGAS planning

[RAGAS-EVAL-1.0](../evaluation/ragas-evaluation.md) adds the two existing Markdown contracts and the later optional evaluation dependency/config/module above, not application scaffolding now. Keep one source of truth for the five user rubric dimensions and one separate evaluator prompt. Implement the custom shared-bundle adapter against verified pinned RAGAS APIs; do not assume built-in rubric scorers return the requested full explanations/examples in one call. Native metrics keep their own definitions/scales and selected request plan. Offline samples come from saved original artifacts, not a CLI that silently regenerates deals; evaluator gold is separately labeled.

Proposed internal entry-point extension after implementation: evaluation --benchmark ragas --sample-id SAVED_SAMPLE_ID --config config/evaluation.toml --output-dir var/evaluations. This is a project CLI proposal, not a verified RAGAS CLI/API or a command run here. Disabled/unconfigured semantic evaluation exits with a specific prerequisite before any paid work. A key alone enables neither scorer nor allowance. Store results in existing evaluation groups/ignored artifacts; read-only Activity shows scores/examples/versions/flags and separate usage. No new database, backend, graph node, sixth screen or default hosted telemetry. Repository/milestone approvals, evaluator rates/access and explicit execution allowance remain separate.

## Tests versus AI evaluations

Application tests under tests/ assert arithmetic, policy boundaries, strict schemas, idempotency, source/revision/capability guards, budgets, recovery, pure report generation and zero unintended inference. Integration tests use the real graph/SQLite with controlled transports. Streamlit AppTest covers supported UI interactions; keyboard/contrast and offline-browser behavior require the separate manual checks in the evaluation plan.

AI evaluations use fixtures/ sources and independently reviewed gold labels via evaluation.py. Extraction accuracy, semantic citation support, supported risk recall and narrative scoring require real model output/human assessment; fixture responses cannot prove these metrics. Eighteen development and twelve held-out cases remain separated. A committed held-out directory is a workflow boundary, not cryptographic blindness: disclose authors who have seen answers and freeze labels before model tuning.

Default test/evaluation commands deny outbound provider traffic, regardless of whether a key happens to exist. Fixture mode can execute the graph, panels and report, but usage is labeled Not applicable for inference. A live API smoke test, quality suite or latency workload is separately authorized and never part of normal pytest/test discovery.

Each implemented test or parameter group links to its planned TEST-* ID, feature and PRD requirement. The planned TEST IDs (including focused review-fix additions) are not passing tests. Preserve both exact case outcomes and failure/denominator information.

## Proposed setup, test, run and build commands

These commands are documentation proposals. Their target files/modules are not created, no dependency is installed, and none of these commands was run. They become usable only after repository approval, first-milestone approval and actual implementation. uv may download packages/interpreters; any environment permission prompts still apply.

~~~powershell
uv sync --group dev
uv run streamlit run app.py --server.address 127.0.0.1
uv run pytest tests/unit tests/integration
uv run pytest tests/ui tests/presentation
uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split development --output-dir var/evaluations
uv run python -m deal_or_no_deal_ai.evaluation --mode fixture --split all --output-dir var/evaluations
uv sync --group dev --group notebook
uv run --group notebook jupyter lab --no-browser --ip 127.0.0.1
uv run --group notebook jupyter nbconvert --execute --to notebook --output-dir var/notebooks notebooks/01_workflow.ipynb
uv run python -m deal_or_no_deal_ai.presentation --run-id RUN_ID_FROM_ACTIVITY --output-dir var/presentation
uv build
~~~

evaluation/presentation CLI flags above are proposed project interfaces, not third-party APIs. RUN_ID_FROM_ACTIVITY is a placeholder for an actually executed synthetic fixture run; the presentation command must reject an unknown/nonfixture/stale run rather than fabricate execution. Generated index.html embeds its reviewed snapshot data, with local CSS/JS; no fetch to a JSON file or server is required for offline file opening.

No separate npm/frontend build is needed. uv build checks the local Python distribution; it does not deploy it or prove the full app is standalone. Notebook launch may expose a local authenticated Jupyter URL; do not put tokens into committed notebook outputs/logs. No live model command or publishing command is authorized by this table. Do not run all suites before their components exist or mark unavailable checks Passed.

## Version control, secrets and runtime data

Proposed tracked content: Python source, docs/archives, config without secrets, reviewed synthetic fixture sources/model-stage fixtures/gold data, test code, source-only notebook, prototype templates/assets, pyproject.toml, generated uv.lock and a blank .env.example.

Proposed .gitignore rules for later implementation:

~~~gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/
build/
dist/
*.egg-info/
.env
.env.*
!.env.example
.streamlit/secrets.toml
*.pem
*.key
var/
.ipynb_checkpoints/
notebooks/.ipynb_checkpoints/
~~~

Blank .env.example is only a template; copying it does not automatically load a key or enable Live. Read the later key from the local process environment or a deliberately approved secret interface; no automatic dotenv dependency is needed. Credentials cannot appear in prompts/config commits/state/checkpoints/notebook outputs/logs/UI/reports. Do not print the environment or raw request headers while troubleshooting.

Keep the database and SQLite -wal/-shm sidecars inside ignored var/. Confirmed P3-04: no automatic expiry in the MVP prototype; no age-based deletion/pruning of persisted documents, deal records, reports, review history or checkpoints. Manual deletion/reset requires an explicit user request and reviewed targets. Tests use disposable temporary directories; no generic recursive cleanup targets the workspace, docs, attachments or archives. Application configuration must reject paths escaping the intended local runtime area. MemorySaver's RAM lifetime and provider-controlled prompt caches are separate from persisted-data retention.

Notebooks are committed without executed outputs/tokens; executed copies stay in var/notebooks. Curated demonstration artifacts are generated locally and linked honestly. Broad .gitignore patterns are a backstop, not a guarantee that data is safe: review every selected file before any future commit/publication. No private real borrower documents are acceptable even under ignored var/. ADR-007 permits only explicitly selected public-reference snapshots in a separate local corpus; they are not synthetic fixtures or a completed loan review.

No Git repository is initialized, commit made, remote added, license selected or external repository created in Phase 4. Future publication/remote creation requires explicit approval separate from local development.

## Phase 4 completion and gate

Planned optional command extension: evaluation --benchmark retrieval --config config/benchmark.toml, implemented through evaluation.py and retrieval_benchmark.py at the approved benchmark milestone. This is a proposed project CLI contract, not an existing command or installed tool. It writes honest local results under var/evaluations and never changes app strategy or starts the lending graph. See the [benchmark protocol](../evaluation/hybrid-retrieval-benchmark.md). No command is executed by this document update.

Created in this phase: this proposal and the AGENTS.md draft; previous Phase 3 approval recorded. Validate Markdown structure, actual local links and absence of application scaffolding. No application tests or dependency compatibility checks can pass before an application exists.

R4-01–08 are the accepted direction for the current execution plan. Parser licensing remains deferred until before parser adoption; it is not implicitly approved by repository or M1 acceptance.

The Phase 5 documents are prepared. Review [M1-01–09 and its definition of done](../execution.md#m1--concrete-first-implementation-milestone-for-approval) before application scaffolding or root AGENTS.md activation. No deployment, publication, paid service or operational financial use is included.

## Principal engineering refinements within the proposed modules

The user-authorized follow-up fixes remain within these existing modules. context.py loads the corrected exact Extractor Runtime prompt and checks its wire/schema/examples/instruction hashes, without appending developer prose. review.py/services.py separate REVIEW-BASIS-1.0's analytical fingerprint from gate progress; the existing condition editor/storage/support service prepares exact edited-condition drafts before accepting a disposition. worker.py/services.py/storage.py enforce EXEC-ADMISSION-1.0 via an atomic unique slot in existing SQLite operation/run records across same-database app/notebook/CLI entry points. contracts.py/storage.py and graph adapters implement STATE-CODEC-1.0's primitive representation, exact type restoration, patch clearing and noncircular parent-content digests. No new module/framework/database/service is needed.

Carry these into Phase 5's existing first compatibility milestone: loaded prompt/schema mismatch negatives; exact Decimal/confidence/checkpoint/fingerprint round trips; two independent process contenders admitting only one; atomic Busy/no-disposition acceptance; and reviewed-handling versus analytical-change invalidation, including prepared edited conditions. Native RAGAS integration remains lazy/later, using the same admission boundary when selected. No existing test is claimed passing and no runtime codec/lock/fixture is created by this proposal. Pending repository/first-milestone approvals and funded Live conditions remain unchanged.

The user's AE-01–07 fix instruction updates contracts, not the pending repository gate. Use existing models/synthesis/evidence/context/retrieval/orchestration/review/repository/provider/evaluation modules for SYN-WIRE-1.0, CANON-1.0, COVERAGE-1.0, PROVIDER-1.0, RUN-OUTCOME-1.0, RESUME-1.0, STATE-UPDATE-1.0 and EVAL-CUTOFF-1.0. No new framework/service/database, external repository or scaffolding is needed for these document refinements. Exact proposed module paths remain subject to Phase 4 approval.

Carry into the first approved milestone: strict wire-to-domain/unknown-authority checks, deterministic fingerprints/current fixture handles, SQLite accepted-receipt/interrupt gap recovery, current-state clear behavior and serialized ordinary/Conditional/correction token feasibility. Before document-evidence demonstration, verify original-span inventory and multi-page citations. Before funded Live, verify normalized refusal/truncation/usage/uncertainty against the selected model. Before quality claims, score original frozen outputs separately from human-edited workflow and report failed-case denominators. Existing planned tests own these checks; none is executed by this update.

SOURCEFIT-1.0 is an additional user-authorized contract refinement within the same proposed modules. Store ReviewSourceBasis, original capture/ingestion/effective metadata and reviewed field-specific source applicability in existing source/case/artifact groups; implement deterministic selection within existing validation/context boundaries. Include basis/profile in exact cache/fixture identities and show selected source/alternatives through existing UI/report projections. Add focused tests to existing families using E-C/missing-data variants. No new crawler, database/index, graph node, paid call, historical-chat feature or automatic deletion schedule. Missing business-date/authority metadata remains a case-authoring prerequisite; do not invent a profile during implementation. Repository/execution/scaffolding approval remains pending.

## Director fixes and the first delivery slice

The user authorized the recommended fixes, not blanket R4-01–08/scaffolding/spending approval. Keep NARRATIVE-CHECK-1.0 in existing synthesis/evidence/contracts/review modules; INPUT-EDU-1.0 in the shared parsing/validation/config boundary; SOURCE-TRIAGE-1.0 in existing issue/review/configuration/UI projections; CONTINUE-CHECK-1.0 in graph/services and the SAME ledger. No new directory, plugin, agent, separate claims database, source editor or workflow-planning framework. Preserve exact model wires and count actual work.

After the existing repository approval, Phase 5 must name concrete first-milestone files/tests/definition of done: strict complete wire/domain and all-field target round trips, bounded numeric arithmetic/duplicate rejection, pinned dependency/SQLite interrupt checks, and continuation9/11/7/9 plus reviewed11+9=20 traces. Resolve parser licensing before PDF dependencies and author reviewed source/factor/date/authority/fixture packs before complete case execution. Deliver E-N01's actual fixture pipeline first, then E-M01, E-P01, source-backed E-N01 correction and E-F03 QA variants, basic five-screen behavior and offline notebook/HTML. All critical applicable checks remain required; optional full-corpus/retrieval/timing studies remain extensions. Later Nebius compatibility/token/rates/access and explicit Live allowance are separate. No tests or application scaffold are created by this refinement.

## Educational review fixes incorporated

Keep [core versus extension acceptance](../specs/overview.md) and [evaluation QA](../evaluation/evaluation-plan.md) authoritative. Runtime fixtures need registered variant and normalized current-stage input digests, with [E-N01 correction](../evaluation/examples/e-n01-correction.md) and [E-F03 Reject](../evaluation/examples/e-f03-reject.md) variant designs. Keep the two QA checks high level in offline results, with no additional UI/data infrastructure or model judge.

Initial fixture authoring covers core cases/variants; all thirty packages, full/batch/benchmark commands remain optional extension work rather than mandatory first-day scaffolding. Compatibility checkpoints are proposed tasks, not verified package capabilities. R4 choices and the subsequent Phase5/first-milestone approvals remain pending.
