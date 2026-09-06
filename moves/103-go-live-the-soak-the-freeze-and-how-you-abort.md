# 103 · Go-live: the soak, the freeze, and how you abort

**Layer:** Edge · **Leaving:** The parallel managed edge: layer-7 balancers and weighted DNS records · **Risk:** High · **Cutover:** 10 min · **Reversible:** 7 days

> Shifts production traffic to your own edge a percentage at a time under a freeze, against abort criteria written before the week began.

## Leaving from
- **AWS:** Route 53 weighted records — sitting in front of the Application Load Balancer, and the mechanism that both shifts the traffic and takes it back.
- **Google Cloud:** Cloud DNS weighted routing — the same shape, in front of the external application load balancer.
- **Azure:** Traffic Manager weighted routing in front of Application Gateway — the same again, with its own probe behaviour.

## Why this works
This is the largest cutover in the book and it is done as a weighted shift rather than a switch, because the way back has to be one record change at every point. Two halves have to be right. The technical half is a synthetic peak that reproduces the failures that only appear under load: connection-tracking exhaustion, ephemeral port limits, name-resolution replica counts and the flow rehash from Move 96. The business half is the one engineers skip: a freeze window, customer notice, a status-page entry, a named person who says go or no-go, and a lowered record lifetime set a week in advance.

## Before you start

**Access**
- The record lifetime lowered a week in advance, so a rollback propagates in minutes rather than hours
- A freeze on unrelated changes for the duration, agreed with everyone who deploys

**Software**
- A synthetic peak that reproduces real traffic shapes at above real volume
- A migration dashboard everybody watches, with the abort criteria as visible thresholds on it

**People**
- A named go and no-go owner, and the on-call rota briefed on what abort looks like

## The runbook
1. Run the synthetic peak against the new edge at above real volume. Look specifically for connection-tracking table exhaustion, ephemeral port limits, name-resolution replica counts under load and the flow rehash from Move 96. These do not appear at any lower volume.
2. Lower the record lifetime a week in advance and confirm it has actually propagated by checking from several networks. A rollback is only as fast as the lifetime clients cached.
3. Write the abort criteria before the week starts, as numbers on the dashboard: error rate above a figure, latency above a figure, any data-path error at all. Somebody who is tired at midnight should be able to read them and act.
4. Open the freeze window, publish the customer notice and the status-page entry, and name the go and no-go owner for the session.
5. Shift a small percentage and hold. Then a larger one, and hold. The holds are the point; a shift with no hold is a switch with extra steps.
6. Expect the ten minutes. There is no write stop, but connections reset across the final weight shifts and a minority of clients ignore the record lifetime entirely. Printing zero here would make the book's largest cutover read as safer than a database audit, which it is not.
7. Hold at full weight for seven days with the managed edge still configured and still paid for, and keep the cost of running both in the programme's numbers rather than hiding it.

## Operator's notes
- **Swap:** Where a customer contract forbids a freeze window, shift during their quiet period at a lower percentage over a longer period. It takes a fortnight instead of a night and it is entirely legitimate.
- **Do it faster:** Do the synthetic peak two weeks early. It is the step that finds real problems and it is the one that gets compressed when the date slips.
- **Watch out:** A minority of clients cache records far beyond their stated lifetime, including some corporate resolvers and some mobile stacks. The old edge must keep working during the whole window for exactly this reason.
- **Leftovers:** Both edges bill for the full seven days, and that overlap is a real line in Move 120's cost model rather than a rounding error.

## Rollback
Setting the weight back to zero returns every new connection to the managed edge within the record lifetime, which is why it was lowered a week in advance. For seven days that path stays fully configured. The point of no return is the deletion of the managed balancer and its rules, which is Part VII. If anything in the data path failed rather than the traffic path, the way back is the restore from Move 74 rather than a weight change, and the abort criteria should say so explicitly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,410/mo | $0/mo | 100% | 10 min | 1 week | 7 days |

## What you can turn off
The managed layer-7 balancer and its listener rules, seven days after full weight, once the record lifetime has been restored to a normal value.
