"""Explicit approved tokenizer-only setup; never download model weights or a key."""
from hashlib import sha256
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"


def bounded_get(url, maximum):
    with urllib.request.urlopen(url, timeout=30) as response:
        raw = response.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError("TOKENIZER_DOWNLOAD_LIMIT")
    return raw


def main():
    metadata = json.loads(bounded_get("https://huggingface.co/api/models/" + MODEL, 1000000))
    revision = metadata["sha"]
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise ValueError("PINNED_TOKENIZER_REVISION_REQUIRED")
    destination = ROOT / "var/models/qwen-generation-tokenizer" / revision
    destination.mkdir(parents=True, exist_ok=True)
    files = {}
    for name in ("tokenizer.json", "tokenizer_config.json"):
        raw = bounded_get("https://huggingface.co/" + MODEL + "/resolve/" + revision + "/" + name, 64 * 1024 * 1024)
        path = destination / name
        if path.exists() and path.read_bytes() != raw:
            raise ValueError("EXISTING_TOKENIZER_CHANGED")
        if not path.exists():
            with path.open("xb") as stream:
                stream.write(raw)
        files[name] = dict(sha256=sha256(raw).hexdigest(), bytes=len(raw))
    record = dict(model=MODEL, revision=revision, files=files, model_weights_downloaded=False,
                  provider_template_verified=False)
    target = ROOT / "var/models/qwen-generation-tokenizer/manifest.json"
    raw = (json.dumps(record, indent=2) + "\n").encode()
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("TOKENIZER_MANIFEST_REVISION_CHANGE_REQUIRES_REVIEW")
    if not target.exists():
        target.write_bytes(raw)
    print(json.dumps(record))


if __name__ == "__main__":
    main()
