---
doc_id: note_004
type: note
subtype: benchmark
title: "ARCA-212 raw results"
author: Mei Lin Zhao
date: 2026-05-15
projects: [Arca]
tickets: [ARCA-212]
tags: [benchmark, results, postgres, mongodb, cockroachdb, raw]
---

# ARCA-212 raw results

Raw. The narrative is in the readout doc. Numbers here are medians of five runs
unless stated. Hardware per note_003.

## Insert throughput (chunks/sec, batched at 500)

| System | Sustained 10 min | Peak 30 s |
|---|---|---|
| MongoDB 7 | 18,100 | 22,400 |
| PostgreSQL 16 | 11,000 | 13,200 |
| PostgreSQL 16 (with HNSW index live) | 4,300 | 5,900 |
| CockroachDB 24.1 | 6,400 | 7,100 |

**The third row matters and I nearly missed it.** Maintaining an HNSW index on write
costs about 60% of insert throughput. 4,300/sec against our 2,300/sec peak is 1.9x
headroom, not 5x. If we put vectors in Postgres, that is the real number.

## Hydration, 200 documents by id (ms)

| System | p50 | p95 | p99 |
|---|---|---|---|
| MongoDB 7 | 22 | 41 | 78 |
| PostgreSQL 16 | 4 | 6 | 14 |
| PostgreSQL 16, cold cache | 19 | 34 | 61 |
| CockroachDB 24.1 | 9 | 14 | 31 |

The Postgres number is only 6 ms because the rows are already in the buffer cache
from the vector scan that produced the ids. Cold cache it is 34 ms, which is Mongo.
**This win exists if and only if the vectors are in the same database.** I will keep
saying this until somebody writes it down.

## Orphan test (kill -9 mid-ingest, 1000 iterations)

| System | Orphaned chunk records |
|---|---|
| MongoDB 7 | 3,847 |
| PostgreSQL 16 | 0 |
| CockroachDB 24.1 | 0 |

Clean. This is the strongest result in the whole exercise.

## Index build (5M vectors, HNSW m=16 ef_construction=200)

Postgres: 71 minutes with `maintenance_work_mem=8GB`. At 3M it was 38 minutes.
That is superlinear-ish over one data point, which is not a trend, but Tomas should
know.

## Restore from backup, full 5M corpus

| System | Time |
|---|---|
| MongoDB 7 | 48 min |
| PostgreSQL 16 | 94 min |
| PostgreSQL 16 (index rebuild included) | 165 min |

Over my two-hour threshold from the plan. I talked to Tomas. He is fine with it if we
have replicas, which we will.

## Open

Recall above 10M vectors — not tested, cannot be tested inside the timebox.
Flagged loudly.
