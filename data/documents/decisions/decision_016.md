---
doc_id: decision_016
type: decision
adr_id: ADR-016
title: "Narrow RLS to the control plane; application-level filtering on the hot path"
date: 2026-07-17
status: accepted
deciders: [Jonas Weiss, Mei Lin Zhao, Daniel Okoye, Tomas Herrera]
project: Migration
project_id: PRJ-1103
tickets: [SEC-44, SEC-51, ARCA-301]
supersedes: [ADR-008]
superseded_by: []
tags: [security, multi-tenancy, rls, performance]
---

# ADR-016: Narrow RLS to the control plane

## Status

Accepted 2026-07-17. Partially supersedes ADR-008.

## Context

ADR-008 put RLS on all four `arca` tables. In staging the cost was 9% p95. In
production, at 60M rows across 32 partitions, it is worse: the RLS predicate is
applied per partition after partition pruning, and on the hydration query the planner
stops using the `(tenant_id, document_id)` index in favour of a parallel seq scan on
three partitions. Measured: hydration p95 goes from 38 ms to 156 ms with RLS on.

ADR-012 gives hydration 40 ms. We are 4x over on that stage alone.

Jonas's position, stated in the review: RLS was never the control, it was the
backstop. The control is that `arca-retrieve` builds every query through one query
builder. The backstop matters most where a human writes ad-hoc SQL, which is the
control plane and the admin tooling, not the hot path.

## Decision

- **Keep RLS** on `arca.tenants` and on the control-plane schema. These are low-volume
  and human-accessed.
- **Drop RLS** on `arca.chunks` and `arca.documents` for the service role used by
  `arca-retrieve`. Keep the policies defined and keep them enforced for every other
  role, including anything a person logs in as.
- **Add a compensating control**: `arca-retrieve` may only construct queries through
  `TenantScopedQuery`, and a CI check (SEC-51) fails the build on any raw SQL string
  in the retrieval path that does not go through it. Karen owns the check.
- **Add a detection control**: a nightly job issues a known cross-tenant probe query
  as the service role and alerts if it ever returns rows.

## Consequences

- We traded a preventive control for a preventive-plus-detective pair that is weaker
  in the worst case and 4x faster in the common case. This is a real reduction in
  isolation guarantees and Jonas wants it re-reviewed before any customer with a
  contractual isolation requirement onboards. Lumen Health (`tnt_7731`) is already
  one; Jonas's sign-off is scoped to the current data set and expires 2026-10-01.
- `arca-ingest` and `arca-index` keep RLS. They are not latency-sensitive.
- SEC-44 stays open with reduced severity. SEC-51 is new and blocks the next release.
