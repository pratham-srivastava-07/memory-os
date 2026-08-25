"""Deterministic stand-ins for the retrieval pipeline.

The eval harness takes `retrieve_fn` as an argument precisely so it can be
tested without a database or a model.
"""

from __future__ import annotations

from typing import Any, Callable


def oracle(eval_set: list[dict], filler: list[str]) -> Callable[..., list[dict[str, Any]]]:
    """Always returns the labelled documents first. Upper bound on any metric."""
    def _retrieve(query: str, k: int = 10) -> list[dict[str, Any]]:
        item = next(i for i in eval_set if i["query"] == query)
        relevant = item["relevant_documents"]
        rest = [n for n in filler if n not in relevant]
        return [{"path": n, "score": 1.0} for n in (relevant + rest)[:k]]
    return _retrieve


def constant(paths: list[str]) -> Callable[..., list[dict[str, Any]]]:
    """Returns the same documents for every query."""
    def _retrieve(query: str, k: int = 10) -> list[dict[str, Any]]:
        return [{"path": p, "score": 0.5} for p in paths[:k]]
    return _retrieve


def empty(query: str, k: int = 10) -> list[dict[str, Any]]:
    """Returns nothing. Lower bound."""
    return []
