---
doc_id: meeting_027
type: meeting
title: "Platform Sync — Week 13"
date: 2026-07-28
time: "09:00–09:45 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Ravi Menon, Ava Duarte, Karen Oyelaran, Elliot Vance, Jonas Weiss]
apologies: [Mei Lin Zhao, Tomas Herrera, Sofia Nyberg]
projects: [Arca, Migration, API v2]
tickets: [MIG-136, MIG-131, ARCA-317, ARCA-329, API-71]
tags: [sync, cutover, completed]
---

# Platform Sync — 2026-07-28

**The read cutover completed last night.** Mei ran it from 22:00 to 01:40 UTC and is
off today, as agreed. Ravi presented.

## Cutover report

**Ravi** — All 84 tenants flipped. Smallest first, largest last. Timeline:

| UTC | Event |
|---|---|
| 22:00 | Window opens. Pre-flight checks green. |
| 22:15 | First batch, 40 tenants under 50k chunks. Zero divergence pre-flip, zero post-flip. |
| 23:10 | Second batch, 30 tenants. One tenant (`tnt_7731`, Lumen Health) held back — pre-flight divergence assertion failed, 12 rows. |
| 23:25 | `tnt_7731` investigated. The 12 rows were documents deleted between the audit and the flip. Re-asserted, clean, flipped. |
| 00:05 | Third batch, 13 tenants. |
| 00:40 | `tnt_8842` (Northwind Retail) flipped alone, watched for 30 minutes. |
| 01:20 | All tenants on Postgres for reads. Error rate flat throughout. |
| 01:40 | Window closed. |

**Elliot** — nDCG@10 measured against production traffic samples before and after:
0.78 both sides. No quality movement, which is what we wanted — this was a storage
change, not a ranking change.

**Daniel** — p95 on `/v1/retrieve` for the first eight hours post-cutover is 268 ms,
against a 400 ms budget. That is better than the 341 ms we were running on Mongo.

> Priya: Because of the hydration hop?
> Daniel: Because of the hydration hop, for the tenants still on pgvector. The nine
> tenants on Qdrant have the hop back and they are at 310 ms. Still under budget.

**Priya:** So the thing we lost by splitting the vector store, we lost. And it is
inside budget. Fine.

## What is still open

- Dual write stays on until **2026-08-10**. It is the rollback.
- Mongo decommission (MIG-131) is **2026-08-14**.
- The 800-token reindex cannot start until dual write is off.

## Round-robin

- **Ravi** — ARCA-317 hybrid search is in review. First change that will go through
  Elliot's harness properly.
- **Ava** — GraphQL gateway deleted. Expansion parameters in progress.
- **Karen** — SEC-51 CI check merged.
- **Jonas** — Nightly cross-tenant probe still not started. He is at 50% and the
  RLS work ate it.
- **Elliot** — GPU nodes are provisioned and still not taking traffic; the runbook is
  Daniel's and Daniel is on call.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Cutover retro note in `#proj-migration` | Ravi | 2026-07-29 |
| 2 | Update `project_migration.md` timeline | Mei | 2026-07-31 |
| 3 | GPU runbook | Daniel | 2026-08-07 |
| 4 | Nightly probe job | Jonas | 2026-08-07 |
