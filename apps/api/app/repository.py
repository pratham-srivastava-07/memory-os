from apps.api.app.db import get_connection

def insert_chunk(content: str, source: str, embeddings):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chunks (content, source, embeddings)
                VALUES (%s, %s, %s)
                """, content, source, embeddings.toList())

            conn.commit()
    except:
        raise ValueError("Couldnot commit to db")
    finally:
        conn.close()

def search_vectors(query_embeddings, k: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT id, content, source, 1 - (embedding <=> %s) AS score FROM chunks ORDER BY embedding <=> %s LIMIT %s;
                """, query_embeddings, query_embeddings, k)
        conn.commit()
    except:
        raise ValueError("Could not retrieve from db")
    finally:
        conn.close()