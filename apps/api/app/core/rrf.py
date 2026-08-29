from collections import defaultdict

K_RRF = 50

def reciprocal_ranking_fusion(*rankings: list[list[str]], k: int = K_RRF) -> list[tuple[str, int]]:
    scores: dict[str, int] = defaultdict(float)

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1.0 / (k + rank)

    return sorted(scores.items(), key=lambda x: -x[1])