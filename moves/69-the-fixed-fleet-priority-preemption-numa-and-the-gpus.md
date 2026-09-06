# 69 · The fixed fleet: priority, preemption, NUMA and the GPUs

**Layer:** Platform · **Leaving:** Node autoscaling groups, cluster autoscalers, just-in-time node provisioners, managed node pools and serverless pod runtimes · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Node count is fixed, so scheduling becomes the scarce resource: accurate requests, tiered priority classes and deliberately wasted headroom replace the autoscaler.

## Leaving from
- **AWS:** Karpenter and managed node groups — a just-in-time provisioner meant this estate never had to express a node class at all, which makes it the most work here.
- **Google Cloud:** node auto-provisioning and Autopilot — the same absence of node classes, with the platform choosing shapes on your behalf.
- **Azure:** cluster autoscaler with node pools and node auto-provisioning — closer to explicit node classes, so this reader starts from a shorter list.

## Why this works
When a scheduler could conjure a machine, inaccurate resource requests were a rounding error. On a fixed fleet they are the whole game, because a request that is twice the real usage wastes half a machine and a request that is half the real usage produces evictions under load. So requests get measured against actual usage; priority classes decide what yields to what when the fleet is full; low-priority placeholder workloads reserve headroom deliberately, so that it exists rather than being consumed by whatever asked last; and a documented overcommit position per machine class replaces the autoscaler's willingness to spend.

## Before you start

**Access**
- Real usage data per workload from Move 62, at percentiles rather than averages
- The SMT and topology decisions from Move 05, which this Move inherits rather than revisits

**Software**
- Priority classes defined as a tier list rather than as ad-hoc numbers
- The device plugin and driver for any accelerators, delivered as a system extension in the image rather than built on the host

**People**
- The owner of every batch workload, because batch is what will be preempted and they need to know

## The runbook
1. Correct the requests first, against measured usage rather than against what the manifest has always said. This single step recovers more capacity than everything else in this Move combined.
2. Define priority classes as a small tier list: serving above batch, batch above best-effort, and a placeholder tier below everything. Three or four tiers, not fifteen.
3. Deploy low-priority placeholder workloads to reserve headroom. This is deliberately wasted capacity that exists so that a serving workload can always be scheduled, and it is the fixed-fleet replacement for an autoscaler's spare machine.
4. Write down the overcommit position per machine class. How much more may be requested than exists, and why. An undocumented overcommit ratio is a decision somebody made once and nobody can defend.
5. Set the topology and processor policies from Move 05 and confirm a guaranteed workload actually receives whole physical cores rather than two halves of one.
6. Install the accelerator driver and device plugin as a system extension baked into the machine image. This is the one place in the Part where the immutable host changes the procedure rather than only the tooling, and it means a driver change is an image change and a reboot.
7. Run the descheduler to correct drift, and watch what it moves for a week before letting it act automatically.

## Operator's notes
- **Swap:** Where an estate genuinely cannot fit, the answer is Move 116 and more capacity, not a cleverer scheduler. Say that out loud rather than tuning for a month.
- **Do it faster:** Fix the ten largest workloads' requests and stop. The distribution is always long-tailed and the top ten are most of the waste.
- **Watch out:** Preemption is invisible to the workload being preempted, which experiences it as a restart. Batch owners need to know their jobs must be resumable, and this Move is when they find out.
- **Leftovers:** The node groups, autoscalers and provisioner configurations stay in the cloud until Part VII, because they are the burst capacity Move 116 may deliberately keep.

## Rollback
Every change here is a scheduler setting and is reverted by reverting it, with the workloads rescheduling within minutes. There is no point of no return. The risk is operational rather than permanent: a priority tier applied wrongly can preempt something important, which is why the tiers are few and why the descheduler is watched before it is trusted. Keep the priority classes and requests in source control so a working scheduling configuration can be restored quickly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 weeks | — |

## What you can turn off
Nothing yet. The autoscaling configuration stays in the cloud, deliberately, because Move 116 may keep it as tested overflow.
