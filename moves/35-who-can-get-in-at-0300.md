# 35 · Who can get in at 03:00

**Layer:** Site · **Leaving:** The shared-responsibility split for physical security · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Settles the access list, the escort rules and a remote-hands agreement measured in ticket-to-touch, and ends with a ticket template a stranger can follow.

## Leaving from
- **AWS:** the shared responsibility model — physical security was entirely theirs, evidenced by a report you downloaded and filed.
- **Google Cloud:** its shared responsibility documentation — the same split, with the physical layer described in a whitepaper rather than inspected.
- **Azure:** its shared responsibility guidance — again the provider's half, and again the reason nobody has an access list to maintain.

## Why this works
Physical access is now yours to manage in both directions. Inward: who is on the named list, how quickly a leaver comes off it, whether contractors need an escort, whether the cabinet is locked and who holds the second key, and how long camera footage is retained. Outward: what the facility's own staff will do for you when nobody can drive there, which is the remote hands agreement, and it is measured in ticket-to-touch rather than in response time. Underneath both sits a fact no contract changes — facility staff can open your cabinet — which is why Move 48 puts encryption and key custody beneath everything that follows.

## Before you start

**Access**
- The facility's access request procedure and how long it takes to add or remove a name
- The remote hands agreement as a document, with its billing increments and escalation path

**Software**
- A ticket template with photographs, cabinet, rack unit and port number, written before it is needed
- A record of who is on the access list, kept somewhere the leaver process actually reaches

**People**
- Whoever runs joiners and leavers, because an access list that is not part of that process rots within a quarter

## The runbook
1. Fix the named access list and how a leaver is removed from it. Bind the removal to the same process that revokes everything else, or the list will contain former employees within a year.
2. Settle the escort rules for contractors and suppliers, and who is permitted to authorise a visit at three in the morning. That authority needs a name and a deputy, not a role nobody occupies out of hours.
3. Decide whether the cabinet is locked, who holds the keys and whether the facility holds a second one. Locked cabinets slow down remote hands; unlocked ones speed up everybody, including people you have not met.
4. Read the remote hands agreement for the number that matters. Ticket-to-touch is how long until somebody is standing at your cabinet; response time is how long until somebody reads the ticket. They differ by hours. Note the billing increment, which is usually fifteen minutes with a minimum.
5. Build the escalation ladder with a name and a telephone number at the top, and test it once during working hours by raising a trivial ticket and following it up.
6. Write the ticket template. The technician does exactly what the ticket says and no more, so it carries photographs of the front and rear, the cabinet identifier, the rack unit, the port number and the expected outcome. A stranger should be able to follow it without ringing you.

## Operator's notes
- **Swap:** Where remote hands is slow or expensive, the cold spare machine from Move 19 covers more faults than any support contract, because it converts a repair into a replacement.
- **Do it faster:** Raise one trivial remote hands ticket in the first week — reseat a cable, read a serial number — purely to learn the process while it does not matter.
- **Watch out:** Camera retention is often shorter than you assume, sometimes only a fortnight. If evidence matters for the audit in Move 119, ask for the retention in writing.
- **Leftovers:** Access lists accumulate contractors. Review the list quarterly, on a date, rather than after an incident.

## Rollback
Every arrangement here is reversed by changing a list or a document, and none of it is structural. The point of no return does not exist in this Move, which is why it is worth doing carefully now rather than under pressure later. Keep the access list, the ticket template and the escalation ladder in source control so a known good version can be restored when somebody edits the template and removes the photographs.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. This Move is what makes the facility usable by a small team that does not live next to it.
