from apps.api.utils.helper import load_corpus
from apps.api.app.retrieval.semantic_search import encode_corpus
from apps.api.app.repository import insert_chunk

def ingest():
    corpus = load_corpus()
    embeddings = encode_corpus(corpus)

    for doc, embedding in zip(corpus, embeddings):
        insert_chunk(content=doc["text"], source=doc["path"], embeddings=embedding)