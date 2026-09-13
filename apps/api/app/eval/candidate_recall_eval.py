from pathlib import Path
import json

from apps.api.app.core.rrf import reciprocal_ranking_fusion
from apps.api.app.eval.evaluate import deduplicate_results, load_eval_set, result_doc_id
from apps.api.app.repository import lexical_search, search_vectors
from apps.api.app.retrieval.semantic_search import encode_query


eval_set = load_eval_set()

candidate_sizes = (10, 25, 50, 100)

all_results = {}

for candidates_k in candidate_sizes:
    per_query = []

    for item in eval_set:
        query = item["query"]
        relevant_docs = set(item["relevant_documents"])
        query_embeddings = encode_query(query=query)

        # dense 
        semantic_results = search_vectors(query_embeddings=query_embeddings, k=candidates_k)

        #sparse
        lexical_results = lexical_search(query=query, k=candidates_k)

        rrf_results = reciprocal_ranking_fusion(semantic_results, lexical_results)

        unique_candidates = deduplicate_results(results=rrf_results)

        candidate_docs = {
            result_doc_id(result=result) for result in unique_candidates
        }

        found_docs = relevant_docs & candidate_docs

        per_query.append({
            "id": item.get("id"),
            "query": query,
            "candidate_k": candidates_k,
            "n_relevant": len(relevant_docs),
            "n_found": len(found_docs),
            "candidate_recall": len(found_docs) / len(relevant_docs),
            "missed": sorted(relevant_docs - candidate_docs)
        })

    overall = {
        "candidate_k": candidates_k,
        "candidate_recall": sum(
            row["candidate_recall"] for row in per_query
        ) / len(per_query),
        "candidate_hit": sum(
            1 for row in per_query if row["n_found"] > 0
        ) / len(per_query),
        "per_query": per_query,
    }

    all_results[str(candidates_k)] = overall

    print(
        f"candidate_k={candidates_k} "
        f"candidate_recall={overall['candidate_recall']:.3f} "
        f"candidate_hit={overall['candidate_hit']:.3f}"
    )

print("\nCandidate recall summary")
print("=" * 55)
print(f"{'candidate_k':>12} {'candidate_recall':>18} {'candidate_hit':>15}")
print("-" * 55)
for candidates_k, result in all_results.items():
    print(
        f"{candidates_k:>12} "
        f"{result['candidate_recall']:>17.1%} "
        f"{result['candidate_hit']:>14.1%}"
    )

output_path = Path("data/eval/candidate_recall.json")
output_path.write_text(
    json.dumps(all_results, indent=2),
    encoding="utf-8"
)
print(f"\nWrote {output_path}")
