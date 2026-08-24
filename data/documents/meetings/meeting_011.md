---
doc_id: meeting_011
type: meeting
title: "Platform Sync — Week 6"
date: 2026-06-09
time: "09:00–09:50 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Jonas Weiss]
projects: [Arca, Migration, API v2]
tickets: [MIG-107, MIG-112, ARCA-260, API-52, SEC-44]
tags: [sync, dual-write, migration]
---

# Platform Sync — 2026-06-09

## Round-robin

**Mei** — Dual write went live in prod yesterday, 2026-06-08, on schedule. Ingest p95
up 14 ms, which is what we modelled. Divergence report running hourly into
`#proj-migration` at 1% sampling.

> Tomas: One percent is thin. If we are behind, we find out an hour late and only on
> one write in a hundred.
> Mei: Agreed, it is thin. Full sampling costs more than the dual write does. I would
> rather add an explicit lag metric on the retry queue than raise the sampling rate.
> Tomas: Then add the lag metric.
> Mei: It is on the list.

*(The lag metric was not added before cutover. It comes back on 2026-06-19 as
postmortem action AI-4 and again on 2026-07-29.)*

**Mei (cont.)** — Backfill MIG-112 starts Thursday. Smallest tenants first.

**Daniel** — US region `arca-prod-us1` is up for the Northwind Retail pilot. Nothing
routed to it yet.

**Elliot** — ADR-005 written, embedding model. The residency constraint Jonas raised
is the load-bearing part.

**Ava** — Protocol pre-read is out for Thursday. Daniel's objection is in it.

**Jonas** — SEC-44 finding 2 formalised: two protocols means two auth paths. He is
raising it Thursday and expects to lose.

**Tomas** — Quiet week. Reminds everyone `arca-rank` still has no runbook and it is
now taking production traffic.

**Karen** — Dual-write test plan done. She is asserting on divergence in staging by
deliberately failing the Postgres write and checking the retry lands.

**Sofia** — Northwind Retail at 4.7M chunks.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Lag metric on dual-write retry queue | Mei | not dated |
| 2 | `arca-rank` runbook | Daniel | 2026-06-16 |
| 3 | Start backfill MIG-112 | Mei | 2026-06-11 |
