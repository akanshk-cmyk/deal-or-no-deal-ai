"""Explicit advisory fact judging; never creates human evidence or resumes a graph."""
from collections import Counter
from pathlib import Path
from typing import Literal
import json
from uuid import UUID, uuid5

from pydantic import Field
from .contracts import StrictModel
from .context import InputError, fingerprint
from .live_review import FACT_CHECKS, request_key, verify_request


class Citation(StrictModel):
    ref: str = Field(min_length=1, max_length=120)
    quote: str = Field(min_length=1, max_length=140)


class FactFinding(StrictModel):
    id: str = Field(min_length=1, max_length=160)
    status: Literal["SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE"]
    issue_checks: list[Literal["reference", "row_label", "value", "units_scale", "period", "subject_facility", "debt_service_scope"]] = Field(max_length=7)
    reason: str = Field(min_length=1, max_length=160)
    citations: list[Citation] = Field(max_length=8)


class FactBatch(StrictModel):
    results: list[FactFinding] = Field(min_length=1, max_length=12)


def validate_batch(raw, targets, sources):
    parsed = FactBatch.model_validate(raw)
    expected = {t["id"]:t for t in targets}
    actual = [v.id for v in parsed.results]
    if len(actual) != len(set(actual)) or set(actual) != set(expected):
        raise InputError("FACT_JUDGE_EXACT_TARGET_COVERAGE_REQUIRED")
    for item in parsed.results:
        target = expected[item.id]
        if not item.reason.strip() or (item.status == "CONTRADICTED" and not item.citations):
            raise InputError("FACT_JUDGE_EXPLANATION_AND_CONTRADICTION_EVIDENCE_REQUIRED")
        if len(item.issue_checks) != len(set(item.issue_checks)):
            raise InputError("FACT_JUDGE_DUPLICATE_CHECK")
        if (item.status == "SUPPORTED") != (not item.issue_checks):
            raise InputError("FACT_JUDGE_STATUS_CHECKS_INCONSISTENT")
        refs = [c.ref for c in item.citations]
        if len(refs) != len(set(refs)):
            raise InputError("FACT_JUDGE_DUPLICATE_REFERENCE")
        if item.status == "SUPPORTED" and set(refs) != set(target["source_refs"]):
            raise InputError("FACT_JUDGE_ALL_TARGET_SOURCES_REQUIRED")
        for citation in item.citations:
            if (citation.ref not in sources or not citation.quote.strip()
                or citation.quote not in sources[citation.ref]):
                raise InputError("FACT_JUDGE_EXACT_SOURCE_QUOTE_REQUIRED")
    return [v.model_dump() for v in parsed.results]


def validate_batch_diagnostic(raw, targets, sources):
    """Retain independent row failures as flags; never upgrade the failed evidence."""
    parsed=FactBatch.model_validate(raw)
    expected={t["id"]:t for t in targets}
    ids=[v.id for v in parsed.results]
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected):
        raise InputError("FACT_JUDGE_EXACT_TARGET_COVERAGE_REQUIRED")
    findings=[]
    for item in parsed.results:
        value=item.model_dump()
        try:
            validate_batch(dict(results=[value]),[expected[item.id]],sources)
            value["validation_status"]="VALIDATED_EVIDENCE"
        except InputError as error:
            value.update(validation_status="INVALID_EVIDENCE",validation_reason=str(error))
        findings.append(value)
    return findings


def freeze(root, actor, operation):
    from .configuration import load_configuration
    from .storage import Store
    from .live_worker import load_live, _request
    from .live_context import prepare_live_tasks
    from .services import load_registered_case
    root=Path(root)
    store=Store(load_configuration(root).database)
    state=load_live(root,actor,operation)
    store.assert_review_open(state["context"]["scope"]["review_id"])
    if state["status"] != "WAITING_EVIDENCE" or state["pending_stage"] != "fact_review":
        raise InputError("CURRENT_LIVE_FACT_REVIEW_REQUIRED")
    request=store.get_record(request_key(state["context"]["scope"]["run_id"],"fact_review"))[1]
    verify_request(request)
    base=load_registered_case(root)
    tasks=prepare_live_tasks(root)
    binding=fingerprint("LIVE_SOURCE_AND_PROMPTS",dict(case=base.dependency_digest,
        instructions={k:v["instruction"] for k,v in tasks.items()},schemas={k:v["schema"] for k,v in tasks.items()}))
    if binding != request["source_binding"] or _request(base,state,"fact_review") != request:
        raise InputError("FACT_JUDGE_CURRENT_SOURCE_AND_PARENT_BINDING_REQUIRED")
    if len(request["targets"]) != 36 or len({t["id"] for t in request["targets"]}) != 36:
        raise InputError("FACT_JUDGE_BOUNDED_36_TARGET_PROFILE_REQUIRED")
    instruction=(root/"docs/agents/extracted-fact-judge.md").read_text(encoding="utf-8").split("## Runtime prompt",1)[1].strip()
    profile=(root/"config/evaluation.toml").read_text(encoding="utf-8")
    sample=dict(version="FACT-JUDGE-1.0",scope=state["context"]["scope"],operation_id=operation,
        request=request,instruction=instruction,profile_digest=fingerprint("FACT_JUDGE_PROFILE",profile),
        provenance="ACTUAL_LIVE_EXTRACTED_FACTS_AND_SEPARATE_AUTHORED_PREMISES",
        original_wire_json=state["artifacts"]["extractor"]["payload"]["wire_json"],
        human_authority=False,maximum_requests=3)
    sample["digest"]=fingerprint("FACT_JUDGE_SAMPLE",sample)
    sample["evaluation_id"]=str(uuid5(UUID(operation),sample["digest"]))
    return sample


