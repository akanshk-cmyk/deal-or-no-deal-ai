# Deal or No Deal AI

## Unified review experience - 2026-10-25

The saved-response UI is the shared baseline. Use one Run AI Deal Review action;
there is no user-facing mode selector. Existing config/app.toml mode selects new
FIXTURE (default, no calls) or LIVE (explicit paid Nebius execution). Both sources
share the six screens and per-deal history. Historical source controls display
and resume; live human verification and all backend rules remain unchanged.
See [the unified review contract](docs/specs/unified-review-experience.md). Earlier sidebar mode instructions
are superseded. This UI change does not authorize a new paid test.

## READINESS-1.0 current update - 2026-10-24

Approval readiness is separate from the original AI proposal and the human credit decision. Standard Deal retains its saved Approve proposal but is Pending Review because mandatory covenant evaluation is incomplete. Readiness is shared across Dashboard, Workspace, Memo and History. See docs/specs/approval-readiness.md and docs/evaluation/approval-readiness-results.md. Historical reports remain original snapshots.


## LIVE-GRAPH-1.0 implementation update - 2026-10-24

User authorized completing the live graph and evidence checkpoints. Follow
[the live graph contract](docs/specs/live-graph-integration.md). The shared build_graph now has an explicit
live branch with a pre-calculation fact_review interrupt and a post-synthesis
evidence_review interrupt. live_worker uses the existing SQLite admission/ledger,
checkpointer, strict wire parsers and deterministic finance/policy/risk services.
Actual response text is retained; registered sample answers are never a fallback.
ReviewedLiveCase binds the actual extraction to source/profile validation and
immutable human-support receipts without changing the original registration.

Every present term/financial fact and authored scoring premise needs RiskManager
support. Every observation, rationale, condition and next-action reason has an
exact target; policy/control meaning requires ComplianceOfficer support and mixed
content needs both domains. Source quotations, seven explicit checks, comments,
role, target/source digests and UTC timestamps are recorded. Support is metadata
only. Analyst continuation resumes the same checkpoint and cumulative ledger.
Confidence-only normal credit review has a separate AuthorizedApprover checkpoint.
Missing information stops before dependent work; live exceptions/conditions beyond
this bounded E-N01 example stay blocked, never generically waived.

Sidebar Review mode selects saved responses or Live AI reviews. Live review start,
evidence forms, recorded activity, source-linked pure-Python memo and scoped local
history are connected. Live setup/readiness remains in the sidebar only.
Provider calls use the worker's existing admission claim, reserve the shared
USD0.10 allowance and record actual reported usage; uncertain usage retains its
reservation and blocks replay. No global enable-flag flip or new database.

This is implemented integration, not evidence of paid model quality. Provider
access, hosted model/schema/current rates and exact whole-request counts still
require verification; each changed synthesis packet needs its own count evidence.
No real Nebius call or judge was executed for this implementation. Hosted vectors,
hybrid semantic benchmarking and LLM-based RAGAS remain separate pending work.


**Demo mode — saved AI responses:** the app uses prepared example AI responses, while calculations, policy checks and review steps run normally. No paid AI calls occur in this mode. Developer code and file names retain `FIXTURE` for compatibility.

## Live foundation update ? 2026-10-24

User approved LIVE-COMPACT-1.0: extraction 4,000 input/1,000 output;
synthesis 2,500/650. Aggregate 8,000/2,000 and protected correction
1,500/350 remain unchanged; Demo prompts and stage limits are unchanged.
The shared authorized spending allowance is USD0.10 across generation, embeddings
and evaluation. See [live integration specification](docs/specs/live-synthetic-integration.md)
and [approved fit profile](docs/evaluation/live-fit-proposal.md).

Implemented: separate live specialist prompts, compact full-source E-N01 offline
packets, explicit credential/readiness checks, guarded transport foundation with
persistent allowance reservation, four-arm retrieval mechanics, and optional
RAGAS 0.4.3/tokenizer dependencies. RAGAS requires the tested
langchain-community 0.3.31 compatibility pin; ID metrics currently use its
available public API with deprecation warnings.

