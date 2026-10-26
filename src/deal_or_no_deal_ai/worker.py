"""Explicit E-N01 Fixture worker with shared SQLite admission and checkpoints."""

from dataclasses import asdict
from contextlib import closing
from datetime import datetime, timezone
import math
import os
from pathlib import Path
import sqlite3
import time
from uuid import UUID, uuid5, NAMESPACE_URL

from .budgets import Ledger, Usage
from .configuration import load_configuration
from .context import InputError, fingerprint, primitive
from .contracts import Scope
from .graph import STAGES, TOOL_STAGES, build_graph
from .memo import ReportInput, render_memo
from .panel_codec import restore_compliance, restore_financial, restore_risk
from .services import compute_compliance, compute_financials, compute_risk, evaluate_panels, load_registered_case
from .storage import RecordWrite, Store
from .synthesis import prepare_synthesis, validate_fixture_synthesis


def run_normal_fixture(root: Path, operation_id: str, *, generation_time: str | None = None,
                       variant: str = "default", scenario_id: str = "E-N01", _resume=None, _continuation=None) -> dict:
    """Explicit command only. No automatic retry/recovery or alternative case."""
    for key in ("LANGSMITH_TRACING", "LANGCHAIN_TRACING_V2", "LANGCHAIN_TRACING"):
        if os.environ.get(key, "").strip().lower() not in ("", "false", "0", "off", "no"):
            raise InputError("FIXTURE_HOSTED_TRACING_MUST_BE_DISABLED")
    if str(UUID(operation_id)) != operation_id:
        raise InputError("CANONICAL_OPERATION_UUID_REQUIRED")
    config = load_configuration(root)
    if (scenario_id not in ("E-N01", "E-M01", "E-F03", "E-P01")
        or scenario_id == "E-M01" and (variant != "default" or _resume is not None or _continuation is not None)
        or scenario_id in ("E-F03", "E-P01") and (variant != "review" or _continuation is not None)):
        raise InputError("UNREGISTERED_SCENARIO_BRANCH")
    if variant not in ("default", "review", "extraction-miss") or (_resume is not None and variant != "review") or (variant == "extraction-miss" and (scenario_id != "E-N01" or _continuation is not None)):
        raise InputError("UNREGISTERED_WORKER_VARIANT")
    root = config.workspace
    store = Store(config.database)
    store.initialize()
    context_key, result_key = "normal-context:" + operation_id, "normal-result:" + operation_id
    prior = store.get_record(context_key)
    correction = _continuation is not None and _continuation.get("kind") == "SOURCE_CORRECTION"
    profile = prior[1].get("profile", "default") if prior else "correction" if correction else "reassessment" if _continuation else "extraction-miss" if variant == "extraction-miss" else "default"
    if profile == "correction" and (not correction or variant != "default"):
        raise InputError("EXPLICIT_READY_CORRECTION_COMMAND_REQUIRED")
    missing = scenario_id == "E-M01" or profile == "extraction-miss"
    if profile == "reassessment" and variant != "review":
        raise InputError("REGISTERED_REASSESSMENT_REQUIRES_REVIEW_VARIANT")
    case = load_registered_case(root, profile=profile, scenario_id=scenario_id)
    from .synthesis import prepare_source_inspection
    packet = prepare_source_inspection(case) if missing else prepare_synthesis(case)
    if prior:
        if prior[1]["variant"] != variant or prior[1]["scenario_id"] != scenario_id:
            raise InputError("EXISTING_OPERATION_VARIANT_CHANGED")
        recorded_time = prior[1]["generation_time"]
        if generation_time is not None and generation_time != recorded_time:
            raise InputError("EXISTING_OPERATION_TIME_CHANGED")
        generation_time = recorded_time
    elif generation_time is None:
        generation_time = datetime.now(timezone.utc).isoformat()
    stamp = datetime.fromisoformat(generation_time.replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise InputError("EXPLICIT_UTC_GENERATION_TIME_REQUIRED")
    uid = lambda label: str(uuid5(UUID(operation_id), label))
    inherited_review = (_continuation["parent"]["context"]["scope"]["review_id"] if _continuation else
                        prior[1]["scope"]["review_id"] if prior and profile in ("reassessment", "correction") else uid("review"))
    scope = Scope(workspace_id=str(uuid5(NAMESPACE_URL, str(root))), deal_id=case.scope.deal_id,
                  review_id=inherited_review, run_id=uid("run"), thread_id=uid("thread"), input_revision=case.scope.revision)
    context = dict(scope=scope.model_dump(), operation_id=operation_id, generation_time=generation_time,
                   case_dependency_digest=case.dependency_digest, synthesis_input_digest=packet["input_digest"],
                   mode="FIXTURE", scenario_id=scenario_id, variant=variant)
    if profile == "extraction-miss":
        context["profile"] = profile
    if profile in ("reassessment", "correction"):
        context.update(profile=profile, entry_stage="financial_analyst",
                       parent_operation=_continuation["parent"]["operation_id"] if _continuation else prior[1]["parent_operation"])
    if correction:
        context["correction_event_id"] = _continuation["event_id"]
        if prior is None or prior[1] != context:
            raise InputError("SAVED_CORRECTION_CONTEXT_REQUIRED")
    ledger_key = "ledger:" + scope.review_id
    initial_ledger = Ledger.from_dict(_continuation["ledger"]) if _continuation else Ledger(scope.review_id)
    if _resume is None:
        initial_ledger.require_path("FINANCIAL_CORRECTION_DIRECT" if correction else "FINANCIAL_CORRECTION_REVIEWED" if _continuation else
                                    "INITIAL_DIRECT" if variant == "default" else "INITIAL_REVIEWED", fixture=True)
    seeds, seed_events, seed_writes = {}, [], []
    if _continuation:
        parent = _continuation["parent"]
        if correction:
            from .source_correction import validate_saved_correction
            validate_saved_correction(root, store, parent, prior[1], _continuation["draft"])
        elif parent["artifacts"]["extractor"]["payload"]["wire"] != case.wire.model_dump():
            raise InputError("REASSESSMENT_CANNOT_REUSE_CHANGED_EXTRACTION")
        for name in STAGES[:2]:
            payload = parent["artifacts"][name]["payload"]
            if name == "pdf_input":
                payload = {**payload, "dependency_digest": case.dependency_digest}
                if correction:
                    payload["source_profile"] = case.registration.source_profile_version
            elif correction:
                payload = dict(wire=case.wire.model_dump(), provenance="REVIEWER_SOURCE_CORRECTION", provider_requests=0,
                    correction_event_id=_continuation["event_id"], original_extraction_digest=parent["artifacts"]["extractor"]["content_digest"])
            artifact = dict(stage=name, scope=scope.model_dump(), case_dependency_digest=case.dependency_digest,
                            input_digest=fingerprint("NORMAL_STAGE_INPUT", seeds), payload=payload)
            artifact["content_digest"] = fingerprint("NORMAL_STAGE_ARTIFACT", artifact)
            seeds[name] = artifact
            event = dict(sequence=len(seed_events) + 1, run_id=scope.run_id, stage=name, event="reviewer_correction_applied" if correction and name == "extractor" else "artifact_reused",
                         parent_run_id=parent["context"]["scope"]["run_id"], artifact_digest=artifact["content_digest"],
                         timestamp=datetime.now(timezone.utc).isoformat())
            seed_events.append(event)
            seed_writes.extend((RecordWrite("normal-artifact:" + scope.run_id + ":" + name, "NORMAL_FIXTURE_ARTIFACT", artifact),
                                RecordWrite(f"normal-event:{scope.run_id}:{event['sequence']}", "NORMAL_FIXTURE_EVENT", event)))
    receipt = _resume["receipt"] if _resume is not None else store.admit(operation_id, scope.model_dump(), {"action": {"E-M01": "RUN_E_M01_MISSING_FIXTURE", "E-F03": "RUN_E_F03_REJECT_FIXTURE", "E-P01": "RUN_E_P01_CONDITIONAL_FIXTURE"}.get(scenario_id, "RUN_E_N01_NORMAL_FIXTURE"), "context": context},
        writes=(RecordWrite(context_key, "NORMAL_FIXTURE_CONTEXT", context, prior[0] if correction else 0),
                RecordWrite(ledger_key, "BUDGET_LEDGER", initial_ledger.to_dict(), _continuation["ledger_version"] if _continuation else 0),
                RecordWrite(result_key, "NORMAL_FIXTURE_OUTCOME", dict(status="RUNNING", scope=scope.model_dump()), store.get_record(result_key)[0] if correction else 0))
                + tuple(seed_writes) + (() if _continuation is None else tuple(_continuation["writes"])))
    if receipt.duplicate:
        saved = store.get_record(result_key)
        if saved is None:
            raise InputError("EXISTING_OPERATION_RESULT_MISSING")
        return {**saved[1], "duplicate": True,
                "status": saved[1]["status"] if receipt.state == "RELEASED" else "RECOVERY_REQUIRED"}
    initial = dict(version="E-N01-GRAPH-1.0", context=context, artifacts=seeds, events=seed_events,
                   ledger=initial_ledger.to_dict(), status="RUNNING", report_markdown=None, report_metadata=None)
    progress_key = "normal-progress:" + operation_id
    started = time.perf_counter()
    order = STAGES if variant != "review" else STAGES[:-1] + ("review_prepare", "human_review", "report_generator")
    from .financial_review import prepare_request, request_key, validate_human_record

    def check_state(state, name):
        store.assert_claim(receipt)
        if state["version"] != "E-N01-GRAPH-1.0" or state["context"] != context:
            raise InputError("NORMAL_GRAPH_CONTEXT_CHANGED")
        if tuple(state["artifacts"]) != order[:order.index(name)]:
            raise InputError("NORMAL_GRAPH_STAGE_DEPENDENCY_MISMATCH")
        for artifact in state["artifacts"].values():
            content = {key: value for key, value in artifact.items() if key != "content_digest"}
            if artifact["content_digest"] != fingerprint("NORMAL_STAGE_ARTIFACT", content):
                raise InputError("NORMAL_GRAPH_ARTIFACT_CHANGED")
            persisted = store.get_record("normal-artifact:" + scope.run_id + ":" + artifact["stage"])
            if persisted is None or persisted[1] != artifact:
                raise InputError("NORMAL_GRAPH_HANDOFF_NOT_CURRENT_RECORD")
        saved = store.get_record(ledger_key)
        if saved is None or saved[1] != state["ledger"]:
            raise InputError("NORMAL_GRAPH_LEDGER_MISMATCH")
        return saved

    def perform(name, state):
        if name == "pdf_input":
            current = load_registered_case(root, profile=profile, scenario_id=scenario_id)
            if current.dependency_digest != case.dependency_digest:
                raise InputError("NORMAL_SOURCE_CHANGED_AFTER_ADMISSION")
            return dict(dependency_digest=current.dependency_digest, source_pages=len(current.inventory),
                        source_profile=current.registration.source_profile_version)
        if name == "extractor":
            return dict(wire=case.wire.model_dump(), provenance="REGISTERED_EXTRACTION_FIXTURE", provider_requests=0)
        if name == "financial_analyst":
            if state["artifacts"]["extractor"]["payload"]["wire"] != case.wire.model_dump():
                raise InputError("NORMAL_EXTRACTION_HANDOFF_CHANGED")
            return primitive(asdict(compute_financials(case)))
        if name == "compliance_check":
            financial = restore_financial(state["artifacts"]["financial_analyst"]["payload"])
            return primitive(asdict(compute_compliance(case, financial)))
        if name == "risk_quantifier":
            financial = restore_financial(state["artifacts"]["financial_analyst"]["payload"])
            compliance = restore_compliance(state["artifacts"]["compliance_check"]["payload"])
            return primitive(asdict(compute_risk(case, financial, compliance)))
        if name == "synthesizer":
            panels = (restore_financial(state["artifacts"]["financial_analyst"]["payload"]),
                      restore_compliance(state["artifacts"]["compliance_check"]["payload"]),
                      restore_risk(state["artifacts"]["risk_quantifier"]["payload"]))
            current_packet = prepare_synthesis(case, panels=panels)
            return validate_fixture_synthesis(root, case, current_packet, scope, operation_id, variant=variant)
        if name == "evidence_review":
            expected = validate_fixture_synthesis(root, case, packet, scope, operation_id, variant=variant)
            if state["artifacts"]["synthesizer"]["payload"] != expected:
                raise InputError("NORMAL_SYNTHESIS_ARTIFACT_CHANGED")
            # Validate recorded handoffs against the same registered case. These
            # are ordinary Python reference checks, not additional agent calls.
            f, c, r = evaluate_panels(case)
            for stage, value in (("financial_analyst", f), ("compliance_check", c), ("risk_quantifier", r)):
                if state["artifacts"][stage]["payload"] != primitive(asdict(value)):
                    raise InputError("NORMAL_PANEL_HANDOFF_CHANGED")
            return dict(status=expected["evidence_status"], narrative_targets=len(expected["targets"]),
                        unsupported_claims=[], human_supported=False, input_digest=packet["input_digest"])
        if name == "route_review":
            routing = state["artifacts"]["synthesizer"]["payload"]["routing"]
            if routing["workflow"] != ("ESCALATE" if scenario_id in ("E-F03", "E-P01") else "CONTINUE" if variant == "default" else "REVIEW_REQUIRED"):
                raise InputError("NORMAL_FIXTURE_REVIEW_BRANCH_UNAVAILABLE")
            from .readiness_service import assess_current, proposal
            assessment=assess_current(store,context,state["artifacts"],receipt)
            return {**routing,"ai_proposal":proposal(state["artifacts"],"FIXTURE"),"approval_readiness":assessment.model_dump(),"human_decision":None}
        if name == "review_prepare":
            return prepare_request(scope, state["artifacts"]["synthesizer"]["payload"],
                                   state["artifacts"]["evidence_review"]["content_digest"])
        if name == "human_review":
            if _resume is None:
                raise InputError("FINANCIAL_REVIEW_ACCEPTED_RECEIPT_REQUIRED")
            human = _resume["human_record"]
            current = store.get_record(request_key(scope.run_id))
            if current is None or current[1].get("human_record") != human:
                raise InputError("FINANCIAL_REVIEW_RECEIPT_NOT_CURRENT")
            if scenario_id in ("E-F03", "E-P01"):
                from .command_center import get_run
                from .financial_review import get_financial_review
                from .review import Actor
                actor = Actor("AuthorizedApprover", scope.workspace_id, frozenset({scope.deal_id}), frozenset({"NORMAL"}))
                get_financial_review(store, actor, get_run(store, actor, operation_id))
            validate_human_record(human, scope)
            if human["event"]["decision"] in ("Approve","Conditional Approve"):
                from .readiness_service import require_approval
                recorded=human["event"].get("approval_readiness",{})
                require_approval(store,dict(context=context,artifacts=state["artifacts"],status="WAITING_REVIEW"),recorded.get("version"),recorded.get("assessment_digest"))
            return human
        if name == "report_generator":
            from .readiness_service import assess_current
            correction_event = None
            if correction:
                from .source_correction import validate_saved_correction
                event = validate_saved_correction(root, store, _continuation["parent"], context, _continuation["draft"])
                correction_event = {key: value for key, value in event.items() if key != "analysis_snapshot"}
            return render_memo(ReportInput(scope, packet, state["artifacts"]["synthesizer"]["payload"],
                                           tuple(state["events"]), generation_time if variant == "default" and not correction else datetime.now(timezone.utc).isoformat(),
                                           state["artifacts"].get("human_review", {}).get("payload"), correction_event,
                                           assess_current(store,context,state["artifacts"],receipt).model_dump()))
        raise InputError("UNREGISTERED_STAGE")

    def action(name):
        def invoke(state):
            saved = check_state(state, name)
            ledger = Ledger.from_dict(saved[1])
            reservation = operation_id + ":" + name
            maximum = Usage(nodes=1, tools=int(name in TOOL_STAGES), active_ms=ledger.operation_timeout_ms())
            if name == "human_review":
                from langgraph.types import interrupt
                signal = interrupt({"request_id": state["artifacts"]["review_prepare"]["payload"]["request"]["request_id"],
                                    "provenance": "EXECUTED_FIXTURE_REVIEW"})
                if _resume is None or signal != {"operation_id": _resume["receipt"].operation_id}:
                    raise InputError("WRONG_FINANCIAL_RESUME_SIGNAL")
                reserved = ledger
                if reservation not in reserved.reservations:
                    raise InputError("HUMAN_NODE_RESERVATION_MISSING")
                event = state["events"][-1]
                if event["stage"] != name or event["event"] != "stage_started":
                    raise InputError("HUMAN_NODE_START_MISSING")
                working = state
                ledger_version = saved[0]
            else:
                reserved = ledger.reserve(reservation, maximum)
                event = dict(sequence=len(state["events"]) + 1, run_id=scope.run_id, stage=name, event="stage_started",
                             timestamp=datetime.now(timezone.utc).isoformat())
                event_key = f"normal-event:{scope.run_id}:{event['sequence']}"
                with store.transaction() as connection:
                    store._write(connection, RecordWrite(ledger_key, "BUDGET_LEDGER", reserved.to_dict(), saved[0]))
                    store._write(connection, RecordWrite(event_key, "NORMAL_FIXTURE_EVENT", event))
                working = {**state, "events": state["events"] + [event]}
                ledger_version = saved[0] + 1
            clock = time.perf_counter()
            payload = primitive(perform(name, working))
            elapsed = max(1, math.ceil((time.perf_counter() - clock) * 1000))
            usage = Usage(nodes=1, tools=int(name in TOOL_STAGES), active_ms=elapsed)
            completed = reserved.settle(reservation, usage)
            if name == "review_prepare":
                completed = completed.reserve(operation_id + ":human_review",
                    Usage(nodes=1, active_ms=completed.operation_timeout_ms()))
            artifact = dict(stage=name, scope=scope.model_dump(), case_dependency_digest=case.dependency_digest,
                            input_digest=fingerprint("NORMAL_STAGE_INPUT", state["artifacts"]), payload=payload)
            artifact["content_digest"] = fingerprint("NORMAL_STAGE_ARTIFACT", artifact)
            end_event = dict(sequence=event["sequence"] + 1, run_id=scope.run_id, stage=name,
                             event="stage_completed", artifact_digest=artifact["content_digest"], active_ms=elapsed,
                             timestamp=datetime.now(timezone.utc).isoformat())
            updated = {**working, "artifacts": {**state["artifacts"], name: artifact},
                       "events": working["events"] + [end_event], "ledger": completed.to_dict()}
            if name == "risk_quantifier" and missing:
                if (payload["score"]["total"] is not None or payload["score"]["band"] is not None
                        or payload["score"]["status"] != "INSUFFICIENT_DATA"
                        or state["artifacts"]["compliance_check"]["payload"]["workflow"] != "NEEDS_INFORMATION"
                        or "financial_input:cash_available_for_debt_service" not in payload["score"]["missing"]):
                    raise InputError("MISSING_CASE_EXPECTED_ABSTENTION_CHANGED")
                updated["status"] = "WAITING_INFORMATION"
            if name == "route_review":
                updated.update(ai_proposal=payload["ai_proposal"],approval_readiness=payload["approval_readiness"],human_decision=None)
                updated["status"] = "REPORT_ALLOWED" if variant == "default" else "WAITING_REVIEW"
            if name == "human_review":
                updated["human_decision"]=payload["event"]
                updated["approval_readiness"]=payload["event"].get("approval_readiness")
                updated["status"] = "REPORT_ALLOWED"
            if name == "report_generator":
                updated.update(status="REPORT_GENERATED", report_markdown=payload["markdown"], report_metadata=payload["metadata"])
            prior_progress = store.get_record(progress_key)
            with store.transaction() as connection:
                store._write(connection, RecordWrite(ledger_key, "BUDGET_LEDGER", completed.to_dict(), ledger_version))
                store._write(connection, RecordWrite("normal-artifact:" + scope.run_id + ":" + name,
                                                    "NORMAL_FIXTURE_ARTIFACT", artifact))
                store._write(connection, RecordWrite(f"normal-event:{scope.run_id}:{end_event['sequence']}",
                                                    "NORMAL_FIXTURE_EVENT", end_event))
                if name == "review_prepare":
                    store._write(connection, RecordWrite(request_key(scope.run_id), "FINANCIAL_REVIEW", payload))
                    pause_event = dict(sequence=end_event["sequence"] + 1, run_id=scope.run_id,
                                       stage="human_review", event="stage_started", timestamp=datetime.now(timezone.utc).isoformat())
                    updated["events"] = updated["events"] + [pause_event]
                    store._write(connection, RecordWrite(f"normal-event:{scope.run_id}:{pause_event['sequence']}",
                                                         "NORMAL_FIXTURE_EVENT", pause_event))
                store._write(connection, RecordWrite(progress_key, "NORMAL_FIXTURE_PROGRESS", updated,
                                                    0 if prior_progress is None else prior_progress[0]))
            return updated
        return invoke

    try:
        from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
        from langgraph.checkpoint.sqlite import SqliteSaver
        with closing(sqlite3.connect(config.database, check_same_thread=False)) as connection:
            serializer = JsonPlusSerializer(pickle_fallback=False, allowed_json_modules=None, allowed_msgpack_modules=None)
            graph = build_graph({name: action(name) for name in order},
                                checkpointer=SqliteSaver(connection, serde=serializer))
            invocation = {"configurable": {"thread_id": scope.thread_id}, "recursion_limit": 20}
            if _resume is not None:
                from langgraph.types import Command
                prior_checkpoint = graph.get_state(invocation)
                if prior_checkpoint.next != ("human_review",) or prior_checkpoint.values["context"] != context:
                    raise InputError("FINANCIAL_PENDING_CHECKPOINT_REQUIRED")
                result = graph.invoke(Command(resume={"operation_id": receipt.operation_id}), invocation)
            else:
                result = graph.invoke(initial, invocation)
            checkpoint = graph.get_state(invocation)
            if missing and result["status"] == "WAITING_INFORMATION":
                if (checkpoint.next or tuple(result["artifacts"]) != STAGES[:5] or result["report_markdown"] is not None
                        or checkpoint.values != result):
                    raise InputError("MISSING_CASE_PAUSE_CHECKPOINT_MISMATCH")
                outcome = dict(status="WAITING_INFORMATION", evidence_type="EXECUTED_FIXTURE_MISSING_DATA",
                    scope=scope.model_dump(), report_markdown=None, report_metadata=None, provider_requests=0,
                    human_disposition=None, human_credit_review="Unavailable until missing CFADS is supplied and validated",
                    missing_items=list(result["artifacts"]["risk_quantifier"]["payload"]["score"]["missing"]),
                    requested_information=["Supply the annual cash available for debt service (CFADS) schedule for the stated 2027 assessment period."],
                    continuation_status="SOURCE_BACKED_CORRECTION_AVAILABLE" if profile == "extraction-miss" else "NOT_IMPLEMENTED_NO_REPLACEMENT_DOCUMENT_ACCEPTED",
                    stages=list(result["artifacts"]), audit_events=result["events"], ledger=result["ledger"], duplicate=False)
                from .readiness_service import assess_current, proposal
                outcome.update(ai_proposal=proposal(result["artifacts"],"FIXTURE"),approval_readiness=assess_current(store,context,result["artifacts"],receipt).model_dump(),human_decision=None)
                saved_outcome = store.get_record(result_key)
                store.put_record(RecordWrite(result_key, "NORMAL_FIXTURE_OUTCOME", outcome, saved_outcome[0]))
                store.release(receipt, confirmed_idle=True)
                return outcome
            if "__interrupt__" in result:
                if variant != "review" or checkpoint.next != ("human_review",) or result["status"] != "WAITING_REVIEW":
                    raise InputError("FINANCIAL_PAUSE_CHECKPOINT_MISMATCH")
                outcome = dict(status="WAITING_REVIEW", evidence_type="EXECUTED_FIXTURE_REVIEW", scope=scope.model_dump(), report_markdown=None, report_metadata=None,
                               provider_requests=0, human_disposition=None, human_credit_review="RiskManager exception handling then NORMAL AuthorizedApprover required" if scenario_id == "E-F03" else "NORMAL AuthorizedApprover required",
                               stages=list(result["artifacts"]), audit_events=result["events"], ledger=result["ledger"], duplicate=False)
                from .readiness_service import assess_current, proposal
                outcome.update(ai_proposal=proposal(result["artifacts"],"FIXTURE"),approval_readiness=assess_current(store,context,result["artifacts"],receipt).model_dump(),human_decision=None)
                saved_outcome = store.get_record(result_key)
                store.put_record(RecordWrite(result_key, "NORMAL_FIXTURE_OUTCOME", outcome, saved_outcome[0]))
                store.release(receipt, confirmed_idle=True)
                return outcome
            if (checkpoint.next or "__interrupt__" in result or result["status"] != "REPORT_GENERATED"
                    or not result["report_markdown"] or checkpoint.values["report_metadata"] != result["report_metadata"]):
                raise InputError("NORMAL_GRAPH_REPORT_OR_TERMINAL_CHECKPOINT_MISSING")
        if (time.perf_counter() - started) * 1000 > 180000:
            raise InputError("NORMAL_WORKER_ACTIVE_TIME_EXHAUSTED")
        outcome = dict(status="COMPLETED", evidence_type="EXECUTED_FIXTURE_NORMAL_ONLY", scope=scope.model_dump(),
                       report_markdown=result["report_markdown"], report_metadata=result["report_metadata"],
                       stages=list(result["artifacts"]), audit_events=result["events"], ledger=result["ledger"],
                       provider_requests=0, billed_tokens=None, actual_model_cost_usd=None,
                       model_usage_status="NOT_APPLICABLE_FIXTURE", human_disposition=None,
                       human_credit_review="Not required by configured demo rules", duplicate=False)
        if variant == "review":
            human = result["artifacts"]["human_review"]["payload"]
            outcome.update(human_disposition=human["event"]["decision"], human_credit_review="Completed by simulated AuthorizedApprover",
                           evidence_type="EXECUTED_FIXTURE_REVIEW")
        from .readiness_service import assess_current, proposal
        outcome.update(ai_proposal=proposal(result["artifacts"],"FIXTURE"),approval_readiness=assess_current(store,context,result["artifacts"],receipt).model_dump(),human_decision=result["artifacts"].get("human_review",{}).get("payload",{}).get("event"))
        saved_outcome = store.get_record(result_key)
        store.put_record(RecordWrite(result_key, "NORMAL_FIXTURE_OUTCOME", outcome, saved_outcome[0]))
        store.release(receipt, confirmed_idle=True)
        return outcome
    except BaseException:
        # Never auto-replay across an uncertain node/app-record/checkpoint gap.
        store.mark_unknown(receipt)
        raise
