# Conditional Human Review, Issue Handling and Corrections

**Uploaded candidate support:** [UPLOAD-FACT-1.0](upload-fact-review.md) persists
RiskManager data-quality assessments against exact current manually proposed inputs.
All seven checks and reason are required for HUMAN_SUPPORTED. Unsupported/Withheld
block the dependent preview. New proposal invalidates support; old events remain.
This is not financial disposition, exception handling or authenticated authority.

**Implemented extraction-miss correction:** [CORRECTION-1.0](source-correction-integration.md)
uses the existing E-N01 example. Analyst Save restores only registered CFADS from
original source, supersedes the terminal information wait and creates READY revision2.
Explicit Update recomputes affected outputs with the same ledger. Original extraction
and event remain recorded. This slice has no pending human request to stale; extension
to completed/interrupted reviews remains unsupported, never an old-thread resume.

**Current E-P01:** [CONDITIONAL-1.0](conditional-integration.md) connects existing
helpers to actual paused graph and persisted actions. RiskManager handling,
AuthorizedApprover preparation, RiskManager FINANCIAL_RISK and ComplianceOfficer
POLICY_CONTROL support are separate gates. Final Conditional Approve/Reject binds
that exact draft. Only the registered annual-statements condition is supported;
no arbitrary edits, repayment cure, fulfilment or new-document continuation.

**Current implementation:** [FIN-REVIEW-1.0 / FIN-REASSESS-1.0](financial-review-integration.md)
now connects financial E-N01/review to persisted requests, role-aware comments,
Approve/Reject receipts, actual interrupt/resume, report/history and bounded
registered-evidence reassessment. The illustrative preview remains isolated.
Conditional editing, generic/new-fact uploads, specialty exception cases and
verified automatic technical recovery remain pending; this note does not complete
every contract below. Unknown resume gaps stop with retained decisions.

