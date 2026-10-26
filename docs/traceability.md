# Deal or No Deal AI — Requirement Traceability

## Current upload acceptance update - 2026-10-25

The user authorized fixing the upload acceptance gaps. This update supersedes
older exact-Standard-only, inspection-only and sequential-only statements for
**new uploaded synthetic text-PDF reviews**. Historical records are unchanged.
See `docs/specs/general-upload-acceptance.md` for the implementation contract.

New uploads can declare their own borrower, reporting periods, transaction date,
USD whole-unit basis and sample-policy applicability. Declarations are unverified
and must be checked against the retained documents. Unknown inputs/applicability
stay unknown. No sample borrower facts or factor ratings are copied. Existing
parser, token, permission and shared spending limits remain in force.

New uploaded reviews use live extraction -> mandatory fact/profile verification
-> parallel Financial / Compliance / Risk subgraph -> joined synthesis ->
mandatory narrative verification -> readiness routing -> partial or complete memo.
Only the parent persists branch outputs; calculations and policy rules are
unchanged. Missing borrower factor assessments produce Insufficient Data, never
a default Low score. Partial reports do not waive approval blockers. The same
Deal ID and uploaded page map feed Workspace, Agent Activity, Memo and History.
Sample Deal and historical contexts keep their existing execution policies.
No new dependencies, migrations, inference model settings or budget were added.
Phase 2 evaluation remains deferred. Offline provider mocks establish functional
behavior, not fresh Nebius answer quality or genuine human verification.

**Current role/flow alignment:** FR-008/011/019 -> SPEC-007/010/011 and
[specialist handoffs](specs/specialist-handoffs.md) ->
`tests/unit/test_specialist_activity.py`, existing command-center/live-graph UI
checks -> current-run output reference correctness, zero writes/calls on view,
correct missing-information and human-pause presentation. README and PRD share
the examiner diagram; HLD retains the same role/dependency/authority boundaries.
The four focused projection and seventeen compatibility checks passed; no scale
measurement or new live completion is implied.

Current unified experience (2026-10-25): [approved contract](specs/unified-review-experience.md).
One Run AI Deal Review action uses config/app.toml mode; saved and live records
share the existing saved UI. Earlier sidebar mode and separate layout descriptions
are historical. Live interrupts, source labels and backend authority remain intact.

## READINESS-1.0 current update - 2026-10-24

FR-READY-001..005 -> docs/specs/approval-readiness.md -> tests/unit/test_readiness.py, tests/integration/test_approval_readiness.py and existing financial_review, live_graph, conditional_review, command_center tests -> forbidden-approval count 0; duplicate decisions 0; unchanged original proposal/source checks; correct readiness outcomes and consistent UI rendering. Measured results: docs/evaluation/approval-readiness-results.md.


**Uploaded candidate support:** SPEC-001/002 FACT-SUPPORT-1.0 / SPEC-003/008/010 →
specs/upload-fact-review.md → tests/integration/test_upload_facts.py. Measures scoped
proposal/support/guard correctness, fresh compatible annual DSCR and UI citation
navigation. Does not measure original AI accuracy or complete uploaded-case readiness.

**Uploads:** FR-001–003/015/019–020 → SPEC-001 / specs/upload-inspection-integration.md
→ tests/integration/test_upload_intake.py. Metrics: valid synthetic package retention/
citation success and guard pass rate; no score/financial-admission/model-quality
claim. Actual browser file upload evidence is recorded in execution.md.

**Source correction:** SPEC-002/007/008/009/010/013 →
specs/source-correction-integration.md → tests/integration/test_source_correction.py.
Checks source-backed fact restoration, explicit no-dispatch Save, new READY revision,
shared budgets, separate Update, unchanged source/parent, exact corrected synthesis,
permission/stale/idempotency/concurrency/tamper guards and memo/history/CSV/UI.
Metric: synthetic correction-path and guard pass rate, not original-model accuracy.

**E-P01 / conditional review:** human permissions, supported-condition, grounding,
source navigation, history and report requirements → specs/conditional-integration.md
→ tests/integration/test_conditional_review.py. Covers all distinct specialist gates,
exact draft/evidence, stale/duplicate/concurrent commands, forbidden invention,
information/source/tamper controls, actual conditional/reject graph, memo/CSV/UI.
Metric: synthetic path/guard pass rate; no live quality/cost claim. This supersedes
historical E-P01-pending observations below; arbitrary editing remains unavailable.

**E-F03 / exception handling:** role/gate/source/history/report requirements →
specs/exception-reject-integration.md → tests/integration/test_exception_reject.py.
Five integration checks cover complete supported Reject, forbidden premature/final
roles, stale and duplicate commands, exact refs/source version, competing identical
handling, information blocking, receipt tamper and actual UI handoff/memo/history.
No generation replay; original exception/AI unchanged. Full and focused results:
execution.md. Does not complete E-P01 Conditional or predictive/live quality.

**E-M01:** missing-data/nonfabrication/source-navigation/role requirements →
specs/missing-data-integration.md → tests/integration/test_missing_data.py:
actual information END, five completed nodes, zero synthesis/report calls,
null score/decision, exact missing field, source binding, duplicate read, cross-case
scope/count isolation, Analyst-only start and blocked UI final actions. Quality
scope is an executed synthetic workflow, not live extraction/summary performance.

**Pending-work implementation (2026-10-24):** provider compatibility requirements →
PROVIDER-1.0 section in evaluation/generation-model-comparison.md → provider.py +
tests/unit/test_provider.py (offline envelope/schema/accounting only); FR-021 →
SPEC-013 → financial history query/filter/CSV and integration/UI tests; core
scenario prerequisites → approved core-case-authoring-proposal →
tools/prepare_core_case_sources.py + test_core_case_sources.py + kernel-only scenario
checks. Source preparation does not satisfy end-to-end Reject/Conditional acceptance.
Current capability evidence is indexed in implementation-status.md/execution.md.

**Financial integration milestone:** FR-010/014/020/021 → SPEC-007/008/009/010/013 +
FIN-REVIEW-1.0 / FIN-REASSESS-1.0 → tests/integration/test_financial_review.py and
test_connected_financial_review_ui_decision_memo_and_history in test_command_center.py.
Checks actual pause/reopen/resume, role/tier/stale/duplicate guards, frozen history,
comments, information blocking, exact registered response, revision2/new thread,
same ledger, stale old approval, reviewed memo and scoped CSV. TEST-007/008/009/010/
011/013 are extended, not wholly completed. Teaching artifact tests check shared
graph SVG, notebook syntax, six HTML destinations and read-only exact-source export.
Live model quality, general intake, Conditional and other case families stay pending.

**Policy-display audit fix:** FR-020 → SPEC-010 / POLICY-VIEW-1.0 →
test_policy_display_uses_final_recorded_evaluation_without_mutating_history and
test_final_policy_card_and_evidence_agree_and_source_mismatch_withholds_links in
tests/integration/test_command_center.py. Covers completed versus preliminary
state, memo/reference consistency, original-record preservation, scope/input
mismatch rejection and unavailable-source link withholding. No financial HITL or
additional-case acceptance is implied.

