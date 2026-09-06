# 63 · Logs and traces, brought home

**Layer:** Platform · **Leaving:** Managed log ingestion and query, managed distributed tracing, the provider's trace agent and its propagation header · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 30 days

> Grafana Alloy or an OpenTelemetry Collector replaces the retired log agent and the provider's trace daemon, which makes trace propagation a rolling code change.

## Leaving from
- **AWS:** CloudWatch Logs with X-Ray — a proprietary trace context header, so services need a translation shim through the mixed weeks.
- **Google Cloud:** Cloud Logging with Cloud Trace — the same shape, with its own propagation header and its own retention pricing.
- **Azure:** Log Analytics with Application Insights — again a proprietary context, and again a shim until every service is speaking the standard one.

## Why this works
Logs and traces move together because they are collected by the same agent and correlated by the same identifier. The collector question is settled rather than left open, since the long-standing log agent reached end of life, and what replaces it also carries traces. The part that surprises people is the propagation header: two of the three clouds propagate their own trace context, so during the mixed weeks a service that has moved and a service that has not need a shim between the standard header and the proprietary one. That makes this a rolling code change across the estate rather than an infrastructure swap.

## Before you start

**Access**
- The object store from Move 49 for the log chunks, under the durability terms Move 54 set
- An export of every saved query in the old console, because each one is rewritten by hand

**Software**
- A collector at a pinned version, and a log store and a trace store, each with its licence read
- Query limits set before any developer is given the address, not after the first unbounded query

**People**
- The owner of each service that emits traces, because the header change lands in their code

## The runbook
1. Choose the collector deliberately and pin it. The old log agent is end of life, so the choice is between the vendor's own collector and the vendor-neutral one, and the second is the safer default for an estate that may change vendors again.
2. Stand up the log store with its chunks in the object store from Move 49, and state its licence in the same breath as its features, because one of the common choices is under a copyleft licence that some organisations will not accept.
3. Put high-cardinality identifiers — request identifiers, user identifiers, trace identifiers — into structured metadata rather than into labels. A label is an index and an index of unique values is a memory leak with a schema.
4. Set query limits before anybody is given the address. An unbounded query over a month of logs will take the store down, and it will be run within a week of the address being shared.
5. Stand up the trace store and roll out the standard propagation header service by service. Where the estate still speaks a proprietary header, run a translation shim at the boundary until the rollout completes.
6. Rewrite the saved queries. This is the larger half of the four weeks, and there is no tool that does it. Rewrite the ones people use, delete the rest, and have the owners confirm each one returns what they expect.
7. Dual-run for thirty days, then turn the managed services off. That window is the reversibility this Move claims.

## Operator's notes
- **Swap:** Where traces are not actually used by anyone, say so and do the logs only. Half this Move delivered well beats all of it delivered badly.
- **Do it faster:** Ship logs first and traces second. They have different consumers and the log half is what an incident needs.
- **Watch out:** Log volume is almost always larger than the estimate, because the estimate came from the managed service's billing after its own sampling and filtering. Size for two to three times what the invoice implies.
- **Leftovers:** Managed log retention keeps billing after ingestion stops, sometimes for months. Set the retention down explicitly rather than assuming it lapses.

## Rollback
For thirty days both pipelines run, so reverting is repointing the collector. The point of no return is turning the managed ingestion off, after which older logs live only in the export you took. Export what compliance requires first and confirm it can be restored and searched, because an archive that has never been read back is an assumption rather than a record.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,620/mo | $220/mo | 94% | 0 min | 4 weeks | 30 days |

## What you can turn off
Managed log ingestion and tracing after thirty days of dual-running, and the retention behind them once the export is proved.
