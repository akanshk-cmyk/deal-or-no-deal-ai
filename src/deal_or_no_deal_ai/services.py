"""M2 registered synthetic-source adapters; no graph, provider or database startup."""

from dataclasses import asdict, dataclass
from datetime import date, datetime
from hashlib import sha256
from importlib.metadata import version
from io import BytesIO
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator

from .context import InputError, fingerprint, instruction_manifest, strict_json
from .contracts import DealTermsWire, Identifier, StrictModel, Text, parse_extraction
from .documents import OriginalBlock, ReviewScope, SourceVersion, verify_evidence
from .finance import MetricValue, calculate_metrics
from .policy import CompliancePanel, PolicyConfig, evaluate_policy, sample_policy_spec
from .risk import FactorAssessment, RiskPanel, assess_risk


Sha = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]


class CaseRegistration(StrictModel):
    version: Literal["CASE-REG-1.0"]
    scenario_id: Literal["E-N01", "E-M01", "E-F03", "E-P01"]
    approval_basis: Text
    approved_assumption_ids: list[Literal["A1", "A2", "A3", "A4"]]
    approved_at_utc: Text
    evidence_cutoff_at: Text
    review_as_of: Text
    purpose: Literal["CURRENT_REVIEW"]
    source_profile_version: Literal["E-N01-SOURCEFIT-1.0", "E-M01-SOURCEFIT-1.0", "E-F03-SOURCEFIT-1.0", "E-P01-SOURCEFIT-1.0", "E-N01-EXTRACTION-MISS-1.0", "E-N01-CORRECTION-1.0"]
    deal_id: Identifier
    subject_id: Identifier
    facility_id: Identifier
    input_revision: Annotated[int, Field(gt=0)]
    manifest_sha256: Sha
    case_sha256: Sha
    case_semantic_digest: Sha
    extraction_sha256: Sha
    extraction_semantic_digest: Sha
    policy_sha256: Sha
    package_digest: Sha
    parser_version: Literal["6.21.2"]
    expected_pages: dict[str, "RegisteredPage"]
    instruction_hashes: dict[str, Sha]
    mode: Literal["FIXTURE"]
    variant: Literal["default"]
    limitations: list[Text]

    @field_validator("approved_assumption_ids")
    @classmethod
    def all_assumptions(cls, value):
        if len(value) != 4 or set(value) != {"A1", "A2", "A3", "A4"}:
            raise ValueError("ALL_PRESENTED_ASSUMPTIONS_REQUIRED")
        return value

    @field_validator("approved_at_utc", "evidence_cutoff_at")
    @classmethod
    def utc(cls, value):
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
            raise ValueError("UTC_REQUIRED")
        return value

    @field_validator("review_as_of")
    @classmethod
    def iso_date(cls, value):
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError("ISO_DATE_REQUIRED")
        return value


class RegisteredPage(StrictModel):
    source_id: Text
    source_version: Text
    source_sha256: Sha
    page: Annotated[int, Field(gt=0)]
    text_sha256: Sha


CaseRegistration.model_rebuild()


@dataclass(frozen=True)
class RegisteredFixtureCase:
    registration: CaseRegistration
    scope: ReviewScope
    wire: DealTermsWire
    case_data: dict
    inventory: tuple[OriginalBlock, ...]
    dependency_digest: str


@dataclass(frozen=True)
class ReviewedLiveCase(RegisteredFixtureCase):
    """Actual response plus exact human-support receipt binding; not a registration."""
    support_digest: str
    human_verified: bool = True


@dataclass(frozen=True)
class FinancialPanel:
    metric_results: tuple[MetricValue, ...]
    metric_source_refs: tuple[tuple[str, tuple[str, ...]], ...]
    missing_dependencies: tuple[str, ...]
    completeness: str
    dependency_digest: str
    input_facts: tuple[dict, ...]
    scope: ReviewScope
    review_source_basis: dict
    support_basis: str = "REGISTERED_SYNTHETIC_FIXTURE_NOT_LIVE_HUMAN_SUPPORT"
    covenant_status: str = "EXTRACTED_NOT_EVALUATED"
    analysis_scope: str = "Supplied annual projections; full-term/balloon/refinancing NOT_EVALUATED"
    reported_ebitda_reconciliation: str = "DEFERRED"


def _sha(data):
    return sha256(data).hexdigest()


