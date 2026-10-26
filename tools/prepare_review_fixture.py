"""Explicit authoring of FIN-REVIEW-1.0; no source edits, database or provider."""
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    from deal_or_no_deal_ai.context import fingerprint, strict_json
    from deal_or_no_deal_ai.contracts import parse_synthesis, wire_json
    pack = ROOT / "fixtures/development/e-n01"
    original = parse_synthesis((pack / "synthesis.default.json").read_bytes())
    decision = original.panel_decision.model_copy(update={"confidence": Decimal("0.65"), "escalate_to_human": True})
    reviewed = original.model_copy(update={"panel_decision": decision})
    raw = wire_json(reviewed).encode("utf-8")
    rubric = strict_json((pack / "synthesis.rubric.json").read_bytes())
    basis = "User authorized the implementation order; separate synthetic confidence0.65 review variant over unchanged approved E-N01 sources. Not a measured model result."
    rubric.update(authoring_basis=basis, wire_content_digest=fingerprint("E-N01-SYNTHESIS-WIRE", reviewed.model_dump()))
    rubric["limitations"] = ["Synthetic confidence0.65 tests existing SYN-ESC-012 only.",
                             "No new financial premises, semantic support or actual lending authority."]
    rubric_raw = (json.dumps(rubric, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    registration = strict_json((ROOT / "config/registrations/e-n01-synthesis.json").read_bytes())
    registration.update(variant="review", wire_sha256=sha256(raw).hexdigest(),
                        rubric_sha256=sha256(rubric_raw).hexdigest(), authoring_basis=basis)
    writes = {pack / "synthesis.review.json": raw, pack / "synthesis.review.rubric.json": rubric_raw,
              ROOT / "config/registrations/e-n01-review-synthesis.json": (json.dumps(registration, indent=2) + "\n").encode()}
    for path, content in writes.items():
        if path.exists() and path.read_bytes() != content:
            raise ValueError("EXISTING_REVIEW_FIXTURE_DIFFERS")
    for path, content in writes.items():
        if not path.exists():
            path.write_bytes(content)
        print(path.relative_to(ROOT))
    from deal_or_no_deal_ai.services import load_registered_case
    from deal_or_no_deal_ai.synthesis import prepare_synthesis
    revision_registration = strict_json((ROOT / "config/registrations/e-n01.json").read_bytes())
    revision_registration.update(input_revision=2, approval_basis="User-authorized FIN-REASSESS-1.0: reassess unchanged registered evidence after a scoped RiskManager response assessment.")
    revision_path = ROOT / "config/registrations/e-n01-reassessment.json"
    revision_raw = (json.dumps(revision_registration, indent=2) + "\n").encode()
    if revision_path.exists() and revision_path.read_bytes() != revision_raw:
        raise ValueError("EXISTING_REVISION_REGISTRATION_DIFFERS")
    if not revision_path.exists():
        revision_path.write_bytes(revision_raw)
    revised = load_registered_case(ROOT, profile="reassessment")
    revised_packet = prepare_synthesis(revised)
    revised_synthesis = {**registration, "case_dependency_digest": revised.dependency_digest,
                          "package_digest": revised_packet["package_digest"], "input_digest": revised_packet["input_digest"],
                          "authoring_basis": "FIN-REASSESS-1.0: confidence0.65 remains review-required; no inferred model improvement."}
    revision_synthesis_path = ROOT / "config/registrations/e-n01-reassessment-review-synthesis.json"
    revision_synthesis_raw = (json.dumps(revised_synthesis, indent=2) + "\n").encode()
    if revision_synthesis_path.exists() and revision_synthesis_path.read_bytes() != revision_synthesis_raw:
        raise ValueError("EXISTING_REVISION_SYNTHESIS_DIFFERS")
    if not revision_synthesis_path.exists():
        revision_synthesis_path.write_bytes(revision_synthesis_raw)
    print("Registered revision2 reuses verified sources; financial values unchanged.")


if __name__ == "__main__":
    main()
