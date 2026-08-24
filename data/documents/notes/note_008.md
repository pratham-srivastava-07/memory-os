---
doc_id: note_008
type: note
subtype: draft
title: "Arca SLO draft"
author: Tomas Herrera
date: 2026-05-29
status: superseded
projects: [Arca]
tickets: [ARCA-301]
tags: [slo, latency, availability, draft, stale]
---

# Arca SLO draft

**Draft. Not agreed by anyone.** I wrote this because we page on numbers nobody has
signed off.

> **Note added 2026-07-03:** superseded by ADR-012. The numbers below are wrong and
> have been wrong since before I wrote them. Leaving the document because the
> *reasoning* about sub-budgets is what ADR-012 built on. Do not quote the table.

## Proposed SLIs and SLOs

| SLI | Target |
|---|---|
| `/v1/retrieve` availability | 99.5% monthly |
| `/v1/retrieve` latency p50 | 90 ms |
| `/v1/retrieve` latency **p95** | **250 ms** |
| `/v1/retrieve` latency p99 | 700 ms |
| Ingest job completion within 5 min | 99% |

## Where these numbers come from

Honestly? The p95 of 250 ms is from a slide in a customer deck from 2025. I could not
find anything better. The availability number is what the standard contract says.

That is the problem I am trying to surface by writing it down. We have a target in a
customer deck, a different one in `project_arca.md` (300 ms), and a monitoring
configuration that alerts on neither because it watches p50.

## What I actually want

Sub-budgets. "p95 250 ms end to end" tells me nothing when it breaches. I need to know
that rerank owns 150 of it and candidate generation owns 60, so that when the number
moves I know which team's problem it is.

Rough attempt, entirely made up:

| Stage | p95 |
|---|---|
| Auth + validation | 10 ms |
| Candidate generation | 80 ms |
| Hydration | 45 ms |
| Rerank | 100 ms |
| Serialisation | 15 ms |

## Error budget

99.5% monthly is 3h 39m. I want a written policy for what happens when we burn it,
because right now the answer is "nothing happens and we keep shipping".

## Blocking question for whoever owns this

**What is the actual latency target, and who decided it?** I have asked twice in sync
and got a shrug both times.
