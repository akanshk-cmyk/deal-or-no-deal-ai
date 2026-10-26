"""Read-only specialist/dependency views of scoped recorded workflow outputs.

These are derived presentation rows, not new messages, receipts or clearances.
No worker, provider, store or graph invocation belongs in this module.
"""
from .presentation import surface
from .labels import friendly


SPECIALISTS = (
    ("Extraction Specialist", ("extractor",),
     "Extracts source-linked terms and financial inputs.",
     "Live: model extraction. Saved example: preserved response."),
    ("Compliance Specialist", ("compliance_check",),
     "Evaluates synthetic policy rules using supported inputs and calculations.",
     "Deterministic Python policy service; no LLM call or waiver authority."),
    ("Risk and Summary Specialist", ("risk_quantifier", "synthesizer"),
     "Combines explainable risk scoring with evidence-linked AI observations.",
     "Python scoring plus the existing synthesis stage; no extra model stage."),
)

DEPENDENCIES = (
    ("Extraction Specialist", "Financial Calculation Service", ("extractor",),
     "financial_analyst", "Extracted values, sources and reporting basis"),
    ("Financial Calculation Service", "Compliance Specialist", ("financial_analyst",),
     "compliance_check", "Calculated metrics and their source references"),
    ("Financial Calculation Service", "Risk and Summary Specialist", ("financial_analyst",),
     "risk_quantifier", "Financial metrics and missing-input findings"),
    ("Compliance Specialist", "Risk and Summary Specialist", ("compliance_check",),
     "risk_quantifier", "Policy findings and workflow requirements"),
    ("Financial / Compliance / Risk services", "Synthesis", ("financial_analyst", "compliance_check", "risk_quantifier"),
     "synthesizer", "Combined findings, illustrative score drivers and evidence"),
    ("Synthesis and evidence checks", "Orchestrator readiness routing", ("synthesizer", "evidence_review"),
     "route_review", "Original AI proposal and evidence-check results"),
)


def _record(run, stage):
    """Match an artifact to an existing current-run output event, not a start."""
    artifact = run["artifacts"].get(stage)
    if artifact is None:
        return None
    digest = artifact.get("content_digest") or artifact.get("digest")
    events = [e for e in run["events"] if e.get("stage") == stage
              and e.get("event") in ("stage_completed", "artifact_reused", "reviewer_correction_applied")
              and e.get("run_id") == run["context"]["scope"]["run_id"]
              and digest is not None and e.get("artifact_digest") == digest]
    if not events:
        return None
    event = max(events, key=lambda e:e["sequence"])
    return dict(stage=stage, digest=digest, sequence=event["sequence"],
                timestamp=event.get("timestamp") or "Not captured", event=event["event"])


