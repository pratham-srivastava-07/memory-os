---
doc_id: meeting_010
type: meeting
title: "Arca Architecture Review #3 — vector storage"
date: 2026-06-04
time: "12:00–13:10 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Mei Lin Zhao, Elliot Vance, Priya Raman, Tomas Herrera]
apologies: [Karen Oyelaran, Jonas Weiss]
projects: [Arca, Migration]
tickets: [ARCA-260, ARCA-329, MIG-101]
decisions: [ADR-004]
tags: [architecture, vector-search, pgvector, qdrant, review]
---

# Arca Architecture Review #3 — 2026-06-04

Pre-read: Daniel's vector storage options doc, 2026-06-03.

**Daniel:** pgvector, HNSW, in the same cluster. `m=16`, `ef_construction=200`,
cosine. The argument is the one from the readout: retrieval becomes a single SQL
statement. Filter, vector search, hydrate, one plan, one round trip. I prototyped it
at 3M vectors and got 22 ms p95.

**Elliot:** Three million is not the number that matters. What happens at eight?

**Daniel:** I do not have that number.

**Mei:** Nor do I, and that is the thing I want on the record. I went looking for a
public benchmark of pgvector HNSW recall above 10M rows and I could not find one I
believe. Everything is at one or two million.

**Elliot:** Qdrant publishes numbers up there and they are good. Real filtering,
quantization, the recall curve stays flat.

**Daniel:** And it is a second datastore, two weeks after we decided to delete one.
I do not think we get to make that argument in May and un-make it in June.

**Elliot:** We would be making it for a different reason.

**Priya:** How big is our biggest tenant?

**Mei:** Northwind Retail, 4.4M chunks and climbing about 300k a week. So they hit
eight million in the autumn on the current curve, and sooner if their backfill lands.

**Tomas:** Index build time is my concern, not recall. Three million took 38 minutes
with 8 GB of maintenance work mem. If that is superlinear then a rebuild at 20M is an
outage-length operation and I need to know that before I promise a restore time.

**Daniel:** Nobody has measured it.

**Priya:** So what are we deciding?

**Mei:** I would decide pgvector now, because the alternative is blocking the
migration on a benchmark I do not have time to run this month, and because moving
vectors later is a bounded piece of work — it is behind an interface either way.
But I want three things written into the ADR. One, that we have no evidence above
10M. Two, that Qdrant is deferred, not rejected. Three, that we open the ticket for
the adapter now so the interface stays honest.

**Daniel:** I will take that.

**Priya:** Decided, with Mei's three conditions in the text. Who runs the benchmark
that answers the question?

**Mei:** Me, when the backfill is not eating my week. Realistically July.

## Decision

pgvector HNSW in the primary cluster. ADR-004, including the explicit statement that
recall above 10M vectors is unverified and that Qdrant is deferred rather than
rejected. `ARCA-329` opened for the adapter interface.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-004 with the three conditions | Daniel | 2026-06-05 |
| 2 | Open ARCA-329, index adapter interface | Daniel | 2026-06-05 |
| 3 | pgvector recall benchmark at 8M+ | Mei | July |
| 4 | Measure HNSW build time scaling | Tomas | 2026-06-26 |
