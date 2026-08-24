---
doc_id: note_011
type: note
subtype: onboarding
title: "Week one — what I have worked out so far"
author: Ravi Menon
date: 2026-06-19
projects: [Arca, Migration]
tickets: [MIG-112, ARCA-233]
tags: [onboarding, new-joiner, notes-to-self]
---

# Week one — what I have worked out so far

Started Monday 15 June. Buddy is Daniel. Writing this partly for me and partly
because Priya asked new people to record what was confusing while it is still
confusing.

## Setup

Compose file worked first try, which Karen seemed pleased about. Four services up
locally in about four minutes.

## The shape of things

Four services: `arca-ingest`, `arca-index`, `arca-retrieve`, `arca-rank`. Split about
five weeks ago (ADR-001). Everything shares `arca-core` for domain types.

Two datastores right now, which is temporary. Mongo is the system of record. Postgres
is being migrated to (PRJ-1103) and dual write went live a week before I started.
Reads still come from Mongo. This is the thing that confused me most in week one and
I have written it down as a diagram on my wall:

```
write → arca-index → Mongo (sync, can fail the request)
                   → Postgres (async, retried)
read  → arca-retrieve → Mongo
```

Daniel says the read arrow flips at cutover, currently 22 June. Nobody said what
happens to the write arrows and I did not think to ask.

## People, from a week of meetings

- **Daniel** — my buddy, reviews all my PRs so far. Thinks in writing. If you ping him
  on Slack with a design idea you get "write it up".
- **Mei** — owns the migration and is who I actually work for day to day, even though
  Priya is my manager. She is in Singapore so my morning overlaps hers, which is
  lucky; almost nobody else on the team overlaps her.
- **Tomas** — SRE. Asks "where is the runbook" in a way that is not rhetorical.
- **Priya** — my manager. Fortnightly 1:1s. Told me in the first one that she expects
  me to say when something looks wrong for at least three months, because after that
  I will have stopped noticing.

## My first ticket

MIG-112, the backfill. Specifically the `content_hash` uniqueness problem. Mongo let
us have duplicate `content_hash` within a tenant; the new Postgres schema has a unique
constraint. 41,000 rows fail.

Four days on this. My finding: about 38k are genuine duplicate uploads — customer
uploads a file, it fails, they upload it again. Those are fine to collapse.

The other 3k are not duplicates. Two different documents hash the same because we hash
the *extracted text*, and two invoices from the same template extract to nearly the
same string — the numbers live in a table our extractor drops. So the hash collision
is a symptom of an extractor bug. I would rather fix the extractor.

Mei says fix it after cutover, skip and log for now. That is the right call for the
schedule and I want to note that the bug is real and will still be there.

## Things nobody has told me and I have not asked

- What happens to the dual-write direction after read cutover
- Who owns ARCA-317, which is referenced in three docs with three different answers
- Whether Helios is a real project or a thing Tomas talks about
