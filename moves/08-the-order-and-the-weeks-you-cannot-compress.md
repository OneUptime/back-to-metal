# 08 · The order, and the weeks you cannot compress

**Layer:** Buy · **Leaving:** Provider-assigned addresses and managed transit · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Everything with a lead time goes on one order this afternoon, so the queues run beside each other instead of one after another.

## Leaving from
- **AWS:** Elastic IP and Direct Connect — the cross-connect authorisation expires ninety days after issue, and an Elastic IP bills on after its instance is gone.
- **Google Cloud:** external IP and Cloud Interconnect — Partner Interconnect uses a provider's connection to Google; order access to that provider separately, with capacity from the supported list.
- **Azure:** Public IP and ExpressRoute — the circuit bills from creation, before the carrier has provisioned anything against its service key.

## Why this works
Orders have lead times that engineering effort cannot shorten. Put cross-connects, optics and carrier access into parallel queues while the machines are being built. The four-week wait below is a planning allowance; replace it with the longest confirmed delivery date. Pay for two transit paths when they can carry your addresses, and record any initial dependence on facility transit. Cancellation rights come from each quote and signed term, not from whether anything has been installed.

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
3. Take the required IPv4 space and IPv6 from the facility. If independent upstream failover is required at go-live, arrange a portable prefix, routing authorisation and an autonomous system number now; a second site is not required. Confirm both carriers accept the prefix before ordering. Facility-assigned space may require renumbering later.
4. Order the out-of-band line: a small separate circuit, or a mobile router. It is the cheapest item here and the one that matters at three in the morning.
5. Order optics and cables from the switch vendor's supported list, twenty per cent over the port count. Then chase the order sheet weekly.

## Operator's notes
- **Swap:** Buy every line from the facility on one invoice. It costs more per megabit and takes four vendors off the critical path.
- **Do it faster:** Ask for the authorisation templates before the agreement is countersigned; no queue starts until they are lodged.
- **Watch out:** The AWS Direct Connect authorisation expires after ninety days; download a renewed letter if installation slips. Other providers have their own terms.
- **Leftovers:** Keep blended transit while it is the only route to facility-assigned addresses. Retire it only after replacement addressing and redundant transit pass their own soak.

## Rollback
Until a signature this Move is undone by an email. The point of no return is the first signed term, not the first delivery: transit and cross-connects carry minimum terms in months, and a circuit against the wrong cabinet is paid for whether or not it is lit. Keep the quotes in version control, so a position can be restored at renewal.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 4 weeks |

## What you can turn off
Nothing yet. Blended transit can go only after its addresses and routing have been replaced, both remaining paths pass failover, and a full month's traffic has stayed healthy.
