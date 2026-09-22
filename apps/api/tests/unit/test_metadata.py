"""Tests for MemoryOS document metadata and supersedence relations."""

from __future__ import annotations

import pytest

from apps.api.app.memory.metadata import (
    SupersedenceEdge,
    build_supersedence_graph,
    parse_markdown_document,
)
from apps.api.utils.helper import load_corpus


def test_parse_markdown_document_normalizes_yaml_date() -> None:
    parsed = parse_markdown_document(
        """---
doc_id: decision_001
date: 2026-05-08
status: accepted
---
# Decision
PostgreSQL was selected.
"""
    )

    assert parsed.metadata["date"] == "2026-05-08"
    assert parsed.body.startswith("# Decision")


def test_parse_markdown_document_requires_front_matter() -> None:
    with pytest.raises(ValueError, match="opening YAML"):
        parse_markdown_document("# Document without metadata")


def test_supersedence_graph_resolves_adr_aliases() -> None:
    documents = [
        {
            "metadata": {
                "doc_id": "decision_old",
                "adr_id": "ADR-001",
                "superseded_by": ["ADR-002"],
            }
        },
        {
            "metadata": {
                "doc_id": "decision_new",
                "adr_id": "ADR-002",
                "supersedes": ["ADR-001"],
            }
        },
    ]

    edges, unresolved = build_supersedence_graph(documents)

    assert edges == [SupersedenceEdge("decision_new", "decision_old")]
    assert unresolved == []


def test_real_corpus_has_resolvable_supersedence_references() -> None:
    edges, unresolved = build_supersedence_graph(load_corpus())

    assert edges
    assert unresolved == []