def batches(sample):
    request=sample["request"]
    for offset in range(0,36,12):
        targets=request["targets"][offset:offset+12]
        packet=dict(review_basis=request["review_basis"],source_metadata=request["source_metadata"],
            original_sources=request["sources"],checks=list(FACT_CHECKS),targets=targets,
            target_origins={t["id"]:"AUTHORED_SCORING_PREMISE" if t["id"].startswith("assessment:") else "ACTUAL_LIVE_EXTRACTED_FACT" for t in targets})
        prompt=sample["instruction"]+"\nKeep reasons and quotes as short as possible, preferably under 90 characters each; preserve essential qualifications.\nINPUT DATA:\n"+json.dumps(packet,ensure_ascii=False,separators=(",",":"))
        yield targets,prompt


def run(sample, judge, checkpoint=None, *, retain_invalid_evidence=False):
    results=[]
    report=dict(status="IN_PROGRESS",evaluation_id=sample["evaluation_id"],sample=sample,
        results=results,batches_completed=0,judge_invocations=0,grants_human_support=False,
        native_ragas_metrics="NOT_RUN_CUSTOM_FACT_JUDGE_ONLY")
    for targets,prompt in batches(sample):
        report["judge_invocations"]+=1
        try:
            raw=judge(prompt,FactBatch.model_json_schema())
            report["last_raw_result"]=raw
            validator=validate_batch_diagnostic if retain_invalid_evidence else validate_batch
            results.extend(validator(raw,targets,sample["request"]["sources"]))
            report["batches_completed"]+=1
        except Exception as error:
            report.update(status="FAILED",error_type=type(error).__name__,
                failure_reason="A batch was incomplete, invalid, uncertain or blocked; no automatic retry.")
        counts=Counter(v["status"] for v in results if v.get("validation_status")!="INVALID_EVIDENCE")
        report["counts"]={k:counts[k] for k in ("SUPPORTED","CONTRADICTED","INSUFFICIENT_EVIDENCE")}
        report["counts"]["INVALID_EVIDENCE"]=sum(v.get("validation_status")=="INVALID_EVIDENCE" for v in results)
        report["counts"]["NOT_EVALUATED"]=36-len(results)
        if report["batches_completed"]==3:
            report["status"]="COMPLETE_WITH_FLAGS" if report["counts"]["INVALID_EVIDENCE"] else "COMPLETE"
        if checkpoint:
            checkpoint(report)
        if report["status"]=="FAILED":
            break
    return report


def markdown(report):
    request=report["sample"]["request"]
    targets={t["id"]:t for t in request["targets"]}
    lines=["# Live extraction — advisory AI fact check", "", "Execution: "+report["status"],
        "", "36 checks: 31 live-extracted facts and five authored scoring premises.",
        "AI judgments only. No human support, credit approval or graph continuation was recorded.",
        "These are not native RAGAS scores. Exact citations validate traceability, not semantic truth.",
        "", "- AI-supported with accepted citations: "+str(report["counts"]["SUPPORTED"]),
        "- Contradicted by the cited evidence: "+str(report["counts"]["CONTRADICTED"]),
        "- Insufficient evidence identified by the judge: "+str(report["counts"]["INSUFFICIENT_EVIDENCE"]),
        "- Needs independent citation/evidence review: "+str(report["counts"].get("INVALID_EVIDENCE",0)),
        "- Not assessed: "+str(report["counts"]["NOT_EVALUATED"]),
        "", "Total judging cost (including the reused first batch): USD "+str(report.get("total_judging_cost_usd","Not available")), ""]
    for item in report["results"]:
        target=targets[item["id"]]
        display=("Needs evidence review — the AI proposed support, but citation validation failed") if item.get("validation_status")=="INVALID_EVIDENCE" else {"SUPPORTED":"AI-supported","CONTRADICTED":"Contradicted by evidence","INSUFFICIENT_EVIDENCE":"Insufficient evidence"}[item["status"]]
        lines.extend(["## "+target["label"],"",display+" — "+item["reason"],
                      "Checks needing attention: "+("Source quotation or citation coverage" if item.get("validation_status")=="INVALID_EVIDENCE" else ", ".join(item["issue_checks"]) or "None identified by the AI judge")])
        if item.get("validation_status")=="INVALID_EVIDENCE":
            reason={"FACT_JUDGE_EXACT_SOURCE_QUOTE_REQUIRED":"The quotation does not exactly match the cited source; this may be a wording or line-break issue, not an incorrect underlying fact.",
                "FACT_JUDGE_ALL_TARGET_SOURCES_REQUIRED":"The judge did not cite every source required for this complete assessment."}.get(item["validation_reason"],"The AI judgment did not satisfy the evidence checks; inspect the JSON report for the exact validation reason.")
            lines.append("Independent check: "+reason)
        for c in item["citations"]:
            meta=request["source_metadata"].get(c["ref"])
            label=("Unverified AI quotation: " if item.get("validation_status")=="INVALID_EVIDENCE" else "")+c["ref"]
            if meta:
                label+=", page "+str(meta["page"])+", version "+meta["source_version"]
            lines.append("- "+label+": "+json.dumps(c["quote"],ensure_ascii=False))
        lines.append("")
    return "\n".join(lines)
