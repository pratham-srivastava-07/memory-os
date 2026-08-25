from __future__ import annotations

import logging

from apps.api.utils.helper import load_corpus
from apps.api.app.repository import insert_chunk
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)


def ingest() -> None:
    corpus = load_corpus()
    total = 0

    for doc in corpus:
        chunks = splitter.split_text(doc["text"])
        logger.debug("ingest: %s -> %d chunk(s)", doc["path"], len(chunks))

        embeddings = embedder.encode_document(
            chunks,
            convert_to_tensor=True
        )

        for chunk, embedding in zip(chunks, embeddings):
            insert_chunk(
                content=chunk,
                source=doc["path"],
                embeddings=embedding
            )
            total += 1

    logger.info("ingest: wrote %d chunk(s) from %d document(s)", total, len(corpus))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    ingest()