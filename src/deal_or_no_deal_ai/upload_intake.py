"""Persistent educational upload inspection, isolated from registered deal analysis."""
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import time
from uuid import UUID, uuid5

from .command_center import ROLES, workspace_id
from .configuration import load_configuration
from .context import InputError, fingerprint, canonical_json, strict_json, unicode_scalar
from .storage import OperationConflict, RecordWrite, Store


def _authorize(root, actor, *, write=False):
    if (actor.attribution != "SIMULATED" or actor.persona not in ROLES
        or actor.workspace_id != workspace_id(root) or write and actor.persona != "Analyst"):
        raise InputError("UPLOAD_PERMISSION_REQUIRED")


def _validate_files(files):
    if type(files) is not list or not 1 <= len(files) <= 3:
        raise InputError("UPLOAD_ONE_TO_THREE_PDFS_REQUIRED")
    size, seen = 0, set()
    for item in files:
        if type(item) is not tuple or len(item) != 2:
            raise InputError("UPLOAD_FILE_SHAPE")
        name, raw = item
        if (type(name) is not str or not name.strip() or len(name) > 255 or name != Path(name).name
            or name != PureWindowsPath(name).name or any(c in name for c in '\\/:\x00') or any(ord(c) < 32 for c in name) or not name.lower().endswith('.pdf')):
            raise InputError("UPLOAD_PDF_BASENAME_REQUIRED")
        unicode_scalar(name)
        if type(raw) is not bytes or not raw or not raw.startswith(b"%PDF-"):
            raise InputError("UPLOAD_INVALID_PDF_BYTES")
        size += len(raw)
        digest = sha256(raw).hexdigest()
        if digest in seen:
            raise InputError("UPLOAD_DUPLICATE_CONTENT")
        seen.add(digest)
    if size > 10_000_000:
        raise InputError("UPLOAD_COMBINED_BYTE_LIMIT")


