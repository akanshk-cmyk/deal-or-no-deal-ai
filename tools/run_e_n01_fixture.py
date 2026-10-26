"""Explicit normal Fixture run and local demo export; no paid/live option."""

import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.context import InputError, canonical_json
from deal_or_no_deal_ai.worker import run_normal_fixture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation-id", help="Reuse the same UUID to read the existing result without replay.")
    parser.add_argument("--variant", choices=("default", "review"), default="default")
    args = parser.parse_args()
    operation_id = args.operation_id or str(uuid4())
    outcome = run_normal_fixture(ROOT, operation_id, variant=args.variant)
    if outcome["status"] != "COMPLETED":
        print(json.dumps(dict(status=outcome["status"], operation_id=operation_id, provider_requests=0)))
        return 0 if outcome["status"] == "WAITING_REVIEW" else 2
    directory = ROOT / "var/demos/e-n01" / outcome["scope"]["run_id"]
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in (("credit-memo.md", outcome["report_markdown"]),
                       ("run.json", canonical_json({**outcome, "duplicate": False}) + "\n")):
        path = directory / name
        if path.exists():
            # A duplicate-read marker is command provenance, not a new report.
            if path.read_text(encoding="utf-8") != text:
                raise InputError("EXISTING_DEMO_REPORT_CHANGED")
        else:
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
    print(json.dumps(dict(status=outcome["status"], operation_id=operation_id,
                          run_id=outcome["scope"]["run_id"], report=str((directory / "credit-memo.md").relative_to(ROOT)),
                          nodes=outcome["ledger"]["committed"]["nodes"],
                          tools=outcome["ledger"]["committed"]["tools"], provider_requests=0,
                          human_credit_review=outcome["human_credit_review"], duplicate=outcome["duplicate"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
