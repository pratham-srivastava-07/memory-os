---
doc_id: meeting_031
type: meeting
title: "Quarter retro — May to August"
date: 2026-08-06
time: "13:00–14:30 UTC"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Ravi Menon, Jonas Weiss]
apologies: [Tomas Herrera]
projects: [Arca, Migration, API v2, Helios]
tickets: [ARCA-341, ARCA-317, MIG-131, API-77]
decisions: [ADR-020]
tags: [retro, process, quarter]
---

# Quarter retro — 2026-08-06

Three months. Priya facilitating. Tomas is back on the 10th and sent written input.

## What we shipped

- Arca split into four services (ADR-001)
- Postgres migration: dual write, backfill, read cutover, all 84 tenants (PRJ-1103).
  Mongo decommission on the 14th.
- Vector store moved to Qdrant, twice: split (ADR-014) then consolidated (ADR-019)
- Chunking v2 decided (ADR-011), reindex not yet run
- Reranker on GPU decided (ADR-017), not yet taking traffic
- Hybrid search (ARCA-317) merged
- API v2 protocol decided and then reversed (ADR-007, ADR-018)
- Eval harness (ARCA-341) built and used
- Two incidents, both SEV-2 or SEV-3, both with real learning

## What went well

**Mei** — The cutover itself. Zero customer-visible impact on 84 tenants. The thing
that made it work was the per-tenant divergence assertion, and that came out of a
condition Karen refused to sign off without.

**Karen** — Being allowed to refuse to sign off.

**Daniel** — Pre-reads. We have not had a meeting this quarter where somebody presented
slides to people who had not read anything, and the discussions are better for it.

**Ravi** — Onboarding. He had a real ticket in week two and owned a subsystem in week
three. He also notes his PRs were all reviewed by Daniel, which he liked and which he
suspects was not sustainable for Daniel.

**Sofia** — Nothing customer-visible broke during a migration. She said she expected
to spend the quarter apologising and did not.

## What did not

**Priya** — The AI-4 pattern. A known gap named three times across seven weeks, with
an owner and a date, that was only closed after it caused an incident. The failure was
not Mei's; the failure was that nothing in our process made an overdue postmortem
action louder than a thing with a customer date on it.

**Elliot** — Decisions made on one-off benchmarks. ADR-011 was right and I shipped a
consequence — the reranker sequence length — that I did not connect until Tomas
raised the latency budget three days later. If the harness had been in CI the number
would have been in front of me.

**Ava** — Three weeks on a spike we then deleted. She wants to be clear she does not
think it was wasted; she thinks the six-week review with a written bar is the only
reason it ended cleanly instead of dragging.

**Mei** — Two schedule slips. Both were real and both were predictable. ADR-006 had
zero slack and that was a planning failure, not an execution one.

**Jonas** — Security work at 50% loses to anything with a date. The nightly probe from
ADR-016 is still not started, six weeks on.

**Tomas** *(written)* — "Documents disagreed with each other all quarter and we only
ever found out when a customer or Sofia read one. The latency number was in three
places with three values. The migration timeline is in a project doc that is still
wrong today. ADRs are good at recording decisions and bad at updating everything the
decision invalidates."

**Sofia** — Agrees, sharply. She quoted 1 September for the v1 shutoff out of a
document that was already wrong.

## What we are changing

1. Open postmortem actions are the first agenda item in every sync until closed.
   Already in effect since 2026-07-30.
2. Eval harness runs in CI as a soft gate on ranking changes. ADR-020.
3. **An ADR that invalidates a document must name the document and the person who
   will update it, in the ADR, as an action.** Priya to add to the handbook.
4. Jonas's security time gets a standing slot rather than competing for slack.

**Priya:** One more. Nobody owns keeping the project docs true. `project_arca.md` has
a performance section that says 300 ms, which ADR-012 replaced five weeks ago.
`project_migration.md` says Mongo goes away on the 21st and it goes away on the 14th.
`project_arca.md` still lists ARCA-317 as unassigned and Ravi shipped it last Friday.

**Daniel:** The 300 ms one is mine. It has been my action since 6 July.

**Priya:** I know. I am not asking for volunteers, I am saying the model is wrong.
A living document nobody is accountable for is a stale document with a nice name.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Write ADR-020, eval gates in CI | Elliot | 2026-08-06 |
| 2 | Handbook: ADRs must name invalidated docs and an owner | Priya | 2026-08-11 |
| 3 | Audit all four project docs against current ADRs | Ravi | 2026-08-14 |
| 4 | Standing security slot | Priya | 2026-08-11 |
| 5 | Re-scope AI-7 with Tomas | Priya | 2026-08-11 |
