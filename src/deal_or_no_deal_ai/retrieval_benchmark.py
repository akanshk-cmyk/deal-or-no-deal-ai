"""Offline scoped DIRECT/BM25/cosine/RRF mechanics; no downloads, model or index I/O."""
from dataclasses import dataclass
import math
import re
from collections import Counter
from .context import InputError, fingerprint


@dataclass(frozen=True)
class Passage:
    passage_id: str
    text: str
    scope_digest: str
    source_sha256: str
    page: int
    eligible: bool


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def retrieve(passages, query, *, scope_digest, strategy="DIRECT", vectors=None, query_vector=None, top_k=5):
    if strategy not in {"DIRECT", "KEYWORD", "VECTOR", "HYBRID"} or type(top_k) is not int or not 1 <= top_k <= 20:
        raise InputError("UNSUPPORTED_RETRIEVAL_REQUEST")
    if not isinstance(query, str) or not query.strip() or len(query) > 4096 or len(passages) > 500:
        raise InputError("BOUNDED_RETRIEVAL_QUERY_REQUIRED")
    if len({p.passage_id for p in passages}) != len(passages):
        raise InputError("DUPLICATE_PASSAGE_ID")
    eligible = [p for p in passages if p.eligible is True and p.scope_digest == scope_digest]
    excluded = [p.passage_id for p in passages if p not in eligible]
    if strategy == "DIRECT":
        selected = eligible
    else:
        counters = [Counter(_tokens(p.text)) for p in eligible]
        average = sum(sum(c.values()) for c in counters) / max(1, len(counters))
        words = set(_tokens(query)); scores = {}
        for p, counts in zip(eligible, counters):
            score = 0.0
            for word in words:
                frequency = counts[word]
                document_frequency = sum(word in c for c in counters)
                idf = math.log(1 + (len(counters) - document_frequency + .5) / (document_frequency + .5))
                if frequency and average:
                    score += idf * frequency * 2.2 / (frequency + 1.2 * (.25 + .75 * sum(counts.values()) / average))
            scores[p.passage_id] = score
        keyword = sorted(eligible, key=lambda p: (-scores[p.passage_id], p.passage_id))
        keyword = [p for p in keyword if scores[p.passage_id] > 0]
        if strategy == "KEYWORD":
            selected = keyword[:top_k]
        else:
            if not vectors or query_vector is None:
                raise InputError("ACTUAL_EMBEDDINGS_REQUIRED_NO_FALLBACK")
            def normalized(vector):
                if not vector or any(type(v) not in (float, int) or not math.isfinite(v) for v in vector):
                    raise InputError("FINITE_NONZERO_VECTORS_REQUIRED")
                norm = math.sqrt(sum(v * v for v in vector))
                if norm == 0 or not math.isfinite(norm):
                    raise InputError("FINITE_NONZERO_VECTORS_REQUIRED")
                return [v / norm for v in vector]
            query_normalized = normalized(query_vector); similarities = {}
            for p in eligible:
                if p.passage_id not in vectors or len(vectors[p.passage_id]) != len(query_vector):
                    raise InputError("CURRENT_EMBEDDING_DIMENSIONS_REQUIRED")
                vector = normalized(vectors[p.passage_id])
                similarities[p.passage_id] = sum(a * b for a, b in zip(query_normalized, vector))
            semantic = sorted(eligible, key=lambda p: (-similarities[p.passage_id], p.passage_id))
            if strategy == "VECTOR":
                selected = semantic[:top_k]
            else:
                fused = Counter()
                for ranking in (keyword, semantic):
                    for rank, p in enumerate(ranking, 1):
                        fused[p.passage_id] += 1 / (60 + rank)
                selected = sorted(eligible, key=lambda p: (-fused[p.passage_id], p.passage_id))[:top_k]
    return dict(strategy=strategy, ranked=strategy != "DIRECT", passage_ids=[p.passage_id for p in selected],
        contexts=[p.text for p in selected], source_refs=[dict(id=p.passage_id, sha256=p.source_sha256, page=p.page) for p in selected],
        excluded_ids=excluded, scope_digest=scope_digest, input_digest=fingerprint("RETRIEVAL_INPUT", dict(query=query, scope=scope_digest, strategy=strategy)))
