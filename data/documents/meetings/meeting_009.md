---
doc_id: meeting_009
type: meeting
title: "Platform Sync — Week 5"
date: 2026-06-02
time: "09:00–09:45 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Jonas Weiss]
projects: [Arca, Migration, API v2, Helios]
tickets: [MIG-101, MIG-107, ARCA-317, API-52, HEL-12]
tags: [sync, migration, helios]
---

# Platform Sync — 2026-06-02

## Round-robin

**Mei** — MIG-101 schema is in review. Four tables in schema `arca`. `arca.chunks` is
hash-partitioned on `tenant_id`, 32 partitions. Starting MIG-107, dual write, this
week. Target: dual write live in prod 2026-06-08.

**Daniel** — ARCA-317 prototype. BM25 over a Postgres full-text index, fused with the
vector results by reciprocal rank fusion. On the identifier queries in Elliot's set it
goes from 0.12 to 0.68 nDCG@10. On everything else it is flat.

> Priya: Ship it?
> Daniel: Not until the chunker changes, because RRF weights are going to be sensitive
> to chunk size and I would rather tune once.
> Priya: Then park it properly, do not leave it half-built.

*(ARCA-317 was parked. It stays parked and unowned for eight weeks.)*

**Tomas** — Kicking off Helios, PRJ-1120. The Datadog renewal is 1 October and the
2026 projection is $214k, most of it cardinality from `arca-index`. Six engineer-weeks
to a usable self-hosted stack, about $3.5k/month to run.

> Priya: Six weeks of whose time?
> Tomas: Mine, mostly. Mei for the storage layer.
> Priya: Those are the two people on the critical path of the migration.
> Tomas: I know. That is why I am raising it now rather than in August.

**Ava** — Protocol decision meeting booked for the 11th. Pre-read out Wednesday.

**Elliot** — Query set at 900. Two more weeks to 1,400.

**Jonas** — RLS design started. He wants to be in the migration schema review because
policies are easier to add now than later.

**Karen** — Asked what the test story is for dual write. Answer: nobody had thought
about it. She will write one.

**Sofia** — Nothing new. Northwind Retail are happy. She notes they are at 4.4M chunks
now, up from 3.1M four weeks ago.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Dual write live in prod | Mei | 2026-06-08 |
| 2 | Test plan for dual write divergence | Karen | 2026-06-09 |
| 3 | Helios go/no-go decision at a future sync | Priya | TBD |
| 4 | Jonas added to schema review | Mei | 2026-06-03 |
