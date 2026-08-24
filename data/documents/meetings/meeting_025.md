---
doc_id: meeting_025
type: meeting
title: "API-52 six-week review — GraphQL spike outcome"
date: 2026-07-22
time: "14:00–15:00 UTC"
attendees: [Ava Duarte, Daniel Okoye, Priya Raman, Jonas Weiss, Karen Oyelaran]
apologies: [Sofia Nyberg, Mei Lin Zhao]
projects: [API v2]
tickets: [API-52, API-63, API-71, API-77, SEC-44]
decisions: [ADR-018]
tags: [api, graphql, rest, reversal, spike-review]
---

# API-52 six-week review — 2026-07-22

The review Priya set as a condition in ADR-007. Bar was: console under one second,
and one auth path or a written plan to converge them.

**Ava:** I will give you the numbers and then my recommendation, and my
recommendation is not the one I argued for in June.

Console document detail: 1.4 s before, 1.1 s now. Real, and under the bar only if you
squint. And I found 400 ms of it in an unbatched avatar endpoint that has nothing to
do with the API shape. Fixing that one endpoint would have got most of the win without
any of this.

Fan-out: a document with 2,000 chunks produces 340 calls into `arca-retrieve` from one
GraphQL query, batched. It was six.

Depth limiting: I set the limit by raising it until the console stopped erroring.
There is no principle behind the number and nobody owns it.

Auth: still two paths. Resolvers for GraphQL, middleware for REST. I do not have a
written plan to converge them because every version I wrote ended with "and then we
would only have middleware", which is just REST.

**Jonas:** Then I do not sign it. Two auth paths, six weeks in, no convergence plan.

**Priya:** Ava, your recommendation.

**Ava:** Drop it. REST only, `expand` parameter for composition, fixed enumerated
expansions rather than arbitrary nesting. Which is Sofia's proposal from June, which I
called REST with GraphQL bolted on badly.

**Daniel:** For what it is worth, I was against this in June and I do not think that
means I was right. The fan-out number is the thing that decides it and nobody had it
in June. We have it because we spent the six weeks.

**Priya:** That is the framing I want in the ADR. The spike answered the question.
That is what a spike is for. Nobody wasted three weeks.

**Karen:** My test matrix halves. I am not sad.

**Ava:** One consequence that is not free. The console needs four to six expansion
parameters and a rewrite of three screens. A week and a half. That eats the buffer
we had before the v1 shutoff.

**Priya:** So v1 moves.

**Ava:** v1 has to move. 1 September is not survivable if v2 changes shape in August.

**Priya:** What date?

**Ava:** 1 November. And Sofia has to agree, and she is out until the 3rd.

**Priya:** Put 1 November in the ADR as the decision, flag that Sofia confirms on her
return. And API-77 still has not started, which is the actual risk here — we have
moved the date twice in a project doc and never told a customer anything.

## Decision

Drop GraphQL. REST only for API v2, `expand` for composition, one auth path.
ADR-018, supersedes ADR-007. v1 shutoff moves from 2026-09-01 to 2026-11-01.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-018 | Ava | 2026-07-22 |
| 2 | Close API-52 as won't-do, delete the gateway | Ava | 2026-07-31 |
| 3 | Expansion parameters (API-71) | Ava | 2026-08-07 |
| 4 | Confirm 1 November with Sofia | Priya | 2026-08-04 |
| 5 | Start API-77 deprecation comms | Sofia | 2026-08-07 |
