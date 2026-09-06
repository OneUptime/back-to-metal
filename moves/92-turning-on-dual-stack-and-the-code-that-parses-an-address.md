# 92 · Turning on dual-stack, and the code that parses an address

**Layer:** Edge · **Leaving:** Provider-managed IPv6 subnets and translation gateways · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Turns on dual-stack Services and pod addressing, then audits the code that parses an address, because a v6 literal breaks a parser that never saw one.

## Leaving from
- **AWS:** VPC IPv6 subnets with an egress-only gateway — the IPv6 cluster mode there gives pods IPv6-only addresses with translation rather than dual-stack.
- **Google Cloud:** dual-stack subnets — dual-stack is supported and IPv6-only is not, which is the more familiar starting point.
- **Azure:** dual-stack virtual networks — the same, with the same limitation and the same habits to unlearn.

## Why this works
The cluster half of this Move is short: dual-stack pod and service addressing, an address family order, and a change to the service range on the API server. Existing services and pods stay single-stack until they are recreated, which is a rollout rather than a switch. The long half is the audit, because application code, log parsers, allowlists and database columns have spent years only ever seeing one address format, and the first time a longer literal with colons in it arrives, something that has worked for a decade produces a wrong answer rather than an error.

## Before you start

**Access**
- Address space for the second family, from Move 39 and Move 91, allocated rather than improvised
- A change window for the API server range change, which is not a live edit

**Software**
- The network plug-in configured for both families with the order chosen deliberately
- A list of every place an address is parsed, stored or compared, which is the real deliverable

**People**
- The owner of every application that logs, stores or filters on an address

## The runbook
1. Allocate the second family properly from the plan in Move 39, rather than taking whatever the tooling suggests. This addressing is as permanent as the first.
2. Change the service range on the API server and configure the network plug-in for both families, with the order set deliberately: the first family listed is what a single-stack client gets.
3. Understand that existing services and pods stay on one family until they are recreated. This is a rolling change and the estate will be mixed for weeks, which is normal and should be expected rather than debugged.
4. Audit the application code. Address parsing, string length assumptions, storage columns sized for the shorter format, comparison functions, and anything that splits on a colon. Two weeks of this Move is here.
5. Audit the operational surfaces too: log parsers, dashboards that group by address, allowlists at partners, and any tooling that assumes an address matches a particular pattern.
6. Roll out family by family and namespace by namespace, watching for the failure that looks like an application bug rather than a network change.
7. Note the provider difference before assuming your starting point is the common one: one cloud's IPv6 cluster mode is not dual-stack at all but IPv6-only with translation, so those readers are changing model rather than adding a family.

## Operator's notes
- **Swap:** Where nothing needs the second family yet, this Move can wait — but not indefinitely, because Move 94 uses public IPv6 to sidestep address translation limits and it is much easier to have it already.
- **Do it faster:** Audit the code before touching the cluster. The cluster change is an afternoon and the audit is the schedule.
- **Watch out:** Database columns sized for the shorter format silently truncate the longer one, which produces a stored address that is wrong rather than absent. That is the worst failure in this Move and it is found by reading schemas.
- **Leftovers:** Egress-only gateways and translation gateways in the cloud keep billing until Part VII and are not removed here.

## Rollback
This Move is irreversible at the cluster level: a cluster converted to dual-stack is not supported converting back, so the decision is taken once and taken here. The point of no return is the service range change on the API server. What remains reversible is the rollout — a workload can be recreated as single-stack — and the underlying data is untouched, so a truncated column is restored from backup rather than from a network change. Rehearse the whole thing on the second cluster from Move 51 first.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 weeks | — |

## What you can turn off
Nothing yet. The provider's egress-only and translation gateways stay until Move 94 has moved the traffic.
