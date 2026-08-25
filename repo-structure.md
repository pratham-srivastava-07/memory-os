memoryos/
│
├── apps/
│   │
│   ├── api/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── router.py
│   │   │   │   └── v1/
│   │   │   │       ├── documents.py
│   │   │   │       ├── search.py
│   │   │   │       ├── memories.py
│   │   │   │       ├── conversations.py
│   │   │   │       └── health.py
│   │   │   │
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── logging.py
│   │   │   │   ├── security.py
│   │   │   │   └── telemetry.py
│   │   │   │
│   │   │   ├── db/
│   │   │   │   ├── session.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── document.py
│   │   │   │   │   ├── chunk.py
│   │   │   │   │   ├── memory.py
│   │   │   │   │   ├── episode.py
│   │   │   │   │   └── user.py
│   │   │   │   └── repositories/
│   │   │   │       ├── documents.py
│   │   │   │       ├── chunks.py
│   │   │   │       └── memories.py
│   │   │   │
│   │   │   ├── ingestion/
│   │   │   │   ├── loaders/
│   │   │   │   │   ├── text.py
│   │   │   │   │   ├── markdown.py
│   │   │   │   │   └── pdf.py
│   │   │   │   ├── chunking/
│   │   │   │   │   ├── base.py
│   │   │   │   │   └── recursive.py
│   │   │   │   ├── embeddings/
│   │   │   │   │   ├── base.py
│   │   │   │   │   └── provider.py
│   │   │   │   └── pipeline.py
│   │   │   │
│   │   │   ├── retrieval/
│   │   │   │   ├── semantic.py
│   │   │   │   ├── lexical.py
│   │   │   │   ├── hybrid.py
│   │   │   │   ├── reranking.py
│   │   │   │   └── context.py
│   │   │   │
│   │   │   ├── memory/
│   │   │   │   ├── extraction.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── semantic.py
│   │   │   │   ├── promotion.py
│   │   │   │   ├── contradiction.py
│   │   │   │   ├── decay.py
│   │   │   │   └── provenance.py
│   │   │   │
│   │   │   ├── agent/
│   │   │   │   ├── agent.py
│   │   │   ├── state.py
│   │   │   ├── planner.py
│   │   │   ├── tools.py
│   │   │   └── policies.py
│   │   │   │
│   │   │   └── llm/
│   │   │       ├── client.py
│   │   │       ├── prompts/
│   │   │       ├── structured.py
│   │   │       └── token_budget.py
│   │   │
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── fixtures/
│   │   │
│   │   └── pyproject.toml
│   │
│   ├── worker/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── jobs/
│   │   │       ├── ingestion.py
│   │   │       ├── embedding.py
│   │   │       ├── memory_extraction.py
│   │   │       ├── memory_promotion.py
│   │   │       └── cleanup.py
│   │   └── pyproject.toml
│   │
│   ├── mcp-server/
│   │   ├── src/
│   │   │   ├── server.py
│   │   │   ├── tools/
│   │   │   │   ├── search_memory.py
│   │   │   │   ├── get_memory.py
│   │   │   │   ├── get_episode.py
│   │   │   │   └── update_memory.py
│   │   │   └── resources/
│   │   └── pyproject.toml
│   │
│   └── web/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── package.json
│
├── packages/
│   ├── contracts/
│   │   ├── memory.py
│   │   ├── retrieval.py
│   │   └── agent.py
│   │
│   └── evals/
│       ├── datasets/
│       ├── scenarios/
│       ├── metrics/
│       └── runner.py
│
├── infra/
│   ├── docker/
│   │   ├── api.Dockerfile
│   │   ├── worker.Dockerfile
│   │   └── mcp.Dockerfile
│   │
│   ├── compose/
│   │   └── docker-compose.yml
│   │
│   └── migrations/
│
├── scripts/
│   ├── seed.py
│   ├── ingest.py
│   └── evaluate.py
│
├── data/
│   ├── seed/
│   └── eval/
│
├── docs/
│   ├── architecture.md
│   ├── retrieval.md
│   ├── memory.md
│   ├── agent.md
│   ├── evaluation.md
│   ├── decisions/
│   │   ├── 001-postgres.md
│   │   ├── 002-hybrid-search.md
│   │   └── 003-memory-promotion.md
│   └── api/
│
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
│
├── .env.example
├── docker-compose.yml
├── Makefile
├── README.md
└── .gitignore