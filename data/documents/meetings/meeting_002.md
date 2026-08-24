---
doc_id: meeting_002
type: meeting
title: "Arca Architecture Review #1 — service decomposition"
date: 2026-05-07
time: "12:00–13:05 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Priya Raman, Tomas Herrera, Mei Lin Zhao, Elliot Vance, Karen Oyelaran]
apologies: [Ava Duarte, Sofia Nyberg]
projects: [Arca]
tickets: [ARCA-233, ARCA-301]
decisions: [ADR-001]
tags: [architecture, services, review]
---

# Arca Architecture Review #1 — 2026-05-07

Pre-read: Daniel's "Arca as four services" doc, circulated 2026-05-06 08:12 UTC.
Priya confirmed she had read it and had comments in the doc before 10:00.

**Priya:** Everyone read it? Mei, it is 20:00 for you, we will keep this to an hour.

**Mei:** I read it. One comment before we start: the doc says "the datastore stays as
is". I want that to be explicitly out of scope today, not implicitly settled. The
spike I opened yesterday might change it.

**Daniel:** Agreed, out of scope. The split does not depend on which store we use.

**Daniel:** Four services. Ingest, index, retrieve, rank. The line I care about is
between ingest and retrieve, because that is where the pain is — a big upload eats
CPU and retrieval latency goes with it. The other two lines are speculative.

**Tomas:** Speculative how?

**Daniel:** Rank is its own service because if we ever want a GPU for the reranker I
do not want that constraint on the whole read path. Index is its own service because
it holds the embedding model in memory and I do not want a 4 GB resident model in the
process that serves queries.

**Elliot:** Both of those become true within the quarter, not speculatively. The
reranker is the thing that is going to want a GPU.

**Tomas:** Four services means four sets of dashboards, four runbooks, four alert
routes. I will do it, but I want the runbooks written as the services are split, not
after. My experience of "we will document it later" is that later is an incident.

**Priya:** Put it in the ADR as a consequence with your name on it.

**Karen:** Test story? Right now integration tests run against one process. Four
processes means either I mock three of them or I run all four in CI.

**Daniel:** Run all four. They are small. Compose file.

**Karen:** Then I want that compose file to be the same one people run locally, not a
separate CI-only thing that rots.

**Mei:** The part that worries me is `arca-core`. If the domain types are a shared
library across four deploys, we get version skew. Service A writes a chunk record
with a field service B does not know about.

**Daniel:** Additive-only changes, and the library version is pinned per service.

**Mei:** That is a policy, not a mechanism. It will be violated. I am not blocking on
it, I want it written down as a known risk.

**Priya:** Written down. Anything that blocks?

*(nothing)*

**Priya:** Then it is decided. Daniel writes ADR-001 by tomorrow. Mei, when does your
spike report?

**Mei:** Two weeks. I would like a session on it rather than a sync slot. It is not a
five-minute update.

**Priya:** Book the 14th, Thursday. That is the slot the architecture review would
have had anyway.

## Decision

Arca splits into `arca-ingest`, `arca-index`, `arca-retrieve`, `arca-rank`.
Datastore explicitly out of scope. Recorded as ADR-001.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-001 | Daniel | 2026-05-08 |
| 2 | Runbook per service, as each is split out | Tomas | ongoing |
| 3 | Single compose file for local + CI | Karen | 2026-05-22 |
| 4 | Datastore options session, book 2026-05-14 | Mei | 2026-05-08 |
