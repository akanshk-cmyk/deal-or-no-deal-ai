# Synthesis, PanelDecision and Evidence Validation

**Registered E-P01 fixture:** Source/rubric registration binds the unchanged
five-field PanelDecision Conditional Approve and one source-linked annual-statements
condition. It is authored fixture content, not measured model quality or a repayment
cure. Independent specialist support binds the prepared draft; it does not upgrade
the original AI narrative to HUMAN_SUPPORTED or change policy Exception. See
[CONDITIONAL-1.0](conditional-integration.md).

Feature ID: SPEC-005
Version: 1.7
Status: Registered saved synthesis/evidence paths and actual-response live integration implemented; saved-answer RAGAS executed; actual live synthesis/evaluation pending
PRD requirements: FR-006–009, FR-014–019
Role instructions: [Synthesizer](../agents/synthesizer.md), [Evidence Reviewer](../agents/evidence-reviewer.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

A learner sees how Financial, Compliance and Risk findings inform a single simulated recommendation and can inspect its support. Synthesis is the second normal live call; Evidence is Python plus human support flags. No judge model or model-written final memo.

## Workflow and rules

Authorized 2026-10-24: [QUALITY-REVIEW-1.0](../evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10) adds read-only original-response review for every narrative target and its transitive source/panel/calculation references. Python recomputes applicable gates for review diagnostics; arbitrary valid prose remains MANUAL_REVIEW_REQUIRED, not accepted synthesis, HUMAN_SUPPORTED or a credit disposition. Preserve the exact registered normal Fixture path and two-call architecture.

Require three current, validated panels. A valid panel may contain explicitly optional Unknowns; mandatory unresolved data/support dependencies prevent synthesis. A known numerical exception with complete evidence can be interpreted, but remains a referral and cannot be waived by prose.

Complete synthesis is restricted to SPEC-001's registered reviewed case packs with current factor/material configuration. Unregistered synthetic uploads remain partial without an accepted PanelDecision. Required critical Live facts must satisfy FACT-SUPPORT-1.0 and subject/facility coherence before the panels are trusted; a model's citation is not its own validation. Fixture execution remains explicitly demonstration-only. These application-side prerequisites add no generation stage.

Create a bounded context, reserve usage, invoke synthesis, validate strict schema and references, then run Evidence checks. Reject unsupported new numbers, omitted mandatory exceptions, invented covenants, false clearance, or claims of completed human action. Keep quarantined response metadata; do not display rejected recommendations as accepted.

PanelDecision fields are exactly:
- decision: Approve / Conditional Approve / Reject, exact literals.
- confidence: finite number 0..1, no Boolean/string coercion.
- rationale: substantive nonblank text.
- conditions: list of nonblank strings; at least one actionable supported condition for Conditional Approve.
- escalate_to_human: Boolean; final effective value computed by Python.

Do not add Unknown as a decision value or use Reject to represent missing data/parser failure. Confidence is uncalibrated. Python routes requested amount >=USD 10M OR confidence <0.7 OR another mandatory referral. A raw model flag cannot defeat this route.

SCORE-ROUTING-1.0 adds mandatory Moderate/High/VeryHigh review reasons to that Python route. A complete supported risk score/band and its authored driver/rubric references may now enter the bounded risk-panel projection for explanation; they are labeled educational assessments, not PD or verified bank ratings. Missing material score inputs pause dependent synthesis/final-decision readiness; do not fill factors to produce a recommendation. A low score cannot cancel independent policy/evidence controls, and no score/breach universally selects Reject.

## Contracts and data changes

synthesize(SynthesisRequest, adapter) -> StageEnvelope[SynthesisResult].
check_evidence(EvidenceRequest) -> StageEnvelope[EvidenceReview].

SynthesisRequest: three panel references, compact terms/evidence packet, current issues/gates, current identity and schema. Fixture requests additionally bind fixture_variant_id and normalized semantic input_digest, excluding generated run/artifact IDs but validating their scope separately.
SynthesisResult: panel_decision, executive_summary list[Claim], financial_interpretation list[Claim], risk_summary list[Claim], rationale_refs, condition_links mapping condition index to supporting finding/source IDs, and application-owned evidence_target_refs covering all narrative fields under NARRATIVE-CHECK-1.0 below. Each required panel has a referenced substantive observation; no exact-wording requirement. evidence_target_refs is not a provider-wire field.

Python maps accepted condition strings and condition_links into SPEC-008's CONDITIONS-1.0 records and attaches application-side condition_record_refs to the artifact projection. The model neither assigns blocking authority nor claims a source covenant was tested/fulfilled. Keep outstanding supported review proposals separate from existing missing-data prerequisites. Supported annual-period observations cannot become full-term/balloon repayment, investment valuation or reported-EBITDA reconciliation claims; those are explicitly unevaluated/deferred in SPEC-003. Bank-policy Pass is not contractual-covenant Pass.
SynthesisResult may additionally contain proposed_action nullable: kind CONTINUE_STANDARD_REVIEW/NORMAL_HUMAN_REVIEW/REFER_CREDIT_RISK_MANAGER/REFER_SENIOR_CREDIT_AUTHORITY/REQUEST_EVIDENCE, target existing owner category, substantive reason and supporting finding/driver/issue references. It is outside the exact five-field PanelDecision and uses the existing single synthesis call. Schema/config changes require matching fixture variants and token preflight; do not assume the existing target caps can fit without measurement. Validate proposal support against current issues/owner/referrals; it grants no tool/approval permission. The Orchestrator computes the actual permitted next action independently. When synthesis was not run/was withheld/stale, proposed_action is unavailable, never generated by a UI template and labeled AI. Missing-data screens show Required action from the Orchestrator instead.
EvidenceReview: claim_checks with reference_resolves, numeric_consistent, conflict_preserved, semantic_status; fact_support_refs and subject/basis checks for material input lineage; omitted_critical_findings; unsupported_claim_ids; issue_refs; completion_gate. Criticality is derived from configured field/control categories, not solely the model's critical Boolean. A scoped human support record cannot override a failed mechanical check, replace absent evidence or clear another issue.

Preserve raw proposed escalation as diagnostic metadata separately from the effective accepted PanelDecision flag. HumanDisposition never overwrites PanelDecision. Executable models follow CONTRACT-1.0, with unknown fields rejected.

## Compact synthesis wire and trusted hydration — SYN-WIRE-1.0

### Authorized E-N01 normal slice — E-N01-SYNTHESIS-1.0

The user's acceptance of the recommended next step on 2026-10-23 authorizes preparing the current E-N01 synthesis packet, validating it offline and connecting the normal Fixture path to report generation. Reuse the ordinary supported example below and the registered source/assessment pack; do not alter the original case registration, source PDFs, instructions or financial rules. A separate synthesis registration pins the exact case dependency, semantic request digest, canned wire and fixture evidence rubric. This is an AI-authored educational stage fixture, not a new bank rule, actual model result or human semantic approval.

synthesis.py prepares the current compact terms, annual financial metrics, all sample-rule results/applicability, authored five-factor score/drivers, basis/cutoff and transitive source/calculation/policy/panel reference dictionary. Include every material qualification. Its provider-shaped request contains no expected answer, review notes or rubric. Freeze the request and schema/instruction/dependency hashes before binding the response. A separate rubric binds all four ordinary narrative targets to exact supported fixture text and references. Exact fixture matching plus deterministic reference/number checks yields FIXTURE_EXPECTATION_CHECKED/REFERENCE_CHECKED, never HUMAN_SUPPORTED or general semantic entailment. New/changed text, wrong input/scope, invented references or changed registration fail explicitly; there is no fuzzy/canned fallback.

After strict SYN-WIRE-1.0 parsing, create every local narrative target with existing hydrate_narrative and verify its references transitively reach the supplied original pages/policy/calculations. Re-evaluate Python's confidence/amount/score and independent controls; preserve raw versus effective escalation. This slice permits only the registered Low/default direct-report case. An unexpected referral or missing support stops with a safe prerequisite reason; reviewed/correction/other-case paths remain pending, never silently bypassed. Full-context tokenizer fit and real model quality remain unverified. Extend the offline Qwen/Nano plan to include this shared synthesis request while leaving model measurements null.

AE-01 is adopted by the user's engineering-fix instruction. The provider returns SynthesisWire, not StageEnvelope, Claim or the full SynthesisResult. All six root keys are required: panel_decision, observations, rationale_refs, condition_links, proposed_action, wire_version. wire_version is the literal SYN-WIRE-1.0. Unknown fields are forbidden at every object boundary; no coercion or silent defaults.

| Wire field | Exact contract |
|---|---|
| panel_decision | Exactly the five domain fields listed above; escalate_to_human is a model proposal only |
| observations | Exactly three objects, one per FINANCIAL/COMPLIANCE/RISK panel, each with only panel, text (nonblank), refs (nonempty distinct supplied logical handles) |
| rationale_refs | Nonempty distinct supplied logical handles supporting the decision rationale |
| condition_links | List of objects with only index (strict integer >=0) and refs (nonempty distinct supplied handles). Exactly one entry per conditions index; empty when conditions is empty; no gaps/duplicates/out-of-range indexes |
| proposed_action | Required nullable object with only kind (the existing five proposal literals), target (existing permitted owner category), reason (nonblank), refs (nonempty supplied handles). Validate kind/owner/evidence compatibility against the current request; no executable authority |

The application creates the allowlisted handle dictionary before dispatch. Handles identify current panels/findings/calculations/issues or original source locations under CANON-1.0; they are not arbitrary model IDs. Every returned handle must resolve in that exact request and permitted scope. No guessed citation repair. The examples below are complete illustrative wire objects, not registered fixtures or observed model outputs. Their handles need real current dictionaries before any execution.

Ordinary supported example:

~~~json
{"wire_version":"SYN-WIRE-1.0","panel_decision":{"decision":"Approve","confidence":0.85,"rationale":"Supported annual repayment metrics and the supplied Low assessment support this simulated recommendation; contractual covenants remain unevaluated.","conditions":[],"escalate_to_human":false},"observations":[{"panel":"FINANCIAL","text":"Annual DSCR is 1.50x; this does not assess full-term repayment.","refs":["calc:DSCR"]},{"panel":"COMPLIANCE","text":"Applicable sample checks passed; this is not legal clearance or covenant compliance.","refs":["panel:COMPLIANCE"]},{"panel":"RISK","text":"The complete authored assessment is Low, not a default probability.","refs":["panel:RISK"]}],"rationale_refs":["calc:DSCR","panel:COMPLIANCE","panel:RISK"],"condition_links":[],"proposed_action":null}
~~~

Conditional supported example:

~~~json
{"wire_version":"SYN-WIRE-1.0","panel_decision":{"decision":"Conditional Approve","confidence":0.8,"rationale":"Annual DSCR is below the sample minimum; the supported exception requires separate Risk Manager handling and package review.","conditions":["Obtain the required current exception handling and package disposition before completing the simulated review."],"escalate_to_human":true},"observations":[{"panel":"FINANCIAL","text":"Annual DSCR is 1.15x.","refs":["calc:DSCR"]},{"panel":"COMPLIANCE","text":"The DSCR exception remains open and cannot be waived by this proposal.","refs":["issue:DSCR"]},{"panel":"RISK","text":"The current complete authored assessment must be considered independently of this exception.","refs":["panel:RISK"]}],"rationale_refs":["calc:DSCR","issue:DSCR","panel:RISK"],"condition_links":[{"index":0,"refs":["issue:DSCR"]}],"proposed_action":{"kind":"REFER_CREDIT_RISK_MANAGER","target":"RiskManager","reason":"The current DSCR exception needs its permitted specialist handling.","refs":["issue:DSCR"]}}
~~~

Python first validates the complete wire and handle resolution, then generates scoped artifact/Claim IDs, provenance, timestamps and dependency metadata. Each observation becomes one INTERPRETATION Claim; executive_summary references all three, financial_interpretation references the FINANCIAL Claim, and risk_summary the RISK Claim. Reusing the same Claim in these views does not create additional claims. Criticality is conservatively derived from trusted field/control categories and referenced dependencies, not submitted by the model. New narrative support starts PENDING, advances only through mechanical Evidence checks to REFERENCE_CHECKED, and requires a separate permitted current support record for HUMAN_SUPPORTED. Hydration cannot invent semantic support, an actor, an approval or fulfilled condition. Python derives condition records and the effective escalation flag; retain the raw flag only as diagnostic provenance. The exact five-field domain PanelDecision is unchanged.

Schema/refusal/transport acceptance is governed by PROVIDER-1.0 in SPEC-007 before hydration. Validate round-trip domain coverage, all three panels, conditional links and unauthorized-field rejection in existing TEST-005-01–06. TEST-006-04/08 must serialize both complete examples, the actual schema and current source dictionaries with the selected tokenizer. The 350-output target is unmeasured and these examples are not proof of fit. Reallocate only inside unchanged global ceilings with the correction reserve protected, or shorten the supported package losslessly and remeasure; otherwise stop. No extra model call or relaxed evidence field is authorized.

## Evidence targets for every narrative field — NARRATIVE-CHECK-1.0

The user authorized the Director review recommendations. Keep the exact SYN-WIRE-1.0 response, five-field PanelDecision and two normal model calls. Python registers a small fixed set of scoped Claim targets after strict wire validation; no sentence-splitting framework, additional agent or LLM judge.

| Local field path | Target kind | Supporting references |
|---|---|---|
| observations[0..2].text | INTERPRETATION; reuse the three existing observation Claims | Each observation's refs, preserving panel identity |
| panel_decision.rationale | INTERPRETATION; additional local target | rationale_refs |
| panel_decision.conditions[i] | PROPOSED_CONDITION; one target per condition | Exact index-matched condition_links entry |
| proposed_action.reason when present | INTERPRETATION; additional local target | proposed_action.refs; independently validate kind/target against current required action |

Each target binds parent synthesis artifact/digest, exact field path/index/text digest, current source/dependency and ReviewSourceBasis/profile versions, existing Claim ID/type/support fields, and derived criticality/domain checks. The application-owned NarrativeTargetRecord has claim_ref, parent_artifact_ref, parent_digest, field_path, index nullable, text_digest, dependency_digest, required_domains (set of FINANCIAL_RISK/POLICY_CONTROL), and record_version. Scope comes from its validated StageEnvelope; text/type/criticality/support state come from the referenced Claim, not a second copied text body. evidence_target_refs is the complete list of these local record references. Generate IDs once per scoped operation/path; rendering/replay cannot duplicate targets. Store target metadata in existing artifacts and attach evidence_target_refs locally. executive_summary still references only the three observation Claims; the additional rationale/condition/action targets do not become duplicate summary text. A three-observation response with no conditions/action has four narrative targets; with N conditions and an action it has 5+N. The model cannot supply target IDs, support labels or approval authority.

Run the same reference-resolution, exact-number/unit/date consistency, SOURCEFIT applicability, mandatory-finding retention and semantic-support checks for EVERY target. A field may contain several assertions: all material assertions must be supported; a correct clause/citation does not compensate for an unsupported guarantee, completed-action claim or invented covenant elsewhere in that field. Do not claim that a deterministic check proves semantic entailment. Start PENDING, advance only to REFERENCE_CHECKED for passed mechanical checks, and confer HUMAN_SUPPORTED only through current scoped SPEC-008 assessment records. Known unsupported critical content is withheld and blocks affected acceptance/completion; unresolved material meaning requests the appropriate existing support assessment. Noncritical uncertainty follows the existing explicitly partial workflow, never a silent edit or verified badge. Numeric confidence remains uncalibrated metadata, not an evidence-supported probability claim.

These support checks do not make every package require credit approval. FACT source support, narrative semantic support, specialist exception handling and conditional credit disposition remain distinct. Risk Manager handles financial/risk targets; Compliance handles policy/control targets. Mixed-domain assertions retain every applicable domain check; one role cannot clear the other's required issue. Human condition edits needing support use SPEC-008's immutable current condition draft and targets BEFORE disposition acceptance. The final disposition consumes those exact reviewed ConditionRecord/target references, without regenerating their parent or erasing original model targets/EVAL-CUTOFF-1.0 scoring. Draft support is only review-gate progress under REVIEW-BASIS-1.0; support changes to accepted analysis still use the existing same-revision continuation/invalidation rules, while actual fact/source/basis edits use analytical revision+1. No extra model call or invisible repair of accepted original PanelDecision is permitted. STATE-CODEC-1.0 defines the immutable parent-content projection before attaching target references, avoiding circular hashes.

Existing TEST-005-03/04/05, TEST-008-06/07, TEST-009-02/05 and TEST-011-01/07 cover unsupported statements inserted separately into an observation, rationale, condition and action reason; same-field mixed supported/unsupported assertions; duplicate target creation; stale support; wrong-domain support; and separate original-versus-human-edited evaluation. Required demo outputs still require complete material citation/support review. No extra TEST ID, metric, schema-visible model field or paid call.

## AI and evidence behavior

Only Synthesizer has a runtime prompt; compact shared instructions and relevant facts accompany it. Evidence resolves references in the same deal/source version, compares copied values to validated calculations, and verifies known mandatory findings are retained.

A resolving citation is not semantic verification. Live narrative defaults to REFERENCE_CHECKED unless human semantic support is recorded; do not label it verified. Known semantic uncertainty creates review need, and critical unsupported content is withheld/blocks completion. This does not require universal human review of every ordinary package: the existing conditional route remains, with explicit machine-check versus human-support labels. Gold annotations validate fixture checks, not unseen live semantic truth.

## Authorization

Dispatch only via SPEC-007. All permitted personas can inspect evidence; semantic-support/correction actions use SPEC-008 capability checks and references. The model has no filesystem, network, policy-edit or external-action tools.

## UI states

Empty: prerequisites absent. Loading: model versus deterministic Evidence stages distinguished. Success: accepted simulated recommendation, panel-linked rationale, support labels and routing reasons. Failure: quarantined/invalid result and permitted repair. Partial: no accepted decision when mandatory evidence is absent; no false completed committee recommendation.

## Reliability and stopping

<=45 seconds per provider call and remaining total active time. Repairs are explicit additional attempts within SPEC-007 limits. Do not add a third routine narrative call or hidden schema-repair loop. A reference-only repair may be local only when deterministic and meaning-preserving; never invent/guess a replacement citation.

## Analytics

synthesis_validated; evidence_checked with accepted/rejected/unknown counts; decision_route_computed with reason codes; provider/context events. No rationale, conditions text, raw confidence narrative or source quotes in routine analytics.

## Small QA checks required for the educational demo

QA-RISK-FP-01 is a high-level offline QA check: manually record false-positive risk counts against the synthetic case's supported findings, alongside recall. Count duplicate versions of the same unsupported risk once. No new UI indicators, scoring workflow, automated judge or LLM call is required. Unsupported critical allegations still fail existing evidence gates. See MET-22 in the evaluation plan.

QA-REJECT-01 uses the [complete E-F03/reject-supported example](../evaluation/examples/e-f03-reject.md): documented negative CFADS with positive debt service, valid negative DSCR and supported Reject rationale; positive EBITDA does not substitute for cash. Python routes the material DSCR exception to review even with confidence .82 and loan belowUSD10M. Separate Risk Manager handling and Authorized Approver Reject retain the exception, then generate the report. Missing-data/technical errors have no accepted PanelDecision, and a simple threshold breach in another case does not automatically mean Reject.

## Tests and acceptance

- TEST-005-01: All labels; required fields; strict Boolean/numeric types; confidence 0/1/.7/.6999/nonfinite; blank rationale/conditions. SYN-WIRE-1.0 ordinary/Conditional examples round-trip; reject extra IDs/support/criticality/authority fields, missing panel observations and invalid condition index links.
- TEST-005-02: Missing/stale panels or material score inputs prevent dispatch; all three panels and current supported score/band/driver context represented in accepted output.
- TEST-005-03: Unsupported number/source/covenant or omitted critical exception is rejected/withheld. Reject invented covenant compliance, completed conditions, full-term/balloon repayment and reported-EBITDA reconciliation; annual-policy evidence cannot support those assertions. An existing missing prerequisite cannot be laundered into a proposed condition. NARRATIVE-CHECK-1.0 checks independent unsupported assertions in rationale, each condition and action reason, including a mixed supported/unsupported field.
- TEST-005-04: Valid source with unsupported meaning is not automatically human-verified. All narrative paths have current application-owned support targets; wrong-domain/stale support or neighboring correct text cannot confer verification.
- TEST-005-05: Model false flag cannot defeat amount/confidence/score/other mandatory referral; gate-conflicting Approve cannot clear a block. Preserve exact five-field PanelDecision; validate optional proposed_action's kind/current references/owner/support and exclude it from permission decisions. Stale/missing/withheld synthesis cannot produce an AI-labeled proposal.
- TEST-005-06: Fixture labeling and two-call normal path; no Evidence/judge/report inference. PROVIDER-1.0 rejects refusal, empty content, unexpected tools, non-success finish and truncation before hydration; reconcile usage independently. INPUT-EDU-1.0 rejects duplicate/oversized embedded JSON and transport envelopes while preserving unresolved usage reservations.
- TEST-005-07: QA-REJECT-01 executes the complete E-F03 variant, preserves a genuine Reject through permitted handling/review/report, retains negative values and never converts schema/missing-data failure into Reject.

Targets: 100% accepted schema validity and critical safeguards; >=90% supported risk recall; >=95% supported material claims overall; zero accepted unsupported critical claims. Required demo outputs require complete material citation/support review. E-N01–N05, E-P01–P05, E-C04 and E-T03.

## Dependencies and implementation boundary

Uses SPEC-003/004/006/007, feeds SPEC-008/009/010. Provider structured-output capability is model-specific and must be validated later; schemas are not an assertion of successful integration.
