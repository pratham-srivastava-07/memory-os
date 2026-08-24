---
doc_id: project_arca
type: project_doc
title: "Project Arca — Retrieval & Context Service"
project: Arca
project_id: PRJ-1042
status: active
owner: Daniel Okoye
created: 2026-05-04
last_updated: 2026-07-06
tags: [arca, retrieval, vector-search, living-doc]
---

# Project Arca (PRJ-1042)

> Living document. Sections carry their own review dates. If a section has not been
> reviewed in 30 days, treat its contents as unverified.

## What Arca is

Arca is the retrieval and context service behind Meridian. It ingests customer
documents, chunks and embeds them, stores the vectors and the metadata, and answers
`/v1/retrieve` with a ranked set of passages plus provenance.

Consumers:
- `meridian-console` (the product UI)
- `api-gateway` (Project API / PRJ-1088), which exposes retrieval to customers
- Internal eval tooling (`arca-eval`)

## Services

*Section reviewed 2026-05-08 — see ADR-001.*

| Service | Repo | Owner | Notes |
|---|---|---|---|
| Ingest | `arca-ingest` | Ravi Menon | Upload, parse, chunk. Was Daniel's until 2026-06-22. |
| Index | `arca-index` | Mei Lin Zhao | Embedding and vector write path |
| Retrieve | `arca-retrieve` | Daniel Okoye | Query planning, hybrid search |
| Rank | `arca-rank` | Elliot Vance | Cross-encoder reranking |

Deployed to `arca-prod-eu1` and `arca-prod-us1`. EU is the primary region; US1 was
brought up on 2026-06-08 for the Northwind Retail pilot.

## Data layer

*Section reviewed 2026-05-12. Not reviewed since.*

MongoDB (`mongo-arca-01`) is the system of record for document metadata, chunk
records, and tenant configuration. Postgres is used only for the control plane
(tenants, API keys, quotas).

Collections:
- `documents` — one record per source document
- `chunks` — one record per chunk, with `doc_id`, `tenant_id`, `ordinal`
- `jobs` — ingest job state

> Note from Mei (2026-05-12): we are actively evaluating a move off Mongo, see
> ARCA-212. Do not build new write paths against `chunks` without talking to me.

## Chunking

*Section reviewed 2026-05-13.*

Fixed-size chunking at **512 tokens with 64 tokens of overlap**, tokenised with the
embedding model tokeniser. Chunk boundaries never cross a document boundary.
Implemented in `arca-ingest/chunker/fixed.py` (ARCA-244).

## Embeddings

*Section reviewed 2026-06-09.*

`gte-large-v2`, self-hosted on CPU nodes in `arca-index`. 1024 dimensions.
Batch size 64. See ADR-005 for why we did not use a hosted embedding API.

## Vector storage

*Section reviewed 2026-06-05.*

pgvector 0.7 with an HNSW index (`m=16`, `ef_construction=200`) living in the same
Postgres cluster as the metadata. One table per region, partitioned by `tenant_id`
hash into 32 partitions.

## Performance targets

*Section reviewed 2026-06-01.*

- `/v1/retrieve` p95 **300 ms** end to end, measured at the gateway
- `/v1/retrieve` p99 900 ms
- Ingest throughput: 400 documents/minute/region
- Availability: 99.5% monthly

## Open workstreams

| Ticket | Description | Owner |
|---|---|---|
| ARCA-233 | Ingest pipeline v2 (streaming parse) | Ravi Menon |
| ARCA-288 | Reranker service hardening | Elliot Vance |
| ARCA-301 | Retrieve query planner rewrite | Daniel Okoye |
| ARCA-317 | Hybrid search: BM25 + vector fusion | *unassigned* |
| ARCA-329 | Qdrant adapter behind the index interface | Mei Lin Zhao |
| ARCA-341 | Offline eval harness | Elliot Vance |

## Related

- Project Migration (PRJ-1103) — `project_migration.md`
- Project API (PRJ-1088) — `project_api.md`
- Team working agreements — `team_handbook.md`
