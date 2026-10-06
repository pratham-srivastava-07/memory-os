# MemoryOS

**Retrieval and context infrastructure for AI systems and agents.**

MemoryOS is an experimental, production-oriented retrieval system for
exploring a question that sits underneath RAG, agent memory, and context
engineering:

> **Given an evolving knowledge base, what information should an AI
> system see right now?**

Rather than treating retrieval as "embed documents, run vector search,
send results to an LLM," MemoryOS builds and evaluates retrieval as a
multi-stage system. The current implementation combines **semantic
retrieval**, **PostgreSQL full-text search**, **Reciprocal Rank Fusion
(RRF)**, and optional **CrossEncoder reranking**, with instrumentation
for retrieval quality and latency.

The longer-term goal is to evolve this retrieval engine into persistent
memory/context infrastructure that can reason about not only what is
similar, but what is **relevant, current, authoritative, and useful**.

------------------------------------------------------------------------

## Why this project exists

A typical RAG pipeline can retrieve semantically similar text, but real
systems have harder requirements:

-   exact names, identifiers, and technical terms may be missed by
    embeddings;
-   semantic and lexical scores are not directly comparable;
-   reranking improves precision but adds inference cost;
-   a reranker cannot recover documents that never entered the candidate
    pool;
-   larger candidate pools can improve recall while hurting latency;
-   historical knowledge can conflict with newer knowledge;
-   chunking changes retrieval behavior, not just preprocessing;
-   an LLM can only reason over the context the retrieval system chooses
    to expose.

MemoryOS is built around measuring these trade-offs instead of assuming
that adding another retrieval component automatically improves the
system.

------------------------------------------------------------------------

## Current architecture

``` text
                              Query
                                |
                        Query Embedding
                                |
                  +-------------+-------------+
                  |                           |
          Semantic Retrieval          Lexical Retrieval
             (pgvector)              (Postgres FTS)
                  |                           |
                  +-------------+-------------+
                                |
                       Reciprocal Rank Fusion
                              (RRF)
                                |
                         Candidate Pool
                                |
                    +-----------+-----------+
                    |                       |
                 RRF only          CrossEncoder Reranking
                                            |
                                      Top-K Results
```

The planned architecture extends this pipeline with metadata/temporal
resolution, context construction, provenance, memory lifecycle
semantics, and agent-facing interfaces.

------------------------------------------------------------------------

## What is implemented

### Semantic retrieval

Documents are embedded with:

``` text
sentence-transformers/all-MiniLM-L6-v2
```

Query embeddings are generated independently and compared against stored
chunk embeddings in PostgreSQL using `pgvector`.

Vector search uses cosine distance and converts it into a similarity
score:

``` sql
1 - (embedding <=> query_vector)
```

This path is useful for conceptual or paraphrased queries where the
query and relevant passage may not share exact words.

### Lexical retrieval

MemoryOS also queries the same chunks through PostgreSQL Full Text
Search.

The implementation uses:

``` sql
websearch_to_tsquery('english', query)
```

with `ts_rank_cd` for ranking.

Lexical retrieval complements embeddings for:

-   exact terminology;
-   identifiers;
-   names;
-   rare tokens;
-   keyword-heavy queries.

### Hybrid retrieval

Semantic and lexical retrieval run independently and return candidate
rankings.

The rankings are fused with **Reciprocal Rank Fusion**:

``` text
RRF(d) = sum(1 / (k + rank(d)))
```

The implementation currently uses:

``` text
k = 50
```

RRF combines **rank positions** instead of trying to normalize
vector-similarity and full-text-search scores onto the same numerical
scale.

### CrossEncoder reranking

The fused candidate set can optionally be reranked using:

``` text
cross-encoder/ms-marco-MiniLM-L6-v2
```

The CrossEncoder evaluates each `(query, candidate)` pair jointly and
produces a new relevance score.

This creates the retrieval pattern:

``` text
high-recall retrieval
        |
candidate fusion
        |
small candidate set
        |
expensive high-precision reranking
```

The CrossEncoder is intentionally not applied to the entire corpus.

### Stage-level latency instrumentation

`hybrid_retrieve()` can collect timing information for:

-   query embedding;
-   vector search;
-   lexical search;
-   RRF;
-   CrossEncoder reranking;
-   total retrieval latency.

This makes retrieval quality vs. latency an explicit engineering
trade-off.

------------------------------------------------------------------------

## Evaluation philosophy

MemoryOS treats evaluation as part of the architecture.

The project has been developed incrementally:

``` text
Build baseline
     |
   Measure
     |
Identify failure mode
     |
Introduce mechanism
     |
Measure again
```

Evaluation work documented in the project includes:

