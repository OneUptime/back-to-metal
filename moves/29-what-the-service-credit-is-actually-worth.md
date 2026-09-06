# 29 · What the service credit is actually worth

**Layer:** Site · **Leaving:** Cloud service-level agreements and their credits · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Until the schedule is signed

> Establishes what the facility owes when it fails, which is a capped credit, and redirects the negotiation onto the derate, the power increase and the exit.

## Leaving from
- **AWS:** the EC2 and EKS service level agreements — a monthly percentage and a credit, claimable by ticket, capped at a share of the bill.
- **Google Cloud:** its compute service level agreements — the same structure, with the same claim window and the same cap.
- **Azure:** its virtual machine service level agreements — the same again, with credits expressed as a percentage of the monthly charge for the affected service.

## Why this works
Everybody negotiates the service level and almost nobody reads what it pays. Facility agreements follow the same shape as the cloud ones you are leaving: a commitment on power and cooling, a set of exclusions, a window inside which a claim must be filed, and a credit that is the sole and exclusive remedy, capped at a fraction of one month's recurring charge. That credit will never approach the cost of an outage, and no amount of negotiation will make it. Establishing that early is useful, because it frees the negotiating hours for the three clauses that do change your position: the derate, the mid-term power increase and the exit.

## Before you start

**Access**
- The draft service level schedule and the exclusions attached to it
- Your own cost of an hour of downtime, calculated rather than asserted

**Software**
- The claim procedure written out as a runbook, including the deadline, because credits expire unclaimed
- A note of the measurement point for each commitment, since it decides whether a failure counts

**People**
- Whoever will actually file a claim at eight in the morning after a bad night

## The runbook
1. Read the commitment and find its measurement point. Power measured at the feed and power measured at the cabinet are different commitments, and cooling measured at the unit return is not the same as cooling measured at your inlet.
2. List the exclusions. Planned maintenance, force majeure and anything caused by your own equipment are standard, and together they remove most of the events you would want to claim for.
3. Find the cap and the claim window. The credit is almost always limited to a share of one month's recurring charge and the window is often as short as thirty days. Both are usually non-negotiable.
4. Calculate what the maximum possible credit would be for your estate, in currency, and put that number next to your cost of an hour of downtime. The comparison is the whole argument of this Move.
5. Redirect the negotiation. Spend the hours on the derate from Move 28, on the written right to increase power, and on the exit terms in Move 30. Those three change what the agreement is worth; the credit does not.
6. Write the claim procedure down anyway, with the deadline in the calendar. A credit you are entitled to and do not claim is a credit you have donated.

## Operator's notes
- **Swap:** Where an outage genuinely would be catastrophic, the answer is the second site in Move 24 or the rehearsed restore in Move 115, not a better credit. Insurance and architecture are the tools here; contract remedies are not.
- **Do it faster:** Ask the facility directly what the largest credit it has ever paid was. The answer, or the refusal to answer, tells you what you need to know.
- **Watch out:** Some schedules require you to prove the outage with your own monitoring, at your own measurement point. If so, Move 114 needs to be collecting that data from the day the cabinet is live.
- **Leftovers:** The cloud service level agreements keep applying to whatever is still running there. Do not stop claiming against them while the migration is in flight.

## Rollback
Nothing here binds you until the schedule is signed with the rest of the agreement in Move 30, and until then every term is a draft. The point of no return is that signature, after which the remedy for a failure is whatever the document says it is. Keep the schedule, the exclusions and your downtime cost calculation in source control, so the analysis can be restored and re-run at renewal rather than done again from nothing.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing. This Move saves negotiating hours rather than money, and spends them somewhere better.
