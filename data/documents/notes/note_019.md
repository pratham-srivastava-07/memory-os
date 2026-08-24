---
doc_id: note_019
type: note
subtype: writeup
title: "API-52 — what six weeks of GraphQL taught us"
author: Ava Duarte
date: 2026-07-21
projects: [API v2]
tickets: [API-52, API-63, API-71]
tags: [graphql, rest, retrospective, api, reversal]
---

# API-52 — what six weeks of GraphQL taught us

Pre-read for tomorrow's review. I argued for this in June. I am going to recommend we
drop it. Here is the working.

## The bar Priya set

1. Console document detail under one second
2. One auth path, or a written plan to converge them

## 1. Console latency

| | Before | After |
|---|---|---|
| Document detail, first paint | 1.42 s | 1.11 s |
| API calls per screen | 9 | 1 |

Under 1.2 s, not under 1 s. And while I was measuring I found that 400 ms of the
remaining time is an avatar endpoint that fetches user profiles one at a time in a
loop. It has nothing to do with API shape. Batching that one endpoint — half a day of
work — gets us to roughly 1.0 s on the *old* nine-call REST version.

So the honest statement is: GraphQL bought us about 310 ms, and there was 400 ms
sitting in a stupid loop the whole time.

## 2. Fan-out

One GraphQL query for a document with 2,000 chunks produces **340 calls** into
`arca-retrieve`. Batched, with DataLoader, as designed.

DataLoader batches within a request. The chunk resolver is called per chunk; batching
collapses those into pages of the batch size. More chunks, more batches. The batching
works exactly as documented and the number is still 340, where REST was 6.

Daniel said this in the June meeting almost word for word and I told him DataLoader
handled it. It handles it. Handling it is not the same as it being fine.

## 3. Auth

Still two paths. Resolvers check scopes for GraphQL, middleware checks for REST.

I tried three times to write the convergence plan Priya asked for. Every version ends
with "and then authorisation only happens in middleware", at which point resolvers are
doing nothing that REST handlers do not do, at which point the GraphQL layer is a
query-composition feature and nothing else. Which is the `expand` parameter.

## 4. The depth limiter

Set to 8. I chose 8 by starting at 4 and raising it until the console stopped
erroring. There is no principle behind it. Nobody owns it. If a customer ever gets on
this surface it is a denial-of-service parameter chosen by trial and error.

*(No customer will get on this surface, because we are not shipping it externally.
But we built the internal surface as if it were external, and then chose its safety
parameter by guessing.)*

## What I would do instead

REST only. `expand` with a fixed, enumerated set of expansions per resource. Not
arbitrary nesting — `?expand=chunks,collection` and that is the whole grammar. It goes
in the OpenAPI file, it goes through the same middleware, it is one auth path, and
Karen's test matrix halves.

Cost: 4–6 expansion parameters, three console screens rewritten, about a week and a
half. And it means the v1 shutoff has to move, because I am not asking customers to
migrate to a surface that changed shape in August with a September deadline.

## What I want on the record

I do not think the six weeks were wasted, and I would be annoyed if anyone framed it
that way. Nobody had the 340 number in June. We have it because we built the thing.
The review with a written bar is what made this end in a decision instead of a
year of nobody wanting to say it.
