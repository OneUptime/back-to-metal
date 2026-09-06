# 41 · Talos as the host OS, and where it cannot go

**Layer:** Cluster · **Leaving:** Managed node images and their patch and time-sync agents · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Commits to Talos as the host OS, names the two cases it cannot take, and sets the time-sync, conntrack, hugepage and interrupt defaults the managed image provided.

## Leaving from
- **AWS:** Bottlerocket, patched by Systems Manager — an image somebody else built, patched on a schedule you did not set.
- **Google Cloud:** Container-Optimized OS with automatic node upgrades — already immutable and shell-restricted, which makes this the shortest agent audit of the three.
- **Azure:** the AKS Ubuntu or Azure Linux node image — usually a general-purpose distribution carrying a full agent estate, which makes this the longest.

## Why this works
Talos Linux is an operating system with no shell, no package manager and no remote login. It is configured entirely by a machine configuration file applied over an API, and the absence of a shell is the feature: there is nothing to log into, nothing to drift, and nothing to patch by hand. The cost is that a handful of things genuinely cannot run on it — an agent that needs a shell or a host package, and any driver that is not in the kernel or an official extension — and those exceptions are written into the design here rather than discovered during a migration. The machine configuration also carries the host tuning the managed image used to supply.

## Before you start

**Access**
- The Talos version you intend to run, pinned, with its release notes read
- An inventory of every agent currently running on your managed nodes, and what each one is for

**Software**
- `talosctl` at the same minor version as the cluster you will build
- The machine configuration held in source control from the first line, because it is the whole operating system

**People**
- Whoever owns each agent on the inventory, to say what happens if it stops existing

## The runbook
1. Audit the agents. Go down the list from your managed nodes and sort each into one of three piles: replaced by something in the cluster, genuinely unnecessary, or requires a host shell. Only the third pile is a problem.
2. Deal with the third pile explicitly. Anything requiring a shell or a host package runs on the hypervisor tier built in Move 70, or on a small labelled pool running a conventional distribution. Write the exception into the design with its owner and its review date.
3. Check every driver you need against the Talos kernel, using the answer already obtained in Move 14. There is no out-of-tree module path, so a driver is in the kernel, in an official extension, or the hardware does not go in this cluster.
4. Write the machine configuration with the host tuning the managed image used to provide: time synchronisation with real servers, connection-tracking table sizing, neighbour table sizing, file-watch limits, transparent hugepages, processor idle states and interrupt affinity.
5. Record the symptom of each setting being wrong, next to the setting. A small connection-tracking table presents as random connection failures under load; undersized file watches present as a controller that silently stops reconciling. These are debugged for weeks by people who do not know the setting exists.
6. Build one machine from the configuration, then rebuild it twice from nothing, first confirming no volume is bound to it, and check that the same configuration produces the same machine every time. That reproducibility is the entire argument for this operating system.

## Operator's notes
- **Swap:** Where a conventional distribution is required by policy, the rest of this book still works, and the cost is that node configuration becomes something you maintain rather than something you declare.
- **Do it faster:** Start from the upstream example configuration and change only what you can justify. Most estates need a dozen changes, not a hundred.
- **Watch out:** Time synchronisation is the setting people skip, and clock drift breaks certificate validation, distributed consensus and log correlation all at once, in ways that look like three unrelated faults.
- **Leftovers:** Patch management, image build pipelines and the agents that fed them can be retired once the fleet is on Talos, but not before Part VII closes the old estate.

## Rollback
A machine configuration is reverted and reapplied, and a node is rebuilt from nothing in minutes, which is what makes this Move low-risk in practice. The point of no return is not in this Move at all; it is Move 47, where a volume binds to a specific machine. Keep every machine configuration version in source control so a previous one can be restored exactly, and keep the agent audit with it so the exceptions can be reviewed rather than rediscovered.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The managed node images keep running production until Part IV moves the workloads.
