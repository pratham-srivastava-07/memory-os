---
doc_id: meeting_028
type: meeting
title: "Arca Architecture Review #7 — post-cutover, INC-2026-0729"
date: 2026-07-30
time: "10:00–11:10 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Mei Lin Zhao, Ravi Menon, Elliot Vance, Priya Raman, Karen Oyelaran]
apologies: [Tomas Herrera, Jonas Weiss, Sofia Nyberg, Ava Duarte]
projects: [Arca, Migration]
tickets: [MIG-107, MIG-118, MIG-131, ARCA-317]
incidents: [INC-2026-0729]
tags: [architecture, incident, review, dual-write]
---

# Arca Architecture Review #7 — 2026-07-30

Agenda was the reindex plan. It became INC-2026-0729.

## INC-2026-0729

**Severity:** SEV-3. **Duration:** 2026-07-29 11:20 – 12:50 UTC.
**Impact:** Documents uploaded by three tenants during the window were not
retrievable for up to 74 minutes after upload. No errors. No alerts. Northwind Retail
noticed and asked in their shared channel.

**Ravi:** Northwind Retail ran a bulk upload yesterday morning, about 90,000
documents. The dual-write path did what MIG-118 does under burst — the async Postgres
retry queue lagged. Peak lag was 74 minutes.

**Mei:** And two days ago that would have been harmless, because reads came from
Mongo and Mongo had the data.

**Daniel:** And now reads come from Postgres.

**Mei:** And now reads come from Postgres. ADR-006 says the Mongo write is the one
that can fail the request and the Postgres write is retried asynchronously. That was
correct while Mongo was authoritative. The moment we flipped reads, it inverted: the
authoritative store is now the one behind the async queue.

**Priya:** Did anybody catch that at the go/no-go?

**Mei:** No. I went back and read the runbook this morning. MIG-124 has a step for
flipping reads and no step for flipping which write is synchronous. I wrote it and I
did not think about it.

**Daniel:** Neither did I, and I reviewed it.

**Priya:** How long were we exposed?

**Mei:** From 01:20 Monday, when the last tenant flipped, until 13:10 yesterday when
Ravi inverted it manually. Roughly 36 hours.

**Ravi:** It is inverted now. Postgres write is synchronous, Mongo write is the
async one. Which is what it should have been from the moment reads moved.

## The alerting

**Priya:** Why did nobody know for 74 minutes?

**Ravi:** There is no alert on retry queue lag.

**Mei:** There is no alert on retry queue lag because it is AI-4 from the
INC-2026-0617 postmortem, it is mine, it was due on 3 July, and I did not do it. It
was also raised on 9 June, before the postmortem, and I said it was on the list.

**Priya:** I am going to be blunt about the pattern rather than about the person.
This is the third time this specific gap has been named. June ninth in a sync, June
nineteenth as a postmortem action, June twenty-third in a sync. It has an owner and a
due date and it has not been done, and the reason it has not been done is that every
week there was something with a date on it and this had a date nobody enforced.

**Mei:** That is accurate.

**Priya:** Then the fix is not "do AI-4". The fix is that postmortem actions get
reviewed in the sync until they are closed, and an open one past its due date is the
first item on the agenda, not the last.

**Karen:** Can the divergence assertion I built run continuously rather than only at
flip time?

**Ravi:** Yes, and that is a better control than an alert on the queue, because it
measures the thing we care about rather than a proxy for it.

**Mei:** Do both. The queue lag alert is ten minutes of work and I will do it today.

## Reindex

Deferred to the next review. Nobody wanted to plan a 46-hour reindex on the day of an
incident.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | AI-4: lag metric and alert on dual-write retry queue | Mei | 2026-07-30 |
| 2 | Continuous per-tenant divergence assertion | Ravi | 2026-08-06 |
| 3 | Add "invert synchronous write" to MIG-124 as a post-cutover step | Mei | 2026-07-31 |
| 4 | Open postmortem actions reviewed at the top of every sync | Priya | ongoing |
| 5 | Short writeup for INC-2026-0729 | Ravi | 2026-07-31 |