-   semantic baseline;
-   PostgreSQL lexical baseline;
-   RRF-only evaluation;
-   RRF + CrossEncoder evaluation;
-   Recall@K;
-   Hit@K;
-   MRR;
-   per-tag analysis;
-   candidate-pool tuning;
-   candidate recall diagnostics;
-   end-to-end p50 latency;
-   end-to-end p95 latency;
-   end-to-end p99 latency.

This makes it possible to compare progressively more expensive retrieval
configurations rather than assuming the most complex pipeline is the
best one.

------------------------------------------------------------------------

## Key engineering lessons

### Retrieval is a multi-stage system

The project models retrieval as:

``` text
Candidate Generation
        |
Candidate Fusion
        |
Reranking
        |
Filtering / Resolution
        |
Context Construction
```

Initial retrieval optimizes primarily for **recall**. Reranking
optimizes more heavily for **precision and ordering**.

### Candidate recall bounds reranking quality

A CrossEncoder can reorder candidates, but it cannot recover a relevant
document that semantic and lexical retrieval both failed to retrieve.

Therefore MemoryOS distinguishes:

``` text
candidate quality != final ranking quality
```

Candidate-pool depth must be evaluated separately.

### Retrieval quality and latency are coupled

Increasing candidate depth may improve recall but also increases:

-   database work;
-   CrossEncoder inference;
-   memory usage;
-   end-to-end latency.

The correct candidate count is therefore a system-design decision rather
than simply the configuration with the highest offline metric.

### Chunking is part of retrieval design

Chunk size and overlap affect:

-   semantic specificity;
-   recall;
-   duplicate retrieval;
-   context quality;
-   embedding/storage cost.

MemoryOS treats chunking as a retrieval decision rather than an
invisible preprocessing step.

------------------------------------------------------------------------

## Storage

The current implementation uses **PostgreSQL + pgvector** as the primary
storage and retrieval layer.

This keeps:

-   source content;
-   embeddings;
-   vector retrieval;
-   lexical retrieval;

inside the same database rather than introducing a separate vector
database.

A chunk currently contains the core fields used by retrieval:

``` text
id
content
source
embedding
```

The repository layer exposes operations for inserting chunks, vector
similarity search, and PostgreSQL full-text search.

------------------------------------------------------------------------

## Corpus

Corpus loading currently reads files recursively from:

``` text
data/documents/
```

Text is normalized before ingestion. Markdown parsing also extracts a
body and metadata separately so temporal/metadata-aware retrieval can
evolve without silently changing the existing semantic baseline.

------------------------------------------------------------------------

## Tech stack

  Area                   Technology
  ---------------------- ------------------------------------
  Language               Python
  Database               PostgreSQL 15
  Vector search          pgvector
  Embeddings             Sentence Transformers
  Embedding model        `all-MiniLM-L6-v2`
  Lexical retrieval      PostgreSQL Full Text Search
  Fusion                 Reciprocal Rank Fusion
  Reranking              Sentence Transformers CrossEncoder
  Reranker               `ms-marco-MiniLM-L6-v2`
  Database client        psycopg2
  Infrastructure         Docker Compose
  Supporting libraries   NumPy, PyYAML, LangChain utilities

------------------------------------------------------------------------

## Repository layout

The repository contains both the **current retrieval implementation**
and scaffolding/design for the broader MemoryOS architecture.

``` text
memory-os/
├── apps/
│   └── api/
│       ├── app/
│       │   ├── core/
│       │   │   ├── rrf.py
│       │   │   └── rerank.py
│       │   ├── retrieval/
│       │   │   ├── hybrid.py
│       │   │   └── semantic_search.py
│       │   ├── memory/
│       │   ├── db.py
│       │   └── repository.py
│       └── utils/
│           └── helper.py
├── data/
├── docs/
├── experiments/
├── infra/
│   └── docker-compose.yml
├── scripts/
├── PROJECT.md
├── repo-structure.md
├── requirements.txt
└── Makefile
```

`repo-structure.md` also documents the intended larger architecture,
including API, worker, MCP, web, memory lifecycle, agent, evaluation,
and infrastructure modules. Some of those modules represent the **target
design rather than completed functionality**.

------------------------------------------------------------------------

## Getting started

### Prerequisites

You will need:

-   Python 3.10+ recommended;
-   Docker;
-   PostgreSQL with pgvector, or the included Docker service.

### 1. Clone the repository

``` bash
git clone https://github.com/pratham-srivastava-07/memory-os.git
cd memory-os
```

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

Linux/macOS:

``` bash
source .venv/bin/activate
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector

The repository includes a Docker Compose configuration using:

``` text
pgvector/pgvector:pg15
```

Start it with:

``` bash
docker compose -f infra/docker-compose.yml up -d
```

The development database configuration in that Compose file is:

``` text
host: localhost
port: 5432
database: memory-db
user: postgres
password: postgres
```

### 5. Configure the database connection

The current Python database module reads connection settings from a
root-level `CONFIG.yml`.

Create one locally:

``` yaml
database:
  host: localhost
  port: 5432
  name: memory-db
  user: postgres
  password: postgres
  sslmode: disable
