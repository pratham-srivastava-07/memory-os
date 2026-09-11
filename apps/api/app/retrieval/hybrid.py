from __future__ import annotations

import logging
from typing import Any

from apps.api.app.repository import search_vectors, lexical_search
from apps.api.app.retrieval.semantic_search import encode_query
from apps.api.app.core.rrf import reciprocal_ranking_fusion
from apps.api.app.core.rerank import rerank

logger = logging.getLogger(__name__)

def hybrid_retrieve(query: str, k: int = 10, candidate_k: int = 10, use_reranker: bool = False) -> list[dict[str, Any]]:
    query_embeddings = encode_query(query=query)

    sematic_search = search_vectors(query_embeddings=query_embeddings, k=candidate_k)
    lexical_retrieval = lexical_search(query=query, k=candidate_k)

    logger.info("hybrid_retrieve: %d semantic + %d lexical candidate(s) for %r",
                len(sematic_search), len(lexical_retrieval), query)

    # RRF is the hybrid result; reranking is an optional second stage.
    rrf_result = reciprocal_ranking_fusion(
        sematic_search,
        lexical_retrieval
    )

    if use_reranker:
        return rerank(query=query, candidates=rrf_result, k=k)

    return rrf_result[:k]

