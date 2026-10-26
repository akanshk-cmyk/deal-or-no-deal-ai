"""Explicit local live-readiness and secret loading; import is side-effect free."""
import os
import json
import tomllib
from hashlib import sha256
from pathlib import Path

from .context import InputError
from .provider import MODELS, LIVE_STAGE_CAPS, SCHEMAS
from .services import load_registered_case
from .model_comparison import prepare_extraction_task
from .synthesis import prepare_synthesis, synthesis_task

MODEL = MODELS[0]
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"


def read_api_key(root):
    """Only literal key assignment is supported; no shell expansion or logging."""
    key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not key:
        path = Path(root) / ".env"
        if path.is_file():
            if path.stat().st_size > 65536:
                raise InputError("LOCAL_ENV_FILE_LIMIT")
            matches = []
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                name, separator, value = line.partition("=")
                if separator and name.strip() == "NEBIUS_API_KEY":
                    matches.append(value.strip().strip('\"\''))
            if len(matches) > 1:
                raise InputError("DUPLICATE_LOCAL_API_KEY")
            key = matches[0] if matches else ""
    if not key or key in {"your_key_here", "REPLACE_ME"}:
        raise InputError("NEBIUS_API_KEY_NOT_CONFIGURED")
    if any(c.isspace() for c in key) or len(key) > 8192:
        raise InputError("INVALID_LOCAL_API_KEY_FORMAT")
    return key


def tokenizer_diagnostic(root, tasks):
    path = Path(root) / "var/models/qwen-generation-tokenizer/manifest.json"
    if not path.is_file():
        return dict(status="NOT_CONFIGURED", counts=None, verified_provider_fit=False)
    manifest = json.loads(path.read_bytes())
    directory = path.parent / manifest["revision"]
    if manifest["model"] != MODEL or len(manifest["revision"]) != 40:
        raise InputError("TOKENIZER_IDENTITY_MISMATCH")
    for name, entry in manifest["files"].items():
        if name not in {"tokenizer.json", "tokenizer_config.json"} or sha256((directory / name).read_bytes()).hexdigest() != entry["sha256"]:
            raise InputError("TOKENIZER_BYTES_CHANGED")
    from tokenizers import Tokenizer
    tokenizer = Tokenizer.from_file(str(directory / "tokenizer.json"))
    counts = {}
    for stage, task in tasks.items():
        counts[stage] = {k: len(tokenizer.encode(v if isinstance(v, str) else json.dumps(v, separators=(",", ":"), ensure_ascii=False)).ids) for k, v in task.items()}
        counts[stage].update(stage_input_cap=LIVE_STAGE_CAPS[stage][0], stage_output_cap=LIVE_STAGE_CAPS[stage][1])
        counts[stage]["component_total"] = sum(counts[stage][k] for k in ("instruction", "context", "schema"))
    return dict(status="LOCAL_COMPONENT_COUNTS_ONLY", model=MODEL, revision=manifest["revision"], counts=counts,
                verified_provider_fit=False, limitation="Provider chat/schema rendering and usage still need verification; no paid dispatch is authorized by this diagnostic.")


def readiness(root):
    case = load_registered_case(Path(root))
    from .live_context import prepare_live_tasks
    tasks = prepare_live_tasks(root)
    try:
        read_api_key(root); key_present = True
    except InputError as error:
        if str(error) != "NEBIUS_API_KEY_NOT_CONFIGURED":
            raise
        key_present = False
    tokenization = tokenizer_diagnostic(root, tasks)
    blockers = ([] if key_present else ["NEBIUS_API_KEY_NOT_CONFIGURED"]) + ["PROVIDER_MODEL_SCHEMA_RATE_AND_FULL_INPUT_FIT_UNVERIFIED"]
    for stage, value in (tokenization.get("counts") or {}).items():
        if value["component_total"] > value["stage_input_cap"]:
            blockers.append(stage.upper() + "_LOCAL_COMPONENTS_EXCEED_APPROVED_LIVE_INPUT_CAP")
    with (Path(root)/"config/live_smoke.toml").open("rb") as stream:
        profile=tomllib.load(stream)
    if profile.get("provider_contract_verified") is True:
        from .live_worker import packet_tokens
        try:
            packet_tokens(root,tasks["extractor"])
        except InputError:
            blockers.append("EXACT_EXTRACTION_PACKET_VERIFICATION_REQUIRED")
        else:
            blockers.remove("PROVIDER_MODEL_SCHEMA_RATE_AND_FULL_INPUT_FIT_UNVERIFIED")
            local_blocker="EXTRACTOR_LOCAL_COMPONENTS_EXCEED_APPROVED_LIVE_INPUT_CAP"
            if local_blocker in blockers:
                blockers.remove(local_blocker)
                tokenization["advisory"]="Local component tokenization overcounts the separately supplied schema relative to actual provider prompt usage. The exact extraction request has provider-measured input fit; future synthesis requests still require their own verification."
    return dict(status="NOT_READY" if blockers else "READY_TO_START", evidence_checkpoints="REQUIRED_AFTER_EXTRACTION_AND_SYNTHESIS", live_graph_integration="IMPLEMENTED_PROVIDER_EXECUTION_NOT_VERIFIED", prompt_profile="LIVE-COMPACT-1.0", generation_model=MODEL, embedding_model=EMBEDDING_MODEL,
        total_authorized_usd="0.10", allowance_basis="User explicitly approved shared live/embedding/evaluation total", api_key_present=key_present,
        tokenizer=tokenization, blockers=blockers, provider_calls=0, paid_cost_usd="0", actual_live_journey_completed=None, journey_status="NOT_ASSESSED_BY_READINESS_CHECK", accounting_scope="THIS_READINESS_CHECK_ONLY")
