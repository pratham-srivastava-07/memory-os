---
doc_id: meeting_014
type: meeting
title: "Arca Architecture Review #4 — cut short, incident triage INC-2026-0617"
date: 2026-06-18
time: "12:00–12:25 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Tomas Herrera, Priya Raman, Elliot Vance, Ravi Menon, Mei Lin Zhao]
projects: [Arca]
tickets: [ARCA-301, MIG-118]
incidents: [INC-2026-0617]
tags: [architecture, incident, review, cut-short]
---

# Arca Architecture Review #4 — 2026-06-18

Agenda was multi-tenancy and RLS. We got twenty minutes in before it turned into
incident follow-up. Multi-tenancy moves to the postmortem week.

**Tomas:** Before the agenda — everyone has seen yesterday's incident. Three hours on
`arca-retrieve`, EU region, elevated errors from 16:40 to 19:35 UTC. Full postmortem
is tomorrow. I want to flag one thing here because it is architectural.

**Daniel:** Go on.

**Tomas:** The deploy that caused it went out at 16:40. The person who deployed it
logged off at 17:00. I was paged at 17:12 and I had no idea what had changed. It took
me forty minutes to find the diff. Forty minutes of a three-hour incident was me
reading git log.

**Priya:** That is a process problem, not an architecture problem.

**Tomas:** The architecture problem is that four services means four deploy streams
and I cannot hold four deploy streams in my head. I need the alert to tell me what
deployed recently, or I need people to not deploy at 16:40 and leave.

**Daniel:** Both.

**Ravi:** In my last job we had a rule: if you deploy, you stay for an hour. It was
unpopular for about two weeks and then it was just how it worked.

**Priya:** I like that. Write it up as a policy, we will take it at the postmortem.

**Elliot:** Can I add one thing to tomorrow? During the incident, retrieval was
serving from Mongo, because we have not cut over. If this had happened after cutover,
with a Postgres primary under load, I do not know what the failure looks like. Nobody
does.

**Mei:** That is a fair thing to raise and it is not a reason to delay. It is a reason
to do a game day.

**Priya:** Add it to the postmortem actions. We are done here, agenda moves to the
next review.

## Carried over

- Multi-tenancy and RLS design review → 2026-07-02
- HNSW build time scaling (Tomas, from 2026-06-04) → not started

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Draft deploy policy for postmortem discussion | Ravi | 2026-06-19 |
| 2 | Add "post-cutover failure mode" to postmortem agenda | Elliot | 2026-06-19 |
