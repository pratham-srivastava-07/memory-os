from __future__ import annotations

import logging
from typing import Any

from apps.api.app.repository import search_vectors, lexical_search
from apps.api.app.retrieval.semantic_search import encode_query
from apps.api.app.core.rrf import reciprocal_ranking_fusion

logger = logging.getLogger(__name__)

def hybrid_retrieve(query: str, k: int = 10) -> list[dict[str, Any]]:
    query_embeddings = encode_query(query=query)

    sematic_search = search_vectors(query_embeddings=query_embeddings, k=10)
    lexical_retrieval = lexical_search(query=query, k=10)

    logger.info("hybrid_retrieve: %d semantic + %d lexical candidate(s) for %r",
                len(sematic_search), len(lexical_retrieval), query)

    # now we rerank here and extract top k

    rrf_result = reciprocal_ranking_fusion(
        sematic_search,
        lexical_retrieval
    )

    logger.info(
    "hybrid_retrieve: returning top %d fused results",
    min(k, len(rrf_result))
    )
    return rrf_result[:k]



