---
doc_id: meeting_020
type: meeting
title: "Platform Sync — Week 10"
date: 2026-07-07
time: "09:00–10:00 UTC"
recurrence: "Platform Sync (weekly, Tuesdays)"
attendees: [Priya Raman, Daniel Okoye, Mei Lin Zhao, Tomas Herrera, Ava Duarte, Sofia Nyberg, Karen Oyelaran, Elliot Vance, Ravi Menon, Jonas Weiss]
projects: [Arca, Migration, Helios]
tickets: [MIG-118, HEL-12, HEL-31, HEL-33, INFRA-95, ARCA-329]
decisions: [ADR-013]
tags: [sync, helios, prioritisation, benchmark]
---

# Platform Sync — 2026-07-07

Ran over. Two big items.

## 1. The recall benchmark

**Mei** — Ran it over Thursday and Friday. pgvector HNSW, our config, our hardware.

| Vectors | Recall@10 | p95 query |
|---|---|---|
| 1M | 0.97 | 8 ms |
| 4M | 0.96 | 19 ms |
| 8M | 0.88 | 71 ms |
| 8M, `ef_search` 200 | 0.95 | 210 ms |

Recall falls off a cliff somewhere between four and eight million in a single index.
The only lever is `ef_search`, and it buys recall back by spending latency we do not
have — ADR-012 gives candidate generation 120 ms and 210 is not 120.

**Daniel:** So Northwind Retail's complaint is real, it is us, and it is exactly the
risk we wrote into ADR-004.

**Mei:** Yes. I want to say clearly that this is not a surprise. It is the thing I
asked to have written down, and it is written down, and it happened.

**Elliot:** Qdrant on the same data, same corpus: 0.96 at eight million, p95 24 ms,
with scalar quantization.

**Priya:** What is the decision and when?

**Mei:** Thursday. I want a proper session, not a sync slot. Partitioning does not
help — Northwind Retail is one tenant that is itself eight million vectors.

**Sofia:** What do I say to them before Thursday?

**Daniel:** That we have reproduced it, we know the cause, and we will have a plan
this week. Do not name the technology.

## 2. Helios

**Priya** — Raising this as a trade, not a debate. Tomas is on the critical path for a
cutover that has already slipped once and is now three weeks from a hard date. Helios
needs six engineer-weeks of Tomas and Mei. We cannot have both.

**Tomas:** I agree, and I want to say it rather than have it said to me. Grafana Cloud
is about $4.2k a month at our volume against $3.5k of infrastructure plus six weeks of
me. Datadog gets cancelled at renewal either way, so the saving is real under both
plans. The only thing Helios buys is control, and I would rather not be learning Mimir
during a migration.

**Priya:** Then Helios pauses. HEL-12, the collector rollout, survives, because
Grafana Cloud needs it. HEL-31 and HEL-33 stop. The cardinality work becomes INFRA-95
and is worth doing under any vendor.

**Tomas:** Revisit in Q4?

**Priya:** Revisit in Q4 if the Grafana bill goes past $8k.

> Priya to sweep the HEL board and close or move the open tickets. *(This did not
> happen. HEL-31 and HEL-33 appear as in-progress in status updates for another two
> weeks.)*

## Everything else, briefly

- **Ravi** — MIG-118 fix went out Thursday and was rolled back Friday morning; it
  changed the retry backoff and made the lag worse under burst. Second attempt this
  week.
- **Elliot** — ADR-011 merged, chunking v2. Reindex cannot start until after cutover.
- **Ava** — Six-week API-52 review is due 22 July. She is writing up honestly.
- **Karen** — Query replay working. It caught a regression in `arca-rank` on Friday
  before it shipped.
- **Jonas** — Waiting on the RLS review, which has moved three times.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Vector store session, Thursday | Mei | 2026-07-09 |
| 2 | Write ADR-013, Helios pause | Priya | 2026-07-08 |
| 3 | Sweep and close HEL tickets | Priya | 2026-07-10 |
| 4 | MIG-118, second attempt | Ravi | 2026-07-10 |
