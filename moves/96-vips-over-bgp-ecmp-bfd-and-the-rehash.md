# 96 · VIPs over BGP: ECMP, BFD and the rehash

**Layer:** Edge · **Leaving:** Managed cross-zone load balancing and anycast front ends · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Advertises service addresses to the leaf switches so ECMP spreads them across nodes, with BFD for fast withdrawal and resilient hashing to protect live flows.

## Leaving from
- **AWS:** cross-zone load balancing on the Network Load Balancer — distribution across zones handled invisibly and billed as capacity units.
- **Google Cloud:** the global external load balancer with anycast — a single address answered from many places, which is the property that does not come with you.
- **Azure:** Standard Load Balancer with zone redundancy — the same distribution, expressed as a zone property of the front end.

## Why this works
Move 95 made an address exist on one node. This Move makes it exist on all of them, by advertising it to both leaf switches so that the fabric spreads traffic across every node that is ready to receive it. Two details decide whether it behaves well. The default routing hold timers leave a dead node attracting traffic for tens of seconds, which is fixed by adding sub-second failure detection. And on many switches, changing the set of next hops rehashes every flow, so an ordinary node drain resets established connections unless the switch supports a hashing scheme designed to avoid exactly that.

## Before you start

**Access**
- The routing sessions from Move 45, already established and stable, on both leaf switches
- The redundancy answer from Move 12, because it decides how the two uplinks behave here

**Software**
- Service address advertisement configured through the network plug-in, per pool
- Sub-second failure detection enabled on both ends, and resilient hashing confirmed on the switch

**People**
- The switch administrator, because the hashing behaviour is configured on their side

## The runbook
1. Configure advertisement of the service address pool through the network plug-in, alongside the pod prefixes already advertised in Move 45. Cut one pool at a time with the Move 95 path still holding the address.
2. Confirm the addresses appear on both leaf switches with multiple next hops, and that traffic is genuinely spread rather than all arriving at one node.
3. Fix the failure detection. Default hold timers mean a dead node keeps attracting traffic for tens of seconds; sub-second detection between the node and the switch reduces that to under a second, and it is the single most valuable setting in this Move.
4. Check the rehash behaviour explicitly. Drain a node and watch whether established connections on the other nodes survive. On many switches they do not, because the next-hop set changed and every flow rehashed.
5. Where the switch supports resilient hashing, turn it on and repeat the drain test. Where it does not, know that a drain resets flows and plan node maintenance in Move 109 accordingly.
6. Spend the second half of the week testing failure rather than success: kill a node, kill a switch, drain a node gracefully, and watch each case.
7. Leave the Move 95 configuration in place. It is the abort path, and reverting is one manifest change.

## Operator's notes
- **Swap:** Where the fabric will not run a routing session with the hosts, the layer-2 mode from Move 95 remains a working answer for a small estate, with the single-node limitation stated.
- **Do it faster:** Cut the internal service pool first. It exercises everything and no external user is watching.
- **Watch out:** An anycast front end answering from many locations is a property of a global network, and you are not building one. What you have is one site with distributed reception, and Move 105 is where geography comes back.
- **Leftovers:** The managed balancer keeps billing throughout, which is expected until Move 103.

## Rollback
Reverting is one manifest change back to the Move 95 path, which is still configured and still able to hold the address. There is no point of no return here, and nothing is serving production through these addresses until Move 103. Keep the switch configuration and the advertisement resources in source control so a working routing state can be restored quickly, because a routing mistake here is fast and total rather than gradual.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing. The managed balancer keeps every user until Move 103.
