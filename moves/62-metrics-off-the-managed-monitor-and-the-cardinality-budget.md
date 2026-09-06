# 62 · Metrics off the managed monitor, and the cardinality budget

**Layer:** Platform · **Leaving:** Managed metric stores, container insight agents, custom metrics and the provider's metric query language · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 14 days

> Prometheus scrapes into storage you sized yourself, where cardinality stops being a smooth monthly charge and becomes an OOMKill during an incident.

## Leaving from
- **AWS:** CloudWatch with Container Insights — a native metric service with its own expression language, so every dashboard and alert is rewritten by hand.
- **Google Cloud:** Cloud Monitoring — the same, with its own query language and its own custom metric pricing.
- **Azure:** Azure Monitor with Log Analytics — the same again, and the one where metrics and logs share a query language and a bill.

## Why this works
On a managed metric service, a careless label was a slightly larger invoice. On storage you run, the same careless label is a memory limit exceeded during the incident you added the label to debug. That change — from a smooth monthly charge to a hard operational limit — is the single most important thing to understand about this Move. Everything else follows from it: a series budget per machine, drop rules applied at scrape time rather than at query time, and a fortnight of running both systems side by side so that the panels are proved before anybody trusts them.

## Before you start

**Access**
- The object store from Move 49 and the durability terms from Move 54, because the metric store wants object storage rather than local disk
- An export of every dashboard and alert expression currently in use, which is the real inventory

**Software**
- A scraper and a long-term store, both at pinned versions, with the store's licence read
- A series budget per machine, written down before the first scrape rather than discovered afterwards

**People**
- Whoever owns each dashboard, because the rewriting is the work and it is theirs to verify

## The runbook
1. Stand up the scraper and the long-term store, with the store's data in the object store from Move 49 rather than on local disk. One common option is permissively licensed; another is under a copyleft licence with a replication factor of three by default, which is a capacity decision as much as a legal one.
2. Set a series budget per machine and enforce it with drop rules at scrape time. A rule that drops a label at query time saves nothing; the memory was consumed when the series was created.
3. Scrape everything and dual-run against the managed service for a fortnight. This is the reversibility window this Move claims, and it is what turns a dashboard from a translation into a verified one.
4. Rewrite the dashboards and alert expressions. All three clouds now sell a managed service speaking the same query language, and a reader on one of those adds a target and is nearly finished; the larger population is on a native expression language and every panel is rewritten by hand. Budget it as engineering rather than as configuration.
5. Compare the two systems on the same incident. Take a real event from the fortnight and confirm both would have shown it, at the same time, with the same shape.
6. Alert on the metric store itself — its ingestion rate, its series count against the budget, and its memory headroom — before turning the managed service off. A monitoring system with no monitoring is the classic second failure during a first one.

## Operator's notes
- **Swap:** For a small estate, a single scraper with local storage and a modest retention is genuinely enough, and the object-store tier can wait until retention becomes a requirement.
- **Do it faster:** Rewrite the twenty dashboards people actually open, and delete the rest. Most estates have a long tail of panels nobody has looked at in a year.
- **Watch out:** The first bad label will arrive from an application team who added a request identifier to a metric. Drop rules at scrape time, plus an alert on series growth, are what stop that being an outage.
- **Leftovers:** Custom metrics, insight agents and the log ingestion that came with them keep billing until the managed service is turned off, which is fourteen days after the dual-run proves clean.

## Rollback
For fourteen days both systems are running and reverting is repointing the dashboards, which is why the dual-run is not optional. The point of no return is turning the managed service off, after which historical data before that date exists only where you exported it. Export what you need to keep first, and confirm it can be restored and queried, because a metric history that cannot be read is not a history.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,180/mo | $140/mo | 94% | 0 min | 3 weeks | 2 weeks |

## What you can turn off
The managed metric service, its insight agents and its custom metrics — fourteen days after the dual-run shows the same incident on both.
