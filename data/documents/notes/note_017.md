---
doc_id: note_017
type: note
subtype: cost_model
title: "Reranker hosting — cost comparison"
author: Elliot Vance
date: 2026-07-16
status: recommendation-reversed
projects: [Arca]
tickets: [ARCA-288, INFRA-92]
tags: [cost, reranking, gpu, cohere, ml]
---

# Reranker hosting — cost comparison

Why this exists: ADR-011 takes chunks to 800 tokens, which takes the reranker's
sequence length from 512 to 1024, which roughly doubles compute per candidate. Our
current CPU setup does 190 ms p95 at 512 tokens for 50 candidates. At 1024 it is
340 ms. ADR-012 gives rerank 180 ms. CPU is out.

## Volume

- 41M rerank calls/month, 50 candidates each, average ~2.05B candidate scorings
- Growing roughly 12% month on month
- Peak is 3.4x average, weekday mornings EU

## Option A — Cohere rerank API

At their published tier for our volume: **$11,200/month**. No infrastructure, no ops,
no model management. Latency 90–140 ms p95 including network from eu-west-1.

## Option B — self-hosted on GPU

First pass, on-demand `g5.xlarge` (A10G), 6 instances for peak: **$13,900/month**.
Worse than Cohere and I nearly stopped here.

Second pass, after Mei pointed out I was costing on-demand for a steady workload and
had guessed at throughput instead of measuring it:

- `g6.xlarge` (L4), TensorRT, fp16, dynamic batching, 12 ms queue window
- Measured **1,340 candidate scorings/sec/node** at 1024 tokens. My estimate had been
  400.
- 4 nodes covers peak with one to spare. Two per region.
- One-year commitment.
- The monthly figure is in Mei's capacity model, section 4. I am not restating it here
  because I have already published three versions of this number and I want one place
  for it.

Measured latency: **71 ms p95** for 50 candidates at 1024 tokens.

## Where the crossover is

Cohere is cheaper below roughly 30M rerank calls/month. We passed that in May.

## Recommendation

**Option A, Cohere.**

*(Struck through 2026-07-16 18:40. See below.)*

~~The cost gap after the re-costing is not large enough on its own to justify
operating GPU nodes with a team that has never operated GPU nodes, three weeks before
a migration cutover, with our only SRE about to go on leave. Take the hosted option
now, revisit when there is slack.~~

## Amendment, same day, after review

Jonas pointed out in the architecture review that Cohere is a new sub-processor.
Lumen Health's contract requires 30 days' notice and a review before we add one. That
is not a cost input, it is a gate, and it would land during the cutover window.

This is the identical constraint that decided ADR-005 for embeddings six weeks ago. I
read that ADR. I wrote that ADR. I did not apply it here, because I had filed it as
"a fact about embeddings" rather than "a fact about hosted inference vendors".

Revised recommendation: **Option B, self-hosted L4.** It is also cheaper, once
costed properly, and the latency is better. The ops concern stands and is answered by
requiring a runbook before it takes traffic, not by choosing the other option.

Whoever writes the next ADR involving any vendor: check the sub-processor list first.
