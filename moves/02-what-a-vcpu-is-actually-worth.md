# 02 · What a vCPU is actually worth

**Layer:** Iron · **Leaving:** The vCPU as a unit of purchase · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Converts a month of samples into a derated core requirement, and corrects the derate on the families where a vCPU is a whole core rather than a thread.

## Leaving from
- **AWS:** EC2 instance families — a vCPU is one SMT thread on the x86 families and one whole physical core on every Graviton generation, which is the correction most people miss.
- **Google Cloud:** Compute Engine machine families — a vCPU is a thread on the Intel and AMD families, and a full core on C4A, T2D, T2A, N4A and H3, all of which are sold in the same units.
- **Azure:** Virtual Machines series — a vCPU is a thread on the D, E and F series, and a physical core on the Cobalt 100 Dpsv6 and Epsv6 series, and the portal draws them identically.

## Why this works
A vCPU is a billing unit, not a quantity of computer. On most x86 families it is one hardware thread, so two of them share one physical core and a fleet of 400 vCPUs is 200 cores of silicon. On the Arm families it is a whole core, so 400 vCPUs is 400 cores. Applying the halving derate to an Arm fleet buys twice the hardware you need, and it is the single most expensive arithmetic error available in this Part. The other correction is statistical: a fleet peak is the sum of peaks that never happened at the same moment, so the requirement is built from per-workload p95 and p99 and the fleet number falls out of that, not the other way round.

## Before you start

**Access**
- The completed thirty-day window from Move 01, in one queryable place
- The instance inventory per account, with family and size, exported rather than screenshotted

**Software**
- A spreadsheet or notebook that other people can check, because this number will be argued with
- The provider documentation for each family you run, saved as PDF against the day you read it

**People**
- Whoever signs the purchase order, present for the derate conversation rather than shown the answer

## The runbook
1. Group every instance by family and mark each group as thread-per-vCPU or core-per-vCPU from the vendor documentation. Do this before any arithmetic; the whole result turns on it.
2. Pull out the burstable families — the t-series, Azure B-series, and e2-medium and smaller. Their utilisation is measured against a credit budget rather than against a core, so their samples say nothing about core requirement. Discard them and re-measure those workloads on a non-burstable shape for a week.
3. For every remaining workload, take p95 and p99 of CPU over the window, per workload rather than per fleet. Size against p99 for anything with a latency commitment and p95 for everything else, and record which you chose for each.
4. Convert to physical cores: halve for the thread-per-vCPU groups, take at face value for the core-per-vCPU groups. Sum by workload class, not by account.
5. Apply a generational factor against the parts you are actually going to buy, taken from a benchmark that resembles your workload rather than from a marketing figure. A current-generation core is not a 2019 core, and pretending it is over-buys as reliably as the derate error under-buys.
6. Write the requirement as a range with the assumptions attached, and have somebody who was not in the room reproduce it from the same data. If they cannot, the number is not ready to spend against.

## Operator's notes
- **Swap:** If you have no month of samples and cannot wait for one, size from the peak of the last quarter's billing and mark the whole result provisional. It will be high by a third and you will pay for that.
- **Do it faster:** Most estates have five workload shapes wearing forty names. Cluster them first and the arithmetic takes an afternoon instead of a week.
- **Watch out:** Rightsizing recommendations from the providers optimise for a smaller rented instance, which is a different question from how much silicon to own. They are a useful sanity check and a bad input.
- **Leftovers:** The exported inventory dates fast. Re-run the export the week the order goes in rather than reusing this one.

## Rollback
This Move produces a number, and a number is undone by writing a better one. Redo the derate, redo the percentile, publish the correction to everyone who saw the first version. The point of no return is Move 20, where the requirement becomes a signed order and the difference between right and wrong stops being a spreadsheet revision and becomes machines in a loading bay. Keep the raw samples and the working, and restore the earlier version from source control if a later revision turns out to be the mistake.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 5 days | — |

## What you can turn off
Nothing yet, though this is usually where somebody notices a family of oversized instances that can be shrunk this week, on the cloud, for free.
