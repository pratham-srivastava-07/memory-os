---
doc_id: project_helios
type: project_doc
title: "Project Helios — In-house Observability Platform"
project: Helios
project_id: PRJ-1120
status: paused
owner: Tomas Herrera
created: 2026-06-01
last_updated: 2026-07-08
tags: [observability, helios, paused, living-doc]
---

# Project Helios (PRJ-1120)

**Status: PAUSED as of 2026-07-08 (ADR-013).** Left in place for the record. Do not
start new work under `HEL-*` without talking to Priya.

## What it was going to be

A self-hosted metrics and trace store to replace the Datadog contract that renews on
2026-10-01. The 2026 Datadog bill is projected at $214k, most of it from Arca ingest
cardinality (every chunk write emits a `tenant_id` labelled counter).

Design: OpenTelemetry collectors to a Mimir/Tempo pair on the existing EKS cluster,
Grafana OSS on top. Tomas estimated 6 engineer-weeks to a usable state and roughly
$3.5k/month of infrastructure.

## Tickets

| Ticket | Description | State at pause |
|---|---|---|
| HEL-12 | OTel collector rollout to `arca-*` | done in staging |
| HEL-31 | Mimir cluster provisioning | in progress |
| HEL-33 | Trace sampling policy | in progress |
| HEL-40 | Dashboard parity audit | not started |

## Why it was paused

The migration cutover slipped twice and Helios was competing with it for Tomas and
Mei. Priya took the trade to the 2026-07-07 sync. Grafana Cloud at roughly
$4.2k/month covers the same ground with no build cost, and the Datadog contract can
be dropped at renewal either way. Revisit in Q4.

## What survives the pause

- The OTel collector work (HEL-12) stays. It is what feeds Grafana Cloud.
- The cardinality reduction on `arca-index` metrics stays and is now INFRA-95.
