---
doc_id: meeting_026
type: meeting
title: "Migration go/no-go #2 — outcome: GO"
date: 2026-07-27
time: "09:00–09:30 UTC"
attendees: [Priya Raman, Mei Lin Zhao, Ravi Menon, Daniel Okoye, Karen Oyelaran, Elliot Vance]
apologies: [Tomas Herrera, Sofia Nyberg, Jonas Weiss]
projects: [Migration]
tickets: [MIG-112, MIG-118, MIG-124, MIG-136]
tags: [migration, go-no-go, decision, cutover]
---

# Migration go/no-go #2 — 2026-07-27

Second and, per ADR-015, final go/no-go. Tomas is out; he reviewed the runbook before
leaving and sent a written position.

## Checklist

| Criterion | Required | Actual | Pass |
|---|---|---|---|
| Backfill complete | 100% | 100% | yes |
| Divergence audit at 100% sampling | zero unexplained | zero unexplained | yes |
| Dual-write retry lag p99 | < 60 s | 6 min spikes | **no** |
| Cutover runbook reviewed (MIG-124) | yes | yes, by Tomas | yes |
| Rollback rehearsed on a real tenant | yes | yes, `tnt_9017` | yes |
| SRE available in window | yes | Daniel primary, Ravi secondary | yes |
| Karen sign-off, unconditional | yes | yes | yes |

Six of seven. The one failure is the same one that failed in June, improved twentyfold
and still not inside the stated bar.

**Priya:** Mei, this is your call to make and I will back it either way.

**Mei:** Go. Here is the reasoning, and I want it recorded because I am consciously
accepting a criterion we set and did not meet.

Six minutes of staleness matters if it is invisible and permanent. It is neither. The
flip is per tenant and reversible for two weeks. Karen's tooling asserts zero
divergence for a tenant immediately before it flips, so we do not flip a tenant that
is behind. And we flip smallest first, so the tenants with the write patterns that
produce lag are last, when we have six hours of evidence.

**Daniel:** What is the abort condition?

**Mei:** Any tenant showing non-zero divergence after flip. Any error rate above 1% on
`/v1/retrieve` for five minutes. Any Postgres replica lag above 30 seconds. Any of
those and we stop where we are — we do not roll back the ones already flipped unless
they are the problem.

**Ravi:** And I am running the flips, Mei is watching the numbers.

**Mei:** Yes. One person's hands, one person's eyes.

**Karen:** My assertion runs pre-flip per tenant and post-flip at five minutes.

**Elliot:** I will have the eval harness running against production traffic samples
before and after. If retrieval quality moves I will see it within the hour.

**Priya:** Tomas's written position, for the record: "The rollback rehearsal is the
thing I cared about and it is done. Six minutes of retry lag on a reversible per-tenant
flip is a risk I would take. Do not let anyone start the reindex in the same window."

**Mei:** We are not starting the reindex. That is after dual write comes off.

**Priya:** GO. Window is tonight, 22:00 UTC to 02:00 UTC. Mei runs it, Ravi executes,
Daniel is on call, Karen and Elliot on verification. Nobody else needs to be awake.

## Decision

**GO.** Read cutover 2026-07-27 22:00 UTC. The retry-lag criterion is knowingly
waived, with the compensating controls above recorded.