**UI redesign V2:** FR-020/021 → SPEC-010/013 +
[V2 presentation contract](design/redesign-v2.md) →
tests/integration/test_command_center.py: borrower grouping, older-run selection
across pages, contextual factor/source navigation, disabled human decisions,
read-only upload placeholder and the original worker-to-memo flow. This is scoped
UX/application evidence; backend HITL, actual uploads and WCAG acceptance remain
pending. Local browser screenshots are retained under ignored
var/evaluations/redesign-v2, without creating or approving financial records.

**Normal financial UI integration (2026-10-24): FR-001/009/014/020/021 -> SPEC-010/013 + [APP-READ-1.0](specs/financial-command-center-integration.md) -> tests/integration/test_command_center.py and normal-graph tests -> scoped TEST-007/010/011/013 and MET-09/15/19 application evidence. Financial approval, generic uploads and complete feature/metric acceptance remain pending.**

Decision History mapping2026-10-24: FR-021 → [SPEC-013](specs/decision-history.md), SPEC-008/010/011 → tests/integration/test_decision_history.py + test_decision_history_ui.py, existing review/normal graph regressions → TEST-013-01–07 and relevant MET-09/15/19 application/preview evidence. This adds a sixth page/scoped CSV explicitly; no full workflow, financial quality, manual accessibility or production audit claim follows.

**Human-review UI mapping — 2026-10-24:** FR-010/014/020 → SPEC-008 REVIEW-UI-1.0 + SPEC-010/011 → tests/integration/test_review_actions.py and test_human_review_ui.py, with existing test_review_basis.py guards → MET-09/13/15/19 as applicable. These implement scoped application/preview checks, not completion of whole metrics, full financial resume or manual usability. Role/scope/tier/basis/gate checks, comments/status/UTC history and information-request blocking are exercised; original E-N01 recommendations/reports remain separate.

**Quality preparation mapping — 2026-10-24:** [QUALITY-REVIEW-1.0](evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) maps SPEC-002/005/006/007 to tests/unit/test_model_quality.py and tests/integration/test_quality_review.py, extending TEST-002/005/006/007 and MET-03/04/05/07/08/09/16. model_comparison.py prepares full-source/basis-aware requests and field/narrative diagnostics; quality_review.py retains exact captures/tasks without modifying the application database. Test-double checks do not populate observed live model metrics or human support. See the current execution record for actual commands/results.

