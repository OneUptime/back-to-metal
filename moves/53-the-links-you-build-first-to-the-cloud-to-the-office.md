# 53 · The links you build first: to the cloud, to the office

**Layer:** Cluster · **Leaving:** Physical data-transfer appliances and managed bulk-copy services · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the private circuit and the office link every later replication stream and mirrored comparison rides on, and prices the migration egress honestly.

## Leaving from
- **AWS:** Direct Connect or Site-to-Site VPN — a virtual interface over a cross-connect, or a tunnel, with data transfer priced per gigabyte.
- **Google Cloud:** Dedicated or Partner Interconnect, or Cloud VPN — the same shapes, with the least conditional exit terms of the three.
- **Azure:** ExpressRoute or VPN Gateway — the same again, with the strictest exit terms, requiring the subscription to be terminated.

## Why this works
Every stream in Parts V and VI rides on this link: the database replication, the object copy, the mirrored comparison in Move 72, the shadow edge in Move 102. Building it early and sizing it properly is what turns those Moves into waiting rather than into crises. Sizing is the part people get wrong, because the number that matters is not steady-state throughput but catch-up throughput — three to five times steady state, so that a stream which falls behind can recover inside a working day rather than inside a fortnight. The lead time is what belongs on the schedule, not the work.

## Before you start

**Access**
- The cross-connect ordered in Move 26, with the provider's authorisation paperwork still inside its validity window
- The address plan from Move 39 and the routed fabric from Move 45

**Software**
- The provider's circuit configuration, and a tunnel configuration as the interim path while the circuit is provisioned
- A throughput test that runs for hours rather than seconds, because the interesting failures are sustained ones

**People**
- Whoever negotiated the cloud contract, because the exit terms need to be obtained in writing before the first byte moves

## The runbook
1. Order the circuit early. Six to twelve weeks is normal, this Move sits inside that wait rather than beside it, and every Part V date depends on it.
2. Build the tunnel first as the interim path. It is available in an afternoon, it carries the low-volume traffic, and it means Parts IV and V are not blocked on a physical order.
3. Address and route both links against the plan from Move 39 and the fabric from Move 45, so that the office prefix and the cloud prefix are reachable from the cluster without exceptions.
4. Size for catch-up rather than for average. Three to five times steady state is the working rule, and the test that matters is a sustained transfer, not a burst.
5. Price the migration egress honestly, including the per-gigabyte charge a managed address-translation gateway adds on top of the transfer itself. That second charge is routinely missed and it is frequently the larger of the two.
6. Get the exit terms in writing before the first byte moves. All three providers now waive egress charges for a customer who is leaving, on materially different terms: one is close to unconditional, one reviews each request and does not require the account to close, and one requires the subscription to be terminated and the move completed inside sixty days. Regional law is also moving on this, and none of it helps unless you asked first.
7. Test the whole path end to end with a sustained transfer and record the achieved throughput. That number, not the circuit's badge speed, is what Part V plans against.

## Operator's notes
- **Swap:** Where the volume is small enough, the tunnel is the whole answer and no circuit is needed. Measure before ordering: a tunnel over good transit carries more than people expect.
- **Do it faster:** Run the free-egress request in parallel with the circuit order. Both take weeks and neither blocks the other.
- **Watch out:** A physical transfer appliance is still the right answer for very large one-off copies, and it is slower to arrange than people assume. Decide early, because it has its own lead time.
- **Leftovers:** The circuit and its port charges continue until Part VII. Do not cancel it when the last workload moves; Move 121's abort path needs it.

## Rollback
Both links are removed by withdrawing routes and cancelling the circuit, and neither leaves anything behind. The point of no return does not exist in this Move, though the circuit's minimum term does have a cost attached. Keep the routing configuration and the negotiated exit terms in source control, so the commercial position can be restored and quoted back when a provider's support desk disagrees with what was agreed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | 6 to 12 weeks |

## What you can turn off
Nothing yet. This Move adds a circuit charge that runs alongside the cloud bill until Part VII.
