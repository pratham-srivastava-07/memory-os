---
doc_id: note_007
type: note
subtype: task_update
title: "Weekly status — week ending 2026-05-22"
author: Priya Raman
date: 2026-05-22
projects: [Arca, API v2]
tickets: [ARCA-212, ARCA-233, ARCA-244, ARCA-301, ARCA-341, API-40, API-58, SEC-44]
tags: [status, task-update, weekly]
---

# Weekly status — week ending 2026-05-22

Posted to `#team-platform` every Friday. Terse on purpose.

## Arca (PRJ-1042)

| Ticket | Owner | State | Note |
|---|---|---|---|
| ARCA-212 | Mei | in review | Benchmark done, readout 28 May |
| ARCA-233 | Daniel | in progress | `arca-ingest` split out, in staging |
| ARCA-244 | Elliot | not started | Chunker, blocked on structured parser output |
| ARCA-301 | Daniel | in progress | Planner rewrite |
| ARCA-341 | Elliot | in progress | Harness at 400 queries, baseline nDCG@10 0.71 |

## API v2 (PRJ-1088)

| Ticket | Owner | State | Note |
|---|---|---|---|
| API-40 | Ava | in progress | Spec draft |
| API-58 | Ava | done | Rate limiting shipped, Northwind override live |

## Security

| Ticket | Owner | State | Note |
|---|---|---|---|
| SEC-44 | Jonas | in progress | Threat model draft, two findings |

## Carried actions not done this week

- p95 alert change (Tomas) — carried from 12 May, now carried twice
- Runbook template (Tomas) — carried from 5 May

## People

Ravi Menon accepted. Starts 15 June. Daniel is his buddy.

## Risks

Three workstreams, four senior engineers. If the datastore evaluation says "migrate",
that is a project with no slack in the current plan.
