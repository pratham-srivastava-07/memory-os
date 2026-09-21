# MemoryOS — Retrieval & Context Engineering System

## Purpose

MemoryOS is a production-oriented AI retrieval and context infrastructure project built to understand how modern AI systems retrieve, rank, and eventually maintain useful information over time.

The goal is not simply to build another RAG application where documents are embedded and passed to an LLM.

The project focuses on the infrastructure underneath such systems:

> **Given a large, evolving knowledge base, how do we retrieve the right information, rank it correctly, handle conflicting or outdated knowledge, and construct high-quality context for an AI system?**

The project is intentionally being built incrementally, with each retrieval component evaluated before additional complexity is introduced.

---

## End Product

The intended end product is a **context and memory retrieval engine for AI applications and agents**.

A client should eventually be able to ask:

```text
"What database did the team decide to use?"
```

and the system should determine the most relevant, authoritative, and current information from potentially conflicting historical knowledge.

The target architecture is:

```text
                        Query
                          │
                ┌─────────┴─────────┐
                │                   │
        Semantic Retrieval    Lexical Retrieval
           (pgvector)          (Postgres FTS)
                │                   │
                └─────────┬─────────┘
                          │
                         RRF
                          │
                  Candidate Pool
                          │
                    CrossEncoder
                      Reranking
                          │
                Metadata / Temporal
                     Resolution
                          │
                 Context Construction
                          │
                  AI / Agent / LLM
```

The system should ultimately support:

- semantic retrieval
- lexical retrieval
- hybrid retrieval
- Reciprocal Rank Fusion (RRF)
- CrossEncoder reranking
- metadata-aware retrieval
- temporal/latest-state retrieval
- context construction
- source attribution
- retrieval evaluation
- latency measurement
- caching
- agent-facing retrieval interfaces
- persistent memory/context infrastructure

---

## Current Implementation

The retrieval system currently includes:

### Storage

PostgreSQL is the primary database.

`pgvector` provides vector storage and similarity search without introducing a separate vector database.

Documents are split into chunks before embedding and ingestion.

### Semantic Retrieval

Chunks are embedded using Sentence Transformers and stored using `pgvector`.

Queries are independently embedded and compared against stored vectors using vector similarity.

### Lexical Retrieval

PostgreSQL Full Text Search provides a lexical retrieval path for exact terminology, identifiers, names, and keyword-heavy queries.

### Hybrid Retrieval

Semantic and lexical retrieval execute independently and produce candidate rankings.

Their rankings are combined using **Reciprocal Rank Fusion (RRF)**.

```text
semantic ranking ──┐
                   ├── RRF → fused candidates
lexical ranking ───┘
```

RRF intentionally operates on rank positions rather than trying to directly compare incompatible semantic and lexical scores.

### Reranking

The fused candidate set is passed through:

```text
cross-encoder/ms-marco-MiniLM-L6-v2
```

The CrossEncoder jointly evaluates:

```text
(query, candidate chunk)
```

and produces a relevance score.

This provides a more expensive but more precise ranking stage after high-recall retrieval.

---

## Evaluation

Retrieval changes are evaluated rather than assumed to improve the system.

Implemented evaluation includes:

- Semantic baseline
- PostgreSQL lexical baseline
- RRF-only evaluation
- RRF + CrossEncoder evaluation
- Recall@K
- Hit@K
- MRR
- Per-tag analysis
- Candidate-pool tuning
- Candidate recall diagnostics
- End-to-end p50 latency
- End-to-end p95 latency
- End-to-end p99 latency

This allows comparisons such as:

```text
Semantic
    ↓
Semantic + Lexical + RRF
    ↓
Semantic + Lexical + RRF + Reranking
```

The objective is not to maximize complexity.

Every additional stage should justify itself through measurable improvements in retrieval quality or system behavior.

---

# What I Am Learning

## 1. Embeddings Are Only One Part of Retrieval

Semantic similarity is useful for conceptual queries but is not universally sufficient.

Exact identifiers, technical terminology, names, and rare tokens can be better served by lexical retrieval.

This motivates hybrid retrieval rather than relying entirely on embeddings.

---

## 2. Retrieval Is a Multi-Stage System

Production retrieval is better understood as:

```text
Candidate Generation
        ↓
Candidate Fusion
        ↓
Reranking
        ↓
Filtering / Resolution
        ↓
Context Construction
```

