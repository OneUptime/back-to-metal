# 45 · BGP to the top-of-rack, and the MTU that breaks five per cent

**Layer:** Cluster · **Leaving:** Cloud network routing and managed transit hubs · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Advertises pod prefixes to the leaf switches over BGP and settles the MTU, including the path-MTU black hole that hangs large responses rather than failing them.

## Leaving from
- **AWS:** VPC route tables with Transit Gateway — routes were API objects and a managed hub computed the paths between networks.
- **Google Cloud:** VPC routes with Network Connectivity Center — the same, and the shortest journey of the three, because an alias-address pod range was already routable inside the network.
- **Azure:** user-defined routes with Virtual WAN — again managed routing, with the hub doing the work your leaf switches are about to do.

## Why this works
With real pod prefixes advertised to the switches, there is no overlay: a packet from one pod to another is routed by the fabric, with no encapsulation, no extra header and nothing to debug in the middle. The routing protocol is configured through the network plug-in's own resources rather than by hand on each machine, and how the two uplinks behave follows the redundancy decision taken back in Move 12. The other half of this Move is the maximum transmit unit, which is worth its own attention because getting it wrong does not produce a clean failure. It produces a black hole where small requests succeed, large responses hang, and about five per cent of traffic is mysteriously broken.

## Before you start

**Access**
- Switch configuration access on both leaves, and an agreed maintenance approach for changing routing on them
- The address plan from Move 39, so the advertised prefixes are the ones everyone expects

**Software**
- The routing configuration for the network plug-in, using its current resources rather than the deprecated ones
- A path-discovery test that sends full-size packets, because a small ping proves nothing about this

**People**
- Whoever administers the switches, since the peering has two ends and one of them is theirs

## The runbook
1. Configure the routing peers on both leaf switches and on the cluster side, using the current resources rather than the deprecated peering policy. Peer each machine with both leaves so the loss of one switch removes one path and not the machine.
2. Advertise the pod prefixes and confirm they appear in the switch routing tables with the next hops you expect. A prefix advertised but not installed is the most common first fault and it is usually a filter on the switch.
3. Route the office prefix through the fabric so that the link built in Move 53 has somewhere to land. Doing it now means the office link is a routing change rather than a design change later.
4. Settle the maximum transmit unit across every segment, and write down which segments are large-frame and which are not. Mixed segments are normal; undocumented mixed segments are how this fails.
5. Test with full-size packets across every path, including the ones through the office link and the cloud circuit. A black hole is invisible to a small ping and obvious to a large one, and it presents to application teams as intermittent slowness rather than as a network fault.
6. Fail one leaf switch deliberately, with no workloads running, and confirm the routes converge and traffic continues. Then fail the other. This is the drill that proves the fabric decision from Move 12 was implemented rather than merely designed.

## Operator's notes
- **Swap:** Where the switches will not run a routing protocol at all, a routed overlay works and costs a header, some throughput and a debugging tool. It is the right answer where the fabric is not yours.
- **Do it faster:** Agree the peering parameters with the network administrator once, in a document, and apply the same pattern to every rack. Per-rack improvisation is how a fabric becomes two fabrics.
- **Watch out:** Large frames must be consistent along the whole path, including the switch uplinks and anything in between. One device at the default size in the middle of a large-frame path is exactly the black hole this Move exists to prevent.
- **Leftovers:** The cloud transit hub keeps billing per attachment and per gigabyte until Part VII. It is also the path Move 53 rides on, so it stays.

## Rollback
Routing changes are reverted by withdrawing the advertisements and restoring the previous switch configuration, which is a minutes-long operation with no workloads on the cluster. The point of no return does not exist here; the risk is entirely about doing it later, with production on the fabric, when a routing mistake is an outage rather than an experiment. Keep both switch configurations and the cluster routing resources in source control so the working state can be restored quickly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The managed transit hub carries the migration traffic and stays until Part VII.
