# 36 · The first rack

**Layer:** Site · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Racks the first cabinet in the order that survives contact with the second: strips first, weight low, gaps blanked, and photographs before any data cable.

## Leaving from
- **AWS:** launching an instance — capacity appeared in ninety seconds and the physical work behind it was somebody else's shift.
- **Google Cloud:** creating an instance — the same, with the machine's location expressed as a zone label.
- **Azure:** deploying a virtual machine — again minutes rather than days, which is the expectation this Move gently corrects.

## Why this works
The first cabinet teaches you how to build the second, and the order of operations is what decides whether that lesson is cheap. Power distribution and cable management go in before anything heavy, because retrofitting them means unracking machines. Switches go where the cabling plan wants them rather than at the top out of habit. The heaviest chassis go low. Rails are checked against the actual cabinet depth rather than the specification, and the rack-unit budget has already counted the strips, the patch panels and the console server. Deliberate gaps are left for year two and every one of them is blanked.

## Before you start

**Access**
- The cabinet, delivered and positioned, with the feeds live and the cross-connects at least ordered
- A booked day on site with the facility notified, because this takes longer than anyone estimates

**Software**
- The cabinet plan from Move 31 and the cabling diagram from Move 12, printed and taken with you
- The acceptance results from Move 18, so you know which machines are known good

**People**
- Two people for the whole day, because a two-rack-unit chassis at height is not a one-person job

## The runbook
1. Fit the power distribution units and the cable management first, then the patch panels. Anything that has to be retrofitted behind a populated cabinet costs an evening.
2. Place the switches where the cabling plan wants them. Top of the cabinet is a habit rather than a rule, and middle placement halves the average cable run in a full cabinet.
3. Rack the heaviest chassis low. Check every rail kit against the actual cabinet depth before lifting anything, because a rail that does not fit is discovered at the worst possible moment.
4. Leave deliberate gaps for the machines Move 11 said you would add in year two, and blank every gap. An unblanked gap recirculates hot air straight back to the inlet above it.
5. Power up, confirm the out-of-band network from Move 16 is reachable from outside the building, and confirm every management controller answers. Do this before touching a data cable, so that a machine that will not come up is a machine you can still reach.
6. Photograph the front and the rear before any data cabling. These photographs go in the ticket template from Move 35 and they are what a remote technician will be looking at.
7. Cable the data network last, to the plan, labelling both ends as you go. Move 37 turns the labels into a document.

## Operator's notes
- **Swap:** Where the supplier offers to rack and cable on delivery, take it for the first cabinet and watch them do it. It is the fastest way to learn what your own second cabinet should look like.
- **Do it faster:** Build the cabinet in the order above and resist the urge to cable as you go. Batch the cabling at the end and it takes half as long and looks like it was planned.
- **Watch out:** Cable slack is the thing that makes a cabinet maintainable. Too little and a machine cannot slide out on its rails; too much and the rear becomes impassable. Dress to a length rather than to a bundle.
- **Leftovers:** Packaging, rails you did not use and cables of the wrong length all accumulate. Take them away the same day, because the facility will charge you or refuse to store them.

## Rollback
Everything in a cabinet can be unracked, and on day one that is a day's work rather than a change window. The point of no return is the moment the cabinet carries production, after which every physical change is a maintenance window. This is the argument for leaving the gaps and blanking them now. Keep the cabinet plan and the photographs somewhere durable and backed up, so the as-built state can be restored and compared after somebody has worked in the cabinet without saying so.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet. There is now a cabinet drawing power in one building and a full cloud bill in another.
