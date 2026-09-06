# 102 · The shadow edge: two gateways and a weighted record

**Layer:** Edge · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Runs the new gateway on a shadow hostname and compares it route by route under mirrored traffic, then restores the drain the managed balancer was providing.

## Leaving from
- **AWS:** Application Load Balancer deregistration delay — connection draining you never configured because it was on by default.
- **Google Cloud:** backend service connection draining — the same property under a different name and a different default.
- **Azure:** Application Gateway connection draining — the same again, enabled per backend pool.

## Why this works
Before shifting a single user, run the new edge on a hostname nobody uses and compare it route by route with mirrored or replayed traffic. Status codes and latency per route, against the metrics from Move 62, for long enough that the awkward traffic shapes have all appeared — which is usually a fortnight rather than a day. The second half of this Move is the thing that gets forgotten: the managed balancer was quietly draining connections when a backend went away, and on your own edge that is a stop delay and a termination grace period that have to be configured and then verified with load actually in flight.

## Before you start

**Access**
- A shadow hostname with its own certificate, resolving to the new edge
- Mirroring or replay of production requests, at a rate that does not affect the real backends

**Software**
- Per-route status-code and latency comparison, on the metrics stack from Move 62
- A load test that can hold connections open while a pod is deleted, to verify draining rather than assert it

**People**
- The owner of each route, to say whether a difference is a defect or an improvement

## The runbook
1. Create the shadow hostname and its certificate, and point it at the gateway from Move 98 with the routes from Move 99. Nothing external resolves to it.
2. Mirror or replay production requests at the shadow edge. Mirroring is better because it captures the real distribution; replay is easier and misses the unusual shapes.
3. Compare per route rather than in aggregate. Status code distribution and latency percentiles, route by route, because one broken route out of two hundred disappears in an aggregate and does not disappear from a customer's day.
4. Run it for a fortnight. Most of that time is waiting for the awkward traffic to appear: the large upload, the slow client, the request with the unusual header, the monthly report.
5. Configure connection draining explicitly. A stop delay long enough for the load balancer to notice, and a termination grace period long enough for in-flight requests to finish.
6. Verify the draining under load. Delete a pod while a load test holds connections open and count the errors. A manifest that claims a grace period and an application that ignores the signal are indistinguishable until this test.
7. Shift nothing. Move 103 does that, and this Move exists so that Move 103 is boring.

## Operator's notes
- **Swap:** Where mirroring is not practical, replaying a day of access logs is a decent substitute for everything except concurrency behaviour.
- **Do it faster:** Start the comparison on the day Move 99 produces its first routes, and let it run while the remaining routes are translated.
- **Watch out:** A difference in latency at the ninety-ninth percentile with identical medians usually means a connection-reuse difference rather than a slow backend. Look at connection behaviour before blaming the application.
- **Leftovers:** The shadow hostname and its certificate are worth keeping permanently as a place to test edge changes.

## Rollback
Nothing is shifted and nothing is decommissioned, so there is nothing to reverse and no point of no return. The comparison data is the output, and it should be kept so that a difference observed during Move 103 can be checked against what the shadow edge showed. Keep the drain configuration in source control, because it is the setting most likely to be lost in a later refactor and its absence is invisible until a deploy drops requests.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 weeks | — |

## What you can turn off
Nothing. This is the last Move before the traffic moves, and both edges are paid for.
