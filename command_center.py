"""Read-only, scope-checked financial projections of existing worker records."""

from pathlib import Path
from copy import deepcopy
from uuid import NAMESPACE_URL, UUID, uuid5

from .context import InputError, fingerprint, strict_json
from .review import Actor
from .storage import Store


ROLES = ("Analyst", "RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator")


def workspace_id(root: Path) -> str:
    return str(uuid5(NAMESPACE_URL, str(root.resolve(strict=True))))


def start_run(root: Path, actor: Actor, operation_id: str, *, variant: str = "default", scenario_id: str = "E-N01") -> dict:
    """Authorize before any worker admission or database initialization."""
    if scenario_id not in ("E-N01", "E-M01", "E-F03", "E-P01"):
        raise InputError("REGISTERED_SCENARIO_REQUIRED")
    registry = strict_json((root / ("config/registrations/" + scenario_id.lower() + ".json")).read_bytes())
    _scope(actor, dict(workspace_id=workspace_id(root), deal_id=registry["deal_id"]))
    if actor.persona != "Analyst":
        raise InputError("FINANCIAL_RUN_START_NOT_PERMITTED")
    from .worker import run_normal_fixture
    return run_normal_fixture(root, operation_id, variant=variant, scenario_id=scenario_id)


def _scope(actor: Actor, scope: dict) -> None:
    if (actor.attribution != "SIMULATED" or actor.persona not in ROLES
            or actor.workspace_id != scope["workspace_id"]
            or scope["deal_id"] not in actor.allowed_deal_ids):
        raise InputError("FINANCIAL_RUN_OUT_OF_SCOPE")


def _read(connection, key):
    row = connection.execute("SELECT payload FROM app_records WHERE record_key=?", (key,)).fetchone()
    return None if row is None else strict_json(row[0], envelope=True)


def list_runs(store: Store, actor: Actor) -> list[dict]:
    """No initialization/seed or write on read; filter before exposing counts."""
    if not store.path.exists():
        return []
    with store.connection() as connection:
        connection.execute("BEGIN")
        exists = connection.execute("SELECT 1 FROM sqlite_master WHERE name='app_records'").fetchone()
        if not exists:
            return []
        rows = connection.execute("SELECT payload FROM app_records WHERE kind='NORMAL_FIXTURE_CONTEXT'").fetchall()
        results = []
        for row in rows:
            context = strict_json(row[0])
            try:
                _scope(actor, context["scope"])
            except InputError:
                continue
            results.append(_project(connection, context))
        results = sorted(results, key=lambda run: (run["context"]["generation_time"], run["operation_id"]), reverse=True)
    return [_review_projection(store, actor, run) for run in results]


def get_run(store: Store, actor: Actor, operation_id: str) -> dict:
    if str(UUID(operation_id)) != operation_id or not store.path.exists():
        raise InputError("FINANCIAL_RUN_UNAVAILABLE")
    with store.connection() as connection:
        connection.execute("BEGIN")
        context = _read(connection, "normal-context:" + operation_id)
        if context is None:
            live=_read(connection,"live-context:"+operation_id)
            if live is None:
                raise InputError("FINANCIAL_RUN_UNAVAILABLE")
            _scope(actor,live["scope"])
        else:
            _scope(actor,context["scope"])
            run=_project(connection,context)
    if context is None:
        from .live_worker import load_live
        state=load_live(store.path.parent.parent,actor,operation_id)
        run=dict(operation_id=operation_id,context=state["context"],status=state["status"],artifacts=state["artifacts"],events=state["events"],outcome=state,human_disposition=state.get("human_decision",{}).get("decision") if state.get("human_decision") else None)
        from .readiness_service import projection
        run.update(projection(store,run))
        return run
    return _review_projection(store, actor, run)


def _review_projection(store, actor, run):
    """Expose only validated current handling status, never a new clearance flag."""
    from .financial_review import get_financial_review
    if run["context"]["scenario_id"] in ("E-F03", "E-P01"):
        panel = get_financial_review(store, actor, run)
        run["unhandled_exception_ids"] = ([] if panel is None else
            [r.key.split(":", 1)[1] for r in panel["request"].requirements if r.key.startswith("exception:") and not r.satisfied])
        if panel is not None and run["context"]["scenario_id"] == "E-P01":
            request = panel["request"]
            run["pending_condition_roles"] = (["AuthorizedApprover"] if panel["data"].get("condition_draft") is None else
                [role for domain, role in (("FINANCIAL_RISK", "RiskManager"), ("POLICY_CONTROL", "ComplianceOfficer"))
                 if any(not r.satisfied and r.key.endswith(":" + domain) for r in request.requirements)])
    from .readiness_service import projection
    run.update(projection(store,run))
    return run


