import json
import time
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

for candidate_k in (10, 25, 50, 100):
    retrieve_fn = partial(
        hybrid_retrieve,
        candidate_k=candidate_k,
        use_reranker=True,
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
        "candidate_k": candidate_k,
        "n_measurements": len(stage_samples["total_ms"]),
        "stages": {
            stage: summarize(values)
            for stage, values in sorted(stage_samples.items())
        },
    }

    print(result)

    output_path = Path(
        f"data/eval/latency_candidate_{candidate_k}.json"
    )

    output_path.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
