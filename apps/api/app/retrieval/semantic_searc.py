from sentence_transformers import SentenceTransformer
import torch
from pathlib import Path
import re
import json

CORPUS_DIR=Path("data/documents")

corpus = []

def extract_documents():
    return [path for path in CORPUS_DIR.rglob("*")]

def extract_text(path):
    return path.read_text(encoding="utf-8")

def clean_text(text):
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

for docs in extract_documents():
    raw_text= extract_text(docs)
    cleaned_text = clean_text(raw_text)

    corpus.append(cleaned_text)

def encode_query(query):
    return embedder.encode_query(query, convert_to_tensor=True)


# embedder for embedding corpus text
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# actually creating the corpus embeddings 
corpus_embeddings = embedder.encode_document(corpus, conver_to_tensor=True)

with open("data/eval/retrieval.json") as f:
    clean_query = json.loads(f)

    for item in clean_query:
        query_embedding = encode_query(item)


tp_k = min(5, len(corpus))

similarity_score = embedder.similarity(query_embedding, corpus_embeddings)[0]
scores, indices = torch.topk(similarity_score, k=tp_k)

print("\nQuery:", clean_query)
print("Top 5 most similar sentences in corpus:")

for score, idx in zip(scores, indices):
    print(f"(Score: {score:.4f})", corpus[idx])