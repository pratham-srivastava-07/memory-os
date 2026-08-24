---
doc_id: meeting_029
type: meeting
title: "Platform Sync — Week 14"
date: 2026-08-04
time: "09:00–09:50 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Ravi Menon, Jonas Weiss]
apologies: [Tomas Herrera]
projects: [Arca, Migration, API v2]
tickets: [MIG-131, ARCA-317, ARCA-329, API-71, API-77, SEC-51]
tags: [sync, postmortem-actions, qdrant]
---

# Platform Sync — 2026-08-04

New format. Open postmortem actions first, per last Thursday.

## Open postmortem actions

| ID | Action | Owner | Due | Status |
|---|---|---|---|---|
| AI-4 | Dual-write retry lag alert | Mei | 2026-07-03 | **done 2026-07-30** |
| AI-7 | Game day: Postgres-primary failure mode | Tomas | 2026-07-10 | open, blocked on Tomas |
| — | Nightly cross-tenant probe (ADR-016) | Jonas | 2026-07-31 | open |
| — | GPU node runbook | Daniel | 2026-08-07 | in progress |

**Priya:** AI-7 was due before the cutover and the cutover has happened. It is now a
different exercise. Tomas is back on the 10th; it gets re-scoped then, not quietly
dropped.

## Round-robin

**Mei** — Dual write comes off on the 10th, Mongo decommission on the 14th. She wants
to raise the vector store split before the reindex, because doing a reindex twice
would be foolish.

> Mei: We have nine tenants on Qdrant and seventy-five on pgvector. The nine are 71%
> of query volume and 88% of vectors. Three tenants crossed the 2M threshold in July
> and Ravi moved them by hand. And after the 800-token reindex, two of the nine drop
> back under the threshold.
> Ravi: I am not moving them back.
> Mei: Nobody is moving them back. That is my point. The threshold is a treadmill.
> Karen: And it is where most of my flakes come from. Two code paths, two behaviours.
> Priya: What is the ask?
> Mei: A session Wednesday. Consolidate on Qdrant, reindex once, delete the pgvector
> path.
> Daniel: I will argue for it, which should tell you something.

**Ravi** — ARCA-317 merged Friday. Exact-identifier queries went from 0.12 to 0.71
nDCG@10 on Elliot's subset. Northwind Retail's other complaint is closed.

**Elliot** — He wants the harness in CI. Three big decisions this quarter turned on a
benchmark someone ran once by hand in a notebook, and one of them (ADR-011) shipped a
consequence he did not connect until Tomas raised the latency budget.

**Ava** — Expansion parameters done for two of three screens. On track for the 7th.

**Sofia** — Back. Confirms 1 November for the v1 shutoff, in writing, and she is
unhappy that the date moved twice inside project docs before anyone told her.

> Sofia: `project_api.md` said 1 September on the day I told a customer 1 September.
> It still says 1 September. I read the document and the document was wrong.
> Priya: The document is wrong because ADR-018 changed it and nobody edited the
> document. That is on us, and specifically it is on whoever writes the ADR.
> Ava: Me. I will fix it today.

**Jonas** — SEC-51 CI check is live and has already blocked one PR. Probe job still
not started; he is at 50% and it keeps losing.

**Karen** — Flake rate on the retrieval suite is 6%, almost all in the two-vector-store
matrix.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Vector store consolidation session | Mei | 2026-08-05 |
| 2 | Update `project_api.md` deprecation dates | Ava | 2026-08-04 |
| 3 | Proposal: eval harness in CI | Elliot | 2026-08-06 |
| 4 | Re-scope AI-7 when Tomas returns | Priya | 2026-08-10 |
