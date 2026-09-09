# VM migration guidance

Reviewed 2026-09-09 for the VM migration correction. The Move files are the published
runbook; these notes retain the sources and boundaries behind the recommendation.

## Platform choice

An EC2, Compute Engine or Azure VM is not evidence that its application already runs
in containers. Move 02 classifies the workload before Move 11 assigns the platform.
Existing VM applications can keep their operating system and deployment recipe in
KVM guests on Proxmox VE. Talos on physical hosts remains appropriate for an estate
that already runs Kubernetes; mixed estates can also use Talos guests.

- [Proxmox VE platform overview](https://www.proxmox.com/en/products/proxmox-virtual-environment/overview)
- [Proxmox VE 9.2-1 installer and checksum](https://www.proxmox.com/en/downloads/proxmox-virtual-environment/iso/proxmox-ve-9-2-iso-installer)
- [Proxmox VM configuration, CPU models, VirtIO and migration](https://github.com/proxmox/pve-docs/blob/master/qm.adoc)
- [Talos on Proxmox and the QEMU guest-agent extension](https://docs.siderolabs.com/talos/v1.12/platform-specific-installations/virtualized-platforms/proxmox)

The installer is a reproducible starting point. The runbook also requires rehearsed
security updates and a recorded package set. It does not recommend freezing an
installation at the ISO's original patch level.

## Storage and physical failure domains

Temporary local storage breaks the bootstrap dependency: Move 11 can start test
guests before Move 12 creates shared storage. Only after all required guest disks
and networks are available on eligible hosts are ordinary guests registered for HA.
Control-plane guests need physical-host separation; separate guest names do not
create independent failure domains. A host failure causes a restart, not a live
migration from the failed host.

Proxmox owns the VM datastore on its path; Rook owns physical disks on the direct
Talos path. Kubernetes can consume an external Ceph cluster. The runbook avoids
another Ceph replication layer inside VMs whose disks already sit on host Ceph.
Local or passthrough storage has a different recovery path and is excluded from the
ordinary shared-storage HA procedure.

- [Proxmox HA resources and affinity rules](https://github.com/proxmox/pve-docs/blob/master/ha-manager.adoc)
- [Proxmox Ceph administration](https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc)
- [Rook external-cluster integration](https://rook.io/docs/rook/latest/CRDs/Cluster/external-cluster/provider-export/)
- [Rook object-store resources](https://rook.io/docs/rook/latest/CRDs/Object-Storage/ceph-object-store-crd/)

## Application migration and recovery

The default VM path is a fresh guest plus the application's existing deployment
tooling. Disk import is conditional on image support, licence portability, boot
mode, drivers and an application-consistent copy of every required disk. Cloud
metadata identities and attached services do not travel with a disk image.

- [AWS VM image export restrictions](https://docs.aws.amazon.com/vm-import/latest/userguide/limits-image-export.html)
- [Google Cloud custom image export](https://docs.cloud.google.com/compute/docs/images/export-image)
- [Azure virtual disk download and snapshot consistency](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/download-vhd)

Move 14's zero-downtime reference covers a parallel stateless service with data
still authoritative in the cloud. Stateful VM migrations in Move 18 have separately
measured write-stop windows. After unique writes reach the destination, returning
requires transferring or restoring those writes; a stale source image is not a
writable fallback. Whole-VM restoration is rehearsed independently of Kubernetes
object and database recovery.

- [Proxmox backup and restore](https://github.com/proxmox/pve-docs/blob/master/vzdump.adoc)

VM-only estates also need an edge independent of Kubernetes. Move 17 uses proxy
guests on separate hosts, health-checked address failover and certificate renewal
verified on both replicas.

- [Keepalived configuration](https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html)
- [HAProxy routing configuration](https://docs.haproxy.org/3.2/configuration.html)
- [ACME certificate renewal](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates)

## Cost and verification limits

The existing figures remain the container reference build. Move 03 and the shared
cost-page text require pricing the actual VM mix, guest licences, support, backup
capacity and recurring operations. No universal consolidation ratio or VM saving
is inferred from the hardware specification.

This correction was checked against the cited documentation and the book's
structure, content, rendering and release gates. It was not a physical migration
test. The Move acceptance drills remain required on the reader's chosen hardware,
guest operating systems, storage and applications.