Measured: local packet components 3,699 extraction and 2,282 synthesis tokens;
provider rendering overhead remains unverified. Six actual native RAGAS ID
measurements over three synthetic questions: DIRECT recall 1.0 (precision not
applicable); KEYWORD recall 1.0, precision 0.5. These tiny author-authored cases
are diagnostic, not proof of semantic quality. VECTOR/HYBRID mechanics tests use
synthetic vectors, not hosted embeddings. No real generation, embedding or judge
calls have run; paid spend is zero. Complete live graph integration, source-backed
critical-fact/narrative review, hosted embeddings/indexing, semantic benchmarks and
LLM-based RAGAS/custom quality scores remain pending. The local API key is absent;
model/schema/current rates and whole-request fit still require verification.
An API key alone does not activate Live mode.


*Every deal has a story. Our agents find the plot holes.*

Local educational financial-review application: six Streamlit screens, a real
LangGraph workflow, deterministic finance/policy/risk checks, source inspection,
human-review interrupts, generated memos and retained decision history.
**Model stages currently use registered synthetic responses, not live inference.**

## Start the application

From the reviewed checkout in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.fileWatcherType poll
```

Open the URL printed by Streamlit. An older server can retain imported modules;
restart that server after code changes. A browser refresh alone may not reload them.

Choose **New Deal**, simulated **Analyst**, then Normal review or Human review
required. Starting is explicit; reading pages never dispatches a review.

If Human Review is read-only on a completed **Normal review**, choose **Prepare a
review-required sample**, then run it as Analyst. Normal runs have no financial
review request. On active reviews choose an action, enter comments and click Submit;
you do not need to click outside the text field first. The submit button is labeled
**Record financial review action**. Final decisions still require
the permitted role, confirmation and all gates. Preparation alone executes nothing.

**E-M01 Missing CFADS** is also selectable. It runs the real graph through risk
checks, then pauses for the missing annual cash schedule. Available facts retain
their own citations; no complete score, AI decision or final memo is generated.
Replacing the missing schedule and continuing this case remains unsupported.

**E-F03 Supported Reject** is now selectable. Start as Analyst, then open
**Review Workspace → Human Review**:
switch to RiskManager, select all required supporting evidence, enter a handling
reason and record Recommend Reject. Switch to AuthorizedApprover, add final comments,
select Reject and confirm. The same paused graph resumes and generates the memo.
Before handling, both final actions are blocked. The policy still says Exception;
handling is a separate recorded judgment. The Moderate45/100 score is not a rejection
rule. History/CSV include the handling and final decision with original snapshots.

For the reviewed sample, select **AuthorizedApprover** in Workspace, inspect
sources, enter comments and confirm Approve/Reject. Request Additional Information
keeps final decisions blocked. **RiskManager** can assess an exact registered PDF
response for every requested item and explicitly start revision2. This preserves
the original review ledger/history and uses a new graph thread. Changed or unknown
PDFs and additional unsupported corrections are rejected.

## Screens

1. **Deal Dashboard:** distinct-deal KPIs, attention queue, borrower/risk/financial/
   policy/workflow/action cards. No invented exposure, owners, PD or trends.
2. **New Deal:** registered E-N01, E-M01 and E-F03 samples; arbitrary intake unavailable.
3. **Review Workspace:** terms, calculations, rules, risk, citations and role-aware review.
4. **Agent Activity:** recorded graph execution and structured handoffs.
5. **Credit Memo:** actual stored seven-section report; AI versus human decisions separate.
6. **Decision History:** permitted financial events, search/filter/pagination, original
   snapshots, selected-deal timeline and all-matching CSV export.

All identities and lending policies are educational simulations. SQLite retains
versioned history; it is not immutable or tamper-proof audit storage.

## Development and verification

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
.\.venv\Scripts\python.exe tools/run_e_n01_fixture.py
.\.venv\Scripts\python.exe tools/prepare_model_comparison.py
```

Use the approved lockfile/setup instructions in AGENTS.md. No dependency install,
provider request or deployment is performed by opening the app or importing modules.
Offline provider-envelope tests exercise schema/finish/usage handling without a
client or credential. They do not prove Nebius model compatibility or quality.

