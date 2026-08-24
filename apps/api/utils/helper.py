from pathlib import Path
import re

CORPUS_DIR=Path("data/documents")

def extract_documents():
    return [path for path in CORPUS_DIR.rglob("*") if path.is_file()] 

def extract_text(path):
    return path.read_text(encoding="utf-8")

def clean_text(text):
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_corpus():
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
    return corpus