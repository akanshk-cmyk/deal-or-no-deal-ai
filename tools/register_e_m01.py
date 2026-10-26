"""Explicit exact-source registration of the approved missing-CFADS fixture."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pypdf import PdfReader
from deal_or_no_deal_ai.context import fingerprint, strict_json
from deal_or_no_deal_ai.contracts import parse_extraction
from deal_or_no_deal_ai.services import load_registered_case


def register(root, *, scenario="E-M01"):
    if scenario not in ("E-M01", "E-F03", "E-P01"):
        raise ValueError("APPROVED_CORE_SCENARIO_REQUIRED")
    pack = root / "fixtures/development" / scenario.lower()
    target = root / "config/registrations" / (scenario.lower() + ".json")
    if target.exists():
        return load_registered_case(root, scenario_id=scenario)
    original = strict_json((root / "config/registrations/e-n01.json").read_bytes())
    candidate = strict_json((pack / "source-manifest.json").read_bytes())
    ids = {name: str(uuid5(NAMESPACE_URL, "educational:" + scenario + ":" + name)) for name in ("deal_id", "subject_id", "facility_id")}
    handles = ("AGREEMENT-P1", "FIN-P1", "FIN-P2", "COLLATERAL-P1", "ASSESSMENT-P2")
    def transform(value):
        if isinstance(value, dict):
            return {transform(k): transform(v) for k, v in value.items()}
        if isinstance(value, list):
            return [transform(v) for v in value]
        if isinstance(value, str):
            if value in handles:
                return scenario + ":" + value
            return value.replace("E-N01", scenario)
        return value
    data = transform(strict_json((root / "fixtures/development/e-n01/case.json").read_bytes()))
    data["scope"] = ids
    data.update(status="REGISTERED_SYNTHETIC_CORE_CASE", registered=True, case_approved=True,
                package_digest=candidate["source_package_digest"], review_status="USER_AUTHORIZED_EDUCATIONAL_CASE")
    for factor in data["factor_assessments"]:
        if factor["factor_id"] == "repayment_capacity":
            factor["proposed_rating"] = None if scenario == "E-M01" else "60" if scenario == "E-P01" else "100"
    sources = []
    for item in candidate["sources"]:
        raw = (pack / item["filename"]).read_bytes()
        if sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("MISSING_CASE_SOURCE_CHANGED")
        sources.append(dict(source_id=item["source_id"], version="CORE-SOURCE-1.0", path=item["filename"],
                            content_digest=item["sha256"], page_count=item["pages"], byte_count=len(raw)))
    pages, expected = {}, {}
    for handle, item in candidate["pages"].items():
        source = next(s for s in sources if s["source_id"] == item["source_id"])
        text = PdfReader(BytesIO((pack / source["path"]).read_bytes()), strict=True).pages[item["page"] - 1].extract_text()
        if sha256(text.encode()).hexdigest() != item["parsed_text_sha256"]:
            raise ValueError("MISSING_CASE_PARSED_SOURCE_CHANGED")
        pages[handle] = dict(source_id=item["source_id"], page=item["page"])
        expected[handle] = dict(source_id=item["source_id"], source_version=source["version"], source_sha256=source["content_digest"],
                                page=item["page"], text_sha256=item["parsed_text_sha256"])
    manifest = dict(scenario_id=scenario, package_digest=candidate["source_package_digest"], sources=sources,
                    page_handles=pages, page_count=5, byte_count=sum(s["byte_count"] for s in sources))
    encode = lambda obj: (json.dumps(obj, indent=2) + "\n").encode()
    case_raw, manifest_raw = encode(data), encode(manifest)
    extraction_raw = (pack / "extraction.candidate.json").read_bytes()
    wire = parse_extraction(extraction_raw)
    stamp = datetime.now(timezone.utc).isoformat()
    registration = deepcopy(original)
    registration.update(scenario_id=scenario, source_profile_version=scenario + "-SOURCEFIT-1.0", **ids,
        approval_basis="User approved synthetic authoring and explicitly instructed implementing the " + scenario + " workflow.",
        approved_at_utc=stamp, evidence_cutoff_at=stamp, input_revision=1,
        manifest_sha256=sha256(manifest_raw).hexdigest(), case_sha256=sha256(case_raw).hexdigest(),
        case_semantic_digest=fingerprint("APPROVED_CASE_METADATA", data), extraction_sha256=sha256(extraction_raw).hexdigest(),
        extraction_semantic_digest=fingerprint("APPROVED_EXTRACTION", wire.model_dump()),
        package_digest=candidate["source_package_digest"], expected_pages=expected,
        limitations=(["Synthetic missing-CFADS example; no complete score, synthesis or final memo", "Information response/continuation unsupported in this slice"] if scenario == "E-M01" else
                     ["Synthetic conditional-review example; annual statements do not cure DSCR", "Separate RiskManager, ComplianceOfficer and AuthorizedApprover gates required"] if scenario == "E-P01" else
                     ["Synthetic supported-Reject example, not a universal rejection rule", "Separate RiskManager handling and AuthorizedApprover required"]))
    writes = {pack / "case.json": case_raw, pack / "manifest.json": manifest_raw, target: encode(registration)}
    for path, raw in writes.items():
        if path.exists() and path.read_bytes() != raw:
            raise ValueError("EXISTING_MISSING_CASE_METADATA_DIFFERS")
    for path, raw in writes.items():
        if not path.exists():
            path.write_bytes(raw)
    return load_registered_case(root, scenario_id=scenario)


if __name__ == "__main__":
    case = register(ROOT)
    print("E-M01 registered; exact five-page source package verified: " + case.dependency_digest)
