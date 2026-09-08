# 07 · A cage, not a data centre

**Layer:** Buy · **Leaving:** The region-and-zone abstraction · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the contract is signed

> A full rack ninety minutes from somebody who can drive to it, and the first line in this programme that costs money instead of saving it.

## Leaving from
- **AWS:** Regions and Availability Zones — zone letters are shuffled per account, so one account's us-east-1a is another's us-east-1c, and cross-zone traffic bills both ways.
- **Google Cloud:** regions and zones — a subnet covers the whole region rather than a zone, and quota is granted per region, so capacity in one zone is not capacity in the next.
- **Azure:** regions, availability zones and zone-redundant tiers — zone support varies by region and by machine series, and a resource created without a zone cannot be moved into one later.

## Why this works
A region and a zone were labels on an invoice. Underneath sat a building, a power feed, a loading dock and somebody's hands, and this Move buys one of each: a full rack in a carrier-neutral facility, near enough that somebody can be at the cabinet within a couple of hours. Nothing binds until a signature, and every term that hurts later is negotiable before it. It also costs more rather than less — about $4,500 a month for the space, the transit, the cross-connects and the hands, paid from handover, before a machine is racked. One site, not two.

## Before you start

**Access**
- The committed power figure and machine count from Move 06
- Quotations from three facilities against one written specification

**Software**
- A comparison sheet with monthly charge, cross-connect price and notice period side by side

**People**
- Two named people who can reach the building out of hours
- Whoever signs the term, before the price is agreed

## The runbook
1. Write one specification — full rack, committed kilowatts, two feeds, cross-connects, remote hands, term — and send it to three facilities within ninety minutes' drive.
2. Size the power commitment against what actually draws: five racked nodes at about 450 W plus two switches is near 2.5 kW, and the eighty per cent rule means a 3 kW commitment only permits 2.4 kW continuously. Ask for 4 kW on two feeds from separate distribution boards, and leave the sixth machine unplugged on the shelf.
3. Put ticket-to-touch, the billing increment and a named escalation into the remote hands contract rather than the sales deck, and two named people on the access list so one holiday is not an outage.
4. Ask which carriers have live fibre in the meet-me room and which of them will sell at your volume, then get the cross-connect price list in writing, installation and disconnection included. Three carriers and a cheap cross-connect beat better marketing.
5. Negotiate the exit with the entrance: a term no longer than the hardware life, a capped escalator, a notice period you could serve. Three years with twelve months' notice repeats the mistake you are here to correct.
6. Before anyone signs, price the alternative in the next column of the comparison sheet: the same eighteen machines rented by the month, racked and powered by somebody else. Quote it rather than taking a figure from here — the spread between the cheapest European provider and a US one is a factor of two or three on the same specification, and it is wide enough to decide the question on its own. At this fleet size that column is at worst competitive, and Move 03's rule applies to it too.

## Operator's notes
- **Swap:** Rented dedicated servers skip this Move and Move 08's lead times — about a month off the programme. Compare whole columns, not the hardware line against a column: rented metal costs somewhere between three-quarters and twice the $3,235 of owned infrastructure depending on whose list you quote, and it wins back about a quarter of an engineer, so the totals land between comfortably under owning and level with it. What you give up is the network, your own addresses and the price you can hold; what you keep is the capital. On short runway, rent.
- **Do it faster:** Ask for the standard agreement and the cross-connect list before price is discussed; a day of reading decides which clauses are worth arguing.
- **Watch out:** A second building doubles the hardware, the spares and the change surface, and is the commonest reason a repatriation stalls. One site with backups held elsewhere beats two nobody has exercised.
- **Leftovers:** The cage invoices from handover while the cloud bill stays where it was; both run in parallel for about four months.

## Rollback
Refusing a facility that will not put ticket-to-touch in writing costs nothing: before signature there is no position to unwind. The point of no return is the commencement date, after which departure runs on the notice period rather than on a decision. File the quotations that lost; at renewal they restore a price to argue from.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | $1,400/mo | — | 0 min | 4 days | 3 weeks |

## What you can turn off
Nothing. This Move adds an outgoing instead of removing one; the cloud bill does not move until the first service does.
