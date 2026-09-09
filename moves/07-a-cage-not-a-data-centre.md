# 07 · A cage, not a data centre

**Layer:** Buy · **Leaving:** The region-and-zone abstraction · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the contract is signed

> The facility supplies power, cooling, connectivity and remote hands. Your team operates the platform; rented metal includes the room and the machines.

## Leaving from
- **AWS:** Regions and Availability Zones — older accounts in some regions map zone letters differently; compare AZ IDs, which identify the same location across accounts.
- **Google Cloud:** regions and zones — a subnet covers the whole region rather than a zone, and quota is granted per region, so capacity in one zone is not capacity in the next.
- **Azure:** regions, availability zones and zone-redundant tiers — zone support varies by region and VM series; moving an existing regional VM into a zone needs a supported migration path and downtime.

## Why this works
Colocation puts the building, power, cooling and physical support under a facility contract. Remote hands inspect equipment, replace labelled parts and move cables to an agreed runbook while the existing team operates the platform. The reference allows $4,500 a month for space, transit, cross-connects and hands before usage-based power; obtain a local quote. Rented metal bundles the room, machines and contracted hardware support into the server price. One rack is one site failure domain, even with redundant power and switches. Match that limitation to the recovery objectives before choosing either route.

## Before you start

**Access**
- The provisional fleet and facility quotes from Move 03, reconciled with Move 06 before signing
- Quotations from three facilities against one written specification

**Software**
- A comparison sheet with monthly charge, cross-connect price and notice period side by side

**People**
- A remote hands team with an agreed response time, plus two internal contacts authorised to direct work
- Whoever signs the term, before the price is agreed

## The runbook
1. Write one specification — full rack, committed kilowatts, two feeds, cross-connects, remote hands, term — and send it to three facilities. Set the location around latency and physical response time. If a site outage must recover faster than replacement hardware and an off-site restore, include an independent recovery site in Move 03's budget.
2. Size power against measured peak draw, including switches and recovery load. The reference's sixteen nodes at 450 W total 7.2 kW before networking, with a provisional 10 kW commitment. Verify the actual fleet, continuous-load limits and cooling allowance; either feed must carry the whole rack after the other fails. Keep owned spares unplugged.
3. Contract the remote hands scope: inspections, labelled disk and machine replacements, cabling and power actions under an approved runbook. Put ticket-to-touch, included hours, out-of-hours rates and a named escalation in writing. Give the team the rack map and spare-part locations; name two internal contacts who can authorise work remotely.
4. Ask which carriers have live fibre in the meet-me room and which of them will sell at your volume, then get the cross-connect price list in writing, installation and disconnection included. Three carriers and a cheap cross-connect beat better marketing.
5. Negotiate the exit with the entrance: a term no longer than the hardware life, a capped escalator, a notice period you could serve. Three years with twelve months' notice repeats the mistake you are here to correct.
6. Before anyone signs, price the alternative in the next column: the same eighteen machines rented by the month, with power, networking and hardware replacement terms specified. Compare current quotes at matching capacity and support. Rented metal removes the fleet purchase and the separate facility agreement; use Move 03's full-cost comparison to choose the route.

## Operator's notes
- **Swap:** Rented dedicated servers can shorten procurement and avoid a separate cage contract. Confirm delivery dates, private networking, failure-domain placement and replacement response. The reference holds staffing constant; validate the actual support and operating effort in Move 03.
- **Do it faster:** Ask for the standard agreement and the cross-connect list before price is discussed; a day of reading decides which clauses are worth arguing.
- **Watch out:** Off-site backups preserve a recovery copy; they do not keep services running during a site outage. Exercise the restore and price a second failure domain when the required recovery time demands it.
- **Leftovers:** The facility invoices from the agreed commencement date while cloud charges continue. Budget overlap from the delivery and migration schedule, including delays.

## Rollback
Refusing a facility before signature leaves no contract to unwind. The contractual point of no return is accepting a binding agreement, which can create liabilities before the commencement date. Check cancellation, minimum-term and notice charges before signing. Keep the losing quotations and the agreed service specification so earlier assumptions can be restored during renewal discussions.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | $4,500/mo | — | 0 min | 4 days | 3 weeks |

## What you can turn off
Nothing. This Move adds an outgoing instead of removing one; the cloud bill does not move until the first service does.
