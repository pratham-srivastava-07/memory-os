---
doc_id: meeting_004
type: meeting
title: "Datastore options workshop — Postgres, MongoDB, CockroachDB"
date: 2026-05-14
time: "12:00–13:30 UTC"
attendees: [Mei Lin Zhao, Daniel Okoye, Tomas Herrera, Priya Raman, Elliot Vance, Jonas Weiss]
apologies: [Ava Duarte]
projects: [Arca, Migration]
tickets: [ARCA-212]
tags: [database, postgres, mongodb, cockroachdb, evaluation, workshop]
---

# Datastore options workshop — 2026-05-14

Pre-read: Mei's ARCA-212 benchmark writeup, circulated 2026-05-13 06:40 UTC.
This session is for discussion, not decision. Priya was explicit that no decision
would be taken today.

**Mei:** The numbers first, then the argument. Same hardware, 5M chunks, 84 synthetic
tenants shaped like real ones.

| | Postgres 16 | MongoDB 7 | CockroachDB 24.1 |
|---|---|---|---|
| Chunk insert/sec (batched) | 11,000 | 18,000 | 6,400 |
| Hydration p95 (200 ids) | 6 ms | 41 ms | 14 ms |
| Cross-collection txn | yes | needs replset change | yes |
| Vector index | pgvector | Atlas Search only | none |
| Team operational experience | high | low | none |

**Daniel:** The hydration number is the whole argument. Forty-one milliseconds on
every single query, purely because the vectors and the rows are in different systems.

**Mei:** Careful. The 6 ms is Postgres hydrating rows that are already in the buffer
cache because the vector scan just touched them. That is only true if the vectors are
*in* Postgres. If we put metadata in Postgres and keep vectors elsewhere, it is not
6 ms, it is a network hop and it looks like the Mongo number.

**Daniel:** So the vector store decision and this decision are coupled.

**Mei:** They are coupled. They are not the same decision, and I want them written up
separately, because the reasons are different and I think one of them is much more
likely to be wrong than the other.

**Priya:** Which one is more likely to be wrong?

**Mei:** The vector one. Postgres for metadata is a boring, well-understood choice.
pgvector at 60M vectors is not something I can find a credible public benchmark for.
I would take the metadata decision now and treat the vector decision as provisional.

**Tomas:** Operationally I have run Postgres for eleven years. I have never done a
Mongo shard rebalance and I do not want to learn during an incident. That is not a
technical argument but it is a real one at three-person-on-call.

**Daniel:** What about Cockroach? I raised it.

**Mei:** Genuinely good. Multi-region story is better than Postgres if we ever need
it, and we might in 2027. Two problems: no vector index at all, so we would be
running a separate vector store forever, and the licensing conversation is longer
than the migration.

**Jonas:** Postgres gives us row-level security. That is directly relevant to SEC-44 —
it turns "somebody forgot a WHERE clause" from a breach into zero rows. Mongo has
nothing equivalent that works at the collection level for us.

**Elliot:** Does Mongo win anything?

**Mei:** Write throughput, 18k against 11k. That is the one place it is clearly
better and it is not close.

**Tomas:** What is our actual peak?

**Mei:** 2,300 a second sustained, and we batch. So we go from about eight times
headroom to about five times. I would want an alert at 60% of measured ceiling.

**Priya:** What would change your mind between now and the readout?

**Mei:** If the backfill estimate comes back at more than six weeks. The migration
cost is the real cost here, not the steady state. I have not costed it yet.

**Priya:** Cost it. Readout on the 28th, decision after that. Daniel, hold your
opinions in the doc, not in the corridor.

## Not decided

Nothing. This was a discussion. The recommendation forms in the 2026-05-28 readout
and the decision is ADR-002.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Cost the migration itself, not just steady state | Mei | 2026-05-28 |
| 2 | Write vector store question up separately | Mei | 2026-05-28 |
| 3 | Confirm whether RLS meets SEC-44 | Jonas | 2026-05-28 |
