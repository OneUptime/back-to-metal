# 24 · The second site you are not building this year

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Refuses a second site in year one, names the three conditions that change the answer, and buys a costed restore into rented metal in another city instead.

## Leaving from
- **AWS:** multi-Region architectures and cross-Region replication — a second site was a configuration option, priced per gigabyte rather than per building.
- **Google Cloud:** multi-region resources and dual-region storage — the same, with some services spanning regions by default so nobody had to design it.
- **Azure:** paired regions and geo-redundant storage — again a second site as a checkbox, which is why its real cost is so widely underestimated.

## Why this works
A second site doubles the facility bill, the cabling, the spares pool and the change surface, and it does so in exchange for protection against a failure that a well-chosen facility already makes rare. In year one, when the team is learning to run one site, a second one usually makes things less reliable rather than more. The defensible answer for most estates is one good site plus a costed and rehearsed restore into rented machines in another city — which is cheap, which can be tested every quarter, and which does not require anyone to be woken up to fail over.

## Before you start

**Access**
- The comparison from Move 22, including the rented-metal option and its price per machine per month
- Whatever contractual or regulatory commitments exist about resilience, read rather than remembered

**Software**
- A recovery objective for each service, expressed as time to restore and acceptable data loss
- A price for the rented standby estate at the size it would need to be, not at the size of production

**People**
- Whoever signs customer commitments, since one of the three conditions is a promise already made

## The runbook
1. Name the three conditions under which a second site is built in year one: a regulator that requires it, a signed customer commitment that names it, or revenue per hour of downtime that exceeds the annual cost of the second site. If none holds, the answer is no and it is written down as a decision rather than a delay.
2. Dispose of the two false second sites explicitly. A second cabinet in the same building is not a second site, and a second building on the same substation and the same fibre route is not one either. Both are common and both are sold as resilience.
3. Cost the alternative properly: rented machines in another city, sized to carry a reduced service rather than full production, with the data arriving there continuously and a rehearsed restore procedure. Move 115 builds it and drills it.
4. Set the recovery objective per service, and be honest about which services genuinely need to come back in an hour and which can wait until the morning. Most estates find the list is shorter than expected.
5. Put the second site in the budget for the year in which one of the three conditions becomes true, with the trigger written next to it. That turns a refusal into a plan.
6. Review the decision annually, on a date, rather than whenever somebody raises it in an incident review.

## Operator's notes
- **Swap:** Where a customer commitment is the trigger, price the commitment. Sometimes the contract can be renegotiated for less than the second site costs, and nobody has ever asked.
- **Do it faster:** Rented machines in a different city can be provisioned in a day. Buying a small standby estate now and drilling against it beats designing a second site for a year.
- **Watch out:** A second site that is never exercised is not a second site. If nothing runs there routinely, it will not work when it is needed, and the drill in Move 115 is the only thing that makes it real.
- **Leftovers:** The provider's cross-region replication keeps billing while you decide. Leave it until Part V has moved the data, then stop it deliberately.

## Rollback
This Move produces a decision and a trigger, both of which are revised by revising them. The point of no return is signing a second facility agreement in Move 30, which commits a term and a monthly charge for years. Until that signature the second site remains a budget line. Keep the decision, the conditions and the recovery objectives in source control so the reasoning can be restored when the question is reopened, as it will be after the first incident.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. Cross-region replication in the cloud stays until Part V has moved the data it protects.
