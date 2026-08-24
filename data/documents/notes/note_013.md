---
doc_id: note_013
type: note
subtype: task_update
title: "MIG-118 — dual-write retry lag investigation"
author: Ravi Menon
date: 2026-06-24
projects: [Migration]
tickets: [MIG-118, MIG-107, MIG-112]
tags: [task-update, migration, bug, dual-write]
---

# MIG-118 — dual-write retry lag

Status: investigating → root caused. Fix not written yet.

## Symptom

The divergence report shows spikes Mei could not explain. Under load, Postgres is
behind Mongo by minutes. Peak measured 2026-06-24 during Northwind Retail's morning
ingest: **41 minutes**.

## How the path actually works

Per ADR-006:

- Mongo write is synchronous. It can fail the request.
- Postgres write is fire-and-forget onto an in-process asyncio queue, drained by four
  worker tasks. Failures retry with exponential backoff.

## Root cause

Three things compounding.

1. **The queue is per-pod and in-memory.** Twelve `arca-index` pods, twelve
   independent queues. A pod that gets a big tenant's traffic backs up alone while
   eleven others idle. There is no work stealing because there is no shared queue.

2. **Four workers per pod, hardcoded.** Set in 2025 when this was a different
   service. Postgres will happily take more concurrency than this; we are not
   database-limited, we are worker-limited.

3. **Backoff applies to the whole queue, not the item.** When one write fails —
   usually a `content_hash` conflict, which is a permanent failure, not a transient
   one — the worker backs off. So 41k rows that will *never* succeed are inserting
   exponential delays into a queue of rows that would succeed immediately.

Point 3 is the big one. We are backing off because of the `content_hash` problem I
was already working on, which means the two bugs have been amplifying each other for
two weeks.

## Proposed fix

- Classify failures. Permanent (constraint violation, malformed) → dead-letter table,
  no retry, no backoff. Transient (connection, timeout, deadlock) → retry.
- Per-item backoff, not per-queue.
- Workers configurable, default 16. Measure before going higher.
- Emit queue depth and oldest-item age as metrics. **This does not exist today. There
  is no way to know we are behind except by reading the divergence report, which
  samples 1%.**

Estimate: 5 days.

## Note

The last bullet is AI-4 from the INC-2026-0617 postmortem, assigned to Mei, due 3
July. I am going to need the metric to verify my own fix, so one of us should do it.
I will ask her whose it is. *(I did not ask. Neither of us did it.)*
