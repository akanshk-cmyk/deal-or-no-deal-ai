"""Explicit registered E-N01 deterministic slice; not the full loan graph."""

from dataclasses import asdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.context import primitive
from deal_or_no_deal_ai.policy import aggregate_workflow
from deal_or_no_deal_ai.services import evaluate_panels, load_registered_case


def run(root=ROOT):
    case = load_registered_case(root)
    financial, compliance, risk = evaluate_panels(case)
    evidence_missing = set(financial.missing_dependencies)
    evidence_missing.update(key for key in risk.score.missing if key.startswith(("financial_input:", "assessment_source:")))
    return primitive(dict(
        evidence_type="APPLICATION_TEST", scope="Registered E-N01 deterministic panels; no graph/model execution",
        scenario_id="E-N01", dependency_digest=case.dependency_digest,
        source_profile=case.registration.source_profile_version, review_as_of=case.registration.review_as_of,
        evidence_cutoff_at=case.registration.evidence_cutoff_at, source_pages=len(case.inventory),
        source_assessments_approved=True, fixture_variant="default", financial=asdict(financial),
        source_registry=[dict(ref=b.block_id, source_id=b.source.source_id, source_version=b.source.version,
                              page=b.page, source_sha256=b.source.content_digest) for b in case.inventory],
        compliance=asdict(compliance), risk=asdict(risk),
        assessments=dict(credit_risk=risk.score.total, credit_band=risk.score.band,
                         policy_exceptions=len(compliance.exception_rule_ids), missing_evidence=len(evidence_missing)),
        current_panel_workflow=aggregate_workflow((compliance.workflow, risk.score.workflow)),
        next_stage="SYNTHESIS_NOT_IMPLEMENTED", final_decision=None, final_ready=False,
        model_calls=0, graph_invoked=False, live_human_supported=False,
        qa=dict(false_positive_risk_count=len(risk.risk_flags),
                expected_risk_flags_basis="Approved E-N01 normal-case expectation: no numerical exceptions",
                risk_recall=None, recall_reason="No positive risk labels in this single normal case"),
        limitations=["Only the exact approved E-N01 default stage fixture is registered",
                     "No synthesis, final disposition, memo, graph, UI or provider execution",
                     "Synthetic assumptions are not calibrated risk or verified banking compliance"],
    ))


if __name__ == "__main__":
    report = run()
    destination = ROOT / "var/evaluations/e-n01-deterministic-panels.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(report_file=str(destination.relative_to(ROOT)), assessments=report["assessments"],
                          financial=report["financial"]["completeness"], policy=report["compliance"]["completeness"],
                          next_stage=report["next_stage"], final_ready=report["final_ready"], model_calls=0)))
