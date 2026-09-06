# 11 · Headroom, and the number of machines you order

**Layer:** Iron · **Leaving:** Elastic node capacity: cluster autoscaling and node auto-provisioning · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Multiplies the node shape by the derated requirement, adds the losses per-hour pricing hid, and produces the machine count, rack-unit budget and total draw.

## Leaving from
- **AWS:** Cluster Autoscaler and Karpenter on EKS — capacity arrived in ninety seconds and left again, so nobody ever had to state a fleet size.
- **Google Cloud:** GKE cluster autoscaling and node auto-provisioning — the same elasticity, with node pools created for you when a pod would not fit.
- **Azure:** AKS cluster autoscaler and node auto-provisioning — the same again, and the same reason the fleet size was never a number anyone wrote down.

## Why this works
Autoscaling let you avoid this arithmetic by paying a premium per hour to never do it. Owning the hardware means doing it once, properly, and then living with the answer for three years. The requirement from Move 02 is not the fleet size, because a node does not give a pod all of its cores or all of its memory: the kubelet and the system take some, the storage and networking daemons take some, bin packing wastes some, and the largest single pod you run sets a floor on how much of a node must stay free. Add the capacity to lose a node — or a rack — without evicting production, and the honest number is meaningfully larger than the raw requirement.

## Before you start

**Access**
- The derated requirement from Move 02 and the non-production decision from Move 03
- The measured largest single pod in the estate, by both cores and memory

**Software**
- The node shape from Moves 04 through 07, with usable cores and usable memory calculated rather than assumed
- A bin-packing model, even a crude one, that can be shown to somebody who doubts the answer

**People**
- Whoever will carry the on-call rota, to agree how much failure the fleet should absorb without a human

## The runbook
1. Compute usable capacity per node: total cores and memory, less kubelet and system reserved, less the daemonsets that run everywhere — the storage agents, the network agent, the log shipper, the metrics agent. On a modern estate that overhead is several cores and several gigabytes per machine, and it is the same on the smallest node as on the largest, which is an argument for larger nodes.
2. Model bin-packing waste against the largest single pod rather than the average one. If your biggest workload needs twelve cores, every node has to be able to hold twelve free cores when it is scheduled, and that constraint costs more than the pod does.
3. Add failure headroom explicitly and say what it protects against, in the terms the on-call rota will experience it. Tolerating one node loss is the minimum. Tolerating the loss of a whole rack is a different number and it is the one that matters once Part II puts more than one rack in the plan.
4. Fix the control-plane count at three, or five for an estate that expects to grow past a few hundred nodes, and state which failure domain each one sits in. Three control-plane nodes in one rack is three machines and one failure domain.
5. Sum the result into three outputs: the machine count, the rack-unit budget from Move 07, and the total power draw at expected and peak load. These three numbers are the entire input to the Part II facility conversation.
6. Show the fleet size to the people who have been asking for this programme, and be honest about what it means. Capacity is now bought in whole servers with a lead time. Nothing scales to meet a launch on Thursday unless it was bought in advance, and that is the real trade this book is asking them to make.

## Operator's notes
- **Swap:** Where the workload genuinely spikes by an order of magnitude a few times a year, keep a small cloud account for the spike and size the metal for the base. Move 116 makes that a deliberate design rather than an admission of defeat.
- **Do it faster:** Model two fleets — many small nodes and few large ones — against the same workload. The overhead figures usually make the decision for you within an hour.
- **Watch out:** A fleet sized exactly to the requirement has no room for the rolling upgrade in Move 109, which needs somewhere to put the workloads from the node it is draining. Headroom is not optional; it is the upgrade path.
- **Leftovers:** The autoscaling configuration, the launch templates and the node auto-provisioning policies stay in the cloud accounts until Part VII closes them. Leave them alone until then; they are the way back.

## Rollback
Until the order is signed the machine count is a number in a model, and it is revised by revising the model. The point of no return is Move 20. Ordering too few is recoverable at the cost of a lead time and a second delivery; ordering too many is capital spent early and racked slowly. Neither is fatal, which is worth saying plainly to whoever is nervous. Keep the model and its inputs in source control so a previous version can be restored when somebody asks why the estate is this size.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. Autoscaling stays exactly as it is until Part VII, because it is what carries production while all of this is being built.
