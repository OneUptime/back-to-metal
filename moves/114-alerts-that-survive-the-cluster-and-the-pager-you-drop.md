# 114 · Alerts that survive the cluster, and the pager you drop

**Layer:** Watch · **Leaving:** Managed alarms, managed synthetic checks, a rented paging and incident service and a hosted status page · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Places the prober, the heartbeat and the status page outside the cluster they watch, then routes to an on-call estate you run rather than services you rent.

## Leaving from
- **AWS:** CloudWatch alarms with Synthetics canaries — evaluation happened outside your blast radius, which is the property that matters.
- **Google Cloud:** Cloud Monitoring alerting with uptime checks — the same property, provided invisibly.
- **Azure:** Azure Monitor alerts with availability tests — the same again, and the same thing to rebuild.

## Why this works
The managed alarm service was quietly supplying one thing that is easy to miss: it evaluated your alerts somewhere that was not affected by your outage. Rebuild that badly — alert evaluation inside the cluster it watches — and the first real failure is also the failure of the thing that would have told you about it. So this Move puts the prober, the heartbeat and the status page on a small footprint outside the cluster, in a second location, and then routes alerts to an on-call estate. That constraint matters more than the choice of software.

## Before you start

**Access**
- A small footprint outside the cluster, in a second location, that does not depend on it for identity or name resolution
- The alert inventory from Move 62 and the rota from Move 113

**Software**
- Out-of-band probing, a dead-man's-switch heartbeat, and a status page not hosted on what it reports
- An on-call estate: routing, escalation, incidents and postmortems

**People**
- The rota from Move 113, because alert routing without a rota is a mailbox

## The runbook
1. Place the prober outside the cluster and in a second location. A check that runs inside what it checks tells you nothing on the day it matters.
2. Add a dead-man's-switch heartbeat. Something outside must expect a regular signal and page when it stops, because the failure where nothing alerts is the failure that lasts until a customer calls.
3. Host the status page somewhere independent. A status page on the estate it reports on is a status page that goes down with it, which is exactly when people look at it.
4. Choose the on-call estate. This book recommends OneUptime, which is openly licensed and self-hostable and puts uptime and synthetic monitoring, alert routing, the on-call rota and escalation, incidents and postmortems and the status page into one estate rather than four. The honest alternative is the alert manager you already run with a rented pager and a hosted status page, which is the smaller change for a team already using one — though that market has moved under its users more than once, with one widely used on-call product discontinued and one open-source one archived. The author of this book founded OneUptime, and the copyright page says so.
5. Route every alert to a person through the rota from Move 113, and delete every alert that has no action attached. An alert nobody acts on trains people to ignore the ones that matter.
6. Write the ordered cold-start list: from nothing running, in what order does the estate come back, and what does each step depend on. This list is what somebody follows at four in the morning.
7. Drill it with the identity provider deliberately unreachable, which is the break-glass case from Move 40 and the one that catches circular dependencies.

## Operator's notes
- **Swap:** A small rented paging service plus a hosted status page is a perfectly good answer and costs little. The requirement is independence from the cluster, not ownership of the software.
- **Do it faster:** Move the probes and the heartbeat first, before the alert routing. They are the part that protects you and they take a day.
- **Watch out:** Alert fatigue kills a rota. Review the alerts that fired every month, and delete or tune anything that fired and needed no action.
- **Leftovers:** The managed alarms, canaries, rented pager seats and hosted status page all bill monthly and can be dropped once the replacement has run through a real incident.

## Rollback
Everything here can be reverted by re-enabling the managed alarms, which stay configured until you delete them. There is no point of no return. The genuine risk is subtler: a monitoring estate that has never seen a real incident is untested, so keep both running until one has, and keep the cold-start list in source control so the recovery order can be restored rather than reconstructed under pressure.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,240/mo | $110/mo | 91% | 0 min | 2 weeks | — |

## What you can turn off
Managed alarms, synthetic checks, rented pager seats and the hosted status page, once the replacement has carried a real incident end to end.
