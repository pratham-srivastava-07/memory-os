---
doc_id: decision_002
type: decision
adr_id: ADR-002
title: "Primary datastore: PostgreSQL 16 over MongoDB"
date: 2026-05-29
status: accepted
deciders: [Mei Lin Zhao, Daniel Okoye, Priya Raman, Tomas Herrera]
project: Migration
project_id: PRJ-1103
tickets: [ARCA-212, MIG-101]
supersedes: []
superseded_by: []
tags: [database, postgres, mongodb, migration]
---

# ADR-002: Primary datastore — PostgreSQL 16 over MongoDB

## Status

Accepted 2026-05-29, one day after the evaluation readout. Mei wrote the evaluation
(ARCA-212); the numbers referenced here are hers.

## Context

Arca has used MongoDB as the system of record since the prototype. Three things
pushed us to re-open the choice:

1. **Consistency across collections.** A document write touches `documents`, `chunks`
   and `jobs`. When ingest fails halfway we get orphaned chunks. We have a nightly
   reconciler; it found 11,400 orphans in April alone, and one customer (Lumen
   Health, `tnt_7731`) noticed before we did.
2. **Two-phase retrieval.** Vectors live in a separate index. `arca-retrieve` does a
   vector search, gets IDs, then hydrates from Mongo. That second hop is 40–60 ms of
   the p95 and it is pure overhead.
3. **We already run Postgres** for the control plane. Two datastores, two backup
   stories, two sets of on-call knowledge.

## Decision

PostgreSQL 16 becomes the system of record for document metadata, chunk records and
job state. The control plane moves into the same cluster under a separate schema.

Vectors go in pgvector in the same database. This is a **separate decision** with its
own trade-offs and is recorded in ADR-004 — do not read this ADR as having settled
the vector store question.

## Rationale

From the evaluation:

- Transactional writes across the three tables remove the orphan class of bug
  entirely, not statistically.
- Postgres p95 on the hydration query was 6 ms against Mongo's 41 ms at the same
  row count, mostly because the rows are already in the buffer cache from the vector
  scan.
- Write throughput was the one place Mongo won: 18k chunk inserts/sec versus 11k for
  Postgres on identical hardware. We accept this. Our peak sustained rate is 2.3k/sec
  and we batch.
- Operational familiarity. Tomas has run Postgres for eleven years and has never run
  a Mongo shard rebalance.

## Alternatives considered

- **Stay on MongoDB, add a transactional wrapper.** Mongo transactions across
  collections exist but require a replica set config we do not have and would have
  meant a migration of its own.
- **CockroachDB.** Evaluated at Daniel's suggestion. Genuinely good fit for the
  multi-region story we might want in 2027. Rejected: no mature vector index, and the
  licensing conversation was going to take longer than the migration.
- **Split: Postgres for metadata, keep Mongo for chunks.** Rejected. Keeps both
  operational burdens and does not fix the orphan problem, which spans the two.

## Consequences

- A migration project. See PRJ-1103.
- Write throughput headroom shrinks from ~8x to ~5x. Tomas wants an alert at 60% of
  measured ceiling.
- Every `arca-*` service needs a connection pool and a story about pool exhaustion.
