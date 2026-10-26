"""Pure seven-section renderer for the registered normal Fixture slice."""

from dataclasses import dataclass
from datetime import datetime
from html import escape
import re

from .context import InputError, fingerprint
from .contracts import Scope, parse_synthesis


SECTIONS = ("Executive Summary", "Compliance", "Financial Analysis", "Risk Scores", "Decision", "Conditions", "Audit Log")
RENDERER_VERSION = "E-N01-MEMO-1.1"
METRIC_LABELS = {"CALC-001": "EBIT", "CALC-002": "EBITDA", "CALC-003": "Post-loan funded debt",
                 "CALC-004": "DSCR", "CALC-005": "Debt / EBITDA", "CALC-006": "Equipment LTV",
                 "CALC-007": "Revenue growth", "CALC-008": "Current ratio", "CALC-009": "Interest coverage"}


def inert(value) -> str:
    return re.sub(r'([\\`*_{}\[\]()#+.!|>~\-])', r'\\\1', escape(str(value), quote=False))


def citation_anchor(handle: str) -> str:
    return "cite-" + fingerprint("MEMO-CITATION", handle)[:16]


@dataclass(frozen=True)
class ReportInput:
    scope: Scope
    packet: dict
    synthesis: dict
    events: tuple[dict, ...]
    generation_time: str
    human_review: dict | None = None
    source_correction: dict | None = None
    approval_readiness: dict | None = None


