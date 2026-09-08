# 12 · Disks: what goes local, what goes on Ceph

**Layer:** Build · **Leaving:** Managed block and shared-file storage · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Ceph takes three drives a node for anything that must survive a node dying. The fourth stays raw under PostgreSQL, which already replicates itself.

## Leaving from
- **AWS:** EBS and EFS — a gp3 volume lives in one Availability Zone and caps at 16,000 IOPS however large it grows, and EFS in bursting mode spends credits that run out.
- **Google Cloud:** Persistent Disk and Filestore — Persistent Disk performance scales with provisioned size and the attached machine's vCPU count, and a Filestore instance grows but never shrinks.
- **Azure:** Managed Disks and Azure Files — Premium SSD steps in fixed tier sizes rather than a dial, and premium file shares need a FileStorage account that standard shares cannot move into.

## Why this works
Two storage systems, and one rule for choosing between them. Ceph, run by Rook, takes anything that must survive a node dying without waking anybody: replicated block volumes, a shared filesystem for the few things that need one, and the object gateway Move 15 and Move 16 build on. PostgreSQL takes the other path, a raw local drive with nothing replicating beneath it. The volume it used to sit on provisioned a few thousand IOPS; the four drives already in the machine will do several hundred thousand. A database writes copies to its own standbys, so a layer repeating that work underneath spends flash to buy nothing.

## Before you start

**Access**
- The device inventory from Move 09, with the four NVMe drives on each node known by serial
- A Talos machine configuration you can edit and roll, because disk layout is fixed at boot

**Software**
- `helm` and `kubectl`, with the Rook chart pinned rather than tracking whatever is newest
- `ceph` for health, capacity and recovery output during the drive-pull test

**People**
- One named owner for Ceph, who will read its health output on the day it is unhappy

## The runbook
1. Name the owner for Ceph, then write the split into the Talos machine configuration: three of the four NVMe devices per node to Ceph, the fourth raw for PostgreSQL. Layout is fixed at boot, so changing it later means draining one node at a time.
2. Install Rook with `helm install rook-ceph rook-release/rook-ceph --version 1.16.9` and let the operator adopt the 15 devices offered. Take the Ceph release that chart version ships with, not the newest published.
3. Create a replicated block pool with three copies and `min_size 2`, a shared filesystem, and the object gateway on its own pool. Erasure coding does not belong under block storage on five nodes: too few failure domains, and a pool holding data will not take a different scheme later.
4. Size for recovery, not for today. Losing one node of five pushes a fifth of the data onto the survivors, so run `ceph df` and hold the pools under 70 per cent. Fuller than that, recovery backfills into a wall and writes start failing.
5. Bind a claim with `kubectl`, write to it, reboot the node beneath it and check the contents survived. Repeat on the shared filesystem, then create the first bucket on the gateway; Move 15 and Move 16 expect that endpoint already.
6. Pull a drive from a running node and time the recovery with `ceph -s`, once the claims above are verified and nothing real is bound. Reseat it and watch the cluster take it back. That number is what somebody works against the first time a device dies for real.

## Operator's notes
- **Swap:** A workload that must move between nodes freely and cannot replicate itself goes on Ceph block, latency included. The choice is which layer pays for replication.
- **Do it faster:** Name the storage classes for the promise they make, not the technology beneath. An engineer picking one is choosing durability, not a product.
- **Watch out:** Ceph says loudly that it is unwell and quietly why. Learn to read `ceph health detail` on a calm afternoon rather than during an outage.
- **Leftovers:** The managed volumes, file shares and their snapshots bill right through Stage 4. This Move stands the replacement up; it stops nothing.

## Rollback
Nothing is bound yet, so removing Rook and handing the devices back is a morning's work — until the first claim binds or the first object lands in the gateway. That is the point of no return: after it, leaving Ceph is a data migration with a write stop, not a configuration change. Prove the way back before you get there — snapshot a test volume, delete the claim, restore it, confirm the contents match. The raw drives hold nothing until Move 16.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $880/mo | $80/mo | 91% | 0 min | 4 days | — |

## What you can turn off
Nothing this week. The managed disks and shares carry production until Stage 4 moves what is on them; the line dies in Move 15 for the buckets and Move 16 for the database.