def _binding(registration, scope, wire, data, inventory):
    return fingerprint("REGISTERED_CASE_INPUTS-1.0", dict(
        registration=registration.model_dump(), scope=asdict(scope), wire=wire.model_dump(),
        case=data, inventory=[asdict(block) for block in inventory],
    ))


def _scope(registration):
    return ReviewScope(registration.deal_id, registration.input_revision, registration.subject_id,
                       registration.facility_id, fingerprint("REGISTERED_REVIEW_BASIS", dict(
                           package=registration.package_digest, review_as_of=registration.review_as_of,
                           cutoff=registration.evidence_cutoff_at, profile=registration.source_profile_version,
                           case_metadata=registration.case_semantic_digest, policy=registration.policy_sha256)))


def _expected_basis(field):
    if field == "previous_revenue":
        return "FY-PREV"
    if field in ("existing_funded_debt", "proposed_funded_borrowing", "transaction_debt_repaid",
                 "eligible_equipment_value", "prior_ranking_liens", "secured_facility_exposure",
                 "current_assets", "current_liabilities"):
        return "TXN-1"
    return "FY-ASSESS"


def _validate_inputs(registration, scope, wire, data, inventory, *, registered_extraction=True):
    if registration.version=='UPLOAD-PROFILE-1.0':
        if fingerprint('APPROVED_CASE_METADATA',data)!=registration.case_semantic_digest or scope!=_scope(registration):raise InputError('UPLOADED_PROFILE_BINDING_CHANGED')
        if wire.terms.borrower.value is not None and wire.terms.borrower.value!=data['subject_registry']['subject_label']:raise InputError('UPLOADED_BORROWER_REQUIRES_REVIEW')
        if wire.terms.legal_entity.value is not None and wire.terms.legal_entity.value!=data['subject_registry']['subject_label']:raise InputError('UPLOADED_ENTITY_REQUIRES_REVIEW')
        refs={b.block_id for b in inventory}
        if wire.terms.currency.value not in (None,'USD'):raise InputError('UPLOADED_USD_PROFILE_REQUIRED')
        if wire.financial_inputs.previous_revenue.value is not None and data['bases']['FY-PREV']['kind']=='NOT_PROVIDED':raise InputError('COMPARATIVE_PERIOD_NOT_DECLARED')
        if not refs or len(refs)!=len(inventory) or any(b.scope!=scope for b in inventory):raise InputError('UPLOADED_PAGE_SCOPE_CHANGED')
        for group in ('terms','financial_inputs'):
            for name,fact in getattr(wire,group).__dict__.items():
                if not set(fact.refs)<=refs:raise InputError('FACT_SOURCE_OUT_OF_SCOPE')
                if fact.value is not None and (not fact.refs or group=='financial_inputs' and fact.basis_id!=_expected_basis(name)):raise InputError('UPLOADED_FACT_BASIS_OR_SOURCE_REQUIRED')
        return
    if fingerprint("APPROVED_CASE_METADATA", data) != registration.case_semantic_digest:
        raise InputError("APPROVED_CASE_CONFIGURATION_CHANGED")
    if scope != _scope(registration) or data["scope"] != dict(
        deal_id=scope.deal_id, subject_id=scope.subject_id, facility_id=scope.facility_id
    ):
        raise InputError("CASE_SCOPE_MISMATCH")
    if data["source_basis"]["proposed_review_as_of"] != registration.review_as_of:
        raise InputError("REVIEW_BASIS_MISMATCH")
    observed = datetime.fromisoformat(registration.approved_at_utc.replace("Z", "+00:00"))
    cutoff = datetime.fromisoformat(registration.evidence_cutoff_at.replace("Z", "+00:00"))
    if observed > cutoff:
        raise InputError("SOURCE_AFTER_EVIDENCE_CUTOFF")
    if registered_extraction and fingerprint("APPROVED_EXTRACTION", wire.model_dump()) != registration.extraction_semantic_digest:
        raise InputError("UNREGISTERED_EXTRACTION_VARIANT")
    if wire.terms.borrower.value != data["subject_registry"]["subject_label"] or wire.terms.legal_entity.value != wire.terms.borrower.value:
        raise InputError("SUBJECT_ATTRIBUTION_MISMATCH")
    refs = {block.block_id for block in inventory}
    if refs != set(registration.expected_pages) or len(refs) != len(inventory):
        raise InputError("INCOMPLETE_REGISTERED_PAGE_INVENTORY")
    for block in inventory:
        expected = registration.expected_pages[block.block_id]
        if (block.scope != scope or block.source.source_id != expected.source_id or block.source.version != expected.source_version
                or block.source.content_digest != expected.source_sha256 or block.page != expected.page
                or _sha(block.text.encode()) != expected.text_sha256):
            raise InputError("REGISTERED_PAGE_BINDING_MISMATCH")
    for group_name in ("terms", "financial_inputs"):
        group = getattr(wire, group_name)
        for field, item in group.__dict__.items():
            if not set(item.refs) <= refs:
                raise InputError("FACT_SOURCE_OUT_OF_SCOPE")
            if item.value is None:
                continue
            if group_name == "financial_inputs":
                if item.basis_id != _expected_basis(field):
                    raise InputError("FINANCIAL_PERIOD_BASIS_MISMATCH")
                basis = data["bases"].get(item.basis_id)
                if not basis or basis["currency"] != "USD" or basis["scale"] != "1":
                    raise InputError("FINANCIAL_UNITS_MISMATCH")
                authority = "equipment" if field in ("eligible_equipment_value", "prior_ranking_liens", "secured_facility_exposure") else "financials"
            else:
                authority = "terms"
            if not set(item.refs) <= set(data["source_basis"]["proposed_field_authority"][authority]):
                raise InputError("FIELD_SOURCE_AUTHORITY_MISMATCH")
    sources = tuple(dict.fromkeys(block.source for block in inventory))
    coverage = verify_evidence(scope=scope, sources=sources, inventory=inventory, roots=(),
                               selected=tuple(refs), purpose="FULL_EXTRACTION", max_context_bytes=100000)
    if coverage.status != "COMPLETE":
        raise InputError("REGISTERED_SOURCE_COVERAGE_NOT_COMPLETE")


