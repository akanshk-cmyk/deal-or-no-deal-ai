"""Bounded LOCAL-REFERENCE-1.0 inspection; no crawler, model, or database startup.

Uploaded bytes have user-declared origin. Plain extracted text and row context
are inspection artifacts, not verified support, financial facts or an index.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from importlib.metadata import version
from io import BytesIO
from pathlib import Path, PureWindowsPath
import tomllib
from typing import Literal

from pydantic import Field

from .context import InputError, fingerprint, unicode_scalar
from .contracts import StrictModel, Text


class EmbeddingProfile(StrictModel):
    """Disabled hosted-provider selection, not a verified executable contract."""

    profile_version: Literal["NEBIUS-EMBEDDING-1.1"]
    provider: Literal["NEBIUS"]
    enabled: Literal[False]
    model_id: Literal["Qwen/Qwen3-Embedding-8B"]
    capability_status: Literal["CATALOG_ONLY_NOT_RUNTIME_VERIFIED"]
    input_usd_per_million_tokens: Literal["0.01"]
    output_usd_per_million_tokens: Literal["0"]
    pricing_checked_on: Literal["2026-10-23"]
    artifact_revision: Literal["UNCONFIGURED"]
    token_count_strategy: Literal["UNCONFIGURED"]
    budget_status: Literal["NOT_APPROVED"]
    dimensions: Literal[4096]
    max_input_tokens: None = None
    download_on_import: Literal[False]


class ReferenceStorage(StrictModel):
    backend: Literal["SQLITE_EXACT_COSINE"]
    index_enabled: Literal[False]
    max_children: int = Field(gt=0, le=500)


class ReferenceProfile(StrictModel):
    profile_version: Literal["LOCAL-REFERENCE-1.0"]
    mode: Literal["LOCAL_FILE"]
    corpus_id: Literal["CAMPBELL-AGREEMENT-2024-REFERENCE"]
    declared_company: Literal["Campbell Soup Company"]
    declared_document_type: Literal["LOAN_AGREEMENT"]
    declared_agreement_date: Literal["2024-04-16"]
    declared_source_url: Literal[
        "https://www.sec.gov/Archives/edgar/data/16732/000119312524097732/d806817dex10.htm"
    ]
    max_file_bytes: int = Field(gt=0, le=10 * 1024 * 1024)
    max_pdf_pages: int = Field(gt=0, le=250)
    crawler_enabled: Literal[False]
    embedding: EmbeddingProfile
    storage: ReferenceStorage


def load_reference_profile(workspace: Path) -> ReferenceProfile:
    """Read trusted configuration only; no environment, setup or source I/O."""
    with (workspace / "config/source_ingestion.toml").open("rb") as stream:
        return ReferenceProfile.model_validate(tomllib.load(stream))


@dataclass(frozen=True)
class InspectionBlock:
    block_id: str
    kind: str
    text: str
    page: int | None = None
    cells: tuple[str, ...] = ()
    header_cells: tuple[bool, ...] = ()


@dataclass(frozen=True)
class LocalReferenceInspection:
    corpus_id: str | None
    filename: str
    media_type: str
    content_sha256: str
    text_sha256: str
    observed_at: str
    byte_count: int
    page_count: int | None
    parser: str
    blocks: tuple[InspectionBlock, ...]
    profile_digest: str
    inspection_digest: str
    declared_source: dict
    expected_profile_source: dict
    inspection_schema_version: str = "LOCAL-REFERENCE-1.1"
    status: str = "INSPECTION_ONLY"
    origin_status: str = "UNBOUND_LOCAL_UPLOAD"
    scope_status: str = "NO_CORPUS_ADMISSION"
    support_status: str = "UNVERIFIED"
    final_ready: bool = False
    index_created: bool = False
    model_calls: int = 0


class _StaticHTML(HTMLParser):
    """Ordered static text/table rows; never render HTML or resolve resources."""

    _inactive = {"script", "style", "template", "head"}
    _boundaries = {"p", "div", "section", "article", "br", "li", "hr", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.text = []
        self.ignored = []
        self.row = None
        self.cell = None
        self.header = False
        self.heading = False

    def flush(self):
        text = " ".join("".join(self.text).split())
        if text:
            self.parts.append(("HEADING" if self.heading else "TEXT", text, (), ()))
        self.text = []

    def finish_cell(self):
        if self.cell is not None:
            if self.row is None:
                raise InputError("UNVERIFIED_HTML_TABLE_STRUCTURE")
            self.row.append((" ".join("".join(self.cell).split()), self.header))
            self.cell = None

    def handle_starttag(self, tag, attrs):
        if self.ignored:
            if tag in self._inactive:
                self.ignored.append(tag)
            return
        if tag in self._inactive:
            self.flush()
            self.ignored.append(tag)
            return
        if tag == "tr":
            if self.row is not None:
                raise InputError("UNVERIFIED_NESTED_OR_UNCLOSED_TABLE_ROW")
            self.flush()
            self.row = []
        elif tag in {"td", "th"}:
            self.finish_cell()
            if self.row is None:
                raise InputError("UNVERIFIED_HTML_TABLE_STRUCTURE")
            self.cell = []
            self.header = tag == "th"
        elif tag in self._boundaries:
            if self.cell is not None:
                self.cell.append("\n")
            else:
                self.flush()
                self.heading = tag.startswith("h") and tag[1:].isdigit()

    def handle_startendtag(self, tag, attrs):
        if tag not in self._inactive:
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.ignored:
            if tag == self.ignored[-1]:
                self.ignored.pop()
            return
        if tag in {"td", "th"}:
            self.finish_cell()
        elif tag == "tr":
            self.finish_cell()
            if self.row is None:
                raise InputError("UNVERIFIED_HTML_TABLE_STRUCTURE")
            cells = tuple(value for value, _ in self.row)
            headers = tuple(flag for _, flag in self.row)
            if any(cells):
                self.parts.append(("TABLE_ROW", " | ".join(cells), cells, headers))
            self.row = None
        elif tag in self._boundaries:
            if self.cell is not None:
                self.cell.append("\n")
            else:
                self.flush()
                self.heading = False

    def handle_data(self, data):
        if not self.ignored:
            (self.cell if self.cell is not None else self.text).append(data)

    def result(self):
        self.close()
        self.flush()
        if self.ignored or self.row is not None or self.cell is not None:
            raise InputError("UNVERIFIED_UNCLOSED_HTML_STRUCTURE")
        return tuple(InspectionBlock(f"HTML-BLOCK-{i}", kind, text,
                                    cells=cells, header_cells=headers)
                     for i, (kind, text, cells, headers) in enumerate(self.parts, 1))


def inspect_uploaded_reference(filename: str, content: bytes, profile: ReferenceProfile,
                               *, observed_at: datetime,
                               html_encoding: Literal["utf-8", "windows-1252"] = "utf-8") -> LocalReferenceInspection:
    """Inspect explicit supplied bytes without filesystem paths or external actions."""
    # Revalidate even an object built via model_construct/model_copy.
    profile = ReferenceProfile.model_validate(profile.model_dump())
    if (type(filename) is not str or not filename.strip() or len(filename) > 255
            or filename != Path(filename).name or filename != PureWindowsPath(filename).name
            or any(c in filename for c in '\\/:\x00')):
        raise InputError("UPLOAD_BASENAME_REQUIRED")
    unicode_scalar(filename)
    if type(content) is not bytes or not content or len(content) > profile.max_file_bytes:
        raise InputError("EMPTY_OR_OVERSIZED_REFERENCE_BYTES")
    if (type(observed_at) is not datetime or observed_at.tzinfo is None
            or observed_at.utcoffset() is None):
        raise InputError("EXPLICIT_AWARE_OBSERVATION_TIMESTAMP_REQUIRED")
    if html_encoding not in {"utf-8", "windows-1252"}:
        raise InputError("UNSUPPORTED_HTML_ENCODING")
    suffix = Path(filename).suffix.lower()
    if suffix in {".html", ".htm"}:
        if content.lstrip().startswith(b"%PDF-"):
            raise InputError("CONTENT_TYPE_MISMATCH")
        try:
            text = content.decode(html_encoding, errors="strict")
        except UnicodeError as error:
            raise InputError("EXPLICIT_HTML_ENCODING_REQUIRED") from error
        if "\x00" in text:
            raise InputError("INVALID_HTML_TEXT")
        parser = _StaticHTML()
        parser.feed(text)
        blocks = parser.result()
        # Plain mislabeled files are not silently admitted as HTML.
        if not any(marker in text.lower() for marker in ("<html", "<body", "<p", "<div", "<table", "<h1")):
            raise InputError("HTML_MARKUP_REQUIRED")
        page_count, media, parser_name = None, "text/html", "stdlib.HTMLParser/LOCAL-REFERENCE-1.0"
    elif suffix == ".pdf":
        if not content.startswith(b"%PDF-"):
            raise InputError("CONTENT_TYPE_MISMATCH")
        from pypdf import PdfReader
        try:
            reader = PdfReader(BytesIO(content), strict=True)
            if reader.is_encrypted:
                raise InputError("ENCRYPTED_REFERENCE_UNSUPPORTED")
            page_count = len(reader.pages)
            if not 0 < page_count <= profile.max_pdf_pages:
                raise InputError("REFERENCE_PAGE_LIMIT")
            blocks = tuple(InspectionBlock(f"PDF-PAGE-{i}", "PDF_PAGE", page.extract_text() or "", page=i)
                           for i, page in enumerate(reader.pages, 1))
            if any(not block.text.strip() for block in blocks):
                raise InputError("REFERENCE_PAGE_WITHOUT_TEXT_NO_OCR")
        except InputError:
            raise
        except Exception as error:
            raise InputError("UNREADABLE_REFERENCE_PDF") from error
        media, parser_name = "application/pdf", "pypdf/" + version("pypdf")
    else:
        raise InputError("UNSUPPORTED_REFERENCE_FILE_TYPE")
    if not blocks or not any(block.text.strip() for block in blocks):
        raise InputError("REFERENCE_WITHOUT_TEXT")
    for block in blocks:
        unicode_scalar(block.text)
    raw_digest = sha256(content).hexdigest()
    profile_digest = fingerprint("REFERENCE_PROFILE", profile.model_dump())
    observation = observed_at.astimezone(timezone.utc).isoformat()
    text_digest = fingerprint("REFERENCE_EXTRACTED_BLOCKS", [vars(b) for b in blocks])
    expectation = dict(corpus_id=profile.corpus_id, company=profile.declared_company,
                  document_type=profile.declared_document_type,
                  agreement_date=profile.declared_agreement_date, url=profile.declared_source_url)
    return LocalReferenceInspection(
        None, filename, media, raw_digest, text_digest, observation,
        len(content), page_count, parser_name, blocks, profile_digest,
        fingerprint("LOCAL_REFERENCE_INSPECTION-1.1", dict(content=raw_digest, profile=profile_digest,
                    text=text_digest, observed_at=observation, filename=filename, parser=parser_name)),
        {}, expectation,
    )
