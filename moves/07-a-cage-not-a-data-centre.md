# 07 · A cage, not a data centre

**Layer:** Buy · **Leaving:** The region-and-zone abstraction · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the contract is signed

> The facility supplies power, cooling, connectivity and remote hands. Your team operates the platform; rented metal includes the room and the machines.

## Leaving from
- **AWS:** Regions and Availability Zones — zone letters are shuffled per account, so one account's us-east-1a is another's us-east-1c, and cross-zone traffic bills both ways.
- **Google Cloud:** regions and zones — a subnet covers the whole region rather than a zone, and quota is granted per region, so capacity in one zone is not capacity in the next.
- **Azure:** regions, availability zones and zone-redundant tiers — zone support varies by region and by machine series, and a resource created without a zone cannot be moved into one later.

## Why this works
Colocation puts the building, power, cooling and physical support under one facility contract. Remote hands can inspect equipment, replace labelled parts and move cables to an agreed runbook while your existing operations team manages the platform remotely. This Move adds a facility charge — about $4,500 a month for space, transit, cross-connects and hands before usage-based power — in exchange for that support. Rented metal bundles the room and machines into the monthly server price. Price both routes before signing; either lets the team operate infrastructure without running a data centre.

## Before you start

**Access**
- The committed power figure and machine count from Move 06
- Quotations from three facilities against one written specification

**Software**
- A comparison sheet with monthly charge, cross-connect price and notice period side by side

**People**
- A remote hands team with an agreed response time, plus two internal contacts authorised to direct work
- Whoever signs the term, before the price is agreed

## The runbook
1. Write one specification — full rack, committed kilowatts, two feeds, cross-connects, remote hands, term — and send it to three facilities. Set the location around network latency, delivery access and the contracted physical response time.
2. Size the power commitment against what actually draws: sixteen active nodes at about 450 W draw 7.2 kW before switches. The reference starts with a 10 kW commitment; verify the switch load and the facility's continuous-load limit, with either feed able to carry the full rack if the other fails. Leave the two spares unplugged on the shelf.
3. Contract the remote hands scope: inspections, labelled disk and machine replacements, cabling and power actions under an approved runbook. Put ticket-to-touch, included hours, out-of-hours rates and a named escalation in writing. Give the team the rack map and spare-part locations; name two internal contacts who can authorise work remotely.
4. Ask which carriers have live fibre in the meet-me room and which of them will sell at your volume, then get the cross-connect price list in writing, installation and disconnection included. Three carriers and a cheap cross-connect beat better marketing.
5. Negotiate the exit with the entrance: a term no longer than the hardware life, a capped escalator, a notice period you could serve. Three years with twelve months' notice repeats the mistake you are here to correct.
6. Before anyone signs, price the alternative in the next column: the same eighteen machines rented by the month, with power, networking and hardware replacement terms specified. Compare current quotes at matching capacity and support. Rented metal removes the fleet purchase and the separate facility agreement; use Move 03's full-cost comparison to choose the route.

## Operator's notes
- **Swap:** Rented dedicated servers can shorten procurement and avoid a separate cage contract. Confirm delivery dates, private networking, address portability and replacement response before ordering. The reference budgets the same operations hours for both routes: remote hands covers contracted physical work in colocation, and the rental provider covers it on dedicated servers. Choose renting when keeping capital available matters more than owning the fleet.
- **Do it faster:** Ask for the standard agreement and the cross-connect list before price is discussed; a day of reading decides which clauses are worth arguing.
- **Watch out:** A second building doubles the hardware, the spares and the change surface, and is the commonest reason a repatriation stalls. One site with backups held elsewhere beats two nobody has exercised.
- **Leftovers:** The cage invoices from handover while the cloud bill stays where it was; both run in parallel for about four months.

## Rollback
Refusing a facility that will not put ticket-to-touch in writing costs nothing: before signature there is no position to unwind. The point of no return is the commencement date, after which departure runs on the notice period rather than on a decision. File the quotations that lost; at renewal they restore a price to argue from.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | $4,500/mo | — | 0 min | 4 days | 3 weeks |

## What you can turn off
Nothing. This Move adds an outgoing instead of removing one; the cloud bill does not move until the first service does.
