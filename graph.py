"""Shared saved-response and explicitly gated Live graph; compilation performs no I/O."""

from typing import TypedDict,Annotated

from .context import InputError


STAGES = ("pdf_input", "extractor", "financial_analyst", "compliance_check", "risk_quantifier",
          "synthesizer", "evidence_review", "route_review", "report_generator")
TOOL_STAGES = frozenset(("financial_analyst", "compliance_check", "risk_quantifier", "evidence_review"))


class FixtureState(TypedDict):
    version: str
    context: dict
    artifacts: dict
    events: list[dict]
    ledger: dict
    status: str
    report_markdown: str | None
    report_metadata: dict | None
    pending_stage: str | None
    ai_proposal: dict | None
    approval_readiness: dict | None
    human_decision: dict | None


def merge_panels(left,right):
    if set(left)&set(right):raise InputError('DUPLICATE_SPECIALIST_OUTPUT')
    return {**left,**right}


class PanelState(TypedDict):
    panels: Annotated[dict,merge_panels]


def run_specialist_branches(actions):
    """Actual fan-out/join; branches return disjoint data, never shared DB writes."""
    from langgraph.graph import START,END,StateGraph
    graph=StateGraph(PanelState)
    names=('financial_analyst','compliance_check','risk_quantifier')
    if set(actions)!=set(names):raise InputError('THREE_SPECIALIST_BRANCHES_REQUIRED')
    for name in names:
        def branch(state,name=name):return {'panels':{name:actions[name]()}}
        graph.add_node(name,branch);graph.add_edge(START,name)
    graph.add_node('specialist_join',lambda s:{})
    graph.add_edge(list(names),'specialist_join');graph.add_edge('specialist_join',END)
    return graph.compile().invoke({'panels':{}},{'max_concurrency':3})['panels']


def build_graph(actions: dict, *, checkpointer=None, live=False, parallel_specialists=False):
    from langgraph.graph import END, START, StateGraph
    if live:
        if set(actions) != set(STAGES) | {"fact_review", "review_prepare", "human_review"} | ({'specialist_panel'} if parallel_specialists else set()):
            raise InputError("EXACT_LIVE_GRAPH_STAGES_REQUIRED")
        graph = StateGraph(FixtureState)
        for name, action in actions.items():
            if parallel_specialists and name in ('financial_analyst','compliance_check','risk_quantifier'):continue
            graph.add_node(name, action)
        order = STAGES[:2] + ("fact_review",) + STAGES[2:]
        if parallel_specialists:order=STAGES[:2]+('fact_review','specialist_panel')+STAGES[5:]
        graph.add_edge(START, order[0])
        for before, after in zip(order, order[1:]):
            if before == "fact_review":
                graph.add_conditional_edges(before, lambda s: "next" if s["status"] == "RUNNING" else "stop", {"next": after, "stop": END})
            elif before in ("risk_quantifier","specialist_panel"):
                graph.add_conditional_edges(before, lambda s: "next" if s["status"] == "RUNNING" else "stop", {"next": after, "stop": END})
            elif before == "route_review":
                graph.add_conditional_edges(before, lambda s: "report" if s["status"] == "REPORT_ALLOWED" else "review" if s["status"] == "WAITING_REVIEW" else "stop", {"report": after, "review": "review_prepare", "stop": END})
            else:
                graph.add_edge(before, after)
        graph.add_edge("review_prepare", "human_review")
        graph.add_edge("human_review", "report_generator")
        graph.add_edge("report_generator", END)
        return graph.compile(checkpointer=checkpointer)
    reviewed = set(actions) == set(STAGES) | {"review_prepare", "human_review"}
    if set(actions) != set(STAGES) and not reviewed:
        raise InputError("EXACT_NORMAL_GRAPH_STAGES_REQUIRED")
    graph = StateGraph(FixtureState)
    for name in actions:
        graph.add_node(name, actions[name])
    if reviewed:
        graph.add_edge("review_prepare", "human_review")
        graph.add_edge("human_review", "report_generator")
    graph.add_conditional_edges(START, lambda state: state["context"].get("entry_stage", STAGES[0]),
                                {STAGES[0]: STAGES[0], "financial_analyst": "financial_analyst"})
    for before, after in zip(STAGES, STAGES[1:]):
        if before == "risk_quantifier":
            graph.add_conditional_edges(before, lambda state: "information" if state["status"] == "WAITING_INFORMATION" else "synthesize",
                                        {"information": END, "synthesize": after})
        elif before == "route_review":
            graph.add_conditional_edges(before, lambda state: "report" if state["status"] == "REPORT_ALLOWED"
                                        else "review" if state["status"] == "WAITING_REVIEW" and reviewed else "stop",
                                        {"report": after, "stop": END, **({"review": "review_prepare"} if reviewed else {})})
        else:
            graph.add_edge(before, after)
    graph.add_edge(STAGES[-1], END)
    return graph.compile(checkpointer=checkpointer)
