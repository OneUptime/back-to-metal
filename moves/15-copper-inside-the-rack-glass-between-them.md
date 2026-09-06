# 15 · Copper inside the rack, glass between them

**Layer:** Iron · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately, at the cost of re-coding or re-ordering

> Orders cabling and optics once both ends exist, settles connector polish and vendor coding at order time, and buys one spare of every type in the same order.

## Leaving from
- **AWS:** VPC and Direct Connect — the physical layer existed and was billed to you as bandwidth, never as a connector type.
- **Google Cloud:** VPC and Cloud Interconnect — the same, with the cross-connect being the one place a physical detail ever reached you.
- **Azure:** Virtual Networks and ExpressRoute — again bandwidth as a product, and again a physical handoff you specified once and forgot.

## Why this works
Cabling is the cheapest part of the estate and the one that produces the most baffling faults, because a marginal optical link does not fail — it degrades, intermittently, under load, and presents as an application problem. The rules are short. Passive direct-attach copper inside a rack, out to about three metres, because it is cheap and it draws almost no power. Active optical or discrete transceivers beyond that. Single-mode fibre between racks rather than multimode, because the incremental cost is small and it does not need replacing at the next speed step. Everything else in this Move is about ordering the right variant of each, once, with the spares.

## Before you start

**Access**
- The cabling diagram from Move 12 with both ends of every link identified
- The switch part numbers from Move 13 and the card models from Move 14

**Software**
- The switch vendor's transceiver compatibility list and its position on third-party modules, in writing
- A link budget for anything longer than a rack, so the optic class is chosen rather than guessed

**People**
- Whoever will terminate the cabling, to agree on lengths and routing before anything is cut

## The runbook
1. Order nothing until both ends of every link exist on paper. A cable with one end is a guess, and a box of guesses is how a rack build stalls on the day.
2. Choose the cabling medium per link from the length: passive copper inside the rack, active optical or discrete transceivers past three metres, single-mode fibre between racks and out to the meet-me room.
3. Record connector type and polish per link. Duplex LC for the common single-mode optics, and MPO-12 with an angled polish for parallel single-mode. An angled channel with a flat-polished patch lead in it presents as a marginal optic and gets diagnosed last, after the switch, the card and the driver have all been blamed.
4. Settle the coding question at order time. Optics carry vendor identity in their memory, and switch vendors variously warn, refuse to link, or decline support on third-party modules. Confirm your choice against the support contract signed in Move 13, and buy accordingly.
5. Configure breakout ports before expecting a link. A hundred gigabit port split into four twenty-five gigabit lanes needs the port mode set on the switch first, and until it is set the link stays down with no useful error.
6. Buy one spare of every optic and cable type in the same order. They are cheap, they are the most common failure in the rack, and a spare that has to be ordered is a fault that lasts a week.

## Operator's notes
- **Swap:** Where a run is awkward and short, an active copper cable saves the transceiver cost and the power. Past five metres it stops being the cheaper answer.
- **Do it faster:** Order cables in the colours you will use for each purpose, and order them cut to length. Both cost almost nothing and both save an hour every time somebody works in the rack.
- **Watch out:** Bend radius is a real limit, not advice. A fibre pulled around a rack post at a tight angle will pass a link test on the day it is installed and fail six weeks later when the cabinet is tidied.
- **Leftovers:** Leftover optics are only useful if they are the coded variant your switch accepts. Keep them labelled with the vendor coding, not just the speed.

## Rollback
Everything in this Move is reversed by unplugging something. The cost is re-coding an optic where the vendor allows it and re-ordering where it does not, plus the delay of a second delivery. There is no point of no return in the usual sense; the nearest thing is the moment fibre is installed in a containment run and pulling it means a maintenance window. Keep the port map and the cable schedule in source control so the intended state can be restored when somebody has moved a cable and not said so.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. This Move is a small line on the bill of materials and an outsized share of the faults you will chase in Part III.
