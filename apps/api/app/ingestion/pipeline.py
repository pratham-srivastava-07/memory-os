from apps.api.utils.helper import load_corpus
from apps.api.app.repository import insert_chunk
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)


def ingest():
    corpus = load_corpus()

    for doc in corpus:
        chunks = splitter.split_text(doc["text"])

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


if __name__ == "__main__":
    ingest()