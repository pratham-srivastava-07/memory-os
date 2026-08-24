---
doc_id: note_010
type: note
subtype: threat_model
title: "SEC-44 — multi-tenant isolation threat model"
author: Jonas Weiss
date: 2026-06-08
projects: [Arca, API v2, Migration]
tickets: [SEC-44]
tags: [security, threat-model, multi-tenancy, rls]
---

# SEC-44 — multi-tenant isolation threat model

Scope: Arca (all four services), `api-gateway`, and the Postgres schema being
designed under MIG-101. Not in scope: infrastructure, supply chain, the console.

## Assets

Customer document content and the derived chunks and embeddings. For Lumen Health
(`tnt_7731`) this is health information under a contract with specific processing
restrictions. For Northwind Retail and Calder Freight it is commercially sensitive
but not regulated.

## Findings

### Finding 1 — Tenant filtering is enforced only in application code (HIGH)

There are **147 query sites** across `arca-retrieve`, `arca-index`, `arca-ingest` and
the admin tooling that append `tenant_id` by hand. There is no mechanical enforcement.
One omission is a cross-tenant read.

This is not hypothetical. On 2026-03-11 an internal admin endpoint (`/admin/chunks`)
shipped to staging without a tenant filter. Caught in review before production. The
review caught it; nothing else would have.

**Recommendation:** enforce at the storage layer. If the Postgres migration proceeds,
row-level security gives us this directly — a missing filter returns zero rows instead
of another tenant's rows. This is the strongest argument I have for the migration and
it is not on Mei's list.

**Status 2026-07-17:** accepted in ADR-008, then narrowed in ADR-016 on performance
grounds. Severity reduced to MEDIUM because `TenantScopedQuery` plus the SEC-51 CI
check plus a nightly probe is a reasonable substitute. It is a substitute, not an
equivalent. See ADR-016 for my full position.

### Finding 2 — Two API protocols will mean two authorisation paths (MEDIUM)

If ADR-007 proceeds, GraphQL resolvers check scopes and REST middleware checks
scopes. These will drift. The drift will be silent and the failure is a cross-tenant
read through the path with the weaker check.

**Recommendation:** one authorisation path, whatever the protocol story is.

**Status 2026-07-22:** resolved by ADR-018. GraphQL removed, one middleware path.

### Finding 3 — Backfill role has BYPASSRLS (MEDIUM, accepted)

The migration backfill job needs to read and write across all tenants. It gets a role
with `BYPASSRLS`. That is correct and unavoidable; the control is that the credential
lives in a separate secret with its own rotation and is not available to any service.

**Recommendation:** delete the role when the migration completes. Currently nobody
owns that deletion.

**Status 2026-08-06:** still not owned. The role still exists. Raised again at retro.

### Finding 4 — Embedding content leaves the VPC if we use a hosted model (HIGH if realised)

Contractual, for `tnt_7731`. Any hosted inference provider is a new sub-processor,
30 days notice.

**Status:** not realised. ADR-005 keeps embeddings in-VPC. ADR-017 nearly broke this
for reranking and caught it in review. **This constraint has now come up twice and
been forgotten once. It should be a checklist item on any ADR that involves a
vendor,** not something I happen to be in the room for.
