# 05 · SMT, NUMA, and the workload that notices

**Layer:** Iron · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately, by reboot

> Settles SMT and the NUMA layout before latency-sensitive work arrives, and sets the kubelet policies without which two containers can share one physical core.

## Leaving from
- **AWS:** EC2 CPU options — you could disable threads per core at launch, and the underlying topology was otherwise hidden behind the instance shape.
- **Google Cloud:** Compute Engine visible NUMA and threads-per-core settings — exposed on some families, absent on others, and never something you had to reason about per host.
- **Azure:** Virtual Machines constrained core sizes — the licensing-driven answer to the same question, which set core count without giving you the topology underneath.

## Why this works
An instance shape hid two decisions from you. The first is simultaneous multithreading: with it on you get more throughput and less predictable latency, because two threads contend for one core's L1 and L2. The second is the NUMA layout, which on a chiplet EPYC matters more than the socket count, since the NUMA-per-socket setting and the last-level-cache boundary decide whether a memory access crosses a link. Kubernetes honours none of this by default. Without the CPU manager on its static policy and the topology manager set to single-numa-node, the scheduler will happily place two containers on the two halves of one physical core and both will run slowly for reasons nothing reports.

## Before you start

**Access**
- Firmware settings on a loan or evaluation machine of the part chosen in Move 04
- A latency-sensitive workload you can run in a loop and measure honestly

**Software**
- A load generator that reports percentiles rather than averages
- `ipmitool` or the vendor equivalent, so firmware settings can be changed without a trip to the rack

**People**
- The owner of the most latency-sensitive service, to agree what regression would be unacceptable

## The runbook
1. Measure the workload with SMT on and again with it off, at the same offered load, and compare p99 rather than throughput. Most services prefer it on; a small, loud minority does not, and the minority is usually the one with a latency commitment.
2. Set the NUMA-per-socket option in firmware with `ipmitool` or the vendor tool, choosing the value that matches how you intend to schedule, and record the resulting node topology. On the current EPYC parts the useful settings are one node per socket for general work and a per-quadrant split for workloads that fit inside a cache boundary.
3. Configure the kubelet with the CPU manager static policy, the full-pcpus-only option, and the topology manager on single-numa-node. Without the second of those, a guaranteed pod can still be handed the two threads of one core.
4. Reserve cores explicitly for the system and the kubelet rather than leaving them to compete. Two cores per socket is a reasonable starting point and it should be measured, not inherited.
5. Re-run the load test with the policies in place and confirm the improvement is real. If it is not, keep the simpler configuration; these settings cost scheduling flexibility and should be paid for with evidence.
6. Write down the symptom of each wrong setting — the throughput cliff above a load threshold, the p99 that only degrades when a neighbouring container is busy — because these faults arrive looking like an application regression and are debugged for weeks by the wrong team.

## Operator's notes
- **Swap:** If nothing in the estate has a hard latency commitment, leave SMT on, leave the topology manager at its default, and revisit when something does. Complexity you cannot measure is complexity you will misconfigure.
- **Do it faster:** Decide once, per machine class, and put the answer in the machine configuration rather than in a runbook. A setting that has to be applied by hand will be wrong on the fourth machine.
- **Watch out:** Changing the CPU manager policy on a running node requires removing its state file and restarting the kubelet; the policy alone does not take effect and the failure is silent.
- **Leftovers:** Halving your logical core count by turning SMT off changes the derated requirement from Move 02. If you choose off, go back and redo that arithmetic before Move 11 counts machines.

## Rollback
Every setting in this Move is reversed by a firmware change and a reboot, or by a kubelet configuration change and a node drain. There is no point of no return here at all, which is precisely why it belongs before the purchase order rather than after it: the same experiment costs an afternoon now and a maintenance window later. Keep the firmware profiles exported to a file so a known good configuration can be restored on a machine that has been fiddled with.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing. This Move changes what the hardware you have not yet bought will be asked to do.
