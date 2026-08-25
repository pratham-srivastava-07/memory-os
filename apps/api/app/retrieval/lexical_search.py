from __future__ import annotations

import logging
from typing import Any

from apps.api.app.repository import lexical_search

logger = logging.getLogger(__name__)

def sparse_retrieval(query: str, k: int = 10) -> list[dict[str, Any]]:
    result = lexical_search(query=query, k=k)
    logger.info("sparse_retrieval: %d result(s) for %r (k=%d)", len(result), query, k)
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    sparse_retrieval("what is the meaning of vector", 10)