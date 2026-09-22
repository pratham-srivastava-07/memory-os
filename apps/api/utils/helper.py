from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from apps.api.app.memory.metadata import parse_markdown_document

logger = logging.getLogger(__name__)

CORPUS_DIR=Path("data/documents")

def extract_documents() -> list[Path]:
    return [path for path in CORPUS_DIR.rglob("*") if path.is_file()] 

def extract_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_corpus() -> list[dict[str, Any]]:
    # not a default arg - a mutable default is shared across calls and the
    # corpus would double every time this is called
    corpus = []
    for docs in extract_documents():
        raw_text= extract_text(docs)
        parsed = parse_markdown_document(raw_text, source=str(docs))
        cleaned_text = clean_text(raw_text)

        corpus.append({
            "path": str(docs),
            # Keep the existing embedding input stable. Temporal retrieval can
            # use the separately parsed body and metadata without silently
            # changing the semantic baseline.
            "text": cleaned_text,
            "body": clean_text(parsed.body),
            "metadata": parsed.metadata,
        })
        logger.debug("loaded %s (%d chars)", docs, len(cleaned_text))

    logger.info("loaded corpus: %d documents from %s", len(corpus), CORPUS_DIR)
    return corpus
