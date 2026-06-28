"""Keyword search (CP14) — V1 fallback over persisted chunks (works without embeddings).

Ranking (CP15 relevance fix): raw term-overlap count favoured long, generic chunks (more words →
more incidental matches). We now score with TF-IDF-style weighting so that (a) rarer query terms
count more than common ones, (b) chunks covering MORE of the query rank higher, and (c) long chunks
are length-normalised so a focused, on-topic chunk beats a sprawling overview. The "≥1 matched term"
gate is unchanged, so the ungrounded → fixed-fallback behaviour (BR-027) is preserved.
"""
from __future__ import annotations

import math
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge.knowledge import Chunk, KnowledgeSource

_STOP = {"the", "a", "an", "of", "to", "in", "and", "or", "is", "are", "for", "on", "by", "what", "how"}


def _terms(text: str) -> set[str]:
    return {t for t in re.findall(r"\w+", (text or "").lower()) if t not in _STOP and len(t) > 1}


def search(db: Session, query: str, top_k: int = 5) -> list[dict]:
    """Return top-k chunks from ACTIVE knowledge sources, ranked by TF-IDF-style relevance."""
    q_terms = _terms(query)
    if not q_terms:
        return []
    rows = db.execute(
        select(Chunk, KnowledgeSource.title, KnowledgeSource.id)
        .join(KnowledgeSource, Chunk.source_id == KnowledgeSource.id)
        .where(KnowledgeSource.status == "active")
    ).all()

    # Pre-compute chunk term sets once, and document frequency for each query term.
    prepared = [(chunk, title, sid, _terms(chunk.text)) for chunk, title, sid in rows]
    n_docs = len(prepared) or 1
    df = {term: sum(1 for _, _, _, ct in prepared if term in ct) for term in q_terms}

    def _idf(term: str) -> float:
        # Smoothed IDF: always positive, even when a term appears in every chunk (df == n_docs).
        return math.log((n_docs + 1) / (df.get(term, 0) + 1)) + 1.0

    scored = []
    for chunk, title, sid, c_terms in prepared:
        matched = q_terms & c_terms
        if not matched:
            continue
        idf_sum = sum(_idf(t) for t in matched)
        coverage = len(matched) / len(q_terms)          # reward covering more of the query
        length_norm = math.sqrt(len(c_terms) or 1)      # dampen long-chunk bias
        score = idf_sum * coverage / length_norm
        scored.append((score, chunk, title, sid))

    scored.sort(key=lambda s: s[0], reverse=True)
    return [
        {"chunk_id": c.id, "source_id": sid, "title": title, "text": c.text, "score": float(score)}
        for score, c, title, sid in scored[:top_k]
    ]
