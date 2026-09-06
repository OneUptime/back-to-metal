# 07 · One rack unit or two, and the watts it draws

**Layer:** Iron · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Chooses chassis and supplies from the CPU and DIMM population, and produces the per-node and per-rack draw the facility contract in Part II is written against.

## Leaving from
- **AWS:** EC2 instance families — density, cooling and power were somebody else's problem, expressed to you only as a price per hour.
- **Google Cloud:** Compute Engine machine families — the same abstraction, with the added detail that local SSD capacity was fixed per shape rather than chosen.
- **Azure:** Virtual Machines series — the L-series existed precisely because drive bays are a physical constraint, which is the constraint this Move makes visible again.

## Why this works
The chassis is where every earlier decision becomes a physical object with a height, a depth, an airflow direction and a power draw. A 1U machine is denser and its fans work harder, which costs watts and makes noise a real consideration in a room you own; a 2U machine gives you drive bays, PCIe slots and cooling headroom for less fan power. Neither is right in general. What is right in general is that the answer is derived from the CPU thermal design power and the module population you have just chosen, and that the output is a number in watts per node and per rack, because that number is what the facility contract in Part II is written against.

## Before you start

**Access**
- The processor and memory selections from Moves 04 and 06, as part numbers rather than descriptions
- The drive count from Move 10 if it exists yet, or a working assumption you will revisit

**Software**
- The vendor's chassis configuration tool, which will refuse combinations a datasheet suggests are fine
- A power calculator from the same vendor, used for shape rather than for precision

**People**
- Whoever will negotiate the facility contract in Part II, because the draw you produce here is their opening number

## The runbook
1. Set the height from what has to fit. Drive bays and PCIe slots drive 2U; nothing else usually does. Count the slots you need for network cards and any accelerator before choosing, because a slot you discover you need after delivery is a new chassis.
2. Fix rack depth and the rail kit against a cabinet you have not signed for yet. Deep chassis in a shallow cabinet is the most common delivery-day failure, and the cabinet is chosen in Part II, so record the constraint rather than assuming a standard.
3. Choose front or rear input and output so that cabling and airflow agree. Cold aisle at the front, hot aisle at the back, cables where the air is not. A machine that has to be cabled from the cold aisle will be cabled from the cold aisle for its whole life.
4. Size the supplies against measured draw rather than badge rating. Titanium-rated units are generally 200 to 240 V input only and peak in efficiency near half load, so a pair of oversized supplies running at fifteen per cent is both more expensive and less efficient than the right pair.
5. Confirm that the two supplies can be fed from two different sources. Two supplies on one busbar is one feed and two failure points, which is worse than one supply and an honest single point of failure, because it is believed to be redundant.
6. Refuse multi-node and blade chassis for this estate. A shared midplane, shared supplies and vendor-locked spares move the failure domain from the node to the enclosure, which is exactly the direction you are trying to travel.
7. Publish per-node and per-rack draw at idle, at your expected load and at the peak the machine can reach. Part II needs all three, and the third one is what a facility charges against.

## Operator's notes
- **Swap:** Where the estate is small and the room is your own, 2U everywhere is a defensible default. Density is a constraint of expensive floor space, and if the floor is cheap, buy the cooling headroom.
- **Do it faster:** Ask the vendor for a configured power report for the exact build. It takes them an hour and it is more accurate than any calculator you will run.
- **Watch out:** Fan power rises steeply with inlet temperature. A 1U node validated in a cool lab can draw considerably more in a warm aisle, and that difference lands on your electricity bill every hour for three years.
- **Leftovers:** Rails, cable-management arms and bezels are usually quoted separately and forgotten. They are trivial money and they hold up an installation day.

## Rollback
Nothing is committed until Move 20 signs the order, and until then a chassis choice is reversed by changing a line in a configuration. The point of no return is that order, after which a machine that does not fit the cabinet is a logistics problem rather than an edit. Keep the vendor's configured build sheets and power reports in source control alongside the bill of materials so the original assumptions can be restored and compared when the delivered draw turns out to differ from the quoted one.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. The output of this Move is a number in watts, and Part II is where it starts costing money.
