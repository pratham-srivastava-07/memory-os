---
doc_id: meeting_016
type: meeting
title: "Platform Sync — Week 8"
date: 2026-06-23
time: "09:00–09:55 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Jonas Weiss, Ravi Menon]
projects: [Arca, Migration, API v2, Helios]
tickets: [MIG-112, MIG-118, ARCA-288, HEL-31]
incidents: [INC-2026-0617]
decisions: [ADR-009]
tags: [sync, migration, slip]
---

# Platform Sync — 2026-06-23

The read cutover was scheduled for yesterday. It did not happen. Formal go/no-go is
Thursday but everyone knows the answer.

## Migration status

**Mei** — Backfill is 62% by row count, not 100%. Two things ate the schedule.

First, `content_hash` uniqueness. Mongo let us store duplicate `content_hash` per
tenant and the Postgres schema has a unique constraint. 41,000 rows affected. Ravi
spent four days working out whether they were genuine duplicates.

**Ravi** — They mostly are. About 38k are the same document uploaded twice, usually
by a customer retrying a failed upload. The other 3k are real collisions where two
different documents hash the same because we hash the extracted text and two invoices
from the same template with different numbers extract to nearly the same string.
Nearly, not exactly — so those are a bug in our extractor, not in the hash.

**Daniel:** That is a good find.

**Ravi:** I would like to fix the extractor rather than loosen the constraint.

**Mei:** Fix it after cutover. Right now we skip and log.

Second, MIG-118. The divergence spikes are real. Under Northwind Retail's write
pattern the async retry queue lags. Measured yesterday at peak: 41 minutes.

> Tomas: Forty-one minutes. And we only know that because you went looking.
> Mei: Yes.
> Tomas: This is AI-4.
> Mei: This is AI-4.

**Priya:** So what is the new date?

**Mei:** I want three weeks, not one. Five days to fix MIG-118 properly, four days for
a 100% divergence audit rather than 1% sampling, and slack, because ADR-006 had none
and that is why we are having this conversation.

**Priya:** Three weeks is 13 July. Take it to Thursday's go/no-go formally.

## Everything else

- **Daniel** — AI-1, load shedding in `arca-rank`, in progress. AI-3, runbook, done.
- **Tomas** — AI-2, deploy annotations, in progress. Helios HEL-31 is stalled because
  he is doing incident actions.
- **Ava** — Fan-out measurement done and it is bad. A document with 2,000 chunks
  produces 340 calls into `arca-retrieve` from one GraphQL query. Batched. It was six
  before. She is not conceding the decision, she is reporting the number.
- **Elliot** — Looked at the Northwind Retail relevance complaints. The chunker is not
  the problem. He thinks it is recall and he cannot prove it without the benchmark
  Mei owes.
- **Priya** — ADR-009, deploy policy, written and merged. In the handbook.
- **Jonas** — RLS is in the schema and enabled in staging. 9% p95 regression on the
  hydration query. He is calling that acceptable; Mei is less sure.
- **Sofia** — Northwind Retail at 5.6M chunks.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Formal go/no-go Thursday | Priya | 2026-06-25 |
| 2 | Fix MIG-118 properly | Ravi | 2026-06-30 |
| 3 | Extractor hash bug, after cutover | Ravi | later |
| 4 | pgvector recall benchmark — now blocking a customer question | Mei | 2026-07-03 |
