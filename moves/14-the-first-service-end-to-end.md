# 14 · The first service, end to end

**Layer:** Move · **Leaving:** Cloud VM and container compute · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The first service runs in a VM or a container on your hardware, with its data still in the cloud and a traffic weight as the way back.

## Leaving from
- **AWS:** EC2 and ECS on Fargate — VM Import/Export excludes Marketplace images and images with encrypted EBS snapshots; its Windows and SQL Server image restrictions also block many exports.
- **Google Cloud:** Compute Engine and Cloud Run — custom images export through Cloud Storage, but Google-provided Windows Server licences do not permit running those images outside Google Cloud.
- **Azure:** Virtual Machines and Container Apps — direct VHD download cannot use a disk attached to a running VM; a snapshot can be exported instead, but live snapshots are only crash-consistent.

## Why this works
The first service produces evidence before it produces savings. Its database remains in the cloud, so the new variables are the host platform, network path and identity. For a VM workload, create a fresh KVM guest on Proxmox VE and deploy the same application using its existing tooling. No container conversion is required. For a container workload, deploy the existing image to Kubernetes. Both routes can run beside the cloud copy and accept the same traffic ramp.

This Move covers stateless services, including those installed inside VMs. A writable application disk makes a VM stateful even when nobody calls it a database. Keep that data authoritative in the cloud, or defer that VM until its owner has rehearsed the data transfer, write stop and return path for Move 18. The zero-minute strip is for parallel stateless deployment, not a promise about exporting a running machine.

## Before you start

**Access**
- Proxmox management access and the VM configuration repository, or write access to the Argo CD application repository
- Permission to edit weighted DNS records and the required cloud credentials

**Software**
- For VMs: the versioned OS template and existing application deployment tooling; `qm` for an optional disk import
- For containers: `kubectl` and `argocd`, pointed at the new cluster
- `dig` for checking public DNS during the ramp

**People**
- The service owner, with test requests, an abort threshold and any guest licence approval
- Whoever maintains partner egress allowlists, warned in advance

## The runbook
1. Choose a low-impact stateless service from Move 02. Identify every disk write, scheduled job and metadata dependency. Disable duplicate jobs in the test copy, and keep it isolated from production traffic until the owner confirms it cannot create a second writer.
2. For a VM, create a KVM guest from the OS template and deploy the pinned application release with its existing tooling. For containers, commit the manifests and let `argocd` sync them. Keep the cloud database endpoint. Replace metadata credentials with an explicit workload identity or scoped credential, and update partner allowlists.
3. If rebuilding a guest is impractical, check the provider's export restrictions and licence portability first. Take an application-consistent copy of every required disk, export through the provider console, then use `qm disk import` to import a supported image. Attach the disks, match BIOS or UEFI and set boot order. Rehearse this off the live path; an export needing a source shutdown gets a separate downtime window.
4. Boot the VM on an isolated VLAN and verify VirtIO drivers, networking, DNS, clock and service startup; an imported disk is not evidence of a working application. For either route, send synthetic requests, check cloud API access without metadata, and compare error rates and latency percentiles with the cloud copy.
5. Ramp the weighted record: one per cent, ten, fifty, all of it. Hold each step a business day, check resolver answers with `dig` and measure the actual request split in service logs. Stop on the owner's error or latency threshold. DNS weight is approximate and cached clients will lag behind it.
6. Soak a week at full weight. Watch guest disks through Proxmox and application metrics, or node and pod health with `kubectl`. Exercise a service restart and check that configuration survives; scratch files must not become untracked application state.
7. Repeat across the stateless inventory, batched by owner. The reference fleet budgets twenty days of work across an eight-week cadence. Measure VM rebuild and export effort separately; do not squeeze stateful disk transfers into that allowance. Retain each cloud copy until its own soak and return-path checks pass.

## Operator's notes
- **Swap:** A proxy you already control can shift request weight faster than DNS. Keep the same acceptance and abort thresholds.
- **Do it faster:** Reuse the verified guest template and deployment recipe for the next VM with the same operating system.
- **Watch out:** Image export preserves bytes, not cloud identity, instance-store data or attached services. Verify every dependency from the inventory.
- **Leftovers:** Exported images, temporary buckets, snapshots, SAS links and both allowlist entries need dated cleanup after verification.

## Rollback
Set the new copy's traffic weight to zero, wait for cached clients to drain, and confirm requests return to the cloud. Keep that copy healthy through the soak. There is no point of no return for this stateless path because its authoritative data never moved. If the new guest has accepted unique persistent writes, stop: returning requires reverse transfer or a restore that preserves those writes before traffic changes. A stale cloud disk or pre-cutover snapshot cannot supply them. That VM needed the separate stateful migration plan.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $30,980/mo | $0/mo | 100% | 0 min | 20 days | 8 weeks |

## What you can turn off
Each old VM or container deployment after its own completed soak and return-path check. Shared instance groups, clusters and log retention stay until their last dependent service has passed; retain the snapshots required by the rollback plan.
