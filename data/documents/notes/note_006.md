---
doc_id: note_006
type: note
subtype: strategy
title: "Test strategy for a four-service Arca"
author: Karen Oyelaran
date: 2026-05-21
projects: [Arca]
tickets: [ARCA-233]
tags: [testing, playwright, strategy, preferences]
---

# Test strategy for a four-service Arca

Written because ADR-001 splits us into four deployables and my current suite assumes
one process.

## Position on tooling, so nobody has to ask twice

Playwright for anything browser-driven. The Cypress migration finished on 12 May and
Cypress is deleted from the repo. I am not relitigating this. The reasons, once:
multi-tab, real network interception, and a debugging story that does not require me
to guess.

For service-level tests: pytest, real processes, real Postgres and Mongo in
containers. No mocks between our own services. A mock of `arca-rank` is a test of my
assumptions about `arca-rank`.

## The compose file

One compose file. It runs locally and it runs in CI, byte for byte. The moment there
is a `docker-compose.ci.yml` it will drift and the CI one will be the one nobody can
reproduce.

## Layers

1. **Unit** — in each repo, fast, no I/O. Owned by whoever writes the code.
2. **Service contract** — each service against its own dependencies, real. Owned by
   the service owner.
3. **Cross-service** — all four up, real data, the paths that matter. Mine.
4. **Browser** — console against a real stack. Mine.

## What I cannot test today and it bothers me

- **Production query mix.** Everything above runs synthetic queries. Our synthetic
  mix has candidate counts under 100 because that is what I wrote in 2025. If someone
  changes a limit, my tests will not notice.
- **Failure under load.** I test that things work. I do not test that they degrade
  well, because I have no load harness.
- **Anything about retrieval quality.** A test can tell you the API returned 200. It
  cannot tell you the results got worse. Elliot's harness is the answer and it is not
  mine.

## What I want from the team

When you split a service out, the contract tests come with it in the same PR. Not
after. "We will add tests once it stabilises" means never, and I will say so in
review every time.
