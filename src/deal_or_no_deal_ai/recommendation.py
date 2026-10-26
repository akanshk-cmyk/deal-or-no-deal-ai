"""Pure explanation of existing readiness/results; no decision rules or model calls."""
from .readiness import ApprovalReadiness


VERSION = "RECOMMENDATION-1.0"
RECOMMENDATIONS = {
    "Pending Review": "Defer approval pending additional validation.",
    "Additional Information Required": "Request the missing evidence before proceeding.",
    "Exception Review Required": "Refer unresolved exceptions to an authorized specialist.",
    "Recovery Required": "Resolve the processing or evidence-validation failure before decision-making.",
}


def format_recommendation(assessment, *, financial=None, risk=None, human_decision=None, ai_proposal=None):
    """Readiness controls the label; supplied facts only explain that label."""
    a = ApprovalReadiness.model_validate(assessment).model_dump() if assessment else None
    human = human_decision.get("decision") if isinstance(human_decision, dict) else human_decision
    human = human or "Not recorded"
    if a is None:
        return dict(version=VERSION, outcome="Pending Review",
                    recommendation=RECOMMENDATIONS["Pending Review"],
                    rationale=[dict(text="Approval readiness has not been established from the available review records.", refs=[]),
                               dict(text="The absence of a recorded blocker does not establish that all required checks passed.", refs=[])],
                    issues=[dict(text="Current readiness assessment is unavailable.", refs=[])],
                    next_action="Establish the current readiness assessment and complete outstanding checks before authorized human review.",
                    human_decision=human, brief_reason="Approval readiness has not been established.")
    outcome = a["outcome"]
    recommendation = RECOMMENDATIONS.get(outcome)
    if outcome == "Ready for Human Decision":
        proposal = (ai_proposal or {}).get("decision")
        recommendation = {
            "Approve": "Recommend consideration for approval by an authorized credit officer.",
            "Conditional Approve": "Refer the AI-proposed conditional approval and its conditions for authorized human assessment.",
            "Reject": "Refer the AI-proposed rejection for independent assessment by an authorized credit officer.",
        }.get(proposal, "Refer the completed review to an authorized credit officer; no AI proposal is recorded.")
    issues = []
    exception_refs = next((r["evidence_refs"] for r in a["evaluated_requirements"] if r["requirement_id"] == "critical_exceptions" and r["status"] == "EXCEPTION"), [])
    for requirement in a["evaluated_requirements"]:
        if requirement["requirement_id"] not in a["blockers"]:
            continue
        text = requirement["reason"]
        if requirement["requirement_id"] == "evidence" and requirement["status"] == "PENDING":
            text = "Current financial and policy evidence verification remains pending."
        refs = exception_refs if requirement["requirement_id"] == "policy" and requirement["status"] == "EXCEPTION" and exception_refs else requirement["evidence_refs"]
        issues.append(dict(text=text.rstrip(".") + ".", refs=refs))
    rationale = []
    financial = financial or {}
    metrics = financial.get("metric_results", financial.get("metrics", []))
    dscr = next((m for m in metrics if m["metric_id"] == "CALC-004" and m.get("validity") == "VALID" and m.get("display") is not None), None)
    evidence = next((r for r in a["evaluated_requirements"] if r["requirement_id"] == "evidence"), None)
    if dscr:
        verified = evidence and evidence["status"] == "SATISFIED"
        rationale.append(dict(text="The calculated annual debt-service coverage ratio is " + str(dscr["display"]) + "x" +
                             (", with current evidence verification recorded." if verified else "; current evidence verification is not complete."), refs=["calc:DSCR"]))
    score = (risk or {}).get("score", {})
    if score.get("band") and score.get("display") is not None:
        rationale.append(dict(text="The supplied illustrative risk assessment is " + str(score["band"]).replace("_", " ").title() +
                             " (" + str(score["display"]) + "/100); this score does not establish approval eligibility.", refs=["panel:RISK"]))
    primary_refs = next((p["refs"] for p in issues if p["text"].rstrip(".") == a["reason"].rstrip(".")), [])
    rationale.append(dict(text=a["reason"].rstrip(".") + ".", refs=primary_refs))
    conclusion = "Unconditional approval is not supported while the recorded mandatory blockers remain unresolved."
    if a["approval_eligible"]:
        conclusion = "The completed case still requires an authorized human credit decision." if human == "Not recorded" else "The recorded human decision is separate from this recommendation and remains unchanged."
    rationale.append(dict(text=conclusion, refs=[]))
    return dict(version=VERSION, outcome=outcome, recommendation=recommendation, rationale=rationale,
                issues=issues, next_action=" ".join(dict.fromkeys(a["permitted_next_actions"])),
                human_decision=human, brief_reason=a["reason"].rstrip(".") + ".")


def from_run(run):
    artifacts = run.get("artifacts", {})
    return format_recommendation(run.get("approval_readiness"),
        financial=artifacts.get("financial_analyst", {}).get("payload"),
        risk=artifacts.get("risk_quantifier", {}).get("payload"),
        human_decision=run.get("human_decision") or run.get("human_disposition"),
        ai_proposal=run.get("ai_proposal"))


def markdown(recommendation, *, escape=str, cite=lambda refs: ""):
    """Same narrative for a memo; caller supplies its existing escaping/citations."""
    r = recommendation
    result = "### AI Recommendation\n\n**Recommended AI Outcome:** " + escape(r["outcome"])
    result += "\n\n**Recommendation:** " + escape(r["recommendation"])
    result += "\n\n**Supporting Rationale:**\n\n" + " ".join(escape(p["text"]) + (" " + cite(p["refs"]) if p["refs"] else "") for p in r["rationale"])
    if r["issues"]:
        result += "\n\n**Outstanding Issues:**\n\n" + "\n".join("- " + escape(p["text"]) + (" " + cite(p["refs"]) if p["refs"] else "") for p in r["issues"])
    result += "\n\n**Required Next Action:** " + escape(r["next_action"])
    result += "\n\n**Human Decision:** " + escape(r["human_decision"])
    return result
