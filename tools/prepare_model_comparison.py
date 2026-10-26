"""Explicit offline paired-input preparation; intentionally no live-run option."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.context import InputError, canonical_json
from deal_or_no_deal_ai.model_comparison import prepare_comparison


def main():
    if sys.argv[1:]:
        raise InputError("OFFLINE_PREPARATION_ONLY_NO_EXECUTION_FLAGS")
    report = prepare_comparison(ROOT)
    destination = ROOT / "var/evaluations/generation-comparison" / report["plan_digest"] / "readiness.json"
    serialized = canonical_json(report) + "\n"
    if destination.exists():
        if destination.read_text(encoding="utf-8") != serialized:
            raise InputError("EXISTING_COMPARISON_ARTIFACT_CHANGED")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    print(json.dumps(dict(status="PREPARED_OFFLINE_NOT_RUN",
                          report=str(destination.relative_to(ROOT)),
                          prepared_task_packets=len(report["task_packets"]), comparison_arms=len(report["arms"]),
                          provider_requests=0, winner=None)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
