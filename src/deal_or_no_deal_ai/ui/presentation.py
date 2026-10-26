"""Local presentation only. All dynamic HTML is escaped; no remote assets."""
from .labels import friendly, FINANCIAL_HELP, case_label


from html import escape


CSS = """
<style>
:root { --ink:#10233f; --muted:#52647c; --line:#dbe3ee; --teal:#087e8b; }
.stApp { background:#f4f7fb; }
.block-container { max-width:1500px; padding-top:4.5rem; padding-bottom:3rem; }
h1,h2,h3 { color:var(--ink); letter-spacing:-.025em; }
h1 { font-size:2rem !important; } h2 { font-size:1.45rem !important; }
[data-testid="stSidebar"] { background:#10233f; }
[data-testid="stSidebar"] :is(p,label,span,h1,h2,h3) { color:#e6edf7; }
[data-testid="stSidebar"] [data-baseweb="select"] :is(span,div) { color:#10233f; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color:#bdcce0; }
[data-testid="stSidebar"] [data-testid="stAlert"] :is(p,span,label,li) { color:#10233f !important; }
[data-testid="stSidebar"] [data-testid="stCode"] { background:#f8fafc; border-radius:8px; }
[data-testid="stSidebar"] [data-testid="stCode"] :is(pre,code,span) { color:#10233f !important; background:#f8fafc !important; font-size:13px; }
[data-testid="stSidebar"] [data-testid="stJson"] :is(span,label) { color:#10233f !important; }
[data-testid="stSidebar"] button[kind="secondary"] :is(p,span) { color:#10233f !important; }
[data-testid="stMetric"] { background:white; border:1px solid var(--line); border-radius:14px; padding:18px 20px; }
[data-testid="stMetricValue"] { font-variant-numeric:tabular-nums; }
button { min-height:44px; border-radius:9px !important; }
button:focus-visible, input:focus-visible, [role="tab"]:focus-visible { outline:3px solid #1599ab !important; outline-offset:3px; }
[data-testid="stTabs"] [role="tablist"] { gap:16px; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] [role="tab"] { padding:10px 2px; }
.eyebrow { font-size:12px; letter-spacing:.13em; font-weight:700; color:#52647c; text-transform:uppercase; margin:0 0 8px; }
.brand { color:white; font-size:25px; font-weight:750; line-height:1.15; margin-bottom:10px; }
.brand-accent { color:#65d6de; } .brand-sub { color:#bdcce0; font-size:13px; }
.demo-strip { background:#eaf4f7; color:#14556a; border:1px solid #b9d8df; border-radius:8px; padding:9px 14px; font-size:13px; margin-bottom:24px; }
.context-card { border:1px solid var(--line); border-left:4px solid var(--teal); background:white; border-radius:12px; padding:20px 24px; margin:14px 0 20px; }
.context-title { font-size:22px; font-weight:700; margin-bottom:6px; color:var(--ink); }
.context-meta { color:var(--muted); font-size:14px; line-height:1.8; overflow-wrap:anywhere; }
.pill { display:inline-block; padding:4px 10px; font-size:12px; font-weight:650; border-radius:6px; background:#eef2f7; color:#42546c; margin:8px 7px 0 0; }
.pill-info { background:#e8f0ff; color:#1e40af; } .pill-warn { background:#fff3dc; color:#864a0c; }
.surface { background:white; border:1px solid var(--line); border-radius:12px; padding:20px; margin:8px 0 16px; }
.surface-label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
.surface-value { font-size:24px; color:var(--ink); font-weight:700; margin:8px 0; }
.surface-note { color:var(--muted); font-size:14px; line-height:1.55; overflow-wrap:anywhere; }
.stage { background:white; border:1px solid var(--line); border-top:3px solid #a4b0c1; border-radius:10px; padding:15px; min-height:130px; margin-bottom:12px; }
.stage-done { border-top-color:#087e8b; } .stage-active { border-top-color:#c47a12; }
.stage-num { color:#52647c; font-size:12px; } .stage-name { font-weight:700; color:var(--ink); margin:8px 0; }
.stage-state { font-size:13px; color:#52647c; }
.milestone { background:white; border:1px solid var(--line); border-left:3px solid #087e8b; border-radius:8px; padding:15px 20px; margin:12px 0; }
[data-testid="stMarkdownContainer"] { overflow-wrap:anywhere; }
@media (max-width:760px) { .block-container { padding:4.5rem 1rem 1rem; } .context-card { padding:16px; } .context-title { font-size:19px; } }
</style>
"""


def safe(value):
    return escape(str(value), quote=True)


def surface(st, label, value, note=""):
    st.markdown('<div class="surface"><div class="surface-label">' + safe(label)
                + '</div><div class="surface-value">' + safe(value)
                + '</div><div class="surface-note">' + safe(note) + '</div></div>', unsafe_allow_html=True)


WORKSPACE_TABS = ("Overview", "Extracted Terms", "Financial Analysis", "Compliance", "Risk Assessment", "Human Review")


def context_header(st, run, terms, *, answer_source="Saved AI responses"):
    scope = run["context"]["scope"]
    borrower = terms.get("borrower", {}).get("value") or "Borrower not available"
    amount = terms.get("requested_amount", {}).get("value")
    currency = terms.get("currency", {}).get("value") or ""
    from decimal import Decimal
    amount_label = "Amount not available" if amount is None else f"{currency} {Decimal(amount):,.0f}"
    st.markdown('<div class="context-card"><div class="eyebrow">Commercial lending / ' + safe(case_label(run["context"]["scenario_id"])) + '</div>'
                + '<div class="context-title">' + safe(borrower) + '</div>'
                + '<div class="context-meta">' + safe(amount_label) + ' · Term loan · Review version '
                + safe(scope["input_revision"]) + '<br>Deal ' + safe(scope["deal_id"])
                + '</div>'
                + '<span class="pill pill-info">' + safe(friendly(run["status"]))
                + '</span><span class="pill">Readiness: ' + safe(run.get("approval_readiness",{}).get("outcome","Pending Review")) + '</span><span class="pill">Human decision: ' + safe(run["human_disposition"] or "Not recorded")
                + '</span><span class="pill">Fictional deal data</span><span class="pill">' + safe(answer_source) + '</span></div>', unsafe_allow_html=True)
