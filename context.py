"""INPUT-EDU-1.0 and CANON-1.0 primitives. No model or tokenizer is loaded."""

from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
from uuid import UUID, uuid5


FINANCIAL_FIELDS = (
    "net_income", "interest_expense", "income_tax_expense", "depreciation",
    "amortization", "cash_available_for_debt_service", "annual_principal_payments",
    "annual_interest_payments", "existing_funded_debt", "proposed_funded_borrowing",
    "transaction_debt_repaid", "eligible_equipment_value", "prior_ranking_liens",
    "secured_facility_exposure", "current_revenue", "previous_revenue",
    "current_assets", "current_liabilities",
)


class InputError(ValueError):
    """Safe reason codes only; never include rejected raw content."""


def unicode_scalar(value: str) -> str:
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise InputError("INVALID_UNICODE")
    return value


def canonical_decimal(value: Decimal) -> str:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise InputError("INVALID_DECIMAL")
    if value.is_zero():
        return "0"
    sign, digits, exponent = value.as_tuple()
    # Bound expansion even for an incorrectly constructed internal Decimal.
    if abs(exponent) > 1000 or len(digits) > 1000:
        raise InputError("DECIMAL_EXPANSION_LIMIT")
    number = format(value, "f")
    if "." in number:
        number = number.rstrip("0").rstrip(".")
    return number


def money_string(value: object) -> str:
    if type(value) is not str or len(value) > 26:
        raise InputError("INVALID_MONEY_STRING")
    if not re.fullmatch(r"-?(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,6})?", value):
        raise InputError("INVALID_MONEY_STRING")
    if canonical_decimal(Decimal(value)) != value:
        raise InputError("NONCANONICAL_MONEY")
    return value


def exact_confidence(value: object) -> Decimal:
    if type(value) is int:
        value = Decimal(value)
    if not isinstance(value, Decimal) or not value.is_finite():
        raise InputError("INVALID_CONFIDENCE")
    if not Decimal(0) <= value <= Decimal(1):
        raise InputError("INVALID_CONFIDENCE")
    _, digits, exponent = value.as_tuple()
    if len(digits) > 24 or max(0, -exponent) > 24:
        raise InputError("CONFIDENCE_PRECISION_LIMIT")
    return value


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("DUPLICATE_JSON_MEMBER")
        result[key] = value
    return result


def _integer(raw: str) -> int:
    if len(raw.lstrip("-")) > 18:
        raise InputError("INTEGER_LIMIT")
    return int(raw)


def _number(raw: str) -> Decimal:
    if len(raw) > 32:
        raise InputError("NUMBER_LITERAL_LIMIT")
    value = Decimal(raw)
    # Only the confidence wire field permits a JSON fractional number.
    # Apply expansion limits before hashing or rendering, not after expansion.
    if abs(value.as_tuple().exponent) > 24 or len(value.as_tuple().digits) > 24:
        raise InputError("NUMBER_EXPANSION_LIMIT")
    return value


def _constant(_: str):
    raise InputError("NONFINITE_JSON_NUMBER")


def strict_json(raw: str | bytes, *, envelope: bool = False) -> dict:
    limit = 262144 if envelope else 65536
    try:
        if isinstance(raw, bytes):
            if len(raw) > limit:
                raise InputError("JSON_BYTE_LIMIT")
            text = raw.decode("utf-8", errors="strict")
        elif type(raw) is str:
            text = unicode_scalar(raw)
            if len(text.encode("utf-8")) > limit:
                raise InputError("JSON_BYTE_LIMIT")
        else:
            raise InputError("JSON_TYPE")
        depth = 0
        quoted = escaped = False
        for char in text:
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char in "[{":
                depth += 1
                if depth > 12:
                    raise InputError("JSON_DEPTH_LIMIT")
            elif char in "]}":
                depth -= 1
        result = json.loads(text, object_pairs_hook=_pairs, parse_int=_integer,
                            parse_float=_number, parse_constant=_constant)
        if type(result) is not dict:
            raise InputError("JSON_ROOT_OBJECT_REQUIRED")

        def check(value):
            if type(value) is str:
                unicode_scalar(value)
                if not envelope and len(value) > 4096:
                    raise InputError("JSON_STRING_LIMIT")
            elif type(value) is dict:
                if not envelope and len(value) > 64:
                    raise InputError("JSON_COLLECTION_LIMIT")
                for key, item in value.items():
                    check(key)
                    check(item)
            elif type(value) is list:
                if not envelope and len(value) > 64:
                    raise InputError("JSON_COLLECTION_LIMIT")
                for item in value:
                    check(item)
        check(result)
        return result
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError("INVALID_JSON") from exc


