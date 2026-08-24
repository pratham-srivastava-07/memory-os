---
doc_id: meeting_013
type: meeting
title: "Platform Sync — Week 7"
date: 2026-06-16
time: "09:00–09:50 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Jonas Weiss, Ravi Menon]
projects: [Arca, Migration, API v2]
tickets: [MIG-112, MIG-118, ARCA-233, API-52]
tags: [sync, onboarding, backfill]
---

# Platform Sync — 2026-06-16

Ravi Menon's first sync. He started yesterday. Buddy is Daniel.

## Round-robin

**Ravi** — Introduced himself. Six years backend, mostly Go and Python, last three at
a payments company doing exactly this kind of datastore migration, which is why Priya
hired him. Environment set up, ran the compose file, it worked first time, which
Karen was pleased about.

**Mei** — Backfill is running. 38% through by tenant count, which is 9% by row count
because we did smallest first. No surprises yet. She flags one thing: the divergence
report shows occasional spikes she cannot explain and wants to look properly.

**Daniel** — `arca-ingest` handover to Ravi from next week. He is keeping ARCA-301.

**Ava** — GraphQL gateway skeleton is up in staging. Console document detail screen
now composes in one request. Has not measured the fan-out yet.

**Tomas** — Deploying `arca-retrieve` this afternoon, small change to the candidate
generation limit. Routine.

**Elliot** — 1,400-query set complete. Baseline re-run: nDCG@10 0.71, recall@20 0.83,
same as the 400-query set, which is reassuring.

**Karen** — Nothing blocking.

**Sofia** — Northwind Retail at 5.1M chunks. She has started noticing complaints in
their shared channel about relevance and wants somebody to look before it becomes an
escalation.

> Daniel: Look at what, specifically?
> Sofia: They say it used to find things and now it does not. Same queries.
> Elliot: That is either the chunker or the index. I can check the chunker.
> Mei: Or it is recall falling as the index grows, which is the thing I said I could
> not rule out.

**Jonas** — RLS design done, in review with Mei. Wants to land it before cutover.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Investigate divergence report spikes | Mei | 2026-06-19 |
| 2 | Check Northwind Retail relevance complaints | Elliot | 2026-06-23 |
| 3 | `arca-ingest` handover | Daniel → Ravi | 2026-06-22 |
| 4 | RLS review | Mei, Jonas | 2026-06-19 |
