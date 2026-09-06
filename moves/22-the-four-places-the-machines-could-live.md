# 22 · The four places the machines could live

**Layer:** Site · **Leaving:** The region-and-zone abstraction · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Prices retail colocation, wholesale space, rented dedicated servers and a room you already occupy against the committed power figure, with staff time counted.

## Leaving from
- **AWS:** Regions and Availability Zones — a physical estate presented as two labels, with the buildings, the power and the people all abstracted away.
- **Google Cloud:** regions and zones — the same abstraction, with the difference that a network spans regions, which is a property you will not be reproducing.
- **Azure:** regions and availability sets — the same again, with the set describing a fault domain inside a building you were never going to see.

## Why this works
A region and a zone were labels. Underneath them were four things you are now choosing between: retail colocation, where you rent cabinets and power in somebody else's building; wholesale space, where you rent a room or a hall; rented dedicated machines, where somebody else owns the metal and you own everything above the operating system; and a room in a building you already occupy. All four are legitimate. What decides between them is not preference but arithmetic: capital cost, monthly cost at the committed power figure from Move 20, staff time consumed, lead time to the first boot, and what it costs to leave.

## Before you start

**Access**
- The committed power figure, rack-unit budget and machine count from Move 20
- Quotations from at least four suppliers, requested against the same specification

**Software**
- A single comparison sheet with the five columns above, filled in for each option
- The staffing model from Part VII brought forward, because the rota changes which options are affordable

**People**
- Whoever will approve headcount, since the difference between these options is measured in people as much as in money

## The runbook
1. Request quotations against the same specification: the committed kilowatts, the rack-unit count, the cross-connects and the term. Suppliers left to propose their own shape will not be comparable.
2. Price all four options on one comparison sheet, on capital cost and monthly cost. For the reference estate in this book, a cabinet with power, transit, a cross-connect and remote hands lands near $2,900 a month per site before the machines are amortised, and the same machines rented as dedicated servers land near $480 each per month with the racking and the hands included.
3. Add the staff time each option consumes, in fractions of a person. This is where retail colocation and rented metal separate: the rented option removes the racking, the hands and most of the physical rota, and removes none of the platform work.
4. Carry the rota arithmetic forward from Move 113 rather than leaving it to Part VII. A rota that covers nights and weekends without burning people out needs a headcount, that headcount has a cost, and that cost changes which of these four options is affordable. This is the last point at which the reader can act on the answer.
5. Add lead time and exit cost. Retail colocation is weeks; wholesale is months; rented metal is days; a room in your own building is however long the plant works take, plus consent.
6. Treat a mixed landing as a real answer rather than indecision. Rented machines in another city are usually the cheapest disaster-recovery target you will ever price, and running the primary estate in colocation with a rented secondary is a defensible design rather than a compromise.

## Operator's notes
- **Swap:** For a team of fewer than about six engineers, rented dedicated machines get most of the economics with almost none of the physical work. It is the right answer more often than this book's title suggests.
- **Do it faster:** Ask each supplier for a price at your committed power and at twice it. The gap between those two numbers tells you what growth will cost, and it is where the surprises live.
- **Watch out:** Retail colocation quotes are per cabinet and per kilowatt, and cross-connects, remote hands and cabinet accessories are all extra. A quote that looks half the price of another is usually missing three lines.
- **Leftovers:** Nothing is decommissioned by this Move. Everything in the cloud keeps running, and will keep running until Part VI.

## Rollback
No commitment is made here: this Move produces a comparison and a recommendation, and both are revised by revising them. The point of no return is Move 28, where a power commitment is signed, and Move 30, where a term is. Until then, changing your mind costs the time spent gathering quotations. Keep the comparison sheet and every quotation in source control, so the reasoning can be restored when somebody asks in a year why the estate landed where it did.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 weeks | 2 weeks |

## What you can turn off
Nothing yet. This Move only spends money on quotations, which are free, and on the time to read them, which is not.
