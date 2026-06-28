"""Document processing (CP14) — V1 text extraction for PDF/DOCX/TXT/MD.

TXT/MD are decoded directly. PDF/DOCX use lazy imports (pypdf / python-docx); if a parser is missing
or extraction fails, a clear error is returned (the source is not silently dropped).
"""
from __future__ import annotations

import base64


def _maybe_b64_to_bytes(content) -> bytes | None:
    if isinstance(content, bytes):
        return content
    if isinstance(content, str):
        try:
            return base64.b64decode(content, validate=True)
        except Exception:
            return None
    return None


def extract_text(*, fmt: str, content) -> tuple[str | None, str | None]:
    """Return (text, error). `content` is raw text (TXT/MD) or base64/bytes (PDF/DOCX)."""
    fmt = (fmt or "").lower().lstrip(".")
    try:
        if fmt in ("txt", "md", "markdown", "text"):
            text = content.decode("utf-8", "ignore") if isinstance(content, bytes) else str(content)
            return text, None

        if fmt == "pdf":
            data = _maybe_b64_to_bytes(content)
            if data is None:
                return None, "PDF content must be bytes or base64."
            try:
                import io
                from pypdf import PdfReader
            except ImportError:
                return None, "PDF support requires 'pypdf' (pip install pypdf)."
            reader = PdfReader(io.BytesIO(data))
            return "\n".join((p.extract_text() or "") for p in reader.pages), None

        if fmt in ("docx", "doc"):
            data = _maybe_b64_to_bytes(content)
            if data is None:
                return None, "DOCX content must be bytes or base64."
            try:
                import io
                import docx  # python-docx
            except ImportError:
                return None, "DOCX support requires 'python-docx' (pip install python-docx)."
            d = docx.Document(io.BytesIO(data))
            return "\n".join(p.text for p in d.paragraphs), None

        return None, f"Unsupported format '{fmt}'. Supported: PDF, DOCX, TXT, MD."
    except Exception as exc:  # never crash ingestion
        return None, f"Extraction failed: {exc}"
