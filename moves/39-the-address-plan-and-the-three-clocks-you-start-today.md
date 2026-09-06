# 39 · The address plan, and the three clocks you start today

**Layer:** Cluster · **Leaving:** Cloud-managed private addressing and inter-network transit · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Fixes the pod, service, node and management ranges before a machine is racked, and starts the RIR, partner-allowlist and hiring clocks that nothing compresses.

## Leaving from
- **AWS:** VPC address ranges with Transit Gateway — the ranges were yours to pick and the routing between them was a managed service.
- **Google Cloud:** VPC subnets with secondary ranges — pod and service ranges belong to the network rather than to the cluster, so the plan has to match ranges that already exist.
- **Azure:** Virtual Network address space with peering or Virtual WAN — the same picking exercise, with peering rather than a hub doing the transit.

## Why this works
Addressing is the one design decision that is free to change today and extremely expensive to change in eighteen months, because by then it is in firewall rules at partners you do not control. So the whole plan is allocated at once: pod, service, node, management, provisioning and a reserved range for a second site, none of which may overlap each other, the offices, any partner you will connect to, or the private space an acquisition will bring with it. The second half of this Move is not technical at all. Three clocks — registry membership, partner allowlisting and hiring — take months and nothing compresses them, so they are started this afternoon.

## Before you start

**Access**
- The current address ranges in every cloud account, exported, including the ones nobody uses
- The office ranges and every partner range you already connect to

**Software**
- A single address plan document, in source control, that is the only place ranges are recorded
- The registry membership application for your region, opened rather than bookmarked

**People**
- Whoever can sign a registry membership and whoever owns hiring, because both clocks start today

## The runbook
1. Inventory every private range already in use across the clouds, the offices and the partners. Overlaps discovered later cannot be routed around; they have to be renumbered, and renumbering a production network is a project rather than a change.
2. Allocate the ranges in one pass, with room to grow: pods, services, nodes, management, provisioning, and a reserved block for the second site that Move 24 declined to build this year. Write down why each is the size it is.
3. Keep the pod range generous. Pod addresses are consumed per node and the number of nodes grows; a pod range sized to today's cluster is the most common address plan mistake and it surfaces as pods that will not schedule.
4. Reconcile with the Google case explicitly if you are leaving it. There, pod and service ranges are secondary ranges owned by the network rather than by the cluster, so the plan has to align with ranges that already exist rather than being invented.
5. Start the registry clock. Membership and an address allocation take weeks to months depending on region, and Move 91 cannot begin until it is done. Apply today, before the first machine is racked.
6. Start the other two clocks the same afternoon: allowlist requests with every partner whose firewall will need your new addresses, and the hiring you concluded you needed in Move 22.

## Operator's notes
- **Swap:** Where an overlap with an office range is unavoidable, translation at the boundary works and is unpleasant. It is a reason to renumber the office rather than the cluster, because the office has fewer dependencies.
- **Do it faster:** Allocate on a clean boundary with obvious arithmetic, so that a person reading a firewall rule can tell what it is for without looking anything up.
- **Watch out:** Cloud-managed transit hubs did route summarisation for you. On your own fabric, an address plan that does not summarise produces a routing table that is hard to read and slow to converge.
- **Leftovers:** The old cloud ranges stay live throughout the migration and are only reclaimed in Part VII. Do not reuse them in the new plan.

## Rollback
On paper this Move is free to redo, and it should be redone as often as needed until it is right. The point of no return is Move 42, which addresses the first node from this plan, and every day after that adds firewall rules at other people's organisations. The registry application can be withdrawn without penalty. Keep the plan in source control as the single source of truth, so an earlier allocation can be restored and compared when somebody claims a range was always meant for something else.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 5 days | 6 to 12 weeks |

## What you can turn off
Nothing yet. The cloud networks carry production for the whole of Parts III and IV.
