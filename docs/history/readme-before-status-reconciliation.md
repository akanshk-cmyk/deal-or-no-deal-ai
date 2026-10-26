# Historical README ? superseded implementation status

Do not use this archive to determine current capability. See ../implementation-status.md.

# Deal or No Deal AI

**Financial fixture workflow:** In New Deal select **Human review required** and
run as simulated Analyst. Open Workspace, select simulated AuthorizedApprover,
enter comments and confirm Approve/Reject; the same financial graph resumes and
generates its memo. Request Additional Information keeps approval blocked. A
RiskManager can assess an exact registered PDF against every item and start the
registered revision2 reassessment on the same ledger; unknown/changed documents
remain unsupported. History shows real fixture decisions and scoped CSV, separate
from the illustrative preview. See [the integration contract](../specs/financial-review-integration.md).

Teaching artifacts: [Jupyter workflow](../../notebooks/01_workflow.ipynb) derives the local
diagram from the shared graph; optional Jupyter/IPython is not installed/verified.
[Offline six-page snapshot](../../prototype/index.html) is clickable and read-only; it
does not execute the graph or invent decisions. Re-export uses the explicit
tools/export_html_demo.py command and preserves an existing snapshot rather than
silently overwriting it. Live inference, embeddings and evaluators remain disabled.

**UI redesign V2:** The local app now uses navy navigation, slate/white surfaces,
deal-centric grouping, analysis tabs, contextual evidence buttons, recorded stage
cards and a document-style memo. Restart Streamlit to load updated modules/theme.
Run `.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1`.
See [the implemented redesign scope](../design/redesign-v2.md). Actual human
decisions/uploads remain unavailable in this financial fixture path.

**Current command center (2026-10-24): Run `.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1` from this checkout. Six destinations show the actual E-N01 fixture pipeline, source citations, execution events and stored memo. Select New Deal and explicitly start the registered sample as Analyst. Navigation never dispatches. Financial Decision History currently shows execution events, not human decisions. The separate illustrative review preview retains role actions/CSV. Financial HITL, information fulfilment, Conditional controls, generic uploads, notebook/HTML and Live remain pending. Earlier full-shell-pending notes describe previous slices.**

**Decision History** is now a dedicated page in the local preview: choose Page → Decision History in the sidebar. Review saved actions across permitted UI deals, filter by deal/borrower/reviewer/action/status/UTC date, inspect event-time context and open clickable deal timelines. Prepare CSV audit report exports all filtered authorized events across pages. Earlier events retain their original context; unavailable names/amounts/AI/risk/documents say Not captured. The preview does not invent submission/AI lifecycle events or connect actual financial reviews. CSV is supported; PDF is deferred. [Feature contract](../specs/decision-history.md).

