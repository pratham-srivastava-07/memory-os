import json
from functools import partial
from pathlib import Path

from apps.api.app.eval.evaluate import evaluate, format_report, load_eval_set
from apps.api.app.retrieval.hybrid import hybrid_retrieve


eval_set = load_eval_set()

experiments = {
    "rrf_only": False,
    "rrf_reranked": True,
}

for name, use_reranker in experiments.items():

    retrieve_fn = partial(
        hybrid_retrieve,
        use_reranker=use_reranker,
    )

    results = evaluate(
        retrieve_fn=retrieve_fn,
        eval_set=eval_set,
        ks=(1, 5, 10),
    )

    print(format_report(results))

    output_path = Path(f"data/eval/results_{name}.json")
    output_path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(f"\nWrote {output_path}")