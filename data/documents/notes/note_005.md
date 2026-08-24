---
doc_id: note_005
type: note
subtype: research
title: "API v2 design partner interviews"
author: Ava Duarte
date: 2026-05-18
projects: [API v2]
tickets: [API-40]
tags: [customer-research, api, interviews]
---

# API v2 design partner interviews

Three calls, 45 minutes each. Northwind Retail (`tnt_8842`), Calder Freight
(`tnt_9017`), Lumen Health (`tnt_7731`).

## Northwind Retail

Talked to their platform lead. They are building an internal search product on top of
us for 4,000 store managers.

- Wants REST with an OpenAPI file. Said "we generate our clients, so give me a spec".
- Asked about rate limits before anything else. They want to backfill 2M documents
  and 600/min will take them forever. **Follow up on a temporary increase.**
- Does not care about response shape efficiency. Their client is a backend service.
- Volunteered, unprompted: "search gets worse the more we put in". Asked whether that
  was expected. I said I would find out. *(I did not follow up on this. It became the
  escalation six weeks later.)*

## Calder Freight

Two engineers, one of them clearly the decision maker.

- Same ask: OpenAPI, generated clients.
- They want webhooks on ingest completion rather than polling `/v2/jobs`. Not in
  scope for v2 but worth logging.
- Asked about versioning policy. What happens when v3 exists. Good question, I did
  not have an answer.
- Pushed hard on error format. They want machine-readable error codes, not prose.
  problem+json satisfies this.

## Lumen Health

Most constrained of the three and the most interesting call.

- Their security team was on the call, not their engineers.
- Data residency is the whole conversation. EU only, and any sub-processor we add
  needs 30 days' notice. **This is contractual, not a preference.**
- They asked specifically whether document content is sent to any third party for
  embedding. I said no. I should confirm that is actually true and stays true.
- REST, obviously. Their integration is a compliance artefact as much as software.

## What I take from this

Three for three want REST and an OpenAPI file. None of them mentioned GraphQL and
when I raised it, two of them said some version of "we would not use it".

That is not the same as saying we should not build it. Our own console is the client
with the performance problem, and no customer is going to advocate for the thing that
makes our console fast. But I should stop describing GraphQL as something customers
want, because it is not.