The **role-aware Human review panel** now has a working local preview. It supports comments, Approve, Reject and Request Additional Information (Pending), with simulated role permissions and retained UTC-stamped history. Run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run tools/preview_human_review.py --server.address 127.0.0.1
```

Choose Prepare UI review samples, select a sample and demo role, then choose an action and enter comments. Approve/Reject require the correct Approver tier and no outstanding blockers; Administrator is read-only. A request for information requires specific items and prevents a final decision. Drafts survive validation errors/deal switching; Refresh review updates a changed record. These are clearly labeled illustrative UI examples in the same local database, not executed financial reviews or real approvals. The full five-screen app and financial interrupt/resume integration remain pending. See [REVIEW-UI-1.0](../specs/human-review-corrections.md#role-aware-review-comments-and-actions--review-ui-10).

**Quality preparation and local response review — 2026-10-24:** The [QUALITY-REVIEW-1.0 contract](../evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) adds complete source/basis preparation, per-field extraction diagnostics and source-review packets for all summary fields. The explicit offline command below preserves a supplied original response and task snapshot under ignored var/, then records conservative checks. It cannot run a model, grant human support or accept a recommendation into the app.

```powershell
.\.venv\Scripts\python.exe tools/prepare_model_comparison.py
.\.venv\Scripts\python.exe tools/review_model_response.py PATH_TO_LOCAL_CAPTURE_JSON
```

PATH_TO_LOCAL_CAPTURE_JSON is a local QUALITY-CAPTURE-1.0 JSON record: version, canonical attempt_id UUID, attempt_number (1–5), selected model_id, stage (extractor/synthesizer), exact current task_digest from the preparation report, origin (FIXTURE_TEST/UNVERIFIED_CAPTURE), completion_status (COMPLETE/TRUNCATED/REFUSED/ERROR/UNKNOWN), and original output_text. These declarations do not verify a Nebius call. Use a new attempt ID for each repair; existing original artifacts are not overwritten. Never include secrets or confidential borrower documents. Live adapter/schema/tokenizer checks, funded runs, manual semantic review, further registered cases and optional RAGAS remain pending.

**Authorized normal Fixture slice — 2026-10-23:** [E-N01-SYNTHESIS-1.0](../specs/synthesis-evidence.md#authorized-e-n01-normal-slice--e-n01-synthesis-10) binds the current synthesis request, exact educational stage response and four narrative evidence targets. The normal nine-stage LangGraph/SQLite path, primitive panel handoffs and pure seven-section memo are now implemented; scoped executed checks are recorded in execution.md after verification. Only E-N01/default is supported. Other cases, actual human-review interrupts/corrections, full UI/notebook/HTML and Live remain pending. Fixture expectation checking is not HUMAN_SUPPORTED or a real model-quality result; provider calls remain disabled. Earlier partial/no-graph status notes describe their historical slices.

Generation-model comparison preparation: [GEN-COMPARE-1.0](../evaluation/generation-model-comparison.md) compares Qwen3-30B-A3B-Instruct-2507 with Nemotron-3-Nano on the same synthetic tasks. Run `.\.venv\Scripts\python.exe tools/prepare_model_comparison.py` to prepare the shared E-N01 extraction and synthesis packets and explicit readiness report under ignored var/. This command makes zero provider requests; model quality/latency/usage/winner remain Not run/null. Other scenario packs and provider/token/budget setup remain pending; both E-N01 task packets are prepared offline. No application model is switched.

**Current embedding decision — 2026-10-23:** [ADR-008](../architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. The deployed API/tokenizer/input limits and paid allowance remain unverified; execution/indexing stay disabled. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

*Every deal has a story. Our agents find the plot holes.*

Run the implemented normal synthetic workflow locally:

```powershell
.\.venv\Scripts\python.exe tools/run_e_n01_fixture.py
```

The command prints its operation UUID and generated memo path under ignored var/demos/e-n01.
Repeat with `--operation-id THE_SAME_UUID` to read that recorded result without replay.
Only E-N01/default is supported by this slice; other cases and actual human-review
branches remain pending. The generated memo is an educational Fixture result with
zero provider requests, rather than a measured live-model recommendation.

Local educational prototype using synthetic USD small-business loans. No real
lending, compliance clearance, investment advice or production-readiness claim.

## Current scope

Latest implementation: the user chose to download/upload the public document.
**Actual uploaded-PDF inspection passed;96 combined methods passed.**
Optional Crawl4AI0.9.5/sentence-transformers6.2.0 and CPU torch2.14.1+cpu are
installed/locked, with an offline import/CPU smoke check. No browser setup,
website crawl, BGE weights, vector index or retrieval benchmark has run. The
newly supplied47-page PDF has now been inspected. [Current source-binding evidence](../execution.md#uploaded-reference-inspection-and-source-binding-correction).

Inspect an explicitly supplied public HTML/text-PDF file locally:

```powershell
.\.venv\Scripts\python.exe tools/check_public_source_setup.py
.\.venv\Scripts\python.exe tools/inspect_local_reference.py "PATH_TO_DOWNLOADED_FILE"
```

For Windows-1252 HTML, explicitly add `--html-encoding windows-1252`.
Inspection retains original bytes/report under ignored var/reference-inspections,
never executes scripts/fetches links, and reports source origin/support as
unverified. LOCAL-REFERENCE-1.1 leaves corpus membership/source identity unbound;
the configured company/URL is an expectation, never an uploaded-file citation.
It does not calculate a loan score or create an index.


Approved public-reference architecture: **local-file intake (optional Crawl4AI) + Nebius-hosted
embeddings (model setup pending) + SQLite-backed vector storage with bounded
exact cosine search**. [Accepted ADR-007](../architecture/decisions/007-proposed-public-financial-rag.md)
and the [source contract](../specs/public-financial-sources.md) record the selected
SEC credit-agreement URL and separate reference-corpus scope. Source/architecture
approval is resolved. Dependency/browser/model revisions, setup and implementation
remain pending; no crawl, embedding/index build or retrieval benchmark has run.
Default setup commands below install the core only. The previously installed local
embedding packages are historical and are not required for the hosted path. Do not
run the retired local-model download command. Nebius embedding setup is pending. Keep DIRECT loan grounding and compare all four retrieval arms
before any default change.

Current milestone: the exact [E-N01 source/assessment/default extraction](../../config/registrations/e-n01.json)
is registered under the user's A1-A4 approval. Actual PDF source checks now feed
scoped financial calculations, fictional policy handlers and authored risk scoring.
**85 tests passed.** The offline result is21/100 Low,0 policy exceptions and0 missing
material inputs; confidence awaits synthesis, final_decision is null and final_ready
is false. This is a deterministic application-test slice, not a complete graph or
model-quality result. [Current evidence](../execution.md#m2-registered-deterministic-panels-evidence).

Run `.\.venv\Scripts\python.exe tools/run_e_n01_panels.py` to write the scoped result
to ignored `var/evaluations/e-n01-deterministic-panels.json`. It accepts only the
registered default; no gold/reference manuscripts or provider calls are used.

The earlier M2 source/parser slice introduced an [E-N01 draft source pack](../../fixtures/development/e-n01/README.md)
with three PDFs/five authored pages and an internal FIN-1.0 arithmetic kernel.
**69 combined tests passed.** The user-approved [parser decision](../architecture/decisions/006-proposed-pdf-parser.md)
is implemented: pypdf6.21.2 parsed all five current pages, which passed full plain/layout
comparisons and focused year/unit/qualification/zero-lien checks. Technical draft2
fixes PDF font encoding; original draft1 and initial failed evidence are retained.
These earlier parser results precede the registration above. Full graph/synthesis/
correction/report/UI and Live execution remain pending. See [parser evidence](../execution.md#m2-parser-installation-and-pdf-verification).

Reproduce known-corpus verification with
`.\.venv\Scripts\python.exe tools/verify_e_n01_pdfs.py`.
The report/raw extraction are under ignored `var/evaluations/e-n01-pdf-verification/`.
This entry point accepts only the known generated sources; it does not enable
general uploaded-PDF review or confer source authority/human support.

The M1 foundation is implemented and locally tested. Its scope is strict contracts,
bounded context loading, exact storage, execution admission, review guards and
offline LangGraph compatibility checks. A complete deal pipeline, UI, sample
case registrations beyond E-N01/default, notebook, HTML walkthrough and Nebius integration are later milestones.

Specifications: [PRD](../product/prd.md), [architecture](../architecture/hld.md),
[execution plan](../execution.md), [feature overview](../specs/overview.md).
The `docs/agents` directory is the sole instruction source; archived prose is not
model context.

Retrieval roadmap: prepare reviewed synthetic sources first, then implement and
report DIRECT, KEYWORD, VECTOR and HYBRID. VECTOR is the semantic retrieval baseline;
RRF combines rankings. Consider a separate reranker only if measured ranking errors
justify its added processing. See the [benchmark sequence and current capability status](../evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision).
Retrieval adapters and benchmark results remain unimplemented/unmeasured; M1 tests
do not establish retrieval quality.

Document checks are now implemented separately in `documents.py`: explicit
year-column alignment, row-label/unit/source references, and complete declared
passage dependencies. BASELINE withholds incomplete evidence; opt-in ADAPTIVE can
restore accepted original blocks. The registered E-N01 services now qualify actual parsed inventory before using
the deterministic panels; generic parsing and the full loan graph remain pending. See [the contract](../specs/context-optimization.md#parsed-document-verification-and-paired-checks--docverify-10)
and [executed evidence](../execution.md#document-verification-extension-evidence).

Document-check extension result: **55 tests passed** before the M2 slice. Its separate offline comparison
checked **14 synthetic cases in both modes (28 executions), with zero check
failures**. It measures deterministic controls, not LLM quality or PDF fidelity.
Reproduce the comparison with `.\.venv\Scripts\python.exe -m tests.compare_document_verification`;
the report is written to ignored `var/evaluations/document-verification-paired.json`.

## Local setup and checks

The optional embedding-library cold import took77.530 seconds without loading
weights. This is measured setup time, not query latency. Application import,
source inspection and ordinary views do not load those libraries.

Python 3.12 and uv are required. Setup downloads dependencies; tests use temporary
databases and prohibit outbound network access. No API key is needed.

```powershell
uv sync --python 3.12 --group dev
uv run --frozen --python 3.12 pytest tests/unit tests/integration
uv build --python 3.12 --no-sources
```

Historical M1 baseline: **43 tests passed** under Python 3.12.15, including Pydantic wire
validation, two-process SQLite admission and actual LangGraph pause/reopen/resume
with a committed-review recovery variant. Dependency installation succeeded;
`.venv` and `uv.lock` now exist, and a local source/wheel build passed.
An additional import check blocked network/database access while tracing flags
were enabled and confirmed zero attempted side effects. See the evidence in
[the execution plan](../execution.md#m1-implementation-evidence).

With an existing Python 3.12 interpreter, `tests/run_offline.py` runs only the
explicit stdlib subset. This does not install dependencies or replace the full
M1 suite. The optional LangSmith pytest plugin is explicitly disabled; its SDK is
a transitive dependency and no hosted tracing service is connected.

Tested direct packages: Pydantic 2.14.1, LangGraph 1.2.16, langchain-core 1.7.0,
SQLite saver 3.1.2, Streamlit 1.66.1, pypdf6.21.2 and pytest 9.1.1. Use `uv.lock` rather than
installing these independently. Build artifacts are under ignored `dist/`; they
are local packages, not a self-contained app or a deployment. Prompts/configuration
remain in this source checkout. M1 does not establish model quality, token fit,
financial workflow completion or UI usability.

Live models, hosted tracing, RAGAS scoring and automatic downloads at app startup
are disabled. Never put keys, real borrower data or raw prompts in logs, fixtures,
notebooks, reports or version control. Local runtime state belongs under ignored
`var/`. No automatic expiry or history cleanup is implemented. No project license
has been selected; no external repository or deployment has been created.

## Third-party credits

Crawl4AI is an optional installed dependency; its installed license includes an
additional attribution requirement:

This product includes software developed by UncleCode (https://x.com/unclecode) as part of the Crawl4AI project (https://github.com/unclecode/crawl4ai).

This credit does not select a license for this project. Browser binaries and BGE
model weights are separate setup artifacts and have not been installed.
