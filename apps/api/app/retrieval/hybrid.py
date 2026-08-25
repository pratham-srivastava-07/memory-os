from apps.api.app.repository import search_vectors, lexical_search
from apps.api.app.retrieval.semantic_search import encode_query

def hybrid_retrieve(query: str, k: int = 10):
    query_embeddings = encode_query(query=query)

    final_result = []

    sematic_search = search_vectors(query_embeddings=query_embeddings, k=10)
    lexical_retrieval = lexical_search(query=query, k=10)

    # now we rerank here and extract top k

    return final_result



