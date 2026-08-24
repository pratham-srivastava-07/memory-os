from sentence_transformers import SentenceTransformer
import torch
from pathlib import Path
import re

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


# embedder for embedding corpus text
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# actually creating the corpus embeddings 
corpus_embeddings = embedder.encode_document(corpus, conver_to_tensor=True)