def load_registered_case(root: Path, *, scenario_id="E-N01", mode="FIXTURE", variant="default", profile="default") -> RegisteredFixtureCase:
    """Only this approved default fixture; unknown edits never inherit its result."""
    if scenario_id not in ("E-N01", "E-M01", "E-F03", "E-P01") or (mode, variant) != ("FIXTURE", "default"):
        raise InputError("REGISTERED_FIXTURE_MODE_OR_VARIANT_UNAVAILABLE")
    if profile not in ("default", "reassessment", "extraction-miss", "correction"):
        raise InputError("REGISTERED_SOURCE_PROFILE_UNAVAILABLE")
    root = root.resolve()
    if scenario_id != "E-N01" and profile != "default":
        raise InputError("MISSING_CASE_CONTINUATION_UNAVAILABLE")
    pack = root / "fixtures/development" / scenario_id.lower()
    registration_path = "config/registrations/" + (scenario_id.lower() + ".json" if profile == "default" else "e-n01-" + profile + ".json")
    registration = CaseRegistration.model_validate(strict_json((root / registration_path).read_bytes()))
    expected_profile = {"extraction-miss": "E-N01-EXTRACTION-MISS-1.0", "correction": "E-N01-CORRECTION-1.0"}.get(profile, scenario_id + "-SOURCEFIT-1.0")
    if registration.scenario_id != scenario_id or registration.source_profile_version != expected_profile:
        raise InputError("REGISTERED_SCENARIO_PROFILE_MISMATCH")
    if registration.input_revision != (1 if profile in ("default", "extraction-miss") else 2):
        raise InputError("REGISTERED_REVISION_PROFILE_MISMATCH")
    files = {name: (pack / name).read_bytes() for name in ("manifest.json", "case.json", "extraction.candidate.json")}
    if profile == "extraction-miss":
        files["extraction.candidate.json"] = (pack / "extraction.miss.json").read_bytes()
    for name, expected in (("manifest.json", registration.manifest_sha256), ("case.json", registration.case_sha256),
                           ("extraction.candidate.json", registration.extraction_sha256)):
        if _sha(files[name]) != expected:
            raise InputError("REGISTERED_METADATA_CHANGED")
    data, manifest = strict_json(files["case.json"]), strict_json(files["manifest.json"])
    if manifest["package_digest"] != registration.package_digest or data["package_digest"] != registration.package_digest:
        raise InputError("PACKAGE_BINDING_MISMATCH")
    policy_raw = (root / "config/sample_policy.json").read_bytes()
    if _sha(policy_raw) != registration.policy_sha256 or strict_json(policy_raw) != sample_policy_spec():
        raise InputError("POLICY_PROFILE_CHANGED")
    if instruction_manifest(root) != registration.instruction_hashes:
        raise InputError("REGISTERED_INSTRUCTION_PROFILE_CHANGED")
    if version("pypdf") != registration.parser_version:
        raise InputError("PARSER_REVERIFICATION_REQUIRED")
    if len(manifest["sources"]) > 3 or manifest["page_count"] > 10 or manifest["byte_count"] > 10000000:
        raise InputError("REGISTERED_PACKAGE_LIMIT")
    scope = _scope(registration)
    from pypdf import PdfReader
    inventory = []
    total_bytes = total_pages = 0
    for item in manifest["sources"]:
        path = (pack / item["path"]).resolve()
        if not path.is_relative_to(pack.resolve()):
            raise InputError("SOURCE_PATH_OUT_OF_SCOPE")
        raw = path.read_bytes()
        total_bytes += len(raw)
        if _sha(raw) != item["content_digest"] or len(raw) != item["byte_count"]:
            raise InputError("REGISTERED_SOURCE_CHANGED")
        reader = PdfReader(BytesIO(raw), strict=True)
        if reader.is_encrypted or len(reader.pages) != item["page_count"]:
            raise InputError("REGISTERED_PARSE_MISMATCH")
        total_pages += len(reader.pages)
        source = SourceVersion(item["source_id"], item["version"], item["content_digest"])
        for number, page in enumerate(reader.pages, 1):
            handles = [key for key, p in manifest["page_handles"].items() if p["source_id"] == item["source_id"] and p["page"] == number]
            if len(handles) != 1:
                raise InputError("REGISTERED_PAGE_MAP_MISMATCH")
            handle = handles[0]
            text = page.extract_text()
            expected_page = registration.expected_pages.get(handle)
            if not expected_page or _sha(text.encode()) != expected_page.text_sha256:
                raise InputError("REGISTERED_PARSED_TEXT_CHANGED")
            inventory.append(OriginalBlock(handle, scope, source, number, 0, text,
                                            dependencies=tuple(data["required_page_dependencies"].get(handle, ())),
                                            parser_verified=True, fit_verified=True))
    if total_bytes != manifest["byte_count"] or total_pages != manifest["page_count"]:
        raise InputError("REGISTERED_PACKAGE_TOTALS_MISMATCH")
    wire = parse_extraction(files["extraction.candidate.json"])
    inventory = tuple(inventory)
    _validate_inputs(registration, scope, wire, data, inventory)
    return RegisteredFixtureCase(registration, scope, wire, data, inventory,
                                 _binding(registration, scope, wire, data, inventory))


