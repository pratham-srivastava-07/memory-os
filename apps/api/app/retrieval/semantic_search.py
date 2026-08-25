from sentence_transformers import SentenceTransformer
from apps.api.utils.helper import load_corpus
from apps.api.app.repository import search_vectors

# embedder for embedding corpus text
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def encode_query(query):
    return embedder.encode_query(query, convert_to_tensor=True)


# retrieval pipeline wiring
def retrieve(query: str, k: int = 5):
    query_embedding = encode_query(query)

    # retrieve data from postgres, with searching from query embeddings and k

    result = search_vectors(query_embedding, k)
    print(f"Retrieved info: {result}")
    return result

if __name__ == "__main__":
    retrieve("What is meant by chunking", 5)
    