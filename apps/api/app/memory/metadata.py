"""Structured document metadata used by MemoryOS resolution stages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import yaml


@dataclass(frozen=True)
class ParsedDocument:
    """A Markdown document split into front matter and readable body."""

    metadata: dict[str, Any]
    body: str


@dataclass(frozen=True, order=True)
class SupersedenceEdge:
    """A directed relation where one document supersedes another."""

    superseding_id: str
    superseded_id: str


def _json_safe(value: Any) -> Any:
    """Normalize YAML values so metadata can later be stored as JSONB."""

    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def parse_markdown_document(raw_text: str, *, source: str = "<document>") -> ParsedDocument:
    """Parse required YAML front matter without changing the Markdown body."""

    lines = raw_text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{source} is missing opening YAML front matter delimiter")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValueError(f"{source} is missing closing YAML front matter delimiter") from exc

    raw_metadata = "\n".join(lines[1:closing_index])
    loaded = yaml.safe_load(raw_metadata)
    if not isinstance(loaded, dict):
        raise ValueError(f"{source} front matter must be a YAML mapping")

    metadata = _json_safe(loaded)
    if not metadata.get("doc_id"):
        raise ValueError(f"{source} front matter must contain doc_id")

    body = "\n".join(lines[closing_index + 1:]).strip()
    if not body:
        raise ValueError(f"{source} has an empty Markdown body")

    return ParsedDocument(metadata=metadata, body=body)


def build_supersedence_graph(
    documents: Iterable[dict[str, Any]],
) -> tuple[list[SupersedenceEdge], list[str]]:
    """Build canonical supersedence edges and report unresolved references.

    References in the corpus use ADR identifiers while retrieval uses document
    identifiers. Both are resolved to the canonical ``doc_id`` here.
    """

    documents = list(documents)
    aliases: dict[str, str] = {}
    for document in documents:
        metadata = document["metadata"]
        doc_id = str(metadata["doc_id"])
        for alias in (doc_id, metadata.get("adr_id")):
            if alias:
                aliases[str(alias)] = doc_id

    edges: set[SupersedenceEdge] = set()
    unresolved: set[str] = set()

    def resolve(reference: Any, owner: str, field: str) -> str | None:
        resolved = aliases.get(str(reference))
        if resolved is None:
            unresolved.add(f"{owner}.{field} -> {reference}")
        return resolved

    for document in documents:
        metadata = document["metadata"]
        doc_id = str(metadata["doc_id"])

        for reference in metadata.get("supersedes", []) or []:
            target = resolve(reference, doc_id, "supersedes")
            if target:
                edges.add(SupersedenceEdge(doc_id, target))

        for reference in metadata.get("superseded_by", []) or []:
            replacement = resolve(reference, doc_id, "superseded_by")
            if replacement:
                edges.add(SupersedenceEdge(replacement, doc_id))

    return sorted(edges), sorted(unresolved)


def document_date(metadata: dict[str, Any]) -> str | None:
    """Return the best available effective date from heterogeneous metadata."""

    value = metadata.get("date") or metadata.get("last_updated") or metadata.get("created")
    return str(value) if value else None

