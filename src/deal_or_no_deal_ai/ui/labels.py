"""Presentation-only labels; stored codes and permissions remain unchanged."""
LABELS = {
    "HUMAN_SUPPORTED": "Evidence verified by reviewer",
    "UNSUPPORTED": "Evidence does not support this value",
    "WITHHELD": "Verification on hold", "PENDING": "Awaiting review",
    "ANNUAL_ACTUAL": "Actual annual figures", "ANNUAL_PROJECTION": "Forecast annual figures",
    "cash_available_for_debt_service": "Cash available for debt service (CFADS)",
    "annual_principal_payments": "Annual principal repayments",
    "annual_interest_payments": "Annual interest payments",
    "stage_started": "Step started", "stage_completed": "Step completed",
    "artifact_reused": "Previous result reused", "reviewer_correction_applied": "Reviewer correction applied",
    "SUPPORT": "Evidence review", "PROPOSE": "Value proposed",
    "reference": "Correct source and page", "row_label": "Correct financial row",
    "value": "Number matches the source", "units_scale": "Correct units and scale",
    "period": "Correct reporting period", "subject_facility": "Correct borrower and loan",
    "debt_service_scope": "Correct repayments included",
    "WAITING_CONFIGURATION": "Waiting for AI setup verification",
    "WAITING_EVIDENCE": "Waiting for evidence verification", "WAITING_REVIEW": "Waiting for a credit decision",
    "fact_review": "Extracted facts review", "evidence_review": "AI conclusions review",
    "FINANCIAL_RISK": "Financial and risk review", "POLICY_CONTROL": "Policy and compliance review",
    "READY": "Ready to review", "RUNNING": "Review in progress", "COMPLETED": "Review completed",
    "WAITING_INFORMATION": "Waiting for additional information", "AWAITING_REVIEW": "Awaiting reviewer decision",
    "RECOVERY_REQUIRED": "Technical assistance required", "CONTINUE": "Continue review",
    "NOT_TRIGGERED": "No additional action required", "NOT_ASSESSED": "Not assessed",
    "VALID": "Calculation available", "MISSING": "Information missing",
    "RiskManager": "Risk Manager", "ComplianceOfficer": "Compliance Officer",
    "AuthorizedApprover": "Authorized Approver", "Administrator": "Administrator", "Analyst": "Analyst",
}

def friendly(value):
    if value is None:
        return "Not available"
    text = str(value)
    return LABELS.get(text, text.replace("_", " ").capitalize() if text.isupper() and "_" in text else text)

FINANCIAL_HELP = "DSCR compares cash available with scheduled loan repayments. EBITDA is earnings before interest, tax, depreciation and amortization. Collateral is an asset pledged to support a loan. Covenants are conditions the borrower must follow. LTV compares the loan amount with collateral value."


CASE_NAMES = {"E-N01": "Standard Deal", "E-M01": "Missing Information", "E-P01": "Policy Exception", "E-F03": "Rejection Example"}


def case_label(value):
    """Display names only; internal identifiers and citation callbacks stay exact."""
    text = str(value)
    for code, name in CASE_NAMES.items():
        text = text.replace(code, name)
    return text
