"""Export the two submission drafts locally; no network or model calls."""
from pathlib import Path
from html import escape
import re
from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
EDGE=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')


def diagram():
    nodes=[
        (200,12,320,46,['New Deal: upload and validate PDFs']),
        (200,80,320,46,['Confirm reporting context']),
        (200,148,320,46,['Extraction Agent — Nebius']),
        (200,216,320,46,['Human fact / profile verification']),
        (16,296,216,60,['Financial Specialist','Python calculations']),
        (252,296,216,60,['Compliance Specialist','Python policy checks']),
        (488,296,216,60,['Risk Specialist','Python flags / ratings']),
        (200,390,320,46,['Join validated specialist outputs']),
        (200,458,320,46,['Synthesizer — Nebius']),
        (200,526,320,46,['Human narrative verification']),
        (200,594,320,46,['Deterministic readiness gate']),
        (200,662,320,46,['Python report generator']),
        (200,730,320,46,['Review Workspace / Credit Memo']),
        (200,798,320,46,['Separate human decision / History']),
    ]
    edges=[(360,58,360,80),(360,126,360,148),(360,194,360,216),
           (360,262,124,296),(360,262,360,296),(360,262,596,296),
           (124,356,360,390),(360,356,360,390),(596,356,360,390)]
    edges += [(360,y+46,360,y+68) for y in (390,458,526,594,662,730)]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 865" role="img" aria-label="Uploaded review architecture"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#52708c"/></marker></defs>']
    for x1,y1,x2,y2 in edges:
        svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#52708c" stroke-width="2" marker-end="url(#arrow)"/>')
    for x,y,w,h,lines in nodes:
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#edf4fa" stroke="#abc2d6"/>')
        for i,line in enumerate(lines):
            baseline=y+h/2+(i-(len(lines)-1)/2)*19+5
            svg.append(f'<text x="{x+w/2}" y="{baseline}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#16334d">{escape(line)}</text>')
    svg.append('</svg>')
    return '<figure class="architecture">'+''.join(svg)+'<figcaption>LangGraph coordinates state, checkpoints and stage routing; SQLite retains records. Agent Activity reads recorded events. Diagram: new uploaded-review path.</figcaption></figure>'


def render(path):
    md=MarkdownIt('commonmark',{'html':False}).enable('table')
    original=md.renderer.rules['fence']
    def fence(tokens,idx,options,env):
        if tokens[idx].info.strip()=='mermaid':return diagram()
        return original(tokens,idx,options,env)
    md.renderer.rules['fence']=fence
    body=md.render(path.read_text(encoding='utf-8'))
    # Relative repo references stay readable without exposing machine-specific URLs.
    body=re.sub(r' href="(?!https?://|#)[^"]*"','',body)
    summary='github-submission' in path.stem
    css='''
    @page { size:A4; margin:17mm 15mm 18mm; }
    * { box-sizing:border-box; }
    body { font-family:Arial,sans-serif; color:#203248; font-size:10pt; line-height:1.44; }
    h1 { font-size:25pt; color:#102a43; line-height:1.14; margin:0 0 10pt; }
    h2 { font-size:16pt; color:#146078; margin:14pt 0 8pt; }
    h3 { font-size:13pt; color:#16334d; margin:17pt 0 7pt; }
    h1,h2,h3,h4 { break-after:avoid; }
    p { margin:0 0 8pt; }
    ul,ol { margin:5pt 0 10pt; padding-left:19pt; }
    li { margin:2pt 0; }
    table { border-collapse:collapse; width:100%; margin:10pt 0 14pt; font-size:8.6pt; line-height:1.36; table-layout:fixed; }
    thead { display:table-header-group; }
    th { background:#16334d; color:white; text-align:left; }
    th,td { border:1px solid #d7e2eb; padding:6pt; vertical-align:top; overflow-wrap:anywhere; }
    tr { break-inside:avoid; }
    tbody tr:nth-child(even) { background:#f3f7fa; }
    code { font-size:9pt; overflow-wrap:anywhere; }
    a { color:#12647c; text-decoration:none; }
    strong { color:#142f48; }
    .architecture { break-inside:avoid; margin:10pt auto; max-width:157mm; }
    .architecture svg { width:100%; height:auto; max-height:205mm; }
    figcaption { color:#52677d; font-size:8.3pt; margin-top:6pt; }
    '''
    if summary:css+='body { font-size:9.7pt; line-height:1.29; } h1 { font-size:22pt; } h2 { font-size:11.5pt; margin:10pt 0 5pt; } p { margin-bottom:6pt; } li { margin:1pt 0; }'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><title>'+escape(path.stem)+'</title><style>'+css+'</style><body>'+body+'</body></html>'


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suffix',default='',help='Version suffix when an existing PDF is open, e.g. -v2')
    args=parser.parse_args()
    if args.suffix and not re.fullmatch(r'-[A-Za-z0-9-]+',args.suffix):parser.error('Use an alphanumeric version suffix starting with a dash')
    out=ROOT/'var/evaluations/submission-pdf'
    out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(EDGE),headless=True)
        page=browser.new_page()
        page.route('**/*',lambda route:route.abort())
        for name in ('weekly-project-report','github-submission-summary'):
            source=DOCS/(name+'.md');html=render(source)
            (out/(name+'.html')).write_text(html,encoding='utf-8')
            page.set_content(html,wait_until='load')
            page.emulate_media(media='print')
            target=DOCS/(name+args.suffix+'.pdf')
            page.pdf(path=str(target),format='A4',print_background=True,prefer_css_page_size=True,
                     display_header_footer=True,header_template='<span></span>',
                     footer_template='<div style="font:8px Arial;color:#64748b;width:100%;text-align:center">Deal or No Deal AI · Educational project · Draft submission &nbsp; | &nbsp; <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            reader=PdfReader(target)
            text='\n'.join(pg.extract_text() or '' for pg in reader.pages)
            assert 'Deal or No Deal AI' in text and len(text)>1500
            assert 'mermaid' not in text
            print(f'{target.name}: {len(reader.pages)} pages, {target.stat().st_size} bytes')
        browser.close()


if __name__=='__main__':main()
