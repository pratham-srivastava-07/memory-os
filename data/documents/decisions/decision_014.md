---
doc_id: decision_014
type: decision
adr_id: ADR-014
title: "Adopt Qdrant for tenants above 2M vectors"
date: 2026-07-10
status: superseded
deciders: [Mei Lin Zhao, Elliot Vance, Daniel Okoye, Tomas Herrera]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-329, INFRA-88]
supersedes: [ADR-004]
superseded_by: [ADR-019]
tags: [vector-search, qdrant, pgvector, scale]
---

# ADR-014: Adopt Qdrant for tenants above 2M vectors

## Status

**Superseded by ADR-019 (2026-08-05),** which consolidated everything on Qdrant.

## Context

Mei's benchmark (2026-07-01) measured pgvector HNSW recall and latency as the index
grows, on `pg-arca-primary-01`-class hardware:

| Vectors | Recall@10 | p95 query | Index build |
|---|---|---|---|
| 1M | 0.97 | 8 ms | 11 min |
| 4M | 0.96 | 19 ms | 54 min |
| 8M | **0.88** | 71 ms | 4 h 20 m |
| 8M, `ef_search=200` | 0.95 | 210 ms | — |

Recall collapses past ~6M in a single index, and the only lever, `ef_search`, trades
it straight back for latency we do not have (ADR-012 gives candidate generation
120 ms). Partitioning by tenant helps the small tenants and does nothing for the one
tenant that is itself 8M vectors.

That tenant is Northwind Retail (`tnt_8842`), whose escalation on 2026-06-29 was
exactly this: relevance getting worse as they uploaded more.

Qdrant on the same data: recall@10 0.96 at 8M with p95 24 ms, using scalar
quantization and a 4-node cluster.

## Decision

Introduce Qdrant as a second vector store, behind the existing index interface
(ARCA-329):

- Tenants with **more than 2M vectors** are served from Qdrant.
- Tenants below that stay on pgvector, where the co-location win is real and the
  recall is fine.
- Routing is a per-tenant flag in `arca.tenants`, not a heuristic.
- Qdrant cluster `qdrant-prod-eu1`, 4 nodes, provisioned under INFRA-88.

## Consequences

- We are running two vector stores. Daniel voted against this and said so: "we are
  reintroducing the hydration hop we did the whole migration to remove, for exactly
  the tenants who care most about latency." He is right and we are accepting it.
- Two code paths in `arca-retrieve`, two sets of recall behaviour, and eval results
  that are not comparable across tenants.
- The threshold of 2M is arbitrary. Mei picked it as "comfortably below where recall
  moves". Expect it to be wrong.
- Tomas needs a Qdrant backup and restore runbook before any tenant is routed there.

## Alternatives considered

- **Shard pgvector across more partitions.** Does not help a single 8M-vector tenant.
- **Reduce dimensions to 768 with a smaller model.** Would buy roughly 2x headroom
  and cost nDCG. Elliot rejected it; we just spent a quarter choosing this model.
- **Move everything to Qdrant now.** Considered and deferred, mid-migration, as too
  much change at once. This is what ADR-019 eventually did anyway.
