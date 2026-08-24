from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-V2")

sentences = [
     "I use PostgreSQL for my backend.",
    "My backend database is Postgres.",
    "I built an API using FastAPI.",
    "I watched a movie yesterday."
]

embeddings = model.encode(sentences)

new_arr = np.array(["Postgres", "PG"])

print(embeddings.shape)
print("simmilarity of the text is below")
print(cosine_similarity(new_arr, sentences))