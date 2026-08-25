from __future__ import annotations

import logging
import re
from pathlib import Path

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


def load_corpus() -> list[dict[str, str]]:
    # not a default arg - a mutable default is shared across calls and the
    # corpus would double every time this is called
    corpus = []
    for docs in extract_documents():
        raw_text= extract_text(docs)
        cleaned_text = clean_text(raw_text)

        corpus.append({
            "path": str(docs),
            "text": cleaned_text
        })
        logger.debug("loaded %s (%d chars)", docs, len(cleaned_text))

    logger.info("loaded corpus: %d documents from %s", len(corpus), CORPUS_DIR)
    return corpus