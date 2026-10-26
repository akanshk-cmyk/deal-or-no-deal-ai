"""Explicit local-file inspection, not a crawler, indexer or loan-review run."""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.public_sources import inspect_uploaded_reference, load_reference_profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Explicit user-supplied public-reference HTML or text PDF")
    parser.add_argument("--html-encoding", choices=("utf-8", "windows-1252"), default="utf-8")
    args = parser.parse_args()
    profile = load_reference_profile(ROOT)
    try:
        path = args.file.resolve(strict=True)
        if not path.is_file():
            raise InputError("REFERENCE_FILE_REQUIRED")
        with path.open("rb") as stream:
            content = stream.read(profile.max_file_bytes + 1)
        result = inspect_uploaded_reference(path.name, content, profile,
                    observed_at=datetime.now(timezone.utc), html_encoding=args.html_encoding)
        destination = ROOT / "var/reference-inspections" / result.inspection_digest
        # New observation directory; never overwrite previous inspection/source records.
        destination.mkdir(parents=True, exist_ok=False)
        (destination / ("source" + path.suffix.lower())).write_bytes(content)
        report = destination / "inspection.json"
        report.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
        print(json.dumps(dict(status=result.status, report=str(report.relative_to(ROOT)),
                              blocks=len(result.blocks), pages=result.page_count,
                              origin_status=result.origin_status, support_status=result.support_status,
                              corpus_id=result.corpus_id, scope_status=result.scope_status,
                              index_created=False, final_ready=False, model_calls=0)))
        return 0
    except (InputError, OSError) as error:
        # Do not dump source text, host filesystem paths or exception bodies to logs.
        print(json.dumps(dict(status="STOPPED", reason=str(error) if isinstance(error, InputError)
                              else "LOCAL_FILE_IO_FAILED", index_created=False, final_ready=False)))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
