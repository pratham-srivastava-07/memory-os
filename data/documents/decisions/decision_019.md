---
doc_id: decision_019
type: decision
adr_id: ADR-019
title: "Consolidate all tenants on Qdrant; retire pgvector"
date: 2026-08-05
status: accepted
deciders: [Mei Lin Zhao, Daniel Okoye, Elliot Vance, Priya Raman]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-329, INFRA-88, MIG-131]
supersedes: [ADR-004, ADR-014]
superseded_by: []
tags: [vector-search, qdrant, pgvector, consolidation, reversal]
---

# ADR-019: Consolidate all tenants on Qdrant; retire pgvector

## Status

Accepted 2026-08-05. Supersedes ADR-004 and ADR-014.

## Context

ADR-014 created a split: tenants over 2M vectors on Qdrant, everyone else on
pgvector. Four weeks of running both:

- Nine tenants are on Qdrant. Seventy-five are on pgvector.
- Nine tenants account for 71% of query volume and 88% of vectors.
- Every change to `arca-retrieve` is written twice and tested twice. Karen's test
  matrix doubled and she has said the split is the single biggest source of flakes.
- The 2M threshold moved once already (three tenants crossed it in July and had to be
  migrated one at a time, by hand, by Ravi).
- Post-ADR-011 reindexing at 800-token chunks reduces chunk count 38%, which would
  push two tenants back *under* the threshold. Nobody wants to migrate them back.
- The co-location argument from ADR-004 is dead anyway: with the reranker on separate
  GPU nodes and hydration already a separate stage, the single-SQL-statement plan
  Daniel prototyped is not what production runs.

## Decision

All tenants move to Qdrant. `qdrant-prod-eu1` grows to 6 nodes, `qdrant-prod-us1` is
provisioned at 3 (INFRA-88).

- Migration runs tenant by tenant, smallest first, reusing Ravi's runbook.
- `arca.chunks.embedding` is kept, populated and read-only, until **2026-09-30**.
  It is our rollback. The HNSW index on it is dropped immediately, which reclaims
  ~180 GB and removes the index maintenance cost from the write path.
- The pgvector code path in `arca-retrieve` is deleted once the last tenant moves,
  not kept behind a flag.

## Consequences

- Postgres remains the system of record for metadata. Retrieval is a Qdrant query
  followed by a Postgres hydration — the two-phase pattern that ADR-002 listed as a
  reason to migrate. Daniel asked that this be recorded plainly: **the vector
  co-location argument for the Postgres migration did not survive contact with our
  scale.** The other two reasons in ADR-002 (transactional consistency, one fewer
  datastore to operate) did, and the migration was still worth doing.
- Hydration is back on the critical path. ADR-012 already budgets 40 ms for it and
  post-ADR-016 it measures 38 ms, so this is covered.
- One vector store, one code path, one recall story.
- This does not change the Mongo decommission, which proceeds on 2026-08-14 (MIG-131).
