---
doc_id: decision_001
type: decision
adr_id: ADR-001
title: "Arca service decomposition"
date: 2026-05-08
status: accepted
deciders: [Daniel Okoye, Priya Raman, Tomas Herrera, Mei Lin Zhao]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-233, ARCA-301]
supersedes: []
superseded_by: []
tags: [architecture, services]
---

# ADR-001: Arca service decomposition

## Status

Accepted 2026-05-08. Discussed in the Arca Architecture Review of the same day.

## Context

Arca started as one Python service, `arca`, doing upload, parse, chunk, embed, store
and query. It is 34k lines and one deploy. Two problems forced the question:

- Ingest is bursty and CPU-bound (embedding). Query is latency-sensitive and mostly
  I/O. They want different scaling curves and different node types, and today one
  large tenant upload makes p95 retrieval jump by 400 ms.
- Any change to the query planner requires a deploy that also restarts in-flight
  ingest jobs.

## Decision

Split into four deployables behind a shared library for the domain types:

| Service | Responsibility |
|---|---|
| `arca-ingest` | Upload, parse, chunk, enqueue |
| `arca-index` | Embed, write vectors and metadata |
| `arca-retrieve` | Query planning, candidate generation, hydration |
| `arca-rank` | Cross-encoder reranking |

`arca-index` and `arca-rank` are the only services that hold a model in memory.
`arca-retrieve` calls `arca-rank` synchronously; everything else is queue-driven.

We are explicitly **not** splitting the datastore. All four services talk to the same
store, whatever that store ends up being — that question is open and tracked in
ARCA-212.

## Consequences

- Four deploy pipelines, four sets of dashboards. Tomas wants a runbook per service
  before any of them page anyone.
- The domain types become a shared library, `arca-core`, and a versioning problem.
- Ingest can now be throttled per tenant without touching the query path.

## Alternatives considered

- **Keep the monolith, scale vertically.** Cheapest today. Rejected because the
  noisy-neighbour effect on retrieval latency is already customer-visible.
- **Two services (write path / read path).** Daniel preferred this. Rejected because
  the reranker needs GPU-class nodes eventually and we did not want that constraint
  on the whole read path.
