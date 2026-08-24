---
doc_id: meeting_017
type: meeting
title: "Migration go/no-go #1 — outcome: NO-GO"
date: 2026-06-25
time: "12:00–12:40 UTC"
attendees: [Mei Lin Zhao, Tomas Herrera, Priya Raman, Ravi Menon, Karen Oyelaran, Sofia Nyberg, Daniel Okoye]
projects: [Migration]
tickets: [MIG-112, MIG-118, MIG-124, MIG-136]
decisions: [ADR-010]
tags: [migration, go-no-go, slip, decision]
---

# Migration go/no-go #1 — 2026-06-25

Decision meeting for the read cutover originally scheduled 2026-06-22.

## Go/no-go checklist

| Criterion | Required | Actual | Pass |
|---|---|---|---|
| Backfill complete | 100% | 64% | no |
| Divergence audit at 100% sampling | complete | not started | no |
| Dual-write retry lag under 60 s at p99 | < 60 s | 41 min peak | no |
| Cutover runbook reviewed (MIG-124) | yes | draft | no |
| Rollback rehearsed | yes | no | no |
| SRE available | yes | yes | yes |
| Karen sign-off on test plan | yes | conditional | partial |

**Priya:** One yes out of seven. Anyone want to argue for go?

*(nobody)*

**Priya:** No-go. Mei, the date.

**Mei:** 13 July. Three weeks. I laid out the reasoning on Tuesday: five days on
MIG-118, four days on a full divergence audit, and the rest is slack because the last
plan had none.

**Tomas:** I want the rollback rehearsed as a hard gate on the next go/no-go, not a
line item that is "in progress". We have never actually flipped a tenant back.

**Karen:** And I want the test plan sign-off to be unconditional next time. My
condition is that I can assert divergence is zero for a tenant before it flips, and
today I cannot, because the audit tooling does not exist.

**Ravi:** I can build that as part of the audit. It is the same query.

**Mei:** Then it is yours.

**Sofia:** Does anything I have told a customer change?

**Mei:** No. Nothing customer-visible moves.

**Sofia:** Good. I would like it to stay that way, and I would like to hear about it
in writing if it stops being true.

**Priya:** One more thing before we close, and I want it in the ADR. Tomas, when are
you out?

**Tomas:** 20 July to 10 August.

**Priya:** So a 13 July cutover puts the entire two-week dual-write safety period
inside your absence.

**Tomas:** It does. I flagged it in my 1:1.

**Priya:** We will deal with it at the next go/no-go. I do not want to move the date
twice in one meeting.

*(This is the constraint that produces the second slip on 2026-07-15. It is discussed
here and does not appear in ADR-010.)*

## Decision

**NO-GO.** Read cutover moves to 2026-07-13. ADR-010.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-010 | Mei | 2026-06-26 |
| 2 | MIG-118 fix | Ravi | 2026-06-30 |
| 3 | Divergence audit tooling, per-tenant zero-divergence assertion | Ravi | 2026-07-06 |
| 4 | Rehearse rollback, hard gate next time | Tomas | 2026-07-10 |
| 5 | Finish MIG-124 cutover runbook | Mei | 2026-07-06 |
