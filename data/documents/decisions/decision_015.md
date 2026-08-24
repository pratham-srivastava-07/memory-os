---
doc_id: decision_015
type: decision
adr_id: ADR-015
title: "Read cutover moved from 2026-07-13 to 2026-07-27"
date: 2026-07-15
status: accepted
deciders: [Priya Raman, Mei Lin Zhao, Sofia Nyberg]
project: Migration
project_id: PRJ-1103
tickets: [MIG-118, MIG-124, MIG-136]
supersedes: [ADR-010]
superseded_by: []
tags: [migration, schedule, slip]
---

# ADR-015: Read cutover moved to 2026-07-27

## Status

Accepted 2026-07-15. Supersedes ADR-010. This is the second slip.

## Context

The 2026-07-13 date did not hold. The stated blockers at the 2026-07-14 sync were
"an unresolved backfill defect and resourcing".

Concretely:

- MIG-118 was fixed and deployed on 2026-07-09, and the second rehearsal on
  2026-07-13 still showed 6-minute lag spikes under the Northwind Retail write
  pattern. Better than 41 minutes, not zero.
- Cutover requires an SRE on the call. Tomas is out from 2026-07-20 to 2026-08-10.
  Running it in the week of 13 July was possible on paper and would have put the
  entire two-week dual-write escape-hatch period inside his absence.

## Decision

Read cutover on **Monday 2026-07-27, 22:00 UTC**, with Tomas present, before he goes
out. Dual write stays on until 2026-08-10.

Downstream dates move accordingly: dual write off 2026-08-10, Mongo decommission
2026-08-14.

## Consequences

- Two weeks of dual write after cutover fall inside Tomas's absence with Daniel as
  primary SRE contact and Ravi as secondary. Ravi has been on the rotation for three
  weeks.
- This is the last date we will move. Priya said so in the sync and asked for it to
  be written here: if 2026-07-27 does not hold, we stop the project and re-plan
  rather than slipping a third time.
- `project_migration.md` timeline table needs updating. It says Mongo decommission
  2026-08-21, which is wrong in both directions and nobody has fixed it.