def _parse(raw, timeout):
    try:
        result = subprocess.run([sys.executable, "-I", "-m", "deal_or_no_deal_ai.upload_parser"], input=raw,
            capture_output=True, timeout=timeout, check=False, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except subprocess.TimeoutExpired as error:
        raise InputError("UPLOAD_PARSER_TIMEOUT") from error
    if result.returncode != 0 or len(result.stdout) > 250_000:
        raise InputError("UPLOAD_PARSER_FAILED")
    parsed = strict_json(result.stdout, envelope=True)
    if "error" in parsed:
        raise InputError(parsed["error"] + ("_PAGE_" + str(parsed["page"]) if parsed.get("page") else ""))
    pages = parsed.get("pages")
    if type(pages) is not list or not 1 <= len(pages) <= 10 or any(type(t) is not str or not t.strip() for t in pages):
        raise InputError("UPLOAD_PARSER_RESULT_INVALID")
    return [unicode_scalar(t) for t in pages]


def inspect_package(root, actor, operation_id, files, *, synthetic_confirmed):
    config = load_configuration(root); root = config.workspace
    _authorize(root, actor, write=True)
    if str(UUID(operation_id)) != operation_id or synthetic_confirmed is not True:
        raise InputError("SYNTHETIC_UPLOAD_CONFIRMATION_REQUIRED")
    _validate_files(files)
    digest = fingerprint("UPLOAD_COMMAND", dict(files=[dict(name=n, sha256=sha256(b).hexdigest()) for n, b in files], actor=actor.persona))
    store = Store(config.database)
    if store.path.exists():
        prior = store.get_record("upload-package:" + operation_id)
        if prior:
            if prior[1]["command_digest"] != digest:
                raise OperationConflict("OPERATION_CONFLICT")
            return load_package(root, actor, operation_id)
        with store.connection() as connection:
            existing = connection.execute("SELECT state FROM app_operations WHERE operation_id=?", (operation_id,)).fetchone()
        if existing is not None and existing[0] != "RELEASED":
            raise InputError("UPLOAD_RECOVERY_REQUIRED")
    started = time.monotonic(); sources = []; page_count = text_bytes = 0
    package_id = str(uuid5(UUID(operation_id), "upload-package"))
    for name, raw in files:
        remaining = 45 - (time.monotonic() - started)
        if remaining <= 0:
            raise InputError("UPLOAD_PARSER_TIMEOUT")
        try:
            texts = _parse(raw, remaining)
        except InputError as error:
            error.filename = name
            raise
        source_id = sha256(raw).hexdigest()
        pages = [dict(page=i, ref=f"upload:{package_id}:{source_id}:p{i}", text=text,
            text_sha256=sha256(text.encode()).hexdigest(), start=0, end=len(text)) for i, text in enumerate(texts, 1)]
        page_count += len(pages); text_bytes += sum(len(t.encode()) for t in texts)
        if page_count > 10 or text_bytes > 120_000:
            raise InputError("UPLOAD_COMBINED_PAGE_OR_TEXT_LIMIT")
        sources.append(dict(filename=name, sha256=source_id, byte_count=len(raw), pages=pages))
    package = dict(version="UPLOAD-1.0", operation_id=operation_id, package_id=package_id, workspace_id=actor.workspace_id,
        command_digest=digest, status="INSPECTED_NOT_REVIEWED", synthetic_attestation=True,
        observed_at_utc=datetime.now(timezone.utc).isoformat(), parser="pypdf/" + version("pypdf"), sources=sources,
        page_count=page_count, byte_count=sum(len(raw) for _, raw in files), origin="UNVERIFIED_LOCAL_UPLOAD",
        subject=None, reporting_period=None, source_authority="UNVERIFIED", model_calls=0, final_ready=False)
    package["package_digest"] = fingerprint("UPLOAD_PACKAGE", package)
    if len(canonical_json(package).encode()) > 262_144:
        raise InputError("UPLOAD_INSPECTION_ENVELOPE_LIMIT")
    store.initialize()
    scope = dict(workspace_id=actor.workspace_id, package_id=package_id, review_id=str(uuid5(UUID(operation_id), "upload-admission")))
    receipt = store.admit(operation_id, scope, dict(action="INSPECT_UPLOAD", digest=digest))
    if receipt.duplicate:
        if receipt.state != "RELEASED":
            raise InputError("UPLOAD_RECOVERY_REQUIRED")
        return load_package(root, actor, operation_id)
    try:
        destination = root / "var/uploads" / actor.workspace_id / package_id
        if not destination.resolve().is_relative_to(root.resolve()):
            raise InputError("UPLOAD_STORAGE_PATH_INVALID")
        destination.mkdir(parents=True, exist_ok=False)
        for source, (_, raw) in zip(sources, files):
            with (destination / (source["sha256"] + ".pdf")).open("xb") as stream:
                stream.write(raw)
        store.put_record(RecordWrite("upload-package:" + operation_id, "UPLOAD_PACKAGE", package))
        store.release(receipt, confirmed_idle=True)
    except BaseException:
        store.mark_unknown(receipt)
        raise
    return package


def load_package(root, actor, operation_id):
    config = load_configuration(root); _authorize(config.workspace, actor)
    if str(UUID(operation_id)) != operation_id:
        raise InputError("UPLOAD_CANONICAL_ID_REQUIRED")
    store = Store(config.database)
    if not store.path.exists():
        raise InputError("UPLOAD_UNAVAILABLE")
    saved = store.get_record("upload-package:" + operation_id)
    if saved is None or saved[1].get("workspace_id") != actor.workspace_id:
        raise InputError("UPLOAD_UNAVAILABLE")
    package = saved[1]
    if package.get("operation_id") != operation_id or package.get("package_id") != str(uuid5(UUID(operation_id), "upload-package")):
        raise InputError("UPLOAD_IDENTITY_CHANGED")
    with store.connection() as connection:
        claim = connection.execute("SELECT state FROM app_operations WHERE operation_id=?", (operation_id,)).fetchone()
    if claim is None or claim[0] != "RELEASED":
        raise InputError("UPLOAD_RECOVERY_REQUIRED")
    if package["package_digest"] != fingerprint("UPLOAD_PACKAGE", {k: v for k, v in package.items() if k != "package_digest"}):
        raise InputError("UPLOAD_RECORD_CHANGED")
    base = config.workspace / "var/uploads" / actor.workspace_id / package["package_id"]
    if not base.resolve().is_relative_to(config.workspace.resolve()):
        raise InputError("UPLOAD_STORAGE_PATH_INVALID")
    for source in package["sources"]:
        if len(source["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in source["sha256"]):
            raise InputError("UPLOAD_SOURCE_ID_INVALID")
        path = (base / (source["sha256"] + ".pdf")).resolve()
        if not path.is_relative_to(base.resolve()) or sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise InputError("UPLOAD_SOURCE_CHANGED")
        for i, page in enumerate(source["pages"], 1):
            if (sha256(page["text"].encode()).hexdigest() != page["text_sha256"] or page["page"] != i
                or page["start"] != 0 or page["end"] != len(page["text"])
                or page["ref"] != f"upload:{package['package_id']}:{source['sha256']}:p{i}"):
                raise InputError("UPLOAD_PAGE_CHANGED")
    return package


def list_packages(root, actor):
    config = load_configuration(root); _authorize(config.workspace, actor)
    store = Store(config.database)
    if not store.path.exists():
        return []
    with store.connection() as connection:
        rows = connection.execute("SELECT payload FROM app_records WHERE kind='UPLOAD_PACKAGE'").fetchall()
    packages = [strict_json(row[0], envelope=True) for row in rows]
    return sorted([p for p in packages if p.get("workspace_id") == actor.workspace_id], key=lambda p: p["observed_at_utc"], reverse=True)
