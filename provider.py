"""PROVIDER-1.0 offline compatibility boundary. No client, secrets or dispatch.

Preparing a request is not permission to send it. A future worker must persist
admission/reservation before dispatch and retain uncertain usage without retries.
"""

from dataclasses import dataclass
import json

from pydantic import ValidationError

from .context import InputError
from .contracts import DealTermsWire, SynthesisWire, parse_extraction, parse_synthesis
from .model_comparison import Baseline, Challenger, estimate_generation_cost


MODELS = ("Qwen/Qwen3-30B-A3B-Instruct-2507", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B")
PARSERS = {"extractor": parse_extraction, "synthesizer": parse_synthesis}
SCHEMAS = {"extractor": DealTermsWire, "synthesizer": SynthesisWire}
# Original P3-05 envelopes; leave 1500/350 protected for synthesis correction.
STAGE_CAPS = {"extractor": (3000, 1000), "synthesizer": (1500, 350)}

LIVE_STAGE_CAPS = {"extractor": (4000, 1000), "synthesizer": (2500, 650)}

def stage_caps(profile=None):
    if profile is None:
        return STAGE_CAPS
    if profile != "LIVE-COMPACT-1.0":
        raise InputError("UNAPPROVED_TOKEN_PROFILE")
    return LIVE_STAGE_CAPS


@dataclass(frozen=True)
class ProviderOutcome:
    status: str
    reason: str
    output_text: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    reasoning_tokens: int | None = None
    estimated_cost_usd: str | None = None
    usage_status: str = "UNKNOWN"
    wire: DealTermsWire | SynthesisWire | None = None
    evidence_label: str = "OFFLINE_PROVIDER_ENVELOPE_CHECK_NOT_VERIFIED_CALL"


def prepare_request(*, model_id: str, stage: str, instruction: str, context: dict,
                    verified_input_tokens: int | None, max_output_tokens: int, profile: str | None = None) -> dict:
    """Prepare only. Caller must supply verified whole-request token accounting.

    The count must include messages, schema and chat-template overhead; a character
    count or a model-independent heuristic is not accepted as tokenizer evidence.
    """
    if model_id not in MODELS or stage not in PARSERS:
        raise InputError("UNAPPROVED_PROVIDER_TASK")
    if type(instruction) is not str or not instruction.strip() or type(context) is not dict:
        raise InputError("PROVIDER_TASK_REQUIRED")
    input_cap, output_cap = stage_caps(profile)[stage]
    if type(verified_input_tokens) is not int or not 0 < verified_input_tokens <= input_cap:
        raise InputError("VERIFIED_PROVIDER_INPUT_FIT_REQUIRED")
    if type(max_output_tokens) is not int or not 0 < max_output_tokens <= output_cap:
        raise InputError("PROVIDER_OUTPUT_CAP_EXCEEDED")
    schema = SCHEMAS[stage].model_json_schema()
    if profile is not None:
        from .live_context import live_wire_schema
        schema = live_wire_schema(stage)
    return dict(model=model_id, messages=[dict(role="system", content=instruction),
        dict(role="user", content=json.dumps(context, ensure_ascii=False, allow_nan=False, separators=(",", ":") if profile else None))],
        response_format=dict(type="json_schema", json_schema=dict(name=stage,
            strict=True, schema=schema)),
        max_tokens=max_output_tokens, temperature=0, stream=False, n=1)


def normalize_response(response: dict, *, model_id: str, stage: str, profile: str | None = None) -> ProviderOutcome:
    """Preserve original text and reject unsafe envelopes before parsing output.

    Usage remains available on refusals/truncation/invalid output: failure can cost
    tokens. Missing/invalid accounting never becomes a free or successful call.
    """
    if model_id not in MODELS or stage not in PARSERS:
        raise InputError("UNAPPROVED_PROVIDER_TASK")
    if type(response) is not dict or response.get("model") != model_id:
        return ProviderOutcome("ERROR", "PROVIDER_MODEL_OR_ENVELOPE_MISMATCH")
    caps = stage_caps(profile)
    usage = response.get("usage")
    accounting = {}
    if type(usage) is dict:
        prompt, completion, total = (usage.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens"))
        if all(type(v) is int and v >= 0 for v in (prompt, completion, total)) and total == prompt + completion:
            details = usage.get("completion_tokens_details")
            reasoning = details.get("reasoning_tokens") if type(details) is dict else None
            if reasoning is None or type(reasoning) is int and 0 <= reasoning <= completion:
                model = Baseline(model_id=model_id, input_usd_per_million_tokens="0.10", output_usd_per_million_tokens="0.30") if model_id == MODELS[0] else Challenger(model_id=model_id, input_usd_per_million_tokens="0.06", output_usd_per_million_tokens="0.24")
                accounting = dict(prompt_tokens=prompt, completion_tokens=completion, reasoning_tokens=reasoning,
                    estimated_cost_usd=estimate_generation_cost(model, input_tokens=prompt, billed_output_tokens=completion),
                    usage_status="REPORTED_UNVERIFIED_PROVIDER_USAGE")
    choices = response.get("choices")
    if type(choices) is not list or len(choices) != 1 or type(choices[0]) is not dict:
        return ProviderOutcome("ERROR", "EXACTLY_ONE_PROVIDER_CHOICE_REQUIRED", **accounting)
    choice = choices[0]
    message = choice.get("message")
    if type(message) is not dict or message.get("role") != "assistant":
        return ProviderOutcome("ERROR", "ASSISTANT_MESSAGE_REQUIRED", **accounting)
    text = message.get("content") if type(message.get("content")) is str else None
    if message.get("refusal") or choice.get("finish_reason") == "content_filter":
        return ProviderOutcome("REFUSED", "PROVIDER_REFUSAL", output_text=text, **accounting)
    if choice.get("finish_reason") == "length":
        return ProviderOutcome("TRUNCATED", "OUTPUT_LIMIT_REACHED", output_text=text, **accounting)
    if choice.get("finish_reason") != "stop" or message.get("tool_calls") or message.get("function_call"):
        return ProviderOutcome("ERROR", "UNEXPECTED_PROVIDER_FINISH", output_text=text, **accounting)
    if not text or len(text.encode("utf-8")) > 262144:
        return ProviderOutcome("ERROR", "EMPTY_OR_OVERSIZED_PROVIDER_OUTPUT", **accounting)
    if not accounting:
        return ProviderOutcome("ACCOUNTING_REQUIRED", "PROVIDER_USAGE_MISSING_OR_INVALID", output_text=text)
    if accounting["prompt_tokens"] > caps[stage][0] or accounting["completion_tokens"] > caps[stage][1]:
        return ProviderOutcome("ACCOUNTING_REQUIRED", "PROVIDER_USAGE_EXCEEDS_STAGE_CAP", output_text=text, **accounting)
    try:
        wire = PARSERS[stage](text)
    except (InputError, ValueError, ValidationError):
        return ProviderOutcome("INVALID_OUTPUT", "WIRE_SCHEMA_REJECTED", output_text=text, **accounting)
    return ProviderOutcome("VALIDATED", "SCHEMA_ONLY_SOURCE_SUPPORT_STILL_REQUIRED", output_text=text, wire=wire, **accounting)


def transport_failure(*, dispatch_started: bool) -> ProviderOutcome:
    if type(dispatch_started) is not bool:
        raise InputError("DISPATCH_STATE_REQUIRED")
    return ProviderOutcome("RECOVERY_REQUIRED" if dispatch_started else "NOT_DISPATCHED",
                           "PROVIDER_OUTCOME_UNCERTAIN_NO_AUTOMATIC_RETRY" if dispatch_started else "LOCAL_PREFLIGHT_FAILED")