## Teaching artifacts and boundaries

- [Shared workflow notebook](notebooks/01_workflow.ipynb): diagram uses the same graph.
  Code syntax is tested; fresh Jupyter-kernel execution remains unverified.
- [Clickable offline snapshot](prototype/index.html): read-only recorded sample;
  clicks do not execute agents or save decisions. Its exporter preserves old snapshots.
- [Current implementation status](docs/implementation-status.md): capability matrix
  and dependencies. This supersedes earlier milestone status paragraphs.
- [Execution evidence](docs/execution.md): actual commands/results and limitations.
- [Product requirements](docs/product/prd.md) and [architecture](docs/architecture/hld.md).

E-P01 Conditional demo: New Deal → choose E-P01 → run as Analyst. In Human Review,
RiskManager records exception handling; AuthorizedApprover prepares the registered
condition; RiskManager and ComplianceOfficer each record specialist support;
AuthorizedApprover chooses Conditional Approve or Reject. Each form requires reason
and source evidence. The condition remains OUTSTANDING and does not cure DSCR.
See [contract](docs/specs/conditional-integration.md).

Source correction demo: New Deal → E-N01 Extraction miss → run as Analyst →
Review Workspace. Inspect FIN-P2, enter CFADS `900000`, basis `FY-ASSESS`, page
`FIN-P2`, reason and verification → Save source-backed correction. The new revision
is READY; click Update affected findings to run analysis. Save alone runs nothing.
Original extraction remains historical and the memo identifies reviewer correction.
See [contract](docs/specs/source-correction-integration.md).

Upload inspection: New Deal → Upload New Deal → submit1–3 synthetic text PDFs and
confirm educational data. Inspect retained file/page citations and download originals.
Limits:10 pages/10 MB combined. Status is Inspected—not reviewed; no AI score/memo
or automatic registration. No model call. See [contract](docs/specs/upload-inspection-integration.md).

Uploaded evidence: Analyst proposes annual CFADS, principal and interest from exact
source quotes with units/period/subject/facility. RiskManager checks each candidate
and records support or withholding. Three compatible supported inputs enable the
annual DSCR preview; replacing a proposal requires fresh support. No AI extraction
or credit decision. See [contract](docs/specs/upload-fact-review.md).

Pending: complete uploaded-source/critical-fact onboarding and full analysis, general field/value corrections, completed/interrupted-review corrections,
arbitrary condition editing/fulfilment,
new-document continuation,
funded Nebius integration, retrieval benchmarking and offline RAGAS execution.
Live, embedding, evaluator and hosted-tracing enable flags remain false. API access
and a hard review ceiling do not authorize spending. No real lending use,
production-readiness, calibrated default prediction or bank-compliance claim.

## Using the live review workflow

1. In the sidebar choose **Review mode > Live AI reviews**.
2. Use **Live AI setup and readiness** in the sidebar to inspect blockers. The current
   local key is absent and hosted provider verification is pending; a key alone does
   not enable calls. Keep secrets only in ignored `.env` or the environment.
3. Once prerequisites are verified, **New Deal > Start live Standard Deal review** explicitly
   starts the registered fictional example, never arbitrary uploaded PDFs.
4. In **Review Workspace**, Risk Manager verifies every extracted fact/scoring premise
   with source quotations, checks and comments. Analyst explicitly continues.
5. The graph runs calculations, policy and scoring. If the next request needs setup
   or token-fit verification it pauses before dispatch and retains the exact packet.
6. After synthesis, Risk Manager and Compliance Officer each verify the generated
   narrative. Their evidence assessments do not approve credit. Analyst continues.
7. When Python requires normal credit review, Authorized Approver separately records
   Approve/Reject and comments; Analyst then continues to the pure-Python credit memo.
8. Inspect citations, recorded model responses and usage in the review/activity/memo
   views. Live support/decision history is distinct from saved-response history.

This first live slice blocks unhandled policy/score escalation and proposed
conditions; general live exception handling, source correction and arbitrary-upload
financial admission remain outside it. Tests use mocked Nebius responses and do not
prove actual model quality. No real provider request has been run by this change.
