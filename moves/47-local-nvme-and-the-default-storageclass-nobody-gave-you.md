# 47 · Local NVMe, and the default StorageClass nobody gave you

**Layer:** Cluster · **Leaving:** Managed network block storage and its default StorageClass · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Puts databases on local NVMe with power-loss protection, keeps replication in the application, and marks a default StorageClass so PVCs stop hanging Pending.

## Leaving from
- **AWS:** EBS with the EBS CSI driver — recent EKS versions ship no default StorageClass at all, so a hanging claim is already a familiar surprise here.
- **Google Cloud:** Persistent Disk with a default StorageClass — provided, so the missing default is a new experience for this reader.
- **Azure:** Managed Disks with a default StorageClass — also provided, with the same consequence.

## Why this works
A database on network storage pays a round trip on every write and inherits a second system's failure modes. A database on local flash does not, and the durability that the network volume was providing is moved into the application, where it belongs: replicas on other machines, and a backup repository somewhere else. This is why local volumes come before Ceph rather than after — Ceph sits on top of these devices in Move 49, while the consensus store and the single-writer databases stay underneath. The cost is real and specific: a local volume pins its pod to one machine, which is what makes the drain arithmetic in Move 109 and the failed device in Move 111 interesting.

## Before you start

**Access**
- The devices specified in Move 09, with power-loss protection confirmed rather than assumed
- The cluster from Move 43 with machines provisioned by Move 42

**Software**
- The Talos user-volume configuration and a local volume provisioner, both pinned to versions
- `kubectl` to mark the default StorageClass and to watch binding behaviour

**People**
- Whoever will own the databases in Part V, because this is the storage they will be running on

## The runbook
1. Declare the user volumes in the machine configuration with the filesystem and mount options you intend to keep. Changing them later means draining the machine and recreating the volume.
2. Install the local volume provisioner at a pinned version and confirm it discovers the devices on every machine, with the right sizes and the right names.
3. Set binding to wait for the first consumer. Without it the scheduler binds a claim to a machine before it knows where the pod can run, and the pod then cannot be scheduled anywhere else.
4. Mark a default StorageClass. Recent managed clusters on one of the three clouds ship without one, and the symptom is a claim that stays pending forever with no error that says why.
5. Verify power-loss protection is present on every device that will hold a database, and record the result per serial number. This is the property the whole of Part V rests on.
6. Write down the consequence in the runbook, plainly: a pod with a local volume runs on one machine and only that machine. Draining it means moving the data or accepting the outage, and Move 109 and Move 111 are where that bill arrives.

## Operator's notes
- **Swap:** Where a workload genuinely needs to move between machines freely and cannot replicate itself, put it on Ceph in Move 49 and accept the latency. The choice is between where the replication lives, not whether it exists.
- **Do it faster:** Name the storage classes after what they are for rather than after the technology. A developer choosing between two classes should not need to know what either is made of.
- **Watch out:** A local volume that is deleted takes its data with it and there is no undelete. The reclaim policy is a decision, and the wrong one is discovered exactly once.
- **Leftovers:** The managed block volumes and their snapshots keep billing in the cloud until Part V has moved the data and Move 38 has removed them deliberately.

## Rollback
The default StorageClass is flipped back in a minute, but this Move is irreversible in the way that matters: once a claim is bound to a local device there is no way back except a data migration with a write stop, which is not a configuration change. The point of no return is the first bound claim. Everything before that is free. Keep the volume configuration in source control, and make sure a backup exists and has been restored before anything real binds, because a local device has no snapshot behind it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,480/mo | $0/mo | 100% | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The managed volumes carry production until Part V, and their snapshots stay for thirty days after that.
