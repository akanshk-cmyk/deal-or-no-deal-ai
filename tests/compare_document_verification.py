"""Explicit offline comparison; no providers, models, parser or auto-discovery IO."""

import json
from pathlib import Path

from tests.document_verification_cases import compare_cases


if __name__ == "__main__":
    report = compare_cases()
    destination = Path("var/evaluations/document-verification-paired.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(dict(report_file=str(destination), unique_cases=report["unique_case_count"],
                          paired_executions=report["paired_execution_count"], failures=report["failures"])))
    raise SystemExit(bool(report["failures"]))
