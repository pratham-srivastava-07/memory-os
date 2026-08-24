---
doc_id: note_009
type: note
subtype: spike
title: "pgvector spike — it is fast"
author: Daniel Okoye
date: 2026-06-02
status: stale
projects: [Arca]
tickets: [ARCA-260, ARCA-329]
tags: [pgvector, spike, stale, optimistic]
---

# pgvector spike — it is fast

Two days of playing with pgvector 0.7 on a copy of three tenants. Writing it up
before Thursday's review.

## Setup

3.1M vectors, 1024 dimensions, HNSW `m=16` `ef_construction=200`, cosine. Same shape
as our largest tenant. 16 vCPU, 64 GB.

## The headline

**22 ms p95** for top-200 vector search with a `tenant_id` filter, hydration
included, in a single SQL statement.

```sql
SELECT c.chunk_id, c.document_id, c.text, d.source_uri,
       c.embedding <=> $1 AS distance
FROM arca.chunks c
JOIN arca.documents d USING (document_id)
WHERE c.tenant_id = $2
ORDER BY c.embedding <=> $1
LIMIT 200;
```

One statement. One round trip. The filter, the search, the join and the hydration all
in one plan. Compare with today: vector index round trip, then a Mongo round trip for
200 documents, 41 ms of which is the second hop.

## Recall

Measured against exact search on the same 3.1M vectors, 500 queries: **recall@10 of
0.97** at default `ef_search`. That is fine. That is better than fine.

## Index build

38 minutes at 3.1M with `maintenance_work_mem=8GB`. Acceptable. It is a one-time cost
and we have replicas.

## Write cost

Insert throughput with the index live drops. Mei measured 4,300/sec against 11,000
without. That is 1.9x over our peak, which is thinner than I would like, but it is
headroom.

## What I did not test

Anything above 3.1M. Our largest tenant is 3.1M today. I extrapolated linearly from
1M → 3.1M and the curve looked flat.

## Conclusion

pgvector is the right call. One database, one backup, one plan, 22 ms. The scale
concern is theoretical and we can move to a dedicated vector store later if it
becomes real — the adapter interface makes that a bounded piece of work.

---

> **[Annotation added by Mei, 2026-07-07]** The extrapolation in "what I did not test"
> is the whole problem. HNSW recall does not degrade linearly, it falls off a cliff
> once the graph gets deep relative to `ef_search`. At 8M we measured 0.88, not 0.97.
> Daniel's numbers here are all correct *at 3.1M* and this document should not be
> cited for anything above that. See my 2026-07-06 benchmark.
