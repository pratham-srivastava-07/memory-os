---
doc_id: meeting_003
type: meeting
title: "Platform Sync — Week 2"
date: 2026-05-12
time: "09:00–09:40 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Jonas Weiss]
projects: [Arca, API v2]
tickets: [ARCA-212, ARCA-233, ARCA-244, API-40]
tags: [sync, spike, chunking]
---

# Platform Sync — 2026-05-12

## Round-robin

**Mei** — ARCA-212 is running. Benchmarking Postgres 16, MongoDB 7 and CockroachDB
24.1 on the same hardware against a 5M-chunk synthetic corpus derived from real
tenant shapes. Report Thursday. She has asked people to hold opinions until then.

> Daniel: I have opinions.
> Mei: Hold them until Thursday.

**Daniel** — `arca-ingest` split out and deploying to staging. `arca-retrieve` next
week. ADR-001 is merged.

**Elliot** — Chunking. He pulled 40 Northwind Retail PDFs and looked at what the
512-token chunker does to them: 31% of chunks split a table across the boundary. He
cannot prove it hurts yet because there is no eval harness. Building one is now
ARCA-341.

> Priya: How long for a harness you would trust?
> Elliot: Three weeks to something with a real query set. One week to something that
> at least gives a number.
> Priya: Do the one-week version first.

**Ava** — Design partner interviews done. Three for three asked for "a normal REST
API with an OpenAPI file". Nobody asked for GraphQL. She still thinks the console
needs GraphQL and is going to write both up.

**Tomas** — Wants to raise something not on the agenda: our retrieval alert fires on
p50, not p95. So we alert when everything is slow and never when the tail is bad.

> Priya: Is that a five-minute fix?
> Tomas: It is a five-minute fix and a longer conversation about what our actual
> target is, because I have "250 ms p95" in my SLO draft and the project doc says
> 300 ms and I do not know where either came from.
> Priya: Park the target. Fix the alert.

*(The alert fix was not done. It comes up again on 2026-06-19 and again in ADR-012.)*

**Jonas** — Starting a threat model for the multi-tenant story, SEC-44. First
observation: 147 query sites append `tenant_id` in application code and any one of
them being wrong is a cross-tenant read.

**Karen** — Playwright migration done. Cypress deleted.

**Sofia** — Northwind Retail want a rate limit increase for a bulk backfill. Approved
600 to 2000/min, temporary, expires end of August.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Datastore evaluation report | Mei | 2026-05-14 |
| 2 | Minimal eval harness (ARCA-341 phase 1) | Elliot | 2026-05-19 |
| 3 | Change retrieval alert from p50 to p95 | Tomas | 2026-05-15 |
| 4 | Write up REST vs GraphQL for v2 | Ava | 2026-05-26 |