def project(run):
    """Accept only an already scoped get_run/list_runs result. Never persist."""
    live = run["context"].get("mode") == "LIVE"
    pending = run.get("outcome", {}).get("pending_stage")
    records = {stage:_record(run, stage) for stage in run["artifacts"]}
    roles = []
    for name, stages, purpose, implementation in SPECIALISTS:
        done = [s for s in stages if records.get(s)]
        status = "Findings recorded" if len(done) == len(stages) else "Partly recorded" if done else "Not started"
        if any(s in run["artifacts"] and not records.get(s) for s in stages):
            status = "Output event not confirmed"
        if live and name == "Extraction Specialist" and pending == "fact_review":
            status = "Extracted facts await human verification"
        if live and name == "Risk and Summary Specialist" and pending == "evidence_review":
            status = "AI conclusions await human verification"
        if run["status"] == "WAITING_INFORMATION" and name == "Risk and Summary Specialist":
            status = "Incomplete information; no complete summary"
        roles.append(dict(name=name, stages=stages, status=status, purpose=purpose,
                          implementation=implementation, recorded_stages=done))
    transfers = []
    for sender, recipient, sources, destination, result in DEPENDENCIES:
        parents = [records.get(s) for s in sources]
        child = records.get(destination)
        ready = all(parents)
        ordered = ready and child is not None and all(p["sequence"] < child["sequence"] for p in parents)
        status = "Downstream result recorded" if ordered else "Awaiting upstream result" if not ready else "Awaiting downstream result"
        if child is not None and not ordered:
            status = "Dependency record not confirmed"
        if live and destination == "financial_analyst" and pending == "fact_review":
            status = "Waiting for human fact verification"
        if live and destination == "route_review" and pending == "evidence_review":
            status = "Waiting for human conclusion verification"
        transfers.append(dict(sender=sender, recipient=recipient, result=result,
                              status=status, review_version=run["context"]["scope"]["input_revision"],
                              source_records=[p for p in parents if p], destination_record=child))
    if run['context'].get('parallel_specialists'):
        transfers=[]
        for stage,recipient in (('financial_analyst','Financial Specialist'),('compliance_check','Compliance Specialist'),('risk_quantifier','Risk Specialist')):
            parent=records.get('fact_review');child=records.get(stage)
            transfers.append(dict(sender='Verified Extraction',recipient=recipient,result='Same verified upload input; branch runs independent deterministic tools',status='Downstream result recorded' if parent and child else 'Awaiting verified input or branch result',review_version=run['context']['scope']['input_revision'],source_records=[parent] if parent else [],destination_record=child))
        parents=[records.get(n) for n in ('financial_analyst','compliance_check','risk_quantifier')]
        transfers.append(dict(sender='Three joined specialists',recipient='Synthesizer',result='Financial, policy and risk outputs joined before synthesis',status='Downstream result recorded' if all(parents) and records.get('synthesizer') else 'Awaiting all three branches or synthesis',review_version=run['context']['scope']['input_revision'],source_records=[p for p in parents if p],destination_record=records.get('synthesizer')))
    if run["status"] in ("RECOVERY_REQUIRED", "MODEL_OUTPUT_INVALID"):
        next_action = "Inspect technical recovery or validation details. Do not replay an uncertain model request."
    elif live:
        from .live_workflow import _next_action
        next_action = _next_action(run["outcome"])
    elif run["status"] == "WAITING_INFORMATION":
        next_action = "Review the missing information request. Dependent analysis must not invent missing values."
    elif run["status"] == "WAITING_REVIEW":
        next_action = "Follow the required role and permitted actions in Human Review."
    else:
        next_action = "Inspect recorded findings, current approval readiness and the memo. Completion is not credit approval."
    return dict(source="Live AI response · Nebius" if live else "Saved example responses",
                roles=roles, handoffs=transfers, next_action=next_action,
                workflow_status=friendly(run["status"]), scope=run["context"]["scope"])


def render(st, run):
    view = project(run)
    st.subheader("Specialist team and coordination")
    st.caption("Hybrid workflow: three specialist roles, two normal live model stages, deterministic financial controls. These are not three autonomous LLM agents.")
    st.caption("Recorded review source: " + view["source"])
    for index, (column, role) in enumerate(zip(st.columns(3), view["roles"]), 1):
        surface(column, str(index)+" / "+role["name"], role["status"], role["purpose"])
        column.caption(role["implementation"])
    st.write("**Orchestrator — LangGraph**")
    flow = "parallel specialist branches and their join" if run['context'].get('parallel_specialists') else "existing sequence"
    st.write("Coordinates the "+flow+", shared state, checkpoints, budgets, missing-information stops and human-review routing. It uses no planning LLM call.")
    st.info("Next action: " + view["next_action"])
    st.subheader("Specialist handoffs")
    st.caption("Read-only view of existing dependencies and output events. A downstream result is not a separate message receipt, verified evidence or credit approval. No history is created by viewing this page.")
    st.dataframe([{"From":row["sender"], "To":row["recipient"], "Shared result":row["result"],
                   "Review version":str(row["review_version"]), "Recorded progress":row["status"]}
                  for row in view["handoffs"]], hide_index=True, width="stretch")
    with st.expander("Technical details: recorded handoff references"):
        st.json(dict(scope=view["scope"], dependencies=view["handoffs"]))
    st.caption("Supporting services: document validation, exact financial calculations, evidence checks, readiness, human credit review where routed, and Python report generation. Risk scoring and synthesis remain separate internal stages.")
