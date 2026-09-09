# 12 · Disks: what goes local, what goes on Ceph

**Layer:** Build · **Leaving:** Managed block and shared-file storage · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Choose who owns each physical disk. Proxmox supplies VM datastores; Rook supplies storage on the direct Talos path. Replication belongs in one layer.

## Leaving from
- **AWS:** EBS and EFS — a gp3 volume lives in one Availability Zone and its provisioned throughput is separate from capacity; EFS in bursting mode spends credits that run out.
- **Google Cloud:** Persistent Disk and Filestore — Persistent Disk performance depends on disk type, size and VM limits; Filestore basic tiers can grow but cannot shrink, unlike zonal, regional and enterprise tiers.
- **Azure:** Managed Disks and Azure Files — Premium SSD v1 uses performance tiers; Premium SSD v2 configures IOPS and throughput separately, and SSD file shares use a FileStorage account.

## Why this works
A VM needs a datastore before it needs Kubernetes. On the Proxmox path, the hosts own Ceph and present shared block storage to guests. On the direct Talos path, Rook manages Ceph on physical disks. Running another replicated Ceph inside guests whose disks already sit on host Ceph multiplies copies and hides the physical failure domains. Choose one owner per device.

PostgreSQL can use local NVMe because it replicates to its own standbys. That saves a second replication layer but binds each copy to its host. Its standbys must occupy different physical machines, even when the database runs inside Kubernetes VMs. The reference disk split and savings below describe the direct Talos build; price the VM datastore and its recovery capacity separately.

## Before you start

**Access**
- The device inventory from Move 09, with data drives identified by serial and boot drives excluded
- Proxmox storage administration or the Talos configuration from Move 11, according to the chosen platform

**Software**
- The Proxmox-supported Ceph package version pinned across hosts, including current security fixes
- `helm` and `kubectl` for Talos or external Ceph clients, with Rook 1.20.7 and Ceph 20.2.4 pinned in the deployment configuration
- `ceph` for health, capacity and recovery output during the drive-pull test

**People**
- One named owner for Ceph, including its object gateway and the recovery drill

## The runbook
1. Record each disk's owner and confirm the selected devices are empty before provisioning. On direct Talos, reserve three data drives per participating node for Rook and the fourth for local PostgreSQL; exclude shelf spares. On Proxmox, assign host datastore disks separately from any local database devices.
2. For Proxmox, use its Ceph wizard with the pinned packages, monitors on separate physical hosts, and only the recorded datastore devices. Add an RBD pool as VM storage. On Talos, add the official Rook chart repository and use `helm install rook-ceph rook-release/rook-ceph --version 1.20.7`. Apply a CephCluster configuration pinning Ceph 20.2.4 and the inventoried raw disks.
3. Set replicated pools to three copies and `min_size 2`, with the failure domain at the physical host. Use `ceph df` and model redistribution after losing the largest storage host; keep utilisation below 70 per cent and verify recovery still has room. Guest count is not a count of independent replicas.
4. Provision the shared filesystem and object gateway required by Moves 15 and 16. Rook creates these on direct Talos. For host-owned Ceph, its owner provisions CephFS and a separate RADOS gateway service; an RBD datastore alone supplies neither an S3 endpoint nor its credentials. Connect Kubernetes through Rook's external-cluster mode, with restricted client keys and the existing gateway endpoint, never guest OSD disks.
5. Keep each local PostgreSQL copy on a different physical host, with placement rules enforced during failover. If passing a disk or controller into a guest, give it exclusive ownership and exclude it from host Ceph. That guest loses ordinary live migration; database replication and a tested restore provide its recovery path.
6. On Proxmox, move ordinary guest disks from Move 11's local bootstrap datastore to shared RBD. Verify every required disk and network exists on eligible hosts, then register those guests as HA resources with negative resource-affinity rules separating control planes. Exclude guests tied to local or passthrough devices. Write test data to a VM disk or a claim created with `kubectl` on Talos. Power off one physical host and verify recovery and contents, including the filesystem and gateway. Confirm no failure removes every database replica.
7. With only verified test data present, pull a storage drive and time recovery with `ceph -s`. Reseat it, wait for health to recover, and record the duration before accepting production data.

## Operator's notes
- **Swap:** Proxmox can use existing shared storage or local datastores. Local disks need transfer during migration; host failure needs replication or restore, so demonstrate the promised recovery before choosing them.
- **Do it faster:** Name storage classes and datastores for the recovery promise they make, so each workload gets a deliberate placement.
- **Watch out:** Snapshotting a volume is not an independent backup. Keep a tested copy beyond the storage cluster that serves it.
- **Leftovers:** The managed volumes, file shares and snapshots keep billing until their contents have moved and the retention window ends.

## Rollback
Before test data lands, backing out means removing the empty pools and restoring the recorded disk layout. The point of no return is the first production write: leaving either Ceph or a local datastore then requires a data migration with a write stop. Back up a test VM or volume outside this cluster, restore it elsewhere, and verify its contents before acceptance. A local database copy needs its own restored backup as well as surviving replicas.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $9,400/mo | $850/mo | 91% | 0 min | 6 days | — |

## What you can turn off
Nothing this week. Retire each managed disk or share only after its workload, data and rollback copy have moved. Object migration in Move 15 does not retire block volumes or file shares; VM disks and shared files need their own acceptance checks before Move 20 removes the leftovers.
