---
doc_id: decision_013
type: decision
adr_id: ADR-013
title: "Pause Project Helios, adopt Grafana Cloud"
date: 2026-07-08
status: accepted
deciders: [Priya Raman, Tomas Herrera]
project: Helios
project_id: PRJ-1120
tickets: [HEL-12, HEL-31, HEL-33, HEL-40, INFRA-95]
supersedes: []
superseded_by: []
tags: [observability, cost, prioritisation, paused]
---

# ADR-013: Pause Project Helios, adopt Grafana Cloud

## Status

Accepted 2026-07-08.

## Context

Helios (PRJ-1120) was going to replace Datadog before the 2026-10-01 renewal. The
projected 2026 Datadog spend is $214k, dominated by cardinality from `arca-index`
metrics.

Since Helios started, the migration cutover has slipped twice, and Helios and the
migration are competing for the same two people. Tomas is the only person who can
build Mimir and the only person who can run a cutover.

## Decision

Pause Helios. Move to Grafana Cloud (Pro, ~$4.2k/month at current volume) for
metrics, logs and traces. Keep HEL-12, the OTel collector rollout, because Grafana
Cloud needs it too. Reduce `arca-index` metric cardinality regardless — that becomes
INFRA-95 and is worth doing under any vendor.

HEL-31 and HEL-33 stop. Revisit in Q4 if the Grafana bill grows past $8k/month.

## Consequences

- Saves roughly six engineer-weeks in Q3, which is what the migration needs.
- Datadog is still cancelled at renewal, so the cost saving is realised either way.
- We are on a vendor for observability during the highest-risk migration of the year.
  Tomas noted he would rather be on a vendor than on something he built three weeks
  ago.
- Anything still open under `HEL-*` should be closed or moved. Priya to sweep the
  board; this did not happen promptly and stale HEL tickets showed up in status
  updates for another two weeks.
