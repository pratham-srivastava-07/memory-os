import json
from functools import partial
from pathlib import Path

from apps.api.app.eval.evaluate import evaluate, load_eval_set, format_report
from apps.api.app.retrieval.hybrid import hybrid_retrieve

eval_set = load_eval_set()

results = evaluate(
    retrieve_fn=partial(hybrid_retrieve, use_reranker=True),
    eval_set=eval_set,
    ks=(1,5,10)
)

print(format_report(results=results))

output_path = Path("data/eval/results_hybrid.json")

output_path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

print(f"\nWrote {output_path}")
