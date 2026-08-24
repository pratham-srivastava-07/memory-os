---
doc_id: note_027
type: note
subtype: scratch
title: "The model rollout problem nobody owns"
author: Elliot Vance
date: 2026-08-07
projects: [Arca]
tickets: [ARCA-260, ARCA-288, ARCA-341]
tags: [ml, models, gap, recurring, scratch]
---

# The model rollout problem nobody owns

Writing this down because I have now raised it three times in three different contexts
and it has been "noted" three times.

## The problem

We have two models in the retrieval path:

- `gte-large-v2` for embeddings, 1024 dims, chosen in ADR-005
- `bge-reranker-v2-m3` for reranking, chosen in ADR-017

Neither ADR says how we change them.

For the reranker it is not that bad. Swap the model, rerun the eval, deploy. The
reranker does not persist anything.

For the embedding model it is genuinely hard and nobody has thought about it:

1. Every stored vector was produced by `gte-large-v2`. 14.6M today, 60M projected.
2. A new model means re-embedding all of them. At 380 chunks/sec/node on six nodes
   that is roughly 18 hours for the current corpus and about 3 days at 60M.
3. During those hours or days, some vectors are from the old model and some from the
   new. **They are not in the same space.** Cosine distance between an old vector and
   a new query embedding is meaningless. Not degraded — meaningless.
4. So either we run both models simultaneously and route by which version a chunk was
   embedded with, or we accept a period where retrieval is broken for a subset of
   documents, or we build a shadow index and swap.
5. If the new model has different dimensionality, `arca.chunks.embedding` is
   `vector(1024)` and that is a schema migration on 60M rows.

Point 3 is the one people do not see coming. I have watched two people nod along to
points 1 and 2 and then be surprised by 3.

## Where I have raised it

- ADR-005, consequences section: "We own model updates. There is no plan yet for how
  we roll a new embedding model without downtime. Tracked loosely as ARCA-260 but
  nobody has written it up." Written by me, 9 June.
- ADR-017, consequences: "The model is pinned by digest. Elliot wants a documented
  process for changing it; same gap as ADR-005 flagged for embeddings and still
  nobody owns it." Written by me, 20 July.
- Architecture review, 16 July, verbally. Noted.

## Why it has not been done

It is not urgent. We are not changing the embedding model this quarter. It only
becomes urgent on the day somebody says "there is a better model now", at which point
it is a quarter of work standing between us and a two-point nDCG gain, and the
decision will get made badly under pressure.

## What I want

A written plan. Not an implementation. Four pages: shadow index approach, dual-model
routing during transition, the dimensionality case, and a rough cost. Two days of my
time.

## The adjacent version of this

ADR-011 changes the chunker, which requires re-chunking and re-embedding 14.6M chunks
— 46 hours of CPU-node time. That reindex has not been run yet and it hits **exactly
the same problem in a smaller form**: during the reindex, some documents are chunked
at 512 and some at 800, and results across the two are not comparable.

We have a mitigation for the eval side of that — ADR-020 makes the harness refuse to
compare runs with different `chunker_version`. We have no mitigation for the *serving*
side. A tenant mid-reindex is serving from a mixed corpus and nobody has said what
that does to their results.

**The reindex is scheduled for after the Mongo decommission. That is next week.**
