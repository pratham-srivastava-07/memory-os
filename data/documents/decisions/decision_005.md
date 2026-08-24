---
doc_id: decision_005
type: decision
adr_id: ADR-005
title: "Embedding model: self-hosted gte-large-v2"
date: 2026-06-09
status: accepted
deciders: [Elliot Vance, Daniel Okoye, Jonas Weiss]
project: Arca
project_id: PRJ-1042
tickets: [ARCA-260]
supersedes: []
superseded_by: []
tags: [embeddings, ml, cost, data-residency]
---

# ADR-005: Embedding model — self-hosted gte-large-v2

## Status

Accepted 2026-06-09.

## Context

We embed roughly 9M chunks a month and growing. Three options: a hosted embedding
API, a self-hosted open model on CPU, or a self-hosted open model on GPU.

Jonas raised the constraint that decides most of this: Lumen Health (`tnt_7731`) is
a healthcare customer and their contract prohibits sending document content to a
third-party processor that is not in our sub-processor list. Adding one takes 30 days
of notice.

## Decision

`gte-large-v2`, 1024 dimensions, self-hosted on CPU nodes (c7i.4xlarge) inside
`arca-index`. Batch size 64, ONNX runtime.

## Rationale

- Data never leaves our VPC, which makes the Lumen conversation a non-conversation.
- At our volume, CPU inference costs about $1,900/month. The equivalent hosted API
  bill was quoted at $4,100/month at list.
- Elliot benchmarked `gte-large-v2` against two alternatives on a 2,000-query
  internal set built from console query logs: nDCG@10 of 0.71 versus 0.68 for
  `e5-large-v2` and 0.73 for a hosted model. The 2-point gap to the hosted model did
  not justify the residency problem.

## Consequences

- 1024 dimensions is now load-bearing. `arca.chunks.embedding` is `vector(1024)` and
  changing model family means a full reindex of 14.6M rows.
- Embedding throughput becomes a capacity planning item: 380 chunks/sec/node.
- We own model updates. There is no plan yet for how we roll a new embedding model
  without downtime. Tracked loosely as ARCA-260 but nobody has written it up.
