# 10 · The network, and the way back in when it breaks

**Layer:** Build · **Leaving:** Cloud-managed private networking · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Address ranges written down before anything is configured, two switches either of which may fail, and a way in that depends on neither.

## Leaving from
- **AWS:** VPC and its subnets — a subnet occupies one Availability Zone; supported EC2 paths allow a 9001-byte MTU, but internet-gateway traffic is limited to 1500.
- **Google Cloud:** VPC networks and subnets — changing network MTU requires stopping all attached VMs, then starting them; a guest reboot is insufficient, and Windows needs an explicit interface update.
- **Azure:** Virtual Network and its subnets — no broadcast or multicast on the wire, so gratuitous ARP and VRRP never worked and a floating address had to be a load balancer.

## Why this works
The address plan is cheap to get right today and expensive to change in a year, because by then it sits in a partner's firewall and on every machine. It is written first, on paper: separate ranges, each with twice the room the estate needs now. The switches come as a pair, since one switch is one maintenance window that takes everything down with it. MTU gets a step of its own, because a mismatch does not fail cleanly — it passes small requests and stalls large ones. Nothing here carries production traffic yet, which is what makes the week safe.

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
1. Write the address plan before touching a switch. Reserve management, storage, host, guest, Kubernetes pod and service networks, and the public block from Move 08, none overlapping the office, cloud accounts or partner routes. For Proxmox, reserve cluster communication and migration paths; storage recovery must not starve quorum traffic. Store the plan in source control.
2. Cable the two top-of-rack switches as a multi-chassis pair with a peer link, and run two uplinks from every node into different switches, bonded. One switch then fails as a component rather than as an outage.
3. Build the controller VLAN with no route to the internet. Reach baseboard controllers and Proxmox administration through the independent jump host, with access rules separating controllers from host management. Guest networks cannot reach either; host updates use controlled outbound access. Prove it from outside the building with an `ipmitool` power status on every node.
4. Record the IP MTU for each path. Keep bonds, bridges and guest interfaces consistent, allow Ethernet and VLAN overhead in switch frame limits, and reduce tunnel-interface MTU for encapsulation. Internet and private storage paths need not share one MTU.
5. Test full-size packets that refuse fragmentation on every traffic path, then application requests through tunnels. Permit the ICMP messages used by path MTU discovery. Small pings can pass while larger requests stall; there is no fixed percentage of traffic a mismatch breaks.
6. Run the drill in daylight, with both engineers watching. Pull the power from one switch, confirm every bond keeps a member, then plug it back in and confirm the link rejoins. Nobody who declines this today will do it under load.

## Operator's notes
- **Swap:** Where the switches will not do multi-chassis aggregation, give each node an address per uplink and let it route to both independently: more host configuration, fewer shared failure modes.
- **Do it faster:** Generate both switch configurations from the address plan rather than typing them twice. Hand-built pairs differ in one port, and the drill is what finds it.
- **Watch out:** The way back in must not depend on the fabric it exists to rescue. A jump host on the data VLAN, or one hosted only inside the Proxmox cluster it must rescue, cannot recover that cluster.
- **Leftovers:** The cloud private network and its per-gigabyte charges keep running throughout, and nothing here removes them.

## Rollback
Nothing here carries production traffic, so backing out is reverting one switch configuration and restoring the previous one from source control. The point of no return is a date rather than a command: once node addresses and partner firewall entries reference the plan from step one, renumbering becomes a weekend rather than an edit. Argue the ranges into shape now, not after Move 11.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The cloud's private network carries every service you run until the traffic moves in Stage 5.
