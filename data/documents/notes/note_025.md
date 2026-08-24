---
doc_id: note_025
type: note
subtype: capacity
title: "Arca capacity and cost model"
author: Mei Lin Zhao
date: 2026-07-15
last_updated: 2026-08-04
projects: [Arca, Migration]
tickets: [INFRA-88, INFRA-92, INFRA-95]
tags: [capacity, cost, infrastructure, model]
---

# Arca capacity and cost model

Maintained by Mei. Updated when something changes, which this quarter has been
constantly. Figures are monthly, eu-west-1, and include both regions unless stated.

## 1. Postgres

`pg-arca-primary-01`: 32 vCPU, 256 GB, gp3 8000 IOPS, plus two read replicas per
region.

| Item | Monthly |
|---|---|
| Primary | $2,840 |
| Replicas (4) | $5,120 |
| Storage, 4.2 TB provisioned | $410 |
| Backups | $180 |

**Heap note.** `arca.chunks.embedding` at `vector(1024)` is roughly 4 KB per row
before TOAST. At the 60M chunks projected for end of 2026 that is about 240 GB of
heap that was not in the original model. Added 2026-05-22 after the architecture
review. Per ADR-019 the HNSW index is dropped, which returns about 180 GB; the column
itself stays until 2026-09-30.

## 2. Embedding (arca-index)

`gte-large-v2` on CPU, c7i.4xlarge, 380 chunks/sec/node.

| Item | Monthly |
|---|---|
| 6 nodes (steady) + burst | $1,900 |

Hosted equivalent was quoted at $4,100 at list. Not viable anyway — see ADR-005 and
the sub-processor constraint.

## 3. Vector store

| Item | Monthly |
|---|---|
| `qdrant-prod-eu1`, 4 nodes (ADR-014) | $2,180 |
| → 6 nodes + `qdrant-prod-us1` at 3 (ADR-019) | $4,910 |

Updated 2026-08-04 for the consolidation. The pgvector line disappears entirely once
the column is dropped on 30 September, which takes about $500/month of storage with it.

## 4. Reranking (arca-rank)

Costed twice. First pass assumed on-demand A10G and measured nothing.

| Option | Monthly | Note |
|---|---|---|
| CPU, current | $1,240 | Does not meet ADR-012 budget at 1024 tokens |
| Cohere rerank API | $11,200 | New sub-processor. Blocked by contract, not cost |
| 6x g5.xlarge (A10G), on-demand | $13,900 | The number Elliot first costed |
| **4x g6.xlarge (L4), 1-year committed** | **$6,800** | Chosen, ADR-017 |

The L4 figure is the one to quote. It assumes measured throughput of 1,340 candidate
scorings/sec/node at 1024 tokens, four nodes for peak with one spare, and a one-year
commitment. Without the commitment it is $9,700 and the argument against Cohere gets
much thinner.

## 5. Observability

| Item | Monthly |
|---|---|
| Datadog (current, to 2026-10-01) | ~$17,800 |
| Grafana Cloud Pro (ADR-013) | $4,200 |
| Helios self-hosted (not proceeding) | $3,500 + 6 engineer-weeks |

INFRA-95 (cardinality reduction on `arca-index`) is worth roughly $6k/month against
the Datadog line and an unknown amount against Grafana, which prices differently.

## Total, current run rate

Roughly **$28,400/month** as of 2026-08-04, against $31,900 in May. The migration and
the Helios pause are both net savings; the GPU nodes and Qdrant are net additions.
