---
doc_id: decision_009
type: decision
adr_id: ADR-009
title: "Deploy freeze windows"
date: 2026-06-22
status: accepted
deciders: [Priya Raman, Tomas Herrera, Daniel Okoye]
project: Team
tickets: [OPS-19]
supersedes: []
superseded_by: []
tags: [process, deploys, oncall]
---

# ADR-009: Deploy freeze windows

## Status

Accepted 2026-06-22. Written up after INC-2026-0617.

## Context

INC-2026-0617 started at 16:40 UTC on a Wednesday with a routine `arca-retrieve`
deploy. It was not a Friday and the freeze policy would not have prevented it. What
made it a 3-hour incident rather than a 20-minute one was that the person who
deployed had already logged off and the on-call had no context on the change.

Separately, Daniel has declined to review Friday deploys for as long as anyone can
remember and it has never been policy, just a thing he does.

## Decision

- No production deploys after **15:00 UTC on Thursday**.
- No production deploys on **Friday**, at all.
- Deploys outside those windows require the author to stay reachable for 60 minutes
  after the rollout completes. "Reachable" means in `#team-platform`.
- Hotfixes are exempt from the window but not from the 60-minute rule, and need an
  SRE acknowledging in the channel.

## Consequences

- The effective deploy week is Monday 09:00 to Thursday 15:00 UTC. Mei's working day
  ends at 10:00 UTC, so anything she ships lands in the morning window or waits.
- Release trains for `api-gateway` move from Friday to Wednesday.
- Ravi joins the on-call rotation from 2026-07-06 as a fourth, which was the actual
  blocker behind the "author stays reachable" rule.
