---
doc_id: note_012
type: note
subtype: incident_raw
title: "INC-2026-0617 — raw timeline notes"
author: Tomas Herrera
date: 2026-06-17
projects: [Arca]
tickets: [ARCA-301, ARCA-288]
incidents: [INC-2026-0617]
tags: [incident, raw, oncall, timeline]
---

# INC-2026-0617 raw notes

Typed while it was happening, cleaned up afterwards only for spelling. The tidy
version is the postmortem on the 19th.

```
17:12  Paged. arca-retrieve error rate 11% eu1 and climbing.
17:13  Dashboard. p95 is 2.1s. It was 310ms an hour ago.
17:14  Not a traffic spike. Request rate is flat.
17:15  arca-rank queue depth 40k and climbing. That is the thing.
17:16  arca-rank CPU pegged. All eight pods.
17:18  Scaling arca-rank 8 -> 16. This will not fix it if the input is wrong
       but it buys time.
17:24  16 pods. Queue still growing. So it is not capacity, it is input volume.
17:26  Something is sending arca-rank more work than it used to. What changed.
17:27  Nothing in #team-platform. Nobody said they deployed.
17:31  git log arca-retrieve. Twelve commits since Monday. Which one is live.
17:38  Deploy history is in the CD tool, not in the alert, not in the dashboard.
       Logging into the CD tool.
17:44  v2026.06.17.3 went out at 16:40. Forty minutes before the page.
17:47  Diff. ARCA-301, candidate limit 100 -> 400.
17:49  Four hundred candidates each going through a CPU cross-encoder. There it is.
17:52  Confirmed. Called it.
17:55  Author is offline. Slack, phone, nothing.
18:02  Priya says roll back, do not wait.
18:05  Rollback started.
18:20  Rollback complete. Error rate falling. 34% -> 19%.
18:30  Still 12%. Queue is 61k deep and draining at maybe 400/s.
18:33  Considering dropping the queue. Decided against - those are real requests
       and the clients have given up anyway, but I do not want to be the person
       who chose to drop them.
19:35  Queue empty. Error rate 0.2%, normal. Closing.
```

## Things I want to say at the postmortem while they are fresh

1. **Forty minutes.** From page to knowing what changed. Thirty-two of those minutes
   were me reading git logs across four repos. The alert should have told me.

2. **Unbounded queue.** `arca-rank` accepts work forever and never says no. It should
   reject when the projected wait exceeds the caller's remaining deadline. Then this
   is a 3% error rate for four minutes instead of 34% for three hours.

3. **No runbook.** I asked for a runbook when `arca-rank` was split out. It was an
   action on 9 June. I have never operated this service and I was reasoning about it
   from first principles at 17:15 on a Wednesday.

4. **Deployed at 16:40 and logged off at 17:00.** I do not want to make this about a
   person. I want a policy so it is not about a person.

5. Staging never saw this because staging's query mix has candidate counts under 100,
   so the limit change was a no-op there. We tested that it worked. We did not test
   that it worked on our traffic.

## One thing that is not about this incident

While I was in the dashboards I noticed the dual-write retry queue went to 90 minutes
of lag during the incident and drained overnight. Nobody was alerted. It did not
matter today because reads come from Mongo. It will matter after cutover. Mei
mentioned this exact gap on 9 June.
