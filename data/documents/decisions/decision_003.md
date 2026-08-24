---
doc_id: decision_003
type: decision
adr_id: ADR-003
title: "Chunking v1: fixed 512-token windows"
date: 2026-06-03
status: superseded
deciders: [Daniel Okoye, Elliot Vance]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-244]
supersedes: []
superseded_by: [ADR-011]
tags: [chunking, ingest, retrieval-quality]
---

# ADR-003: Chunking v1 — fixed 512-token windows

## Status

**Superseded by ADR-011 (2026-07-01).** Kept because the 512-token corpus is still in
Mongo and will be until the reindex completes.

## Context

We have been chunking at 512 tokens with 64 overlap since the prototype and never
wrote it down. Elliot asked what the number was based on and nobody could answer.
This ADR records the existing behaviour rather than changing it, so that changing it
later is a decision and not a surprise.

## Decision

Fixed-size chunking, 512 tokens, 64 tokens of overlap, tokenised with the embedding
model tokeniser. Boundaries never cross a document boundary. Tables and code blocks
are chunked as opaque units if they fit and split naively if they do not.

## Consequences

- Predictable chunk counts, which makes cost modelling easy.
- Bad on structured documents. Elliot's spot check of 40 Northwind Retail PDFs found
  that 31% of chunks split a table across a boundary.
- The 512 number is baked into the reranker's max sequence length. Changing chunk
  size means retuning `arca-rank`.

## Alternatives considered

- Semantic chunking on paragraph and heading boundaries. Deferred — no eval harness
  to prove it helps. That harness is ARCA-341.
