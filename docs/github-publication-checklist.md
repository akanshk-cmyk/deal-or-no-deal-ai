# GitHub publication checklist

The local pre-publication audit checks proposed repository files without creating
a repository, publishing files, or calling Nebius. Run from the project root:

```powershell
.venv\Scripts\python.exe tools\audit_publish_secrets.py
```

The report and candidate-file list are saved under ignored `var/security-audit/`.
The audit compares candidate contents with locally configured credentials without
printing those values, checks common credential patterns, extracts PDF text, and
checks notebook outputs. It is a diagnostic, not a guarantee that every possible
secret or personal detail has been detected. It currently audits a proposed new
repository, not an existing commit history or a GitHub repository.

Before the first commit:

- Keep `.env`, Streamlit secrets, credentials, logs, runtime uploads, databases,
  caches and local environments excluded. `.env.example` contains no key.
- Review the candidate list. Publish only authored code, documentation and
  intentionally shared synthetic examples. Do not add real borrower documents,
  public-source snapshots or runtime review records.
- Keep notebook execution outputs cleared. Review generated reports separately
  for confidential content before including them.
- After staging files, inspect `git diff --cached --name-only` and the staged
  changes locally. Confirm excluded files have not been force-added.
- Review the actual staged snapshot and any commits for secrets before pushing;
  the proposed-file audit does not cover those snapshots.
- Choose the destination repository and visibility deliberately. A project license
  has not been selected automatically.

If a credential is ever committed or published, revoke or rotate it with its
provider and remove it from repository history. Adding an ignore rule afterward
does not remove an existing commit or make an exposed key safe.

## Local audit result — 2026-10-26

The initial scan examined 403 candidate files and found no configured-credential
matches or common secret-pattern findings. All seven exclusion probes passed.
The one notebook had no saved execution outputs. No other unscanned binary files
or matching local machine paths were reported. This result predates this checklist;
rerun the audit before staging the final publication snapshot.

No Git repository or remote existed in the inspected workspace. No GitHub content
or commit history was inspected, and nothing was published by this audit.
