from __future__ import annotations

import logging
from typing import Any

from apps.api.app.db import get_connection

logger = logging.getLogger(__name__)

def insert_chunk(content: str, source: str, embeddings: Any) -> None:
    logger.debug("insert_chunk: source=%s content=%d chars", source, len(content))
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chunks (content, source, embedding)
                VALUES (%s, %s, %s)
                """, (content, source, embeddings.tolist()))

            conn.commit()
    except:
        logger.exception("insert_chunk failed for source=%s", source)
        raise ValueError("Couldnot commit to db")
    finally:
        conn.close()

def search_vectors(query_embeddings: Any, k: int) -> list[dict[str, Any]]:
    logger.debug("search_vectors: k=%d", k)
    if hasattr(query_embeddings, "tolist"):      
        query_embeddings = query_embeddings.tolist()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, content, source,
                    1 - (embedding <=> %s::vector) AS score
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """, (query_embeddings, query_embeddings, k))
            rows = cur.fetchall()       
    except Exception as e:
        logger.exception("search_vectors failed (k=%s)", k)
        conn.rollback()
        raise ValueError("Could not retrieve from db") from e
    finally:
        conn.close()

    logger.info("search_vectors: returned %d row(s) for k=%d", len(rows), k)
    return [{"id": r[0], "content": r[1], "source": r[2], "score": float(r[3])}
            for r in rows]

def lexical_search(query: str, k: int = 10) -> list[dict[str, Any]]:
    logger.debug("lexical_search: k=%d query=%r", k, query)
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT id, content, source, ts_rank_cd(content_tsv, websearch_to_tsquery('english', %s)) AS score FROM chunks WHERE content_tsv @@ websearch_to_tsquery('english', %s) ORDER BY score DESC
                    LIMIT %s;""", (query, query, k))
            rows = cur.fetchall()
    except Exception as e:
        logger.exception("lexical_search failed (k=%s query=%r)", k, query)
        conn.rollback()
        raise ValueError("Could not fetch via lexical search from db")
    finally:
        conn.close()

    logger.info("lexical_search: returned %d row(s) for k=%d", len(rows), k)
    return [{"id": r[0], "content": r[1], "source": r[2], "score": float(r[3])}
        for r in rows]