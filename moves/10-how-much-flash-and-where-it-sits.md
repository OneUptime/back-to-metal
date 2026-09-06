# 10 · How much flash, and where it sits

**Layer:** Iron · **Leaving:** Block volumes that grow with an API call · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the bays are full

> Turns the measured capacity requirement into drives against Ceph's replication and its nearfull thresholds, and separates the etcd, local-NVMe and OSD tiers.

## Leaving from
- **AWS:** EBS — a volume grew with a modify call and the capacity behind it was somebody else's planning problem.
- **Google Cloud:** Persistent Disk and Hyperdisk — the same elasticity, with performance provisioned separately from capacity on the newer types.
- **Azure:** Managed Disks — resized in place with the same one-way ratchet, since none of the three let you shrink a volume afterwards either.

## Why this works
Capacity used to be a request. Now it is a purchase with a lead time, and the arithmetic between the two is not one to one, because a replicated storage system consumes more raw space than it presents. Three-way replication triples raw consumption. Erasure coding does not, and pays for it in recovery cost when a device fails. Both need free space held back, because Ceph warns at eighty-five per cent, stops backfilling at ninety and stops accepting writes at ninety-five — so a cluster planned to sit at its nearfull mark passes every check on a healthy day and fails during precisely the recovery it was bought for.

## Before you start

**Access**
- The measured capacity and write rate from Move 01, separated by workload rather than summed
- The bay count per chassis from Move 07, and the device choice from Move 09

**Software**
- A capacity model you can show people, with the replication factor and the reserve as visible inputs
- The Ceph documentation for the version you intend to run, since the default thresholds are version-specific

**People**
- Whoever owns the largest dataset, to say how fast it is actually growing rather than how fast it grew once

## The runbook
1. Separate the three tiers before sizing any of them, because they have different endurance, different sizes and different failure consequences: a mirrored pair of small high-endurance drives per control-plane node for etcd, local NVMe for the single-writer databases that will not sit on a replicated pool, and the OSD devices that make up the cluster's own storage.
2. Size the OSD tier from usable capacity backwards. Decide the replication scheme per pool, multiply, then divide by the fraction of the cluster you are willing to fill. Planning to sixty-five per cent of raw is a reasonable default and anything above seventy-five is a decision that needs writing down.
3. Add the growth you actually measured plus the lead time you will actually face. Twelve to eighteen months of headroom is normal when new drives take six weeks to arrive, and it is cheaper than an emergency order.
4. Check the failure arithmetic. Losing one device must not push the cluster past its backfill threshold while it recovers, and losing a whole node must leave enough space for the data that node held to land somewhere. Both of those are capacity questions, and both are missed.
5. Buy chassis with bays deliberately left empty. Capacity that grew with an API call now grows only when somebody walks to the rack, and an empty bay is the cheapest form of that walk.
6. Write down the point at which you would add a node rather than more drives, and what triggers it. Without that line, a cluster grows by drive until it is unbalanced and nobody can say when that happened.

## Operator's notes
- **Swap:** For cold, large, rarely-read data, erasure coding across more nodes saves real money. It costs recovery time and CPU, and it is a poor choice for anything latency-sensitive.
- **Do it faster:** Model the cluster at full, at one device down and at one node down in the same spreadsheet. Three columns settle most of the arguments this Move produces.
- **Watch out:** Mixed drive sizes in one pool skew placement, so the largest devices take proportionally more data and fill first. Keep a pool's devices the same size, or accept the imbalance deliberately.
- **Leftovers:** The old provider's volumes keep billing after the data has moved, and unattached ones bill silently. They are deleted in Part V, after the copy is proven, and not before.

## Rollback
Until the bays are full, this is reversed by ordering more drives, which is the whole point of leaving them empty. After that it becomes a node purchase with a lead time. The point of no return is the moment the bays fill and the next increment is a chassis rather than a device. Under-buying is recoverable and over-buying is money spent early; both are survivable. Keep the capacity model in source control so an earlier version can be restored and compared against what the cluster actually consumed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. The provider volumes stay until Part V has moved the data and proved the copy.
