# 11 · A cluster, in an afternoon

**Layer:** Build · **Leaving:** The managed Kubernetes control plane · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> The frightening part is the short part: eighteen machines, one file in Git, and an operating system with no shell to log into.

## Leaving from
- **AWS:** EKS — tearing a cluster down leaves its IAM OIDC provider behind, still trusting an issuer URL nothing resolves.
- **Google Cloud:** GKE — the control plane upgrades on its release channel regardless; a full-freeze exclusion cannot exceed 90 days, and holding a minor version only lasts until that version leaves support.
- **Azure:** AKS — the Free tier carries no API server uptime guarantee at all, so what is given up is a paid Standard tier or nothing at all.

## Why this works
A control plane is three machines that agree with each other, and the agreement is etcd. Talos Linux removes the reason hand-built clusters rot: no shell, no package manager, no login, so changing a machine means changing the YAML in Git and applying it. Drift stops being a category. Doing this while nothing runs is what makes the risk survivable — every mistake costs a rebuild, and an empty cluster rebuilds in twenty minutes. Be plain about the money: a managed control plane is about $73 a month each and you run three — the same ten cents an hour at all the providers — so this is not the Move that pays for the migration.

Everybody arriving from EC2 asks why there is no hypervisor — why this sits on the metal rather than on Proxmox, with as many virtual machines as you like. Because you are not moving virtual machines: Move 02's inventory is already containers, and a hypervisor under a container platform is a second control plane to patch, licence and back up for a problem this estate does not have. It also puts back the shell that Talos removes, which is what the ongoing-hours figure assumes you did not do. The Swap says when to take the other branch.

## Before you start

**Access**
- The eighteen machines from Move 10, powered and reachable on the management VLAN
- One unused address on the server VLAN, for the API virtual IP

**Software**
- `talosctl` and `kubectl` at the same minor version as the cluster you are building
- `helm` and the Cilium chart pinned to an exact chart version, not a range
- The `cilium` CLI, for the connectivity test

**People**
- Someone to power a machine off at the wall while another watches the API

## The runbook
1. Commit the machine configuration before applying it. Generate the base with `talosctl gen config`, pin the Kubernetes version one minor behind the newest, point the API endpoint at the virtual address on the server VLAN, and give etcd a partition on its own NVMe device — every etcd commit is an fsync, and nothing doing bulk writes shares that device.
2. Apply it to the three control-plane machines and run `talosctl bootstrap` on one. The installer wipes and repartitions the target disk, so confirm each machine's serial against the rack map first.
3. Join the rest. Thirteen become workers; the two spares take the same configuration and stay cordoned, so replacing a dead node is an uncordon rather than a build. At this size the control-plane nodes can stop taking workload — sixteen machines can spare three that only run etcd, and three that do nothing else are three that never get evicted at the wrong moment.
4. Install Cilium with `helm install` at the pinned chart version, kube-proxy replacement on, and the API host set to the virtual address, never a name: a name needs DNS, and DNS needs the network this step builds. Disable kube-proxy in the machine configuration in the same commit.
5. Verify with `kubectl` that no kube-proxy service chains survive on any node, then run the `cilium` connectivity test and read all of its output.
6. The acceptance test: pull the power on one machine at random, watch the API stay reachable and the pods reschedule, then power it back on and confirm it rejoins untouched. Do it while the cluster is empty; that is the last time it is cheap.

## Operator's notes
- **Swap:** If replacing kube-proxy on day one is a step too far, run Cilium alongside it and take kube-proxy out a week later.
- **Swap:** Proxmox underneath, cluster in virtual machines, is right in three cases: workloads that are not containers and never will be; rebuilding or resizing a node without walking to the rack; or snapshotting a whole machine before an upgrade rather than only its workloads. The price is a second platform to patch. Take it deliberately, not by habit.
- **Do it faster:** Build the cluster twice from the same commit. The second build takes twenty minutes and shows whether the first was reproducible or lucky.
- **Watch out:** On flash without power-loss protection, etcd throws leader elections under write load, which reads as an intermittent network fault.
- **Leftovers:** Write the upgrade cadence down today — one minor behind, reviewed quarterly. Nobody picks it calmly once a version is out of support.

## Rollback
While the cluster is empty nothing here is hard to undo. Reverting the kube-proxy flag in the machine configuration and reapplying it takes a minute: an enormous blast radius, and a way back that is one flag. The point of no return is Move 12, where the first volume binds to a machine. Keep every configuration version in Git so a known-good one can be restored exactly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $220/mo | $0/mo | 100% | 0 min | 4 days | — |

## What you can turn off
Nothing yet — the managed cluster still carries production and stays until Move 20. Its per-hour control-plane charge is the first bill line to reach zero.
