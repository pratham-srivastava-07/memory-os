from sentence_transformers import SentenceTransformer
import torch
from apps.api.utils.helper import load_corpus
from apps.api.app.repository import search_vectors

corpus = load_corpus()

corpus_text = [doc["text"] for doc in corpus]

# embedder for embedding corpus text
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def encode_query(query):
    return embedder.encode_query(query, convert_to_tensor=True)


def encode_corpus(corpus_text):
    # actually creating the corpus embeddings 
    corpus_embeddings = embedder.encode_document(corpus_text, convert_to_tensor=True)
    return corpus_embeddings

corpus_embeddings = encode_corpus(corpus_text)


# retrieval pipeline wiring
def retrieve(query: str, k: int = 5):
    query_embedding = encode_query(query)

    # retrieve data from postgres, with searching from query embeddings and k

    return search_vectors(query_embedding, k)


    # similarity_scores = embedder.similarity(query_embedding, corpus_embeddings)[0]

    # k = min(k, len(corpus))

    # scores, indices = torch.topk(similarity_scores, k=k)

    # results = []

    # for score, idx in zip(scores, indices):
    #     results.append({
    #         "score": float(score),
    #         "path": corpus[idx]["path"],
    #         "text": corpus[idx]["text"]
    #     })

    # return results

# evaluation lives in apps/api/app/eval/evaluate.py:
#     python -m apps.api.app.eval.evaluate
