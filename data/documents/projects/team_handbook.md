---
doc_id: team_handbook
type: project_doc
title: "Platform Team Handbook — Working Agreements"
project: Team
status: active
owner: Priya Raman
created: 2026-05-04
last_updated: 2026-08-06
tags: [team, process, oncall, preferences, living-doc]
---

# Platform Team Handbook

Maintained by Priya Raman. Anything here can be changed by saying so in the Tuesday
sync and updating this file in the same week.

## Who we are

| Person | Role | Location / TZ | Core hours (UTC) |
|---|---|---|---|
| Priya Raman | Engineering Manager | London, UTC+1 | 08:00–16:00 |
| Daniel Okoye | Staff Engineer, Arca lead | Berlin, UTC+2 | 07:00–15:00 |
| Mei Lin Zhao | Senior Engineer, storage | Singapore, UTC+8 | 01:00–09:00 |
| Tomas Herrera | SRE Lead | Lisbon, UTC+1 | 08:00–16:00 |
| Ava Duarte | Senior Engineer, API lead | Austin, UTC-5 | 13:00–21:00 |
| Sofia Nyberg | Product Manager | Stockholm, UTC+2 | 07:00–15:00 |
| Jonas Weiss | Security Engineer (50%) | Zurich, UTC+2 | 07:00–15:00 |
| Karen Oyelaran | QA Lead | Lagos, UTC+1 | 08:00–16:00 |
| Elliot Vance | Applied ML Engineer | Toronto, UTC-4 | 12:00–20:00 |
| Ravi Menon | Backend Engineer (from 2026-06-15) | Bengaluru, UTC+5:30 | 04:00–12:00 |

The only hour everyone shares is 13:00–14:00 UTC, and Mei is at 21:00 local for it.
We do not use it.

## Recurring meetings

- **Platform Sync** — Tuesdays 09:00 UTC, 45 min. Whole team. This is the one meeting
  nobody may skip without sending written notes.
- **Arca Architecture Review** — Thursdays 12:00 UTC, biweekly, 60 min. Moved to
  10:00 UTC from 2026-07-16 at Mei's request.
- **1:1s** — Priya with each person, fortnightly, scheduled individually.

## Meeting rules

1. A written pre-read lands 24 hours before any architecture review or decision
   meeting. No pre-read, no meeting. Priya will cancel it.
2. Decisions get an ADR in `decisions/` within two working days, or they did not
   happen.
3. If you cannot make a meeting in your night, do not attend it. Send notes.

## Deploy policy

*Updated 2026-06-22, see ADR-009.*

No production deploys after 15:00 UTC on Thursday, and none on Friday. Hotfixes are
exempt but need an SRE in the room. Daniel refuses to be the second pair of eyes on a
Friday deploy and has said so enough times that we wrote it down.

## On-call

One-week rotation, handover Mondays 09:00 UTC. Rotation is Tomas, Daniel, Mei, Ravi
(from 2026-07-06). Ava, Elliot, Karen, Jonas and Sofia are not on the rotation.
Secondary is always Tomas until we have a fourth trained person (OPS-19).

## Individual preferences worth knowing

- **Mei** does not take calls after 18:00 SGT (10:00 UTC). She will read anything you
  write, at length, and reply the same day.
- **Daniel** wants design discussion in writing before it is spoken. He will not
  engage with a whiteboard-first proposal.
- **Ava** prefers walking 1:1s and blocks Wednesday afternoons for deep work.
- **Karen** owns the test stack and has standardised on Playwright. Do not open a
  Cypress PR.
- **Tomas** wants every alert to have a runbook link or it does not get to page him.
- **Sofia** asks for customer-facing dates in writing only, never in a call.
- **Priya** reads pre-reads in the morning UTC and will comment before 10:00.
