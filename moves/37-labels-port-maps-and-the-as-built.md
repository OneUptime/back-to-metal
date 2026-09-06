# 37 · Labels, port maps and the as-built

**Layer:** Site · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the label scheme, port map and as-built that let somebody who has never entered the room replace the correct part at three in the morning.

## Leaving from
- **AWS:** instance identifiers and tags — an identifier that followed the resource, with no physical position to reconcile it against.
- **Google Cloud:** instance names and labels — the same, with a naming convention that never had to survive a machine being moved.
- **Azure:** resource names and tags — again logical identity only, which is why physical labelling is an unfamiliar discipline.

## Why this works
The document this Move produces has one test: hand it to a technician in another city who has never seen your cabinet, and see whether they can find and replace the correct part without ringing you. That requires a label scheme that names the position rather than the machine, so that moving a machine does not invalidate the label; both ends of every cable labelled, because a cable with one label is half a label; a port map tying switch port to cabinet, rack unit and interface; and serial numbers recorded against positions, so the drive that fails in Move 111 can be found by its bay rather than by guesswork.

## Before you start

**Access**
- The racked cabinet from Move 36, with the photographs taken
- The switch running configuration, exported, so port descriptions can be reconciled against reality

**Software**
- A label printer and durable labels, because paper and tape do not survive a warm aisle
- A single source for the as-built, in source control rather than in a drawing on somebody's laptop

**People**
- Whoever will be the remote technician's contact, since they are the one who will use this document

## The runbook
1. Choose a label scheme that names the position, not the equipment. Cabinet, rack unit, and where relevant the bay or port. A label that says which machine is in a slot is wrong the first time a machine moves; a label that says which slot it is stays true forever.
2. Label both ends of every cable with the same identifier, and put port descriptions into the switch configuration that match. A port map that disagrees with the switch is worse than no port map.
3. Record serial numbers against positions for every machine, drive bay and distribution unit. This is the table Move 110 will maintain and Move 111 will read at three in the morning.
4. Write the as-built: cabinet elevation, power plan with outlet and phase, network port map, cross-connect terminations, and the photographs from Move 36. One document, in source control, with a date.
5. Test it the only way that means anything. Send it to a supplier or technician in another city and ask them to describe how they would replace a specific drive in a specific machine. If they have to ask you a question, the document is not finished.
6. Put a review date on it and bind updates to the change process, because an as-built that is not updated when a cable moves becomes actively dangerous within about two months.

## Operator's notes
- **Swap:** Where a full asset system is available, use it, but keep the as-built as a flat document as well. The document is what somebody reads on a phone in a hall with no signal.
- **Do it faster:** Print the labels before going to site, from the cabinet plan. Labelling during the build takes minutes; labelling after it takes an afternoon and a torch.
- **Watch out:** Serial numbers on drives are frequently unreadable once installed. Record them during the build in Move 36, not afterwards, and photograph the labels while you can still see them.
- **Leftovers:** Old labels from a previous occupant of a cabinet are a genuine hazard. Remove them rather than labelling over them.

## Rollback
Documentation is corrected by correcting it, and there is nothing here to undo. The point of no return is the moment the document stops matching the cabinet, which happens silently and is the whole reason for the review date. Keep the as-built in source control with the photographs, so a previous version can be restored and compared when the cabinet and the document disagree and nobody remembers which changed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. This is the cheapest four days in this Part and the one that pays for itself in Part VII.
