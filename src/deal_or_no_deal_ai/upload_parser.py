"""Short-lived PDF text worker; stdin bytes, bounded JSON stdout, no file/network tools."""
from io import BytesIO
import json
import sys


def main():
    raw = sys.stdin.buffer.read(10_000_001)
    result = {}
    page_number = None
    try:
        if not raw or len(raw) > 10_000_000 or not raw.startswith(b"%PDF-"):
            raise ValueError("INVALID_PDF_BYTES")
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(raw), strict=True)
        if reader.is_encrypted:
            raise ValueError("ENCRYPTED_PDF_UNSUPPORTED")
        if not 1 <= len(reader.pages) <= 10:
            raise ValueError("PDF_PAGE_LIMIT")
        pages, size = [], 0
        for page_number, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if not text.strip():
                raise ValueError("PAGE_WITHOUT_TEXT_NO_OCR")
            size += len(text.encode("utf-8"))
            if size > 120_000:
                raise ValueError("EXTRACTED_TEXT_LIMIT")
            pages.append(text)
        result = dict(pages=pages)
    except Exception as error:
        allowed = {"INVALID_PDF_BYTES", "ENCRYPTED_PDF_UNSUPPORTED", "PDF_PAGE_LIMIT", "PAGE_WITHOUT_TEXT_NO_OCR", "EXTRACTED_TEXT_LIMIT"}
        result = dict(error=str(error) if str(error) in allowed else "UNREADABLE_PDF", page=page_number)
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
