from __future__ import annotations

import logging
import time
from typing import Any

from apps.api.app.repository import search_vectors, lexical_search
from apps.api.app.retrieval.semantic_search import encode_query
from apps.api.app.core.rrf import reciprocal_ranking_fusion
from apps.api.app.core.rerank import rerank

logger = logging.getLogger(__name__)

def hybrid_retrieve(
    query: str,
    k: int = 10,
    candidate_k: int = 10,
    use_reranker: bool = False,
    timings: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    total_start = time.perf_counter_ns()

    stage_start = time.perf_counter_ns()
    query_embeddings = encode_query(query=query)
    if timings is not None:
        timings["embedding_ms"] = (time.perf_counter_ns() - stage_start) / 1_000_000

    stage_start = time.perf_counter_ns()
    sematic_search = search_vectors(query_embeddings=query_embeddings, k=candidate_k)
    if timings is not None:
        timings["vector_search_ms"] = (time.perf_counter_ns() - stage_start) / 1_000_000

    stage_start = time.perf_counter_ns()
    lexical_retrieval = lexical_search(query=query, k=candidate_k)
    if timings is not None:
        timings["lexical_search_ms"] = (time.perf_counter_ns() - stage_start) / 1_000_000

    logger.info("hybrid_retrieve: %d semantic + %d lexical candidate(s) for %r",
                len(sematic_search), len(lexical_retrieval), query)

    # RRF is the hybrid result; reranking is an optional second stage.
    stage_start = time.perf_counter_ns()
    rrf_result = reciprocal_ranking_fusion(
        sematic_search,
        lexical_retrieval
    )
    if timings is not None:
        timings["rrf_ms"] = (time.perf_counter_ns() - stage_start) / 1_000_000

    if use_reranker:
        stage_start = time.perf_counter_ns()
        result = rerank(query=query, candidates=rrf_result, k=k)
        if timings is not None:
            timings["reranker_ms"] = (time.perf_counter_ns() - stage_start) / 1_000_000
    else:
        result = rrf_result[:k]

    if timings is not None:
        timings["total_ms"] = (time.perf_counter_ns() - total_start) / 1_000_000
    return result

