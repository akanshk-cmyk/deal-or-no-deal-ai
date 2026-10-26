"""Explicit local original-response review; no inference, secrets or deal mutation."""

from hashlib import sha256
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator

from .context import InputError, canonical_json, fingerprint, primitive, strict_json, unicode_scalar
from .contracts import Identifier, StrictModel
from .model_comparison import check_extraction_response, check_synthesis_response, prepare_comparison
from .services import load_registered_case
from .synthesis import prepare_synthesis


class QualityCapture(StrictModel):
    version: Literal["QUALITY-CAPTURE-1.0"]
    attempt_id: Identifier
    attempt_number: Annotated[int, Field(ge=1, le=5)]
    model_id: Literal["Qwen/Qwen3-30B-A3B-Instruct-2507", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"]
    stage: Literal["extractor", "synthesizer"]
    task_digest: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    origin: Literal["FIXTURE_TEST", "UNVERIFIED_CAPTURE"]
    completion_status: Literal["COMPLETE", "TRUNCATED", "REFUSED", "ERROR", "UNKNOWN"]
    output_text: Annotated[str, Field(max_length=65536)]

    @field_validator("output_text")
    @classmethod
    def bounded_unicode(cls, text):
        unicode_scalar(text)
        if len(text.encode("utf-8")) > 65536:
            raise ValueError("OUTPUT_BYTE_LIMIT")
        return text


def _retain(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise InputError("ORIGINAL_RESPONSE_ARTIFACT_CHANGED")
        return
    # Exclusive create: never overwrite a first response or a partial write.
    with path.open("xb") as stream:
        stream.write(content)


def review_capture(root: Path, raw_capture: bytes) -> dict:
    """Retain declared original bytes, then run conservative local diagnostics.

    Capture model/status/origin declarations are unverified. This is NOT a
    provider adapter, human support decision, model benchmark or paid runner.
    """
    if type(raw_capture) is not bytes:
        raise InputError("CAPTURE_BYTES_REQUIRED")
    capture = QualityCapture.model_validate(strict_json(raw_capture, envelope=True))
    plan = prepare_comparison(root)
    if capture.task_digest != plan["task_digests"][capture.stage]:
        raise InputError("CAPTURE_TASK_BINDING_MISMATCH")
    task = plan["task_packets"][capture.stage]
    output = capture.output_text.encode("utf-8")
    retained = {"capture.json": raw_capture, "original-output.txt": output,
                "task.json": (canonical_json(task) + "\n").encode("utf-8")}
    base = (root / "var/evaluations/response-review").resolve()
    destination = base / capture.attempt_id
    if not destination.resolve().is_relative_to(base):
        raise InputError("RESPONSE_REVIEW_DESTINATION_OUT_OF_SCOPE")
    # Inspect all existing originals before adding any missing artifact.
    for name, content in retained.items():
        target = destination / name
        if target.is_symlink() or (target.exists() and target.read_bytes() != content):
            raise InputError("ORIGINAL_RESPONSE_ARTIFACT_CHANGED")
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in retained.items():
        _retain(destination / name, content)
    case = load_registered_case(root)
    eligible = capture.completion_status == "COMPLETE"
    # Never accept a parseable fragment from a truncated/refused/unknown attempt.
    raw = capture.output_text if eligible else "{}"
    checks = (check_extraction_response(raw, case) if capture.stage == "extractor"
              else check_synthesis_response(raw, case, prepare_synthesis(case)))
    report = primitive(dict(version="QUALITY-REVIEW-1.0", evidence_type="LOCAL_RESPONSE_CHECK_ONLY",
        origin=capture.origin, provider_identity_status="UNVERIFIED_DECLARATION",
        model_id=capture.model_id, stage=capture.stage, attempt_id=capture.attempt_id,
        attempt_number=capture.attempt_number,
        output_cutoff="ORIGINAL_FIRST_ATTEMPT" if capture.attempt_number == 1 else "SEPARATE_DECLARED_LATER_ATTEMPT",
        capture_sha256=sha256(raw_capture).hexdigest(), output_sha256=sha256(output).hexdigest(),
        task_digest=capture.task_digest, case_dependency_digest=case.dependency_digest,
        completion_status=capture.completion_status, completion_eligible=eligible, checks=checks,
        tool_provider_requests=0, measured_provider_requests=None, billed_input_tokens=None,
        billed_output_tokens=None, measured_latency_ms=None, actual_cost_usd=None,
        live_quality_established=False, accepted_for_application=False, human_support=None,
        pending=["Verified provider identity, completion and usage contract", "Provider token preflight",
                 "Manual semantic support/omission review", "Additional registered quality scenarios",
                 "Separately authorized live benchmark and optional RAGAS"]))
    report["review_digest"] = fingerprint("QUALITY-REVIEW-1.0", report)
    artifact = destination / "review.json"
    if artifact.is_symlink():
        raise InputError("ORIGINAL_RESPONSE_ARTIFACT_CHANGED")
    _retain(artifact, (canonical_json(report) + "\n").encode("utf-8"))
    return dict(status="OFFLINE_REVIEW_RECORDED", report=str(artifact.relative_to(root)),
                stage=capture.stage, completion_eligible=eligible, schema_valid=checks["schema_valid"],
                tool_provider_requests=0, live_quality_established=False)