def _project(connection, context):
    operation_id, scope = context["operation_id"], context["scope"]
    outcome = _read(connection, "normal-result:" + operation_id)
    progress = _read(connection, "normal-progress:" + operation_id)
    claim = connection.execute("SELECT state FROM app_operations WHERE operation_id=?", (operation_id,)).fetchone()
    ready_correction = (outcome is not None and outcome.get("status") == "READY" and context.get("profile") == "correction" and claim is None)
    if outcome is None or outcome["scope"] != scope or claim is None and not ready_correction:
        raise InputError("FINANCIAL_RUN_RECORD_MISMATCH")
    status = outcome["status"]
    if ready_correction:
        draft = _read(connection, "source-correction:" + operation_id)
        if draft is None or draft.get("state") != "READY" or draft.get("context") != context:
            raise InputError("READY_CORRECTION_RECORD_MISMATCH")
    elif claim[0] != "RELEASED":
        status = "RECOVERY_REQUIRED" if claim[0] == "RECOVERY_REQUIRED" else "RUNNING"
    active_rows = connection.execute("SELECT state,scope_payload FROM app_operations WHERE review_id=? AND state!='RELEASED'",
                                (scope["review_id"],)).fetchall()
    active = [row for row in active_rows if strict_json(row["scope_payload"])["run_id"] == scope["run_id"]]
    if active:
        status = "RECOVERY_REQUIRED" if any(row[0] == "RECOVERY_REQUIRED" for row in active) else "RUNNING"
    artifacts = {} if progress is None else progress["artifacts"]
    if progress is not None and progress["context"] != context:
        raise InputError("FINANCIAL_RUN_CONTEXT_MISMATCH")
    for stage, artifact in artifacts.items():
        content = {key: value for key, value in artifact.items() if key != "content_digest"}
        if (artifact["scope"] != scope or artifact["stage"] != stage
                or artifact["case_dependency_digest"] != context["case_dependency_digest"]
                or artifact["content_digest"] != fingerprint("NORMAL_STAGE_ARTIFACT", content)
                or _read(connection, "normal-artifact:" + scope["run_id"] + ":" + stage) != artifact):
            raise InputError("FINANCIAL_RUN_ARTIFACT_MISMATCH")
    if status == "COMPLETED":
        report = artifacts.get("report_generator", {}).get("payload", {})
        if (not report or outcome.get("report_markdown") != report.get("markdown")
                or outcome.get("report_metadata") != report.get("metadata")):
            raise InputError("FINANCIAL_RUN_REPORT_MISMATCH")
        if "human_review" in artifacts:
            from .financial_review import validate_human_record
            from .contracts import Scope
            human = artifacts["human_review"]["payload"]
            validate_human_record(human, Scope.model_validate(scope))
            if outcome.get("human_disposition") != human["event"]["decision"]:
                raise InputError("FINANCIAL_RUN_DISPOSITION_MISMATCH")
    events = [strict_json(row[0]) for row in connection.execute(
        "SELECT payload FROM app_records WHERE kind='NORMAL_FIXTURE_EVENT' AND record_key LIKE ?",
        ("normal-event:" + scope["run_id"] + ":%",)).fetchall()]
    events.sort(key=lambda event: event["sequence"])
    if any(event["run_id"] != scope["run_id"] or event["sequence"] != index
           for index, event in enumerate(events, 1)):
        raise InputError("FINANCIAL_RUN_EVENT_MISMATCH")
    return dict(operation_id=operation_id, context=context, status=status,
                outcome=outcome, artifacts=artifacts, events=events,
                provenance=outcome.get("evidence_type", "EXECUTED_FIXTURE_NORMAL_ONLY"), human_disposition=outcome.get("human_disposition"))


def source_packet(root: Path, run: dict) -> dict:
    """Resolve only the run's registered source version; never substitute latest."""
    from .services import load_registered_case
    from .synthesis import prepare_synthesis, prepare_source_inspection
    if run["context"]["mode"]=="LIVE":
        from .live_worker import _live_case
        from .live_context import prepare_live_tasks
        from .panel_codec import restore_financial,restore_compliance,restore_risk
        from .upload_live import case_for_context
        # get_run already enforces the actor; this resolver receives its scoped run.
        from .review import Actor
        scope=run['context']['scope']
        reader=Actor('Analyst',scope['workspace_id'],frozenset({scope['deal_id']}))
        base=case_for_context(root,reader,run['context'])
        tasks=prepare_live_tasks(root,case=base) if run['context'].get('upload_origin') else prepare_live_tasks(root)
        binding=fingerprint("LIVE_SOURCE_AND_PROMPTS",dict(case=base.dependency_digest,instructions={k:v["instruction"] for k,v in tasks.items()},schemas={k:v["schema"] for k,v in tasks.items()},
            **({"verification_policy":"DEMO_DRAFT"} if run["context"].get("verification_policy")=="DEMO_DRAFT" else {})))
        if binding!=run["context"]["source_binding"]:
            raise InputError("LIVE_SOURCE_OR_PROMPT_CHANGED")
        case=_live_case(base,run,Store(root/"var/deal_review.sqlite3"))
        original=run["artifacts"]["synthesizer"]["payload"]["packet"]
        panels=(restore_financial(run["artifacts"]["financial_analyst"]["payload"]),restore_compliance(run["artifacts"]["compliance_check"]["payload"]),restore_risk(run["artifacts"]["risk_quantifier"]["payload"]))
        if original!=prepare_synthesis(case,panels=panels):
            raise InputError("LIVE_RECORDED_SOURCE_MISMATCH")
        return original
    scenario = run["context"]["scenario_id"]
    case = load_registered_case(root, profile=run["context"].get("profile", "default"), scenario_id=scenario)
    packet = prepare_source_inspection(case) if scenario == "E-M01" or run["context"].get("profile") == "extraction-miss" else prepare_synthesis(case)
    context = run["context"]
    if (case.dependency_digest != context["case_dependency_digest"]
            or packet["input_digest"] != context["synthesis_input_digest"]):
        raise InputError("RECORDED_SOURCE_VERSION_UNAVAILABLE")
    return packet


