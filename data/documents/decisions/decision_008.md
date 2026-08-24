---
doc_id: decision_008
type: decision
adr_id: ADR-008
title: "Multi-tenant isolation via PostgreSQL row-level security"
date: 2026-06-19
status: partially-superseded
deciders: [Jonas Weiss, Mei Lin Zhao, Daniel Okoye]
project: Migration
project_id: PRJ-1103
tickets: [SEC-44, MIG-101]
supersedes: []
superseded_by: [ADR-016]
tags: [security, multi-tenancy, postgres, rls]
---

# ADR-008: Multi-tenant isolation via PostgreSQL row-level security

## Status

**Partially superseded by ADR-016 (2026-07-17).** RLS is retained on the control
plane; the hot retrieval path moved back to application-level filtering.

## Context

Jonas's threat model (SEC-44) put "cross-tenant data exposure through a missing
`WHERE tenant_id` clause" as the highest-severity realistic failure. It has already
happened once, in March, on an internal admin endpoint, caught before it shipped.

Every `arca-*` service currently appends `tenant_id` in application code. There are
147 query sites. One of them being wrong is a breach.

## Decision

Enable row-level security on `arca.documents`, `arca.chunks`, `arca.jobs` and
`arca.tenants`. Each request sets `SET LOCAL app.tenant_id` from the validated token
inside the transaction. Policies filter on `tenant_id = current_setting('app.tenant_id')::uuid`.

Services connect as a role without `BYPASSRLS`. The backfill job gets a separate role
that does have it, and that role's credentials live in a different secret.

## Consequences

- A missing filter becomes zero rows instead of another tenant's rows. This is the
  whole point.
- Every query now runs inside an explicit transaction so that `SET LOCAL` applies.
  This is a real change to `arca-retrieve`, which used autocommit.
- Query plans change. Jonas and Mei both flagged that RLS predicates can defeat index
  usage; Mei measured a 9% p95 regression on the hydration query in staging and
  called it acceptable. At production scale it was not — see ADR-016.

## Alternatives considered

- **Schema per tenant.** Real isolation, but 84 schemas today and migrations become a
  fan-out job. Rejected on operational cost.
- **Database per tenant.** Same, worse.
- **Keep application-level filtering and add a linter.** Rejected at the time as
  "a control that depends on people running it". Partly reinstated by ADR-016.
