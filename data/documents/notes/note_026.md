---
doc_id: note_026
type: note
subtype: one_to_one
title: "1:1 — Daniel"
author: Priya Raman
date: 2026-07-30
visibility: manager-private
projects: [Team, Arca]
tickets: [ARCA-317, ARCA-301]
tags: [1-1, personal, workload, private]
---

# 1:1 — Daniel, 2026-07-30

## Load

He is holding: Arca tech lead, `arca-retrieve` and ARCA-301, primary SRE contact
while Tomas is out, Ravi's buddy and reviewer on every one of his PRs, and the GPU
runbook. He picked up ARCA-317 on 2 July and has not started it, and Ravi has quietly
done it instead, which Daniel found out about from a note.

I asked how he felt about that. "Relieved, and slightly embarrassed to be relieved."

Ravi has ARCA-317 now, in fact and in name. The project doc still says unassigned; I
am not going to make Daniel fix it.

## The reversals

Two of his positions have been overturned this quarter. He argued for pgvector in
ADR-004 and it was reversed twice. He argued against GraphQL in ADR-007, lost, and was
vindicated in ADR-018.

I wanted to know whether that has landed badly. It has not, and his reasoning is worth
recording: "I was wrong about pgvector because I extrapolated from three million to
sixty million and wrote down that I had. Mei asked me to write down that I had not
tested it, and I did, and that is the only reason we knew what to change when it
broke. I would rather be wrong like that than right by accident."

On GraphQL: "Being right six weeks early is the same as being unhelpful. Ava got the
number. I only had an argument."

I have not managed many staff engineers who talk like that.

## Buddying

Reviewing every one of Ravi's PRs was the right call for six weeks and is now a
bottleneck. Ravi is shipping faster than Daniel can review while holding on-call.
Agreed: Mei picks up review for anything migration-side, Daniel keeps `arca-retrieve`.

He wanted to say that he thinks Ravi is the strongest hire we have made and that he
would like it noted somewhere that is not a performance review in November.

## Fridays

He asked, half joking, whether ADR-009 means he has to stop saying no to Friday
deploys, since it is policy now and nobody asks him.

Told him he has been made redundant by process, which is the goal.

## Thing I need to do

He has had an action to update the `project_arca.md` performance section since 6 July.
It is still wrong — it says 300 ms, ADR-012 says 400. He is not going to do it and I
should stop asking. The problem is not Daniel, it is that the doc has an owner in name
and no owner in practice. Raising at retro.
