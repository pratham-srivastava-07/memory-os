# Retrieval Evaluation Notes

## Current pipeline

The retrieval system works in stages:

```text
semantic retrieval + lexical retrieval
            ↓
      RRF rank fusion
            ↓
 optional CrossEncoder reranking
            ↓
       final top-k results
```

The first-stage retrievers return chunks. Evaluation labels identify source
documents, so duplicate chunks are collapsed by source before document-level
metrics are calculated.

## Reciprocal Rank Fusion

RRF combines ranked lists using rank positions rather than raw scores:

```text
RRF_score(document) = sum(1 / (rrf_constant + rank))
```

This is useful because semantic similarity scores and lexical relevance scores
usually have different scales. A document that appears near the top in more
than one retriever receives a stronger fused score.

RRF does not understand document meaning and does not directly combine vector
and lexical scores. It combines their rankings.

Reference: [Reciprocal Rank Fusion](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)

## CrossEncoder reranking

After first-stage retrieval, only a limited candidate set is passed to the
CrossEncoder. It scores each query-document pair together:

```python
pairs = [(query, candidate["content"]) for candidate in candidates]
scores = reranker.predict(pairs)
```

The candidates are sorted by these scores and the final top-k is returned.

The CrossEncoder is more expensive than a bi-encoder because it processes the
query and each candidate together. It can improve ordering, but it cannot
recover a relevant document that was absent from the candidate pool.

Reference: [Sentence Transformers: Retrieve and Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

## Candidate pool

`candidate_k` controls how many chunks each first-stage retriever returns. A
larger pool can improve recall, but gives the reranker more pairs to score and
therefore increases latency.

Current reranked results:

| candidate_k | Recall@5 | Recall@10 | Hit@10 | MRR |
|---:|---:|---:|---:|---:|
| 10 | 0.625 | 0.729 | 0.875 | 0.642 |
| 25 | 0.615 | 0.750 | 0.875 | 0.625 |
| 50 | 0.656 | 0.750 | 0.917 | 0.642 |
| 100 | 0.660 | 0.795 | 0.958 | 0.645 |

## Current latency measurements

These are warm end-to-end measurements for 240 requests per configuration.

| candidate_k | p50 (ms) | p95 (ms) | p99 (ms) |
|---:|---:|---:|---:|
| 10 | 470 | 1362 | 1752 |
| 25 | 680 | 958 | 1043 |
| 50 | 1380 | 1588 | 1760 |
| 100 | 2716 | 2997 | 3161 |

The current evidence suggests that `candidate_k=100` gives the best recall,
while `candidate_k=50` may offer a better quality/latency balance. Confirm this
with repeated, randomized latency runs before choosing a production value.

## Candidate recall versus final ranking

These are separate questions:

```text
candidate recall: did a relevant document enter the RRF candidate pool?
final ranking:    did it remain in the final top-k after reranking?
```

The CrossEncoder cannot fix low candidate recall. If relevant documents are
missing before reranking, improve the first-stage retrievers or increase the
candidate pool.

## Next experiments

1. Add an isolated RRF unit test with known ranked lists.
2. Add an isolated CrossEncoder test with an obviously relevant and irrelevant
   candidate.
3. Report candidate recall separately from final Recall@K.
4. Measure component latency for query encoding, dense search, lexical search,
   RRF, and reranking.
5. Run RRF-only and reranked latency experiments for candidate sizes 10, 25,
   50, and 100.
6. Choose a candidate size using both Recall@10 and p95 latency.
7. Only after correctness is stable, test query/candidate score caching.

The evaluation set currently contains 24 labelled queries, so results should be
described as an early internal baseline rather than a general benchmark.
