# 109 · The fleet roll with no thirteenth machine

**Layer:** Watch · **Leaving:** Managed node groups, image-based node rollouts, autoscaler surge capacity and managed node auto-repair · **Risk:** High · **Cutover:** 10 min · **Reversible:** Immediately

> Rolls the fleet one failure domain at a time, because the surge node the provider added before taking one away does not exist on metal you already own.

## Leaving from
- **AWS:** managed node group updates — a surge node added before one is drained, which is capacity you were renting by the minute.
- **Google Cloud:** surge upgrades on node pools — the same mechanism, with the surge count configurable.
- **Azure:** node image upgrades with max surge — the same again, and the same assumption of spare capacity on demand.

## Why this works
Every managed rollout worked the same way: add a machine, drain one, remove it. On hardware you own there is no thirteenth machine, so the roll has to work inside the headroom that Move 11 bought deliberately. That makes three things matter: disruption budgets that are honest, an inventory of pods that cannot be evicted, and awareness that a local volume from Move 47 pins its pod to one machine. The saving grace is that upgrades here are image-based with a fallback, so a bad image is a reboot back rather than a rebuild, which is what makes this reversible immediately.

## Before you start

**Access**
- The headroom from Move 11, confirmed to still exist after Move 69's scheduling work
- The failure-domain labels from Move 42, because the roll is ordered by them

**Software**
- A disruption budget audit: every workload, its budget, and whether that budget is achievable
- Reboot orchestration that reads the rack, feed and switch labels and respects a concurrency limit

**People**
- The owner of any workload pinned to a local volume, because theirs is the one that sees a window

## The runbook
1. Audit the disruption budgets before rolling anything. A budget that permits zero disruption blocks the drain forever, and a budget nobody set permits everything. Both are common.
2. List the pods that cannot be evicted: single-replica workloads, pods with local volumes from Move 47, and anything without a controller. Each is a decision rather than an obstacle.
3. Order the roll by failure domain using the labels from Move 42. One rack at a time, or one feed at a time, so that a mistake affects a domain the estate is designed to lose.
4. Set a concurrency budget and hold to it. The temptation on a slow roll is to widen it, and widening it is how a fleet roll becomes an outage.
5. Roll with the image-based upgrade and its fallback. A machine that does not come back healthy is rebooted into the previous image, which is a minutes-long recovery rather than a reprovision.
6. Accept the ten minutes where it applies. A workload pinned to a local volume is unavailable while its machine reboots; anything with a replica in another rack sees nothing at all.
7. Time the first full roll and record it. That number is the input to Move 108's calendar and to Move 116's capacity planning.

## Operator's notes
- **Swap:** Where headroom is genuinely insufficient, the cold spare machine from Move 19 can be racked temporarily as the surge node. It is exactly what it is for.
- **Do it faster:** Roll the non-production cluster first, always. It finds the disruption-budget problems at no cost.
- **Watch out:** A drain that hangs is almost always a disruption budget that cannot be satisfied, and the temptation is to force it. Forcing a drain kills the pod the budget was protecting.
- **Leftovers:** Node auto-repair and the surge capacity settings stay configured on the old cluster and stop billing when it does.

## Rollback
An image-based upgrade with a fallback is reverted by rebooting into the previous image, so a bad roll is undone per machine within minutes. There is no point of no return in this Move. Where a workload with a local volume did not come back, the way back is the restore path built in Move 74 or Move 115 rather than anything in this Move, which is why those exist before this one.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 10 min | 1 week | — |

## What you can turn off
Nothing here. This Move replaces a capability rather than a service, and its cost is headroom you already bought.
