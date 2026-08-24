---
doc_id: meeting_023
type: meeting
title: "Arca Architecture Review #6 — reranker hosting, RLS"
date: 2026-07-16
time: "10:00–11:20 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Elliot Vance, Mei Lin Zhao, Jonas Weiss, Tomas Herrera, Priya Raman, Ravi Menon]
projects: [Arca, Migration]
tickets: [ARCA-288, INFRA-92, SEC-44, SEC-51]
decisions: [ADR-016, ADR-017]
tags: [architecture, reranking, rls, security, review]
---

# Arca Architecture Review #6 — 2026-07-16

**First review at the new time.** Moved from 12:00 to 10:00 UTC at Mei's request —
12:00 UTC is 20:00 in Singapore and she has missed three of the last five. Handbook
updated.

## 1. RLS, fourth attempt

**Mei:** I have production numbers now and they are worse than staging. RLS on
`arca.chunks`, 60M rows, 32 partitions: the predicate is applied per partition after
pruning and the planner abandons the `(tenant_id, document_id)` index in favour of a
parallel sequential scan on three partitions. Hydration p95 goes from 38 ms to 156 ms.

**Tomas:** ADR-012 gives hydration forty.

**Mei:** Yes. We are four times over on that stage alone.

**Jonas:** Then I will say something I did not expect to say. RLS was never the
control. The control is that `arca-retrieve` builds every query through one query
builder. RLS was the backstop for the case where somebody writes SQL by hand, and
that case is the control plane and the admin tooling, not the hot path.

**Daniel:** So keep it where humans write SQL and drop it where the machine does.

**Jonas:** With compensating controls, yes. A CI check that fails the build on raw SQL
in the retrieval path that does not go through `TenantScopedQuery`. And a nightly
probe that runs a known cross-tenant query as the service role and alerts if it ever
returns a row.

**Priya:** Is this a weakening?

**Jonas:** It is a weakening. I want that in the ADR in plain words, not hedged. We
are trading a preventive control for a preventive-plus-detective pair that is weaker
in the worst case. I will sign it for the current customer set. Lumen Health has a
contractual isolation requirement and my sign-off is scoped to today's data and
expires 1 October.

**Karen** *(via written comment)*: the CI check is mine. It needs to run on the
retrieval path only or it will flag every migration script.

## 2. Reranker hosting

**Elliot:** My note is out. Two options for the reranker once chunks go to 800 tokens.
CPU is dead either way — 340 ms p95 at 1024 tokens for 50 candidates against a 180 ms
budget.

Cohere hosted: about $11,200 a month at our volume, no ops, and it was ahead when I
first costed it.

Self-hosted GPU: I originally costed on-demand A10G and it looked worse. Re-costed on
L4 with a one-year commitment and on measured throughput rather than my estimate, it
is the number Mei put in the capacity doc. That reverses the recommendation.

**Daniel:** How far does it reverse it?

**Elliot:** Far enough that I would not argue for Cohere on cost. And there is a
second thing I missed entirely.

**Jonas:** Cohere is a new sub-processor. Thirty days' notice to Lumen Health and a
contract conversation, three weeks before a cutover.

**Daniel:** That is the same constraint that decided the embedding model in ADR-005.

**Jonas:** It is exactly the same constraint and we forgot it. That is worth noticing
as a pattern: any hosted inference vendor is a sub-processor decision before it is a
cost decision.

**Priya:** Then it is self-hosted. Elliot, what is the measured latency?

**Elliot:** 71 ms p95 for 50 candidates at 1024 tokens on L4 with TensorRT and fp16.
109 ms under budget.

**Tomas:** Nobody here has run GPU nodes in production. I want a runbook for "the GPU
node is unhealthy" before it takes traffic, and I am out from Monday.

**Priya:** Then it does not take traffic before you are back, or somebody else writes
it. Daniel?

**Daniel:** I will write it.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-016, RLS narrowing, unhedged | Jonas | 2026-07-17 |
| 2 | SEC-51 CI check on the retrieval path | Karen | 2026-07-24 |
| 3 | Nightly cross-tenant probe job | Jonas | 2026-07-31 |
| 4 | Write ADR-017, reranker self-hosted | Elliot | 2026-07-20 |
| 5 | Provision L4 nodes (INFRA-92) | Tomas | 2026-07-17 |
| 6 | GPU node runbook | Daniel | 2026-08-07 |
