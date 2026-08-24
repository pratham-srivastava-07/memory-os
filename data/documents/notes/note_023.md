---
doc_id: note_023
type: note
subtype: incident_writeup
title: "INC-2026-0729 — writeup"
author: Ravi Menon
date: 2026-07-31
projects: [Migration, Arca]
tickets: [MIG-107, MIG-118, MIG-124]
incidents: [INC-2026-0729]
tags: [incident, dual-write, writeup, missed-action]
---

# INC-2026-0729 — writeup

**Severity:** SEV-3
**Window:** 2026-07-29 11:20 – 12:50 UTC (detected 12:34, mitigated 13:10)
**Impact:** Documents uploaded by `tnt_8842`, `tnt_9017` and one other tenant were
not retrievable for up to 74 minutes after upload. No errors returned. No alerts
fired. Detected by the customer.

## What happened

Northwind Retail ran a bulk upload of about 90,000 documents starting 11:20. The
dual-write async retry queue lagged under the burst, as it does — MIG-118 reduced this
from 41 minutes to roughly 6-minute spikes, and a 90k-document burst is well outside
what MIG-118 was tuned against. Peak lag reached 74 minutes.

Two days earlier this would have been harmless. Reads came from Mongo, Mongo had the
data, the Postgres lag was invisible and did not matter.

Since 2026-07-28 01:20, reads come from Postgres.

## Root cause

ADR-006 specifies:

- Mongo write: synchronous, can fail the request
- Postgres write: asynchronous, fire-and-forget onto a retry queue

That was correct while Mongo was authoritative. The read cutover inverted which store
is authoritative and **nothing inverted the write path**. From 01:20 on the 28th until
13:10 on the 29th — about 36 hours — the authoritative store for reads was the one
sitting behind an async queue with no alerting.

MIG-124, the cutover runbook, has a step for flipping reads. It has no step for the
write path. I read that runbook four times and executed it and did not notice.

## Why nobody knew for 74 minutes

There is no alert on retry queue depth or oldest-item age.

This is AI-4 from the INC-2026-0617 postmortem. Assigned to Mei, due 2026-07-03. It
was also raised in the sync on 2026-06-09, before the postmortem, and again on
2026-06-23. It was in my own MIG-118 writeup on 2026-06-24, where I noted I would need
the metric to verify my fix and that I would ask Mei whose it was. I did not ask.

The metric was written and deployed on 2026-07-30, the day after this incident, and it
took about twenty minutes.

## Mitigation

Inverted the write path at 13:10 on the 29th: Postgres synchronous, Mongo async.
Which is what it should have been from 01:20 on the 28th.

## What I would change

1. Runbooks for a cutover should enumerate every invariant the cutover changes, not
   every action the operator takes. "Reads now come from Postgres" is an action.
   "Postgres is now authoritative" is an invariant, and if we had written the second
   one down, the write path question asks itself.
2. The alert. It is done now.
3. My own note from cutover night lists both of the observations that would have
   caught this — the lag artefact on `tnt_7731`, and that nobody discussed the write
   path. I wrote them at 02:00, filed them, and did not look at them again.

## What I do not think should change

Nobody should feel bad about the 27th. The cutover was executed well and this is a
different failure from a different gap.
