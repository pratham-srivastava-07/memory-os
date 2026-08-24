---
doc_id: project_api
type: project_doc
title: "Project API — Meridian Public API v2"
project: API v2
project_id: PRJ-1088
status: active
owner: Ava Duarte
created: 2026-05-18
last_updated: 2026-06-30
tags: [api, graphql, rest, public-api, living-doc]
---

# Project API — Meridian Public API v2 (PRJ-1088)

Owner: Ava Duarte. Product partner: Sofia Nyberg.

## Goal

Replace the v1 API, which grew organically around the console, with a versioned,
documented, rate-limited public surface. Design partners for v2 are Northwind Retail
(`tnt_8842`), Calder Freight (`tnt_9017`), and Lumen Health (`tnt_7731`).

## Protocol

*Reviewed 2026-06-12.*

Per ADR-007 the shape is split:

- **Internal consumers** (`meridian-console`, `arca-eval`) talk GraphQL through
  `api-gateway`. The console needs to compose four or five resources per screen and
  the round trips are what customers notice.
- **External consumers** get REST and JSON over HTTPS. Cursor pagination, `ETag` on
  every collection, problem+json errors.

The GraphQL gateway spike is API-52. Schema lives in `api-gateway/schema/`.

## Resource model

*Reviewed 2026-06-30.*

```
/v2/documents
/v2/documents/{document_id}
/v2/documents/{document_id}/chunks
/v2/collections
/v2/retrieve            (POST, the interesting one)
/v2/jobs/{job_id}
```

`/v2/retrieve` is a thin pass-through to `arca-retrieve`. It inherits the Arca latency
budget; anything Arca does to that budget shows up here.

## Auth

API keys scoped per tenant, exchanged for short-lived tokens. Scopes: `read`,
`write`, `retrieve`, `admin`. See API-63. Jonas signed off on the scope model on
2026-06-08 with one open finding (SEC-44).

## Rate limiting

Token bucket per API key, 600 requests/minute burst 60 (API-58). Northwind Retail
asked for 2000/min during their backfill; Sofia approved a temporary override that
expires 2026-08-31.

## v1 deprecation

*Reviewed 2026-06-02.*

- 2026-06-15 — v2 beta opens to design partners
- 2026-08-01 — v1 marked deprecated in docs, `Sunset` header added
- **2026-09-01 — v1 shut off**

Comms tracked in API-77. Sofia owns the customer email.

## Open tickets

| Ticket | Description | State |
|---|---|---|
| API-40 | v2 OpenAPI spec | in review |
| API-52 | GraphQL gateway spike | in progress |
| API-58 | Rate limiting | done |
| API-63 | Auth scopes | in progress |
| API-71 | REST resource model | in progress |
| API-77 | v1 deprecation comms | not started |
