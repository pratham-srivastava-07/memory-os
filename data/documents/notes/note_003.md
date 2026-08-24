---
doc_id: note_003
type: note
subtype: spike_plan
title: "ARCA-212 datastore evaluation — plan"
author: Mei Lin Zhao
date: 2026-05-11
projects: [Arca]
tickets: [ARCA-212]
tags: [spike, evaluation, methodology, postgres, mongodb, cockroachdb]
---

# ARCA-212 — datastore evaluation plan

Two-week timebox, ends 2026-05-22. Readout 2026-05-28.

## What I am and am not testing

I am testing whether a different system of record would be better for Arca. I am
**not** testing where vectors live. Those are two questions and I have watched teams
conflate them and end up with a decision nobody can unpick later. If the benchmark
shows the two are coupled I will say so and still write them up separately.

## Candidates

- PostgreSQL 16 + pgvector 0.7
- MongoDB 7 (current, as the baseline)
- CockroachDB 24.1 (Daniel asked)

Not testing: DynamoDB (no vector story, and we would be inventing a query layer),
Elasticsearch (we are not looking for a search engine, we are looking for a store),
anything managed-only where I cannot control the hardware for a fair comparison.

## Corpus

5M chunks. Not synthetic-random — generated from the tenant size distribution we
actually have, so the long tail of tiny tenants and the two enormous ones are both
represented. Largest synthetic tenant is 3.1M chunks, matching Northwind Retail.

## Hardware

Identical for all three: 16 vCPU, 64 GB, gp3 at 8000 IOPS. Single node. I am
deliberately not testing replication topology; that is an operations question and
Tomas has opinions that are not benchmarkable.

## Measurements

1. Chunk insert throughput, batched, sustained for 10 minutes
2. Hydration p50/p95/p99: fetch 200 documents by id
3. Behaviour under a partial-failure ingest (kill the process mid-write, count orphans)
4. Index build time where applicable
5. Restore time from a backup of the full corpus

## What would change my mind

I want to write this down before I have numbers so I cannot move the goalposts.

- If Postgres insert throughput is below 5k/sec batched, that is disqualifying. Our
  peak is 2.3k/sec and I want at least 2x headroom.
- If the orphan test does not come out clean on the transactional stores, my main
  argument is gone.
- If restore time for Postgres at 5M chunks is over two hours, I want to talk to
  Tomas before recommending it.
- If Mongo's hydration number is within 10 ms of Postgres, reason 2 for moving
  evaporates and this becomes a much weaker case.

## What I am not going to be able to answer

pgvector recall above 10M vectors. Our corpus for this test is 5M and building a 20M
corpus is a week I do not have. I will flag this as an open risk in the readout and I
expect somebody to want to skip past it.