Different stages optimize for different objectives.

Initial retrieval prioritizes **recall**.

Reranking prioritizes **precision and ordering**.

---

## 3. Scores From Different Retrieval Systems Are Not Directly Comparable

Vector similarity scores and lexical ranking scores represent different things and have different distributions.

Reciprocal Rank Fusion avoids naive score normalization by combining rank positions:

```text
RRF(d) = Σ 1 / (k + rank(d))
```

This provides a simple mechanism for combining heterogeneous retrieval systems.

---

## 4. Reranking Trades Compute for Relevance

Bi-encoder retrieval independently represents queries and documents, making large-scale search efficient.

A CrossEncoder processes the query and document together.

This is more computationally expensive but provides richer relevance estimation.

Therefore:

```text
Fast retrieval → small candidate set → expensive reranking
```

is preferable to running a CrossEncoder over the entire corpus.

---

## 5. Candidate Quality Places an Upper Bound on Reranking

A reranker cannot recover a relevant document that never entered the candidate pool.

Therefore candidate recall must be measured separately from final ranking quality.

This led to candidate-pool experiments rather than arbitrarily selecting a retrieval depth.

---

## 6. Retrieval Quality and Latency Must Be Evaluated Together

Increasing candidate count can improve recall while increasing:

- database work
- CrossEncoder inference cost
- memory usage
- end-to-end latency

The correct candidate size is therefore an engineering trade-off rather than simply the configuration with the highest retrieval metric.

---

## 7. Chunking Is a Retrieval Decision

Chunk size and overlap directly affect:

- semantic specificity
- retrieval recall
- duplicate results
- context quality
- embedding/storage cost

Chunking therefore belongs to retrieval system design rather than being treated as simple preprocessing.

---

## 8. Evaluation Must Drive Architecture

A retrieval component should not be added merely because it is common in RAG architectures.

The process used throughout this project is:

```text
Build baseline
     ↓
Measure
     ↓
Identify failure mode
     ↓
Introduce mechanism
     ↓
Measure again
```

This makes architectural decisions explainable and measurable.

---

# Next Engineering Problems

## Component-Level Latency

Measure individual latency for:

```text
query embedding
vector retrieval
lexical retrieval
RRF
CrossEncoder reranking
context construction
```

This will identify where the retrieval latency budget is actually being spent.

---

## RRF vs Reranking Cost

Compare:

```text
Hybrid + RRF
```

against:

```text
Hybrid + RRF + CrossEncoder
```

to quantify the relevance improvement obtained for the additional inference latency.

---

## Final Candidate Pool Selection

Evaluate different candidate depths such as:

```text
10
20
30
50
```

and select a configuration based on both retrieval quality and latency.

---

## Graded Relevance and nDCG@K

Current binary relevance evaluation will be extended to graded relevance:

```text
3 → ideal
2 → highly relevant
1 → partially relevant
0 → irrelevant
```

This enables nDCG@K and better evaluation of ranking quality.

---

## Temporal / Latest-State Retrieval

The next major retrieval problem is handling knowledge that changes over time.

For example:

```text
January:
"We are evaluating MongoDB."

February:
"PostgreSQL has been selected."

March:
"The PostgreSQL migration is complete."
```

For:

```text
"What database are we using?"
```

semantic similarity alone may retrieve all three.

The system must understand that information can be:

```text
historical
superseded
current
```

This introduces temporal retrieval and eventually memory lifecycle semantics.

---

# Long-Term Direction

The retrieval engine is intended to become the foundation for a broader memory system.

The progression is:

```text
Retrieval
   ↓
Hybrid Search
   ↓
Reranking
   ↓
Temporal Knowledge
   ↓
Context Construction
   ↓
Memory
   ↓
Agent Context
```

Future versions should explore concepts such as:

- episodic memory
- semantic memory
- memory consolidation
- memory promotion
- temporal decay
- superseded knowledge
- entity-aware retrieval
- context budgeting
- agent-specific memory
- memory provenance

The eventual goal is for an AI system to retrieve not merely what is **similar**, but what is:

> **relevant, current, authoritative, and useful for the task being performed.**

---

## Core Takeaway

The central lesson of this project is that building reliable AI systems is not primarily about calling an LLM.

A significant engineering problem exists before generation:

```text
What information should the model see?
```

MemoryOS explores the systems, retrieval algorithms, evaluation methodology, and infrastructure required to answer that question reliably.