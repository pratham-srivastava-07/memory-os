---
doc_id: decision_017
type: decision
adr_id: ADR-017
title: "Reranker: self-host bge-reranker-v2-m3 on L4 GPUs"
date: 2026-07-20
status: accepted
deciders: [Elliot Vance, Daniel Okoye, Priya Raman, Jonas Weiss]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-288, INFRA-92]
supersedes: []
superseded_by: []
tags: [ml, reranking, cost, gpu, latency]
---

# ADR-017: Reranker — self-host bge-reranker-v2-m3 on L4 GPUs

## Status

Accepted 2026-07-20. This reverses the recommendation in Elliot's 2026-07-16 cost
note, which favoured the hosted Cohere rerank API.

## Context

ADR-011 raised chunk size to 800 tokens, which raised the reranker's sequence length
from 512 to 1024, which roughly doubled rerank cost per candidate. ADR-012 gives
rerank 180 ms of a 400 ms p95 budget. Current production: `bge-reranker-base` on CPU,
rerank p95 at 512 tokens is 190 ms for 50 candidates. At 1024 tokens it is 340 ms.
CPU is out.

Two options were costed: hosted Cohere rerank, or self-hosting on GPU.

Elliot's 2026-07-16 note put Cohere ahead at $11,200/month against a self-hosted
figure that assumed on-demand A10G instances. Two things changed between that note
and this decision:

1. The self-hosted number was re-costed on **L4** instances with a one-year
   commitment, and on measured throughput rather than an estimate. The figure Mei put
   in the capacity doc is what we used.
2. Jonas pointed out that Cohere would be a new sub-processor, which triggers the
   30-day notice clause in the Lumen Health contract and a conversation we do not
   want to have three weeks before a migration cutover. This is the same constraint
   that decided ADR-005 and we had forgotten it.

## Decision

Self-host `bge-reranker-v2-m3` on 4x `g6.xlarge` (L4) in `arca-rank`, two per region,
one-year committed. TensorRT, fp16, dynamic batching with a 12 ms queue window.

Measured: rerank p95 71 ms for 50 candidates at 1024 tokens. That is 109 ms under the
ADR-012 sub-budget, which is the headroom we wanted.

## Consequences

- Fixed monthly cost instead of per-request. Below roughly 30M rerank calls/month
  Cohere would be cheaper; we crossed that in May.
- No new sub-processor. No customer notice. No contract review.
- We now operate GPU nodes, which nobody on the team has done in production. Tomas
  wants a runbook for "the GPU node is unhealthy" before this takes traffic, and it
  is not written.
- The model is pinned by digest. Elliot wants a documented process for changing it;
  same gap as ADR-005 flagged for embeddings and still nobody owns it.

## Alternatives considered

- **Cohere rerank API.** See above. Would have been simpler and is not ruled out
  forever; revisit if GPU ops turn out to be a tax.
- **Drop reranking for large result sets.** Elliot measured nDCG@10 falling from 0.78
  to 0.64 without rerank. Not a real option.
- **Keep 512-token chunks to keep CPU rerank.** Would give back the ADR-011 quality
  win, which is larger than the rerank win. Rejected.
