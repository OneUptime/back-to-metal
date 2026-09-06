# 95 · The first VIP: L2, and failover when nobody will peer

**Layer:** Edge · **Leaving:** Managed layer-4 load balancers · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Produces a working LoadBalancer address in layer-2 mode, at the cost of one elected node carrying every packet destined for it.

## Leaving from
- **AWS:** Network Load Balancer — a layer-4 balancer with cross-zone distribution and its own health checking.
- **Google Cloud:** the external passthrough load balancer — the same, implemented in the network rather than as an appliance.
- **Azure:** Standard Load Balancer — the same again, with its own health probe model and backend pool semantics.

## Why this works
The first service address on your own hardware should be the simplest thing that works, and that is layer-2 mode: one node claims the address, answers for it, and every packet destined for it arrives there. That is address failover rather than load balancing, and the cost is honest — one node carries all of it, and failover is measured in however long it takes neighbouring devices to update their address caches. It is enough to make a working address exist, and it stays in place afterwards to hold the address while Move 96 cuts distribution over pool by pool.

## Before you start

**Access**
- The address pool for services, from the plan in Move 39 and, for public ones, Move 91
- A layer-2 domain the nodes share, which is the requirement this mode has and Move 96 does not

**Software**
- The load-balancer address management configured with a pool and an assignment mode
- A way to observe which node currently holds each address, because that is the thing that changes

**People**
- Whoever will test failover, since the interesting behaviour is what neighbouring devices do

## The runbook
1. Define the address pool and assign the first address. Keep the pool small and documented; addresses assigned ad hoc become impossible to reconcile against the plan.
2. Bring up a service and confirm the address answers from outside the cluster. This is the moment the estate has its first address of its own.
3. Understand what you have built. One node holds the address and answers for it; the others do not. Traffic is not distributed, and the node holding it is a single point of failure for that address until Move 96.
4. Decide the external traffic policy deliberately. Sending traffic on to any node preserves reachability and hides the client address; keeping it local preserves the client address and requires the health-check port to work correctly.
5. Test failover by stopping the node that holds the address. Measure how long the address takes to answer again, which depends on how quickly neighbouring devices refresh their caches rather than on anything in the cluster.
6. On rented metal, note the constraint: address filtering on the provider's network usually prevents this mode entirely, and the answer is their own floating-address mechanism with a failover measured in tens of seconds.
7. Decommission nothing. The managed balancer keeps serving production until Move 103, which is why this Move is reversible immediately.

## Operator's notes
- **Swap:** Where the nodes do not share a layer-2 domain at all, skip this Move and go straight to Move 96. It exists as a stepping stone, not as a requirement.
- **Do it faster:** Use it for internal services first. They are lower stakes and they exercise the same mechanism.
- **Watch out:** A stale neighbour cache on a switch or a firewall will keep sending traffic to the old node after failover, and the symptom is that the address works from some places and not others. That is the classic layer-2 mode fault.
- **Leftovers:** The managed balancer keeps billing per hour and per capacity unit throughout, which is expected: this is the period where you pay for both.

## Rollback
Nothing is serving production through this address, so the rollback is deleting the service and its address assignment. There is no point of no return in this Move at all. That is deliberate: it exists so that the first address is created in a situation where being wrong costs nothing, and so that the address itself survives into Move 96 rather than being created twice.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing. The managed balancer carries every user until Move 103 moves the traffic.
