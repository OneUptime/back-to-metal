# 17 · Who you buy from, and what is safe to buy used

**Layer:** Iron · **Leaving:** The hardware refresh someone else did for you · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 14 to 30 days, per the vendor's return window

> Prices the specification three ways, reads the warranty for response against restore, and treats lead time rather than unit price as the schedule risk.

## Leaving from
- **AWS:** EC2 instance generations — a refresh was a change of instance type, done by somebody else on a schedule you never saw.
- **Google Cloud:** Compute Engine machine generations — the same, with live migration meaning you often did not notice hardware changing underneath you.
- **Azure:** Virtual Machines series refreshes — again somebody else's capital cycle, surfaced to you only as a new series in the portal.

## Why this works
The cloud did your hardware refresh for you, and the price of taking it back is that you now have a supplier relationship, a warranty to read and a lead time to plan around. The three ways to buy the same specification are a tier-one vendor with next-business-day on-site parts, a whitebox builder at a lower price with return-to-base service, and refurbished. All three are legitimate. What separates them is not the unit price but what happens in year four, when the platform reaches end of service life and spares stop being manufactured — and, in the meantime, how long a machine takes to arrive, which is the risk that actually moves this programme's dates.

## Before you start

**Access**
- The complete specification from Moves 04 through 15, in enough detail that three suppliers quote the same thing
- Your organisation's position on refurbished equipment, since some procurement policies forbid it outright

**Software**
- A comparison sheet with warranty terms as columns rather than a footnote
- A written inspection list for any used equipment, agreed before anything is shipped

**People**
- Two reference customers per supplier, spoken to rather than read about

## The runbook
1. Write one specification and send it to all three channels unchanged. Suppliers who are allowed to propose their own configuration will each propose a different one, and you will end up comparing three things instead of three prices.
2. Read each warranty for the distinction that matters: response against restore. A four-hour response commitment means an engineer is dispatched, not that the machine works again. Parts-only against parts-and-labour is the second column, and end of service life is the third.
3. Price the refurbished option honestly. It is legitimate for chassis, processors, switches and optics, and it is where a memory price spike will push you. It is never right for flash, batteries or supercapacitors, because those wear and their remaining life is the thing you cannot see.
4. For anything used, apply the inspection list before payment: percentage used and power-on hours from every drive, the controller event log, the current firmware level and whether it can still be updated, and whether the serial number is still entitled to vendor support.
5. Compare lead times as carefully as prices. Memory is the long pole, quoted build times move by months, and a quote is not a delivery date. Ask for a date, in writing, with a penalty or a cancellation right attached.
6. Call the reference customers and ask one question: what happened the last time you had a failure. The answer separates suppliers more reliably than any specification sheet.

## Operator's notes
- **Swap:** For a first rack that mainly needs to prove the approach, a whitebox builder with return-to-base is often the right economics. Move to a tier-one contract when the estate is carrying revenue and an outage costs more than the premium.
- **Do it faster:** Ask each supplier for their lead time before their price. Two of the three will usually disqualify themselves on the date, which shortens the exercise considerably.
- **Watch out:** A support entitlement follows the serial number, not the invoice. A machine sold on twice can arrive with a valid warranty that the vendor will not honour for you until it is transferred, and transfers can be refused.
- **Leftovers:** Suppliers will offer to hold stock. A holding agreement without a signed order is worth exactly nothing when somebody else pays first.

## Rollback
A purchase from a reputable supplier can be returned inside its window, which is fourteen to thirty days on most contracts and is the reason this Move sits before the acceptance testing in Move 18 rather than after it. Past that window the equipment is yours. The point of no return is the expiry of the return period, not the delivery date, and the two are frequently confused. Keep every quote, warranty document and entitlement check filed with the bill of materials so a support position can be restored when a vendor disputes it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 weeks | 2 weeks |

## What you can turn off
Nothing yet. The old estate carries production until Part V and Part VI have moved off it.
