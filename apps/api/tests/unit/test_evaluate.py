"""Unit tests for the retrieval evaluation harness.

These are the tests that let you trust a recall number. If the metrics are
wrong, every measurement taken with them is wrong in a way nothing else
will reveal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.api.app.eval.evaluate import (
    check_eval_set,
    doc_id,
    evaluate,
    hit_at_k,
    load_eval_set,
    recall_at_k,
    reciprocal_rank,
)
from apps.api.tests.fixtures import fake_retrievers


class TestDocId:
    def test_posix_path(self) -> None:
        assert doc_id("data/documents/meetings/meeting_001.md") == "meeting_001.md"

    def test_windows_path(self) -> None:
        assert doc_id(r"data\documents\meetings\meeting_001.md") == "meeting_001.md"

    def test_bare_filename_unchanged(self) -> None:
        assert doc_id("meeting_001.md") == "meeting_001.md"


class TestRecallAtK:
    def test_all_relevant_in_window(self) -> None:
        assert recall_at_k(["a", "b", "c"], {"a", "b"}, 3) == 1.0

    def test_none_retrieved(self) -> None:
        assert recall_at_k(["x", "y"], {"a"}, 2) == 0.0

    def test_partial(self) -> None:
        assert recall_at_k(["a", "x"], {"a", "b"}, 2) == 0.5

    def test_k_smaller_than_relevant_set_caps_the_score(self) -> None:
        """Three relevant documents cannot fit in a top-1 list."""
        assert recall_at_k(["a", "b", "c"], {"a", "b", "c"}, 1) == pytest.approx(1 / 3)

    def test_ignores_results_past_k(self) -> None:
        assert recall_at_k(["x", "a"], {"a"}, 1) == 0.0

    def test_duplicate_results_do_not_inflate(self) -> None:
        assert recall_at_k(["a", "a"], {"a", "b"}, 2) == 0.5


class TestHitAtK:
    def test_hit(self) -> None:
        assert hit_at_k(["x", "a"], {"a"}, 2) == 1.0

    def test_miss(self) -> None:
        assert hit_at_k(["x", "y"], {"a"}, 2) == 0.0

    def test_respects_the_cutoff(self) -> None:
        assert hit_at_k(["x", "a"], {"a"}, 1) == 0.0

    def test_is_binary_regardless_of_how_many_match(self) -> None:
        assert hit_at_k(["a", "b"], {"a", "b"}, 2) == 1.0


class TestReciprocalRank:
    def test_first_position(self) -> None:
        assert reciprocal_rank(["a", "b"], {"a"}) == 1.0

    def test_third_position(self) -> None:
        assert reciprocal_rank(["x", "y", "a"], {"a"}) == pytest.approx(1 / 3)

    def test_absent(self) -> None:
        assert reciprocal_rank(["x", "y"], {"a"}) == 0.0

    def test_uses_the_earliest_match(self) -> None:
        assert reciprocal_rank(["b", "a"], {"a", "b"}) == 1.0


class TestLoadEvalSet:
    def test_loads_the_real_file(self) -> None:
        eval_set = load_eval_set()
        assert eval_set
        assert all("query" in item for item in eval_set)

    def test_rejects_missing_keys(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps([{"query": "no labels here"}]), encoding="utf-8")
        with pytest.raises(ValueError, match="relevant_documents"):
            load_eval_set(bad)

    def test_rejects_empty_label_list(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text(
            json.dumps([{"id": "q1", "query": "q", "relevant_documents": []}]),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="no relevant documents"):
            load_eval_set(bad)


class TestCheckEvalSet:
    def test_real_eval_set_has_no_dangling_labels(self) -> None:
        """Every labelled document must exist, or recall is understated."""
        assert check_eval_set(load_eval_set()) == []

    def test_detects_a_missing_document(self) -> None:
        fake = [{"id": "q1", "query": "q", "relevant_documents": ["nope.md"]}]
        assert check_eval_set(fake)


class TestEvaluate:
    @pytest.fixture
    def eval_set(self) -> list[dict]:
        return [
            {"id": "q1", "query": "first", "relevant_documents": ["a.md"],
             "tags": ["alpha"]},
            {"id": "q2", "query": "second", "relevant_documents": ["b.md", "c.md"],
             "tags": ["beta"]},
        ]

    @pytest.fixture
    def corpus_names(self) -> list[str]:
        return ["a.md", "b.md", "c.md", "d.md", "e.md"]

    @pytest.fixture(autouse=True)
    def _skip_existence_check(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The synthetic labels above are not real files."""
        monkeypatch.setattr(
            "apps.api.app.eval.evaluate.check_eval_set", lambda *a, **kw: []
        )

    def test_oracle_scores_perfectly_at_k5(self, eval_set, corpus_names) -> None:
        results = evaluate(
            retrieve_fn=fake_retrievers.oracle(eval_set, corpus_names),
            eval_set=eval_set,
        )
        assert results["overall"]["recall@5"] == pytest.approx(1.0)
        assert results["overall"]["mrr"] == pytest.approx(1.0)

    def test_oracle_recall_at_1_is_bounded_by_label_count(
        self, eval_set, corpus_names
    ) -> None:
        """q1 has 1 label (scores 1.0), q2 has 2 (scores 0.5). Mean 0.75."""
        results = evaluate(
            retrieve_fn=fake_retrievers.oracle(eval_set, corpus_names),
            eval_set=eval_set,
        )
        assert results["overall"]["recall@1"] == pytest.approx(0.75)

    def test_empty_retriever_scores_zero(self, eval_set) -> None:
        results = evaluate(retrieve_fn=fake_retrievers.empty, eval_set=eval_set)
        assert results["overall"]["recall@10"] == 0.0
        assert results["overall"]["hit@1"] == 0.0

    def test_reports_every_query(self, eval_set, corpus_names) -> None:
        results = evaluate(
            retrieve_fn=fake_retrievers.constant(corpus_names), eval_set=eval_set
        )
        assert results["n_queries"] == len(eval_set)
        assert len(results["per_query"]) == len(eval_set)

    def test_per_query_records_what_was_missed(self, eval_set) -> None:
        results = evaluate(retrieve_fn=fake_retrievers.empty, eval_set=eval_set)
        by_id = {row["id"]: row for row in results["per_query"]}
        assert by_id["q2"]["missed"] == ["b.md", "c.md"]

    def test_tag_breakdown_partitions_the_queries(self, eval_set, corpus_names) -> None:
        results = evaluate(
            retrieve_fn=fake_retrievers.oracle(eval_set, corpus_names),
            eval_set=eval_set,
        )
        assert set(results["per_tag"]) == {"alpha", "beta"}
        assert results["per_tag"]["alpha"]["n"] == 1

    def test_custom_k_values_are_reported(self, eval_set, corpus_names) -> None:
        results = evaluate(
            retrieve_fn=fake_retrievers.constant(corpus_names),
            eval_set=eval_set,
            ks=(2, 4),
        )
        assert results["ks"] == [2, 4]
        assert "recall@2" in results["overall"]
        assert "recall@4" in results["overall"]
