"""Integration tests for the repository layer.

Require a running PostgreSQL with pgvector and a populated `chunks` table.
Skipped automatically when the database is unreachable.
"""

from __future__ import annotations

import pytest

from apps.api.app.repository import lexical_search, search_vectors
from apps.api.tests.conftest import requires_db

pytestmark = [pytest.mark.db, requires_db]

EXPECTED_KEYS = {"id", "content", "source", "score"}


class TestSearchVectors:
    def test_returns_at_most_k_rows(self, sample_embedding) -> None:
        assert len(search_vectors(sample_embedding, k=3)) <= 3

    def test_row_shape(self, sample_embedding) -> None:
        rows = search_vectors(sample_embedding, k=1)
        if not rows:
            pytest.skip("chunks table is empty")
        assert set(rows[0]) == EXPECTED_KEYS

    def test_accepts_a_plain_list(self, sample_embedding) -> None:
        search_vectors(sample_embedding, k=1)

    def test_accepts_a_torch_tensor(self, sample_embedding) -> None:
        """search_vectors calls .tolist() on anything that offers it."""
        torch = pytest.importorskip("torch")
        search_vectors(torch.tensor(sample_embedding), k=1)

    def test_scores_are_floats(self, sample_embedding) -> None:
        rows = search_vectors(sample_embedding, k=5)
        if not rows:
            pytest.skip("chunks table is empty")
        assert all(isinstance(r["score"], float) for r in rows)

    def test_results_are_ordered_by_descending_score(self, sample_embedding) -> None:
        """Ordering is the entire product. If it regresses, nothing else matters."""
        scores = [r["score"] for r in search_vectors(sample_embedding, k=10)]
        if len(scores) < 2:
            pytest.skip("not enough rows to check ordering")
        assert scores == sorted(scores, reverse=True)

    def test_k_of_zero_returns_nothing(self, sample_embedding) -> None:
        assert search_vectors(sample_embedding, k=0) == []


class TestLexicalSearch:
    def test_returns_at_most_k_rows(self) -> None:
        assert len(lexical_search("migration", k=3)) <= 3

    def test_row_shape(self) -> None:
        rows = lexical_search("postgres", k=1)
        if not rows:
            pytest.skip("no lexical match in the corpus")
        assert set(rows[0]) == EXPECTED_KEYS

    def test_ordered_by_descending_score(self) -> None:
        scores = [r["score"] for r in lexical_search("postgres migration", k=10)]
        if len(scores) < 2:
            pytest.skip("not enough matches to check ordering")
        assert scores == sorted(scores, reverse=True)

    def test_nonsense_term_returns_empty(self) -> None:
        assert lexical_search("zzzzqqqxxnotaword", k=5) == []

    def test_matches_are_relevant_to_the_term(self) -> None:
        rows = lexical_search("pgvector", k=5)
        if not rows:
            pytest.skip("no lexical match in the corpus")
        assert any("pgvector" in r["content"].lower() for r in rows)

    def test_empty_query_does_not_raise(self) -> None:
        """websearch_to_tsquery('') is valid and matches nothing."""
        assert lexical_search("", k=5) == []
