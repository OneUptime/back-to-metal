# 09 · The drive you are allowed to put etcd on

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Per drive, at the cost of a Ceph rebuild

> Fixes interface, form factor and endurance, and makes power-loss protection a hard requirement, because a drive without it is a quorum defect you have bought.

## Leaving from
- **AWS:** EBS io2 and gp3, and instance store — durability, endurance and power-loss behaviour were the provider's problem, expressed as an IOPS number you paid for.
- **Google Cloud:** Persistent Disk and Local SSD — the same split, with local devices explicitly ephemeral so nobody was tempted to trust them.
- **Azure:** Premium SSD v2 and local temporary disks — again a provisioned IOPS figure standing in for every physical property of the device underneath.

## Why this works
etcd is a consensus system that makes a durability promise on every write, so it calls fsync constantly and its latency is the fsync latency of the device under it. A drive with power-loss protection has a capacitor bank that lets it acknowledge a flush as soon as the data is in its own protected buffer. A drive without one must genuinely push the data to flash on every fsync, which turns a microsecond into a millisecond and turns a healthy cluster into one that loses leadership under load. That is why this is a hard requirement and not a preference: a consumer solid-state drive in a control-plane node is a quorum outage you have paid for in advance.

## Before you start

**Access**
- The chassis and bay configuration from Move 07, because the form factor question is decided by the backplane
- Datasheets for the candidate devices, with the endurance term stated rather than implied

**Software**
- A test rig capable of measuring fsync latency, not just throughput
- The vendor's compatibility matrix for the exact backplane in the exact chassis

**People**
- Whoever will hold the spares budget, since endurance class and spare count are the same conversation

## The runbook
1. Fix the interface first. NVMe for anything that matters, SATA only for cold bulk where cost per terabyte dominates, and SAS only where an enclosure you already own forces the issue. There is no case in this book for putting the cluster's consensus data on anything but NVMe.
2. Make power-loss protection a stated requirement on the purchase order, checked per part number. It is the property most often absent from a drive that otherwise looks identical on a comparison table.
3. Settle the form factor against the backplane, because compatibility runs one way. A U.2 drive works in a U.3 bay; a U.3 drive does not work in a U.2 bay. A mixed order placed without checking can arrive entirely unusable.
4. Set the endurance class in drive writes per day against the measured write rate from Move 01, and read the warranty term it is quoted over. Two drives with different terms are not comparable on that number alone, and the shorter term flatters the figure.
5. Separate the control-plane devices from everything else at order time: a mirrored pair of small, high-endurance drives per control-plane node, sized for the consensus data and its own snapshot rather than for capacity.
6. Name the wear metrics you will alarm on, and confirm the candidate reports them: percentage used, available spare against its own threshold, media and data integrity errors, and unsafe shutdowns. A drive that does not report these is a drive you will replace after it has already caused an incident.

## Operator's notes
- **Swap:** Where a control-plane node cannot take two devices, put the consensus data on the fastest single protected drive and take the node loss seriously. Three nodes each with one good drive beats three nodes each with two bad ones.
- **Do it faster:** Buy one of each candidate and measure fsync latency at queue depth one. It is a ten-minute test and it settles arguments that datasheets cannot.
- **Watch out:** Firmware matters as much as the part number. Fleets have been bitten by a specific firmware revision that reports wear incorrectly or drops out under a particular queue pattern, and the fix is a controlled update rather than a return.
- **Leftovers:** Drives pulled from the old estate are almost never suitable here. Unknown wear, unknown firmware, no protection, and the failure mode is silent.

## Rollback
A drive choice is reversed one device at a time, and outside the control plane that is a Ceph operation rather than an outage: mark the device out, let the cluster restore its data by backfilling from the surviving copies, and replace it. The cost is rebuild time and the risk window while the pool is degraded. The point of no return is the purchase order in Move 20, since a bay full of the wrong form factor cannot be corrected by software. Keep the compatibility matrix and the measured latency results with the bill of materials.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. This Move decides whether Part III has a control plane that stays elected.
