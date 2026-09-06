# 116 · Capacity planning, and the cloud footprint you keep

**Layer:** Watch · **Leaving:** On-demand elasticity and managed cluster autoscaling (keeping a minimal tested overflow) · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Counts headroom per failure domain so it holds with the largest node gone, and keeps a tested cloud overflow where owning the peak costs more than renting it.

## Leaving from
- **AWS:** on-demand instances and Auto Scaling — capacity in ninety seconds, which is what you are choosing to keep a small amount of.
- **Google Cloud:** on-demand instances with managed instance groups — the same, and the least conditional exit terms if you do leave entirely.
- **Azure:** on-demand instances with scale sets — the same again, with exit terms that require the subscription to close.

## Why this works
On your own hardware, headroom is a purchase made a quarter in advance, so it has to be counted properly: per failure domain, and held so that it still stands with the largest machine removed. That is a stricter test than an average utilisation figure and it is the one that matters during a rack failure. The second half of this Move is deliberate retention. A tested overflow target, occasional accelerators and the appliances that did not become workloads in Move 70 are all legitimately kept — and keeping them costs more than the invoice, because the free-egress-on-exit programmes generally require a full departure.

## Before you start

**Access**
- A year of real load on your own estate, because a capacity model built on three months of migration traffic is fiction
- The procurement lead times from Move 17, which turn adding capacity into a quarterly decision

**Software**
- A headroom model per failure domain, tested with the largest node removed
- A pre-built overflow target in the cloud, deployable and tested rather than described

**People**
- Whoever approves capital, because the model's output is a purchase order placed a quarter early

## The runbook
1. Build the headroom model against real failure domains from Move 42 rather than against the fleet total. A cluster with twenty per cent headroom spread evenly has none in the rack that just failed.
2. Test the model by removing the largest node on paper. If the remaining capacity cannot carry production, the headroom figure is wrong regardless of what the average says.
3. Add the procurement lead time. A model that says you need a machine in six weeks and a supplier who needs twelve is a model that produces an outage on schedule.
4. Decide the retained cloud footprint deliberately and list it: a pre-built overflow target, accelerators used intermittently, and the appliances from Move 70 that stayed rented.
5. Test the overflow quarterly or delete it honestly. An untested overflow is a line on an invoice and a false sense of safety, and the second is worse than the first.
6. Resolve the egress conflict now rather than in Move 122. The free-egress-on-exit programmes generally require full departure, so a retained footprint may cost you the credit — and that trade should be made deliberately with the numbers in front of you.
7. Refresh the model annually and review it quarterly. A day a quarter keeps it honest.

## Operator's notes
- **Swap:** Where the load is genuinely predictable, retaining nothing is the cheapest and cleanest answer, and it makes Move 122 much simpler.
- **Do it faster:** Build the model after a year of real load, not before. Anything earlier is measuring the migration rather than the business.
- **Watch out:** An overflow target that has never been used at scale will fail at scale. Quarterly testing means running real traffic through it, not confirming it deploys.
- **Leftovers:** The retained footprint keeps a whole account alive, with credentials, permissions and an audit obligation attached. Move 119 and Move 122 both inherit that.

## Rollback
The model is revised by revising it, and the retained footprint is deleted whenever you decide to. There is no point of no return in this Move. What is not reversible is under-buying against a twelve-week lead time, which is why the model is built early and reviewed often. Keep it in source control so a previous year's assumptions can be restored and compared against what actually happened.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $56,513/mo | $1,900/mo | 97% | 0 min | 1 week | — |

## What you can turn off
Everything except the retained list, and the retained list is short, written down and tested quarterly.
