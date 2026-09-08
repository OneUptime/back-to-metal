# 05 · From rented vCPUs to cores you own

**Layer:** Buy · **Leaving:** The vCPU as a unit of purchase · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Two vCPUs is one physical core, and the second thread is worth about a quarter of the first — the gap between three machines and six.

## Leaving from
- **AWS:** EC2 instance types — a vCPU is one SMT thread on the x86 families but a whole physical core on Graviton, labelled the same.
- **Google Cloud:** Compute Engine machine types — custom shapes set memory apart from cores, within a per-core band that drags cores onto the bill.
- **Azure:** Virtual Machine sizes — the B-series meters CPU against a credit balance, so a saturated workload reads low once its credits run out.

## Why this works
Move 01's samples become a part number here. The first conversion is the one nobody writes down: on x86 a vCPU is one hyperthread, so two share a physical core, and the second thread is worth fifteen to thirty per cent of the first, not another hundred. A 96-vCPU estate is a 48-core estate, which fits in two of these machines. Then three rules in order: memory, the ceiling a node reaches; clock, because a query plan runs mostly on one core; flash, because local NVMe beats rented block storage by orders of magnitude.

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
1. Group the instance inventory by family and mark each thread-per-vCPU or core-per-vCPU against the vendor documentation. On Graviton and the other Arm shapes a vCPU is already a whole core, and halving buys double.
2. Pull the burstable families out of the measurement window. `B-series` and `t3` in standard mode meter against a credit balance, and once the balance is empty a saturated workload pins at its baseline — twenty per cent on a `t3.medium`. `t3` defaults to unlimited mode, where the number is honest and the burst above baseline arrives on the invoice instead. Re-measure either way before the figure reaches the sizing sheet.
3. Halve the thread groups and credit the second thread with the fraction it is worth. Record which peak you sized against: you paid for peak every hour of the month, and owned iron carries peak by definition.
4. Size memory from the working set plus kubelet reserve, page cache and the eviction threshold, then round up to a population that fills every channel. A node cannot be widened while it runs.
5. Take clock over count on the latency path — most of a Postgres query plan executes on one core — then turn capacity and write rate into drives and hand the specification to whoever signs the order in Move 06.

## Operator's notes
- **Swap:** With the window unfinished, size against last quarter's billed peak and mark the sheet provisional. It lands a third high.
- **Do it faster:** Most estates run five workload shapes wearing forty names. Cluster them and the conversion takes an afternoon.
- **Watch out:** Rightsizing advice optimises for a smaller rented instance, a different question from how much silicon to own.
- **Leftovers:** Local NVMe delivers the provisioned IOPS line as a property of the drive. Check it against your measured write rate.

## Rollback
A specification is undone by writing a better one: change the derate and reissue it. Nothing has been bought. The point of no return is the signature in Move 06, after which a short memory line is a second purchase with a lead time. Keep the sheet in version control so a revision can be restored.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet, though the re-measurement in step two usually finds a service two sizes above its demand — shrink it and the bill falls this month.
