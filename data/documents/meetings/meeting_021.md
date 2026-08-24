---
doc_id: meeting_021
type: meeting
title: "Vector store bake-off — pgvector vs Qdrant"
date: 2026-07-09
time: "12:00–13:20 UTC"
attendees: [Mei Lin Zhao, Elliot Vance, Daniel Okoye, Tomas Herrera, Priya Raman, Ravi Menon, Sofia Nyberg]
projects: [Arca]
tickets: [ARCA-329, INFRA-88]
decisions: [ADR-014]
tags: [vector-search, qdrant, pgvector, decision, bake-off]
---

# Vector store bake-off — 2026-07-09

Pre-read: Mei's recall benchmark, 2026-07-06. Elliot's Qdrant comparison, 2026-07-08.

**Mei:** The numbers are in the pre-read. Short version: pgvector recall collapses
above roughly six million vectors in one index and we cannot buy it back inside our
latency budget. Qdrant holds 0.96 at eight million with p95 24 ms on a four-node
cluster with scalar quantization.

**Daniel:** I want to make the argument against and then vote for it anyway, because
I think somebody should say it out loud.

We chose Postgres partly because vectors and rows in one place removes a network hop
worth 40 to 60 ms. Six weeks later we are proposing to put the vectors somewhere
else. That reintroduces the hop, for the largest tenants, who are the ones who care
most about latency. We will have done a migration and kept the thing the migration
was supposed to fix.

**Mei:** That is fair and it is why I want it in the ADR in those words.

**Daniel:** The other two reasons in ADR-002 still hold. Transactions and one fewer
datastore to operate. The migration is still right. This specific argument for it was
wrong.

**Priya:** Options.

**Mei:** Three. Everything on Qdrant. Everything stays on pgvector and we tell
Northwind Retail to live with it, which is not an option. Or a split: large tenants on
Qdrant, small tenants stay on pgvector where co-location is real and recall is fine.

**Elliot:** I would do everything on Qdrant. A split means two recall behaviours and
my eval results stop being comparable across tenants.

**Mei:** And moving all eighty-four tenants two weeks before a cutover is how we get a
second incident. The split is the smaller change.

**Tomas:** I have not run Qdrant. I need a backup and restore runbook before a single
tenant is routed to it, and I need to have tested a restore.

**Priya:** Where is the line?

**Mei:** Two million vectors. I picked it because it is comfortably below where the
curve moves. It is arbitrary and it will be wrong.

**Ravi:** Wrong in which direction?

**Mei:** Tenants grow across it. Somebody has to move them, one at a time, by hand.

**Ravi:** That is me, isn't it.

**Mei:** That is you.

**Sofia:** How long until the escalation is fixed?

**Mei:** Northwind Retail can be on Qdrant in about ten days if INFRA-88 lands.

**Priya:** Do the split. Write down Daniel's argument in full, write down that the
threshold is arbitrary, and open ARCA-329 properly.

## Decision

Qdrant for tenants above 2M vectors, pgvector below. ADR-014. `qdrant-prod-eu1`,
four nodes, INFRA-88.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-014 including Daniel's objection verbatim | Mei | 2026-07-10 |
| 2 | Provision `qdrant-prod-eu1` (INFRA-88) | Tomas | 2026-07-16 |
| 3 | Qdrant backup/restore runbook, tested | Tomas | 2026-07-17 |
| 4 | ARCA-329 adapter implementation | Mei, Ravi | 2026-07-20 |
| 5 | Move `tnt_8842` to Qdrant | Ravi | 2026-07-21 |
