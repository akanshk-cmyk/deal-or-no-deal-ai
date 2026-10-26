"""Derived activity never invents receipts, consumes tools or mutates records."""
from copy import deepcopy
from deal_or_no_deal_ai.ui.specialists import project


def recorded(*stages, mode="FIXTURE", status="COMPLETED", pending=None):
    artifacts={s:{"stage":s,"content_digest":"output:"+s,"payload":{}} for s in stages}
    events=[dict(stage=s,event="stage_completed",run_id="current",sequence=i+1,
                 artifact_digest="output:"+s,timestamp="2026-10-25T00:00:00+00:00")
            for i,s in enumerate(stages)]
    return dict(context=dict(mode=mode,scope=dict(run_id="current",input_revision=2)),
                artifacts=artifacts,events=events,status=status,outcome=dict(pending_stage=pending,status=status))


def test_complete_recorded_dependency_and_projection_are_read_only():
    run=recorded("extractor","financial_analyst","compliance_check","risk_quantifier","synthesizer","evidence_review","route_review")
    before=deepcopy(run)
    view=project(run)
    assert len(view["roles"])==3
    assert all(row["status"]=="Downstream result recorded" for row in view["handoffs"])
    assert all(row["review_version"]==2 for row in view["handoffs"])
    assert view["handoffs"][0]["source_records"][0]["digest"]=="output:extractor"
    assert run==before


def test_start_wrong_run_digest_and_reversed_events_do_not_prove_handoff():
    for change in (dict(event="stage_started"),dict(run_id="another-review"),dict(artifact_digest="wrong"),dict(sequence=100)):
        run=recorded("extractor","financial_analyst")
        run["events"][0].update(change)
        row=project(run)["handoffs"][0]
        assert row["status"]=="Dependency record not confirmed"


def test_live_human_pause_is_not_an_accepted_handoff():
    run=recorded("extractor",mode="LIVE",status="WAITING_EVIDENCE",pending="fact_review")
    view=project(run)
    assert "await human verification" in view["roles"][0]["status"]
    assert view["handoffs"][0]["status"]=="Waiting for human fact verification"
    assert view["handoffs"][0]["destination_record"] is None
    assert "Risk Manager" in view["next_action"]


def test_missing_information_and_recovery_do_not_claim_complete_analysis():
    run=recorded("extractor","financial_analyst","compliance_check","risk_quantifier",status="WAITING_INFORMATION")
    view=project(run)
    assert "no complete summary" in view["roles"][2]["status"]
    assert view["handoffs"][4]["destination_record"] is None
    run["status"]="RECOVERY_REQUIRED"
    assert "Do not replay" in project(run)["next_action"]
