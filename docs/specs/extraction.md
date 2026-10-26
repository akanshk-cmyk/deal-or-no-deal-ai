# Structured Deal Extraction

**Uploaded candidate implementation:** [UPLOAD-FACT-1.0](upload-fact-review.md)
implements manual source-bound proposals and separate RiskManager semantic support
for three CALC-004 inputs. Exact reference/token normalization is not human support.
Candidates remain REVIEWER_PROVIDED / UPLOAD_CANDIDATE_ONLY, not hydrated Live deal
facts. All other critical facts, full source/subject registry and model extraction
remain pending; existing wire shape/Runtime prompts are unchanged.

Feature ID: SPEC-002
Version: 1.6
Status: Registered saved extraction and actual Nebius extraction verified; live fact support pending; generic uploaded-case financial admission unsupported
PRD requirements: FR-003, FR-007–008, FR-015, FR-019
Role instructions: [Extractor](../agents/extractor.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

A learner receives normalized source-linked terms from the synthetic package. Extraction interprets language once; it performs no financial arithmetic, policy decision, risk scoring, or automatic source precedence.

## Workflow and rules

Authorized 2026-10-24: implement the bounded [QUALITY-REVIEW-1.0 preparation/response checks](../evaluation/generation-model-comparison.md#authorized-quality-preparation-and-response-review--quality-review-10). Preserve full registered source context, reviewed basis and original page locations; compare each returned field's value/basis/reference separately. Wrong/missing/conflicting fields and malformed or non-complete responses remain visible without semantic self-certification. Live provider execution/token fit and general PDF layout fidelity remain unverified.

Verify current manifest, select faithful source context via SPEC-006, reserve usage via SPEC-007, and dispatch one structured request. Parse strict types, reject unsupported source IDs, and retain missing/conflicting candidates. Publish a valid or clearly partial DealTerms artifact; do not promote malformed/critical unsupported facts into financial inputs.

Documentary absence uses status MISSING and normalized value null; explicitly stated zero is KNOWN. Conflicting authoritative-looking terms remain two candidates with both references. No regex-based substantive deal-term extractor or unapproved source-priority heuristic replaces the agreed model task; deterministic format validation is permitted.

## Contracts and data changes

Proposed internal services: extract_terms(ExtractionRequest, adapter) -> StageEnvelope[DealTerms]; validate_terms(DealTerms, manifest) -> ValidationReport. Adapter selection is injected, never inferred from file content.

DealTerms: borrower, legal_entity, facility_type, requested_amount, currency, term_months, maturity_date, interest_terms, repayment_structure, collateral, guarantees, covenants, use_of_proceeds, financial_inputs, missing_fields, conflicts. Each scalar is a Fact or explicitly absent Fact; repeated clauses are Fact lists with provenance. facility_type must be supported term loan or flagged out of scope; requested_amount is a finite positive Decimal string when known; currency USD or unsupported flag, with no FX conversion; term_months positive integer, not rounded from an invented date basis.

InterestTerms preserves fixed/floating label, source-supported rate/spread/index/reset/floor details, raw text and refs. It does not forecast rates. Conflict: conflict_id, field_name, candidate facts, materiality/configuration status, affected metrics, resolution nullable.

FinancialInputs uses a fixed registry of Fact names: net_income, interest_expense, income_tax_expense, depreciation, amortization, cash_available_for_debt_service, annual_principal_payments, annual_interest_payments, existing_funded_debt, proposed_funded_borrowing, transaction_debt_repaid, eligible_equipment_value, prior_ranking_liens, secured_facility_exposure, current_revenue, previous_revenue, current_assets, current_liabilities. Preserve period/as-of/assessment basis. Authorized SME-06 resolution: normalized reported/adjusted-EBITDA extraction and automated reconciliation are deferred in this five-day MVP. Original passages remain inspectable; do not promise a separate retained EBITDA observation, mismatch alert, discretionary addbacks or substitution for FIN-1.0. The existing eighteen keys and provider wire shape remain unchanged.

Provider-facing DealTermsWire has exactly three required root keys: terms (fixed registered keys), financial_inputs (fixed registered keys) and conflicts (list). Every WireFact has exactly value, refs (list of passage IDs) and basis_id (known registry ID or null where inapplicable). All field keys are present; missing fields have value=null, refs=[] and basis_id=null. Conflict fields have value=null with their candidates retained in conflicts. Unknown keys and coercion are rejected.

[The complete wire contract/example](examples/extraction-wire.md) specifies the field registry, strict types, null handling, InterestTerms object and deterministic mapping. term_months is a strict positive integer; Booleans/strings cannot substitute for it. Money and financial inputs are canonical finite Decimal strings; dates are validated ISO-date strings, not arbitrary text. Typed InterestTerms and list values are allowed only for their registered fields.

Python hydrates raw_text from the first referenced verbatim source passage (display choice, never authority precedence), retains all references, resolves basis/unit/type from the registry, derives missing/conflict status, and adds trusted StageEnvelope metadata. It does not ask the model to repeat source text, UUIDs, filenames or complete source objects. A cited passage must still support the normalized value; hydration does not certify semantic accuracy. Missing has no fabricated source, and conflict candidates retain both passages. Reviewer corrections remain distinct from model extraction.

### Critical fact support — FACT-SUPPORT-1.0

Authorized SME-03 fix: Fact.status KNOWN means an extracted value exists, not that its meaning was verified. Attach separate FactSupportRecord references after hydration; add no model-output fields. A record binds deal/input revision, fact_id/value digest, source digests/passages, basis/subject registry versions, checks for reference/row/label/unit/scale/period/entity compatibility, status PENDING/REFERENCE_CHECKED/HUMAN_SUPPORTED/UNSUPPORTED/WITHHELD, reason, actor/method, UTC time and operation identity. Mechanical resolution cannot set HUMAN_SUPPORTED. Wrong or unresolved scope/source/value support prevents trusted use even when the JSON parses.

Trusted CriticalFieldRegistry identifies current required inputs by field and applicability: borrower/entity, requested amount/currency/facility, required loan terms, and each material FIN-1.0/risk-input dependency, including documented zeros and basis/subject attribution. Optional absent measures or an inapplicable equipment valuation do not become mandatory. Registry changes are reviewed configuration, not model-controlled critical flags. Missing facts remain MISSING rather than acquiring support from a free-text assessment.

In Live mode, a required extracted/corrected critical fact must have current HUMAN_SUPPORTED evidence before it enters trusted dependent calculations/policy/risk/synthesis. The simulated Risk Manager records source-backed factual support through SPEC-008's generalized target; this is data-quality review, not a loan disposition or score-referral handling. The Workspace groups the existing fact/evidence checks for review without a new screen or model. Unchecked facts can be inspected as extracted, but affected metrics remain Unknown and dependent work pauses. An unflagged reference-only check is not implicit semantic approval. Required support for source clauses cannot be replaced with notes.

Registered Fixture mode may execute its explicitly labeled demonstration from validated scoped stage fixtures using REFERENCE_CHECKED facts. This mode-specific permission is not HUMAN_SUPPORTED, Live verification or observed extraction quality. Gold support evaluation stays outside the runtime/model inputs. A malformed, wrong-subject or known unsupported fixture input still cannot pass; offline case QA checks the fixture's source faithfulness before acceptance. No evaluator gold is loaded to confer runtime authority.

record_support_assessment appends evidence support without changing a fact's value/source/basis. It dispatches no graph/model work and is idempotent for the target digest. Correction of a value/source/basis still uses the analytical revision path. Changed dependencies stale prior support. SPEC-007 defines explicit same-revision continuation after a support pause; no paid extraction replay or new budget. The normal complete Live path still has two generation calls, with human waiting reported separately.

FixtureResponseKey includes scenario_id, fixture_variant_id, stage, package_digest and input_digest (the normalized current-stage semantic input digest). Matching PDF bytes alone is insufficient for corrected synthesis. A registered E-N01/extraction-miss -> corrected-from-extraction-miss variant supports the educational correction path. Unknown edits/dependency digests return FIXTURE_VARIANT_UNAVAILABLE; never reuse a canned synthesis for different facts. See [correction example](../evaluation/examples/e-n01-correction.md).

No amount, lien, debt repayment or missing financial component is silently zero. The fixture manifest supplies explicit zeros where appropriate. Unknown maturity/term blocks the dependent term check, not every safe observation.

## Engineering boundary refinements

The runtime prompt must explicitly name DealTermsWire and its exact three roots/WireFact fields. Its missing representation is JSON null with empty refs/null basis, never a literal Unknown. Notes, raw_text, source objects, status and envelope metadata are forbidden provider fields. The richer domain representation is hydrated only in Python. TEST-002-07 and TEST-006-01/04 inspect the actually loaded Runtime prompt plus schema/example, rather than assuming a developer-only clarification outside that section reaches the model. Updating this prompt requires new instruction hashes and reviewed fixture/profile dependencies; do not silently reuse an older matching key.

Use SPEC-006 CANON-1.0 for exact typed dependency/fixture fingerprints and logical-handle-to-current-reference hydration. Same semantic inputs with new incidental UUIDs may match a reviewed variant, but changed support/source/basis/subject/instruction/schema/model configuration does not inherit the old result. A passage ID can expand to all contributing original locations under COVERAGE-1.0; do not collapse a cross-page table into a fabricated single page. Preserve the existing three-root extraction wire and field registry.

Normalize raw provider completion/refusal/truncation/usage through SPEC-007 PROVIDER-1.0 before accepting a wire. Snapshot original extraction and repair lineage before human edits under EVAL-CUTOFF-1.0. Refine existing TEST-002-06/07 and TEST-011-07; no new inference stage or automatic repair loop.

SOURCEFIT-1.0 in SPEC-006 distinguishes application-current from business-applicable. Extract the faithful bounded source package and preserve alternatives, dates, units, periods and qualifiers; do not choose a candidate because it is newest or remove an amendment exception. Python uses the reviewed source profile/selection record to determine eligible dependent use. Different financial periods, price types or applicability tiers are not automatically conflicting facts. If the unchanged wire needs to retain same-field alternatives, use its conflict representation and explicit source-backed resolution rather than silently replacing the original extraction. Unknown material temporal/authority fit pauses affected use even when JSON and HUMAN_SUPPORTED checks otherwise pass. No wire-field expansion or additional inference.

INPUT-EDU-1.0 in the overview is the shared raw-JSON/field validation profile for commands/model content. Reject nested/escaped duplicate keys before Pydantic or hydration; never select the last duplicate decision/value. Bound bytes/depth/collections/text and normalized financial numeric representation before Decimal expansion/canonical hashing. The existing extraction wire still has three roots/thirteen terms/eighteen financial keys. Out-of-profile values produce technical input/schema errors, not clamped values or credit Reject; preserve raw source evidence for diagnosis. Normal document units must be normalized exactly before applying input bounds. Existing TEST-002-04/07 exercises profile boundaries, legitimate negatives/zero and no automatic paid repair.

## AI and evidence behavior

Load only the Extractor Runtime prompt, shared Model context rules, required schema and source blocks. One normal live attempt; zero in matching Fixture mode. Require source references per known material fact; reviewer-provided values never receive fabricated PDF refs. Treat embedded instructions as untrusted data. Any semantic uncertainty remains visible.

Use provider-supported structured output with verified model compatibility; local Pydantic validation remains mandatory. Valid JSON alone does not establish factual correctness. No extra extraction summarizer/judge call.

## Authorization

Only the orchestrator/service dispatches extraction for a current permitted run. Analyst corrections go through SPEC-008, never directly overwrite the extraction artifact. No model shell/web/filesystem tools.

## UI states

Loading: Extractor stage and mode. Empty: no accepted source/terms yet. Success: known fields plus citations and explicit gaps. Failure: schema/provider/source error with safe next action. Partial/conflict: candidate values, affected dependencies and evidence request.

## Reliability and stopping

Provider timeout <=45 seconds and remaining active time. One transient retry per operation only if all global reservations permit; one intentional structured repair may be offered within five total attempts and token/cost limits, not an automatic nested loop. Empty/unsupported output can stop with a partial package, never a Reject decision. Record uncertain provider outcomes conservatively.

## Analytics

stage_started/completed/failed; extraction_validated with field/gap/conflict counts; provider_attempt_* and context_prepared events. No raw field values or source quotes in ordinary events.

## Tests and acceptance

- TEST-002-01: Normalize USD thousands/millions while preserving raw text/units/source/period.
- TEST-002-02: Missing versus explicit zero; all required Fact shapes and absent fields represented.
- TEST-002-03: Conflicting amount/rate/debt inputs preserve both refs and pause dependencies; subject/facility/basis mismatch cannot become a trusted borrower input merely because its passage is in the same package. SOURCEFIT-1.0 distinguishes different tiers/value kinds/periods from comparable conflicts; unknown authority/effective scope cannot be resolved by newest upload.
- TEST-002-04: Invalid literals/types/nonfinite numbers/unknown source refs fail validation. INPUT-EDU-1.0 rejects nested/escaped duplicate keys and exact resource/numeric overruns before hydration, without choosing a duplicate or clamping a value.
- TEST-002-05: Document instruction injection cannot expand permissions or erase policy.
- TEST-002-06: Fixture matching, visible live errors, counted repairs, no arithmetic or extra call. Apply PROVIDER-1.0 refusal/empty/truncated/uncertain-response controls and CANON-1.0 exact variant matching.
- TEST-002-07: Complete wire example round-trips to domain Facts; strict integer term, Decimal strings, typed objects/lists, missing and conflicting values preserve sources; unknown keys/wrong basis rejected. Eighteen financial keys remain fixed with reported-EBITDA normalization/reconciliation explicitly deferred. Hydrated KNOWN facts do not imply HUMAN_SUPPORTED; wrong-row/scale/period/entity support is blocked and current scoped support is recorded independently of the wire. CANON-1.0 logical handles map to current IDs, including every original page location; unknown handles or changed semantic dependencies cannot inherit old output.

Targets: >=95% normalized available-field accuracy, 100% critical missing/conflict handling, 100% accepted schema validity. Scenarios E-N01–N05, E-C01–C04, E-A01; model results remain unmeasured.

## Dependencies and implementation boundary

Consumes SPEC-001/006/007; feeds SPEC-003/004/005. Exact schema is specified here but no Pydantic code, model adapter, fixture payload or provider call is created.
