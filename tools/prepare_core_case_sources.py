"""Explicit approved synthetic source authoring; no runtime admission or model.

Writes new separate packages only, verifies actual PDF text and preserves existing
bytes. Source preparation is not a completed registered financial walkthrough.
"""

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from pypdf import PdfReader
from tools.prepare_e_n01 import DOCUMENTS, extraction_candidate, pdf_bytes
from deal_or_no_deal_ai.context import InputError, fingerprint
from deal_or_no_deal_ai.contracts import parse_extraction
from deal_or_no_deal_ai.finance import calculate_metrics


CHANGES = {
    "E-P01": {"cash_available_for_debt_service": "690000"},
    "E-M01": {"cash_available_for_debt_service": None},
    "E-F03": {"net_income": "-300000", "interest_expense": "100000", "income_tax_expense": "0",
              "depreciation": "500000", "amortization": "800000", "cash_available_for_debt_service": "-300000"},
}
AUTHORING = "CORE-SOURCE-AUTHORING-1.0"


def sha(raw):
    return sha256(raw).hexdigest()


def prepare(root: Path, destination: Path):
    """No mutation of config/registrations, app DB, approved originals or prompts."""
    base = root / "fixtures/development/e-n01/authoring"
    packets = {}
    for scenario, changes in CHANGES.items():
        wire = deepcopy(extraction_candidate())
        for name, value in changes.items():
            wire["financial_inputs"][name] = (dict(value=None, refs=[], basis_id=None) if value is None
                                             else {**wire["financial_inputs"][name], "value": value})
        for group in (wire["terms"], wire["financial_inputs"]):
            for fact in group.values():
                fact["refs"] = [scenario + ":" + ref for ref in fact["refs"]]
        wire["terms"]["collateral"]["value"] = ["First-ranking charge over " + scenario + "-COLLATERAL-1 equipment pool"]
        manuscripts = {}
        for _, _, pages in DOCUMENTS:
            for handle, filename in pages:
                text = (base / filename).read_text(encoding="utf-8")
                text = text.replace("E-N01", scenario)
                for old in ("AGREEMENT-1", "FINANCIALS-1", "COLLATERAL-1"):
                    text = text.replace(old, scenario + "-" + old)
                if filename == "financials-p1.txt" and scenario == "E-F03":
                    lines = []
                    replacements = {"Net income": "-300000", "Interest expense": "100000", "Income-tax expense": "0", "Depreciation": "500000", "Amortization": "800000"}
                    for line in text.splitlines():
                        match = next((label for label in replacements if line.startswith(label)), None)
                        lines.append(f"{match:<34} Not supplied {replacements[match]:>12}" if match else line)
                    text = "\n".join(lines) + "\n"
                if filename == "financials-p2.txt":
                    text = text.replace("900000", changes["cash_available_for_debt_service"] or "Not supplied")
                    if scenario == "E-F03":
                        text += ("\nAPPROVED FICTIONAL CASH BRIDGE, BEFORE DEBT SERVICE\n"
                                 "EBITDA 1100000 less working-capital cash outflow 800000\n"
                                 "less capital cash outflow 600000 = CFADS -300000.\n"
                                 "No further tax/interest deductions in this supplied bridge.\n")
                if filename == "assessments-p2.txt":
                    if scenario == "E-M01":
                        text = text.replace("Repayment capacity: 20/100.", "Repayment capacity: Not assessed; material CFADS is missing.")
                        text += "\nNo complete composite score is available; do not reweight factors.\n"
                    else:
                        rating = "60" if scenario == "E-P01" else "100"
                        text = text.replace("Repayment capacity: 20/100.", "Repayment capacity: " + rating + "/100.")
                        text += "\nUser-approved fictional authoring assumptions; not a bank rating.\n"
                text = "\n".join("\n".join(textwrap.wrap(line, width=88, replace_whitespace=False)) if len(line) > 88 else line
                                 for line in text.splitlines()) + "\n"
                manuscripts[scenario + ":" + handle] = text
        parse_extraction(json.dumps(wire))
        metrics = calculate_metrics({key: fact["value"] for key, fact in wire["financial_inputs"].items()}, secured_equipment=True)
        raw_files = {}
        sources, blocks = [], {}
        for source_id, filename, pages in DOCUMENTS:
            handles = [scenario + ":" + handle for handle, _ in pages]
            raw = pdf_bytes([manuscripts[handle] for handle in handles])
            raw = raw.replace(b"% E-N01 SYNTHETIC", ("% " + scenario + " SYNTHETIC").encode("ascii"), 1)
            raw_files[filename] = raw
            reader = PdfReader(BytesIO(raw), strict=True)
            if len(reader.pages) != len(handles):
                raise InputError("CORE_SOURCE_PAGE_COUNT_MISMATCH")
            for index, handle in enumerate(handles):
                parsed = reader.pages[index].extract_text()
                expected = "\n".join(line for line in manuscripts[handle].splitlines() if line)
                if parsed != expected:
                    raise InputError("CORE_SOURCE_PARSED_TEXT_MISMATCH")
                blocks[handle] = dict(source_id=scenario + "-" + source_id, page=index + 1,
                    parsed_text_sha256=sha(parsed.encode()), source_sha256=sha(raw))
            sources.append(dict(source_id=scenario + "-" + source_id, filename=filename,
                                sha256=sha(raw), pages=len(handles)))
        factor_ratings = None if scenario == "E-M01" else ["60" if scenario == "E-P01" else "100", "25", "20", "15", "30"]
        total = None if factor_ratings is None else sum(Decimal(a) * Decimal(b) for a, b in zip(factor_ratings, ("0.3", "0.2", "0.2", "0.2", "0.1")))
        metadata = dict(version=AUTHORING, scenario_id=scenario,
            approval_basis="User explicitly approved core-case-authoring-proposal synthetic assessments and cash bridge in this session.",
            status="PARSED_SOURCE_CANDIDATE_NOT_RUNTIME_REGISTERED", registered=False,
            source_review="AUTHOR_SELF_CHECK_NOT_INDEPENDENT_SME_REVIEW", sources=sources, pages=blocks,
            financial_results={key: dict(value=None if item.value is None else str(item.value), display=item.display, validity=item.validity) for key, item in metrics.items()},
            approved_factor_ratings=factor_ratings, expected_score=None if total is None else str(total),
            panel_decision=None, runtime_status="PENDING_CASE_REGISTRATION_REVIEW_GATES_AND_SYNTHESIS_RUBRIC",
            limitations=["Not a graph run or model-quality result", "No complete score for missing CFADS", "Threshold breach is not a general Reject rule"])
        metadata["source_package_digest"] = fingerprint(AUTHORING, sources)
        raw_files["source-manifest.json"] = (json.dumps(metadata, indent=2) + "\n").encode()
        raw_files["extraction.candidate.json"] = (json.dumps(wire, indent=2) + "\n").encode()
        for handle, text in manuscripts.items():
            raw_files["authoring/" + handle.split(":")[-1].lower() + ".txt"] = text.encode()
        packets[scenario] = raw_files
    # Verify every target first; do not partly replace a mismatched existing pack.
    for scenario, files in packets.items():
        for name, raw in files.items():
            path = destination / scenario.lower() / name
            if path.exists() and path.read_bytes() != raw:
                raise InputError("EXISTING_CORE_SOURCE_DIFFERS_PRESERVE_AND_REVIEW")
    for scenario, files in packets.items():
        for name, raw in files.items():
            path = destination / scenario.lower() / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_bytes(raw)
    return {scenario: dict(files=len(files), status="SOURCE_PREPARED_NOT_RUNTIME_REGISTERED") for scenario, files in packets.items()}


if __name__ == "__main__":
    print(json.dumps(prepare(ROOT, ROOT / "fixtures/development"), indent=2))
