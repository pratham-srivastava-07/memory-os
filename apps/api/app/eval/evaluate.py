"""Retrieval evaluation harness.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable, Sequence

EVAL_PATH = Path("data/eval/retrieval.json")
DEFAULT_KS: tuple[int, ...] = (1, 5, 10)


def load_eval_set(path: Path = EVAL_PATH) -> list[dict]:
    
    with open(path, encoding="utf-8") as f:
        eval_set = json.load(f)

    for i, item in enumerate(eval_set):
        if "query" not in item or "relevant_documents" not in item:
            raise ValueError(f"eval item {i} is missing 'query' or 'relevant_documents'")
        if not item["relevant_documents"]:
            raise ValueError(f"eval item {item.get('id', i)} has no relevant documents")

    return eval_set


def doc_id(path: str) -> str:
    return Path(path).name


def check_eval_set(
    eval_set: Iterable[dict], corpus_dir: Path = Path("data/documents")
) -> list[str]:
    """Return labels that point at documents which do not exist on disk.

    A silently mislabelled eval set reports low recall that looks like a
    retrieval bug, so this runs before every evaluation.
    """
    known = {p.name for p in corpus_dir.rglob("*.md")}
    dangling = []
    for item in eval_set:
        for name in item["relevant_documents"]:
            if name not in known:
                dangling.append(f"{item.get('id', item['query'][:30])} -> {name}")
    return dangling



def recall_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    """Fraction of the relevant documents that appear in the top ``k``.

    Note this is bounded by ``k / len(relevant)``: a query with 3 relevant
    documents can score at most 0.33 on Recall@1. That is intended — it is why
    ``hit@k`` is reported alongside it.
    """
    hits = len(relevant & set(retrieved[:k]))
    return hits / len(relevant)


def hit_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    """1.0 if at least one relevant document is in the top ``k``, else 0.0."""
    return 1.0 if relevant & set(retrieved[:k]) else 0.0


def reciprocal_rank(retrieved: Sequence[str], relevant: set[str]) -> float:
    """1 / rank of the first relevant document, or 0.0 if none was retrieved."""
    for i, name in enumerate(retrieved, start=1):
        if name in relevant:
            return 1.0 / i
    return 0.0


def _default_retrieve() -> Callable[..., list[dict]]:
    """Import the real pipeline lazily so importing this module stays cheap.

    ``semantic_search`` embeds the whole corpus at import time.
    """
    from apps.api.app.retrieval.semantic_search import retrieve

    return retrieve


def evaluate(
    retrieve_fn: Callable[..., list[dict]] | None = None,
    eval_set: list[dict] | None = None,
    ks: Sequence[int] = DEFAULT_KS,
) -> dict:
    """Run every eval query through ``retrieve_fn`` and score the results.

    Args:
        retrieve_fn: callable ``(query, k) -> [{"path": ..., "score": ...}, ...]``,
            ranked best first. Defaults to the semantic search pipeline.
        eval_set: labelled queries. Defaults to ``data/eval/retrieval.json``.
        ks: cutoffs to report.

    Returns:
        A dict with ``overall`` metrics, ``per_query`` detail and a ``per_tag``
        breakdown.
    """
    if eval_set is None:
        eval_set = load_eval_set()
    if retrieve_fn is None:
        retrieve_fn = _default_retrieve()

    dangling = check_eval_set(eval_set)
    if dangling:
        raise ValueError(
            "eval set references documents that do not exist:\n  "
            + "\n  ".join(dangling)
        )

    ks = tuple(sorted(ks))
    max_k = max(ks)

    per_query: list[dict] = []
    for item in eval_set:
        relevant = set(item["relevant_documents"])
        results = retrieve_fn(item["query"], k=max_k)
        retrieved = [doc_id(r["path"]) for r in results]

        row = {
            "id": item.get("id"),
            "query": item["query"],
            "tags": item.get("tags", []),
            "n_relevant": len(relevant),
            "retrieved": retrieved,
            "missed": sorted(relevant - set(retrieved[:max_k])),
            "mrr": reciprocal_rank(retrieved, relevant),
        }
        for k in ks:
            row[f"recall@{k}"] = recall_at_k(retrieved, relevant, k)
            row[f"hit@{k}"] = hit_at_k(retrieved, relevant, k)
            # best possible score for this query: you cannot fit 3 relevant
            # documents into a top-1 list
            row[f"ceiling@{k}"] = min(k, len(relevant)) / len(relevant)
        per_query.append(row)

    metric_names = (
        [f"recall@{k}" for k in ks]
        + [f"hit@{k}" for k in ks]
        + [f"ceiling@{k}" for k in ks]
        + ["mrr"]
    )

    def _mean(rows: list[dict], name: str) -> float:
        return sum(r[name] for r in rows) / len(rows) if rows else 0.0

    overall = {name: _mean(per_query, name) for name in metric_names}

    by_tag: dict[str, list[dict]] = defaultdict(list)
    for row in per_query:
        for tag in row["tags"]:
            by_tag[tag].append(row)
    per_tag = {
        tag: {"n": len(rows), **{name: _mean(rows, name) for name in metric_names}}
        for tag, rows in sorted(by_tag.items())
    }

    return {
        "n_queries": len(per_query),
        "ks": list(ks),
        "overall": overall,
        "per_query": per_query,
        "per_tag": per_tag,
    }



def format_report(results: dict, show_failures: int = 10) -> str:
    """Render results as a plain-text report."""
    ks = results["ks"]
    overall = results["overall"]
    lines: list[str] = []

    lines.append(f"Retrieval evaluation — {results['n_queries']} queries")
    lines.append("=" * 62)
    lines.append("")
    for k in ks:
        ceiling = overall[f"ceiling@{k}"]
        recall = overall[f"recall@{k}"]
        pct = f"{recall / ceiling:.0%}" if ceiling else "n/a"
        lines.append(
            f"  Recall@{k:<3} {recall:.3f}   (ceiling {ceiling:.3f}, {pct:>4} of achievable)"
            f"   Hit@{k:<3} {overall[f'hit@{k}']:.3f}"
        )
    lines.append(f"  MRR        {overall['mrr']:.3f}")
    lines.append("")
    lines.append("  Recall@k = share of relevant docs found")
    lines.append("  ceiling  = best possible Recall@k, since a top-k list cannot")
    lines.append("             hold more than k of the n relevant documents")
    lines.append("  Hit@k    = share of queries with >=1 relevant doc in top k")
    lines.append("")

    lines.append("By tag")
    lines.append("-" * 62)
    header = f"  {'tag':<24} {'n':>3}" + "".join(f"  {'R@'+str(k):>6}" for k in ks)
    lines.append(header)
    for tag, m in sorted(results["per_tag"].items(), key=lambda kv: kv[1][f"recall@{ks[0]}"]):
        row = f"  {tag:<24} {m['n']:>3}" + "".join(f"  {m[f'recall@{k}']:>6.3f}" for k in ks)
        lines.append(row)
    lines.append("")

    worst = sorted(results["per_query"], key=lambda r: (r[f"recall@{ks[-1]}"], r["mrr"]))
    failures = [r for r in worst if r[f"recall@{ks[-1]}"] < 1.0][:show_failures]
    if failures:
        lines.append(f"Weakest queries (by Recall@{ks[-1]})")
        lines.append("-" * 62)
        for r in failures:
            lines.append(f"  [{r['id']}] {r['query']}")
            lines.append(
                f"        recall@{ks[-1]}={r[f'recall@{ks[-1]}']:.2f}"
                f"  mrr={r['mrr']:.2f}  missed={r['missed']}"
            )
            lines.append(f"        top3={r['retrieved'][:3]}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the retrieval pipeline.")
    parser.add_argument("--k", type=int, nargs="+", default=list(DEFAULT_KS))
    parser.add_argument("--eval-path", type=Path, default=EVAL_PATH)
    parser.add_argument("--json", type=Path, help="write full results to this path")
    parser.add_argument("--show-failures", type=int, default=10)
    args = parser.parse_args()

    results = evaluate(eval_set=load_eval_set(args.eval_path), ks=args.k)
    print(format_report(results, show_failures=args.show_failures))

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
