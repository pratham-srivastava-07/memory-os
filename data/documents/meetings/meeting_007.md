---
doc_id: meeting_007
type: meeting
title: "Platform Sync — Week 4"
date: 2026-05-26
time: "09:00–09:35 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance]
apologies: [Jonas Weiss]
projects: [Arca, API v2]
tickets: [ARCA-212, ARCA-317, API-52, API-58]
tags: [sync]
---

# Platform Sync — 2026-05-26

Short one. Half the team is heads-down.

- **Mei** — Migration costing done, in the readout doc for Thursday. Headline: eleven
  to fourteen weeks end to end if we do it as a dual-write with backfill, of which
  three weeks are backfill and the rest is everything else. She wants everyone to have
  read it before Thursday and will not present slides.
- **Daniel** — All four services split. `arca-rank` deployed Friday, uneventful.
  Starting ARCA-317, hybrid search, because exact-identifier queries are the top
  complaint he can actually fix this month.
- **Ava** — Writeup is out. She recommends GraphQL internal, REST external. She knows
  Daniel disagrees and has put his objection in the doc verbatim rather than
  paraphrasing it.
- **Tomas** — p95 alert changed. It fired twice on Sunday. Both were real; we have
  been missing our tail latency target for some time and never knew.

  > Priya: What is our target?
  > Tomas: Still two different numbers in two documents. Still nobody's job to fix.

- **Elliot** — Harness at 400 queries. Wants to get to 1,400 across six tenants but
  needs labelling help. Karen volunteered two afternoons.
- **Sofia** — Northwind Retail's rate limit override is live. She has told them the
  v1 shutoff is 1 September so they should plan the v2 move for August.
- **Karen** — Nothing blocking.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Everyone reads the migration readout before Thursday | all | 2026-05-28 |
| 2 | Label 500 more eval queries | Karen | 2026-06-05 |
| 3 | Book API protocol decision meeting | Ava | 2026-06-02 |
