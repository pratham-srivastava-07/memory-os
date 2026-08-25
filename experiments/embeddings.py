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

new_arr = np.array(["Postgres", "PG"]) # wont work

print(embeddings.shape)
print("simmilarity of the text is below")
print(cosine_similarity(new_arr, sentences))

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
