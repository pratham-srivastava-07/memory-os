---
doc_id: decision_004
type: decision
adr_id: ADR-004
title: "Vector index: pgvector HNSW in the primary Postgres cluster"
date: 2026-06-05
status: superseded
deciders: [Daniel Okoye, Mei Lin Zhao, Elliot Vance]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-260, MIG-101]
supersedes: []
superseded_by: [ADR-014, ADR-019]
tags: [vector-search, pgvector, database]
---

# ADR-004: Vector index — pgvector HNSW in the primary Postgres cluster

## Status

**Partially superseded by ADR-014 (2026-07-10), fully superseded by ADR-019
(2026-08-05).**

## Context

ADR-002 moved metadata to Postgres. The follow-on question is where the vectors live.
Daniel argued hard for keeping them in the same database: the whole reason the
hydration hop costs us 40–60 ms is that the vector index and the rows are in
different systems, and putting them back together is most of the win.

Our current scale: 14.6M chunk vectors across 84 tenants, largest tenant 3.1M.
Projected end of 2026: 60M.

## Decision

Store embeddings in `arca.chunks.embedding` as `vector(1024)` and build an HNSW index
with `m=16`, `ef_construction=200`, cosine distance. pgvector 0.7.

No separate vector database. One store, one backup, one set of credentials.

## Consequences

- Retrieval becomes a single SQL statement: vector search and metadata filter and
  hydration in one plan. Daniel prototyped this against 3M vectors and got 22 ms p95.
- Index build time is the risk. 3M vectors took 38 minutes to build with
  `maintenance_work_mem=8GB`. Nobody has tested 20M.
- Postgres becomes the single point of failure for retrieval as well as for writes.
- We are betting that pgvector recall holds at our projected scale. Mei flagged in
  review that she has not seen a credible public benchmark above 10M rows and wanted
  that written down. It is written down.

## Alternatives considered

- **Qdrant.** Better recall/latency curves in published benchmarks, real filtering
  support, but a second datastore two weeks after we decided to remove one. Elliot
  preferred it. Deferred, not rejected — see ARCA-329.
- **Pinecone.** Managed, no ops. Rejected on cost at 60M vectors and on the data
  residency conversation we would have to have with Lumen Health.
- **FAISS in-process.** No filtering, no updates without a rebuild. Rejected.
