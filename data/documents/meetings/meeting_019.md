---
doc_id: meeting_019
type: meeting
title: "Arca Architecture Review #5 — latency budget, RLS carried over"
date: 2026-07-02
time: "12:00–13:15 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Tomas Herrera, Elliot Vance, Priya Raman, Sofia Nyberg, Ravi Menon]
apologies: [Mei Lin Zhao, Jonas Weiss]
notes_sent_to: [Mei Lin Zhao, Jonas Weiss]
projects: [Arca]
tickets: [ARCA-301, ARCA-288, ARCA-317]
decisions: [ADR-012]
tags: [architecture, latency, slo, review]
---

# Arca Architecture Review #5 — 2026-07-02

Mei is running the recall benchmark and sent apologies. RLS review slips again, to
the 16th. That is the third time it has been carried.

## Latency budget

**Tomas:** I am going to do the thing I have been threatening since May. We have three
different latency numbers in three places. My SLO draft says p95 250 ms.
`project_arca.md` says 300 ms. Nobody can tell me where either came from. Last month
Sofia quoted 250 to a customer.

**Sofia:** I quoted the number in the document I was given.

**Tomas:** I know. That is the problem, not you. Here is the actual number: p95 over
the last 30 days at the gateway is **341 ms**. We have been missing both targets for
the entire time either target existed, and we never alerted, because until three weeks
ago the alert was on p50.

**Priya:** So the honest options are to fix the system or fix the number.

**Tomas:** Fix the number, and then fix the system against a number that means
something. And split it into sub-budgets, because "400 ms end to end" is not
actionable — I need to know that rerank owns 180 of it.

**Elliot:** That matters more than it sounds. ADR-011 takes chunks to 800 tokens,
which takes the reranker sequence length to 1024, which roughly doubles rerank cost
per candidate. On CPU that is 340 ms p95 for 50 candidates. It does not fit in 180.

**Daniel:** So the chunking decision has already spent the rerank budget.

**Elliot:** Yes. I should have connected those two things in the ADR and I did not.

**Priya:** Write the budget with the sub-budgets. The rerank one is going to force a
hosting decision and I would rather that be a decision than a surprise.

**Sofia:** What do I tell customers? 400 is worse than 250 and I have said 250.

**Priya:** "Sub-half-second retrieval." And you say it once, in writing, and we hold
to it.

**Tomas:** Error budget policy too. Two consecutive weeks above 50% burn freezes
feature work on `arca-retrieve`.

**Daniel:** Agreed, with the caveat that "feature work" needs a definition or we will
argue about it during an incident.

## Other

**Daniel:** ARCA-317, hybrid search, has been parked since 2 June. Northwind Retail's
second-biggest complaint is exact identifier search. I am picking it back up.

**Priya:** Yours, then. But you also own AI-1 follow-ups and ARCA-301.

**Daniel:** It is mine.

*(ARCA-317 is recorded here as Daniel's. `project_arca.md` still lists it unassigned.
The work is done in late July by Ravi.)*

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-012, budget with sub-budgets | Tomas | 2026-07-03 |
| 2 | Update `project_arca.md` performance section | Daniel | 2026-07-06 |
| 3 | Define "feature work" for the error budget freeze | Tomas | 2026-07-16 |
| 4 | RLS review, third attempt | Jonas, Mei | 2026-07-16 |
