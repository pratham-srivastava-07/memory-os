---
doc_id: decision_007
type: decision
adr_id: ADR-007
title: "API v2 protocol: GraphQL for internal consumers, REST for public"
date: 2026-06-12
status: superseded
deciders: [Ava Duarte, Daniel Okoye, Sofia Nyberg, Priya Raman]
project: API v2
project_id: PRJ-1088
tickets: [API-40, API-52, API-71]
supersedes: []
superseded_by: [ADR-018]
tags: [api, graphql, rest]
---

# ADR-007: API v2 protocol — GraphQL internal, REST public

## Status

**Superseded by ADR-018 (2026-07-22).**

## Context

`meridian-console` makes 6–9 API calls to render the document detail screen. On a
median customer connection that is 1.4 s before anything paints. Ava wants a single
composed request. Meanwhile external design partners have asked, unprompted, for
"a normal REST API with an OpenAPI file".

Daniel's objection, filed in writing before the meeting per the handbook: a GraphQL
gateway in front of a service that already has a query planner means two query
planners, and the interesting failure modes live in the seam.

## Decision

Split by audience.

- **Internal** (`meridian-console`, `arca-eval`): GraphQL, served by `api-gateway`,
  resolving against the same internal service calls the REST layer uses.
- **External** (customers): REST and JSON, OpenAPI 3.1, cursor pagination.

Both surfaces are generated from one internal resource model (API-71) so they cannot
drift in what they expose, only in how.

## Consequences

- `api-gateway` grows a schema, a resolver layer, and a depth/complexity limiter.
- Two auth paths to keep in sync. Jonas asked for this to be one code path and it is
  not, which is SEC-44's second finding.
- N+1 risk on the resolver layer. Ava's mitigation is DataLoader batching per request.

## Alternatives considered

- **REST everywhere with a `?expand=` parameter.** Sofia preferred it. Rejected as
  "REST with GraphQL bolted on badly", though ADR-018 later revisits exactly this.
- **GraphQL everywhere.** Rejected: rate limiting and cost attribution on arbitrary
  GraphQL queries is a research project, and we bill on request count.