def validate_registered_case(case: RegisteredFixtureCase) -> None:
    """Recheck the current registered binding without granting Live support."""
    expected = _binding(case.registration, case.scope, case.wire, case.case_data, case.inventory)
    if isinstance(case, ReviewedLiveCase):
        expected = fingerprint("REVIEWED_LIVE_CASE", dict(inputs=expected, support=case.support_digest,
            **({"verification_policy":"DEMO_DRAFT"} if not case.human_verified else {})))
    if case.dependency_digest != expected:
        raise InputError("STALE_OR_MUTATED_CASE_INPUTS")
    _validate_inputs(case.registration, case.scope, case.wire, case.case_data, case.inventory,
                     registered_extraction=not isinstance(case, ReviewedLiveCase))


def compute_financials(case: RegisteredFixtureCase) -> FinancialPanel:
    validate_registered_case(case)
    values = {name: fact.value for name, fact in case.wire.financial_inputs.__dict__.items()}
    metrics = calculate_metrics(values, secured_equipment=case.case_data["policy_config"]["secured_equipment"])
    metric_refs = tuple((metric.metric_id, tuple(sorted({ref for key in metric.inputs
                        for ref in getattr(case.wire.financial_inputs, key).refs}))) for metric in metrics.values())
    required = {field for a in case.case_data["factor_assessments"] for field in a["material_financial_fields"]}
    missing = tuple(sorted("financial_input:" + field for field in required if values[field] is None))
    complete = not missing and all(metrics[m].validity == "VALID" for m in ("CALC-004", "CALC-005", "CALC-006"))
    facts = tuple(dict(field=name, value=item.value, refs=tuple(item.refs), basis_id=item.basis_id,
                        basis=case.case_data["bases"].get(item.basis_id),
                        provenance=("NEBIUS_RESPONSE_HUMAN_REVIEWED" if case.human_verified else "NEBIUS_DEMO_DRAFT_NOT_HUMAN_VERIFIED") if isinstance(case, ReviewedLiveCase) else "REGISTERED_EXTRACTION_FIXTURE",
                        human_supported=isinstance(case, ReviewedLiveCase) and case.human_verified and item.value is not None)
                  for name, item in case.wire.financial_inputs.__dict__.items())
    return FinancialPanel(tuple(metrics.values()), metric_refs, missing, "COMPLETE" if complete else "PARTIAL",
                          case.dependency_digest, facts, case.scope,
                          dict(review_as_of=case.registration.review_as_of, evidence_cutoff_at=case.registration.evidence_cutoff_at,
                               source_profile_version=case.registration.source_profile_version),
                          support_basis=("LIVE_CURRENT_HUMAN_SUPPORT" if case.human_verified else "AUTOMATED_DEMO_CHECKS_NOT_HUMAN_SUPPORT") if isinstance(case, ReviewedLiveCase) else "REGISTERED_SYNTHETIC_FIXTURE_NOT_LIVE_HUMAN_SUPPORT")


