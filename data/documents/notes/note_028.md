---
doc_id: note_028
type: note
subtype: audit
title: "Project doc audit against current ADRs"
author: Ravi Menon
date: 2026-08-14
projects: [Arca, API v2, Migration, Helios]
tickets: [ARCA-317]
tags: [audit, documentation, staleness, contradictions]
---

# Project doc audit

Action 3 from the 2026-08-06 retro. I read the four project docs against every ADR
and wrote down where they disagree. I have not fixed anything yet — I want owners to
confirm before I edit documents I do not own.

## project_arca.md

| Section | Says | Should say | Source |
|---|---|---|---|
| Performance targets | p95 300 ms | p95 400 ms, with sub-budgets | ADR-012, 3 July |
| Chunking | 512 tokens, 64 overlap | Structure-aware, target 800, 15% overlap | ADR-011, 1 July |
| Vector storage | pgvector HNSW in the primary cluster | Qdrant, all tenants | ADR-019, 5 Aug |
| Data layer | "MongoDB is the system of record" | Postgres. Mongo decommissioned today | ADR-002, cutover 27 July |
| Open workstreams | ARCA-317 unassigned | ARCA-317 is mine, merged 31 July | — |
| Services table | Ingest owner Ravi Menon | correct | — |

The data layer section is the worst one. It carries a review date of 12 May and a note
from Mei saying "we are actively evaluating a move off Mongo". Anyone reading that
document today would conclude we are on MongoDB.

## project_api.md

| Section | Says | Should say | Source |
|---|---|---|---|
| Protocol | GraphQL internal, REST external | REST only, `expand` for composition | ADR-018, 22 July |
| v1 deprecation | v1 shut off 2026-09-01 | 2026-11-01 | ADR-018 |
| Open tickets | API-52 in progress | closed, won't-do | ADR-018 |

Ava said on 4 August she would fix the dates that day. As of today the file still says
1 September. Sofia quoted 1 September to a customer from this document in June.

## project_migration.md

| Section | Says | Should say |
|---|---|---|
| Timeline: Mongo decommissioned | 2026-08-21 | 2026-08-14 (today) |
| Timeline: dual write off | 2026-08-10 | correct, done |
| Risks: MIG-118 | described as open | fixed 9 July, though the underlying burst behaviour caused INC-2026-0729 |
| Why, reason 3 | already annotated as undermined | correct, and ADR-019 makes it final |

Credit where due: this is the only doc that annotated its own obsolete reasoning
rather than leaving it standing.

## project_helios.md

Accurate. It says paused, it says why, it says what survives. It is also the only doc
nobody has needed to change since it was written, which is what being paused means.

## Things I could not resolve

- **The 2M vector threshold** appears in ADR-014 and in my own runbook (note_020).
  ADR-019 makes it obsolete but the runbook still opens by referencing it. Mine to fix.
- **`tnt_8842` chunk count** appears as 6.2M (Sofia, 29 June), 8.1M (Mei, 6 July),
  8.4M (cutover log, 28 July). All three were correct on their date. I do not think
  this is a bug, but anything that reads these documents without dates will average
  three true numbers into one false one.
- **AI-7, the game-day** — I cannot tell from any document whether this is still
  intended to happen. It was due 10 July, marked "blocked on Tomas" on 4 August, and
  Priya said it would be re-scoped when he returned. Tomas returned on the 10th.
  Nothing since.

## What I would suggest

The retro action was "audit the docs". The problem is not that they were not audited,
it is that six of the nine discrepancies above have existed for over a month with a
named owner. Auditing quarterly produces a list like this one quarterly.
