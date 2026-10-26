"""Retain and inspect an explicitly supplied local response; no Live option."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pydantic import ValidationError
from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.quality_review import review_capture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="Local QUALITY-CAPTURE-1.0 JSON file")
    args = parser.parse_args()
    try:
        with args.capture.open("rb") as stream:
            raw = stream.read(262145)
        result = review_capture(ROOT, raw)
    except (OSError, InputError, ValidationError):
        # Validation exceptions can contain rejected financial text: never print them.
        print(json.dumps(dict(status="OFFLINE_REVIEW_FAILED", tool_provider_requests=0)))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
