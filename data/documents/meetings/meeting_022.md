---
doc_id: meeting_022
type: meeting
title: "Platform Sync — Week 11"
date: 2026-07-14
time: "09:00–09:50 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Ravi Menon]
apologies: [Jonas Weiss]
projects: [Arca, Migration, API v2]
tickets: [MIG-118, MIG-112, MIG-124, ARCA-329, INFRA-88, API-52]
tags: [sync, migration, slip]
---

# Platform Sync — 2026-07-14

The read cutover was scheduled for yesterday, 13 July. It did not happen. This is the
second time.

## Migration

**Mei** — Rehearsal #2 ran on Sunday against a full copy. Two findings.

The MIG-118 fix is deployed and working — the second attempt, from the 9th. Lag under
the Northwind Retail write pattern is down from 41 minutes to spikes of about six
minutes. That is a twentyfold improvement and it is not zero.

Backfill is complete as of Saturday. The 100% divergence audit is running and is
about half done.

**Priya:** Is six minutes a blocker?

**Mei:** On its own, no. Six minutes of staleness on a flip we can reverse is
survivable. Combined with the second thing, it is.

**Priya:** Which is?

**Mei:** Resourcing. I would rather not go into it in the sync.

**Priya:** Then the answer is that we move the date, and I will write up the reasons
in the ADR. New date is Monday 27 July, 22:00 UTC. Mei, does that work?

**Mei:** It works.

**Priya:** And I want this in the notes, said out loud: this is the last time. If the
27th does not hold we stop the project and re-plan it from scratch rather than moving
it a third time. Two slips is a plan that needs adjusting. Three is a plan that is
not real.

**Sofia:** Anything customer-visible?

**Mei:** Still nothing.

## Round-robin

- **Ravi** — Qdrant adapter (ARCA-329) about 70% done. `qdrant-prod-eu1` provisioned
  Friday, four nodes.
- **Tomas** — INFRA-88 done. Backup runbook written, restore not yet tested. He has
  four working days left before he is out and he is prioritising the cutover runbook
  review over the Qdrant restore test.
- **Elliot** — Reranker costing. ADR-011 doubled the sequence length and CPU rerank
  now does not fit the budget. Two options, Cohere hosted or self-hosted GPU. Note
  going out this week.
- **Ava** — API-52 review is next Wednesday. She will present the numbers and the
  recommendation, and the recommendation is not what she argued for in June.
- **Karen** — Wants a decision on whether she is testing one vector store or two,
  because the matrix doubles.

  > Mei: Two, for now.
  > Karen: Then my matrix doubles and my flake rate doubles with it. I am telling you
  > now so that it is not a surprise in six weeks.

- **Daniel** — ARCA-301 planner rewrite merged. He has not started ARCA-317.
- **Sofia** — Northwind Retail have gone quiet since the technical call, which she
  reads as "waiting to see", not "satisfied".

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-015, cutover moves to 2026-07-27 | Priya | 2026-07-15 |
| 2 | Finish divergence audit | Mei | 2026-07-17 |
| 3 | Test the Qdrant restore | Tomas | 2026-07-17 |
| 4 | Reranker hosting note | Elliot | 2026-07-16 |
