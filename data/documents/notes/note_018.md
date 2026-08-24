---
doc_id: note_018
type: note
subtype: task_update
title: "Weekly status — week ending 2026-07-17"
author: Priya Raman
date: 2026-07-17
projects: [Arca, Migration, API v2, Helios]
tickets: [MIG-112, MIG-118, MIG-124, ARCA-288, ARCA-329, ARCA-317, API-52, HEL-31, HEL-33, SEC-51, INFRA-88, INFRA-92]
tags: [status, task-update, weekly]
---

# Weekly status — week ending 2026-07-17

## Migration (PRJ-1103)

| Ticket | Owner | State | Note |
|---|---|---|---|
| MIG-112 | Ravi | **done** | Backfill complete 11 July |
| MIG-118 | Ravi | **done** | Second fix deployed 9 July. Lag 41 min → ~6 min spikes. First attempt (2 July) was rolled back — changed backoff, made burst behaviour worse. |
| MIG-124 | Mei | in review | Cutover runbook, reviewed by Tomas before leave |
| MIG-136 | Mei | not started | Read cutover, 27 July |

Cutover moved to **2026-07-27** (ADR-015). Second slip. Priya's note in the ADR: this
is the last move.

## Arca (PRJ-1042)

| Ticket | Owner | State | Note |
|---|---|---|---|
| ARCA-288 | Elliot | in progress | Reranker → self-hosted L4 per ADR-017 |
| ARCA-317 | Daniel | not started | Hybrid search. Parked since 2 June, picked back up 2 July, still not started |
| ARCA-329 | Mei, Ravi | in progress | Qdrant adapter ~70% |
| INFRA-88 | Tomas | **done** | `qdrant-prod-eu1`, 4 nodes |
| INFRA-92 | Tomas | in progress | L4 nodes |

## API v2 (PRJ-1088)

| Ticket | Owner | State | Note |
|---|---|---|---|
| API-52 | Ava | in review | Six-week spike review 22 July |

## Helios (PRJ-1120)

| Ticket | Owner | State | Note |
|---|---|---|---|
| HEL-31 | Tomas | in progress | Mimir cluster |
| HEL-33 | Tomas | in progress | Trace sampling |

## Security

| Ticket | Owner | State |
|---|---|---|
| SEC-51 | Karen | in progress |

## People

Tomas out from Monday 20 July, back 10 August. Sofia out from 20 July, back 3 August.
Daniel is primary SRE contact for the migration window, Ravi secondary.

## Carried, still not done

- Nightly cross-tenant probe (Jonas) — from ADR-016
- AI-4, dual-write lag alert (Mei) — due 3 July
- AI-7, game day (Tomas) — due 10 July
- GPU node runbook (Daniel)
- `project_arca.md` performance section (Daniel) — due 6 July