def primitive(value):
    """Convert only supported known types; never arbitrary object reconstruction."""
    if isinstance(value, Decimal):
        return canonical_decimal(value)
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset().total_seconds() != 0:
            raise InputError("UTC_REQUIRED")
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if value is None or type(value) in (str, int, bool):
        if type(value) is str:
            unicode_scalar(value)
        return value
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise InputError("STRING_KEYS_REQUIRED")
        return {unicode_scalar(key): primitive(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [primitive(item) for item in value]
    if type(value) in (set, frozenset):
        items = [primitive(item) for item in value]
        return sorted(items, key=lambda item: canonical_json(item))
    raise InputError("UNSUPPORTED_CANONICAL_TYPE")


def canonical_json(value) -> str:
    return json.dumps(primitive(value), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def fingerprint(domain: str, projection) -> str:
    unicode_scalar(domain)
    content = "CANON-1.0\0" + domain + "\0" + canonical_json(projection)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def stable_id(operation_id: str, field_path: str) -> str:
    return str(uuid5(UUID(operation_id), field_path))


def narrative_parent(wire: dict, dependencies: dict) -> str:
    allowed = {"wire_version", "panel_decision", "observations", "rationale_refs",
               "condition_links", "proposed_action"}
    content = {key: value for key, value in wire.items() if key in allowed}
    if set(content) != allowed:
        raise InputError("INCOMPLETE_NARRATIVE_CONTENT")
    return fingerprint("NARRATIVE_CONTENT", {"wire": content, "dependencies": dependencies})


def instruction_manifest(workspace: Path) -> dict[str, str]:
    """Explicit authoring operation; a returned hash is not independent approval."""
    return {role: hashlib.sha256(_instruction(workspace, role).encode()).hexdigest()
            for role in ("extractor", "synthesizer")}


def _section(text: str, title: str) -> str:
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == "## " + title]
    if len(starts) != 1:
        raise InputError("MISSING_OR_AMBIGUOUS_PROMPT_SECTION")
    start = starts[0] + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "".join(lines[start:end]).strip()


def _instruction(workspace: Path, role: str) -> str:
    if role not in ("extractor", "synthesizer"):
        raise InputError("MODEL_ROLE_NOT_ALLOWED")
    folder = workspace.resolve() / "docs" / "agents"
    shared = _section((folder / "shared-contract.md").read_text(encoding="utf-8"), "Model context rules")
    task = _section((folder / (role + ".md")).read_text(encoding="utf-8"), "Runtime prompt")
    return shared + "\n\n" + task


def load_instruction(workspace: Path, role: str, expected_sha256: str) -> str:
    text = _instruction(workspace, role)
    actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if actual != expected_sha256:
        raise InputError("INSTRUCTION_HASH_MISMATCH")
    return text


def request_size(instructions: str, schema: dict, sources: dict, wire: dict | str) -> dict:
    """Exact serialized UTF-8 sizes, NOT tokenizer or provider-template evidence."""
    measured = {"measurement": "UTF8_BYTES_NOT_TOKENS", **{
        name: len(canonical_json(value).encode("utf-8"))
        for name, value in {"instructions": instructions, "schema": schema,
                            "sources": sources, "illustrative_response": wire}.items()
    }}
    if type(wire) is str:
        measured["illustrative_response"] = len(wire.encode("utf-8"))
    return measured
