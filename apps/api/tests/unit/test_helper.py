"""Unit tests for corpus loading. No database, no model."""

from __future__ import annotations

from pathlib import Path

import pytest

from apps.api.utils.helper import (
    CORPUS_DIR,
    clean_text,
    extract_documents,
    extract_text,
    load_corpus,
)


class TestCleanText:
    def test_strips_null_bytes(self) -> None:
        assert "\x00" not in clean_text("a\x00b")

    def test_collapses_whitespace_runs(self) -> None:
        assert clean_text("a   \n\n  b") == "a b"

    def test_strips_leading_and_trailing(self) -> None:
        assert clean_text("  hello  ") == "hello"

    def test_empty_string(self) -> None:
        assert clean_text("") == ""

    def test_whitespace_only_becomes_empty(self) -> None:
        assert clean_text("  \n\t ") == ""


class TestExtractDocuments:
    def test_returns_paths(self) -> None:
        docs = extract_documents()
        assert docs, "corpus directory is empty"
        assert all(isinstance(p, Path) for p in docs)

    def test_returns_files_only(self) -> None:
        assert all(p.is_file() for p in extract_documents())

    def test_all_inside_corpus_dir(self) -> None:
        root = CORPUS_DIR.resolve()
        assert all(root in p.resolve().parents for p in extract_documents())


class TestExtractText:
    def test_reads_a_known_file(self) -> None:
        path = CORPUS_DIR / "decisions" / "decision_002.md"
        if not path.exists():
            pytest.skip(f"{path} not present")
        text = extract_text(path)
        assert "PostgreSQL" in text

    def test_handles_unicode(self) -> None:
        """The corpus contains em dashes; cp1252 would raise on read."""
        for path in extract_documents()[:10]:
            extract_text(path)


class TestLoadCorpus:
    def test_returns_path_and_text_keys(self) -> None:
        corpus = load_corpus()
        assert corpus
        assert set(corpus[0]) == {"path", "text"}

    def test_one_entry_per_file(self) -> None:
        assert len(load_corpus()) == len(extract_documents())

    def test_no_empty_documents(self) -> None:
        assert all(entry["text"] for entry in load_corpus())

    def test_repeated_calls_do_not_accumulate(self) -> None:
        """Regression: a mutable default argument made the corpus grow."""
        assert len(load_corpus()) == len(load_corpus())

    def test_paths_are_unique(self) -> None:
        paths = [entry["path"] for entry in load_corpus()]
        assert len(paths) == len(set(paths))
