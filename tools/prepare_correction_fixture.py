"""Explicit immutable source-backed extraction-miss/corrected fixture registration."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deal_or_no_deal_ai.context import fingerprint, strict_json
from deal_or_no_deal_ai.contracts import parse_extraction
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.synthesis import prepare_synthesis


def prepare(root):
    pack = root / "fixtures/development/e-n01"
    original = strict_json((root / "config/registrations/e-n01.json").read_bytes())
    wire = strict_json((pack / "extraction.candidate.json").read_bytes())
    wire["financial_inputs"]["cash_available_for_debt_service"] = dict(value=None, refs=[], basis_id=None)
    encode = lambda obj: (json.dumps(obj, indent=2) + "\n").encode()
    raw = encode(wire); parsed = parse_extraction(raw)
    miss = {**original, "source_profile_version": "E-N01-EXTRACTION-MISS-1.0",
        "approval_basis": "User-authorized CORRECTION-1.0: deliberate extraction miss over unchanged approved sources.",
        "extraction_sha256": sha256(raw).hexdigest(), "extraction_semantic_digest": fingerprint("APPROVED_EXTRACTION", parsed.model_dump()),
        "limitations": ["Deliberate missing CFADS in fixture response, not missing source evidence or measured model quality"]}
    corrected = {**original, "input_revision": 2, "source_profile_version": "E-N01-CORRECTION-1.0",
        "approval_basis": "User-authorized CORRECTION-1.0: Analyst restores documented CFADS900000 using original FIN-P2/FY-ASSESS; no new facts."}
    writes = {pack / "extraction.miss.json": raw,
        root / "config/registrations/e-n01-extraction-miss.json": encode(miss),
        root / "config/registrations/e-n01-correction.json": encode(corrected)}
    for path, content in writes.items():
        if path.exists() and path.read_bytes() != content:
            raise ValueError("EXISTING_CORRECTION_FIXTURE_DIFFERS")
    for path, content in writes.items():
        if not path.exists():
            path.write_bytes(content)
    case = load_registered_case(root, profile="correction")
    packet = prepare_synthesis(case)
    synthesis = strict_json((root / "config/registrations/e-n01-synthesis.json").read_bytes())
    synthesis.update(case_dependency_digest=case.dependency_digest, input_digest=packet["input_digest"],
        authoring_basis="CORRECTION-1.0: source-backed reviewer correction, not an original model improvement or human approval.")
    path = root / "config/registrations/e-n01-correction-synthesis.json"
    content = encode(synthesis)
    if path.exists() and path.read_bytes() != content:
        raise ValueError("EXISTING_CORRECTION_SYNTHESIS_DIFFERS")
    if not path.exists():
        path.write_bytes(content)
    load_registered_case(root, profile="extraction-miss")
    return case


if __name__ == "__main__":
    prepare(ROOT)
    print("Extraction-miss/corrected profiles registered; no graph/model/database dispatch.")
