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