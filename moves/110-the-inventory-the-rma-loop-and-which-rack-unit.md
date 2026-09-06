# 110 · The inventory, the RMA loop and which rack unit

**Layer:** Watch · **Leaving:** The provider's capacity pool and its hardware-retirement notices · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Holds serial, rack unit, bay and node name in one inventory with a funded return loop, because hardware nobody can find is hardware nobody can replace.

## Leaving from
- **AWS:** EC2 instance retirement notices — a failing machine was replaced by somebody else and announced to you as an event.
- **Google Cloud:** Compute Engine host maintenance events — the same, mostly handled by migration before you noticed.
- **Azure:** Virtual Machines planned and unplanned maintenance events — again a notification rather than a part in your hand.

## Why this works
This Move is logistics rather than engineering, and it is the difference between a two-hour repair and a two-week one. One inventory holds serial number, rack unit, bay and node name for every machine and every device, seeded from the as-built in Move 37 and the bill of materials in Move 20. Behind it sits a return loop that is funded and has a named contact, because a warranty claim with no owner is a warranty claim nobody files. Diagnosis is Move 111; the spares themselves were budgeted in Move 19. What is new here is being able to find the thing.

## Before you start

**Access**
- The as-built from Move 37 and the bill of materials from Move 20, both current
- The support contracts from Move 17, with their return terms read rather than assumed

**Software**
- An inventory system that holds physical position as a first-class field, not a tag on a virtual resource
- A seeding script, because typing three hundred serial numbers by hand produces three hundred opportunities for error

**People**
- A named contact for returns at every supplier, and a named owner for the inventory

## The runbook
1. Choose an inventory system that models racks, rack units, bays and devices properly. A spreadsheet works for a single rack and stops working at the second.
2. Seed it with a script from the as-built and the bill of materials. Serial number, position, node name, and the acceptance test result from Move 18 for each machine.
3. Record the firmware baseline per machine while you are there, because Move 111 treats firmware as a data-loss concern and needs a starting point.
4. Build the return loop: who raises a claim, with which supplier, under which contract, and what advance replacement does to your holdings. Advance replacement is worth paying for and it obliges you to return the failed part or be billed for it.
5. Read the warranty terms for rented dedicated machines separately. They differ sharply from owned hardware, and the provider replaces the machine rather than the part, which changes what your inventory has to track.
6. Establish a parts service level with a named contact and a telephone number, and test it once with a trivial claim while nothing is broken.
7. Reconcile the inventory against reality monthly. Half a day a month keeps it true; a year of neglect makes it worse than nothing, because people trust it.

## Operator's notes
- **Swap:** For a single rack, a well-maintained document from Move 37 plus a spares list is enough. The inventory system earns its place at the second rack or the second site.
- **Do it faster:** Seed it during the build in Move 36, when the serial numbers are visible and the machines are open. Reading a serial number off an installed machine is a torch-and-mirror job.
- **Watch out:** A device replaced under warranty comes back with a different serial number. An inventory that is not updated at replacement time drifts immediately and silently.
- **Leftovers:** The provider's retirement notification wiring — the event rules and the notifications behind it — can be removed when the old estate goes.

## Rollback
An inventory is corrected by correcting it and there is nothing here to reverse. The point of no return is the moment it stops matching reality, which happens quietly and is why the monthly reconciliation exists. Keep the inventory's data exported to source control periodically so a corrupted or lost system can be restored, and so that the physical estate can be reconstructed on paper if the system is unavailable during an incident.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
The provider's retirement notification wiring, once the old estate is gone. This Move adds a small cost and removes a category of two-week repairs.
