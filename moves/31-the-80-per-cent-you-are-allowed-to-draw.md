# 31 · The 80 per cent you are allowed to draw

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Turns the bill of materials into a per-cabinet power budget in the units the facility bills in, with outlets counted and the phases balanced.

## Leaving from
- **AWS:** instance families and their implied draw — power existed only as a component of the hourly rate you paid.
- **Google Cloud:** machine families and their carbon reporting — the closest any of the three came to telling you what a workload drew, and it was a report rather than a budget.
- **Azure:** virtual machine series and their sustainability calculator — again a report after the fact, never a constraint you designed against.

## Why this works
The facility bills in kilowatts against a committed figure, and your bill of materials is in machines. This Move does the conversion explicitly, because the arithmetic has two traps in it. The first is the derate: a 208 volt three-phase 30 amp feed is 10.8 kVA on the nameplate and about 8.6 kW once a continuous-load derate is applied, while a 400 volt three-phase 32 amp European feed is 22.2 kVA and is sold against a different convention entirely. The second is outlets, which nobody counts until the strips arrive: every machine takes two, every switch takes two, and the mix of socket types is fixed the day the distribution units are ordered.

## Before you start

**Access**
- The per-node and per-rack draw from Move 07, and the machine count from Move 11
- The feed type the facility is offering, as volts, phases and amps rather than as a kilowatt figure

**Software**
- The power distribution unit datasheets for the exact model you intend to order, with the outlet mix listed
- A cabinet elevation drawing, even a rough one, so outlets and rack units are counted together

**People**
- Whoever will order the distribution units, because the outlet mix cannot be changed afterwards

## The runbook
1. Convert the feed to a usable figure. Multiply volts by amps by the phase factor for the nameplate, then apply the derate the contract in Move 28 actually states. Write both numbers down, because people will quote the first one at you.
2. Sum the measured draw of everything going in the cabinet at expected load and at peak, using the figures from Move 07 rather than badge ratings.
3. Count the outlets by type. Every machine takes two, every switch takes two, the console server takes one or two, and the mix of socket types is fixed when the strips are ordered. Running out of one type with spare capacity in the other is a common and avoidable delivery-day failure.
4. Balance the phases. A three-phase strip distributes outlets across phases in a fixed pattern, so which slot a machine plugs into decides which phase it loads. An unbalanced cabinet trips a breaker at a total draw well below its rating.
5. Leave headroom for year two. A cabinet planned to its committed figure on day one has nowhere to put the machines Move 11 said you would add, and increasing the commitment is an amendment under Move 28's terms.
6. Publish the cabinet plan: position, draw, outlet, phase. Move 36 racks against it and Move 37 documents it.

## Operator's notes
- **Swap:** Where the facility offers metered distribution units, take them. Per-outlet measurement turns Move 120's cost arithmetic from an estimate into a reading, and it is worth the small premium.
- **Do it faster:** Ask the facility which distribution units their other customers use in that hall. Matching them means the remote hands technician in Move 35 already knows the equipment.
- **Watch out:** Inrush at power-on is much higher than steady draw. A cabinet that sits comfortably inside its budget can trip a breaker when everything starts at once after a supply failure, which is precisely when you least want it.
- **Leftovers:** Distribution units bought for one feed type do not work on another. If the facility choice is not final, do not order the strips.

## Rollback
Nothing here is committed until the distribution units are ordered, and a cabinet plan is revised by revising it. The point of no return is the strip order, because the outlet mix and the feed type are fixed at that moment and a wrong choice is a re-purchase rather than a reconfiguration. Keep the cabinet plan and the power arithmetic in source control so the intended layout can be restored when somebody has moved a machine to a different outlet without updating the drawing.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. This Move turns a bill of materials into the number the facility invoices against.
