---
doc_id: meeting_024
type: meeting
title: "Platform Sync — Week 12"
date: 2026-07-21
time: "09:00–09:40 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Ava Duarte, Karen Oyelaran, Elliot Vance, Ravi Menon, Jonas Weiss]
apologies: [Tomas Herrera, Sofia Nyberg]
projects: [Arca, Migration, API v2]
tickets: [MIG-124, MIG-136, ARCA-329, ARCA-317, HEL-31, HEL-33, API-52]
tags: [sync, absence, cutover-prep]
---

# Platform Sync — 2026-07-21

Tomas is out until 10 August. Sofia is out until 3 August. Daniel is primary SRE
contact for the migration window, Ravi is secondary.

## Cutover prep

**Mei** — Six days out. Divergence audit finished Friday: zero divergence on 81 of 84
tenants, three tenants with a handful of rows each, all traced to documents deleted
during the audit window. Not real divergence.

MIG-124 runbook reviewed by Tomas before he left. Rollback rehearsed on Thursday on
`tnt_9017` — flipped to Postgres, ran for an hour, flipped back. Clean. That was the
hard gate from the last go/no-go and it is now green.

**Priya:** Go/no-go is Monday morning, cutover Monday 22:00 UTC.

**Mei:** 22:00 UTC is 06:00 for me on Tuesday. I will be there for the whole window.

**Priya:** You will be there for the window and then you will not be online Tuesday.

**Mei:** Agreed.

**Ravi** — Northwind Retail (`tnt_8842`) moved to Qdrant on Friday. Their saved
queries now return the documents they expected. Sofia sent them the results before
she went out.

> Elliot: For the record, nDCG@10 on their query subset went from 0.58 to 0.79.
> Priya: That is the escalation closed, then.
> Elliot: That is the escalation closed.

Ravi has also picked up ARCA-317, hybrid search, because it is the other half of
their complaint and Daniel is holding the SRE role for two weeks.

> Daniel: It is nominally mine. Take it.
> Priya: Then it is Ravi's. Someone update the project doc.

*(The project doc was not updated. It lists ARCA-317 as unassigned.)*

## Round-robin

- **Ava** — API-52 review is tomorrow. Writeup circulated last night.
- **Elliot** — ADR-017 written. L4 nodes provisioned. Not taking traffic until the GPU
  runbook exists.
- **Karen** — SEC-51 CI check in progress. She flags that her status board still shows
  HEL-31 and HEL-33 as in progress and asks whether Helios is a thing.

  > Priya: Helios is paused. That was two weeks ago.
  > Karen: Then somebody should close the tickets, because I am reporting on them.
  > Priya: That was my action and I did not do it. I will do it today.

- **Jonas** — ADR-016 merged. Nightly probe job not started.
- **Daniel** — GPU runbook started. Also holding `arca-*` on-call.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Go/no-go Monday 2026-07-27 09:00 UTC | Priya | 2026-07-27 |
| 2 | Close or move HEL tickets, actually | Priya | 2026-07-21 |
| 3 | Update ARCA-317 owner in `project_arca.md` | Ravi | 2026-07-24 |
