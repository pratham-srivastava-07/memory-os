---
doc_id: note_021
type: note
subtype: signoff
title: "Cutover test plan — sign-off"
author: Karen Oyelaran
date: 2026-07-24
projects: [Migration]
tickets: [MIG-124, MIG-136]
tags: [testing, signoff, cutover, quality-gate]
---

# Cutover test plan — sign-off

For the 2026-07-27 read cutover. This is the unconditional sign-off I refused to give
in June.

## What I refused in June and why

On 25 June I signed off conditionally. My condition was that I could assert zero
divergence for a specific tenant immediately before flipping it, and at that point I
could not, because the audit tooling ran across the whole corpus overnight and told
you about yesterday.

Ravi built the per-tenant assertion. It runs in about 40 seconds for a mid-size tenant
and about 4 minutes for `tnt_8842`. That is fast enough to be a gate rather than a
report.

## What is verified

1. **Per-tenant pre-flip assertion.** Row counts match, and a full checksum comparison
   over `(chunk_id, document_id, ordinal, token_count, content_hash)` for every row.
   Not sampled. All of them.
2. **Post-flip assertion at 5 minutes.** Same query, re-run. Catches writes that
   landed in the gap.
3. **Retrieval smoke, per tenant.** Three saved queries per tenant, results compared
   against the pre-flip run. Not a quality test — an "is it returning anything at all"
   test.
4. **Rollback rehearsed.** Executed on `tnt_9017` (Calder Freight) on 2026-07-23.
   Flipped to Postgres, ran an hour of real traffic, flipped back. Clean both ways.
   This was the hard gate Tomas set and it is green.
5. **Error rate and latency dashboards** with a named person watching them, which is
   Mei.

## What is not verified, stated plainly

- **Behaviour under a Postgres primary failure during the window.** AI-7 from the
  June postmortem was the game day for this. It was due 10 July. It did not happen.
  If the primary fails during cutover we are improvising.
- **The dual-write retry lag.** Still spikes to ~6 minutes under burst. The go/no-go
  criterion is under 60 seconds. It will not be met. Mei's compensating argument —
  reversible per-tenant flips, assertion immediately before each flip, biggest tenants
  last — is reasonable and I am accepting it. I want it written down that I am
  accepting a criterion that was not met, rather than pretending it was.
- **Anything about what happens after cutover.** My plan covers the window. It does
  not cover the two weeks of dual write that follow, and nobody has asked me to.

## Sign-off

Signed off, unconditional, for the cutover window itself.

— K. Oyelaran, 2026-07-24
