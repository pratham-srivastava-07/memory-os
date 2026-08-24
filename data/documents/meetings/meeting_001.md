---
doc_id: meeting_001
type: meeting
title: "Platform Sync — Week 1"
date: 2026-05-05
time: "09:00–09:45 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance]
apologies: [Jonas Weiss]
projects: [Arca, API v2]
tickets: [ARCA-233, ARCA-244, ARCA-301, API-40]
tags: [sync, mongodb, arca, kickoff]
---

# Platform Sync — 2026-05-05

Notes by Priya. Format is round-robin, five minutes each, blockers first.

## Round-robin

**Daniel** — Arca is one deploy and it is starting to hurt. Last Thursday's ingest
burst from Calder Freight (`tnt_9017`) pushed retrieval p95 from 240 ms to 640 ms for
about eleven minutes. Wants to propose a split into separate services. Will write it
up as a pre-read for Thursday's architecture review.

**Mei** — April reconciler numbers are in. 11,400 orphaned chunk records for the
month, meaning chunks whose parent document write failed. Every one of them is a
document a customer thinks they uploaded and cannot find. Lumen Health (`tnt_7731`)
filed a support ticket about exactly this on 24 April and we told them it was a
"transient indexing delay", which was not true.

> Priya: Is this a Mongo problem or an us problem?
> Mei: Both. We do three collection writes with no transaction. Mongo can do
> multi-document transactions but not with our replica set config. We could fix the
> config, or we could ask whether Mongo is the right store at all.
> Daniel: We should be looking at PostgreSQL. We already run it for the control plane.
> Priya: Then look at it properly. Spike it, do not decide it in a sync.

Mei to open a spike ticket. Timebox two weeks.

**Tomas** — On-call was quiet. One page, disk on `mongo-arca-01` secondary, resolved
by the runbook. He wants every new service to arrive with a runbook or it does not
get an alert. Nobody argued.

**Ava** — Starting the v2 API design. The console makes nine calls to render document
detail; median customer sees 1.4 s to first paint. Talking to design partners this
week: Northwind Retail, Calder Freight, Lumen Health.

**Elliot** — Asked what our chunk size is and why. Daniel said 512 with 64 overlap.
Elliot asked why 512. Nobody knew. He is going to build an eval harness so that this
class of question has an answer.

**Karen** — Migrating the last Cypress suites to Playwright. Two weeks. Please stop
opening Cypress PRs.

**Sofia** — Northwind Retail is the pilot that matters this quarter. They are at
3.1M chunks and uploading hard. If retrieval quality degrades as they grow, we lose
the reference customer.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write up Arca service split as a pre-read | Daniel | 2026-05-06 |
| 2 | Open datastore evaluation spike, two-week timebox | Mei | 2026-05-06 |
| 3 | Runbook template in the handbook | Tomas | 2026-05-12 |
| 4 | Design partner interviews for API v2 | Ava | 2026-05-15 |
