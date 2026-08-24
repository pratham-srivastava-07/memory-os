---
doc_id: note_022
type: note
subtype: task_update
title: "Cutover night log"
author: Ravi Menon
date: 2026-07-28
projects: [Migration]
tickets: [MIG-136, MIG-124]
tags: [cutover, log, migration, operations]
---

# Cutover night log — 2026-07-27/28

Posted to `#proj-migration`. Times UTC. Mei ran it, I executed, Daniel on call, Karen
and Elliot verifying. Mei's local time was 06:00 to 09:40 Tuesday; she had been up
since 05:30 and went offline immediately after.

```
21:40  Everyone in the call. Pre-flight checklist from MIG-124.
21:52  Backfill: complete. Divergence audit: zero unexplained. Replica lag: 200ms.
       Qdrant: healthy. Error budget: 31% consumed this month, fine.
22:00  Window open.
22:04  Batch 1. 40 tenants, all under 50k chunks.
       Per-tenant: assert -> flip -> assert at 5 min. Karen's tooling, automated,
       Ravi confirming each one by hand because it is night one.
22:31  Batch 1 done. 40/40. Zero divergence pre and post. Error rate flat.
23:10  Batch 2. 30 tenants, 50k to 1M.
23:18  tnt_7731 (Lumen Health) FAILED pre-flight assertion. 12 rows differ.
       Held back, continuing with the other 29.
23:24  Batch 2 done except tnt_7731.
23:25  tnt_7731 investigation. The 12 rows are documents deleted between the
       overnight audit and now. Deletes propagate to Postgres via the same async
       path. They are correctly absent in Mongo and present-but-tombstoned in
       Postgres. Not divergence, a lag artefact.
23:31  Re-ran assertion for tnt_7731. Clean. Flipped. Post-assert clean.
00:05  Batch 3. 13 tenants, 1M to 5M.
00:34  Batch 3 done.
00:40  tnt_8842 (Northwind Retail) alone. 8.4M chunks. Assert took 4m10s.
00:45  Flipped. Watching.
01:15  30 minutes on tnt_8842. p95 311ms. Error rate 0.04%. Elliot: nDCG on their
       saved query subset unchanged from pre-flip.
01:20  All 84 tenants reading from Postgres.
01:25  Elliot's harness against production traffic samples: 0.78 before, 0.78 after.
01:40  Window closed. Nobody touches anything until the sync.
```

## Numbers

- 84 tenants, 84 flipped, 0 rolled back
- One held back and resolved in 13 minutes
- Error rate never exceeded 0.09%
- p95 first eight hours: 268 ms against a 400 ms budget, better than the 341 ms we
  were running on Mongo

## Things I noticed and did not act on

- The `tnt_7731` failure was a *lag artefact*. The async path was 6 minutes behind at
  23:18. We treated it as a false positive, which it was, and moved on.
- Nobody said anything about the write path during the whole window. The runbook has a
  step for flipping reads and no step for anything else.

*(Both of the above are the incident on the 29th. I wrote them down at 02:00 and did
not think about them again until Ravi — me — was paged about it 34 hours later.)*
