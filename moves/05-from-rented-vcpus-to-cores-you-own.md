# 05 · From rented vCPUs to cores you own

**Layer:** Buy · **Leaving:** The vCPU as a unit of purchase · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> A cloud vCPU is a scheduling unit. Measure the workload before buying cores, then leave room for the guests and a failed host.

## Leaving from
- **AWS:** EC2 instance types — a vCPU is one SMT thread on many x86 families but a whole physical core on Graviton, labelled the same.
- **Google Cloud:** Compute Engine machine types — custom shapes have family-specific memory limits; supported families offer extended memory at a premium without adding vCPUs.
- **Azure:** Virtual Machine sizes — the B-series meters CPU against a credit balance, so a saturated workload reads low once its credits run out.

## Why this works
Move 01's samples become a part number here. On many x86 families two vCPUs share a physical core; that identifies the source topology, not the throughput of a replacement processor. Benchmark the workload on the proposed hardware. Existing VMs share a Proxmox VE host as KVM guests, each with its own operating system and resource allocation. You are buying a pool of capacity, not one physical machine per cloud instance. Memory, peak CPU demand and the capacity left after a host fails decide how many guests fit.

## Before you start

**Access**
- The two-week measurement window from Move 01, working set sampled apart from CPU
- The instance inventory from Move 02, exported with family and size

**Software**
- A sizing sheet other people can check, with the derate and headroom visible
- The vendor documentation for each instance family you run

**People**
- Whoever signs the order in Move 06, present for the derate rather than shown it

## The runbook
1. Group the instance inventory by family and record threads per physical core from the vendor documentation. Graviton and many Arm shapes expose one vCPU per core; some x86 families do too. Do not halve those counts as though they were SMT threads.
2. Review burstable families separately. Azure `B-series` and EC2 `t3` in standard mode fall to their baseline after credits run out — twenty per cent per vCPU on a `t3.medium`. T3 normally defaults to unlimited, but account settings and Dedicated Hosts differ. Check actual credit mode, throttling and charges, then re-measure unconstrained demand before sizing.
3. Enter the source topology in the sizing sheet, then benchmark a representative workload on the proposed CPU. Record peak demand and latency at that load; halving a vCPU count is not a performance test. Rebuild Arm applications for x86 before testing them on this reference hardware; an Arm disk image will not boot as an x86 KVM guest.
4. For VMs, budget guest RAM plus Proxmox VE, QEMU and storage reserves; do not sell the same RAM twice through ballooning. For containers, use working sets plus kubelet reserve, page cache and eviction thresholds. In both cases prove that the surviving hosts carry peak load after the largest host is unavailable, without counting an unplugged spare.
5. Benchmark per-core performance on the latency path as well as fleet throughput. PostgreSQL can parallelise some queries; others remain serial. Turn capacity, sustained write rate and recovery headroom into drives. Record guest vCPU allocations separately from physical cores, and hand the specification to whoever signs the order in Move 06.

## Operator's notes
- **Swap:** With the window unfinished, use provisioned capacity as a provisional ceiling. It does not measure demand; finish the workload tests before approving the order.
- **Do it faster:** Group workloads with similar resource profiles, then test representative examples and the outliers separately.
- **Watch out:** Rightsizing advice optimises for a smaller rented instance, a different question from how much silicon to own.
- **Leftovers:** Drive IOPS depend on block size, queue depth, read/write mix and steady-state behaviour. Test the intended storage stack; a drive's peak specification is not the application's guaranteed rate.

## Rollback
A specification is undone by writing a better one: change the derate and reissue it. Nothing has been bought. The point of no return is the signature in Move 06, after which a short memory line is a second purchase with a lead time. Keep the sheet in version control so a revision can be restored.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet, though the re-measurement in step two usually finds a service two sizes above its demand — shrink it and the bill falls this month.
