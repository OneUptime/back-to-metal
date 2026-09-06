# 34 · The importer of record and the loading dock

**Layer:** Site · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the shipment is booked

> Names the importer of record, settles the customs and import-VAT position, and books the dock, the lift and the window against a cabinet approaching a tonne.

## Leaving from
- **AWS:** EC2 capacity — hardware logistics were entirely invisible, and the only thing that ever crossed a border was a packet.
- **Google Cloud:** Compute Engine capacity — the same, with regional expansion happening without any involvement from you at all.
- **Azure:** Virtual Machines capacity — again a service, and again the reason a customs entry feels like an unfamiliar kind of problem.

## Why this works
Getting the hardware into the building has a legal half and a physical half, and both stop a delivery cold. The legal half is that a colocation provider will not act as importer of record, because that would put its name on a customs debt for equipment it does not own. You need an entity with a customs registration in the destination country and a broker who has read the commercial invoice before the pallet flies. The physical half is that a populated cabinet approaches a tonne, delivery windows are booked, docks have hours, and lifts have limits — and a pallet that will not fit a passenger lift is a delivery that goes back on the truck.

## Before you start

**Access**
- The customs registration for the importing entity in the destination country, obtained rather than assumed
- The facility's delivery procedure, dock hours and lift capacity, in writing

**Software**
- A commercial invoice reviewed by the broker before shipping, with correct classification and values
- A delivery plan naming who receives, who signs, and where the packaging goes afterwards

**People**
- A customs broker engaged early, and somebody at the facility expecting the pallet on the day

## The runbook
1. Name the importer of record and confirm it holds a customs registration in the destination country. The facility will decline this role, and discovering that when the shipment is at the border is expensive in both fees and days.
2. Settle the classification and the tax position with the broker. Servers generally fall under a heading that attracts no duty under the international agreement covering information technology equipment, but import tax falls due on the landed value, only the named importer can recover it, and origin-based tariffs can override the headline treatment.
3. Have the broker review the commercial invoice before anything ships. Wrong values, wrong classification or a missing importer reference are the three things that hold a pallet, and all three are fixed in an email beforehand.
4. Book the delivery window with the facility, in writing, with dock hours and an on-site contact. Ask specifically about lift capacity and dimensions, because a populated cabinet approaching a tonne does not go in a passenger lift.
5. Decide whether cabinets arrive populated or are built in place. Populated saves days of work and needs a goods lift and a dock; built in place is slower and fits through more doors.
6. Plan where the packaging goes. A pallet of cardboard in a hall is a fire-load problem and most facilities will charge you to remove it or refuse to let it stay.

## Operator's notes
- **Swap:** Where the importing entity does not exist in the destination country, a delivered-duty-paid arrangement with the supplier can work, at a premium, and it removes the recovery of import tax. Price both.
- **Do it faster:** Ask the supplier to ship to a local staging warehouse first. It converts an international shipment with a border in it into a domestic delivery you can reschedule.
- **Watch out:** Lithium batteries in uninterruptible supplies have their own shipping rules, and a mixed pallet can be held for one item. Ask the supplier to ship batteries separately if there is any doubt.
- **Leftovers:** Keep the customs entry documents. They are needed to recover import tax and they will be asked for at the audit in Move 119.

## Rollback
Until a shipment is booked this is paperwork, and paperwork is revised. Once goods are in transit the importer of record is named on a customs entry and changing it means an amended entry, delay and fees. The point of no return is the booking, not the border. Keep every entry document, invoice and delivery note filed with the bill of materials so the import position can be restored and evidenced months later when finance or an auditor asks.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 5 days | 3 to 6 weeks |

## What you can turn off
Nothing yet. This Move is pure overhead, and skipping it is how hardware sits at a border for a fortnight.
