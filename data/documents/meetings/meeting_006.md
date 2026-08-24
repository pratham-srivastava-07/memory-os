---
doc_id: meeting_006
type: meeting
title: "Arca Architecture Review #2 — chunking and embeddings"
date: 2026-05-21
time: "12:00–13:00 UTC"
recurrence: "Arca Architecture Review (biweekly, Thursdays)"
attendees: [Daniel Okoye, Elliot Vance, Priya Raman, Karen Oyelaran, Jonas Weiss]
apologies: [Mei Lin Zhao, Tomas Herrera]
notes_sent_to: [Mei Lin Zhao]
projects: [Arca]
tickets: [ARCA-244, ARCA-260, ARCA-341]
tags: [architecture, chunking, embeddings, review]
---

# Arca Architecture Review #2 — 2026-05-21

Mei sent apologies (21:00 SGT) and asked for notes. Tomas was on call and got paged.

## Chunking

**Elliot:** I have a baseline now, so I can argue about chunking with evidence instead
of taste. But I want to separate two things. One: what our chunker does today, which
is undocumented. Two: what it should do, which I cannot answer for another two weeks.

**Daniel:** Write down what it does today first. If we change it later, at least the
change is deliberate.

**Elliot:** That is what I want. An ADR that says "512, 64 overlap, here is what it is
bad at" and nothing else. It is not a decision, it is a confession.

**Priya:** Write it. Call it what it is.

**Elliot:** The thing it is bad at is structure. 31% of chunks in a sample of
Northwind Retail PDFs split a table. And a table split across a boundary is worse
than useless — both halves embed as noise.

**Karen:** Can we assert on that in the harness? "No chunk boundary inside a table
element."

**Elliot:** Yes, once the parser gives me structure. Today it gives me text.

## Embeddings

**Elliot:** Second thing. We are on `gte-large-v2` self-hosted, and that is also
undocumented and also nobody remembers deciding it. Three options if we re-open it:
hosted API, self-host CPU, self-host GPU.

**Jonas:** Before you cost that — Lumen Health's contract prohibits sending document
content to a processor that is not on our sub-processor list. Adding one is 30 days'
notice and a conversation. A hosted embedding API is a new sub-processor.

**Daniel:** That is close to decisive on its own.

**Jonas:** It is decisive unless the quality gap is enormous.

**Elliot:** It is two nDCG points against the best hosted model I tested. 0.71 versus
0.73.

**Daniel:** Then it is decided and we should write it down for the same reason.

**Priya:** Same treatment. ADR that records the existing choice and the reason we now
know we had.

## Note added by Mei (async, 2026-05-22 02:10 UTC)

> Read the notes. One thing nobody said: `gte-large-v2` is 1024 dimensions and if we
> put vectors in Postgres that is about 4 KB a row before TOAST. At the 60M chunks we
> project for the end of the year that is a quarter of a terabyte of heap that is not
> in my capacity model. I will add it. It does not change the model choice; it might
> change the vector store choice.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | ADR recording current chunking behaviour | Elliot | 2026-06-03 |
| 2 | ADR recording embedding model choice + residency constraint | Elliot | 2026-06-09 |
| 3 | Structure-aware parser output for the chunker | Daniel | 2026-06-19 |
| 4 | Add vector heap size to capacity model | Mei | 2026-05-28 |
