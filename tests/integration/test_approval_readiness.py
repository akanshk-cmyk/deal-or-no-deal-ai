"""Current saved proposal, role/version enforcement and exact historical preservation."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pytest
from deal_or_no_deal_ai.command_center import get_run, workspace_id, source_packet
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.readiness_service import (assess_current,require_approval,record_review,
    ReadinessReviewCommand,HumanReadinessDecision,record_ready_decision,evidence_targets,CHECKS)
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store,StaleRecord,OperationConflict
from deal_or_no_deal_ai.worker import run_normal_fixture
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import uid
from tests.unit.test_readiness import ready_inputs


@pytest.fixture
def saved_deal():
    with TemporaryDirectory() as folder:
        root=Path(folder);copy_workspace(root);operation=uid("readiness-standard")
        result=run_normal_fixture(root,operation,generation_time="2026-10-24T05:00:00+00:00")
        actor=Actor("AuthorizedApprover",workspace_id(root),frozenset({result["scope"]["deal_id"]}),frozenset({"NORMAL"}))
        store=Store(root/"var/deal_review.sqlite3")
        yield root,operation,actor,store,result


def test_standard_deal_proposal_preserved_pending_report_and_projection(saved_deal):
    root,operation,actor,store,result=saved_deal
    before=store.path.read_bytes();run=get_run(store,actor,operation)
    assert store.path.read_bytes()==before
    assert run["ai_proposal"]["decision"]=="Approve"
    assert run["approval_readiness"]["outcome"]=="Pending Review"
    assert run["approval_readiness"]["reason"]=="Mandatory covenant evaluation incomplete"
    assert run["human_decision"] is None
    assert "annual financial-statement" in run["approval_readiness"]["permitted_next_actions"][0]
    assert result["status"]=="COMPLETED" and result["report_markdown"]
    assert "Pending Review" in result["report_markdown"]
    assert len(result["audit_events"])==18
    assert result["ledger"]["committed"]["attempts"]==0
    assert run["ai_proposal"]["original_wire_json"]==run["artifacts"]["synthesizer"]["payload"]["wire_json"]
    with pytest.raises(InputError,match="APPROVAL_READINESS_BLOCKED"):
        a=run["approval_readiness"];require_approval(store,run,a["version"],a["assessment_digest"])


def test_role_source_timing_and_duplicate_metadata_checks(saved_deal):
    root,operation,actor,store,result=saved_deal
    run=get_run(store,actor,operation);a=run["approval_readiness"]
    sources={k:v["text"] for k,v in source_packet(root,run)["request"]["reference_dictionary"].items() if v["kind"]=="SOURCE"}
    covenant=a["covenants"][0]
    from deal_or_no_deal_ai.readiness import CovenantEvaluation
    c=CovenantEvaluation.model_validate(covenant)
    c=c.model_copy(update={"evaluation_status":"EVALUATED","reason":"No contractual timing is stated; retain pending review."})
    cmd=ReadinessReviewCommand(operation_id=uid("record-covenant"),expected_version=a["version"],expected_analysis=a["analysis_digest"],part="COVENANT",covenant=c,quotes=sources,comments="Inspected actual source; do not assume an annual due date.")
    with pytest.raises(InputError,match="PERMISSION"):
        record_review(root,actor,operation,cmd)
    officer=replace(actor,persona="ComplianceOfficer")
    future=cmd.model_copy(update={"covenant":c.model_copy(update={"due_date":"2027-03-31"})})
    with pytest.raises(InputError,match="DUE_DATE_EVIDENCE"):
        record_review(root,officer,operation,future)
    event=record_review(root,officer,operation,cmd)
    assert record_review(root,officer,operation,cmd)==event
    with pytest.raises(OperationConflict):
        record_review(root,officer,operation,cmd.model_copy(update={"comments":"Changed command"}))
    new=get_run(store,actor,operation)
    assert new["approval_readiness"]["version"]==a["version"]+1
    assert new["approval_readiness"]["outcome"]=="Pending Review"
    assert new["artifacts"]==run["artifacts"]
    assert new["outcome"]["report_markdown"]==result["report_markdown"]
    assert new["approval_readiness"]["previous_assessment_id"]==a["assessment_id"]
    with pytest.raises(StaleRecord):
        record_review(root,officer,operation,cmd.model_copy(update={"operation_id":uid("stale-covenant")}))


def test_evidence_review_requires_every_target_and_correct_role(saved_deal):
    root,operation,actor,store,_=saved_deal;run=get_run(store,actor,operation);a=run["approval_readiness"]
    sources={k:v["text"] for k,v in source_packet(root,run)["request"]["reference_dictionary"].items() if v["kind"]=="SOURCE"}
    cmd=ReadinessReviewCommand(operation_id=uid("verify-evidence"),expected_version=a["version"],expected_analysis=a["analysis_digest"],part="EVIDENCE",domain="FINANCIAL_RISK",status="VERIFIED",checked_targets=evidence_targets(run["artifacts"],"FINANCIAL_RISK"),checks=list(CHECKS),quotes=sources,comments="Synthetic reviewer checked every financial target.")
    with pytest.raises(InputError,match="PERMISSION"):
        record_review(root,actor,operation,cmd)
    with pytest.raises(InputError,match="ALL_CURRENT_TARGETS"):
        record_review(root,replace(actor,persona="RiskManager"),operation,cmd.model_copy(update={"checked_targets":[]}))
    record_review(root,replace(actor,persona="RiskManager"),operation,cmd)
    assert get_run(store,actor,operation)["approval_readiness"]["outcome"]=="Pending Review"


def test_fully_satisfied_synthetic_gate_enforces_role_latest_version_and_one_decision(saved_deal):
    """Injected pure eligibility inputs test the command boundary, not E-N01 creditworthiness."""
    root,operation,actor,store,result=saved_deal;run=get_run(store,actor,operation)
    data=ready_inputs();data.update(scope=run["context"]["scope"],analysis_digest=run["approval_readiness"]["analysis_digest"])
    for k in ("version","evaluated_at_utc"):
        data.pop(k)
    with patch("deal_or_no_deal_ai.readiness_service.inputs",return_value=data):
        receipt=store.admit(uid("test-ready-assessment"),result["scope"],{"action":"TEST_ONLY_ELIGIBILITY"})
        ready=assess_current(store,run["context"],run["artifacts"],receipt);store.release(receipt,confirmed_idle=True)
        cmd=HumanReadinessDecision(operation_id=uid("test-human-ready"),expected_version=ready.version,expected_digest=ready.assessment_digest,expected_analysis=ready.analysis_digest,decision="Approve",comments="Explicitly hypothetical satisfied prerequisites; not a claim about the saved source.")
        with pytest.raises(InputError,match="AUTHORIZED"):
            record_ready_decision(root,replace(actor,persona="Analyst"),operation,cmd)
        with pytest.raises(StaleRecord):
            record_ready_decision(root,actor,operation,cmd.model_copy(update={"expected_version":ready.version-1}))
        event=record_ready_decision(root,actor,operation,cmd)
        assert record_ready_decision(root,actor,operation,cmd)==event
        with pytest.raises(InputError,match="ALREADY_RECORDED"):
            record_ready_decision(root,actor,operation,cmd.model_copy(update={"operation_id":uid("second-human-decision")}))
        current=get_run(store,actor,operation)
        assert current["human_decision"]["decision"]=="Approve" and current["human_disposition"]=="Approve"
        assert current["outcome"]["report_markdown"]==result["report_markdown"]
        from deal_or_no_deal_ai.financial_review import financial_history
        assert financial_history(store,actor)[-1]["approval_readiness"]==ready.model_dump()
    assert get_run(store,actor,operation)["approval_readiness"]["outcome"]=="Pending Review"


def test_changed_source_and_missing_resume_version_cannot_approve(saved_deal):
    root,operation,actor,store,result=saved_deal
    run=get_run(store,actor,operation)
    with pytest.raises(InputError,match="LATEST_READINESS_VERSION_REQUIRED"):
        require_approval(store,run)
    agreement=root/"fixtures/development/e-n01/sources/agreement.pdf"
    agreement.write_bytes(agreement.read_bytes()+b"changed-source")
    with pytest.raises(InputError):
        source_packet(root,run)
    a=run["approval_readiness"]
    cmd=HumanReadinessDecision(operation_id=uid("changed-source-approval"),expected_version=a["version"],expected_digest=a["assessment_digest"],expected_analysis=a["analysis_digest"],decision="Approve",comments="Should not be accepted")
    with pytest.raises(InputError):
        record_ready_decision(root,actor,operation,cmd)
    assert store.get_record("readiness-human:"+result["scope"]["run_id"]) is None


def test_previous_evidence_support_becomes_stale_for_changed_analysis(saved_deal):
    from copy import deepcopy
    root,operation,actor,store,_=saved_deal;run=get_run(store,actor,operation);a=run["approval_readiness"]
    sources={k:v["text"] for k,v in source_packet(root,run)["request"]["reference_dictionary"].items() if v["kind"]=="SOURCE"}
    cmd=ReadinessReviewCommand(operation_id=uid("evidence-before-change"),expected_version=a["version"],expected_analysis=a["analysis_digest"],part="EVIDENCE",domain="FINANCIAL_RISK",status="VERIFIED",checked_targets=evidence_targets(run["artifacts"],"FINANCIAL_RISK"),checks=list(CHECKS),quotes=sources,comments="Current synthetic facts reviewed")
    record_review(root,replace(actor,persona="RiskManager"),operation,cmd)
    context=deepcopy(run["context"]);context["case_dependency_digest"]="different-analysis-source"
    assessment=assess_current(store,context,run["artifacts"])
    assert assessment.version==0 and not assessment.approval_eligible
    assert next(r for r in assessment.evaluated_requirements if r.requirement_id=="evidence").status=="STALE"


def test_resume_credit_receipt_cannot_bypass_pending_readiness(saved_deal):
    """Exercise the actual resume receipt loader against a real persisted blocker."""
    from deal_or_no_deal_ai.live_worker import _credit_record
    from deal_or_no_deal_ai.storage import RecordWrite
    root,operation,actor,store,result=saved_deal
    run=get_run(store,actor,operation);context=run["context"];scope=context["scope"]
    artifacts={**run["artifacts"],"review_prepare":{"payload":{"analysis_digest":"resume-test-basis"}}}
    store.put_record(RecordWrite("live-progress:"+operation,"TEST_RESUME_PROGRESS",dict(artifacts=artifacts,status="WAITING_REVIEW"),0))
    event=dict(scope=scope,analysis_digest="resume-test-basis",reviewer_role="AuthorizedApprover",reviewer_tier="NORMAL",decision="Approve",comments="An approval receipt must not bypass the gate",timestamp_utc="2026-10-24T05:00:00+00:00",approval_readiness=run["approval_readiness"])
    store.put_record(RecordWrite("live-credit:"+scope["run_id"],"LIVE_CREDIT_DECISION",event,0))
    with pytest.raises(InputError,match="APPROVAL_READINESS_BLOCKED"):
        _credit_record(store,context)
