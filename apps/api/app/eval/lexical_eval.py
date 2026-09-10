import json
from pathlib import Path

from apps.api.app.eval.evaluate import evaluate, format_report, load_eval_set
from apps.api.app.retrieval.lexical_search import sparse_retrieval

eval_set = load_eval_set()

results = evaluate(retrieve_fn=sparse_retrieval, eval_set=eval_set, ks=(1,5,10))

print(format_report(results=results))

output_path = Path("data/eval.results_lexical.json")

output_path.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print(f"\nWrote {output_path}")