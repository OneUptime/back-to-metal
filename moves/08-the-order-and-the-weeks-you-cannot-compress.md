# 08 · The order, and the weeks you cannot compress

**Layer:** Buy · **Leaving:** Provider-assigned addresses and managed transit · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Everything with a lead time goes on one order this afternoon, so the queues run beside each other instead of one after another.

## Leaving from
- **AWS:** Elastic IP and Direct Connect — the cross-connect authorisation expires ninety days after issue, and an Elastic IP bills on after its instance is gone.
- **Google Cloud:** external IP and Cloud Interconnect — the partner variant hides the physical layer, so there is no cross-connect to order and capacity comes from a fixed list.
- **Azure:** Public IP and ExpressRoute — the circuit bills from creation, before the carrier has provisioned anything against its service key.

## Why this works
Every other stage of this migration is work you control. This one is queueing, and the only thing you control is when it starts. A cross-connect and an optic ordered in the same week arrive while the machines are being built; ordered in sequence they add a month each. So the whole list goes in on one afternoon, and you accept paying for two transit paths from the start, because one upstream is a single point of failure with a contract attached. Nothing is installed yet, so every line can be withdrawn up to signature.

## Before you start

**Access**
- The signed facility agreement from Move 07 and its cross-connect price list
- Purchase authority to sign transit and circuits

**Software**
- The switch part numbers from Move 06, for the optic compatibility list
- A written order sheet, one promised date and one name per line

**People**
- A named technical contact the carriers can reach in week three

## The runbook
1. Order the cross-connects the day the facility agreement is countersigned: one per upstream, one for the out-of-band line, one spare. Ask whether the panels to the meet-me room are in place; that decides days against weeks.
2. Take the facility's blended transit for go-live, already in the building, and order a second upstream from a carrier on a different fibre route to run beside it. On the facility's own addresses that second circuit buys a price and a path to grow into rather than a failover, because only the facility's transit routes to you; it becomes a failover the day you announce your own prefix to both.
3. Take a /24 or a /25 and IPv6 from the facility. Your own autonomous system number can wait until a second site earns its eight weeks of registry paperwork. Rented space is a renumbering you may do twice.
4. Order the out-of-band line: a small separate circuit, or a mobile router. It is the cheapest item here and the one that matters at three in the morning.
5. Order optics and cables from the switch vendor's supported list, twenty per cent over the port count. Then chase the order sheet weekly.

## Operator's notes
- **Swap:** Buy every line from the facility on one invoice. It costs more per megabit and takes four vendors off the critical path.
- **Do it faster:** Ask for the authorisation templates before the agreement is countersigned; no queue starts until they are lodged.
- **Watch out:** A cloud's interconnect paperwork expires if the cross-connect is not done inside ninety days, and it is re-issued rather than extended.
- **Leftovers:** The blended transit stays on the invoice until your own circuit has carried a full month including a peak.

## Rollback
Until a signature this Move is undone by an email. The point of no return is the first signed term, not the first delivery: transit and cross-connects carry minimum terms in months, and a circuit against the wrong cabinet is paid for whether or not it is lit. Keep the quotes in version control, so a position can be restored at renewal.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 4 weeks |

## What you can turn off
Nothing yet — this Move only adds lines. The first it retires is the blended transit, once your own upstream has held a month.
