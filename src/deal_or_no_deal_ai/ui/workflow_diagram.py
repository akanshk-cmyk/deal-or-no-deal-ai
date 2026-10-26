"""Local SVG derived from the same compiled LangGraph. No network rendering."""
from html import escape
from ..graph import STAGES, build_graph


def workflow_svg(*, reviewed=True, live=False):
    stages = STAGES[:-1] + ("review_prepare", "human_review", "report_generator") if reviewed else STAGES
    if live:
        stages=STAGES+("fact_review","review_prepare","human_review")
    graph = build_graph({stage: lambda state: state for stage in stages},live=live).get_graph()
    nodes = list(graph.nodes)
    positions = {node: (180, 45 + index * 85) for index, node in enumerate(nodes)}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Compiled financial review workflow" viewBox="0 0 560 {len(nodes)*85+20}">',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#52647c"/></marker></defs>']
    for index, edge in enumerate(graph.edges):
        x1, y1 = positions[edge.source]
        x2, y2 = positions[edge.target]
        if abs(y2-y1) <= 90:
            path = f'M{x1},{y1+24} L{x2},{y2-24}'
        else:
            side = 350 + (index % 4) * 35
            path = f'M{x1+120},{y1} C{side},{y1} {side},{y2} {x2+120},{y2}'
        dash = 'stroke-dasharray="5 4"' if edge.conditional else ''
        parts.append(f'<path d="{path}" fill="none" stroke="#52647c" {dash} marker-end="url(#arrow)"/>')
    for node, (x, y) in positions.items():
        label = node.strip('_').replace('_', ' ').title()
        parts.append(f'<rect x="{x-120}" y="{y-24}" width="240" height="48" rx="10" fill="#eef6f8" stroke="#087e8b"/>')
        parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#10233f">{escape(label)}</text>')
    return ''.join(parts) + '</svg>'
