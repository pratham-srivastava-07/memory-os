---
doc_id: note_024
type: note
subtype: checklist
title: "MongoDB decommission checklist"
author: Mei Lin Zhao
date: 2026-08-03
projects: [Migration]
tickets: [MIG-131, MIG-107]
tags: [decommission, mongodb, checklist, migration]
---

# MongoDB decommission checklist — MIG-131

**Target date: 2026-08-14.** Dual write comes off 2026-08-10; four days of
Postgres-only before the cluster goes away, deliberately, so that anything that was
silently depending on Mongo has time to break while the data still exists.

> `project_migration.md` says 2026-08-21. That is wrong; it predates ADR-015 and
> nobody has updated the table. The date is the 14th.

## Before dual write comes off (by 2026-08-10)

- [ ] Retry queue depth and oldest-item age alerting live — **done 2026-07-30**, and
      it should have been done on 3 July
- [ ] Continuous per-tenant divergence assertion running (Ravi) — in progress
- [ ] Zero unexplained divergence for 7 consecutive days
- [ ] Confirm no service reads Mongo. Grep is not sufficient; check the connection
      metrics on `mongo-arca-01` for any client that is not `arca-index`
- [ ] Tomas back (10 August) or explicit agreement that we proceed without him

## Between 10 and 14 August

- [ ] Dual write disabled. `arca-index` writes Postgres only.
- [ ] Mongo cluster left running, receiving nothing. **Do not stop it.** If something
      breaks we want the data, not a restore.
- [ ] Watch: ingest error rate, retrieval error rate, any 404 on documents
- [ ] Final full backup of `mongo-arca-01`, verified restorable into a scratch
      cluster. Retain 12 months. This is the actual insurance.

## On 14 August

- [ ] Final backup verified (again, on the day)
- [ ] Stop the cluster. Do not delete.
- [ ] Delete on **2026-09-14**, one month later, and put that in someone's calendar
      rather than leaving it to memory

## After

- [ ] Delete the `arca_backfill` role with `BYPASSRLS`. Jonas raised this as SEC-44
      finding 3 and it has had no owner since June. Taking it.
- [ ] Remove Mongo from the on-call runbooks
- [ ] Remove the Mongo connection from `arca-core`
- [ ] Cancel the Atlas contract — check the notice period, I think it is 30 days
- [ ] The nightly orphan reconciler, 340 lines, deleted. It exists only because Mongo
      had no cross-collection transaction. This is the thing I have wanted to delete
      since April.

## Not in scope

The 800-token reindex (ADR-011) starts after this, not during. And per ADR-019 the
Qdrant consolidation runs in parallel with the decommission but touches nothing Mongo
holds.
