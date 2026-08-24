---
doc_id: decision_011
type: decision
adr_id: ADR-011
title: "Chunking v2: structure-aware chunking at ~800 tokens"
date: 2026-07-01
status: accepted
deciders: [Elliot Vance, Daniel Okoye, Karen Oyelaran]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-244, ARCA-341]
supersedes: [ADR-003]
superseded_by: []
tags: [chunking, retrieval-quality, ingest]
---

# ADR-011: Chunking v2 — structure-aware chunking at ~800 tokens

## Status

Accepted 2026-07-01. Supersedes ADR-003.

## Context

ARCA-341 gave us an eval harness, which gave us permission to change the chunker.
Elliot ran three strategies over a 1,400-query set drawn from console logs across
six tenants:

| Strategy | nDCG@10 | Recall@20 | Chunks per doc (median) |
|---|---|---|---|
| Fixed 512 / 64 overlap (current) | 0.71 | 0.83 | 24 |
| Fixed 1024 / 128 overlap | 0.69 | 0.86 | 12 |
| Structure-aware, target 800, 15% overlap | 0.78 | 0.89 | 15 |

The structure-aware win is concentrated in documents with tables and headings, which
is most of what Northwind Retail and Calder Freight upload.

## Decision

Structure-aware chunking:

- Split on heading boundaries first, then paragraph, then sentence.
- Target **800 tokens**, hard maximum 1,024, minimum 120 (below which we merge
  forward).
- Overlap **15% of the preceding chunk**, not a fixed token count.
- Tables are never split. A table over 1,024 tokens becomes its own chunk and is
  flagged `oversized=true`.
- Each chunk carries its heading path as metadata (`section_path`), which the
  reranker gets as a prefix.

## Consequences

- **Full reindex required.** 14.6M chunks re-chunked and re-embedded. Elliot's
  estimate is 46 hours of CPU-node time. It cannot start until after the migration
  cutover, because doing both at once is how you get an incident.
- Median chunks per document drops 38%, which reduces storage and embedding cost.
- `arca-rank` max sequence length must go from 512 to 1024. Elliot flagged this adds
  roughly 1.8x to rerank latency per candidate, which eats into the latency budget —
  see ADR-012.
- The 512-token corpus and the 800-token corpus will coexist during the reindex, and
  scores are not comparable across them. Karen wants the eval harness to refuse to
  compare runs with different `chunker_version`.
