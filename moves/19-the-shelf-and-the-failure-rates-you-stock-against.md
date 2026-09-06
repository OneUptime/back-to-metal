# 19 · The shelf, and the failure rates you stock against

**Layer:** Iron · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Sets on-site spares from population and published failure rates, stocks a whole cold spare node, and counts the consumables nobody budgets for.

## Leaving from
- **AWS:** EC2 capacity pools — a failed host meant a new instance, and the spare parts inventory was a problem you never had.
- **Google Cloud:** Compute Engine host maintenance — the same, with the fleet's spare capacity standing in for your shelf.
- **Azure:** Virtual Machines fault domains — again capacity as the spare, which is why nobody arriving from a cloud has a parts cupboard.

## Why this works
Spares are the difference between a fault that costs an hour and a fault that costs a week, and the right number of them is arithmetic rather than instinct. Take the population, take the published annualised failure rate for each component class, and stock what a year is likely to consume plus a margin for the fact that failures cluster. The largest public storage fleet dataset has reported annualised drive failure in the region of one to one and a half per cent for several years running — a figure worth quoting and worth discounting, because it is a disk fleet rather than a flash one. Fans and power supplies are the commodity failures. Memory modules are the ones that hide for weeks as a correctable-error trend before anyone notices.

## Before you start

**Access**
- The final population from Move 11: machines, drives, modules, supplies, fans, optics
- The support contract from Move 17, and specifically its promised turnaround

**Software**
- A parts list keyed by the exact part numbers on the bill of materials, not by description
- Somewhere to record what was consumed, so next year's number is measured rather than repeated

**People**
- Whoever can physically reach the site, since a spare nobody can fit is inventory rather than a spare

## The runbook
1. Compute the expected annual consumption per component class from the population and the published failure rates, then round up. For a small estate the rounding dominates the arithmetic, and that is fine: the point is to have a defensible number rather than a precise one.
2. Stock a whole cold spare machine. It beats any return-and-repair cycle on time to service, and it is the only spare that covers a fault you have not yet diagnosed. For a fleet of a dozen it is the single best value line in this Move.
3. Stock the commodity failures on site: supplies, fans, a small number of drives of each size in use, and modules of the exact part number. Modules in particular must match, because a replacement of a different rank or speed changes how the whole channel map runs.
4. Count the consumables nobody budgets: rails, cage nuts, patch leads, optics of every type from Move 15, labels and a printer, and a bay map that says which drive is in which slot. These cost very little and their absence stops an installation day.
5. Record the promised turnaround from the support contract next to the turnaround the vendor actually achieves. They are different numbers and only the second one belongs in the runbook that Move 110 will write.
6. Put the spares on the bill of materials rather than buying them later out of a different budget. Later means the first failure arrives before the shelf does.

## Operator's notes
- **Swap:** Where a facility offers a bonded parts locker or a vendor holds local stock, that can substitute for some of the shelf. Confirm the access process at three in the morning before relying on it.
- **Do it faster:** Buy spares as part of the main order. They are cheaper, they arrive together, and the part numbers are guaranteed to match what was delivered.
- **Watch out:** Firmware drift between a spare and the fleet is the quiet failure here. A drive or supply that has sat on a shelf for a year needs updating before it goes in, and Move 110 needs to say so.
- **Leftovers:** Spares for a generation you no longer run are money on a shelf. Review the cupboard when the fleet changes, not five years later.

## Rollback
Spares are inventory, and inventory is reversed by not buying more of it. There is no commitment here beyond the cash. The point of no return is the moment the fleet's part numbers change and the shelf no longer matches, which is a slow, quiet failure rather than an event. Keep the parts list and the consumption record in source control alongside the bill of materials so the previous year's figures can be restored and compared when next year's number is set.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. This is a line you are adding, and it is the line that makes Part VII survivable.
