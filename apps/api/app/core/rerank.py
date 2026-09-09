from sentence_transformers import CrossEncoder

# global declaration for reranking

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

def rerank(query: str, candidates: list[dict[str, any]], k: int =10) -> list[dict[str, any]]:
    if not candidates:
        return

    pairs = [
        (query, result["content"])
        for result in candidates
    ]

    scores = reranker.predict(pairs)

    reranked = []

    for candidate, score in zip(candidates, scores):
        result = candidate.copy()
        result["rerank_score"] = float(score)
        reranked.append(result)

    reranked.sort(
        key = lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:k]