**Authorized normal Fixture slice — 2026-10-23:** [E-N01-SYNTHESIS-1.0](specs/synthesis-evidence.md#authorized-e-n01-normal-slice--e-n01-synthesis-10) binds the current synthesis request, exact educational stage response and four narrative evidence targets. The normal nine-stage LangGraph/SQLite path, primitive panel handoffs and pure seven-section memo are now implemented; scoped executed checks are recorded in execution.md after verification. Only E-N01/default is supported. Other cases, actual human-review interrupts/corrections, full UI/notebook/HTML and Live remain pending. Fixture expectation checking is not HUMAN_SUPPORTED or a real model-quality result; provider calls remain disabled. Earlier partial/no-graph status notes describe their historical slices.

**Current embedding decision — 2026-10-23:** [ADR-008](architecture/decisions/008-nebius-hosted-embeddings.md) supersedes the earlier local-BGE selection. Use Nebius-hosted embeddings; no local embedding weights are required. Qwen/Qwen3-Embedding-8B is selected; its dated catalog dimensions/rates are recorded in ADR-008. Subsequent bounded generation/embedding capability probes and the shared USD0.10 allowance are verified; this does not establish a built public-corpus index or measured VECTOR/HYBRID quality. Each changed generation packet still needs exact token-fit evidence; the corpus benchmark remains pending. Retain local-file intake, source isolation, SQLite storage, DIRECT grounding and the four-arm benchmark. Earlier installation/test observations remain historical evidence, not hosted readiness.

**Current M1 evidence, 2026-10-23:** [M1 evidence](execution.md#m1-implementation-evidence) maps43 passing methods to scoped portions of existing TEST families, now including eight wire methods and the actual saver method with two variants. No whole90-ID feature inventory, deal workflow, Live quality or UI result is claimed complete. Runtime contracts and the positive requested-amount rule passed; no new TEST/MET IDs were added.

Version: 1.32
Date: 2026-10-23
Status: Approved traceability;85 combined methods passed2026-10-23; full graph/model/UI feature coverage remains planned

## Current implementation mapping

E-N01-SYNTHESIS-1.0 and the normal M3 slice map existing SPEC-002/003/004/005/007/009/011 and TEST-005/007/009/011 families to synthesis.py, panel_codec.py, graph.py, worker.py, memo.py, separate synthesis registration/fixture/rubric and the explicit run command. The executed normal graph has nine stages, four Python tools, source-linked handoffs, four narrative targets, SQLite checkpoints and a pure seven-section memo. [Current execution evidence](execution.md#executed-normal-e-n01-graph-synthesis-and-memo--2026-10-24) records120 tests/206 subtests, a generated local report and zero provider calls. This does not complete human-review/correction/other-case/UI/Live or model-quality coverage.

GEN-COMPARE-1.0 maps existing extraction/synthesis/grounding/budget FR-003/006/007/008/015/019 and SPEC-002/005/007 to config/generation_comparison.toml, model_comparison.py, tools/prepare_model_comparison.py and focused unit/CLI tests. Existing TEST-002/005/007 and model-quality/citation/cost/latency metrics retain their definitions. [Comparison contract](evaluation/generation-model-comparison.md) separates shared-source preparation and exact local checks from unrun provider, manual grounding and full-case measurements; no new release threshold or financial rule. Measured test evidence is recorded in execution.md after checks run.

LOCAL-REFERENCE-1.1 extends the same FR-002/003/007/019 and SPEC-001/006 source-isolation boundary: arbitrary uploads cannot inherit the configured company/URL/corpus. public_sources.py and the CLI emit null admission/empty declared source and explicit profile expectations; the existing source tests gain a matching-text/source-instruction regression. [96-method and real-PDF inspection evidence](execution.md#uploaded-reference-inspection-and-source-binding-correction) preserves earlier95/85 results as history. No index/loan-registration/credit score/model-quality claim.

LOCAL-REFERENCE-1.0: FR-002/003/007/019 and SPEC-001/006 map the local-file portion of PUB-01/02 to config/source_ingestion.toml, public_sources.py, inspect_local_reference.py/check_public_source_setup.py and eight unit/two CLI integration methods. [95-method evidence](execution.md#local-reference-setup-and-inspection-evidence) is actual setup/application evidence for supplied synthetic bytes, unsupported/oversize/encoding/encrypted/no-text/malformed-file handling, inactive HTML resources, unverified provenance and retained observation identity. No original core TEST/MET/scenario count is expanded. Actual public uploads/model artifacts/embeddings/vector schema/retrieval remain pending; no MET-23/RAGAS or financial-decision success is implied.

Accepted public-source extension maps source/privacy/grounding FR-002/003/007/019 and SPEC-001/006/011 to the [source contract](specs/public-financial-sources.md), [accepted ADR-007](architecture/decisions/007-proposed-public-financial-rag.md) and execution PUB-01-06. Local-file inspection is implemented; Nebius-hosted embeddings are selected under ADR-008 with model/API/allowance unconfigured, and SQLite exact-vector storage remains planned. Existing TEST-001/006/011 families and MET-23 cover planned mocked intake/network/snapshot controls, faithful tables/notes, temporal/company isolation, additive schema/build/model integrity and citations; all extension runtime checks remain Not run. Preserve separate synthetic/public corpus measurements. No frozen public corpus or passed release threshold is claimed; E-N01 evidence is unchanged.

CASE-REG-1.0/M2: FR-002–008/015/019 map SPEC-001/002/003/004/006 to the approved registration/sample-policy JSON, services.py, policy.py, risk.py and tools/run_e_n01_panels.py. Ten new unit methods and six registered-panel integration methods extend TEST-001-05/06, TEST-002-06/07, TEST-003-04, TEST-004-01/02/03/04/05/07/09/10/11, TEST-006-03/05. [85-method evidence](execution.md#m2-registered-deterministic-panels-evidence): actual source→registered extraction→Python panels, scope/date/unit/source/stage/policy tamper rejection, no gold input, independent assessments and high-level normal-case false-positive0/recall N/A. Relevant eventual MET-01/02/04/07/08/09/11/15/18 retain their definitions; these scoped tests do not establish complete families, real model quality, multi-case recall or business savings. Full graph/other cases/Live/UI remain pending.

Current parser scope: FR-002/003/007/019, SPEC-001/006, TEST-001-02/03/04 and TEST-006-02/03 map to tools/verify_e_n01_pdfs.py and three actual parser integration methods. [Parser evidence](execution.md#m2-parser-installation-and-pdf-verification):five pages pass full text/layout checks; altered bytes stop before parsing; year ambiguity and source-fit withholding are tested; combined69 methods pass. Related eventual MET-03/04/07/08/15 remain distinct from local extraction-fidelity checks. Known-corpus verification does not complete generic intake, source approval, registered Fixture or Live evaluation. Original failed evidence/source draft retained.

M2 partial: FR-002/003/004/007/019 map SPEC-001/002/003/006 to `finance.py`, the E-N01 draft pack, source-authoring utility, nine finance methods and two candidate-integrity methods. Existing TEST-003-01/02/03/05/06/07 and TEST-001-04/005-03/006-03/05 receive scoped application evidence; related eventual MET-01/04/07/08/09/15. [M2 evidence](execution.md#m2-source-candidate-and-arithmetic-evidence):66 combined methods passed; source case/parser approval, actual parsing, trusted stage integration and registered Fixture execution remain pending. No new core TEST/MET ID or separate loan scenario.

DOCVERIFY-1.0 maps FR-002/003/007/008/019 to SPEC-001/006 and existing TEST-001-04, TEST-006-02/03/05/07; related eventual metrics MET-03/04/07/08/21. `documents.py`, eleven unit methods and one paired integration method are implemented/tested; the explicit runner reports14 synthetic parsed cases/28 executions with zero failures. [Extension evidence](execution.md#document-verification-extension-evidence) separates this from the retained43-method M1 baseline. Actual PDF parsing, complete ContextPacket/graph integration and model-quality/latency/token results remain pending. No whole planned test family is marked complete; DIRECT and optional retrieval adapters remain unimplemented/unmeasured.

Historical Phase5 planning mapping: [M1-01-09](execution.md) links foundation tasks to existing feature contracts/TEST IDs, and its measurement section maps23 core MET definitions. Current scoped M1/M2 evidence above supersedes the original first-implementation-pending note. The [design system](design/design-system.md) retains visual review boundaries. Accepted ADR-007 and PUB-01-06 extend the plan without claiming completed retrieval/public-source test families. All90 planned core TEST IDs and existing synthetic scenario/metric counts remain unchanged.
Sources: [PRD](product/prd.md), [HLD](architecture/hld.md), [spec overview](specs/overview.md), [evaluation plan](evaluation/evaluation-plan.md)

## Functional requirements

CITEVIEW-1.0 maps the user's discoverable-citations requirement to FR-007/009/020 and SPEC-010, with SPEC-005 reference validation, SPEC-009 inline memo links and SPEC-012 static snapshot behavior. Existing TEST-010-03/05/06, TEST-009-05 and TEST-012-04/05 verify inline discoverability, exact versioned targets/context, calculation-input/policy/assessment origins, all/conflicting sources, honest fallback/error states, keyboard/return behavior and zero model/gate side effects. UX-T03/05 and MET-07/08/15/19 retain their existing definitions; no new test ID, metric or scenario is added. Detailed interaction: [citation discovery contract](specs/command-center-ui.md#citation-discovery-and-source-navigation--citeview-10).

Authorized SME fix coverage, 2026-10-23:

| Finding | PRD requirements | Canonical specification / dependent behavior | Existing planned checks | Metrics |
|---|---|---|---|---|
| SME-01 assessment onboarding | FR-001–003/006/015/020 | SPEC-001 prepared complete case packs versus unregistered partial upload; SPEC-004/005 score/recommendation prerequisites | TEST-001-05; TEST-004-10; TEST-010-02; existing core/partial variant | MET-04/09/15/19 |
| SME-02 entity coherence | FR-003/004/007 | SPEC-001 subject/facility registry; SPEC-002/003 trusted input dependency | TEST-002-03; TEST-003-04; E-C03 variant | MET-01/04/08/09 |
| SME-03 critical fact support | FR-003/007/008/010/014 | SPEC-002 FACT-SUPPORT-1.0; SPEC-008 typed FACT/CLAIM assessment; SPEC-007 same-revision continuation; SPEC-011 persistence | TEST-002-07; TEST-005-03/04; TEST-007-02; TEST-008-06; TEST-011-01; E-C03/C04 | MET-04/07/08/09/11 |
| SME-04 conditions | FR-009/010/016/017/020 | SPEC-008 CONDITIONS-1.0; SPEC-005 model condition links; SPEC-009/010 completion labels | TEST-008-03/07; TEST-009-02/03; E-P01/E-M01 | MET-09/10/15/19 |
| SME-05 covenant scope | FR-003–005/007/009 | SPEC-003 extracted/not-evaluated covenant projection; SPEC-005/009/010 no policy-to-covenant clearance | TEST-003-07; TEST-005-03; TEST-010-03 | MET-02/07/09/10 |
| SME-06 EBITDA contract | FR-003/004/007 | SPEC-002 fixed wire; SPEC-003 explicit reported-EBITDA normalization/reconciliation deferment | TEST-002-07; TEST-003-07; wire example | MET-01/05/15 |
| SME-07 analysis horizon | FR-004/006/007/009 | SPEC-003 annual-period scope; SPEC-005/009 no invented full-term/balloon/refinancing finding | TEST-003-07; TEST-005-03; TEST-009-02 | MET-07/10/15 |

All seven are documentation fixes authorized by the user's request to fix the identified issues. These mappings refine existing tests/cases, not new completed evaluations, model calls, metrics or scenario families. The full acceptance details are in the evaluation plan's SME regression table. No actual result is implied.

TEST IDs refer to planned cases in the linked specs. E-* case IDs and MET-* metric definitions are defined in the evaluation plan. Ranges are inclusive. A mapped requirement is not evidence that it passes.

| PRD ID | Required behavior | Feature ownership | Planned tests | Planned evaluation | Metric |
|---|---|---|---|---|---|
| FR-001 | Create scoped deal workspace | [SPEC-001, 010, 011](specs/document-intake.md) | TEST-001-01; TEST-010-01; TEST-011-01 | E-N01; E-A02 | MET-13, 15 |
| FR-002 | Validate/source-version PDFs | [SPEC-001, 006](specs/document-intake.md) | TEST-001-02–06; TEST-006-02–03 | E-T01/T02; E-M04 | MET-04, 08, 11 |
| FR-003 | Extract normalized supported terms and retain corrections | [SPEC-002, 008](specs/extraction.md) | TEST-002-01–07; TEST-008-05/08 | E-N01–N05; E-C01–C03 | MET-03–05, 08 |
| FR-004 | Calculate FIN-1.0 ratios | [SPEC-003](specs/financial-analysis.md) | TEST-003-01–07 | E-F01–F05; E-N01/N02 | MET-01, 04 |
| FR-005 | Apply fictional versioned sample policy and inspect its recorded evaluation | [SPEC-004 / RULEVIEW-1.0](specs/policy-risk.md#read-only-rule-evaluation-details--ruleview-10) | TEST-004-01–03, 06–07, 09; TEST-010-03 | E-P01–P05; E-N05; existing equality/missing/version cases | MET-02, 07–09, 15, 19 |
| FR-006 | Quantify supported risks, educational score/band and summary | [SPEC-004, 005](specs/policy-risk.md) | TEST-004-05/08/10/11; TEST-005-02–03/07 | E-P01–P05; E-F02/F03; focused synthetic score goldens | MET-01, 06, 07, 16, 22 |
| FR-007 | Verify source/calculation references and show uncertainty | [SPEC-002–006, 008](specs/synthesis-evidence.md) | TEST-005-03–04; TEST-006-02–03; TEST-008-06 | E-C01–C04; E-M01–M04 | MET-04, 07–08 |
| FR-008 | Delegate through explicit guarded state | [SPEC-007, 011](specs/orchestration-budgets.md) | TEST-007-01–08; TEST-011-02–04 | E-N01/N04; E-T03/T04 | MET-09, 11, 14 |
| FR-009 | Generate grounded credit review memo | [SPEC-009](specs/credit-memo.md) | TEST-009-01–06 | E-N01/N04; E-P01; E-M01 | MET-07–08, 10 |
| FR-010 | Conditional human review, correction and history | [SPEC-008, 011](specs/human-review-corrections.md) | TEST-008-01–08; TEST-011-03–05 | E-P01/P05; E-A02/A03 | MET-09, 11 |
| FR-011 | Expose actual progress/errors/usage | [SPEC-007, 010, 011](specs/persistence-observability.md) | TEST-007-01, 03, 06; TEST-010-04; TEST-011-05–06 | E-T03/T04; coordination batch | MET-11, 14–15, 17–18 |
| FR-012 | Inspect honest evaluation results | [SPEC-011; evaluation plan](specs/persistence-observability.md) | TEST-011-07; TEST-006-09; core QA and optional extension protocol | Core walkthroughs/variants first; thirty-case and hybrid-retrieval extensions separately | MET-01–23 |
| FR-013 | Shared-graph offline Jupyter notebook | [SPEC-012](specs/jupyter-html.md) | TEST-012-01–03, 06 | Graph-only fresh-kernel protocol | MET-15, 20 |
| FR-014 | Preserve escalation/status/owner/closure integrity | [SPEC-004, 007, 008](specs/policy-risk.md) | TEST-004-02–07; TEST-008-01–06 | E-P01/P05; E-M01–M04; E-A03 | MET-02, 04, 09 |
| FR-015 | Fixture/live separation and later Nebius integration | [SPEC-001, 002, 005–007, 011](specs/orchestration-budgets.md) | TEST-001-05; TEST-005-06; TEST-007-05; TEST-011-06 | Registered packages; later live suite | MET-11–13, 17–18 |
| FR-016 | Pure seven-section report and explicit audit cutoff | [SPEC-009, 011](specs/credit-memo.md) | TEST-009-01–06; TEST-011-05 | E-N01/N04; E-M01 preview | MET-10–11 |
| FR-017 | Five-field PanelDecision and three-panel synthesis | [SPEC-005](specs/synthesis-evidence.md) | TEST-005-01–07 | E-N01–N05; E-P01; E-F03/reject-supported; E-C04; E-T03 | MET-05–07, 09, 16 |
| FR-018 | Amount/confidence plus independent score/mandatory Python routing and guarded same-thread resume | [SPEC-004, 007, 008](specs/human-review-corrections.md) | TEST-004-11; TEST-007-02; TEST-008-01–04, 07 | E-N04/N05; amount/confidence and continuous unrounded score boundaries | MET-09, 11 |
| FR-019 | Working three-core/seven-responsibility pipeline and sample output | [SPEC-007, 009, 011, 012](specs/orchestration-budgets.md) | TEST-007-01, 04; TEST-009-01; TEST-012-02 | Three core walkthroughs plus correction/Reject QA; optional ten-deal batch | MET-10–15, 20 |
| FR-020 | Six-screen command center with evidence/next actions | [SPEC-008–012](specs/command-center-ui.md) | TEST-010-01–07; TEST-008-01–07 | Three walkthroughs; UI checklist | MET-09, 15, 19 |

## Principal engineering fix coverage

Subsequent user-authorized Principal fixes, 2026-10-23, retain the existing coverage inventory:

| Requirement / boundary | Canonical contract | Existing planned verification / metric |
|---|---|---|
| FR-003/008/019 compact prompt/output consistency | Corrected Extractor Runtime prompt; SPEC-002; PRD8.3/8.9 | TEST-002-07, TEST-006-01/04; MET-03/05/11; no notes, Unknown strings, stale hash or archive fallback |
| FR-010/014/018 current review against unchanged analysis | [REVIEW-BASIS-1.0](specs/human-review-corrections.md#analytical-basis-versus-review-progress--review-basis-10) | TEST-008-02/03/04/07, TEST-007-02/08, TEST-006-05; MET-09/10/13; handling progress versus analytical staleness |
| FR-010/020 edited conditions support before disposition | Existing editor, prepare_review_conditions, typed CLAIM support and exact draft consumption in SPEC-008/010 | TEST-008-03/06/07, TEST-010-03/05; MET-07/09/10/19; no target-creation/approval loop or extra inference |
| FR-008/011/015/019 same-workspace execution admission | [EXEC-ADMISSION-1.0](specs/orchestration-budgets.md#shared-execution-admission--exec-admission-10); SPEC-011 operations | TEST-007-05/06/07, TEST-011-02/03/04, TEST-012-01/03; MET-11/14/17/18; one process contender succeeds, Busy rollback, no uncertain claim stealing |
| FR-004/007/010/019 exact persistence/current-state identity | [STATE-CODEC-1.0](specs/persistence-observability.md#exact-checkpoint-and-artifact-representation--state-codec-10); CANON-1.0 | TEST-011-01/03, TEST-003-06, TEST-004-11, TEST-006-05, TEST-007-02; MET-05/09/10/15; exact values/types/fingerprints after restart and noncircular parent hashes |

These are documentary fixes and focused harness requirements, not executed passing tests, a new corpus/metric or permission to scaffold/enable paid work. The original AE-01–07 table below remains the historical engineering-fix map, with current contracts governing implementation.

AE-01–07 were authorized for documentation fixes on 2026-10-23. The [review resolution table](evaluation/ai-engineering-review.md#resolution-status--authorized-fixes-2026-10-23) records current status and remaining implementation prerequisites.

| Finding / linked requirement | Canonical feature contract | Existing planned tests | Existing metric |
|---|---|---|---|
| AE-01; FR-007/017 typed, trusted synthesis | SPEC-005 SYN-WIRE-1.0; SPEC-006 preflight | TEST-005-01–06; TEST-006-04/08 | MET-05/07/08/11/21 |
| AE-02; FR-003/008/015 current fixture/reuse | SPEC-006 CANON-1.0; SPEC-002 | TEST-002-06/07; TEST-006-05; TEST-007-08 | MET-03/05/09/11 |
| AE-03; FR-008/010 safe resume/outcome | SPEC-008 RESUME-1.0; SPEC-007 RUN-OUTCOME-1.0; SPEC-011 | TEST-007-02/06/07; TEST-008-04/07; TEST-011-02–04 | MET-09/10/11/13 |
| AE-04; FR-003/007/020 complete evidence/navigation | SPEC-006 COVERAGE-1.0; SPEC-001 | TEST-001-04; TEST-006-02/03/09; TEST-010-03 | MET-04/07/08/15/23 |
| AE-05; FR-015/017 safe provider acceptance | SPEC-007 PROVIDER-1.0; SPEC-002/005 | TEST-002-06; TEST-005-06; TEST-007-03/05/06 | MET-05/11/12/18 |
| AE-06; FR-008/010/011/016 current artifact integrity | Overview STATE-UPDATE-1.0; SPEC-007/011 | TEST-007-07/08; TEST-011-01/02 | MET-09/10/11 |
| AE-07; FR-012 honest AI versus reviewed quality | Evaluation EVAL-CUTOFF-1.0; SPEC-011 | TEST-011-07; existing E-N01 correction/E-M01/rubric checks | MET-03/04/06–10/13/16 |

No new TEST IDs, metrics, independent scenarios, UI tasks, model calls, paid evaluations or architecture components are required. Historical scope: that design-only update ran no application/model tests. Later executed evidence is recorded in the current implementation status; design changes alone never count as passed tests.

## Source relevance and temporal correctness coverage

The user requires stale/irrelevant details not to become current conclusions. [SOURCEFIT-1.0](specs/context-optimization.md#source-relevance-authority-and-temporal-fit--sourcefit-10) is canonical; the [focused evaluation variants](evaluation/evaluation-plan.md#stale-irrelevant-and-historically-incorrect-evidence-checks) cover uploaded-document failure patterns analogous to the supplied website examples. No website crawler or retail-Q&A scope is added.

| Requirement / need | Feature and planned existing coverage | Existing measures |
|---|---|---|
| FR-003/007 exact field/period/tier/source applicability | SPEC-001/002/003/006 SOURCEFIT-1.0; TEST-002-03/04, TEST-003-04, TEST-006-01/03; E-C01–04 variants | MET-03/04/07/08 |
| FR-005/014 justified policy version and authority | SPEC-004/006; TEST-004-02/07/09; unresolved applicability cannot become Pass or guessed retroactivity | MET-02/04/09 |
| FR-007/008 historical cutoff and no stale reuse | SPEC-006 CANON-1.0/SOURCEFIT-1.0; TEST-001-06, TEST-006-05/09, TEST-008-05; review date/cutoff/profile changes invalidate dependencies even with identical PDFs | MET-04/09/21/23 |
| FR-009/020 inspect selected evidence and alternatives | SPEC-009/010; TEST-010-03/05/06 and UX-T03/05; existing seven-section memo shows selected basis/source and historical/current distinction | MET-07/08/10/15/19 |

Retain90 planned TEST IDs,30 independent scenario designs,23 metric IDs and five UX tasks. Keep no automatic expiry, DIRECT grounding, unchanged chunk/overlap settings and two normal model calls. Reviewed dates/authority profiles and all runtime validation remain pending; no universal source hierarchy or document-recency business rule is invented.

## Authorized Director-fix coverage

The user authorized fixes to the reviewed recommendations. These are current specification changes, not runtime results or authorization for later phases.

| Requirement / finding | Canonical contract | Existing planned checks | Existing measures |
|---|---|---|---|
| FR-007/009/017; support for every narrative field | [NARRATIVE-CHECK-1.0](specs/synthesis-evidence.md#evidence-targets-for-every-narrative-field--narrative-check-10) | TEST-005-03/04/05; TEST-008-06/07; TEST-009-02/05; TEST-011-01/07 | MET-05/07/08/10/16; original versus human-edited targets remain separate |
| FR-003/008/015/017; strict unambiguous bounded input | [INPUT-EDU-1.0](specs/overview.md#strict-external-input-limits--input-edu-10) | TEST-002-04/07; TEST-003-02/03/06; TEST-005-01/06; TEST-006-04/05; TEST-007-03/06 | MET-01/05/09/11/18; technical limits are not lending thresholds |
| FR-007/010/014/020; source repair owner/action/counts | [SOURCE-TRIAGE-1.0](specs/human-review-corrections.md#source-issue-ownership-and-permitted-repair--source-triage-10) | TEST-008-01/03/05/06; TEST-010-03/05/06 | MET-04/09/15/19; assignment cannot clear unknown authority or another gate |
| FR-008/010/011/015; bounded continuation and safe stop | [CONTINUE-CHECK-1.0](specs/orchestration-budgets.md#bounded-continuation-feasibility--continue-check-10) | TEST-007-02/03/06/08; TEST-006-08; TEST-008-04/07 | MET-09/11/13/18/21; actual node counts and provider cost are distinct |

The [focused evaluation table](evaluation/evaluation-plan.md#authorized-director-fixes-and-focused-acceptance) supplies failure/boundary examples within90 existing TEST IDs and30 case designs. No additional metric, UI task/screen, model wire field/call or production infrastructure. Phase 4 repository approval, Phase 5 execution/design-system planning and first implementation approval remain pending; runtime compatibility/token-fit/quality checks remain Not run.

## User-authorized RAGAS evaluation coverage

NATIVE-REPORT-1.0 and the [evaluation report template](evaluation/evaluation-report-template.md) extend FR-012 with four visible native rows: Faithfulness, Response Relevancy, Context Precision and Context Recall. Existing TEST-011-07/TEST-010-04 verify exact variants/scales, null versus measured zero, DIRECT ranked precision Not applicable, missing-reference status, valid negative cosine relevance and no fabricated overall score. Native requests/embeddings remain separately planned/accounted under existing offline permission/usage tests; report reads make no calls. These native families are separate from RAG-R01–05 and do not add core MET definitions or release thresholds.

[RAGAS-EVAL-1.0](evaluation/ragas-evaluation.md) and the [offline role prompt](agents/ragas-evaluator.md) add five custom rubric dimensions, distinct from the23 existing core MET definitions and MET-16 human rubric. They extend FR-007/012/020 and HHH diagnostic evidence without another application call, runtime judge or screen. No RAGAS package/scorer/results have executed.

| New dimension | Intended evidence | Existing planned checks / related measures |
|---|---|---|
| RAG-R01 Faithfulness1–5 | Original response assertions versus exact actual generation context; explanation and traceable examples | TEST-005-03, TEST-006-01/05, TEST-011-07; related MET-07, not an identical/native score |
| RAG-R02 Context Relevance1–5 | Task-relevant evidence, omissions and noise, preserving required qualifiers/conflicts | TEST-006-01/09, TEST-011-07; related MET-23; native definitions remain separate |
| RAG-R03 Answer Completeness1–5 | Supported task aspects/next action/appropriate abstention versus separate evaluator reference | TEST-011-07; related MET-04/13/16; original/human subjects stay distinct |
| RAG-R04 Source Attribution1–5 | Material claim origins and resolvable supporting scoped locators, with examples | TEST-011-01/07, TEST-005-03; related MET-07/08; score cannot replace source validation |
| RAG-R05 Response Coherence1–5 | Clear logical structure/readability and explicit findings/uncertainty/action | TEST-011-07, TEST-010-04/06; related MET-16/19, not substituted for those rubrics |

Use TEST-007-03/05/06 and TEST-011-06 for explicit mode/lazy imports, single shared routine bundle/call accounting, separate approved evaluator allowance, usage uncertainty and privacy. No outbound RAGAS call from normal graph/UI/Fixture/notebook paths. Preserve90 TEST IDs/30 case designs; manual baseline/controlled adapter/actual package execution have different labels, native results retain their exact declared scales and remain separate and critical gates are never averaged away. Paid execution, package/adapter compatibility and score calibration remain pending.

## Nonfunctional and AI-specific controls

| PRD source | Feature/specification | Planned verification | Metric |
|---|---|---|---|
| NFR-001 latency; NFR-015 time/tools | SPEC-007/011; evaluation timing protocol | TEST-007-03/06; separately funded >=30 completed timing runs | MET-11, 17 |
| NFR-002 best-effort demo availability | SPEC-007/011 | TEST-007-05/06; TEST-011-03/04; visible recovery limits, no SLA | MET-13, 15 plus failure counts |
| NFR-003 reproducibility | SPEC-003/004/009/011 | TEST-003-01; TEST-004-01; TEST-009-04; versioned fixtures | MET-01–02, 10 |
| NFR-004 accepted schema validity | SPEC-002/005/006 | TEST-002-04; TEST-005-01; strict output validation | MET-05 plus raw invalid rate |
| NFR-005 recorded decisions | SPEC-008/009/011 | TEST-008-04/07; TEST-011-05; explicit records and cutoff | MET-09–10 |
| NFR-006 zero unauthorized external writes | SPEC-005–008/011/012 | TEST-002-05; TEST-007-05; TEST-009-06; TEST-012-06 | MET-09, 11, 15 |
| NFR-007/008 node/retry limits | SPEC-007 | TEST-007-03/06; nested work/retry accounting | MET-11 |
| NFR-009 cost; NFR-013/014 tokens/attempts | SPEC-006/007/011 | TEST-006-04/06/08; TEST-007-03/06/08; usage reconciliation | MET-11, 18, 21 |
| NFR-010 package limits | SPEC-001 | TEST-001-02/03; E-T01/T02 | MET-04, 11 |
| NFR-011 scoped deal access | SPEC-001/008/011 | TEST-001-04; TEST-008-04; TEST-011-01/02; role simulation limits | MET-09 |
| NFR-012 error transparency | SPEC-007/010/011 | TEST-007-07; TEST-010-06; explicit stop/next action | MET-13, 15, 19 |
| NFR-016 escalation integrity | SPEC-004/007/008 | TEST-004-04/06; TEST-007-02; TEST-008-01–07 | MET-02, 04, 09 |
| PRD 7 grounding/approved sources/citations | SPEC-001–006/009 | TEST-001-04; TEST-005-03/04; TEST-006-02/03; TEST-009-05 | MET-07–08 |
| PRD 7.6 document-specific segmentation, direct-grounding boundary | [SEG-1.0](specs/context-optimization.md#document-specific-segmentation-and-overlap--seg-10), SPEC-001/006 | Existing TEST-001-04 and TEST-006-02/03 cover four content profiles, source spans, qualifications, duplicate-row prevention and context overflow | MET-04,07–08,11; targets unmeasured, no added model calls or vector retrieval |
| PRD 7.6 optional retrieval benchmark and conditional reranker decision | [RET-1.0](specs/context-optimization.md#shared-evidence-selection-interface-and-optional-benchmark--ret-10); [benchmark sequence/status/report gate](evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision) | Planned TEST-006-09; sources ready before ten-query DIRECT/KEYWORD/VECTOR/HYBRID comparison; VECTOR semantic baseline; RRF fusion; inspect ranking failures and added work before separately selected reranker; app default unchanged | MET-23; per-query counts/ranks/coverage/work and specified/implemented/tested/measured status; no automatic download/spend, new metric/test ID or assumed uplift |
| PRD 8 bounded role prompts | SPEC-002/005/006 | TEST-006-01/06; no whole-pack prompt or extra judge | MET-05, 11, 21 |
| PRD 9 unknown/refusal/escalation behavior | SPEC-002/004/005/008 | E-M01–M04; E-C01–C04; E-A01/A03 | MET-04, 07, 09 |
| PRD 5/6 privacy/tool permissions | SPEC-001/006–008/011/012 | TEST-006-01; TEST-008-01/06; TEST-011-06/08; TEST-012-06 | MET-09, 11, 15 |
| PRD 6 memory/checkpoints/retention | SPEC-008/011 | TEST-011-03–05/08; confirmed P3-04 no automatic expiry, including time-advance/SQLite-restart checks | MET-09–10, 15 |
| PRD 3/11 educational outcomes and HHH | SPEC-010/012; evaluation rubric | Three walkthroughs, usability/learning checks, factual/support controls | MET-13, 15–16, 19–20 |

## Feature-inventory scope

P0 F-001–012 and F-017–023 are covered by the functional rows above. F-013 general cross-document conflict discovery is deferred, while P0 explicit critical field conflicts/contradictory evidence remain required by FR-003/007/014. F-014 semantic policy RAG and F-015 downloadable packages remain P1; F-016 external integrations remains P2. No tests falsely claim these deferred features implemented.

HTML is a required educational presentation artifact under PRD required deliverables and SPEC-012, not a new financial-service feature. Runtime source inspection and Markdown report display remain P0.

## UI acceptance map

All screen criteria remain exactly those in PRD section 4.3, not renamed. The following rows link each criterion to planned tests and metrics.

| UI criterion | Planned feature/test | Metric |
|---|---|---|
| UI-DASH-01 | [SPEC-010](specs/command-center-ui.md), TEST-010-01 | MET-15, 19 |
| UI-DASH-02 | [SPEC-010](specs/command-center-ui.md), TEST-010-01 | MET-15, 19 |
| UI-DASH-03 | [SPEC-010](specs/command-center-ui.md), TEST-010-01 | MET-15, 19 |
| UI-DASH-04 | [SPEC-010](specs/command-center-ui.md), TEST-010-01 | MET-15, 19 |
| UI-NEW-01 | [SPEC-010](specs/command-center-ui.md), TEST-010-02 | MET-15, 19 |
| UI-NEW-02 | [SPEC-010](specs/command-center-ui.md), TEST-010-02 | MET-15, 19 |
| UI-NEW-03 | [SPEC-010](specs/command-center-ui.md), TEST-010-02 | MET-15, 19 |
| UI-NEW-04 | [SPEC-010](specs/command-center-ui.md), TEST-010-02 | MET-15, 19 |
| UI-NEW-05 | [SPEC-010](specs/command-center-ui.md), TEST-010-02 | MET-15, 19 |
| UI-WORK-01 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-WORK-02 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-WORK-03 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-WORK-04 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-WORK-05 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-WORK-06 | [SPEC-010](specs/command-center-ui.md), TEST-010-03 | MET-15, 19 |
| UI-ACT-01 | [SPEC-010](specs/command-center-ui.md), TEST-010-04 | MET-15, 19 |
| UI-ACT-02 | [SPEC-010](specs/command-center-ui.md), TEST-010-04 | MET-15, 19 |
| UI-ACT-03 | [SPEC-010](specs/command-center-ui.md), TEST-010-04 | MET-15, 19 |
| UI-ACT-04 | [SPEC-010](specs/command-center-ui.md), TEST-010-04 | MET-15, 19 |
| UI-ACT-05 | [SPEC-010](specs/command-center-ui.md), TEST-010-04 | MET-15, 19 |
| UI-MEMO-01 | [SPEC-010](specs/command-center-ui.md), TEST-010-05 | MET-15, 19 |
| UI-MEMO-02 | [SPEC-010](specs/command-center-ui.md), TEST-010-05 | MET-15, 19 |
| UI-MEMO-03 | [SPEC-010](specs/command-center-ui.md), TEST-010-05 | MET-15, 19 |
| UI-MEMO-04 | [SPEC-010](specs/command-center-ui.md), TEST-010-05 | MET-15, 19 |
| UI-MEMO-05 | [SPEC-010](specs/command-center-ui.md), TEST-010-05 | MET-15, 19 |

## Implementation prerequisite coverage

The user-authorized [PREREQ-01–08 checklist](specs/overview.md#implementation-prerequisites-and-required-evidence) is the single status/dependency/evidence source. These are readiness IDs, not new application requirements, MET definitions, TEST IDs or automatic acceptance results. Existing90 planned test IDs,30 case designs,23 core metrics,25 UI criteria and five UX tasks remain unchanged.

| Prerequisite | Existing contract / verification coverage | Existing outcome evidence |
|---|---|---|
| PREREQ-01 approvals | Repository proposal, AGENTS draft, current PRD/HLD/specs; later gated execution/design-system plan | Explicit content-bound approval references; no runtime test substitute |
| PREREQ-02 local foundation | SPEC-007/008/011; TEST-011-01/02/03/04, TEST-007-02/05/06/07, TEST-006-05 | Exact restart/identity, unique admission, safe recovery; MET-09/14/17/18 as applicable |
| PREREQ-03 prompt/context contracts | SPEC-002/005/006 and wire examples; TEST-002-07, TEST-005-01/03/06, TEST-006-01/03/04/05/08 | Actual wire/context/reference/coverage checks, local size versus later verified token accounting; MET-05/07/08/11/21 |
| PREREQ-04 reviewed synthetic packs | SPEC-001–004/006; TEST-001-02/03/04/05/06, TEST-002-03/04/07, TEST-004-10/11; existing scenario designs | Authored source/config/fixture/gold separation and reviewed arithmetic/provenance; MET-03/04/05/07/08 as actually evaluated |
| PREREQ-05 core pipeline | Existing E-N01/E-P01/E-M01 and correction/E-F03 variants; TEST-007/008/009/011 families | Actual graph/handoff/report/review evidence, original-versus-corrected outcomes and offline risk QA; MET-06/09/10/11/13/22 |
| PREREQ-06 user-facing artifacts | SPEC-009/010/012; TEST-010-01–07, TEST-012-01–06, TEST-009-05, UX-T01–05 | Real source navigation, usable task completion and shared graph/offline lineage; MET-15/19/20 |
| PREREQ-07 Nebius | SPEC-006/007/011; PROVIDER-1.0; TEST-007-03/05/06 and Live protocol | Explicit access/allowance/profile/token/cost proof and actual synthetic end-to-end output; no fixture-as-model or single-run-general-quality claim |
| PREREQ-08 selected extensions | RET-1.0, RAGAS-EVAL-1.0/NATIVE-REPORT-1.0; TEST-006-09, TEST-011-07, TEST-007-05/06/07 | Separately labeled actual native/custom/retrieval results and usage; MET-23 plus distinct RAG-R/native dimensions where selected |

The evaluation plan owns the actual evidence record; the later approved execution plan will map small tasks/files to these prerequisites. All current runtime results remain Not run, with optional execution planned/disabled rather than silently treated as a failed core gate.

## Change and approval discipline

RISK-EDU-1.0/SCORE-BANDS-1.0/SCORE-ROUTING-1.0/SCOREVIEW-1.0 map the user's confirmed risk requirements to FR-006/009/018/020 and UI-WORK-02. Planned TEST-004-10 covers exact weighted aggregation/material provenance/no reweighting; TEST-004-11 covers unrounded continuous band boundaries, independent counts and score referrals. Existing TEST-007-02, TEST-008-01–04/07 and TEST-010-03/05/06 cover routing, permissions/tier/handling, stale review, three cards and actual required action versus accepted current AI proposal. SPEC-005 tests preserve exact five-field PanelDecision and validate optional proposal/reference lineage. MET-01/05/09/10/15/19 cover arithmetic/data/display/control integrity, not statistical prediction. Supplied ratings60/40/30/20/50 yield41 Moderate; Moderate always human, High Credit Risk Manager then package review, Very High senior-tier review. Missing material inputs yield Insufficient Data and pause dependent synthesis/readiness. Low never clears independent gates. No new metric, loan-case count, generation stage or automatic approval/rejection threshold. Factor-rating generation and PD/expected loss remain outside scope. TEST-004-11 adds one planned test identifier; static document coverage is not executed application QA.

RULEVIEW-1.0 maps FR-005/007/014/020 and existing UI-WORK-01/03 to exact condition/input/source/formula/version inspection with distinct outcome/workflow meaning. TEST-004-09 checks trace/source integrity and no read-side execution/mutation; TEST-010-03 covers compact policy-row detail and return context, UX-T03 the operator's explanation, and TEST-012-04 the static walkthrough example. All are planned; sample attachment ACCEPT/REROUTE/risk-score/Plaid values create no project rules or integrations. Rule validation here means reviewable recorded evidence, not policy editing, legal clearance or a new approval flag.

UX-1.0 presentation fixes are authorized by the user's2026-10-23 issue-fix request. Existing25 UI IDs and TEST-010-01–07 remain authoritative: Dashboard five-column defaults (01), three-step readiness/intake (02), Workspace overview/actions/evidence/correction impact (03), progressive Activity detail (04), separate memo recommendation/review/report (05), focus/keyboard/narrow-layout and shared selection (06), and UX-T01–05 operator walkthrough (07). SPEC-008 TEST-008-05 and SPEC-007 TEST-007-08 cover zero-dispatch Save and explicit continuation; TEST-009-03 retains seven-section output/separate UI summary; TEST-012-04 applies hierarchy to static HTML without fake processing. Map usability outcomes to MET-19 and learning to MET-20; all remain Not run. This adds no new test family, UI screen or model call.

Every implemented change must identify a PRD requirement, feature and planned test/evaluation. A changed formula, authority/capability, schema, prompt, provider configuration or threshold must update the relevant spec/gold labels/traceability before acceptance. No claim of test coverage follows from this table.

Phase 3 approval on 2026-10-22 accepted P3-01–09. Provider/rates/live allowance, dependency compatibility/licensing and actual fixture authoring remain later explicit checkpoints. The [Phase 4 repository proposal](architecture/repository-design.md) is next; no immediate application scaffolding.

## Authorized review-fix coverage

Static audit result for this retrieval update:17 relevant documents all reference the canonical decision;51 active Markdown files checked,566 local links and136 section references valid, four illustrative JSON blocks parsed, no broken targets. Application/test source hashes match the last M1 evidence and both model Runtime prompt hashes match trusted configuration. The90 planned TEST IDs and23 core MET IDs are unchanged. No retrieval implementation or benchmark execution occurred during this documentation audit; application tests were not rerun for these prose-only changes.

Retrieval documentation audit, 2026-10-23: PRD7.6, HLD, SPEC-006, execution M7-03, the canonical benchmark and evaluation plan carry the approved source-ready/four-baseline/conditional-reranker sequence. Supporting repository/overview guidance, active root AGENTS.md and its inactive draft, agent catalog/evaluation instructions, RAGAS protocol/report linkage, project README and engineering-review scope are now aligned. All point to the [single decision/status/report source](evaluation/hybrid-retrieval-benchmark.md#implementation-order-and-conditional-reranker-decision). VECTOR is the semantic retrieval baseline, RRF is fusion, and separately selected reranking needs measured ranking-error/processing evidence. Existing TEST-006-09/MET-23 own future verification; no new ID, metric, model or UI is added. Source/test code and actual model Runtime prompts are unchanged; the43 prior M1 methods do not establish retrieval quality. Historical archives remain untouched.

Product Designer integration, 2026-10-23: PRD section4.3 now states CX-1.0 behavior within the actual screen requirements rather than relying only on its opening change note. Existing UI-DASH-04, UI-NEW-05, UI-WORK-04, UI-ACT-02 and UI-MEMO-02 explicitly cover sample preparation, complete/partial scope, retained work/local handoff, saved/pending recovery and the final recap. Cross-screen checks add consistent explicit human disposition with no preselected outcome, distinct edit/processing cancellation and readable historical artifacts while stale mutation remains blocked. Existing TEST-010-02/03/04/05/06/07, TEST-009-03 and TEST-012-04/05 plus UX-T01–05/MET-19 remain the planned coverage; no IDs, gates, banking rules or model requests are added. Visual tokens and all rendered/runtime results remain pending.

Customer-experience fixes, 2026-10-23: [CX-1.0](specs/command-center-ui.md#first-use-review-effort-and-completion-experience--cx-10) links FR-002/007/009/010/011/020 to sample/readiness/help, scoped evidence checks, local handoffs, saved/pending recovery and the final recap. Existing TEST-010-02–07, TEST-009-03, TEST-012-04/05 and UX-T01–05 verify those behaviors with zero new inference. MET-19 retains its definition/target; click/role-change/repeated-evidence observations are descriptive manual task fields, not new core metrics or telemetry. Optional unfamiliar-person feedback is separate from author self-assessment. SPEC-009 and SPEC-012 keep memo and static-walkthrough semantics aligned. Phase 5 visual consolidation and actual usability evidence remain pending; no phase gate is advanced.

These documentary fixes are authorized by the user's request to fix the review findings; repository and first-implementation gates remain pending.

| Requirement / need | Contract and planned verification | Metric / scope |
|---|---|---|
| FR-003 strict Fact/wire typing | [Complete wire example](specs/examples/extraction-wire.md), TEST-002-07 | MET-03–05; core |
| FR-003/010 source-backed correction, genuine missing-data pause | [E-N01 correction](evaluation/examples/e-n01-correction.md), TEST-008-08 | MET-04,09; E-M01 cannot be completed with an unsupported number |
| FR-008/010 revision/thread continuation and shared allowance | TEST-007-08; TEST-006-08 | MET-09,11,18; analytical new thread vs review-only same thread |
| FR-006/012 QA-RISK-FP-01 | TEST-004-08; high-level offline expected-finding comparison | MET-06 plus MET-22 false-positive count; no UI visibility or detailed scoring requirement |
| FR-006/009/017 supported Reject QA-REJECT-01 | [E-F03 variant](evaluation/examples/e-f03-reject.md), TEST-005-07; existing review/report tests | MET-05–10,13; credit Reject differs from absent information/technical stop |
| Five-day educational feasibility | Core walkthroughs/variants and critical controls; first-milestone compatibility/token check | MET-13/19/20; broader thirty-case, batch, timing and multi-person studies optional |

All additional TEST IDs are planned acceptance cases, not implemented/passing tests. No new universal lending rule, additional model stage, paid run, automatic expiry or real financial action is introduced.
# Dashboard presentation refinement — 2026-10-24

Screen 1 attention/grounding requirements → `design/dashboard-redesign.md` and
`specs/command-center-ui.md` → `test_dashboard_filters_and_citation_navigation_are_read_only`,
`test_dashboard_low_score_does_not_hide_mandatory_human_review`, existing run-grouping
and connected financial review tests → distinct-deal count accuracy, permission/gate
visibility, source navigation and zero read-triggered executions. Actual results and
UI limitations: `design/dashboard-implementation-review.md`.


## Live integration traceability

FR-015 / extraction / orchestration / evidence / human review / memo requirements -> specs/live-graph-integration.md -> tests/integration/test_live_graph.py. Checks cover checkpoint pause/resume, exact source/target/domain support, critical missing-data abstention, independent confidence review, no provider fallback, retained unknown allowance and explicit UI support without dispatch. These are mocked-provider integration checks, not model-quality acceptance scores.