def policy_display(run: dict, packet: dict | None) -> dict:
    """Project recorded policy state, never recalculate or rewrite history.

    Call with a scoped get_run/list_runs result. Source references additionally
    require the exact registered packet; unavailable sources yield no links.
    """
    context = run["context"]
    artifacts = run["artifacts"]
    synthesis_artifact = artifacts.get("synthesizer")
    final = synthesis_artifact is not None
    live=context.get("mode")=="LIVE"
    if live:
        artifact=artifacts.get("route_review") or artifacts.get("compliance_check")
        final="route_review" in artifacts
        panel=None
        if artifact is not None:
            content={k:v for k,v in artifact.items() if k!="digest"}
            if (artifact["source_binding"]!=context["source_binding"]
                    or artifact["digest"]!=fingerprint("LIVE_ARTIFACT",content)):
                raise InputError("LIVE_POLICY_DISPLAY_ARTIFACT_MISMATCH")
            panel=artifact["payload"]["final_policy"] if final else artifact["payload"]
        dependency=artifacts.get("financial_analyst",{}).get("payload",{}).get("dependency_digest")
    elif final:
        synthesis = synthesis_artifact["payload"]
        if (synthesis_artifact["scope"] != context["scope"]
                or synthesis["input_digest"] != context["synthesis_input_digest"]
                or synthesis["case_dependency_digest"] != context["case_dependency_digest"]):
            raise InputError("POLICY_DISPLAY_SYNTHESIS_MISMATCH")
        panel = synthesis["routing"]["final_policy"]
    else:
        panel = artifacts.get("compliance_check", {}).get("payload")
    if not live:
        dependency=context["case_dependency_digest"]
    refs = {}
    if packet is not None:
        if live and synthesis_artifact is None:
            raise InputError("LIVE_POLICY_DISPLAY_SYNTHESIS_REQUIRED")
        expected_input=(synthesis_artifact["payload"]["packet"]["input_digest"] if live else context["synthesis_input_digest"])
        if (packet["input_digest"] != expected_input
                or packet["case_dependency_digest"] != dependency
                or packet["input_digest"] != fingerprint("E-N01-SYNTHESIS-INPUT-1.0",
                    {k: v for k, v in packet.items() if k != "input_digest"})):
            raise InputError("POLICY_DISPLAY_SOURCE_MISMATCH")
        refs = deepcopy(packet["request"]["reference_dictionary"])
    if panel is None:
        return dict(basis="NOT_CHECKED", rules=[], exception_rule_ids=None, references=refs)
    if panel["dependency_digest"] != dependency:
        raise InputError("POLICY_DISPLAY_DEPENDENCY_MISMATCH")
    rows = []
    for rule in panel["rules"]:
        if rule["dependency_digest"] != panel["dependency_digest"] or rule["policy_version"] != panel["policy_version"]:
            raise InputError("POLICY_DISPLAY_RULE_MISMATCH")
        handle = f"policy:{rule['policy_version']}:{rule['rule_id']}"
        if packet is not None:
            if handle not in refs:
                raise InputError("POLICY_DISPLAY_REFERENCE_MISSING")
            # Same recorded rule and dependency representation used by the memo.
            refs[handle] = {**refs[handle], "value": deepcopy(rule),
                            "refs": [ref for ref in rule["source_refs"] if ref != handle]}
        result = "Pending" if rule["evaluation_state"] == "NOT_EVALUATED" else rule["outcome"] or rule["control_result"] or "Pending"
        rows.append(dict(ref=handle, result=result,
                         result_kind="Policy outcome" if rule["outcome"] is not None else "Workflow control",
                         state=rule["evaluation_state"], observed=rule["observed"], threshold=rule["threshold"],
                         predicate=rule["predicate"], workflow=rule["workflow"], reason=rule["reason"]))
    return dict(basis="POST_SYNTHESIS_RECORDED" if final else "PRE_SYNTHESIS_PRELIMINARY",
                rules=rows, exception_rule_ids=list(panel["exception_rule_ids"]), references=refs)
