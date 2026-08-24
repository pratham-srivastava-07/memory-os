---
doc_id: note_015
type: note
subtype: benchmark
title: "pgvector recall at scale — the benchmark I said I could not run in May"
author: Mei Lin Zhao
date: 2026-07-06
projects: [Arca]
tickets: [ARCA-329, ARCA-260]
tags: [benchmark, pgvector, qdrant, recall, scale]
---

# pgvector recall at scale

Ran Thursday and Friday. This is the benchmark I flagged as untestable in the ARCA-212
timebox (note_003) and as an unverified risk in ADR-004. It is now tested.

## Method

Real data, not synthetic: a copy of `tnt_8842` (Northwind Retail), which is
**8.1M chunks** as of 2026-07-02, plus padding from two other tenants to hit round
numbers at the lower points. 1024-dim `gte-large-v2` vectors, the production model.

Ground truth by exact search (`ORDER BY embedding <=> $1` with the index disabled) on
the same 500 queries drawn from their query log. Recall@10 is against that.

Hardware matched to `pg-arca-primary-01`: 32 vCPU, 256 GB.

## pgvector HNSW, m=16, ef_construction=200

| Vectors | Recall@10 | p95 query | Index build |
|---|---|---|---|
| 1M | 0.97 | 8 ms | 11 min |
| 2M | 0.97 | 11 ms | 24 min |
| 4M | 0.96 | 19 ms | 54 min |
| 6M | 0.93 | 38 ms | 2 h 05 m |
| 8M | **0.88** | 71 ms | 4 h 20 m |

With `ef_search` raised to 200 at 8M: recall 0.95, p95 **210 ms**.

## What this means

The curve is flat to about four million and then it is not. At eight million we are
losing one relevant result in eight, silently — there is no error, no alert, the
query returns ten things and two of them are wrong.

The only lever is `ef_search` and it buys recall with latency. 210 ms of candidate
generation against ADR-012's 120 ms budget is not a trade we can make.

Index build at 4h20m is its own problem. That is not a maintenance window, that is an
outage.

## Qdrant, same data, same queries

Elliot set this up; I verified the ground truth matched.

| Vectors | Recall@10 | p95 query |
|---|---|---|
| 8M | 0.96 | 24 ms |

Four nodes, scalar quantization, `hnsw_ef` 128. Filtering by `tenant_id` in the
payload index, which is a real filter, not a post-filter.

## What I want to say about ADR-004

I asked for three things to be written into that ADR: that we had no evidence above
10M, that Qdrant was deferred rather than rejected, and that the adapter ticket be
opened. All three were written. That is the process working — we made a decision with
a known unknown, wrote the unknown down, and when it resolved against us we knew
immediately what had to change and we had the interface to change it behind.

It is still a decision that turned out wrong, and Northwind Retail spent six weeks
with degraded search because of it. Both things are true.

## Correction

An earlier version of this note said `tnt_8842` was at 6.2M chunks. That figure was
from Sofia's escalation on 29 June and it was accurate then. They are at 8.1M as of
2 July. They are adding roughly 300k a week.
