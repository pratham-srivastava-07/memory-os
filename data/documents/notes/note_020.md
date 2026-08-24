---
doc_id: note_020
type: note
subtype: runbook
title: "Tenant migration runbook — pgvector to Qdrant"
author: Ravi Menon
date: 2026-07-19
projects: [Arca]
tickets: [ARCA-329, INFRA-88]
tags: [runbook, qdrant, migration, operations]
---

# Tenant migration runbook — pgvector → Qdrant

Written for `tnt_8842` and then generalised. Per ADR-014 this applies to tenants over
2M vectors; in practice it is the runbook for moving any tenant and I expect to run it
a lot, because the threshold is a treadmill.

## Preconditions

- [ ] Qdrant collection exists for the tenant, correct dimensionality (1024) and
      distance (cosine)
- [ ] `qdrant-prod-eu1` has headroom: check disk and RAM, quantized index is roughly
      0.28 bytes/dim/vector plus payload
- [ ] Tenant's `chunker_version` is recorded. **Do not migrate a tenant mid-reindex.**
- [ ] Backup taken of the Qdrant collection if it exists (empty is fine, take it
      anyway so restore is rehearsed)

## Steps

1. **Snapshot the source.** Record `SELECT count(*) FROM arca.chunks WHERE
   tenant_id = $1`. This is the number everything is checked against.

2. **Bulk copy.** `arca-index` has a `--migrate-vectors` mode. Batches of 1,000,
   ordered by `chunk_id` so it is resumable from the last committed id. Roughly
   14 minutes per million vectors observed on `tnt_8842`.

3. **Dual read verification.** Set the tenant's `vector_store` flag to `both`. Every
   query goes to pgvector and Qdrant; pgvector's result is served, Qdrant's is
   compared and logged. Run for at least 2 hours of real traffic.
   - Acceptance: overlap@10 above 0.93 between the two stores. It will not be 1.0 and
     it should not be — Qdrant's recall is *better*, so disagreements are mostly
     Qdrant finding things pgvector missed. Spot check the disagreements; do not just
     read the number.

4. **Flip.** Set `vector_store` to `qdrant`. This is a config change, no deploy.

5. **Watch.** 30 minutes. Error rate, p95, and the eval harness on that tenant's query
   subset if one exists.

6. **Do not delete anything.** The pgvector rows stay. Per ADR-019 they stay until
   2026-09-30.

## Rollback

Set `vector_store` back to `pgvector`. That is the entire rollback. It is a config
flag and it takes effect on the next request. This is the reason step 6 exists.

## Observed on tnt_8842 (2026-07-17)

- 8.1M vectors, copy took 1 h 54 m
- Dual read ran 3 hours, overlap@10 was 0.91 — below my threshold. Investigated: the
  disagreements were all cases where Qdrant returned a relevant document pgvector had
  missed. Elliot confirmed against ground truth. Proceeded.
- Post-flip nDCG@10 on their saved queries: 0.79, up from 0.58.
- p95 went from 71 ms to 26 ms on candidate generation, and end-to-end went *up* by
  about 40 ms because hydration is a separate round trip again. Net win, but worth
  knowing the shape of it.

## Note on ARCA-317

I have picked up hybrid search. It is listed as Daniel's in the 2 July architecture
review notes and unassigned in `project_arca.md`. It is mine; Daniel is holding the
SRE role while Tomas is out. Somebody should fix the project doc.
