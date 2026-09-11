import json
import time
from functools import partial
from pathlib import Path
from statistics import median

from apps.api.app.eval.evaluate import load_eval_set
from apps.api.app.retrieval.hybrid import hybrid_retrieve


def percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    index = round((percentile / 100) * (len(ordered) - 1))
    return ordered[index]


eval_set = load_eval_set()
repetitions = 10

for candidate_k in (10, 25, 50, 100):
    retrieve_fn = partial(
        hybrid_retrieve,
        candidate_k=candidate_k,
        use_reranker=True,
    )

    # Warm-up
    for item in eval_set[:3]:
        retrieve_fn(item["query"], k=10)

    latencies_ms = []

    for _ in range(repetitions):
        for item in eval_set:
            start = time.perf_counter_ns()

            retrieve_fn(item["query"], k=10)

            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
            latencies_ms.append(elapsed_ms)

    result = {
        "candidate_k": candidate_k,
        "n_measurements": len(latencies_ms),
        "p50_ms": median(latencies_ms),
        "p95_ms": percentile(latencies_ms, 95),
        "p99_ms": percentile(latencies_ms, 99),
        "mean_ms": sum(latencies_ms) / len(latencies_ms),
    }

    print(result)

    output_path = Path(
        f"data/eval/latency_candidate_{candidate_k}.json"
    )

    output_path.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )