---
doc_id: meeting_005
type: meeting
title: "Platform Sync — Week 3"
date: 2026-05-19
time: "09:00–09:45 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Karen Oyelaran, Elliot Vance, Jonas Weiss]
apologies: [Sofia Nyberg]
projects: [Arca, API v2]
tickets: [ARCA-212, ARCA-244, ARCA-341, API-58, SEC-44]
tags: [sync, eval, hiring]
---

# Platform Sync — 2026-05-19

## Round-robin

**Elliot** — Phase 1 eval harness exists. 400 queries scraped from console logs,
hand-labelled by him over the weekend, which he does not want to do again.
Baseline on current production: nDCG@10 0.71, recall@20 0.83. That is now a number we
can regress against.

**Mei** — Migration costing in progress. Early read: the backfill is the long pole,
not the schema. 14.6M chunks today, and copying them at a rate that does not compete
with live ingest is roughly two weeks of wall clock, assuming nothing goes wrong.
She has assumed something will go wrong.

**Daniel** — `arca-retrieve` is split out. `arca-rank` next. Then he wants to look at
ARCA-317, hybrid search, because pure vector search is bad at exact identifiers.
Somebody searching for "invoice INV-88213" gets nothing useful.

> Sofia (async, in the doc): this is the second-most common complaint from Northwind
> Retail after "it gets worse as we upload more".

**Ava** — REST vs GraphQL writeup half done. She wants a decision meeting, not a sync
slot.

**Tomas** — Nothing on fire. Says he still owes the p95 alert change.

**Jonas** — SEC-44 draft is out. Two findings so far. Finding 1: application-level
tenant filtering across 147 query sites, no mechanical enforcement. Finding 2: if
API v2 ends up with two protocols, that is two auth paths, and he will push back on
that when the protocol decision happens.

**Karen** — Compose file done. Same one runs locally and in CI.

**Priya** — Headcount approved. One backend engineer, starting mid-June. Ravi Menon,
offer accepted, start date 2026-06-15, based in Bengaluru. He will need a buddy.

> Daniel: I will do it.
> Priya: You are also splitting three services and leading Arca.
> Daniel: I will do it.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Finish REST vs GraphQL writeup, book decision meeting | Ava | 2026-05-26 |
| 2 | p95 alert change (carried from 2026-05-12) | Tomas | 2026-05-26 |
| 3 | Onboarding plan for Ravi | Daniel | 2026-06-10 |
