---
doc_id: decision_018
type: decision
adr_id: ADR-018
title: "Drop GraphQL; REST-only for API v2"
date: 2026-07-22
status: accepted
deciders: [Ava Duarte, Daniel Okoye, Sofia Nyberg, Priya Raman, Jonas Weiss]
project: API v2
project_id: PRJ-1088
tickets: [API-52, API-71, API-77, SEC-44]
supersedes: [ADR-007]
superseded_by: []
tags: [api, graphql, rest, reversal]
---

# ADR-018: Drop GraphQL; REST-only for API v2

## Status

Accepted 2026-07-22. Supersedes ADR-007.

## Context

ADR-007 split the API by audience: GraphQL internally, REST externally. Six weeks in,
Ava wrote up what actually happened (see her 2026-07-16 note):

- The DataLoader batching that was supposed to solve N+1 solves it per request. The
  document detail screen issues one GraphQL query that fans out to 340 calls into
  `arca-retrieve` for a document with many chunks. It was 6 calls before.
- Depth and complexity limiting turned into a tuning exercise nobody owns. The limit
  is currently set to a number Ava picked to make the console work.
- The two auth paths (SEC-44 finding 2) never converged. The GraphQL path validates
  scopes in resolvers; REST does it in middleware. Jonas will not sign off on
  shipping both.
- Console load time, the thing this was for, went from 1.4 s to 1.1 s. Real, but
  smaller than the 400 ms we later found in a single unbatched avatar endpoint.

Meanwhile all three design partners are building against REST and none has asked for
GraphQL.

## Decision

- Remove the GraphQL gateway. API-52 is closed as won't-do.
- `meridian-console` moves to the REST surface, using a `?expand=` parameter for
  composition — the option Sofia proposed in ADR-007 and we rejected.
- `?expand=` supports a fixed, enumerated set of expansions per resource. Not
  arbitrary nesting. Documented in the OpenAPI file.
- One auth path: middleware, scope-checked, shared by all consumers.

## Consequences

- Three weeks of Ava's work on API-52 is thrown away. Priya's framing in the meeting:
  the spike answered the question, which is what a spike is for.
- The console needs 4–6 new expansion parameters (API-71). Ava estimates 1.5 weeks.
- **v1 deprecation moves from 2026-09-01 to 2026-11-01.** The console rewrite eats
  the buffer we had, and Sofia will not shut off v1 while customers are still
  migrating to a v2 that changed shape under them. `project_api.md` still lists
  2026-09-01 and needs updating; API-77 is still not started.
