---
doc_id: decision_010
type: decision
adr_id: ADR-010
title: "Read cutover moved from 2026-06-22 to 2026-07-13"
date: 2026-06-26
status: superseded
deciders: [Mei Lin Zhao, Priya Raman, Tomas Herrera, Sofia Nyberg]
project: Migration
project_id: PRJ-1103
tickets: [MIG-112, MIG-118, MIG-136]
supersedes: [ADR-006]
superseded_by: [ADR-015]
tags: [migration, schedule, slip]
---

# ADR-010: Read cutover moved to 2026-07-13

## Status

**Superseded by ADR-015 (2026-07-15),** which moved it again.

## Context

ADR-006 set the read cutover for 2026-06-22. On 2026-06-25 the go/no-go returned
no-go. Two blockers:

1. **MIG-118.** The dual-write async retry queue falls behind during large-tenant
   ingest. Measured lag on 2026-06-24 was 41 minutes at peak on `tnt_8842`. Cutting
   reads over with a 41-minute lag means serving stale documents.
2. **Backfill is 62% complete,** not the 100% ADR-006 assumed. The `content_hash`
   uniqueness violations (41k rows) stalled it for four days while Ravi worked out
   whether the duplicates were real duplicates. They mostly were.

## Decision

Move the read cutover to **2026-07-13**. Three weeks, not one, because:

- MIG-118 needs a real fix, not a bigger queue. Ravi estimated 5 days.
- Backfill needs to finish and then needs a full divergence audit at 100% sampling,
  not 1%. Mei estimated 4 days of wall clock for the audit on 60M rows.
- We wanted slack. ADR-006's timeline had none and that is why we are here.

## Consequences

- Dual write runs three weeks longer. Ingest p95 stays elevated by 14 ms.
- Mongo decommission moves to 2026-08-10, which is after the Datadog renewal
  conversation, so the Helios cost model needs updating.
- Sofia tells design partners nothing, because nothing customer-visible changed.
