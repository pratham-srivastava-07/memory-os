---
doc_id: meeting_015
type: meeting
title: "Postmortem — INC-2026-0617 arca-retrieve degradation"
date: 2026-06-19
time: "13:00–14:20 UTC"
attendees: [Tomas Herrera, Daniel Okoye, Priya Raman, Mei Lin Zhao, Elliot Vance, Ravi Menon, Karen Oyelaran, Sofia Nyberg]
apologies: [Ava Duarte, Jonas Weiss]
projects: [Arca, Migration]
tickets: [ARCA-301, ARCA-288, MIG-118, OPS-19]
incidents: [INC-2026-0617]
decisions: [ADR-009]
tags: [postmortem, incident, blameless, actions]
---

# Postmortem — INC-2026-0617

**Severity:** SEV-2
**Duration:** 2026-06-17 16:40 – 19:35 UTC (2h 55m)
**Impact:** `/v1/retrieve` error rate peaked at 34% in `arca-prod-eu1`. 61 tenants
affected. Northwind Retail, Calder Freight and Lumen Health all saw failures.
**Facilitator:** Priya. Blameless. Tomas wrote the timeline.

## Timeline (UTC)

| Time | Event |
|---|---|
| 16:40 | `arca-retrieve` v2026.06.17.3 deployed to eu1. Change: candidate generation limit raised from 100 to 400 (ARCA-301). |
| 16:41–17:05 | Latency climbs steadily. p95 goes 310 ms → 2.1 s. No alert; the p95 alert threshold is 800 ms with a 15-minute window. |
| 17:00 | Deploy author logs off for the day. |
| 17:08 | First customer report, Calder Freight, into the shared channel. |
| 17:12 | Tomas paged by error-rate alert. |
| 17:12–17:52 | Tomas investigating. No indication in the alert of a recent deploy. Time spent reading `git log` across four service repos. |
| 17:52 | Deploy identified as probable cause. |
| 18:05 | Rollback started. |
| 18:20 | Rollback complete. Error rate falls but does not recover — `arca-rank` request queue is saturated and draining. |
| 19:35 | Queue drained, error rate normal. Incident closed. |
| 2026-06-18 09:10 | Mei notices the dual-write retry queue had backed up to 90 minutes of lag during the incident and drained overnight. Nobody had been alerted. Not customer-visible, but we did not know. |

## What happened

ARCA-301 raised the candidate generation limit from 100 to 400 to improve recall on
long queries. Each candidate goes through `arca-rank`, which runs a cross-encoder on
CPU. Four times the candidates is four times the rerank work. `arca-rank` saturated,
its request queue grew unbounded, and `arca-retrieve` requests timed out waiting.

The change was tested in staging, where the query mix is synthetic and the candidate
count rarely exceeded 100 in practice, so the fan-out never materialised.

## Contributing factors

1. **No load shedding in `arca-rank`.** The queue is unbounded. It should reject when
   the wait exceeds the caller's remaining budget.
2. **The alert did not carry deploy context.** Forty minutes of a 175-minute incident
   was spent identifying what changed.
3. **`arca-rank` has no runbook.** Action from 2026-06-09, not done. Tomas had to
   reason from first principles about a service he has never operated.
4. **Author unreachable.** Deployed at 16:40, logged off at 17:00.
5. **Staging query mix is not representative.** Karen: "we test that it works, not
   that it works under our traffic."
6. **The dual-write lag was invisible.** The 1% divergence sample did not surface a
   90-minute backlog. This was raised on 2026-06-09 and not actioned.

## What went well

- Rollback was clean and took 15 minutes.
- Sofia had customer comms out within 20 minutes of being told.

## Discussion

**Daniel:** The load shedding is the real fix. Everything else is a mitigation.

**Tomas:** The load shedding is the fix for this incident. The deploy context in
alerts is the fix for the next four incidents.

**Ravi:** The policy I mentioned yesterday — deploy and stay reachable for an hour.

**Priya:** Taking that, plus a Thursday afternoon and Friday freeze. Daniel has been
refusing Friday deploys unilaterally for a year and it may as well be policy.

**Elliot:** And my question from yesterday. What does this failure look like after
cutover, when Postgres is the primary and it is also holding the vector index?

**Mei:** Worse, probably. The rerank saturation would be the same, but a retry storm
against Postgres also degrades ingest, which is not true today because ingest writes
to Mongo. We should game-day it.

**Priya:** Before or after cutover?

**Mei:** Before. It is a reason to not cut over on the 22nd, which we were probably
not going to do anyway.

## Action items

| ID | Action | Owner | Due | Status |
|---|---|---|---|---|
| AI-1 | Bounded queue and deadline-aware load shedding in `arca-rank` | Daniel | 2026-07-03 | open |
| AI-2 | Deploy annotations on retrieval dashboards and in alert payloads | Tomas | 2026-06-30 | open |
| AI-3 | `arca-rank` runbook (carried from 2026-06-09) | Daniel | 2026-06-26 | open |
| AI-4 | Explicit lag metric and alert on the dual-write retry queue | Mei | 2026-07-03 | open |
| AI-5 | Deploy policy: Thursday 15:00 UTC cutoff, no Friday deploys, author reachable 60 min | Priya | 2026-06-22 | open |
| AI-6 | Replay production query mix against staging before ranking changes | Karen | 2026-07-10 | open |
| AI-7 | Game day: Postgres-primary failure mode, before cutover | Tomas | 2026-07-10 | open |

