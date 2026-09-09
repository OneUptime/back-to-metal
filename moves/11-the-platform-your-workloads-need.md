# 11 · The platform your workloads need

**Layer:** Build · **Leaving:** Managed VM and Kubernetes compute · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Cloud VMs become KVM guests on Proxmox VE. Containers keep Kubernetes. Owning the hardware does not require changing the application's packaging.

## Leaving from
- **AWS:** EC2 and EKS — instance-role credentials depend on metadata, while pod identity can depend on an IAM OIDC trust that your new cluster must replace.
- **Google Cloud:** Compute Engine and GKE — attached service-account credentials come from a metadata service; copying the boot disk does not bring that service with it.
- **Azure:** Virtual Machines and AKS — managed identities are Azure resources with role assignments; neither a guest image nor a pod manifest transfers that trust.

## Why this works
Bare metal is the hardware layer. For an estate with VMs, install Proxmox VE on the physical hosts and run those workloads in KVM guests. A guest keeps its operating system, service manager and deployment tooling; several guests share each host. Proxmox manages their lifecycle and placement. It does not recreate the cloud's metadata, identity or autoscaling services.

For an estate already running containers, Talos Linux directly on the hosts remains a useful choice. In a mixed estate, Talos can also run in Proxmox guests, with physical failure domains and storage ownership made explicit. The strip below retains the container reference's control-plane charge. Add VM platform support, guest licences and operating time to Move 03 before using that model for a VM estate.

## Before you start

**Access**
- The machines and VLANs from Move 10, with host roles assigned from Move 02's inventory
- An API virtual address for Kubernetes and management access restricted to the private VLAN

**Software**
- For VMs: the Proxmox VE 9.2-1 installer, its published checksum, and versioned guest OS templates with a matching QEMU guest agent
- For Kubernetes: Talos 1.14.0 and Kubernetes 1.35.8 pinned in Git; matching `talosctl` and `kubectl` clients
- `helm`, Cilium chart 1.20.1, the `cilium` CLI, and cert-manager chart v1.21.1
- An encrypted credential store outside the platform for Talos configuration and recovery keys

**People**
- A platform owner and someone to disconnect a host while the owner watches recovery

## The runbook
1. Write the host and guest plan in Git. Reserve CPU and RAM for the hypervisor, storage and a failed host as sized in Move 05. Enable hardware virtualisation in firmware for the VM pool. Keep the management and cluster-quorum networks away from guest traffic and storage saturation.
2. For that pool, verify the Proxmox VE 9.2-1 checksum and each empty boot pair's serial before the installer erases it. Apply security updates in the lab, record the tested package versions, then roll that set to the hosts. Create a Proxmox cluster and join the empty hosts; use at least three for quorum.
3. Create test KVM guests from the versioned OS templates on the local datastore reserved during host installation. Set CPU, RAM, boot mode, VirtIO disks and VLAN bridges; enable and test the QEMU guest agent. Pick a CPU model supported by every migration destination. Keep HA disabled: Move 12 moves ordinary guest disks to shared storage before production.
4. Where Kubernetes is needed, allocate three control-plane nodes on separate physical hosts, whether they are Talos guests or physical machines. For Talos guests, include the `siderolabs/qemu-guest-agent` extension in the pinned installer image. Distribute workers across hosts and reserve etcd memory and disk I/O. Guests on one host share its failure; keep capacity available for recovery.
5. Generate configuration with `talosctl gen config --kubernetes-version 1.35.8`. Keep generated files and their private keys in the encrypted store; commit only non-secret patches. Confirm each installation disk before Talos repartitions it. Set the API virtual address, disable the default CNI and kube-proxy, apply configuration, then run `talosctl bootstrap` on one control plane.
6. Install Cilium with `helm install` at chart version 1.20.1, using its documented Talos capabilities and cgroup settings. Set `ipam.mode=kubernetes`, `kubeProxyReplacement=true`, and the API to KubePrism at `localhost:7445`. Verify kube-proxy is absent with `kubectl`, then run the `cilium` connectivity test. Save the complete Helm values in Git.
7. Install cert-manager with `helm install` at chart version v1.21.1, enabling `crds.enabled=true`. With `kubectl`, wait for its controller, webhook and cainjector deployments to become available. Later database and edge Moves need these certificate services. A VM-only estate skips the Kubernetes steps.
8. Disconnect one physical host while only test workloads run. Kubernetes must retain API quorum and reschedule replaceable pods; local guest disks remain unavailable, so expect no VM failover yet. Move 12 repeats this with shared storage and HA affinity rules. A failed VM restarts; it does not live-migrate from a dead host.

## Operator's notes
- **Swap:** A container-only estate can skip Proxmox and boot Talos directly. Choose from the inventory, not from the name of the cloud service on the invoice.
- **Do it faster:** Build a guest template once and clone it. Keep its image digest and configuration alongside the application release.
- **Watch out:** Do not stack Rook OSDs on replicated virtual disks. Passing through physical storage restricts migration; Move 12 assigns each device one owner.
- **Leftovers:** Schedule host and guest patching separately, and rehearse upgrades on the spare. A VM snapshot is not an independent backup.

## Rollback
While only test guests and an empty cluster exist, restore the recorded configuration or rebuild from the saved images and encrypted keys. Returning to kube-proxy also requires a compatible Cilium configuration and another connectivity test; one flag cannot repair every network failure. The point of no return is the first production disk or application write: after that, rebuilding a host requires preserving its datastore and restoring affected workloads. Keep cloud production authoritative until the later Moves test migration and recovery.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $220/mo | $0/mo | 100% | 0 min | 4 days | — |

## What you can turn off
Nothing yet. Cloud instances and managed clusters still serve production. Their charges stop only after their workloads pass the later migration gates.
