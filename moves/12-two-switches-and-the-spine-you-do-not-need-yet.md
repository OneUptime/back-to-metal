# 12 · Two switches, and the spine you do not need yet

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the second rack is cabled

> Chooses the fabric topology from measured east-west traffic, refuses a spine below four racks, and records whether the fabric runs MLAG or BGP to the host.

## Leaving from
- **AWS:** VPC networking — a flat, high-bandwidth fabric with no topology you could see and no oversubscription you could measure.
- **Google Cloud:** VPC networks and subnets — the same absence of shape, with the added property that a network spans regions, which nothing you build will do.
- **Azure:** Virtual Networks — again a fabric with no visible shape, plus accelerated networking as the one knob that hinted there was hardware underneath.

## Why this works
A leaf-spine diagram is the standard answer to a question most estates do not have. Below four racks, a pair of top-of-rack switches with a peer link between them carries everything, costs a fraction as much, and has fewer devices to fail and fewer to upgrade. A spine earns its place when the rack count or the cabling makes a direct mesh unmanageable, and buying it early spends ports, optics, power and rack units for years before anything uses them. What decides the shape is the east-west traffic you have actually measured, and the second output — whether the fabric runs a multi-chassis link aggregation or plain routing to the host — determines how Cilium is configured in Move 45 and how service addresses are advertised in Move 96.

## Before you start

**Access**
- East-west traffic measurements from the existing estate, per availability zone and between zones
- The rack count and machine count from Move 11

**Software**
- Flow data from the current cloud, exported for a representative week rather than a quiet Sunday
- A cabling diagram tool, or graph paper, because the mesh is easier to refuse once drawn

**People**
- Whoever will be cabling the racks in Part II, since a topology nobody can cable is not a topology

## The runbook
1. Measure east-west traffic properly, per hour, across a full week. Most estates discover their real internal traffic is an order of magnitude smaller than they assumed, and a small number of pairs — the application to its database, the log shipper to its store — account for nearly all of it.
2. Compute the oversubscription ratio you would run at with a given uplink count, using those measurements. A ratio between three and one and five and one is unremarkable for general workloads; storage replication traffic is the thing that argues for less.
3. Decide the topology from that number and the rack count. One to three racks is a pair of top-of-rack switches with a peer link and no spine. Four or more, or a cabling plan that has become a mesh, is where leaf-spine starts paying for itself.
4. Settle the redundancy model, and settle it now rather than at installation. Either the two leaves present as one logical switch to the host through a multi-chassis link aggregation, or each leaf is an independent router and the host runs a routing protocol to both. Both work; they lead to different configurations in Part III.
5. Size uplinks and leave ports free. A fabric with no spare ports is a fabric that cannot absorb the next rack, and ports are cheapest when bought with the switch.
6. Write the topology decision down with the traffic data attached, because it will be challenged by somebody holding a reference architecture, and the traffic data is the only answer that ends that conversation.

## Operator's notes
- **Swap:** Where a spine is genuinely needed later, adding one to a well-cabled pair of leaves is a planned change with a maintenance window, not a rebuild. Design the addressing in Move 39 so that it stays true.
- **Do it faster:** Draw the cabling for the target rack count before choosing. If it fits on one page and a person can follow it, you do not need a spine.
- **Watch out:** A multi-chassis link aggregation is two switches pretending to be one, and the pretence has failure modes — split brain, unequal state, upgrade coupling — that plain routing does not. Choosing it because the diagram is simpler is choosing it for the wrong reason.
- **Leftovers:** Cloud flow logs cost money to keep and this Move is the last time you need them at this resolution. Turn the sampling back down when you are done.

## Rollback
A topology decision is free to change right up until the second rack is cabled, because a pair of leaves with spare ports can become the first two leaves of a spine design without recabling the first rack. The point of no return is the day the second rack's uplinks are terminated against a design, since undoing that means a fabric outage and an afternoon with a cable tester. Keep the traffic measurements and the cabling diagram in source control so the original design can be restored and compared when the third rack arrives.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet, though the flow-log sampling rate this Move needed can go back down as soon as the measurement is finished.
