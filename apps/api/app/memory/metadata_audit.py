"""Audit the corpus metadata that will power temporal retrieval."""

from __future__ import annotations

from collections import Counter

from apps.api.app.memory.metadata import build_supersedence_graph, document_date
from apps.api.utils.helper import load_corpus


def main() -> None:
    corpus = load_corpus()
    edges, unresolved = build_supersedence_graph(corpus)

    statuses = Counter(
        str(document["metadata"].get("status", "unspecified"))
        for document in corpus
    )
    dated = sum(document_date(document["metadata"]) is not None for document in corpus)

    print("MemoryOS metadata audit")
    print("=" * 58)
    print(f"documents parsed        {len(corpus):>6}")
    print(f"documents with a date   {dated:>6}")
    print(f"supersedence relations  {len(edges):>6}")
    print(f"unresolved references   {len(unresolved):>6}")
    print("\nDocument status")
    print("-" * 58)
    for status, count in sorted(statuses.items()):
        print(f"{status:<32} {count:>6}")

    if unresolved:
        print("\nUnresolved supersedence references")
        print("-" * 58)
        for reference in unresolved:
            print(reference)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

