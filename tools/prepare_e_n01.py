"""Fixed E-N01 authoring utility. No PDF parsing, registration or model calls."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "fixtures/development/e-n01"
DRAFT_VERSION = "2-draft"  # Explicit font encoding fix; original files retained under history/1-draft.
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.context import canonical_json, fingerprint
from deal_or_no_deal_ai.contracts import parse_extraction


DOCUMENTS = (
    ("AGREEMENT-1", "agreement.pdf", (("AGREEMENT-P1", "agreement-p1.txt"),)),
    ("FINANCIALS-1", "financials.pdf", (("FIN-P1", "financials-p1.txt"), ("FIN-P2", "financials-p2.txt"))),
    ("COLLATERAL-1", "collateral-and-assessments.pdf", (("COLLATERAL-P1", "collateral-p1.txt"),
                                                       ("ASSESSMENT-P2", "assessments-p2.txt"))),
)
FINANCIAL = {
    "net_income": "700000", "interest_expense": "100000", "income_tax_expense": "100000",
    "depreciation": "100000", "amortization": "100000", "cash_available_for_debt_service": "900000",
    "annual_principal_payments": "500000", "annual_interest_payments": "100000",
    "existing_funded_debt": "2400000", "proposed_funded_borrowing": "1200000",
    "transaction_debt_repaid": "300000", "eligible_equipment_value": "2000000",
    "prior_ranking_liens": "0", "secured_facility_exposure": "1200000", "current_revenue": "4400000",
    "previous_revenue": "4000000", "current_assets": "1500000", "current_liabilities": "750000",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pdf_bytes(pages):
    """Write only known ASCII manuscripts with a fixed monospaced layout."""
    objects = [b"", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>"]
    kids = []
    for text in pages:
        lines = text.splitlines()
        if len(lines) > 49 or any(len(line) > 88 for line in lines):
            raise ValueError("Authoring page exceeds fixed visible bounds; edit manuscript explicitly")
        commands = ["BT /F1 10 Tf 14 TL 36 756 Td"]
        for index, line in enumerate(lines):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(("T* " if index else "") + f"({escaped}) Tj")
        commands.append("ET")
        stream = ("\n".join(commands) + "\n").encode("ascii")
        page_id = len(objects) + 1
        kids.append(f"{page_id} 0 R")
        objects.append((f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                        f"/Resources << /Font << /F1 3 0 R >> >> /Contents {page_id + 1} 0 R >>").encode())
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"endstream")
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[1] = f"<< /Type /Pages /Count {len(pages)} /Kids [{' '.join(kids)}] >>".encode()
    result = bytearray(b"%PDF-1.4\n% E-N01 SYNTHETIC AUTHORING DRAFT\n")
    offsets = [0]
    for index, item in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{index} 0 obj\n".encode() + item + b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010} 00000 n \n".encode())
    result.extend((f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n").encode())
    return bytes(result)


def fact(value, ref="AGREEMENT-P1", basis=None):
    return dict(value=value, refs=[ref], basis_id=basis)


def extraction_candidate():
    terms = {k: fact(v) for k, v in dict(
        borrower="Example Equipment LLC", legal_entity="Example Equipment LLC", facility_type="TERM_LOAN",
        requested_amount="1200000", currency="USD", term_months=48, maturity_date="2030-10-23",
        interest_terms=dict(kind="FIXED", annual_rate_percent="6", index=None, spread_bps=None,
                            reset_frequency=None, floor_percent=None),
        repayment_structure="Principal and interest per supplied annual forecast schedule; full-term adequacy not assessed",
        collateral=["First-ranking charge over COLLATERAL-1 equipment pool"], guarantees=[],
        covenants=["Supply annual financial statements"],
        use_of_proceeds="USD 900000 equipment purchase and USD 300000 repayment of existing funded debt",
    ).items()}
    inputs = {}
    for name, value in FINANCIAL.items():
        if name in ("eligible_equipment_value", "prior_ranking_liens", "secured_facility_exposure"):
            ref, basis = "COLLATERAL-P1", "TXN-1"
        elif name in ("existing_funded_debt", "proposed_funded_borrowing", "transaction_debt_repaid",
                      "current_assets", "current_liabilities"):
            ref, basis = "FIN-P2", "TXN-1"
        elif name in ("cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments"):
            ref, basis = "FIN-P2", "FY-ASSESS"
        else:
            ref, basis = "FIN-P1", "FY-PREV" if name == "previous_revenue" else "FY-ASSESS"
        inputs[name] = fact(value, ref, basis)
    wire = dict(terms=terms, financial_inputs=inputs, conflicts=[])
    parse_extraction(canonical_json(wire))
    return wire


def artifacts():
    output = {}
    manifest_sources, handles = [], {}
    for source_id, filename, page_specs in DOCUMENTS:
        pages = [(PACK / "authoring" / name).read_text(encoding="utf-8") for _, name in page_specs]
        generated = pdf_bytes(pages)
        relative = "sources/" + filename
        output[relative] = generated
        source = dict(source_id=source_id, version=DRAFT_VERSION, path=relative, content_digest=digest(generated),
                      page_count=len(pages), byte_count=len(generated), parser_verified=False,
                      source_fit_verified=False, knowledge_available_at=None, ingested_at=None)
        manifest_sources.append(source)
        for number, ((handle, manuscript), text) in enumerate(zip(page_specs, pages), 1):
            paragraphs, cursor = [], 0
            for chunk in text.split("\n\n"):
                # Offsets describe authored page text, not a PDF parser's output.
                paragraphs.append(dict(block_id=f"{handle}-B{len(paragraphs) + 1:02}",
                                       start=cursor, end=cursor + len(chunk), text=chunk))
                cursor += len(chunk) + 2
            handles[handle] = dict(source_id=source_id, version=DRAFT_VERSION, page=number,
                                   manuscript="authoring/" + manuscript, manuscript_sha256=digest(text.encode()),
                                   paragraphs=paragraphs, location_kind="AUTHORING_MAP_NOT_PARSER_OUTPUT",
                                   parser_verified=False, source_fit_verified=False)
    manifest = dict(scenario_id="E-N01", status="AUTHORING_DRAFT", registered=False, case_approved=False,
                    sources=manifest_sources, page_handles=handles, page_count=sum(s["page_count"] for s in manifest_sources),
                    byte_count=sum(s["byte_count"] for s in manifest_sources))
    manifest["package_digest"] = fingerprint("E-N01-SOURCE-CANDIDATE-1.0", manifest_sources)
    material = {
        "repayment_capacity": ["cash_available_for_debt_service", "annual_principal_payments", "annual_interest_payments"],
        "financial_leverage": ["existing_funded_debt", "proposed_funded_borrowing", "transaction_debt_repaid",
                               "net_income", "interest_expense", "income_tax_expense", "depreciation", "amortization"],
        "collateral_quality": ["eligible_equipment_value", "prior_ranking_liens", "secured_facility_exposure"],
        "borrower_credit_profile": [], "business_industry_risk": [],
    }
    case = dict(
        scenario_id="E-N01", version=DRAFT_VERSION, status="AUTHORING_DRAFT", registered=False, case_approved=False,
        package_digest=manifest["package_digest"], author="AI-assisted fixture preparation",
        human_reviewer=None, review_status="PENDING", approved_assumption_ids=[],
        proposed_assumption_ids=["A1", "A2", "A3", "A4"], mode="FIXTURE_CANDIDATE_NOT_EXECUTABLE",
        scope={k: str(uuid5(NAMESPACE_URL, "deal-or-no-deal:e-n01:" + k))
               for k in ("deal_id", "subject_id", "facility_id")},
        source_basis=dict(proposed_review_as_of="2026-10-23", evidence_cutoff_at=None,
                          profile_id="E-N01-SOURCEFIT-DRAFT", profile_approved=False,
                          proposed_field_authority={"terms": ["AGREEMENT-P1"],
                                                    "financials": ["FIN-P1", "FIN-P2"],
                                                    "equipment": ["COLLATERAL-P1"],
                                                    "authored_assessments": ["ASSESSMENT-P2"]}),
        bases={"FY-ASSESS": dict(kind="SUPPLIED_ANNUAL_PROJECTION", start="2027-01-01", end="2027-12-31", currency="USD", scale="1"),
               "FY-PREV": dict(kind="SUPPLIED_COMPARABLE_ANNUAL_PROJECTION", start="2026-01-01", end="2026-12-31", currency="USD", scale="1"),
               "TXN-1": dict(kind="SUPPLIED_PRO_FORMA_TRANSACTION", as_of="2026-10-23", currency="USD", scale="1")},
        policy_config=dict(version="E-N01-APPLICABILITY-DRAFT", policy_pack="SAMPLE-LOAN-POLICY-1.0",
                           secured_equipment=True, kyc_fixture_required=False, sanctions_fixture_required=False,
                           basis="Fictional teaching case only; not a legal exemption", approved=False),
        subject_registry=dict(subject_label="Example Equipment LLC", role="BORROWER_STANDALONE",
                              facility_reference="E-N01-FACILITY", page_handles=list(handles), approved=False),
        required_page_dependencies={"FIN-P1": ["FIN-P2"], "FIN-P2": ["FIN-P1", "COLLATERAL-P1"]},
        factor_assessments=[dict(factor_id=name, proposed_rating=rating, status="PROPOSED_NOT_USABLE",
                                 attribution="AI_ASSISTED_CASE_AUTHOR_DRAFT", version="1-draft",
                                 as_of="2026-10-23", refs=["ASSESSMENT-P2"],
                                 material_financial_fields=material[name],
                                 material_source_refs=(["FIN-P1", "FIN-P2"] if name in ("repayment_capacity", "financial_leverage")
                                                       else ["COLLATERAL-P1"] if name == "collateral_quality" else ["ASSESSMENT-P2"]))
                            for name, rating in zip(material, ("20", "25", "20", "15", "30"))],
        limitations=["No registered extraction/synthesis variant", "No current-input fixture matching yet",
                     "No HUMAN_SUPPORTED records", "No parser fidelity or source applicability verification"],
    )
    output.update({"manifest.json": (json.dumps(manifest, indent=2) + "\n").encode(),
                   "case.json": (json.dumps(case, indent=2) + "\n").encode(),
                   "extraction.candidate.json": (json.dumps(extraction_candidate(), indent=2) + "\n").encode()})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = artifacts()
    # Validate all existing files first, before creating any new artifacts.
    for name, content in expected.items():
        target = PACK / name
        if target.exists() and target.read_bytes() != content:
            raise SystemExit(f"Changed generated artifact needs explicit review: {name}")
        if args.check and not target.exists():
            raise SystemExit(f"Missing generated artifact: {name}")
    if args.write:
        for name, content in expected.items():
            target = PACK / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(content)
    print(json.dumps(dict(status="AUTHORING_DRAFT_NOT_REGISTERED", artifacts=len(expected),
                          generated_pdf_count=3, authored_page_count=5, parser_executed=False,
                          checked=True, wrote_missing=args.write)))


if __name__ == "__main__":
    main()
