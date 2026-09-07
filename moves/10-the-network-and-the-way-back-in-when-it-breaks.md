# 10 · The network, and the way back in when it breaks

**Layer:** Build · **Leaving:** Cloud-managed private networking · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Four address ranges written down before anything is configured, two switches either of which may fail, and a way in that depends on neither.

## Leaving from
- **AWS:** VPC and its subnets — a subnet is pinned to one Availability Zone and its block is fixed at creation, and frames run at 9001 bytes inside the VPC but 1500 through the internet gateway.
- **Google Cloud:** VPC networks and subnets — the MTU belongs to the network rather than the instance, and every virtual machine must be restarted before it uses a changed value.
- **Azure:** Virtual Network and its subnets — no broadcast or multicast on the wire, so gratuitous ARP and VRRP never worked and a floating address had to be a load balancer.

## Why this works
The address plan is cheap to get right today and expensive to change in a year, because by then it sits in a partner's firewall and on every machine. It is written first, on paper: four ranges, each with twice the room the estate needs now. The switches come as a pair, since one switch is one maintenance window that takes everything down with it. MTU gets a step of its own, because a mismatch does not fail cleanly — it passes small requests and stalls large ones. Nothing here carries production traffic yet, which is what makes the week safe.

## Before you start

**Access**
- Console access to both switches, and the out-of-band line from Move 09 answering
- The public address range from Move 08, and the private ranges the organisation already uses

**Software**
- `ipmitool` 1.8.19 or newer, to prove the baseboard controllers answer on the management range
- A packet test that sets the do-not-fragment bit, because a default-size ping proves nothing here

**People**
- Two engineers for the switch-pull drill, one at the rack and one watching the graphs

## The runbook
1. Write the address plan before touching a switch. Four ranges — management, storage, node addressing and the public block from Move 08 — none overlapping the office, the cloud accounts or anything a partner routes. It lives in source control and nowhere else.
2. Cable the two top-of-rack switches as a multi-chassis pair with a peer link, and run two uplinks from every node into different switches, bonded. One switch then fails as a component rather than as an outage.
3. Build the management VLAN with no route to the internet. The baseboard controllers and the out-of-band circuit sit on it, and the way in is a jump host, never a public address. Prove it from outside the building with an `ipmitool` power status on every node.
4. Set the MTU identically on every switch port, every bond and every node, and record the number beside the address plan. Undocumented mixed segments are how a fortnight disappears.
5. Test with full-size packets that refuse fragmentation, on every path that will carry traffic. A mismatch breaks about five per cent of it and reads as an application bug for a week.
6. Run the drill in daylight, with both engineers watching. Pull the power from one switch, confirm every bond keeps a member, then plug it back in and confirm the link rejoins. Nobody who declines this today will do it under load.

## Operator's notes
- **Swap:** Where the switches will not do multi-chassis aggregation, give each node an address per uplink and let it route to both independently: more host configuration, fewer shared failure modes.
- **Do it faster:** Generate both switch configurations from the address plan rather than typing them twice. Hand-built pairs differ in one port, and the drill is what finds it.
- **Watch out:** The way back in must not depend on the fabric it exists to rescue. A jump host on the data VLAN, or a mesh agent that needs the production default route, is neither.
- **Leftovers:** The cloud private network and its per-gigabyte charges keep running throughout, and nothing here removes them.

## Rollback
Nothing here carries production traffic, so backing out is reverting one switch configuration and restoring the previous one from source control. The point of no return is a date rather than a command: once node addresses and partner firewall entries reference the plan from step one, renumbering becomes a weekend rather than an edit. Argue the ranges into shape now, not after Move 11.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The cloud's private network carries every service you run until the traffic moves in Stage 5.
