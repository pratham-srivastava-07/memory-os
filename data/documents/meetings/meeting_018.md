---
doc_id: meeting_018
type: meeting
title: "Platform Sync — Week 9"
date: 2026-06-30
time: "09:00–09:45 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Ravi Menon]
apologies: [Jonas Weiss]
projects: [Arca, Migration, API v2]
tickets: [MIG-118, MIG-112, ARCA-244, ARCA-288, ARCA-341]
tags: [sync, escalation, chunking]
---

# Platform Sync — 2026-06-30

## Escalation first

**Sofia** — Northwind Retail escalated yesterday. Written, to their account manager,
copied to their CTO. The complaint: search quality has degraded materially since
April and they can demonstrate it with saved queries that used to return the right
document and now do not. They are at 6.2M chunks. They have asked for a technical
call this week.

> Priya: Elliot, is it the chunker?
> Elliot: No. I ran their saved queries against a re-chunked copy of their corpus and
> the results are the same. It is not chunking.
> Mei: Then it is recall, and it is the thing in ADR-004 that I said we had no
> evidence about.
> Priya: How long to have the evidence?
> Mei: Two days if I stop doing migration work.
> Priya: Stop doing migration work.

## Round-robin

**Mei** — MIG-118 fix is written, in review, deploying Thursday. Backfill at 81%.
Pausing both to run the recall benchmark.

**Ravi** — Divergence audit tooling done. It can now assert zero divergence per tenant
before a flip, which is Karen's condition.

**Elliot** — ARCA-341 harness at 1,400 queries. He has run the three chunking
strategies and structure-aware wins clearly: 0.78 nDCG@10 against 0.71 for the current
fixed 512. Writing it up as an ADR for Wednesday.

> Daniel: That is a bigger jump than I expected.
> Elliot: It is concentrated in documents with tables. Which is most of what our two
> biggest customers upload.

**Daniel** — AI-1 load shedding merged. `arca-rank` now rejects when the projected
wait exceeds the caller's deadline.

**Tomas** — AI-2 deploy annotations done. Alerts now carry the last three deploys
across all four services.

**Ava** — GraphQL depth limiter in. She notes she picked the limit by increasing it
until the console stopped erroring, which she says out loud because she does not want
it to be a secret.

**Karen** — AI-6, production query replay, started.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | pgvector recall benchmark at 8M+, drop everything | Mei | 2026-07-02 |
| 2 | Chunking v2 ADR | Elliot | 2026-07-01 |
| 3 | Technical call with Northwind Retail | Sofia, Daniel | 2026-07-03 |
| 4 | Deploy MIG-118 fix | Mei | 2026-07-02 |
