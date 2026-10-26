"""Local pre-publication audit. Never prints or persists matched secret values.

Uses an isolated temporary Git index to evaluate this checkout's ignore rules.
Does not initialize, commit or publish the actual project. Not a replacement for
reviewing an eventual Git history or GitHub-side secret scanning.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import base64,json,os,re,subprocess
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=ROOT/'var/security-audit';out.mkdir(parents=True,exist_ok=True)
    secrets=set()
    env=ROOT/'.env'
    if env.exists():
        for line in env.read_text(encoding='utf-8-sig').splitlines():
            name,sep,value=line.partition('=')
            if sep and re.search(r'key|token|secret|password',name,re.I):
                value=value.strip().strip('\"\'')
                if len(value)>=12 and value not in ('your_key_here','REPLACE_ME'):secrets.add(value)
    for name,value in os.environ.items():
        if re.search(r'(?:API_KEY|ACCESS_TOKEN|SECRET_ACCESS_KEY|CLIENT_SECRET)$',name) and len(value)>=12:secrets.add(value)
    needles=set()
    for value in secrets:
        raw=value.encode();needles.add(raw);needles.add(base64.b64encode(raw))
    patterns={
        'PRIVATE_KEY':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
        'AWS_ACCESS_KEY':re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
        'GITHUB_TOKEN':re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),
        'API_TOKEN_PATTERN':re.compile(r'\bsk-[A-Za-z0-9_-]{24,}\b'),
        'JWT_LITERAL':re.compile(r'\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b'),
    }
    findings=[];privacy=[];notebooks=[];binary=[]
    def inspect(path,text):
        if any(n in text.encode('utf-8',errors='replace') for n in needles):findings.append(dict(path=path,kind='CONFIGURED_SECRET_MATCH'))
        for kind,pattern in patterns.items():
            if pattern.search(text):findings.append(dict(path=path,kind=kind))
        if re.search(r'[A-Za-z]:[\\/](?:Users|code)[\\/]',text):privacy.append(path)
    with TemporaryDirectory(prefix='git-ignore-check-',dir=out) as temporary:
        subprocess.run(['git','init','--quiet',temporary],check=True,capture_output=True)
        git=['git','-c','core.excludesFile=NUL','--git-dir='+str(Path(temporary)/'.git'),'--work-tree='+str(ROOT)]
        raw=subprocess.run(git+['ls-files','--others','--exclude-standard','-z'],check=True,capture_output=True).stdout
        candidates=sorted(p.decode('utf-8') for p in raw.split(b'\0') if p)
        excluded={}
        for name in ('.env','.streamlit/secrets.toml','var/deal_review.sqlite3','var/deal_review.sqlite3-wal','.venv/example','sample.log','.aws/credentials'):
            excluded[name]=subprocess.run(git+['check-ignore','--no-index','--quiet',name],capture_output=True).returncode==0
        for name in candidates:
            path=ROOT/name
            if not path.is_file():continue
            data=path.read_bytes()
            if any(n in data for n in needles):findings.append(dict(path=name,kind='CONFIGURED_SECRET_BYTES_MATCH'))
            suffix=path.suffix.lower()
            if suffix=='.pdf':
                try:
                    from pypdf import PdfReader
                    inspect(name,'\n'.join(p.extract_text() or '' for p in PdfReader(path).pages))
                except Exception:findings.append(dict(path=name,kind='PDF_CONTENT_NOT_SCANNED'))
            elif suffix=='.ipynb':
                notebook=json.loads(data)
                count=sum(bool(c.get('outputs')) or c.get('execution_count') is not None for c in notebook.get('cells',[]) if c.get('cell_type')=='code')
                notebooks.append(dict(path=name,executed_or_output_cells=count))
                if count:findings.append(dict(path=name,kind='NOTEBOOK_OUTPUT_REVIEW_REQUIRED'))
                inspect(name,data.decode('utf-8',errors='replace'))
            elif b'\0' in data[:8192]:binary.append(name)
            else:inspect(name,data.decode('utf-8',errors='replace'))
        result=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
            scope='PROPOSED_NEW_REPOSITORY_FILES_ONLY_NOT_GITHUB_OR_HISTORY',
            files_scanned=len(candidates),configured_credentials_checked=bool(secrets),
            findings=findings,exclusion_checks=excluded,notebooks=notebooks,
            local_path_privacy_review=sorted(set(privacy)),other_binary_files=binary,
            limitations=['No Git history exists in the actual workspace.','No GitHub repository or remote was inspected.','Pattern matching cannot prove absence of every possible secret or personal datum.'])
        (out/'publication-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        (out/'candidate-files.txt').write_text('\n'.join(candidates),encoding='utf-8')
    print(json.dumps(result,indent=2))
    return 1 if findings or not all(excluded.values()) else 0


if __name__=='__main__':raise SystemExit(main())
