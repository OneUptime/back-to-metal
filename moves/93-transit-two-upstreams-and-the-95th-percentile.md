# 93 · Transit: two upstreams and the 95th percentile

**Layer:** Edge · **Leaving:** Metered data transfer out and dedicated interconnect · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 30 days

> Buys transit from two upstreams on disjoint paths and reads a 95th-percentile invoice, where sustained rate rather than total bytes sets the bill.

## Leaving from
- **AWS:** metered data transfer out with Direct Connect — port hours plus a per-gigabyte rate, billed on total bytes rather than on rate.
- **Google Cloud:** network service tiers with Interconnect — where the tier itself changes the egress rate, and an unlimited-data plan exists alongside the metered one.
- **Azure:** metered egress with ExpressRoute — port hours plus per-gigabyte, with an unlimited option on some circuit types.

## Why this works
Cloud egress is billed on total bytes, and transit is billed on sustained rate. That single difference reorganises everything: a nightly backup that costs a fortune as bytes costs nothing as rate if it runs off-peak, and a short daily spike that was invisible as bytes sets the price for the whole month. So this Move buys two upstreams on genuinely disjoint paths, sizes the commit against a percentile rather than a peak, and shapes the traffic that would otherwise set that percentile — the nightly backups and the migration pull from Move 53 — off the measured rate.

## Before you start

**Access**
- The cross-connect price list from Move 26 and the address space and network number from Move 91
- Traffic measurements at five-minute resolution, because that is the resolution the invoice uses

**Software**
- Authorisation letters and cross-connect orders prepared, priced from the Move 26 list
- Shaping or scheduling for the backup and migration traffic, in place before the first invoice

**People**
- Whoever will hold the transit contracts, because the commit level is a three-year decision

## The runbook
1. Choose upstreams on genuinely disjoint paths, using the fibre route information gathered in Move 25. Two transit providers sharing a duct are one transit provider with two invoices.
2. Understand the billing before negotiating. The rate is measured in five-minute samples across the month, the top five per cent are discarded, and the highest remaining sample sets the bill. Total volume is almost irrelevant.
3. Size the commit against that measurement rather than against a peak. A commit that is too low costs a punitive overage rate; one that is too high is paid whether or not it is used.
4. Order the cross-connects with their authorisation paperwork, priced from Move 26's list, and remember the ninety-day validity on the cloud on-ramp paperwork noted there.
5. Add an exchange port if the traffic profile justifies it, and be honest about what peering saves: it is usually a meaningful share of traffic and a smaller share of cost, because the transit commit does not fall in proportion.
6. Shape the backup window and the migration pull from Move 53 off the measured rate. This is the single highest-value configuration change in this Move and it is frequently forgotten until the first invoice.
7. Compare the result against the cloud egress bill in your own units. One cloud sells an unlimited-data plan, one sells tiers that change the rate itself, and one charges port hours plus per gigabyte, so the comparison has to be re-expressed rather than read off.

## Operator's notes
- **Swap:** A small reader should buy none of this. A blended-bandwidth port from the facility, with the facility handling the upstreams, is cheaper and adequate below a few hundred megabits, and this Move says so explicitly.
- **Do it faster:** Order the circuits early, in parallel with everything else in this Part. Six to twelve weeks of lead time is normal and nothing depends on them until Move 103.
- **Watch out:** A single burst from a misconfigured job can set the percentile for a whole month. Alert on the rate approaching the commit, not on the monthly total.
- **Leftovers:** The dedicated interconnect from Move 53 stays until Part VII, because the abort path in Move 121 needs it.

## Rollback
Transit contracts have notice periods, so backing out costs the remainder of a term rather than being impossible, and for thirty days the cloud egress path is still carrying everything. The point of no return is the commit level on a signed contract, not the circuit itself. Keep the traffic measurements and the commit arithmetic in source control so the sizing can be restored and re-argued at renewal, when the invoice will look different from the model.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $9,216/mo | $1,800/mo | 80% | 0 min | 2 weeks | 6 to 12 weeks |

## What you can turn off
Nothing yet. Cloud egress carries production until Move 103 moves the traffic.
