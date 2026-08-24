---
doc_id: decision_012
type: decision
adr_id: ADR-012
title: "Retrieval latency budget revised to p95 400 ms"
date: 2026-07-03
status: accepted
deciders: [Tomas Herrera, Daniel Okoye, Sofia Nyberg, Elliot Vance]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-301, ARCA-288]
supersedes: []
superseded_by: []
tags: [slo, latency, performance]
---

# ADR-012: Retrieval latency budget revised to p95 400 ms

## Status

Accepted 2026-07-03.

## Context

The Arca SLO has been "p95 250 ms" in Tomas's SLO draft and "p95 300 ms" in
`project_arca.md`, and nobody noticed the two documents disagreed until Sofia quoted
one of them to a customer. Neither number was derived from anything; both predate
the reranker.

Meanwhile ADR-011 raises the reranker sequence length, which adds roughly 60 ms p95,
and ADR-008's RLS predicates added 9% in staging and more in production.

Actual production p95 over the last 30 days on `/v1/retrieve`, measured at the
gateway: **341 ms**. We have been missing both stated targets the entire time and
have never alerted on it, because the alert was configured against p50.

## Decision

The end-to-end budget for `/v1/retrieve`, measured at `api-gateway`, is:

| Percentile | Budget |
|---|---|
| p50 | 120 ms |
| p95 | **400 ms** |
| p99 | 900 ms |

Sub-budgets, which is the part that was actually missing:

| Stage | p95 budget |
|---|---|
| Gateway auth + validation | 15 ms |
| Candidate generation (vector + BM25) | 120 ms |
| Hydration | 40 ms |
| Rerank | 180 ms |
| Serialisation | 25 ms |

Availability target stays 99.5% monthly. Error budget policy: two consecutive weeks
of budget burn above 50% freezes feature work on `arca-retrieve`.

## Consequences

- 400 ms is a relaxation against both previous numbers and Sofia is uncomfortable
  saying so to design partners. Agreed wording: "sub-half-second retrieval".
- `project_arca.md` still says 300 ms and needs updating. Daniel owns that.
- The rerank sub-budget of 180 ms is the one under pressure. It is what forced the
  reranker hosting question in ADR-017.
