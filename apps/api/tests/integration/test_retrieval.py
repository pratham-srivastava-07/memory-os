"""Integration tests for the retrieval entry points.

These load the sentence-transformers model, so they are marked `slow`.
"""

from __future__ import annotations

import pytest

from apps.api.tests.conftest import requires_db

pytestmark = [pytest.mark.db, pytest.mark.slow, requires_db]


class TestSemanticRetrieve:
    def test_returns_at_most_k(self) -> None:
        from apps.api.app.retrieval.semantic_search import retrieve
        assert len(retrieve("postgres migration", k=3)) <= 3

    def test_result_rows_carry_a_source(self) -> None:
        from apps.api.app.retrieval.semantic_search import retrieve
        rows = retrieve("what did the team decide about the database", k=5)
        if not rows:
            pytest.skip("chunks table is empty")
        assert all(r["source"] for r in rows)


class TestSparseRetrieval:
    def test_returns_at_most_k(self) -> None:
        from apps.api.app.retrieval.lexical_search import sparse_retrieval
        assert len(sparse_retrieval("migration", k=3)) <= 3

    def test_passes_k_through_to_the_repository(self) -> None:
        from apps.api.app.retrieval.lexical_search import sparse_retrieval
        assert len(sparse_retrieval("the", k=1)) <= 1


class TestHybridRetrieve:
    """Documents current behaviour. Fusion is not implemented yet."""

    def test_returns_a_list(self) -> None:
        from apps.api.app.retrieval.hybrid import hybrid_retrieve
        assert isinstance(hybrid_retrieve("postgres", k=5), list)

    @pytest.mark.xfail(
        reason="hybrid_retrieve builds candidates then returns an empty "
               "final_result; RRF fusion is the unfinished half",
        strict=True,
    )
    def test_returns_results(self) -> None:
        from apps.api.app.retrieval.hybrid import hybrid_retrieve
        assert hybrid_retrieve("postgres migration", k=5)

    @pytest.mark.xfail(
        reason="k is accepted but both sub-searches are hardcoded to 10",
        strict=True,
    )
    def test_respects_k(self) -> None:
        from apps.api.app.retrieval.hybrid import hybrid_retrieve
        assert len(hybrid_retrieve("postgres", k=3)) == 3
