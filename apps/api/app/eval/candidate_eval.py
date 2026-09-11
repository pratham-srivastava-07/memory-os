import json
from pathlib import Path
from functools import partial

from apps.api.app.eval.evaluate import evaluate, format_report, load_eval_set
from apps.api.app.retrieval.hybrid import hybrid_retrieve

eval_set = load_eval_set()

for candidate_k in (10, 25, 50, 100):
    retrieve_fn = partial(
        hybrid_retrieve,
        candidate_k=candidate_k,
        use_reranker=True,
    )

    results = evaluate(
        retrieve_fn=retrieve_fn,
        eval_set=eval_set,
        ks=(1,5,10)
    )

    print(format_report(results=results))

    output_path = Path(
        f"data/eval/results_candidate_{candidate_k}.json"
    )

    output_path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8"
    )