Feature ID: SPEC-008
Version: 1.7
Status: Bounded saved financial interrupt/resume, role-aware decisions, conditions and source-backed correction implemented; live evidence checkpoints integrated; actual live completion pending
PRD requirements: FR-003, FR-007–010, FR-014, FR-018–020
Role instructions: [Human Review](../agents/human-review.md), [Shared contract](../agents/shared-contract.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

Decision History extension2026-10-24: [SPEC-013](decision-history.md) adds a dedicated sixth read-only page and CSV export. New review events include the original pre-action status, trusted simulated reviewer display name and DECISION-SNAPSHOT-1.0 context; this does not expand final-decision permissions or connect preview records to financial HITL. Prior review events are not rewritten.

### Role-aware review comments and actions — REVIEW-UI-1.0

Authorized by the user on 2026-10-24. Add an existing-screen Human review panel for individual deals, not another screen or financial authority. Required actions are Add comment, Approve, Reject and Request Additional Information (Pending). Preserve Conditional Approve and its existing supported-condition contract; it is not removed or implemented as a generic approval shortcut by this slice.

| Action | Permitted simulated roles | Additional requirements |
|---|---|---|
| Read review/history | All five existing roles | Same workspace and allowed deal |
| Add comment | Analyst, RiskManager, ComplianceOfficer, AuthorizedApprover | Required nonblank comment; current record version; metadata only |
| Request Additional Information (Pending) | Analyst, RiskManager, ComplianceOfficer, AuthorizedApprover | Required comment and 1–20 explicit requested items; current pending review; no disposition or gate clearance |
| Approve / Reject | AuthorizedApprover only | Required comment; current pending review/basis/version; required NORMAL/SENIOR tier; every prerequisite satisfied; no outstanding additional-information request; existing accept_review guard |
| Administrator actions | Read only in this panel | No credit/comment/request permission is inferred from administration |

Request Additional Information records status NEEDS_INFORMATION, displayed Pending — additional information requested. It is not a fourth PanelDecision literal, credit rejection, or a LangGraph resume. Preserve the pending package request and independent blockers. A subsequent Approve/Reject remains unavailable until the existing source/support/correction flow actually resolves and revalidates information prerequisites; neither notes nor role switching resolve them. The bounded preview has no information-clearance/reset action. Additional requests can be recorded without losing earlier requests.

Every submitted action requires a comment (1–4096 characters after nonblank validation). Request items are nonblank, distinct, at most512 characters each. Record application-generated UTC time, stable simulated reviewer ID/role, action, resulting decision status, request/deal/thread/revision/basis IDs, expected record version, operation ID and requested items when applicable. Human review records stay separate from the original AI recommendation and report completion. Comments after a recorded decision may append history without changing its decision. A new/changed final decision is denied once recorded; corrections follow the existing revision workflow.

Use existing SQLite app_records/history in the same configured file; no new database/schema, automatic expiry or editable/deletable history. Validate scope, role, state, tiers, input/basis/version and prerequisites on the service side inside the serialized transaction. Duplicate identical operation IDs return the original event/timestamp; changed payload reuse conflicts. Denied actions write no comments/decisions/events. Ordinary diagnostics exclude comment text. Render submitted comments/items as inert text, never HTML or executable Markdown.

Implementation boundary: build a reusable Streamlit human-review component and an explicitly labeled ILLUSTRATIVE_UI_ONLY local preview before the five-screen shell/actual interrupt adapter exist. Preview requests contain no loan analysis, risk grades, real identity, claimed human-supported evidence or fabricated graph checkpoint. Creating the fixed UI examples requires an intentional Prepare UI review samples action; merely opening/importing/refreshing the panel writes no records. All examples use isolated ui-review record keys in the same SQLite database; no original E-N01 artifacts are modified or registered. Approve/Reject in this preview record only simulated UI outcomes, with graph_progress=NOT_CONNECTED and report status Not generated by this preview. The complete five-screen app, actual pending-request registration and RESUME-1.0 worker integration remain pending and must not consume preview records. This is a concrete reviewable UI feature, not a claim of completing the financial HITL workflow.

Tests extend TEST-008-01/03/06/07, TEST-010-03/05/06 and TEST-011-01/02/06: all roles, both tiers, wrong deal/workspace, missing comments/items, stale versions/bases, unresolved blockers, final versus information state, retained comments/history, duplicate exact timestamps, operation conflicts/transaction rollback, inert rendering, draft retention and zero provider/graph work. Use Streamlit AppTest plus application tests; manual browser/accessibility verification remains separately reported.

A simulated owner investigates an issue, records permitted handling and a current-revision review disposition, while preserving evidence and the original model recommendation. No real identity, committee authority, loan approval, screening clearance, notice, notification or financial commitment.

## Workflow and rules

Python computes requested amount >=USD10M OR confidence <0.7 plus active mandatory referrals. An unresolved required source/control blocks affected completion; a numerical exception with supported panels may reach pending review. Each referral retains its final-review requirement even after separate exception handling. A satisfied current ReviewRequest allows reporting after resume; do not repeatedly route an already-recorded review because the original threshold remains true.

SCORE-ROUTING-1.0 is now an independent mandatory referral source. Moderate requires NORMAL Authorized Approver review, High requires recorded credit-risk handling by Credit Risk Manager (existing RiskManager persona) then package review, and VeryHigh requires the existing AuthorizedApprover in SENIOR review tier. No sixth persona or verified bank authority is implied. Score referrals never clear policy exceptions/missing evidence; material scoring gaps show Insufficient Data and pause dependent conclusions. ReviewRequest carries required owner categories/tier/score refs and all unmet gates; data-blocked cases cannot be approved because an AI proposal or another issue owner suggested referral.

Human node interrupts with pending_review_id, thread/deal/run/revision, original PanelDecision, panels, evidence, owners, gates and permitted actions. Keep provider work upstream. Validate command before resume AND inside the resumed service against latest state. Interrupted-node preamble may repeat; writes are operation-idempotent.

## Review acceptance and graph resumption — RESUME-1.0

AE-03 fixes transaction ordering within the existing one-process/SQLite design. A recorded human decision and a finished graph are separate outcomes. resume_review returns an accepted-disposition receipt with graph_progress PENDING/PAUSED/FINISHED/RECOVERY_REQUIRED, never an unconditional completion claim.

1. Before any graph invocation, the command service acquires the existing serialized mutation guard, validates operation identity/digest, workspace/deal/revision/thread, expected record version, pending request, simulated capability/tier, original artifacts, conditions and all current gates. An identical committed operation returns its receipt without scheduling another task; changed payload is OPERATION_CONFLICT. Another operation cannot replace an already accepted disposition.
2. In one short application transaction, reserve the operation intent and EXEC-ADMISSION-1.0 claim, persist the validated HumanDisposition/ConditionRecords, mark that request RECORDED, append disposition_recorded once and commit its accepted receipt with graph_progress=PENDING. Bind the receipt to exact pending request, actor, REVIEW-BASIS-1.0 analytical_basis_digest and accepted review-gate snapshot/version, and operation ID. Busy or validation/storage failure rolls back these changes; it cannot record a disposition that the same transaction failed to admit. No provider call, long transaction or checkpointer write occurs here.
3. After commit, schedule the one worker with Command(resume=validated_receipt_payload) on the exact paused thread; the payload contains operation_id, receipt_id, pending_review_id and disposition_digest. Trusted worker configuration resolves the receipt; submitted text cannot substitute new facts or approval. Reserve/count actual resumed node work within the original ledger. The node's pre-interrupt prelude is read-only/idempotent: rebuild the stored JSON-serializable review payload and call the same interrupt at the same position. It must not demand PENDING after this operation already recorded RECORDED, perform provider/report side effects before interrupt, or catch the framework interrupt in a broad exception handler.
4. After interrupt returns its resume value, the service revalidates identity, receipt/disposition digest, current analytical basis and review gates under REVIEW-BASIS-1.0. The normal PENDING guard has exactly one exception: the same committed operation/receipt may consume its own matching RECORDED request. The accepted gate snapshot must remain satisfied; an acknowledgement or missing/retracted support cannot substitute for it. Reuse the existing disposition without inserting another or accepting a changed payload. Other recorded, stale, superseded, wrong-thread or analytically changed requests fail. Analyst corrections use the separate new-run path and never this exception.
5. The report node independently rechecks current prerequisites, writes its report/event once under a stable operation identity, and returns state. After graph/checkpoint reconciliation, update graph_progress and lifecycle from the actual outcome. Keep accepted human attribution/history even if completion stops; an accepted receipt alone cannot clear an unresolved gate or establish COMPLETED.

Crash handling stays explicit and local. Before the transaction commit there is no accepted disposition; an intentional identical retry may validate anew. After commit but before graph consumption, expose Recovery required; an explicit retry/recovery of the same operation may schedule its saved Command only after confirming the original current pending checkpoint and unchanged dependencies. After node/report commit but before checkpoint, reuse those verified receipts/artifacts on re-entry. If the checkpoint already contains the result, reconcile rather than invoke again. Checkpointer and application commits are separate; unknown or inconsistent progress stops for investigation, without inserting a new disposition, re-running a model, resetting allowance or automatically replaying after restart. A receipt read itself is always read-only; recovery is a distinct explicit service action using the original operation identity.

Existing TEST-008-04/07, TEST-007-02/06/07 and TEST-011-02–04 cover these commit gaps, self-replay versus a competing command, changed conditions/dependencies and zero approval-only inference. Exact pinned interrupt/checkpointer APIs remain a compatibility prerequisite, not an invented shared transaction.

## Analytical basis versus review progress — REVIEW-BASIS-1.0

The user authorized the Principal review fixes. Distinguish the immutable basis being reviewed from permitted progress in reviewing it. Use existing request/issue/disposition records; do not add another graph, model call or lending rule.

analytical_basis_digest binds CANON-1.0's current source/fact/subject/period/ReviewSourceBasis/profile/policy/formula/factor/method dependencies, relevant prerequisite fact/narrative-support lineage for accepted analysis, accepted original panel/synthesis content and instruction/schema/config versions. It excludes display formatting, local owner/notes, progress-only exception/High-score handling records and support of the separate human-condition draft. Preserve the exact original issue finding/predicate/evidence as analytical content; handling does not turn Exception into Pass. Relevant semantic support that changes trusted analytical use still follows SPEC-007's support-continuation/invalidation rules; this exception is not permission to reuse retracted or changed support. Draft-condition support instead binds the separate gate snapshot below.

review_gate_version and review_gate_snapshot_digest are separate application-owned request fields. They bind the current prerequisite IDs, original issue/score/analysis refs, required role/tier, accepted specialist handling/support receipts, and the exact proposed human conditions/links/required support being submitted. The positive gate version advances once per committed relevant handling/draft/support mutation; idempotent repeats and reads never increment it, and unrelated owner/notes do not satisfy or change gate requirements. The snapshot excludes the pending package disposition's own PENDING -> RECORDED consumption: prerequisites must be satisfied before acceptance, while that package-review requirement is satisfied by the accepted command/receipt itself. They do not replace analytical_basis_digest or confer authority. Refresh the read projection from current records; do not compare a frozen list of OPEN gates as though every later permitted handling were an analytical change.

| Change while review is pending | Required behavior |
|---|---|
| Source, fact, applicable basis/profile/policy/method/factor or relevant prerequisite support changes | Invalidate affected analysis and old pending review under existing rules; no old disposition/approval rebinding. Use the existing new-run continuation where required |
| Risk Manager records current permitted numerical-exception or High-score handling against unchanged analysis | Advance that gate's current version/projection, retain the original exception/referral and final package-review requirement. Keep the same pending request/thread; no extraction/synthesis rerun. Old expected gate versions must refresh before submission |
| Notes, owner assignment, acknowledgement or intentional persona selection | Metadata only; no satisfied gate, analytical change or inference |
| Condition text/links change, or required condition support is absent/retracted | The old condition snapshot is unusable. Validate the exact current targets/links and all required domain checks before accepting the package disposition; no generic condition waiver |

Before committing a disposition, compare expected request/gate versions, analytical_basis_digest and current capabilities in one application transaction; recompute authoritative prerequisite satisfaction from current receipts. Accept only the same analysis with all applicable prerequisite gates satisfied; do not require the pending package disposition to have already happened. Bind the accepted receipt to that exact snapshot. The resumed node/report rechecks analysis, those accepted prerequisites and this operation's own recorded package disposition, rather than treating its PENDING -> RECORDED transition as a stale-analysis error. A later unsatisfied/new requirement stops completion. Keep human-review acceptance and graph completion separate.

Synthesis fixture/cache keys still bind the exact input used at generation. This contract never relabels a handled issue as though the model saw that future action. The unchanged original synthesis can remain a proposal while current review progress is rendered separately; actual analytical edits invalidate it. Extend TEST-008-02/03/04/07, TEST-007-02/08 and TEST-006-05 with handling-after-pause success, stale expected-gate rejection, post-handling source-change rejection, wrong-tier/competing receipts and unchanged original model output. E-P01/E-F03 remain the walkthroughs; tests are planned, not executed.

The paused checkpoint may retain the original request/gate snapshot as history. On permitted resume, the existing human_review node reads and validates current authoritative handling/condition/disposition records, then returns their scoped current references in its normal state patch before report_generator. ReportInput is assembled from that verified current projection and its accepted snapshot, not stale embedded OPEN statuses in the old interrupt payload. Preserve original model/panel artifacts separately. This adds no graph node/inference and cannot import unrelated or uncommitted handling; TEST-008-07, TEST-009-03 and TEST-011-04 check the final report reflects actual current handling exactly once.

### Edited-condition preparation before disposition

The follow-up check closes a sequencing ambiguity: a condition requiring scoped semantic support must have a reviewable target before final package disposition is accepted. Do not create the target only after committing the disposition and then require an unavailable earlier assessment. Use the existing condition editor, artifact/ConditionRecord storage and typed CLAIM support service; no extra screen, agent, model request or automatic approval.

When proposed human conditions differ from the accepted model conditions and need new support, the Authorized Approver intentionally saves them for review through prepare_review_conditions. This is a metadata-only draft command, not resume_review or HumanDisposition. Validate the current pending request/analysis/gate version and mechanical source/condition links, then save an immutable REVIEW_CONDITION_DRAFT artifact with exact ordered text/links, its content digest and current scope. Create the HUMAN_EDIT ConditionRecords and NARRATIVE-CHECK-1.0 targets against that draft, with their own existing domain-support requirements; no preselected/support-complete state. A malformed draft is rejected with safe retained form data, not accepted as a credit decision.

Permitted Risk Manager/Compliance reviewers assess those exact draft CLAIM targets through the existing capability matrix. Recording draft support against unchanged text/source/analysis advances only the review-gate snapshot; it does not rerun Evidence/Synthesis, alter analytical fact support or invoke the support-continuation path for an accepted model artifact. This narrow draft rule cannot promote unknown source authority or bypass existing mechanical/domain checks. Changing any draft text/link/basis creates a new draft version and stales the affected support. Original model conditions and their evaluation remain unchanged.

Final resume_review must name the prepared draft when used and exactly match its text/links, current analytical basis, gate version and all required support. The accepted HumanDisposition references the same reviewed draft/ConditionRecord/target identities rather than regenerating unsupported targets under a new parent. Bind that association in the acceptance transaction. Unchanged original conditions can instead reference their existing current supported model targets; do not force duplicate draft review. If any required check remains missing or stale, keep the request pending with the actual owner/action and create no disposition/resume. A draft or support acknowledgement alone never satisfies final credit review.

Extend TEST-008-03/06/07 and TEST-010-03/05 using E-P01's existing condition-edit walkthrough: saved draft without disposition/dispatch; correct-domain support before acceptance; exact draft consumption; changed/unchecked/wrong-domain target rejection; no support-parent regeneration after commit; original model conditions preserved. This adds a preparation command within existing review behavior, not a new banking decision, independent scenario or release metric.

## Capability matrix — accepted P3-02

The baseline matrix was accepted with P3-02 on 2026-10-22; score-routing and typed FACT/CLAIM source-support refinements were authorized on 2026-10-23. These are explicit simulated capabilities, not inferred powers from a persona name.

| Action | Permitted simulated persona | Guard |
|---|---|---|
| Inspect local scoped records/sources | All five | Service workspace/deal scope |
| Create/upload/run/correct analytical inputs | Credit Analyst | Current revision, supported synthetic sources, remaining allowance |
| Add note/assign permitted owner/request handoff | Analyst, Risk Manager, Compliance Officer, Authorized Approver | Metadata only; configured owner categories, record-version check |
| Acknowledge issue | Assigned Analyst/Risk/Compliance/Approver | No resolution or gate change |
| Record supported sample numerical exception disposition | Risk Manager | ONLY SYN-ESC-001/002/004/005; current evidence, reason and handling; nonblank conditions for ACCEPT_FOR_CONDITIONAL_REVIEW, conditions may be empty for supported RECOMMEND_REJECT; no missing/control/integrity waiver |
| Record credit-risk score handling | Risk Manager, displayed Credit Risk Manager | ONLY current SCORE-REVIEW-HIGH; complete supported score/driver refs and nonblank reason; distinct from four-rule sample-exception handling and final package decision |
| Record semantic-support assessment | Risk Manager for financial/risk FACT or CLAIM targets, including critical borrower/loan/financial basis; Compliance Officer for sample-policy/control CLAIM targets | Current target/value/source/basis digest, explicit supporting passages/checks/reason; cannot replace a missing source or grant credit disposition |
| Apply supplied control-disposition fixture | Compliance Officer | ONLY allowlisted current-scenario fixture for 009/010 with verified digest/basis; labeled synthetic status update |
| Record package Approve/Reject/Conditional Approve | Authorized Approver | Current pending request; all prerequisite gates handled; NORMAL or required SENIOR tier recorded from trusted demo capability/request; preserve original recommendation |
| Prepare edited conditions for support review | Authorized Approver | Current pending request/analytical basis/gate version; immutable draft with exact links; no disposition, execution or self-granted domain support |
| Cancel/reconcile technical operation | Analyst may cancel; Administrator may cancel/reconcile | Safe boundary; no fabricated provider usage or reset of spent budget |

Every other action/capability defaults to denied. No persona clears purported legal/AML/fraud restrictions by free text. Financial Crimes/Legal are unconnected owner categories, not additional implicit personas. Administrator has no financial or compliance disposition capability.

A numerical exception disposition keeps policy outcome Exception and original comparison. It records DISPOSITIONED plus supported explanation, handling, applicable conditions and actor; package review still follows. RECOMMEND_REJECT may have empty conditions and cannot waive unrelated gates. An unsupported critical source cannot be cured by a reviewer marking “looks fine”. Allowlisted control fixtures are educational supplied evidence, not actual verification. Applying changed control evidence creates a new analytical revision and invalidates affected panels/synthesis/old review.

## Source-issue ownership and permitted repair — SOURCE-TRIAGE-1.0

The authorized Director fixes make SOURCEFIT-1.0 failures actionable using existing issues, five personas, services and offline case preparation. Assignment/acknowledgement is metadata only; it grants no authority and changes no gate. Evaluate whether the dependency is actually required before creating a blocking issue. Optional unassessed content remains explicitly unassessed without inventing a lending requirement.

| Existing-source problem / local reason code | Issue classification and state for a required dependency | Owner and permitted next action |
|---|---|---|
| Required document genuinely absent | Preserve the existing configured missing-evidence rule/root and NEEDS_INFORMATION; do not create a duplicate source-triage exception | Analyst provides/requests supported evidence through existing source replacement/addition and explicit continuation |
| Borrower/facility/financial period/value kind/tier/effective scope unresolved; SOURCE-APPLICABILITY-UNRESOLVED | DEMO_PRODUCT_CONTROL, HIGH, NEEDS_INFORMATION; policy_outcome=null | Risk Manager investigates financial/borrower source context; Analyst performs any authorized source/fact correction. Policy/control applicability is investigated by Compliance Officer instead |
| Field-level authority unresolved or comparable sources disagree; SOURCE-AUTHORITY-UNRESOLVED / SOURCE-CONFLICT-UNRESOLVED | DEMO_PRODUCT_CONTROL, HIGH, NEEDS_INFORMATION; retain both sources and scoped reasons; policy_outcome=null | Risk Manager for financial/loan-term evidence, Compliance Officer for policy/control evidence. Request source-backed resolution and reviewed profile evidence; a role, note or support checkbox cannot invent precedence |
| Trusted source profile/policy-applicability configuration absent or invalid; SOURCE-PROFILE-UNAVAILABLE | DEMO_PRODUCT_CONTROL, HIGH, BLOCKED for affected complete-review dispatch/completion; CONFIGURATION_REQUIRED; safe partial inspection/analysis remains limited by existing guards | Administrator coordinates offline developer/instructor case preparation or restores an already reviewed configuration. No UI profile editor, new upload-registration permission, self-authored financial authority or generic clearance action |

These are product-control reason codes, not additional banking rules or financial decision labels. If an existing subject/conflict issue already represents the same root, enrich/link it instead of counting a second blocker. Store source-selection/profile refs, affected field/node/report scope, required action and existing Issue history. The missing-document card counts only genuine unresolved required-source absence; an available PDF with unclear dates/authority does not count as missing. These product controls never inflate lending-policy exception counts. Show their distinct blocker/reason/owner in the existing Workspace even when the Evidence card says 0 Missing. Unknown source validity cannot be labeled an expired source unless supported.

Only actual supported source/basis/profile repair followed by the normal validation service can resolve the issue. Risk/Compliance investigation records are not new configuration-edit capabilities. Reviewed offline configuration is applied through the existing controlled analytical revision/impact/Save/explicit-continue path by the permitted service, never by a submitted role name or document instruction. Same-revision semantic support cannot substitute for a changed authority/profile/date. Changed dependencies invalidate support, affected panels/synthesis, pending handling and current report under STATE-UPDATE-1.0; preserve history and the SAME ledger. Administrator can coordinate technical repair but cannot clear financial/control content or approve a package. Package review remains unavailable until its actual prerequisites are met.

NARRATIVE-CHECK-1.0 also extends the existing CLAIM target to rationale, individual conditions and proposed-action reasons via application-owned IDs/path/text/source digests. Human-edited conditions retain their own targets; mixed policy/financial assertions require every applicable domain check under the same capability matrix. Source support and underwriting remain separate. INPUT-EDU-1.0 validates commands before any mutation; a rejected input does not create a disposition or trigger inference. Refine TEST-008-01/03/05/06/07 and TEST-010-03/05/06 without adding a screen, role, model call or generic Resolve control.

## Contracts and data changes

| Proposed command | Required payload beyond CommandMeta | Effect |
|---|---|---|
| record_exception_disposition | issue_id/version, handling ACCEPT_FOR_CONDITIONAL_REVIEW or RECOMMEND_REJECT, reason, source/evidence refs, proposed conditions | Separate SampleExceptionDisposition, no fact edit/no inference; original Exception remains |
| record_credit_risk_review | SCORE-REVIEW-HIGH issue/version, exact score/band/method artifact refs, reason, supporting driver refs, proposed conditions | CreditRiskReview record satisfies only current high-score specialty handling; no score/fact/gate waiver or model call; final package review remains |
| record_support_assessment | target: discriminated FACT(fact_id, value/source/basis/subject digests) or CLAIM(claim_id, claim/source digest); support outcome, source refs, reason and explicit checks; current target record version | Scoped FactSupportRecord or SemanticAssessment with simulated attribution; current source-backed support only, no fact edit/graph/model dispatch; claim_id alone is replaced by the typed target contract |
| apply_control_fixture | issue_id, registered fixture_id/version/digest | New control evidence/revision; bounded dependency rerun only on explicit continue |
| prepare_review_conditions | pending_review_id, original panel artifact_id, expected_review_gate_version, analytical_basis_digest, exact ordered conditions/condition_links | Immutable current review-condition draft/targets for existing domain support; no HumanDisposition, resume, graph dispatch or execution claim |
| resume_review | pending_review_id, thread_id, expected_review_gate_version, analytical_basis_digest, human_decision, notes, conditions, condition_links, prepared_condition_draft_ref nullable, original panel artifact_id | HumanDisposition and operation receipt bound to current reviewed conditions/gates; validated Command(resume=payload); no gate downgrade through text or regenerated support targets |
| correct_fact / replace_source | field/fact or source reference, expected old digest, new value/source, reason | Correction record, input_revision+1, invalidation set |
| update_issue_metadata | issue_id, expected_record_version, owner/note/handoff | Metadata-only update and event |

HumanDisposition: id, pending request/thread/deal/run/revision, original_panel_id, exact decision literal, notes, conditions, condition_links, derived condition_record_refs, actor, UTC time, operation_id. Conditional Approve requires >=1 nonblank condition; rationale/notes for overrides are nonblank. Approve/Reject preserve any supplied supported conditions without manufacturing an external decision.

REVIEW-BASIS-1.0 adds analytical_basis_digest, accepted_review_gate_version/snapshot digest and prepared_condition_draft_ref nullable to the application-owned HumanDisposition/receipt metadata. A draft-backed disposition keeps the exact reviewed ConditionRecord/target references. These are local fields, not extra PanelDecision/provider fields; CANON-1.0 binds them to the command and accepted receipt. Review-only handling stays in the same paused thread when analysis is unchanged.
Record required_review_tier and handled_score_referral_refs with disposition. A NORMAL payload cannot satisfy a SENIOR request. Existing AuthorizedApprover is configured for the displayed senior-demo category rather than adding an account/role system; service guards still check current request/tier. CreditRiskReview links the scoped issue/score/assessment/config versions and actor/time/operation. Acknowledgement, note or assignment never substitutes for that record; policy-exception handling and missing-source controls remain independent.

Correction: old/new values and provenance, reason, actor, source refs, affected_artifact_ids, old/new revision. A source-free correction is REVIEWER-provided and cannot satisfy a mandatory documentary-evidence gate. Candidate conflicts require supported resolution, not guessed precedence.

### Fact-support review versus credit disposition

FACT-SUPPORT-1.0 in SPEC-002 governs Live critical-input use. The simulated Risk Manager inspects the exact value, row/label, unit/scale, period, subject and basis alongside cited passages and records HUMAN_SUPPORTED only when supported. A bulk UI action may submit individually identified checked targets; unchecked rows are never auto-accepted. Missing/contradictory evidence remains unsupported; a note, role switch, copied case rating or generic approval is insufficient. A negative support outcome withholds affected trusted use and retains the original extraction for inspection.

Recording support changes no analytical value/source/basis and increments only the support record's version. It has zero inference and does not automatically continue processing. An existing paused run can explicitly continue at its earliest affected dependency under SPEC-007 with the same input revision and cumulative ledger; source/value correction requires the separate new-input-revision path. Support lineage enters dependency digests, so changed support invalidates dependent current metrics/synthesis/review/report where present. Source replacement or retraction stales old support. Prior generated artifacts remain history.

### Condition records — CONDITIONS-1.0

Python derives ConditionRecord from source covenant Facts, accepted synthesis conditions plus condition_links, numerical-exception handling, and supported human edits. The provider-facing five-field PanelDecision and its list[str] conditions are unchanged. Each record has condition_id; deal/input revision; origin SOURCE_COVENANT/MODEL_PROPOSAL/HUMAN_EDIT/SAMPLE_EXCEPTION; category CONTRACTUAL_COVENANT/PROPOSED_REVIEW_CONDITION/EXISTING_PREREQUISITE; exact text; parent artifact/fact/index and source/finding refs; owner_category nullable with explicit Unassigned label; status RECORDED/OUTSTANDING/REVIEW_HANDLED/SUPERSEDED; linked_issue_ids and computed blocks_completion; timestamps/attribution/provenance. Stable scoped IDs and parent/index/digests make repeated rendering idempotent; old text is retained when superseded.

Classification and blocking derive from source origin and linked existing configured issues, never an LLM's or submitted form's permission flag. An EXISTING_PREREQUISITE retains its required owner/action until the underlying issue is actually handled by its permitted service. A missing required current CFADS cannot become an acceptable future condition. Source covenants are RECORDED with EXTRACTED_NOT_EVALUATED coverage from SPEC-003, not contractually fulfilled; no actual covenant monitoring or funding step is built. Proposed review conditions remain OUTSTANDING unless the existing scoped handling actually records a review outcome. Do not invent fulfillment dates, recovery values or external completed actions.

Human-edited/proposed conditions need nonblank text and current supporting condition_links to allowed facts/findings/issues. Owner assignment uses existing role/configuration services; a source clause with no owner displays Unassigned without a fabricated authority. Proposed conditions cannot create or waive an executable lending rule. A simulated Conditional Approve report may complete with OUTSTANDING proposed conditions after all existing mandatory prerequisites and required review are satisfied. Its review/report completion is not fulfillment, funding, covenant compliance or readiness for a real lending decision. No generic Mark satisfied control or separate condition-management screen is added.

Correction impact is a scoped read-only projection: get_correction_impact(CorrectionDraft, ActorContext) -> CorrectionImpact. Draft identifies current fact/source, expected revision/old digest, proposed new value/reference and reason. Impact returns original/proposed values, documentary support status, affected artifacts/sections, planned rerun entry/stages, whether model work may be required, current continuation availability/reason and a verified estimate or Unavailable. It uses existing dependency/budget logic; it reserves no usage, changes no record and invokes no provider/graph. Saving revalidates the draft against current state, rather than trusting an earlier preview. No new database table or remote API is required.

UX-1.0 correction interaction: preview impact -> Save correction -> explicit Update affected findings. Save persists the new analytical revision/provenance/invalidation and prepares the new run/thread as READY against the original review ledger, but schedules no worker/graph/provider work. Preserve original terminal history and stale old requests. Display affected outputs as Out of date after correction and the saved-result message. Only explicit continuation queues the validated rerun; unavailable budget/mode/permission shows its exact prerequisite. Review-only decisions/condition edits remain on the pending thread with zero new model calls. Notes and owner changes do not use this analytical flow.

## AI and evidence behavior

No model call for disposition, note, owner change, support assessment, or preview. Apply SPEC-007's exact transition table: a source-backed analytical correction increments revision, retires the old pending review and prepares a new READY run/thread with the SAME review_id/ledger. Explicit Update affected findings starts at Financial; saving alone does not dispatch it. Do not use Command(resume=...) to insert new facts into an old interrupt. Source addition/replacement affecting extracted information similarly prepares Intake/Extraction continuation and may need further model attempts only on explicit continuation. Prior recommendation/report/disposition becomes stale; unaffected artifacts require verified dependency equality and a fresh envelope. Review-only disposition uses the original pending run/thread and has no model work.

For the core correction demo use E-N01/extraction-miss: the original source DOES state CFADS900,000, but the registered extraction variant misses it. Analyst selects that existing passage and corrects the missing fact; the derived/current terms record both the original extraction result and source-backed human correction. The known corrected-panels synthesis variant then produces the supported current recommendation. E-M01 is a different case: its sources genuinely omit CFADS, so an uncited number cannot complete it. New evidence would require the separate source-addition path, not fake citation reuse.

Fixture synthesis accepts only a registered input_digest for the exact current terms/panels/policy/sources. Unknown edits return FIXTURE_VARIANT_UNAVAILABLE and preserve partial state. See [registered correction example](../evaluation/examples/e-n01-correction.md).

A Risk Manager may record RECOMMEND_REJECT for a supported numerical exception, followed by Authorized Approver's Reject disposition. This is documented handling, not a waiver: original Exception and negative values remain. It cannot clear missing evidence, sanctions/control or integrity blocks. The complete E-F03/reject-supported variant demonstrates this path; no threshold universally forces Reject.

## Authorization

Services enforce the matrix and current capabilities, not just hidden/disabled buttons. Cross-deal, stale, wrong-thread, wrong-role, duplicate-changed-payload and no-pending-review commands fail before graph resume. The local operator can switch personas; this is simulation, not security certification.

## UI states

Pending: reason, owner, original panel and required action. Ready: only permitted actions enabled. Missing/blocked: evidence request and unavailable action explanation. Success: original versus human decision/conditions and recorded attribution. Stale: previous action cannot apply to new revision. Empty: Not required or Not evaluated, never Human approved.

## Reliability and stopping

Same durable thread/checkpointer for resume; RAM saver only in the same process. Duplicate resume returns the original result without another mutation or paid step. If handling is incomplete, leave the pending request/partial state rather than report completed. Human waiting excluded from active time; resumed node counts again. Uncertain/stale resume recovery follows SPEC-011, not automatic provider replay.

## Analytics

review_requested/resumed/disposition_recorded; exception_disposition_recorded; credit_risk_review_recorded; semantic_assessment_recorded; control_fixture_applied; correction_recorded; artifacts_invalidated; issue_metadata_updated; action_denied. Log reason categories, scoped artifact/control IDs and required/recorded tier, not notes, conditions, factor ratings or source contents.

## Tests and acceptance

- TEST-008-01: Complete matrix allow/deny cases, especially Admin versus Approver, separate Risk Manager High-score handling and unmapped specialties; NORMAL capability cannot satisfy SENIOR review tier. SOURCE-TRIAGE-1.0 maps financial/policy/configuration problems to existing owners without granting configuration/clearance powers.
- TEST-008-02: Amount/confidence/score/other mandatory referral; Moderate always human, High handling plus package review, Very High senior tier; same-thread pause/resume without a repeated-referral loop; no-review labels only for valid Low/no-independent-referral packages.
- TEST-008-03: Numerical exception disposition, credit-risk handling and package review are separate records; generic acknowledgement cannot satisfy High-score handling; missing/specialty gate cannot be waived by a score, acceptance or proposed condition. E-M01 CFADS stays blocking; E-P01 may complete its simulated Conditional report with outstanding supported proposals, never fulfilled/funded labels.
- TEST-008-04: Stale/wrong-thread/duplicate/invalid payloads and blank modified conditions rejected. RESUME-1.0 allows only its own committed receipt after RECORDED, not a competing operation; no duplicate disposition/report at acceptance/checkpoint crash gaps.
- TEST-008-05: Read-only impact preview preserves revision/usage and rejects wrong scope; Save revalidates stale drafts, records provenance/new revision and READY rerun while invalidating precise dependencies/reports/dispositions with zero graph/provider dispatch; only explicit permitted continuation starts affected work. Notes invoke zero inference.
- TEST-008-06: Registered versus unregistered synthetic control fixtures; required documentary source cannot be replaced by opinion. FACT/CLAIM support targets enforce role, current value/source/basis/subject digests and substantive checks; stale/wrong-row/scale/entity support is denied or withheld. Support-only changes no fact/revision, triggers no model, and needs explicit dependency continuation; source/value correction uses the analytical path. NARRATIVE-CHECK-1.0 includes rationale/condition/action CLAIM targets and all applicable domain checks; source authority cannot be granted through semantic support.
- TEST-008-07: Resume-only consumes zero new model attempts, preserves PanelDecision and explicitly separates human conditions; current score/band/configuration references and review tier required, dependent analytical correction stales previous handling/disposition. Accepted disposition versus graph progress remain distinct; stable interrupt position/read-only prelude and explicit current-receipt recovery are required.
- TEST-008-08: E-N01 missed-but-documented correction matches its registered synthesis variant; E-M01 unsupported manual value stays blocked; unknown correction variant cannot receive canned success or revive a stale review.

Target: 100% controlled review/permission/invalidation cases. E-P01/P05, E-M01–M03, E-C01–C04, E-A02/A03 plus additional focused tests.

## Dependencies and implementation boundary

Uses SPEC-004/005/007/011. P3-01/02 are accepted; changes require review before code. No actual review endpoint, capability file, synthetic control fixture, checkpointer or authenticated identity exists yet.