def compute_compliance(case: RegisteredFixtureCase, financial: FinancialPanel) -> CompliancePanel:
    validate_registered_case(case)
    if financial.dependency_digest != case.dependency_digest or financial.scope != case.scope:
        raise InputError("FINANCIAL_HANDOFF_SCOPE_MISMATCH")
    metrics = {m.metric_id: m for m in financial.metric_results}
    cfg = case.case_data["policy_config"]
    return evaluate_policy(metrics, case.wire.terms,
                             config=PolicyConfig(cfg["secured_equipment"], cfg["kyc_fixture_required"], cfg["sanctions_fixture_required"], cfg["basis"]),
                             dependency_digest=case.dependency_digest, metric_source_refs=dict(financial.metric_source_refs),
                             material_financial_ready=financial.completeness == "COMPLETE",
                             term_conflicts=any(c.field_name in ("terms.interest_terms", "terms.term_months") for c in case.wire.conflicts))


def compute_risk(case: RegisteredFixtureCase, financial: FinancialPanel, policy: CompliancePanel) -> RiskPanel:
    validate_registered_case(case)
    if (financial.dependency_digest != case.dependency_digest or policy.dependency_digest != case.dependency_digest
            or financial.scope != case.scope):
        raise InputError("RISK_HANDOFF_SCOPE_MISMATCH")
    metrics = {m.metric_id: m for m in financial.metric_results}
    required_metrics = {"repayment_capacity": ("CALC-004",), "financial_leverage": ("CALC-005",), "collateral_quality": ("CALC-006",)}
    reasons = {
        "repayment_capacity": "Authored assessment supported by supplied annual cash available and debt-service schedule; no ratio-to-grade conversion",
        "financial_leverage": "Authored assessment supported by funded-debt and unadjusted EBITDA components; no automatic rating rule",
        "collateral_quality": "Authored assessment supported by eligible equipment value, secured exposure and explicit prior liens",
        "borrower_credit_profile": "Authored assessment based on the approved fictional payment-current premise; no bureau verification",
        "business_industry_risk": "Authored assessment based on the approved fictional manufacturing/cyclicality premise; no market research or concentration score",
    }
    factors = tuple(FactorAssessment(
        a["factor_id"], a["proposed_rating"], "assessment:" + case.registration.scenario_id + ":" + a["factor_id"], a["version"],
        reasons[a["factor_id"]],
        tuple(sorted(set(a["refs"] + a["material_source_refs"]))), tuple(a["material_financial_fields"]),
        required_metrics.get(a["factor_id"], ()), case.scope, a["as_of"],
    ) for a in case.case_data["factor_assessments"])
    risk = assess_risk(factors=factors, metrics=metrics,
                       financial_values={k: f.value for k, f in case.wire.financial_inputs.__dict__.items()},
                       available_refs=frozenset(b.block_id for b in case.inventory), scope=case.scope,
                       as_of=case.registration.review_as_of, compliance=policy, dependency_digest=case.dependency_digest)
    return risk


def evaluate_panels(case: RegisteredFixtureCase) -> tuple[FinancialPanel, CompliancePanel, RiskPanel]:
    financial = compute_financials(case)
    policy = compute_compliance(case, financial)
    return financial, policy, compute_risk(case, financial, policy)
