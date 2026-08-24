---
doc_id: note_014
type: note
subtype: customer
title: "Northwind Retail escalation — what they actually said"
author: Sofia Nyberg
date: 2026-06-29
projects: [Arca, API v2]
tickets: [ARCA-329]
tags: [customer, escalation, northwind, relevance]
---

# Northwind Retail escalation

`tnt_8842`. Written escalation to their account manager, copied to their CTO, received
this morning. I am recording what they said rather than what I think it means.

## Their words

> "Retrieval quality has degraded materially since April. We have saved queries that
> returned the correct document in April and return nothing useful today. The corpus
> has grown but the documents have not changed. We are three weeks from a go/no-go on
> rolling this out to 4,000 store managers and we cannot recommend it on current
> performance."

They attached eleven example queries with the document they expect and the results
they get. That is a genuinely useful artefact and I have given it to Elliot.

## Facts

- They are at **6.2M chunks**. In April they were at about 2.6M.
- Their rollout decision is 21 July.
- They are our reference customer for the segment. Two of our current pipeline
  opportunities have asked to speak to them.
- Their platform lead told Ava on 18 May, unprompted, that "search gets worse the more
  we put in". That was six weeks ago and it was in Ava's interview notes.

## What I have said to them

That we have their examples, that we are treating it as a priority, and that they will
have a technical response this week. I have not offered a cause or a date and I will
not until somebody gives me one in writing.

## What I want from engineering

1. Is this real and is it us? Yes or no, this week.
2. If yes, what is the fix and when.
3. Whether it affects anyone else. If our largest tenant has this problem, our
   second-largest is presumably two months behind them.

## What I am unhappy about

Their platform lead said this to us on 18 May in a research call. It is in the notes.
Nobody followed up, and the first time it reached anyone who could act on it was when
it arrived as an escalation six weeks later.

I do not think that is Ava's fault. I think our research notes go into a folder and
nothing reads them.
