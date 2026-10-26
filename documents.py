"""DOCVERIFY-1.0 checks on supplied parsed blocks; no PDF parsing or inference.

COMPLETE means declared original-block coverage, not semantic truth. Upstream
adapters must establish source fit, parser fidelity and dependency completeness.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal

from .context import InputError, canonical_json, fingerprint, money_string, unicode_scalar


@dataclass(frozen=True)
class ReviewScope:
    deal_id: str
    revision: int
    subject_id: str
    facility_id: str
    basis_digest: str

    def __post_init__(self) -> None:
        if type(self.revision) is not int or self.revision < 1 or not all(
            type(v) is str and v for v in (self.deal_id, self.subject_id, self.facility_id, self.basis_digest)
        ):
            raise InputError("INVALID_REVIEW_SCOPE")


@dataclass(frozen=True)
class SourceVersion:
    source_id: str
    version: str
    content_digest: str

    def __post_init__(self) -> None:
        if not all(type(v) is str and v for v in vars(self).values()):
            raise InputError("INVALID_SOURCE_VERSION")


@dataclass(frozen=True)
class OriginalBlock:
    block_id: str
    scope: ReviewScope
    source: SourceVersion
    page: int
    start: int
    text: str
    role: str = "BODY"
    dependencies: tuple[str, ...] = ()
    parser_verified: bool = False
    fit_verified: bool = False

    def __post_init__(self) -> None:
        if type(self.parser_verified) is not bool or type(self.fit_verified) is not bool:
            raise InputError("VERIFICATION_FLAGS_REQUIRE_BOOLEANS")
        if type(self.text) is not str:
            raise InputError("INVALID_ORIGINAL_TEXT")
        unicode_scalar(self.text)
        if type(self.dependencies) is not tuple or any(type(k) is not str or not k for k in self.dependencies):
            raise InputError("INVALID_DEPENDENCY_HANDLES")


@dataclass(frozen=True)
class EvidenceCheck:
    status: Literal["COMPLETE", "INCOMPLETE", "UNVERIFIED"]
    mode: Literal["BASELINE", "ADAPTIVE"]
    required: tuple[str, ...]
    selected: tuple[str, ...]
    missing: tuple[str, ...]
    expanded: tuple[str, ...]
    reasons: tuple[str, ...]
    context_bytes: int
    packet_digest: str | None
    dispatch_blocks: tuple[OriginalBlock, ...]


def _projection(block: OriginalBlock) -> dict:
    return {
        "block_id": block.block_id,
        "source": vars(block.source),
        "page": block.page,
        "start": block.start,
        "end": block.start + len(block.text),
        "text": block.text,
        "role": block.role,
        "dependencies": sorted(set(block.dependencies)),
        "parser_verified": block.parser_verified,
        "fit_verified": block.fit_verified,
    }


def verify_evidence(
    *,
    scope: ReviewScope,
    sources: tuple[SourceVersion, ...],
    inventory: tuple[OriginalBlock, ...],
    roots: tuple[str, ...],
    selected: tuple[str, ...],
    max_context_bytes: int,
    mode: Literal["BASELINE", "ADAPTIVE"] = "BASELINE",
    purpose: Literal["SUPPORT_LOOKUP", "FULL_EXTRACTION"] = "SUPPORT_LOOKUP",
) -> EvidenceCheck:
    """Validate closure; optionally restore existing blocks, never invent them.

    Scope/source allowlists and material roots must come from trusted current
    application metadata, not model output. Byte diagnostics do not count tokens.
    """
    if mode not in ("BASELINE", "ADAPTIVE") or purpose not in (
        "SUPPORT_LOOKUP", "FULL_EXTRACTION"
    ):
        raise InputError("Unsupported verification mode or purpose")
    if type(max_context_bytes) is not int or max_context_bytes <= 0:
        raise InputError("A positive context byte allowance is required")
    reasons: set[str] = set()
    invalid = False
    if not inventory or not sources or max(map(len, (inventory, sources, roots, selected))) > 64:
        reasons.add("EMPTY_OR_OVERSIZED_INVENTORY")
        return EvidenceCheck("UNVERIFIED", mode, (), (), (), (), tuple(sorted(reasons)), 0, None, ())
    if len(set((s.source_id, s.version) for s in sources)) != len(sources):
        reasons.add("AMBIGUOUS_SOURCE_ALLOWLIST")
        invalid = True
    blocks = {b.block_id: b for b in inventory}
    if len(blocks) != len(inventory):
        reasons.add("DUPLICATE_BLOCK_ID")
        invalid = True
    for b in inventory:
        if b.scope != scope or b.source not in sources:
            reasons.add("SCOPE_OR_SOURCE_MISMATCH")
            invalid = True
        if (not b.block_id or type(b.page) is not int or b.page < 1
                or type(b.start) is not int or b.start < 0 or not b.text
                or len(b.dependencies) > 64):
            reasons.add("INVALID_ORIGINAL_LOCATION")
            invalid = True
    if invalid:
        return EvidenceCheck("UNVERIFIED", mode, (), (), (), (), tuple(sorted(reasons)), 0, None, ())

    chosen = set(selected)
    pending = list((set(blocks) if purpose == "FULL_EXTRACTION" else set(roots)) | chosen)
    required: set[str] = set()
    while pending:
        block_id = pending.pop()
        if block_id in required:
            continue
        required.add(block_id)
        if len(required) > 64:
            reasons.add("DEPENDENCY_WORK_LIMIT")
            invalid = True
            break
        block = blocks.get(block_id)
        if block:
            pending.extend(block.dependencies)
    if not required:
        reasons.add("NO_MATERIAL_ROOTS")
        invalid = True
    if mode == "ADAPTIVE":
        chosen.update(required & blocks.keys())
    missing = required - chosen | required - blocks.keys()
    if missing:
        reasons.add("MISSING_REQUIRED_CONTEXT")
    for block_id in required & blocks.keys():
        b = blocks[block_id]
        if not b.parser_verified:
            reasons.add("PARSER_OR_DEPENDENCIES_UNVERIFIED")
            invalid = True
        if not b.fit_verified:
            reasons.add("SOURCE_FIT_UNVERIFIED")
            invalid = True
    packet_blocks = tuple(blocks[k] for k in sorted(chosen & blocks.keys()))
    packet = {"scope": vars(scope), "sources": [vars(s) for s in sorted(sources, key=lambda s: s.source_id)],
              "mode": mode, "purpose": purpose, "required": sorted(required),
              "blocks": [_projection(b) for b in packet_blocks]}
    size = len(canonical_json(packet).encode("utf-8"))
    if size > max_context_bytes:
        reasons.add("CONTEXT_BYTE_LIMIT")
        invalid = True
    status = "UNVERIFIED" if invalid else "INCOMPLETE" if missing else "COMPLETE"
    return EvidenceCheck(
        status, mode, tuple(sorted(required)), tuple(sorted(chosen)), tuple(sorted(missing)),
        tuple(sorted(chosen - set(selected))), tuple(sorted(reasons)), size,
        fingerprint("DOCVERIFY-1.0", packet) if status == "COMPLETE" else None,
        packet_blocks if status == "COMPLETE" else (),
    )


@dataclass(frozen=True)
class StatementPeriod:
    end: date
    start: date | None = None

    def __post_init__(self) -> None:
        if type(self.end) is not date or (self.start is not None and (
            type(self.start) is not date or self.start >= self.end
        )):
            raise InputError("Invalid annual/as-of period")


@dataclass(frozen=True)
class ColumnHeader:
    block_id: str
    layout_id: str
    period: StatementPeriod
    x0: Decimal
    x1: Decimal


@dataclass(frozen=True)
class NumericCell:
    block_id: str
    layout_id: str
    metric: str
    row_label_block_id: str
    x0: Decimal
    x1: Decimal


@dataclass(frozen=True)
class AlignedValue:
    value: str
    period: StatementPeriod
    currency: str
    scale: str
    basis: str
    source: SourceVersion
    required_blocks: tuple[str, ...]


@dataclass(frozen=True)
class AlignmentCheck:
    status: Literal["KNOWN", "UNVERIFIED", "MISSING", "CONFLICT"]
    reason: str
    value: AlignedValue | None = None


def align_table_value(
    *, scope: ReviewScope, source: SourceVersion, inventory: tuple[OriginalBlock, ...],
    headers: tuple[ColumnHeader, ...], cells: tuple[NumericCell, ...],
    metric: str, period: StatementPeriod, currency: str | None, scale: str | None,
    basis: str | None, units_block_id: str,
    expected_currency: str, expected_scale: str, expected_basis: str,
) -> AlignmentCheck:
    """Associate numeric cells with supplied geometry/periods, not column order.

    Values remain unscaled original strings. KNOWN means unambiguous alignment,
    not HUMAN_SUPPORTED or permission to use an incomplete evidence packet.
    """
    if not inventory or max(len(inventory), len(headers), len(cells)) > 64:
        return AlignmentCheck("UNVERIFIED", "EMPTY_OR_OVERSIZED_TABLE")
    blocks = {b.block_id: b for b in inventory}
    if len(blocks) != len(inventory) or any(
        b.scope != scope or b.source != source for b in inventory
    ):
        return AlignmentCheck("UNVERIFIED", "SCOPE_OR_SOURCE_MISMATCH")
    if not currency or not scale or not basis or units_block_id not in blocks:
        return AlignmentCheck("UNVERIFIED", "MISSING_UNITS_OR_BASIS")
    if (currency, scale, basis) != (expected_currency, expected_scale, expected_basis):
        return AlignmentCheck("UNVERIFIED", "INCOMPATIBLE_UNITS_OR_BASIS")
    referenced = ({units_block_id} | {h.block_id for h in headers}
                  | {c.block_id for c in cells} | {c.row_label_block_id for c in cells})
    if any(k not in blocks or not blocks[k].parser_verified or not blocks[k].fit_verified
           or type(blocks[k].page) is not int or blocks[k].page < 1
           or type(blocks[k].start) is not int or blocks[k].start < 0
           for k in referenced):
        return AlignmentCheck("UNVERIFIED", "UNVERIFIED_OR_MISSING_LOCATION")
    for item in (*headers, *cells):
        if (not item.layout_id or not isinstance(item.x0, Decimal) or not isinstance(item.x1, Decimal)
                or not item.x0.is_finite() or not item.x1.is_finite() or item.x0 >= item.x1):
            return AlignmentCheck("UNVERIFIED", "INVALID_GEOMETRY")
    for index, header in enumerate(headers):
        if any(header.layout_id == other.layout_id and max(header.x0, other.x0) < min(header.x1, other.x1)
               for other in headers[index + 1:]):
            return AlignmentCheck("UNVERIFIED", "OVERLAPPING_HEADERS")
    matches: list[tuple[NumericCell, ColumnHeader]] = []
    for cell in cells:
        if cell.metric != metric:
            continue
        containing = [h for h in headers if h.layout_id == cell.layout_id
                      and h.x0 <= cell.x0 and cell.x1 <= h.x1]
        if len(containing) != 1:
            return AlignmentCheck("UNVERIFIED", "MISSING_OR_AMBIGUOUS_YEAR_HEADER")
        if containing[0].period == period:
            matches.append((cell, containing[0]))
    if not matches:
        return AlignmentCheck("MISSING", "REQUESTED_METRIC_PERIOD_ABSENT")
    if len(matches) != 1:
        return AlignmentCheck("CONFLICT", "MULTIPLE_CELLS_FOR_METRIC_PERIOD")
    cell, header = matches[0]
    try:
        raw = blocks[cell.block_id].text
        money_string(raw)
    except InputError:
        return AlignmentCheck("UNVERIFIED", "NONCANONICAL_NUMERIC_CELL")
    return AlignmentCheck("KNOWN", "EXPLICIT_PERIOD_GEOMETRY_MATCH", AlignedValue(
        raw, period, currency, scale, basis, source,
        tuple(sorted({cell.block_id, header.block_id, cell.row_label_block_id, units_block_id})),
    ))
