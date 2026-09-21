import json
from functools import partial
from pathlib import Path
from statistics import median
from collections import defaultdict

from apps.api.app.eval.evaluate import load_eval_set
from apps.api.app.retrieval.hybrid import hybrid_retrieve


def percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    index = round((percentile / 100) * (len(ordered) - 1))
    return ordered[index]


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "p50_ms": median(values),
        "p95_ms": percentile(values, 95),
        "p99_ms": percentile(values, 99),
        "mean_ms": sum(values) / len(values),
    }


eval_set = load_eval_set()
repetitions = 10
results_summary: list[dict] = []

for use_reranker in (False, True):
    mode = "reranked" if use_reranker else "rrf_only"

    for candidate_k in (10, 25, 50, 100):
        retrieve_fn = partial(
            hybrid_retrieve,
            candidate_k=candidate_k,
            use_reranker=use_reranker,
        )

        # Warm-up
        for item in eval_set[:3]:
            retrieve_fn(item["query"], k=10)

        stage_samples: dict[str, list[float]] = defaultdict(list)

        for _ in range(repetitions):
            for item in eval_set:
                timings: dict[str, float] = {}
                retrieve_fn(item["query"], k=10, timings=timings)
                for stage, elapsed_ms in timings.items():
                    stage_samples[stage].append(elapsed_ms)

        result = {
            "mode": mode,
            "candidate_k": candidate_k,
            "n_measurements": len(stage_samples["total_ms"]),
            "stages": {
                stage: summarize(values)
                for stage, values in sorted(stage_samples.items())
            },
        }
        results_summary.append(result)

        print(result)

        output_path = Path(
            f"data/eval/latency_{mode}_candidate_{candidate_k}.json"
        )

        output_path.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

print("\nLatency summary")
print("=" * 86)
print(
    f"{'mode':<12} {'candidate_k':>12} {'p50_ms':>10} "
    f"{'p95_ms':>10} {'p99_ms':>10} {'rerank_p95_ms':>15}"
)
print("-" * 86)
for result in results_summary:
    stages = result["stages"]
    rerank_p95 = stages.get("reranker_ms", {}).get("p95_ms")
    rerank_text = f"{rerank_p95:.1f}" if rerank_p95 is not None else "-"
    total = stages["total_ms"]
    print(
        f"{result['mode']:<12} {result['candidate_k']:>12} "
        f"{total['p50_ms']:>10.1f} {total['p95_ms']:>10.1f} "
        f"{total['p99_ms']:>10.1f} {rerank_text:>15}"
    )
