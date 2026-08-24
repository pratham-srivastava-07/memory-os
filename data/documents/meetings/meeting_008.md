---
doc_id: meeting_008
type: meeting
title: "Datastore evaluation readout and recommendation"
date: 2026-05-28
time: "12:00–13:25 UTC"
attendees: [Mei Lin Zhao, Daniel Okoye, Priya Raman, Tomas Herrera, Jonas Weiss, Elliot Vance, Sofia Nyberg]
projects: [Arca, Migration]
tickets: [ARCA-212, MIG-101]
decisions: [ADR-002]
tags: [database, postgres, mongodb, decision, readout]
---

# Datastore evaluation readout — 2026-05-28

Pre-read: ARCA-212 final report, circulated 2026-05-27 05:55 UTC. Everyone confirmed
having read it. Priya cancelled the slide portion.

**Mei:** Recommendation is PostgreSQL 16 as system of record. Three reasons, in
order of how much I believe them.

One, transactional writes across `documents`, `chunks` and `jobs`. This removes a
class of bug, not a percentage of it. Eleven thousand orphans in April becomes zero,
structurally.

Two, we already operate Postgres. One datastore instead of two, one backup story,
one thing to know at 3 a.m.

Three, vector co-location. This is the one I believe least. It is worth 40 to 60 ms
of p95 *if* pgvector holds up at our scale, and I cannot prove it does above 10M
vectors. I want that recorded as a separate decision with its own risk.

**Daniel:** I would put co-location first, not third.

**Mei:** I know. That is why I want it separate — so that if it turns out to be wrong,
we find out that one decision was wrong, not that the migration was wrong.

**Priya:** Do it as two ADRs. What is the cost?

**Mei:** Eleven to fourteen weeks. Dual write, then backfill, then a per-tenant read
cutover. Backfill is three weeks of the total. The rest is schema, application
changes, testing, and the two weeks of dual-write safety net after cutover.

**Tomas:** What breaks if we do nothing?

**Mei:** Nothing breaks. Orphans keep happening, we keep apologising to Lumen Health,
and the hydration hop stays in the p95. It is a "this gets worse slowly" problem.

**Sofia:** Is any of this visible to customers during the migration?

**Mei:** It should not be. Dual write costs about 14 ms on ingest, which is inside
budget. Read cutover is per-tenant and reversible until we turn dual write off.

**Sofia:** Then I do not tell design partners anything, and I would rather not have to.

**Jonas:** Postgres also gets me RLS, which is my answer to SEC-44 finding 1. I want
that noted as a reason even though it is not on Mei's list.

**Priya:** Objections to Postgres? Daniel, this is your moment.

**Daniel:** No objection. I wanted Postgres before the spike and I want it after. My
only note is that if pgvector does not hold, we should not treat that as a failure of
this decision.

**Priya:** Then it is decided. Mei writes ADR-002 tomorrow, vector store gets its own
ADR, and PRJ-1103 is a project with a name. Mei owns it, Tomas is the SRE partner.

**Mei:** I want a second engineer on the backfill. It is not a one-person job for
three weeks.

**Priya:** Ravi starts 15 June. He is yours from the 22nd, once he can find the
bathroom.

## Decisions

- **PostgreSQL 16 is the system of record for Arca.** ADR-002.
- Vector store deferred to a separate ADR.
- PRJ-1103 opened. Owner Mei, SRE partner Tomas.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-002 | Mei | 2026-05-29 |
| 2 | Open PRJ-1103, MIG-101 schema design | Mei | 2026-05-29 |
| 3 | Vector store ADR with recall risk stated | Daniel | 2026-06-05 |
| 4 | RLS design against SEC-44 | Jonas | 2026-06-19 |
