---
doc_id: note_002
type: note
subtype: scratch
title: "Everything that is wrong with our Mongo setup"
author: Daniel Okoye
date: 2026-05-07
projects: [Arca]
tickets: [ARCA-212]
tags: [mongodb, scratch, complaints]
---

# Everything that is wrong with our Mongo setup

Not an argument, a list. Mei asked me to write down the pain rather than say
"Postgres" at her in the sync. Fair.

1. **No transaction across `documents`, `chunks`, `jobs`.** Ingest writes three
   collections. If it dies between one and two we get orphans. 11,400 in April. The
   nightly reconciler is 340 lines of code that exists only because of this.

2. **The hydration hop.** Vector search returns 200 ids, we go to Mongo for 200
   documents, that is 41 ms p95 and it is on every single query. It is a third of our
   candidate generation budget doing nothing but fetching.

3. **No real filtering in the vector index.** We over-fetch by 4x and filter in
   application code because the index cannot filter by `tenant_id` and date at the
   same time without falling over.

4. **Schema is whatever the last writer thought.** `chunks` has documents with
   `ordinal`, documents with `order`, and documents with both. Three years of
   accretion. Nobody knows which readers depend on which.

5. **Two datastores.** We already run Postgres for the control plane. Two backup
   procedures, two restore rehearsals, two things Tomas has to know at 3 a.m.

6. **The 3 a.m. thing.** Tomas has never done a shard rebalance. Neither have I.

## What Mongo is genuinely better at

Being honest so this is not just a hit piece:

- Write throughput. Materially better, not marginally.
- Schema evolution. Adding a field to 40M documents is free. In Postgres it is a
  conversation.
- It has never lost data. Three years, zero data loss incidents. That is worth
  something and I keep forgetting to say it.

## What I actually want

Postgres. But I want Mei to run the benchmark, because if I run it I will find what I
am looking for.