def render_memo(data: ReportInput) -> dict:
    """Copy recorded data only; no calculations, clocks, lookup, writes or inference."""
    packet, synthesis = data.packet, data.synthesis
    request = packet["request"]
    if (packet["input_digest"] != fingerprint("E-N01-SYNTHESIS-INPUT-1.0", {k: v for k, v in packet.items() if k != "input_digest"})
            or synthesis["input_digest"] != packet["input_digest"]
            or synthesis["case_dependency_digest"] != packet["case_dependency_digest"]
            or data.scope.deal_id != request["scope"]["deal_id"]
            or data.scope.input_revision != request["scope"]["revision"]):
        raise InputError("REPORT_INPUT_SCOPE_OR_DIGEST_MISMATCH")
    wire = parse_synthesis(synthesis["wire_json"])
    if synthesis["wire_digest"] != fingerprint("E-N01-SYNTHESIS-WIRE", wire.model_dump()):
        raise InputError("REPORT_SYNTHESIS_CHANGED")
    reviewed = data.human_review is not None
    conditional_review = reviewed and request["review_basis"]["source_profile"] == "E-P01-SOURCEFIT-1.0"
    exception_review = reviewed and request["review_basis"]["source_profile"] in ("E-F03-SOURCEFIT-1.0", "E-P01-SOURCEFIT-1.0")
    renderer_version = "E-N01-REVIEW-MEMO-1.0" if reviewed else RENDERER_VERSION
    if (synthesis["evidence_status"] != "FIXTURE_EXPECTATION_CHECKED_NOT_HUMAN_SUPPORTED"
            or synthesis["routing"]["workflow"] != ("ESCALATE" if exception_review else "REVIEW_REQUIRED" if reviewed else "CONTINUE")
            or synthesis["routing"]["human_disposition"] is not None
            or wire.panel_decision.escalate_to_human != reviewed
            or request["risk"]["score"]["workflow"] != ("REVIEW_REQUIRED" if exception_review else "CONTINUE")
            or any(row["workflow"] != "CONTINUE" and not (exception_review and row["ref"] == "policy:SAMPLE-LOAN-POLICY-1.0:SYN-ESC-001"
                and row["result"] == "Exception" and row["workflow"] == "ESCALATE") for row in request["compliance"]["rules"])):
        raise InputError("REPORT_REQUIRES_CURRENT_NORMAL_FIXTURE_GATES")
    if reviewed:
        from .financial_review import validate_human_record
        validate_human_record(data.human_review, data.scope)
        if data.human_review["event"]["analysis_snapshot"]["ai"] != synthesis:
            raise InputError("REPORT_HUMAN_ANALYTICAL_SNAPSHOT_MISMATCH")
        if exception_review and (wire.panel_decision.decision != ("Conditional Approve" if conditional_review else "Reject") or data.human_review["event"]["decision"] not in (("Conditional Approve", "Reject") if conditional_review else ("Reject",))
                or request["risk"]["score"]["band"] != "MODERATE"
                or synthesis["routing"]["final_policy"]["exception_rule_ids"] != ["SYN-ESC-001"]
                or len(data.human_review.get("exception_events", [])) != 1):
            raise InputError("REPORT_SUPPORTED_REJECT_HANDLING_REQUIRED")
        final_rules = synthesis["routing"]["final_policy"]["rules"]
        if any(r["workflow"] != "CONTINUE" and not (r["rule_id"] == "SYN-ESC-012"
                and r["authority"] == "DEMO_PRODUCT_CONTROL" and r["workflow"] == "REVIEW_REQUIRED")
                and not (exception_review and r["rule_id"] == "SYN-ESC-001" and r["authority"] == "INTERNAL_SAMPLE_POLICY"
                         and r["outcome"] == "Exception" and r["workflow"] == "ESCALATE") for r in final_rules):
            raise InputError("REPORT_UNHANDLED_POLICY_GATE")
    if data.approval_readiness is not None:
        renderer_version += "/READINESS-1.0/RECOMMENDATION-1.0"
    stamp = datetime.fromisoformat(data.generation_time.replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise InputError("REPORT_EXPLICIT_UTC_TIME_REQUIRED")
    if [event["sequence"] for event in data.events] != list(range(1, len(data.events) + 1)):
        raise InputError("REPORT_EVENT_SEQUENCE_GAP")
    if any(event["run_id"] != data.scope.run_id for event in data.events):
        raise InputError("REPORT_EVENT_SCOPE_MISMATCH")
    cutoff = len(data.events)
    if any(e["stage"] == "report_generator" and e["event"] == "stage_completed" for e in data.events):
        raise InputError("REPORT_CANNOT_CONTAIN_OWN_FUTURE_COMPLETION")
    refs = dict(request["reference_dictionary"])
    # The request retains pre-synthesis confidence=Not evaluated. The generated
    # memo cites the recorded final evaluation without rewriting that request.
    for rule in synthesis["routing"]["final_policy"]["rules"]:
        handle = f"policy:{rule['policy_version']}:{rule['rule_id']}"
        refs[handle] = {**refs[handle], "value": rule,
                        "refs": [ref for ref in rule["source_refs"] if ref != handle]}
    def cite(handle):
        if handle not in refs:
            raise InputError("REPORT_REFERENCE_OUT_OF_SCOPE")
        return f'[{inert(refs[handle]["label"])}](#{citation_anchor(handle)})'
    def cites(handles):
        return " · ".join(cite(handle) for handle in handles)
    terms = request["terms"]
    correction = data.source_correction
    corrected_profile = request["review_basis"]["source_profile"] == "E-N01-CORRECTION-1.0"
    if corrected_profile != (correction is not None):
        raise InputError("REPORT_CORRECTION_PROVENANCE_REQUIRED")
    if correction is not None:
        from uuid import UUID, uuid5
        if (correction.get("action") != "SOURCE_CORRECTION_SAVED" or correction.get("reviewer_role") != "Analyst"
            or not correction.get("comments", "").strip() or correction.get("field") != "cash_available_for_debt_service"
            or correction.get("corrected_fact") != dict(value="900000", refs=["FIN-P2"], basis_id="FY-ASSESS")
            or correction.get("old_fact") != dict(value=None, refs=[], basis_id=None)
            or correction.get("scope", {}).get("deal_id") != data.scope.deal_id
            or correction["scope"].get("workspace_id") != data.scope.workspace_id
            or correction["scope"].get("review_id") != data.scope.review_id
            or correction["scope"].get("input_revision") != 1 or data.scope.input_revision != 2
            or str(uuid5(UUID(correction["new_operation"]), "run")) != data.scope.run_id
            or correction.get("evidence_refs") != ["FIN-P2"] or "FIN-P2" not in refs):
            raise InputError("REPORT_CORRECTION_EVIDENCE_MISMATCH")
    title = "# Deal or No Deal AI — Educational Credit Memo\n\n"
    title += "**Fixture demonstration. Canned stage response; no live AI inference or real credit approval.**\n\n"
    title += f"Run: {inert(data.scope.run_id)} · Revision: {data.scope.input_revision} · Generated: {inert(data.generation_time)}\n\n"
    parts = []
    summary = f"Borrower: {inert(terms['borrower']['value'])}. {cites(terms['borrower']['refs'])}\n\n"
    if correction is not None:
        summary += "Reviewer-corrected extraction; this is not the original model response. CFADS was originally missing and restored from the existing source. " + cite("FIN-P2") + "\n\n"
    for name, label in (("facility_type", "Facility"), ("requested_amount", "Requested amount"), ("currency", "Currency"),
                        ("term_months", "Term in months"), ("maturity_date", "Maturity date"),
                        ("repayment_structure", "Repayment structure"), ("use_of_proceeds", "Use of proceeds"),
                        ("collateral", "Collateral"), ("guarantees", "Guarantees")):
        value = terms[name]["value"]
        if type(value) is list:
            value = "; ".join(value) if value else "Explicitly none documented"
        summary += f"- {label}: {inert(value)}. {cites(terms[name]['refs'])}\n"
    interest = terms["interest_terms"]
    rate = interest["value"]
    interest_label = (f"Fixed annual rate {rate['annual_rate_percent']}%" if rate["kind"] == "FIXED"
                      else f"Floating rate: {rate['index']}, spread {rate['spread_bps']} basis points")
    summary += f"- Interest terms: {inert(interest_label)}. {cites(interest['refs'])}\n"
    summary += "\n" + "\n\n".join(inert(item.text) + " " + cites(item.refs) for item in wire.observations)
    parts.append(summary)
    final_rules = synthesis["routing"]["final_policy"]["rules"]
    policy_exception_count = len(synthesis["routing"]["final_policy"]["exception_rule_ids"])
    missing_material_count = len(request["risk"]["score"]["missing"])
    compliance = "Fictional policy pack: " + inert(request["compliance"]["policy_version"]) + ".\n\n"
    for rule in final_rules:
        handle = f"policy:{rule['policy_version']}:{rule['rule_id']}"
        result = rule["outcome"] if rule["outcome"] is not None else rule["control_result"]
        matched = "Yes" if rule["condition_result"] is True else "No" if rule["condition_result"] is False else "Not evaluated"
        observed = rule["observed"] if rule["observed"] is not None else "Not a numeric check"
        compliance += (f"- {inert(rule['rule_id'])}: {inert(result)}; {inert(rule['applicability'])}; observed {inert(observed)}. "
                       f"Exception/referral trigger: {inert(rule['predicate'])}; matched: {matched}. {cite(handle)}\n")
    compliance += f"\nPolicy exceptions: {policy_exception_count}. Sample-policy results are not legal clearance or covenant compliance."
    if exception_review:
        for event in data.human_review["exception_events"]:
            compliance += ("\n\nException handling: DISPOSITIONED / " + inert(event["handling"]) + "; " + inert(event["rule_id"])
                + ". Original policy outcome remains Exception.\n\nReason: " + inert(event["comments"])
                + "\n\nReviewer: " + inert(event["reviewer_name"]) + "; UTC: " + inert(event["timestamp_utc"])
                + "; receipt: " + inert(event["operation_id"]) + ". " + cites(event["evidence_refs"]))
    parts.append(compliance)
    financial = f"Review as of {inert(request['review_basis']['review_as_of'])}; evidence cutoff {inert(request['review_basis']['cutoff'])}.\n\n"
    basis = request["review_basis"]["financial_assessment_basis"]
    financial += f"Supplied annual projection: {inert(basis['start'])} to {inert(basis['end'])}, {inert(basis['currency'])}, scale {inert(basis['scale'])}.\n\n"
    financial += "Annual-period analysis; full-term/balloon/refinancing adequacy not evaluated. Reported/adjusted EBITDA reconciliation deferred.\n\n"
    for metric in request["financial"]["metrics"]:
        handle = "calc:DSCR" if metric["metric_id"] == "CALC-004" else "calc:" + metric["metric_id"]
        financial += f"- {METRIC_LABELS[metric['metric_id']]}: {inert(metric['display'])} {inert(metric['unit'])}; {inert(metric['definition_version'])}. {cite(handle)}\n"
    parts.append(financial)
    score = request["risk"]["score"]
    risk = f"Credit risk: **{inert(score['display'])}/100 — {inert(score['band'])}**. {cite('panel:RISK')}\n\n"
    risk += f"Policy exceptions: {policy_exception_count}. Missing material evidence: {missing_material_count}. These are separate assessments for this registered synthetic fixture.\n\n"
    for factor in score["factors"]:
        risk += f"- {inert(factor['factor_id'])}: rating {inert(factor['rating'])}; weight {inert(factor['weight'])}; contribution {inert(factor['contribution'])}. {cite(factor['assessment_id'])}\n"
    risk += "\nAuthored educational assessments, not probability of default. Concentration: Not assessed."
    parts.append(risk)
    decision = wire.panel_decision
    parts.append(f"Simulated recommendation: **{inert(decision.decision)}**. Uncalibrated fixture confidence: {inert(decision.confidence)}.\n\n"
                 + inert(decision.rationale) + " " + cites(wire.rationale_refs)
                 + "\n\nHuman credit review: Not required by configured demo rules. Human disposition: None recorded.\n\n"
                 + "Narrative support: FIXTURE_EXPECTATION_CHECKED; not HUMAN_SUPPORTED. This report does not authorize lending or funding.")
    if reviewed:
        event = data.human_review["event"]
        parts[-1] = parts[-1].replace("Human credit review: Not required by configured demo rules. Human disposition: None recorded.",
            "Human credit review: Completed by simulated AuthorizedApprover. Human disposition: " + inert(event["decision"]) + ".\n\n"
            + "Reviewer: " + inert(event["reviewer_name"]) + "; UTC: " + inert(event["timestamp_utc"]) + ".\n\n"
            + "Review comments: " + inert(event["comments"]) + ".\n\n"
            + "Decision event: " + inert(event["operation_id"]) + ". Original confidence referral remains recorded.")
    parts.append("Model-proposed conditions: None. Human modifications: None recorded.\n\n"
                 + "Documentary covenants — EXTRACTED_NOT_EVALUATED: " + inert(terms["covenants"]["value"])
                 + ". " + cites(terms["covenants"]["refs"]))
    if conditional_review:
        from .conditional_review import condition_record, decode_draft
        condition = condition_record(data.scope.model_dump(), synthesis, decode_draft(data.human_review["condition_draft"]))
        if data.human_review["event"].get("condition_record") != condition:
            raise InputError("REPORT_CONDITION_RECORD_MISMATCH")
        parts[-1] = ("Model-proposed condition, unchanged by reviewers: " + inert(condition["text"]) + ". " + cites(condition["refs"])
            + "\n\nStatus: **OUTSTANDING**. Owner: Unassigned. Origin: MODEL_PROPOSAL / SOURCE_COVENANT."
            + "\n\nBoth specialist reviews are recorded; support does not fulfil the condition or cure DSCR. No funding is authorized."
            + "\n\nDocumentary covenant: EXTRACTED_NOT_EVALUATED. Draft: " + inert(condition["draft_id"]))
    audit = f"Recorded audit cutoff: sequence {cutoff}. Local SQLite history is not immutable audit storage.\n\n"
    if correction is not None:
        audit += ("Source correction: " + inert(correction["operation_id"]) + "; field: CFADS; original: Missing; corrected: USD900000; basis: FY-ASSESS. " + cite("FIN-P2")
            + "\n\nReviewer: " + inert(correction["reviewer_name"]) + "; UTC: " + inert(correction["timestamp_utc"])
            + ". Reason: " + inert(correction["comments"]) + ". Original run and extraction remain historical.\n\n")
    if exception_review:
        audit += "Exception handling receipts: " + ", ".join(inert(e["operation_id"]) for e in data.human_review["exception_events"]) + ".\n\n"
    if conditional_review:
        audit += "Condition preparation/support receipts: " + ", ".join(inert(e["operation_id"]) for e in data.human_review["condition_events"]) + ".\n\n"
    audit += "\n".join(f"- {event['sequence']}: {inert(event['stage'])} — {inert(event['event'])}." for event in data.events)
    audit += "\n\nSource and reference index (retained synthetic snapshot):\n\n"
    for handle, item in refs.items():
        audit += f"#### {citation_anchor(handle)}\n\n{inert(item['label'])} · {inert(item['kind'])}\n\n"
        if item["kind"] == "SOURCE":
            audit += f"Source SHA256: {inert(item['source_sha256'])}\n\n"
            audit += "\n".join("> " + inert(line) for line in item["text"].splitlines()) + "\n\n"
        elif item.get("value") is not None:
            # Render supplied operands/predicates/provenance, never recompute.
            audit += "\n".join(f"- {inert(key)}: {inert(value)}" for key, value in item["value"].items()) + "\n\n"
        if item["refs"]:
            audit += "Supporting references: " + cites(item["refs"]) + "\n\n"
    parts.append(audit)
    if data.approval_readiness is not None:
        from .readiness import ApprovalReadiness
        readiness=ApprovalReadiness.model_validate(data.approval_readiness)
        if readiness.scope!=data.scope.model_dump():
            raise InputError("REPORT_READINESS_SCOPE_MISMATCH")
        summary="Approval readiness: **"+inert(readiness.outcome)+"**. "+inert(readiness.reason)+"\n\n"
        summary+="Original AI proposal: "+inert(wire.panel_decision.decision)+". Human credit decision: "+(inert(data.human_review["event"]["decision"]) if reviewed else "Not recorded")+".\n\n"
        summary+="Next action: "+inert(readiness.permitted_next_actions[0])+"\n\n"
        parts[0]=summary+parts[0]
        from .recommendation import format_recommendation, markdown as recommendation_markdown
        recommendation=format_recommendation(readiness.model_dump(),financial=request["financial"],risk=request["risk"],
            human_decision=data.human_review["event"] if reviewed else None,ai_proposal=dict(decision=wire.panel_decision.decision))
        original_decision=parts[4]
        parts[4]=recommendation_markdown(recommendation,escape=inert,cite=lambda handles:cites([h for h in handles if h in refs]))
        parts[-1]+="\n\n### Original AI proposal and historical review details\n\nNot the effective recommendation or an authorization to lend.\n\n"+original_decision
        parts[-1]+="\n\nReadiness assessment: "+inert(readiness.assessment_id)+"; version "+str(readiness.version)+"; "+inert(readiness.assessment_digest)+"."
    markdown = title + "\n\n".join(f"## {heading}\n\n{body}" for heading, body in zip(SECTIONS, parts)) + "\n"
    digest = fingerprint("MEMO-INPUT", dict(scope=data.scope.model_dump(), packet=packet["input_digest"],
        synthesis=synthesis, events=data.events, generation_time=data.generation_time, renderer_version=renderer_version,
        **({"human_review": data.human_review} if reviewed else {}),
        **({"source_correction": correction} if correction is not None else {}),
        **({"approval_readiness":data.approval_readiness} if data.approval_readiness is not None else {})))
    return dict(markdown=markdown, section_index=list(SECTIONS),
                citation_index={h: dict(anchor=citation_anchor(h), kind=v["kind"], label=v["label"], refs=v["refs"])
                                for h, v in refs.items()},
                unresolved_issue_ids=[], metadata=dict(report_id=fingerprint("MEMO-ID", digest),
                    run_id=data.scope.run_id, deal_id=data.scope.deal_id, input_revision=data.scope.input_revision,
                    mode="FIXTURE", template_version="MEMO-1.0", renderer_version=renderer_version,
                    render_kind="GENERATED", completeness="COMPLETE",
                    input_digest=digest, audit_cutoff_sequence=cutoff, generation_time=data.generation_time,
                    semantic_support="FIXTURE_EXPECTATION_CHECKED_NOT_HUMAN_SUPPORTED", supersedes_report_id=None))


def render_live_memo(state, generation_time, support_events):
    """Pure educational Live report; consumes only recorded supported upstream data."""
    required={"extractor","fact_review","financial_analyst","compliance_check","risk_quantifier","synthesizer","evidence_review","route_review"}
    artifacts=state["artifacts"]
    demo=state["context"].get("verification_policy")=="DEMO_DRAFT"
    if not required<=set(artifacts) or state["context"]["mode"]!="LIVE" or state["status"]!="REPORT_ALLOWED":
        raise InputError("LIVE_REPORT_PREREQUISITES_REQUIRED")
    if demo and not all(artifacts[n]["payload"].get("automated_integrity_checked") is True and artifacts[n]["payload"].get("human_supported") is False for n in ("fact_review","evidence_review")):
        raise InputError("LIVE_DRAFT_INTEGRITY_CHECKS_REQUIRED")
    if not demo and not all(artifacts[n]["payload"].get("human_supported") is True for n in ("fact_review","evidence_review")):
        raise InputError("LIVE_REPORT_HUMAN_SUPPORT_REQUIRED")
    for artifact in artifacts.values():
        if artifact["digest"]!=fingerprint("LIVE_ARTIFACT",{k:v for k,v in artifact.items() if k!="digest"}):
            raise InputError("LIVE_REPORT_ARTIFACT_CHANGED")
    synthesis=artifacts["synthesizer"]["payload"]
    packet=synthesis["packet"]; request=packet["request"]
    if packet["input_digest"]!=fingerprint("E-N01-SYNTHESIS-INPUT-1.0",{k:v for k,v in packet.items() if k!="input_digest"}):
        raise InputError("LIVE_REPORT_PACKET_CHANGED")
    wire=parse_synthesis(synthesis["wire_json"])
    routing=artifacts["route_review"]["payload"]
    general=state['context'].get('upload_origin',{}).get('profile')=='USER_DECLARED_UPLOAD-1.0'
    if not general and (routing["workflow"] not in ("CONTINUE","REVIEW_REQUIRED") or routing["final_policy"]["exception_rule_ids"] or (wire.panel_decision.conditions and not demo)):
        raise InputError("LIVE_REPORT_UNHANDLED_GATE")
    human=artifacts.get("human_review",{}).get("payload")
    if not demo and not general and routing["workflow"]=="REVIEW_REQUIRED" and (human is None or human["scope"]!=state["context"]["scope"] or human["analysis_digest"]!=artifacts["review_prepare"]["payload"]["analysis_digest"]):
        raise InputError("LIVE_REPORT_CREDIT_REVIEW_REQUIRED")
    stamp=datetime.fromisoformat(generation_time.replace("Z","+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds()!=0:
        raise InputError("REPORT_EXPLICIT_UTC_TIME_REQUIRED")
    refs=request["reference_dictionary"]
    def cite(handles):
        if any(h not in refs for h in handles):
            raise InputError("LIVE_REPORT_REFERENCE_MISSING")
        return " ".join("["+inert(h)+"](#"+citation_anchor(h)+")" for h in handles)
    if not support_events:
        raise InputError("LIVE_REPORT_SUPPORT_AUDIT_REQUIRED")
    sections=[]
    sections.append("Borrower: "+inert(request["terms"]["borrower"]["value"])+". "+cite(request["terms"]["borrower"]["refs"])+"\n\n"+"\n\n".join(inert(o.text)+" "+cite(o.refs) for o in wire.observations))
    for field,label in (("requested_amount","Requested amount"),("currency","Currency"),("term_months","Term in months"),("maturity_date","Maturity date"),("repayment_structure","Repayment"),("use_of_proceeds","Use of proceeds"),("collateral","Collateral"),("guarantees","Guarantees"),("covenants","Covenants")):
        fact=request["terms"][field]
        sections[0]+="\n\n"+label+": "+inert(fact["value"] if fact["value"] is not None else "Not available")+". "+cite(fact["refs"])
    interest=request["terms"]["interest_terms"]
    sections[0]+="\n\nInterest terms: "+inert(interest["value"])+". "+cite(interest["refs"])
    rules=routing["final_policy"]["rules"]
    sections.append("\n".join("- "+inert(r["rule_id"])+": "+inert(r["outcome"] or r.get("control_result"))+"; observed "+inert(r["observed"])+"; rule "+inert(r["predicate"])+". "+cite(["policy:"+r["policy_version"]+":"+r["rule_id"]]) for r in rules))
    sections.append("Annual-period analysis only; full-term/balloon/refinancing not evaluated.\n\n"+"\n".join("- "+inert(METRIC_LABELS.get(m["metric_id"],m["metric_id"]))+": "+inert(m["display"] or "Not available")+" "+inert(m["unit"])+". "+cite(m["source_refs"]) for m in request["financial"]["metrics"]))
    risk=request["risk"]["score"]
    risk_label = "Insufficient data; no composite credit risk score" if risk["total"] is None else inert(risk["display"])+"/100; "+inert(risk["band"])
    sections.append(risk_label+". Educational authored factor ratings, not probability of default. Concentration not assessed.\n\n"+"\n".join("- "+inert(f["factor_id"])+": "+inert(f["rating"])+"; weight "+inert(f["weight"])+"; contribution "+inert(f["contribution"])+". "+cite(f["refs"]) for f in risk["factors"]))
    decision="AI proposal: "+inert(wire.panel_decision.decision)+". "+inert(wire.panel_decision.rationale)+" "+cite(wire.rationale_refs)+"\n\nConfidence is uncalibrated. Python routing: "+inert(routing["workflow"])+"."
    decision+="\n\nHuman credit decision: "+(inert(human["decision"])+"; "+inert(human["comments"])+"; "+inert(human["timestamp_utc"]) if human else "Not recorded; human review remains required for this unverified draft." if demo else "Not recorded; not required by the configured route. An AI proposal is not a human approval.")
    if state.get("approval_readiness"):
        from .recommendation import format_recommendation, markdown as recommendation_markdown
        original_decision=decision
        recommendation=format_recommendation(state["approval_readiness"],financial=request["financial"],risk=request["risk"],human_decision=human,ai_proposal=dict(decision=wire.panel_decision.decision))
        decision=recommendation_markdown(recommendation,escape=inert,cite=lambda handles:cite([h for h in handles if h in refs]))
    sections.append(decision)
    sections.append(("Proposed conditions — not accepted or fulfilled:\n"+"\n".join("- "+inert(c) for c in wire.panel_decision.conditions) if wire.panel_decision.conditions else "No conditions proposed.")+" No funding or real lending action is authorized.")
    sections.append("\n".join("- "+str(e["sequence"])+". "+inert(e["stage"])+"; "+inert(e["timestamp"])+"; "+inert(e["artifact_digest"]) for e in state["events"])+"\n\nFact support receipt: "+inert(artifacts["fact_review"]["payload"]["support_digest"])+"\n\nNarrative support receipt: "+inert(artifacts["evidence_review"]["payload"]["support_digest"])+"\n\nLocal history is retained, not tamper-proof.")
    if state.get("approval_readiness"):
        sections[-1]+="\n\n### Original AI proposal and historical review details\n\nNot the effective recommendation or an authorization to lend.\n\n"+original_decision
    sections[-1]+="\n\nRecorded usage (provider reported; cost at verified rates): "+inert(state["ledger"]["committed"])+"."
    for event in support_events:
        sections[-1]+="\n\nEvidence reviewed: "+inert(event["target"])+"; "+inert(event["domain"])+"; "+inert(event["reviewer"])+"; UTC "+inert(event["timestamp_utc"])+". "+inert(event["comments"])+" "+cite(event["source_refs"])
    markdown=("# Deal or No Deal AI - Live Draft Credit Memo\n\nUNVERIFIED EDUCATIONAL DRAFT. Actual Nebius responses; automated integrity checks only. No human evidence verification or credit decision.\n\n" if demo else "# Deal or No Deal AI - Educational Live Credit Memo\n\nActual provider responses with simulated human evidence review. Fictional deal only; no real credit authority.\n\n")
    if state['context'].get('upload_origin'):
        markdown+='Deal ID: '+inert(state['context']['scope']['deal_id'])+'\n\nUploaded package: '+inert(state['context']['upload_origin']['package_id'])+'\n\n'
        markdown+='Uploaded source mapping:\n'+"\n".join('- '+inert(k)+': '+inert(v['filename'])+'; page '+str(v['page'])+'; '+inert(v['upload_ref']) for k,v in state['context']['upload_origin']['page_map'].items())+'\n\n'
    markdown+="\n\n".join("## "+heading+"\n\n"+body for heading,body in zip(SECTIONS,sections))
    markdown+="\n\n## Supporting sources and calculations\n\n"
    for handle,entry in refs.items():
        markdown+='\n<a id="'+citation_anchor(handle)+'"></a>\n\n**'+inert(handle)+'** '+inert(entry["label"])+"\n\n"
        if entry["kind"]=="SOURCE":
            markdown+="Page "+str(entry["page"])+"; version "+inert(entry["source_version"])+"; SHA256 "+inert(entry["source_sha256"])+"\n\n"+inert(entry["text"])+"\n"
        elif entry.get("refs"):
            markdown+="Supporting references: "+cite(entry["refs"])+"\n"
    if state.get("approval_readiness"):
        from .readiness import ApprovalReadiness
        readiness=ApprovalReadiness.model_validate(state["approval_readiness"])
        markdown=markdown.replace("## Executive Summary", "Approval readiness: **"+inert(readiness.outcome)+"**. "+inert(readiness.reason)+"\n\nNext action: "+inert(readiness.permitted_next_actions[0])+"\n\n## Executive Summary",1)
    metadata=dict(renderer_version="LIVE-MEMO-1.0/READINESS-1.0/RECOMMENDATION-1.0",generation_time=generation_time,scope=state["context"]["scope"],source_binding=state["context"]["source_binding"],audit_cutoff_sequence=len(state["events"]),mode="LIVE",model_requests=2)
    if demo:
        metadata.update(verification_policy="DEMO_DRAFT",human_verified=False,report_kind="UNVERIFIED_DRAFT")
    metadata["content_digest"]=fingerprint("LIVE_REPORT",dict(markdown=markdown,metadata=metadata))
    return dict(markdown=markdown,metadata=metadata)
