from collections import defaultdict
from typing import Any

K_RRF = 50

def reciprocal_ranking_fusion(
    *rankings: list[dict[str, Any]], k: int = K_RRF
) -> list[dict[str, Any]]:
    """Fuse ranked document rows while preserving their payload.

    Retrieval rows contain the ``content`` needed by the cross-encoder, so
    fusion must return rows rather than reducing them to ``(id, score)``
    tuples. The fused score is exposed separately as ``rrf_score``.
    """
    scores: dict[Any, float] = defaultdict(float)
    documents: dict[Any, dict[str, Any]] = {}

    for ranking in rankings:
        for rank, document in enumerate(ranking, start=1):
            doc_id = document.get("id", document.get("path"))
            if doc_id is None:
                raise ValueError("RRF documents must contain 'id' or 'path'")
            scores[doc_id] += 1.0 / (k + rank)
            documents.setdefault(doc_id, document)

    fused = []
    for doc_id, score in sorted(scores.items(), key=lambda item: -item[1]):
        document = documents[doc_id].copy()
        document["rrf_score"] = score
        fused.append(document)
    return fused
