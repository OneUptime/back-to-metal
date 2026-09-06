# 04 · Cores against clock, and the licence that decides it

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Picks socket count, generation and vendor against the derated requirement, then re-checks the answer against per-core licensing, which frequently inverts it.

## Leaving from
- **AWS:** Dedicated Hosts and licence-included instances — the licence was bundled into the hourly rate, or brought under a host you did not have to count cores on yourself.
- **Google Cloud:** Sole-tenant nodes — the same bundling, with node affinity labels doing the work that a physical machine boundary will do for you afterwards.
- **Azure:** Azure Hybrid Benefit and dedicated hosts — the one place where the licensing arithmetic was already visible to you, which makes this Move less of a surprise there.

## Why this works
Silicon is priced per core and software is priced per core, and the two curves point in opposite directions. A dense dual-socket part gives you the cheapest core you will ever buy and, under a per-core licence, the most expensive server you will ever run. Oracle counts every physical core in the host at the 0.5 x86 factor unless the partitioning is one it has approved as hard; SQL Server licenses every core on the server with a four-core minimum per processor; Windows Server carries an eight-core minimum per processor and sixteen per server. So the shape of the fleet is decided by what is licensed, not by what is fastest, and the licensed workloads want few fast cores on a machine of their own.

## Before you start

**Access**
- The derated core requirement from Move 02, and the non-production requirement from Move 03
- Your current licence entitlements, in writing, from whoever holds the contracts

**Software**
- Benchmark results for the candidate parts on something that resembles your workload, not a synthetic score
- A three-year power price for the site you expect to use, even if the site is not chosen yet

**People**
- Someone from procurement or legal who can get a licensing position confirmed in writing rather than assumed

## The runbook
1. Split the requirement into licensed and unlicensed workloads before choosing anything. These are two different fleets that happen to arrive on the same delivery.
2. For the unlicensed majority, pick the cheapest core that meets the clock floor your latency-sensitive services need. One socket is usually right for a Kubernetes node; two sockets earn their place only for memory capacity or PCIe lanes, not for core count.
3. For the licensed workloads, invert the question. Choose the smallest core count that clears the performance requirement and the highest clock available at that count, then check the per-server minimums, which frequently make a small machine cost the same as a medium one.
4. Price the generation behind the current one. It is worth buying when the discount exceeds the performance-per-watt gap over three years of electricity, and on a site where you now pay the power bill directly that calculation is different from the one the cloud made for you.
5. Get the licensing position in writing before the order goes anywhere. Ask the specific question — how many licences does this exact configuration require — and keep the answer. Verbal reassurance from a reseller is not a defence in an audit.
6. Publish the two fleet shapes with their cost per core and their cost per licensed core side by side. The second number is the one that changes minds.

## Operator's notes
- **Swap:** Where a licensed database is the only reason for an expensive shape, price migrating it off that engine instead. Sometimes the licence is the migration, and the hardware question disappears.
- **Do it faster:** Ask two vendors to quote the same requirement rather than the same configuration. They will each propose a different part and the gap between them is the information you wanted.
- **Watch out:** Core factors and minimums change between contract versions. The position that held for your last renewal may not hold for the estate you are about to build.
- **Leftovers:** Licences already bought against cloud instances may or may not carry to hardware you own. Establish that now, because it is worth more than the servers.

## Rollback
A choice of part is reversed by choosing a different one, at no cost, right up until Move 20 turns it into an order. The point of no return is that signature: after it, a licensing error is a bill rather than a revision. Keep the benchmark data, the vendor quotes and the written licensing position in source control, so the reasoning can be restored and re-argued when somebody asks in eighteen months why the estate is shaped like this.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 5 days | 2 weeks |

## What you can turn off
Nothing yet, but the licensing audit this Move forces has been known to find entitlements already paid for and never deployed.
