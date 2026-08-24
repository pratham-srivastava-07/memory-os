---
doc_id: meeting_012
type: meeting
title: "API v2 protocol decision — REST vs GraphQL"
date: 2026-06-11
time: "14:00–15:15 UTC"
attendees: [Ava Duarte, Daniel Okoye, Sofia Nyberg, Priya Raman, Jonas Weiss, Karen Oyelaran]
apologies: [Mei Lin Zhao]
projects: [API v2]
tickets: [API-40, API-52, API-63, API-71, SEC-44]
decisions: [ADR-007]
tags: [api, graphql, rest, decision]
---

# API v2 protocol decision — 2026-06-11

Scheduled at 14:00 UTC to catch Ava's morning. Mei sent apologies (22:00 SGT) and
noted she has no view on the protocol.

**Ava:** The console makes nine calls to render document detail. 1.4 seconds to first
paint on a median connection. That is the problem I am solving. Design partners, all
three of them, asked for REST with an OpenAPI file and none of them asked for
GraphQL. So: GraphQL for us, REST for them.

**Daniel:** My objection, which is in the doc. A GraphQL gateway in front of a service
that already has a query planner gives us two query planners. The interesting failures
live in the seam between them and nobody owns the seam.

**Ava:** DataLoader batching handles the fan-out.

**Daniel:** Per request. One GraphQL query that touches a document with two thousand
chunks fans out to how many calls into `arca-retrieve`?

**Ava:** Batched, so bounded by the batch size. I would have to measure it.

**Daniel:** Measure it before, not after.

**Jonas:** My objection. Two protocols is two auth paths. GraphQL checks scopes in
resolvers, REST checks in middleware. Those will drift and the drift is a
cross-tenant read. I would rather have one surface with a worse ergonomics story than
two with a good one.

**Sofia:** Counter-proposal I have made before: REST everywhere, with an `expand`
parameter for composition. It is less elegant and it is one thing.

**Ava:** That is REST with GraphQL bolted on badly.

**Sofia:** Yes. It is also one auth path and one thing to document.

**Priya:** Ava, what do you need to believe to be wrong?

**Ava:** If the console gets under a second with `expand` and REST, I do not need
GraphQL. I do not think it does.

**Priya:** Then here is what I will accept. Do it your way, with two conditions.
API-52 is a time-boxed spike with a stated success criterion — console under one
second, one auth path or a written plan to converge them — and we review it at six
weeks. If it does not clear the bar we take Sofia's option and I do not want anyone
sulking about the three weeks.

**Ava:** Fine.

**Jonas:** I want my finding to stay open, not be closed by this decision.

**Priya:** It stays open.

**Karen:** Test matrix doubles. Same suite against two surfaces.

**Priya:** Noted, and that is a cost of the decision, not a reason to skip the tests.

## Decision

GraphQL for internal consumers, REST for external. ADR-007. Six-week review with a
stated bar. SEC-44 finding 2 stays open.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-007 including the review bar | Ava | 2026-06-12 |
| 2 | Measure resolver fan-out on a large document | Ava | 2026-06-26 |
| 3 | Book the six-week review | Priya | 2026-07-22 |
