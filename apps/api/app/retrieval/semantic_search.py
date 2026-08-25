from __future__ import annotations

import logging
from typing import Any

from sentence_transformers import SentenceTransformer
from apps.api.utils.helper import load_corpus
from apps.api.app.repository import search_vectors

logger = logging.getLogger(__name__)

# embedder for embedding corpus text
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def encode_query(query: str) -> Any:
    logger.debug("encode_query: %r", query)
    return embedder.encode_query(query, convert_to_tensor=True)


# retrieval pipeline wiring
def retrieve(query: str, k: int = 5) -> list[dict[str, Any]]:
    query_embedding = encode_query(query)

    # retrieve data from postgres, with searching from query embeddings and k

    result = search_vectors(query_embedding, k)
    logger.info("retrieve: %d result(s) for %r (k=%d)", len(result), query, k)
    logger.debug("retrieve results: %s", result)
    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    retrieve("What is meant by chunking", 5)
    