---
doc_id: meeting_030
type: meeting
title: "Vector store consolidation session"
date: 2026-08-05
time: "10:00–11:00 UTC"
attendees: [Mei Lin Zhao, Daniel Okoye, Elliot Vance, Priya Raman, Ravi Menon, Karen Oyelaran]
apologies: [Tomas Herrera, Jonas Weiss]
projects: [Arca]
tickets: [ARCA-329, INFRA-88, MIG-131]
decisions: [ADR-019]
tags: [vector-search, qdrant, pgvector, consolidation, decision]
---

# Vector store consolidation session — 2026-08-05

Pre-read: Mei's one-pager, 2026-08-04. Short because the numbers are from ADR-014 and
everyone has seen them.

**Mei:** Four weeks of running both. Nine tenants on Qdrant, seventy-five on pgvector.
The nine are 71% of query volume and 88% of vectors. Everything below the threshold
is, in aggregate, a rounding error we are maintaining a second code path for.

Three things changed my mind since ADR-014:

One, the threshold moves. Three tenants crossed 2M in July and were migrated by hand.
Two of the nine will drop back under after the reindex. It is a treadmill and Ravi is
the treadmill.

Two, the cost is not the infrastructure, it is Karen's matrix. Six percent flake rate
on the retrieval suite, almost all of it in the two-store paths.

Three, the reason for the split has expired. ADR-014 said moving eighty-four tenants
two weeks before a cutover was too much change at once. The cutover is done.

**Daniel:** I want to say the thing I said in July, from the other side.

In ADR-004 I argued for pgvector because co-location removes the hydration hop. That
argument is now dead, and not because of Qdrant. It is dead because the reranker is on
separate GPU nodes and hydration is a separate stage anyway. The single-SQL-statement
plan I prototyped in June is not what production runs and has not been for a month.
So I am no longer defending a thing that exists.

**Priya:** Say that in the ADR. Plainly.

**Daniel:** I will. And the other half: the migration was still right. Transactions
and one datastore instead of two — both real, both delivered. One of the three reasons
did not survive contact with our scale. That is a normal outcome and I do not want it
written up as a mistake.

**Elliot:** Practical point. Post-consolidation the eval baseline has to be re-taken.
Runs across different vector stores are not comparable and the harness should refuse
to compare them, not silently do it.

**Ravi:** Smallest first, same runbook I used in July. Seventy-five tenants, mostly
tiny. A week, maybe less.

**Karen:** And then I delete half my test matrix.

**Mei:** What is the rollback?

**Daniel:** Keep `arca.chunks.embedding` populated and readable. Drop the HNSW index
immediately — that is about 180 GB back and it takes the index maintenance cost off
the write path — but keep the column.

**Mei:** Until when? An unowned rollback path lives forever.

**Daniel:** 30 September. Written in the ADR with a date, not "for now".

**Priya:** Agreed. And delete the pgvector code path once the last tenant moves. Not
behind a flag. A flag is a code path.

## Decision

All tenants consolidate on Qdrant. ADR-019, supersedes ADR-004 and ADR-014.
`qdrant-prod-eu1` to six nodes, `qdrant-prod-us1` at three. `arca.chunks.embedding`
kept read-only until 2026-09-30, HNSW index dropped immediately.

Does not affect the Mongo decommission, which stays 2026-08-14.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-019 including Daniel's statement | Mei | 2026-08-05 |
| 2 | Grow Qdrant clusters (INFRA-88) | Ravi | 2026-08-07 |
| 3 | Migrate remaining 75 tenants | Ravi | 2026-08-14 |
| 4 | Re-baseline eval after consolidation | Elliot | 2026-08-17 |
| 5 | Delete pgvector path from `arca-retrieve` | Daniel | 2026-08-21 |