```

> `CONFIG.yml` should remain local if it contains real credentials. The
> repository's `.env.example` is currently empty, so configuration is
> not yet fully standardized around environment variables.

### 6. Prepare the database

The retrieval code expects a `chunks` table with vector embeddings and
PostgreSQL full-text-search support.

At minimum, the running schema must provide the fields referenced by the
repository layer:

``` text
id
content
source
embedding
content_tsv
```

and the `vector` extension must be enabled.

### 7. Add corpus documents

Place source documents under:

``` text
data/documents/
```

The corpus loader recursively discovers files from this directory.

------------------------------------------------------------------------

## Using the retrieval pipeline

The main hybrid retrieval entry point is:

``` python
from apps.api.app.retrieval.hybrid import hybrid_retrieve

results = hybrid_retrieve(
    query="What database did the team decide to use?",
    k=5,
    candidate_k=20,
    use_reranker=True,
)

for result in results:
    print(result["source"])
    print(result["content"])
    print(result.get("rerank_score"))
```

To collect component timings:

``` python
timings = {}

results = hybrid_retrieve(
    query="What database did the team decide to use?",
    k=5,
    candidate_k=20,
    use_reranker=True,
    timings=timings,
)

print(timings)
```

The timing dictionary can contain:

``` text
embedding_ms
vector_search_ms
lexical_search_ms
rrf_ms
reranker_ms
total_ms
```

For an RRF-only run:

``` python
results = hybrid_retrieve(
    query="What database did the team decide to use?",
    k=5,
    candidate_k=20,
    use_reranker=False,
)
```

This makes A/B comparisons between hybrid retrieval with and without
reranking straightforward.

------------------------------------------------------------------------

## Why RRF instead of score averaging?

The semantic path and lexical path produce fundamentally different
scores.

A vector similarity score and a PostgreSQL `ts_rank_cd` score do not
have equivalent meanings or distributions. Naively adding or averaging
them can make one retrieval system dominate because of scale rather than
relevance.

RRF avoids that problem by combining **rank order**:

``` text
semantic ranking -----+
                      +--> RRF --> fused ranking
lexical ranking ------+
```

This keeps the fusion method simple and avoids arbitrary score
calibration.

------------------------------------------------------------------------

## Roadmap

The retrieval core is the first layer of a larger memory/context system.

### Near-term retrieval work

-   component-level latency breakdown;
-   quantify RRF-only vs. RRF + CrossEncoder quality/latency;
-   finalize candidate-pool size;
-   graded relevance labels;
-   nDCG@K;
-   larger development/test evaluation splits;
-   statistical confidence intervals;
-   query/candidate caching experiments.

### Temporal and latest-state retrieval

A major next problem is conflicting knowledge over time.

For example:

``` text
January:  "We are evaluating MongoDB."
February: "PostgreSQL has been selected."
March:    "The PostgreSQL migration is complete."
```

For:

``` text
What database are we using?
```

semantic similarity alone may retrieve all three passages.

The system eventually needs to distinguish:

``` text
historical
superseded
current
```

This leads into temporal retrieval and memory lifecycle semantics.

### Long-term MemoryOS direction

``` text
Retrieval
   |
Hybrid Search
   |
Reranking
   |
Temporal Knowledge
   |
Context Construction
   |
Memory
   |
Agent Context
```

Future areas include:

-   episodic memory;
-   semantic memory;
-   memory consolidation;
-   memory promotion;
-   temporal decay;
-   superseded knowledge;
-   entity-aware retrieval;
-   context/token budgeting;
-   agent-specific memory;
-   provenance and source attribution;
-   persistent agent-facing retrieval interfaces.

------------------------------------------------------------------------

## What MemoryOS is not

MemoryOS is currently **not** a finished general-purpose memory platform
or a complete agent framework.

The checked-in, working center of gravity is the retrieval/evaluation
layer. The broader memory, agent, worker, MCP, and web structure
represents the direction in which the project is evolving.

That distinction is intentional: each layer should earn its complexity
through measurable improvements before becoming part of the system.

------------------------------------------------------------------------

## Project principle

> **The hardest part of a reliable AI system often happens before
> generation: deciding what information the model should see.**

MemoryOS is an exploration of the retrieval algorithms, evaluation
methodology, storage infrastructure, and eventually memory semantics
required to make that decision reliably.

------------------------------------------------------------------------

## Author

Built by [Pratham Srivastava](https://github.com/pratham-srivastava-07).

Repository:
[github.com/pratham-srivastava-07/memory-os](https://github.com/pratham-srivastava-07/memory-os)
