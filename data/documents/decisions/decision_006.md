---
doc_id: decision_006
type: decision
adr_id: ADR-006
title: "Migration strategy: dual-write with backfill, cutover 2026-06-22"
date: 2026-06-10
status: superseded
deciders: [Mei Lin Zhao, Tomas Herrera, Priya Raman]
project: Migration
project_id: PRJ-1103
tickets: [MIG-107, MIG-112, MIG-124, MIG-136]
supersedes: []
superseded_by: [ADR-010]
tags: [migration, postgres, cutover, dual-write]
---

# ADR-006: Migration strategy — dual-write with backfill

## Status

**Timeline superseded by ADR-010, then by ADR-015.** The strategy itself still
stands; only the dates moved.

## Context

ADR-002 chose Postgres. This decides how we get there without downtime. Arca ingests
continuously for 84 tenants and there is no window in which writes stop.

## Decision

Three phases:

1. **Dual write** (MIG-107). `arca-index` writes to Mongo and Postgres in the same
   request. Mongo remains authoritative and its write is the one that can fail the
   request; a Postgres failure is logged and retried asynchronously. Divergence
   sampled hourly into `#proj-migration`.
2. **Backfill** (MIG-112). A resumable job copies history in `tenant_id` order,
   smallest tenants first, checkpointing per tenant. Rate-limited to 3k rows/sec so
   it does not compete with live ingest.
3. **Read cutover** (MIG-136). A per-tenant flag flips reads to Postgres. Roll out
   tenant by tenant, largest last. Dual write stays on for two weeks after the last
   tenant flips, then Mongo is decommissioned (MIG-131).

## Timeline

| Milestone | Date |
|---|---|
| Dual write on in prod | 2026-06-08 |
| Backfill complete | 2026-06-19 |
| Read cutover | 2026-06-22 |
| Dual write off | 2026-07-06 |
| Mongo decommissioned | 2026-07-20 |

## Consequences

- Every write costs two round trips until cutover. Measured at +14 ms p95 on ingest,
  which is inside budget.
- Divergence detection at 1% sampling is a known weak point. Tomas asked for an
  explicit lag metric on the async retry queue and it is in the plan as a follow-up.
- Rollback is cheap right up until dual write is turned off. After that it is a
  restore.

## Alternatives considered

- **Logical replication via a CDC pipeline (Debezium).** More faithful, no
  application change. Rejected: nobody on the team has run Debezium and the Mongo
  oplog connector has a reputation. Mei called it "a second migration to do the first
  migration".
- **Big-bang with a maintenance window.** Rejected. Sofia will not ask design
  partners for a four-hour window during their evaluation.
