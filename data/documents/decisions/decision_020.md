---
doc_id: decision_020
type: decision
adr_id: ADR-020
title: "Retrieval quality gates in CI before any ranking change ships"
date: 2026-08-06
status: accepted
deciders: [Elliot Vance, Karen Oyelaran, Daniel Okoye, Priya Raman]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-341, ARCA-317]
supersedes: []
superseded_by: []
tags: [eval, quality, ci, process]
---

# ADR-020: Retrieval quality gates in CI

## Status

Accepted 2026-08-06, out of the quarter retro.

## Context

Three of this quarter's larger decisions — chunking (ADR-011), the vector store
(ADR-014, ADR-019), the reranker (ADR-017) — were made or reversed on the strength of
a benchmark somebody ran by hand, once, in a notebook. ADR-003 existed because nobody
could remember why 512.

The eval harness (ARCA-341) works and is used ad hoc. It is not in CI.

## Decision

`arca-eval` runs on every pull request that touches `arca-retrieve`, `arca-rank`, or
the chunker.

- Fixed query set: 1,400 queries across six tenants, versioned, stored in
  `arca-eval/sets/core-v1`.
- Gate: nDCG@10 may not drop more than **0.01** against the base branch. Recall@20
  may not drop more than 0.02.
- Runs are tagged with `chunker_version`, `embedding_model`, `reranker_model` and
  `vector_store`. The harness refuses to compare runs whose tags differ, which is why
  the pgvector-to-Qdrant move needed a re-baseline rather than a comparison.
- A gate failure is overridable by two reviewers with a written reason recorded in
  the PR. It is not a hard block; Daniel argued a hard block would just get disabled
  the first Friday it was wrong.

## Consequences

- PR time on those three repos goes up by about 9 minutes.
- ARCA-317 (hybrid BM25 + vector fusion) is the first change to go through the gate.
  It has been unowned since June and is now Ravi's, in name as well as in practice.
- We need a policy for refreshing the query set, because a fixed set goes stale and
  optimising against it is a known failure mode. Nobody owns that yet. Elliot's
  suggestion of quarterly resampling from console logs was noted and not decided.
