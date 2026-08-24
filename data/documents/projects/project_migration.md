---
doc_id: project_migration
type: project_doc
title: "Project Migration — MongoDB to PostgreSQL"
project: Migration
project_id: PRJ-1103
status: active
owner: Mei Lin Zhao
created: 2026-05-29
last_updated: 2026-07-16
tags: [migration, postgres, mongodb, living-doc]
---

# Project Migration (PRJ-1103)

Move the Arca document metadata and chunk records from MongoDB to PostgreSQL 16.
Driver, target state and rejected alternatives are in ADR-002. Strategy is in ADR-006.

Owner: Mei Lin Zhao. SRE partner: Tomas Herrera. Backfill and dual-write:
Ravi Menon (from 2026-06-22).

## Why

Short version, long version in ADR-002:

1. Cross-collection consistency. `documents` and `chunks` drift under partial ingest
   failures and we have no transaction to lean on.
2. We already run Postgres for the control plane, so this removes a datastore rather
   than adding one.
3. pgvector puts vectors next to the metadata, which kills the two-phase
   search-then-hydrate pattern in `arca-retrieve`.

Reason 3 has since been undermined — see ADR-014 and ADR-019.

## Target schema

MIG-101. Four tables in schema `arca`:

```sql
arca.documents   (document_id uuid pk, tenant_id uuid, source_uri text,
                  content_hash bytea, created_at timestamptz, ...)
arca.chunks      (chunk_id uuid pk, document_id uuid fk, tenant_id uuid,
                  ordinal int, token_count int, embedding vector(1024), ...)
arca.jobs        (job_id uuid pk, tenant_id uuid, state text, ...)
arca.tenants     (tenant_id uuid pk, name text, plan text, ...)
```

`arca.chunks` is hash-partitioned on `tenant_id`, 32 partitions. Row-level security
is enabled on all four (ADR-008), though ADR-016 narrowed where we rely on it.

Primary is `pg-arca-primary-01` (32 vCPU, 256 GB, gp3 8000 IOPS), two read replicas
per region.

## Approach

Three phases, per ADR-006:

1. **Dual write** (MIG-107) — every write goes to Mongo and Postgres. Mongo stays
   authoritative. Divergence is reported to `#proj-migration` hourly.
2. **Backfill** (MIG-112) — historical documents copied in `tenant_id` order,
   smallest tenants first. Resumable, checkpointed per tenant.
3. **Cutover** (MIG-124) — reads flip to Postgres (MIG-136), dual write stays on for
   two weeks as an escape hatch, then Mongo is decommissioned (MIG-131).

## Timeline

*Reviewed 2026-07-16.*

| Milestone | Original | Current |
|---|---|---|
| Dual write on in prod | 2026-06-08 | 2026-06-08 (done) |
| Backfill complete | 2026-06-19 | 2026-07-24 |
| Read cutover | 2026-06-22 | 2026-07-27 |
| Dual write off | 2026-07-06 | 2026-08-10 |
| Mongo decommissioned | 2026-07-20 | 2026-08-21 |

Slip history: ADR-010 moved the cutover from 2026-06-22 to 2026-07-13. ADR-015 moved
it again to 2026-07-27.

## Risks

- **Backfill lag under write load.** MIG-118. The dual-write path falls behind during
  large tenant ingests and the divergence report only samples 1%, so we find out late.
- **`content_hash` collisions.** Mongo allowed duplicate `content_hash` per tenant;
  the Postgres schema has a unique constraint. Ravi found 41k affected rows.
- **Vector column size.** `arca.chunks.embedding` at 1024 dims is about 4 KB per row
  before TOAST. At 60M chunks that is a lot of heap we did not budget for.
