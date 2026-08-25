from apps.api.app.retrieval.semantic_search import encode_query
from apps.api.app.repository import lexical_search

def sparse_retrieval(query: str, k: int = 10):
    result = lexical_search(query=query, k=k)
    return result


if __name__ == "__main__":
    sparse_retrieval("what is the meaning of vector", 10)