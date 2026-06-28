"""In-memory vector store (CP14 V1). Pluggable; pgvector/Chroma later. Used only when embeddings exist."""
from __future__ import annotations

import math


class InMemoryVectorStore:
    def __init__(self):
        self._items: dict[str, tuple[list[float], dict]] = {}

    def add(self, chunk_id: str, vector: list[float], meta: dict) -> None:
        self._items[chunk_id] = (vector, meta)

    def remove_source(self, source_id: str) -> None:
        self._items = {k: v for k, v in self._items.items() if v[1].get("source_id") != source_id}

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0

    def search(self, query_vec: list[float], top_k: int = 5) -> list[dict]:
        scored = [(self._cosine(query_vec, vec), cid, meta) for cid, (vec, meta) in self._items.items()]
        scored = [s for s in scored if s[0] > 0]
        scored.sort(key=lambda s: s[0], reverse=True)
        return [{"chunk_id": cid, "score": round(score, 4), **meta} for score, cid, meta in scored[:top_k]]

    def size(self) -> int:
        return len(self._items)


# process-wide store (V1)
VECTOR_STORE = InMemoryVectorStore()
