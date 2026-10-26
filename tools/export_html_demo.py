"""Explicit read-only export of scoped fixture records; no provider or graph run."""
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def render(root):
    from deal_or_no_deal_ai.command_center import list_runs, policy_display, source_packet, workspace_id
    from deal_or_no_deal_ai.configuration import load_configuration
    from deal_or_no_deal_ai.context import strict_json
    from deal_or_no_deal_ai.financial_review import financial_history
    from deal_or_no_deal_ai.review import Actor
    from deal_or_no_deal_ai.storage import Store
    config = load_configuration(root)
    registration = strict_json((root / "config/registrations/e-n01.json").read_bytes())
    actor = Actor("Analyst", workspace_id(root), frozenset({registration["deal_id"]}))
    store = Store(config.database)
    runs = list_runs(store, actor)
    pages = ("Deal Dashboard", "New Deal", "Review Workspace", "Agent Activity", "Credit Memo", "Decision History")
    selected = runs[0] if runs else None
    packet = source_packet(root, selected) if selected else None
    refs = policy_display(selected, packet)["references"] if packet else {}
    events = financial_history(store, actor, registration["deal_id"]) if runs else []
    header = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Deal or No Deal AI — offline snapshot</title>'
    style = '<style>body{margin:0;font:16px/1.6 system-ui;background:#f4f7fb;color:#10233f}aside{background:#10233f;color:white;padding:24px;width:230px;position:fixed;height:100vh}main{margin-left:280px;padding:32px;max-width:1050px}button,select{font:inherit;min-height:44px;padding:8px 14px;margin:5px;border:1px solid #52647c;border-radius:8px}aside button{display:block;width:100%;text-align:left;background:#eef4fa;color:#10233f}button:focus-visible,select:focus-visible{outline:3px solid #087e8b}.card{background:white;border:1px solid #dbe3ee;border-radius:12px;padding:22px;margin:18px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 system-ui}.notice{background:#eaf4f7;padding:12px;border-left:4px solid #087e8b}section[hidden]{display:none}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid #dbe3ee}@media(max-width:760px){aside{position:static;width:auto;height:auto}main{margin:0;padding:16px}}</style>'
    nav = '<aside><h2>Deal or No Deal AI</h2><p>AI credit intelligence</p>' + ''.join('<button data-page="' + str(i) + '">' + escape(name) + '</button>' for i, name in enumerate(pages)) + '<p>Educational offline snapshot</p></aside>'
    shared = '<main><p class="notice">Recorded fictional example data · Offline snapshot · No actions, model calls or live updates</p>'
    if selected:
        shared += '<div class="card"><strong>Example Equipment LLC · USD 1,200,000</strong><p>Run ' + escape(selected["context"]["scope"]["run_id"]) + '</p><p>Execution: ' + escape(selected["status"]) + ' · Human decision: ' + escape(selected["human_disposition"] or "Not recorded") + '</p></div>'
        from deal_or_no_deal_ai.recommendation import from_run
        recommendation=from_run(selected)
        shared += '<div class="card"><h2>Current approval readiness</h2><p><strong>'+escape(recommendation["outcome"])+'</strong></p><p>'+escape(recommendation["brief_reason"])+'</p><p>Next action: '+escape(recommendation["next_action"])+'</p><p>Review source: Saved example responses. An original AI proposal is not an authorized credit decision.</p></div>'
    bodies = []
    bodies.append('<p>' + str(len({r["context"]["scope"]["deal_id"] for r in runs})) + ' recorded deal(s) · ' + str(len(runs)) + ' recorded run(s).</p><button data-page="2">Open review workspace</button>')
    bodies.append('<div class="card"><h3>Standard Deal sample package</h3><p>Five registered source pages.</p><button disabled>Run AI Deal Review — use the local Streamlit application</button><p>This snapshot does not upload documents or execute the graph.</p></div>')
    if packet:
        rows = ''.join('<tr><th scope="row">' + escape(k.replace('_', ' ').title()) + '</th><td>' + escape(str(v["value"])) + '</td></tr>' for k, v in packet["request"]["terms"].items())
        workspace = '<div class="card"><h3>Extracted terms</h3><table>' + rows + '</table></div><label for="source">Supporting evidence</label><select id="source">' + ''.join('<option value="' + escape(k, quote=True) + '">' + escape(k) + '</option>' for k in refs) + '</select><pre id="evidence" class="card"></pre>'
    else:
        workspace = '<p>No recorded financial analysis. Run a registered sample in the local app first.</p>'
    bodies.append(workspace)
    bodies.append('<pre class="card">' + escape(json.dumps(selected["events"] if selected else [], indent=2)) + '</pre>')
    bodies.append('<p class="notice">Preserved historical memo. Current readiness appears above; the original AI proposal does not clear mandatory blockers.</p><pre class="card">' + escape(selected["outcome"].get("report_markdown") or "No completed memo for the selected run." if selected else "No recorded memo.") + '</pre>')
    bodies.append('<p>Actual financial review events only. Illustrative preview actions are excluded.</p><pre class="card">' + escape(json.dumps(events, indent=2, ensure_ascii=False) if events else "No human decisions recorded.") + '</pre>')
    sections = ''.join('<section id="page-' + str(i) + '"' + (' hidden' if i else '') + '><h1 tabindex="-1">' + escape(name) + '</h1>' + body + '</section>' for i, (name, body) in enumerate(zip(pages, bodies)))
    payload = json.dumps(refs, ensure_ascii=False).replace('<', '\\u003c')
    script = '<script type="application/json" id="sources">' + payload + '</script><script>document.querySelectorAll("[data-page]").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll("section").forEach(s=>s.hidden=s.id!=="page-"+b.dataset.page);document.querySelector("section:not([hidden]) h1").focus()}));const r=JSON.parse(document.getElementById("sources").textContent);const s=document.getElementById("source");function show(){document.getElementById("evidence").textContent=JSON.stringify(r[s.value],null,2)}if(s){s.addEventListener("change",show);show()}</script>'
    return header + style + nav + shared + sections + '</main>' + script + '</html>'


def main():
    destination = ROOT / "prototype/index.html"
    if destination.exists():
        raise ValueError("OFFLINE_SNAPSHOT_EXISTS_PRESERVE_OR_EXPLICITLY_VERSION_IT")
    content = render(ROOT)
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
