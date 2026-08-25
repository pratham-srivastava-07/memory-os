from apps.api.app.db import get_connection

def insert_chunk(content: str, source: str, embeddings):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chunks (content, source, embedding)
                VALUES (%s, %s, %s)
                """, (content, source, embeddings.tolist()))

            conn.commit()
    except:
        raise ValueError("Couldnot commit to db")
    finally:
        conn.close()

def search_vectors(query_embeddings, k: int):
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
        conn.rollback()
        raise ValueError("Could not retrieve from db") from e
    finally:
        conn.close()

    return [{"id": r[0], "content": r[1], "source": r[2], "score": float(r[3])}
            for r in rows]