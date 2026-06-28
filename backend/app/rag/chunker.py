"""Chunker (CP14) — split text into overlapping chunks for retrieval."""
from __future__ import annotations

import re

DEFAULT_SIZE = 600      # chars
DEFAULT_OVERLAP = 80


def chunk_text(text: str, size: int = DEFAULT_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[str]:
    if not text:
        return []
    # normalise whitespace; prefer paragraph boundaries
    text = re.sub(r"\r\n?", "\n", text).strip()
    if len(text) <= size:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks
