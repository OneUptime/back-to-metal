# 06 · Memory is what runs out first

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Sizes memory from measured working set plus reserves, rounds up to a population that fills every channel, and orders it first because it is the longest lead.

## Leaving from
- **AWS:** EC2 memory-optimised families — memory came in fixed ratios to vCPU, so you bought cores you did not want to reach a capacity you did.
- **Google Cloud:** Compute Engine custom machine types — the one place you could set memory independently of cores, within a per-core band that still constrained the answer.
- **Azure:** Virtual Machines E-series and constrained-core sizes — memory was bought by series, and constrained cores existed mainly to make the licensing arithmetic survivable.

## Why this works
Nodes do not run out of CPU. They run out of memory, and when they do the kubelet starts evicting, which is a much worse failure than being slow. So memory is sized from the measured working set from Move 01, plus page cache, plus the kubelet and system reserved, plus the eviction threshold you intend to set — and then rounded up to a DIMM population that fills every memory channel, because a half-populated channel map throws away bandwidth out of all proportion to the capacity it saves. This is also the line with the longest lead time and the most volatile price in the whole bill of materials, which is why it is sized here and ordered first.

## Before you start

**Access**
- The thirty-day window from Move 01, with per-container working set separated from page cache
- A live quote for the exact module part number, dated, because last quarter's price is not a price

**Software**
- The vendor's memory population guide for the chosen socket, which is a real document and not a rule of thumb
- The bandwidth figures for one and two modules per channel on that part, at the speed you will actually run

**People**
- Whoever approves capital spend, warned that this line moves between quote and order

## The runbook
1. Take the measured working set per node class and add the reserves that are not optional: kubelet reserved, system reserved, the eviction threshold, and page cache sized against how much of your read traffic currently comes from it. Fifteen to twenty-five per cent above raw working set is a defensible starting point, and it should be written as a calculation rather than a factor.
2. Round the result up to a population that fills every channel. Current AMD EPYC on the SP5 socket has twelve channels per socket and accepts two modules per channel, so a full first fill is twelve modules and the second fill is twenty-four. The Intel Xeon 6 6900P parts also have twelve channels but are one module per channel, so twelve is both the first fill and the last.
3. Check the speed penalty before choosing the second fill. Two modules per channel runs slower than one on the same part, by a documented step, and that step is worth reading rather than guessing: on a memory-bandwidth-bound workload it can cost more than the capacity gains.
4. Decide now whether memory is ever added later, because on a one-module-per-channel part the answer is no and on a two-module part it means replacing modules rather than adding them. Either way it is a decision made at purchase, not deferred by it.
5. Get a live quote and treat it as expiring. Server memory prices and lead times have moved a long way outside their historical range as high-bandwidth allocation has consumed fabrication capacity, and the figure that matters is the one your supplier will honour this week.
6. Order this line first, ahead of everything else on the bill of materials. A rack of machines waiting for modules is the most common way this programme slips a quarter.

## Operator's notes
- **Swap:** Where capacity matters more than bandwidth — a large in-memory cache, a build farm — the second module per channel is worth its speed penalty. Measure the workload rather than applying a rule.
- **Do it faster:** Order one machine's worth of modules early and test them in a loan chassis. A population that the firmware will not train at the rated speed is much cheaper to discover on one machine than on twenty.
- **Watch out:** Registered and load-reduced modules are not interchangeable, ranks affect the achievable speed, and mixing part numbers within a channel map is how a machine ends up running a whole speed grade below its rating with nothing reporting it.
- **Leftovers:** Modules pulled from decommissioned machines are rarely worth carrying forward. Different rank, different speed, out of warranty, and the failure they cause is intermittent.

## Rollback
Until the order is signed this is a spreadsheet and reversing it costs an afternoon. After that it is the hardest line to change, because modules are consumed by the population map and a smaller order cannot be topped up without replacing what arrived. The point of no return is the purchase order in Move 20. Keep the sizing calculation, the quote and the population guide in source control so the reasoning can be restored when a machine arrives with a different part number on the label than the one you priced.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. This Move is where the largest single line on the bill of materials gets its number.
