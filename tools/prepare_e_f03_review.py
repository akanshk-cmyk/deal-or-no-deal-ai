"""Explicit source-bound E-F03 Reject fixture authoring; no model or database."""
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from tools.register_e_m01 import register
from deal_or_no_deal_ai.context import fingerprint
from deal_or_no_deal_ai.contracts import Scope, hydrate_narrative, parse_synthesis, wire_json
from deal_or_no_deal_ai.synthesis import prepare_synthesis


def prepare(root, scenario="E-F03"):
    if scenario not in ("E-F03", "E-P01"):
        raise ValueError("APPROVED_SCENARIO_REQUIRED")
    case = register(root, scenario=scenario)
    packet = prepare_synthesis(case)
    record = dict(wire_version="SYN-WIRE-1.0", panel_decision=dict(decision="Reject", confidence=0.82,
        rationale="Documented negative cash available cannot support the proposed annual debt service. Positive EBITDA does not remove the cash shortfall, and no supported repayment remedy is supplied.",
        conditions=[], escalate_to_human=True), observations=[
        dict(panel="FINANCIAL", text="Annual DSCR is -0.50x and interest coverage is -2.00x; supplied EBITDA is positive but does not replace negative cash available.", refs=["calc:DSCR", "calc:CALC-009", "calc:CALC-002", "E-F03:FIN-P2"]),
        dict(panel="COMPLIANCE", text="SYN-ESC-001 remains an Exception requiring separate RiskManager handling and final AuthorizedApprover review.", refs=["policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"]),
        dict(panel="RISK", text="The complete authored score is 45/100 Moderate and requires normal human underwriting; it is not a default probability or a rejection rule.", refs=["panel:RISK"])],
        rationale_refs=["E-F03:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"], condition_links=[], proposed_action=None)
    if scenario == "E-P01":
        record = dict(wire_version="SYN-WIRE-1.0", panel_decision=dict(decision="Conditional Approve", confidence=0.82,
            rationale="Annual DSCR of 1.15x is below the synthetic 1.25x policy limit. Refer for explicit exception handling and condition review; annual financial statements do not cure the repayment shortfall.",
            conditions=["Supply annual financial statements"], escalate_to_human=True), observations=[
            dict(panel="FINANCIAL", text="Annual CFADS of USD 690,000 covers USD 600,000 service at 1.15x, with a 0.10x shortfall against policy.", refs=["calc:DSCR", "E-P01:FIN-P2"]),
            dict(panel="COMPLIANCE", text="SYN-ESC-001 remains an Exception. The documented annual-statements covenant requires separate specialist support; it is not a repayment cure.", refs=["policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001", "E-P01:AGREEMENT-P1"]),
            dict(panel="RISK", text="The complete authored score is 33/100 Moderate and requires human underwriting. It is not a probability of default or an approval rule.", refs=["panel:RISK"])],
            rationale_refs=["E-P01:FIN-P2", "calc:DSCR", "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"],
            condition_links=[dict(index=0, refs=["E-P01:AGREEMENT-P1"])], proposed_action=None)
    wire = parse_synthesis(json.dumps(record))
    uid = lambda name: str(uuid5(NAMESPACE_URL, scenario + "-authoring:" + name))
    scope = Scope(workspace_id=uid("workspace"), deal_id=case.scope.deal_id, review_id=uid("review"), run_id=uid("run"), thread_id=uid("thread"), input_revision=1)
    targets = hydrate_narrative(wire, scope, uid("operation"), {k: scope for k in packet["request"]["reference_dictionary"]},
        dict(input_digest=packet["input_digest"], case=case.dependency_digest))
    rubric = dict(version="E-F03-REJECT-RUBRIC-1.0", evidence_type="EDUCATIONAL_FIXTURE_NOT_LIVE_QUALITY",
        wire_content_digest=fingerprint("E-N01-SYNTHESIS-WIRE", wire.model_dump()),
        narrative_text_digests={t.field_path: t.text_digest for t in targets},
        expected=dict(dscr="-0.50", interest_coverage="-2.00", score="45", band="MODERATE", decision="Reject"),
        limitations=["Case-specific authored judgment, not a universal policy rule", "RiskManager handling does not replace final AuthorizedApprover decision"])
    if scenario == "E-P01":
        rubric.update(version="E-P01-CONDITIONAL-RUBRIC-1.0", expected=dict(dscr="1.15", score="33", band="MODERATE", decision="Conditional Approve"),
            limitations=["Registered source covenant, not a DSCR remedy", "All specialist and final review gates required; condition remains outstanding"])
    raw, rubric_raw = wire_json(wire).encode(), (json.dumps(rubric, indent=2) + "\n").encode()
    registration = dict(version="E-N01-SYNTHESIS-1.0", scenario_id="E-F03", variant="review", mode="FIXTURE",
        case_dependency_digest=case.dependency_digest, package_digest=packet["package_digest"], input_digest=packet["input_digest"],
        wire_sha256=sha256(raw).hexdigest(), rubric_sha256=sha256(rubric_raw).hexdigest(),
        authoring_basis="User approved the fictional source premises and requested RiskManager handling then supported E-F03 Reject integration.",
        semantic_support="AI_AUTHORED_EDUCATIONAL_FIXTURE_NOT_HUMAN_VERIFIED")
    if scenario == "E-P01":
        registration.update(scenario_id=scenario, authoring_basis="User authorized the separate source-backed E-P01 educational review workflow.")
    pack = root / "fixtures/development" / scenario.lower()
    writes = {pack / "synthesis.review.json": raw, pack / "synthesis.review.rubric.json": rubric_raw,
        root / ("config/registrations/" + scenario.lower() + "-review-synthesis.json"): (json.dumps(registration, indent=2) + "\n").encode()}
    for path, content in writes.items():
        if path.exists() and path.read_bytes() != content:
            raise ValueError("EXISTING_REJECT_FIXTURE_DIFFERS")
    for path, content in writes.items():
        if not path.exists():
            path.write_bytes(content)
    return case


if __name__ == "__main__":
    prepare(ROOT)
    print("E-F03 source/Reject fixture prepared; no review or model call executed.")
