# 49 · Ceph under Rook: block, shared filesystem and the object store

**Layer:** Cluster · **Leaving:** Managed network block storage, managed shared filesystems and managed object storage · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Installs Rook and Ceph for block and shared filesystem, and stands up the object gateway that Harbor, Loki and Velero will need before Part V begins.

## Leaving from
- **AWS:** EBS, EFS and S3 — three products, three billing models, and three sets of assumptions baked into your applications.
- **Google Cloud:** Persistent Disk, Filestore and Cloud Storage — the same three, with the shared filesystem sold in fixed capacity tiers.
- **Azure:** Managed Disks, Azure Files and Blob Storage — the same again, and the only one of the three offering a first-class Windows file-sharing protocol.

## Why this works
Three managed products are replaced by one system with three interfaces. Ceph provides block volumes, a shared filesystem and an object gateway from the same pool of devices, and Rook runs it as a set of Kubernetes resources rather than as a separate estate to administer. The failure domains come from the rack labels in Move 42, so the cluster spreads copies across racks rather than across machines that share a switch. The object gateway is stood up here rather than in Part V, because the registry, the log store, the backup tool and the database repository all need an object endpoint from Move 58 onwards.

## Before you start

**Access**
- The device count and capacity plan from Move 10, reconciled against what was actually delivered
- Machines installed with encryption from Move 48, since the devices are created encrypted

**Software**
- `helm`, with Rook at a pinned chart version and the Ceph version it supports rather than the newest one
- `ceph` for the health checks, and `kubectl` for everything the operator does not do for you

**People**
- A named owner for Ceph. This is the one condition this Move refuses to waive

## The runbook
1. Name the owner first. Ceph is a distributed storage system with its own failure modes, its own vocabulary and its own upgrade cadence, and an estate that runs it without somebody who understands it will have an outage nobody can diagnose.
2. Install Rook with `helm install` at a pinned chart version and let it create the storage devices encrypted, per Move 48. Encrypting them afterwards is a rebuild of every device, one at a time.
3. Build the placement rules on the rack labels from Move 42 rather than on machine names. A three-copy pool that puts all three copies in one cabinet is a pool that loses data when the cabinet loses power.
4. Set the replication scheme and the fullness thresholds against the drive count from Move 10. Reconcile them explicitly: a pool that will sit above the backfill threshold when one machine is lost is a pool that stops accepting writes during the recovery it exists for.
5. Create the block storage class and the shared filesystem, and confirm a claim binds, mounts, survives a machine reboot and can be restored from a snapshot before anything real uses either.
6. Stand up the object gateway with its own pool and its own placement, and create the first bucket. Move 58 onwards depends on this endpoint existing, so it is built now even though nothing uses it yet.
7. Pull a device out of a running machine and watch the cluster recover. Time it. That number is what Move 111 will be working against at three in the morning.

## Operator's notes
- **Swap:** Where the estate needs a Windows file-sharing protocol as a first-class citizen, Ceph does not provide it directly and a separate file-sharing tier or an application change is required. Only one of the three clouds offered it, and that reader has real work here.
- **Do it faster:** Build it on the second cluster from Move 51 first and break it deliberately several times. Every hour spent breaking it there is a day saved later.
- **Watch out:** The protection scheme on a data pool cannot be changed in place once the pool holds data. Choose replication or erasure coding deliberately, with the recovery cost understood, because changing your mind means a new pool and a copy.
- **Leftovers:** The managed volumes, filesystems and buckets keep billing until Part V has moved the data and Move 38 has removed them against a signed data-owner approval.

## Rollback
Uninstalling Rook before anything binds is clean. After that it is not: this Move is irreversible once a volume or a bucket holds data, because moving off Ceph is a data migration rather than a configuration change. The point of no return is the first bound volume or the first object written, not the installation. Prove the restore path before that point — take a snapshot, delete a claim, restore it — because a storage system nobody has restored from is a storage system nobody should be trusting.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,940/mo | $0/mo | 100% | 0 min | 3 weeks | — |

## What you can turn off
Nothing yet. The managed block, file and object services carry production until Part V moves the data off them.
