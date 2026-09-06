# 70 · The workloads that must stay virtual machines

**Layer:** Platform · **Leaving:** Rented virtual machines outside the cluster, managed hypervisor estates and the appliance images sold through cloud marketplaces · **Risk:** Medium · **Cutover:** 30 min · **Reversible:** 14 days

> Some workloads never containerised, so KubeVirt runs them as virtual machines on the same nodes, drawing storage, addresses, identity and backups from the cluster.

## Leaving from
- **AWS:** EC2 instances and Marketplace appliance images — exported as raw or VMDK, which is the friendliest of the three formats to import.
- **Google Cloud:** Compute Engine instances and Marketplace images — exported as a disk image through a bucket, which adds a copy step but is otherwise straightforward.
- **Azure:** Virtual Machines and Marketplace images — exported as a VHD that must be fixed-size and correctly aligned, or the import fails after the copy has finished.

## Why this works
Some things never containerised and never will: a licensed database engine whose vendor supports one deployment shape, a Windows workload, an appliance sold only as a disk image. Running a hypervisor tier inside the cluster is how those workloads get the same storage, the same addresses, the same identity, the same policy and the same backups as everything else, instead of becoming a second estate with its own everything. The virtual machines run on the same nodes, their disks live on the storage from Move 49, and their identity and policy are inherited from Moves 55 and 60 rather than reinvented.

## Before you start

**Access**
- The list of workloads that genuinely cannot containerise, with a reason next to each one
- Export permissions in the source cloud, and somewhere to stage the disk images

**Software**
- KubeVirt at a pinned version, with the virtualisation and guest-agent system extensions in the machine image
- Storage classes that support the access mode live migration needs, which is not the default one

**People**
- The owner of each appliance, because a vendor support position may forbid this and it is better to know first

## The runbook
1. Justify each entry on the list. A workload goes here because it cannot containerise, not because containerising it is work nobody has scheduled. The list should be short and each line should have a reason.
2. Add the virtualisation and guest-agent extensions to the machine image and roll the nodes. On an immutable host this is an image change and a reboot, not an installation.
3. Install KubeVirt at a pinned version and run one throwaway virtual machine end to end before touching anything real.
4. Set the storage up properly. Disks live on the block storage from Move 49, and live migration requires a shared access mode that the default class does not provide — so that is a deliberate storage class rather than an oversight discovered during the first migration.
5. Export, convert and import each disk. One provider needs the image to be a fixed-size, correctly aligned disk, and the failure appears only after the copy has finished, so validate the format before transferring gigabytes.
6. Give each virtual machine an address from the plan in Move 39, an identity from Move 55 and a policy from Move 60. The hypervisor tier is not an exception to the platform; that is the whole point of putting it here.
7. Cut over one machine at a time: stop it, copy the final delta, start it here. Thirty minutes is the honest figure per machine, and the source stays in place for a fortnight.

## Operator's notes
- **Swap:** Where a vendor will not support their appliance on your hypervisor, keep renting it. That is a legitimate outcome and it belongs on the list in Move 116 of things you deliberately keep.
- **Do it faster:** Convert the disk images in advance and keep them current with a periodic delta copy, so the cutover is a short final synchronisation rather than a full transfer.
- **Watch out:** Live migration is not free and not always possible. A virtual machine with a local disk or an attached device does not migrate, which means node maintenance in Move 109 has to plan around it.
- **Leftovers:** The source instances, their disks and their snapshots stay for fourteen days, and the marketplace subscriptions behind the appliances are cancelled in Move 122 rather than here.

## Rollback
The source instance is stopped rather than deleted, so for fourteen days reverting is starting it again and moving the address back. The point of no return is the deletion of the source disk, which is deliberately deferred. Because the cutover involves a stop and a copy, any data written on the new side after the switch has to be restored to the source if you go back — so the fortnight is a window for deciding, not for running both.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,870/mo | $0/mo | 100% | 30 min | 3 weeks | 14 days |

## What you can turn off
The source instances and their disks after fourteen days, and their snapshots when Move 38 removes them against a signed approval.
