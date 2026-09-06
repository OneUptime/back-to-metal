# 90 · Orchestrated workflows: the dated exception

**Layer:** Data · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Argo Workflows and Temporal do not replace the provider service integrations, so low-frequency state machines keep running against a budgeted and dated rewrite.

## Leaving from
- **AWS:** Step Functions — a few dozen direct service integrations, which is the smallest of the three catalogues and still not nothing.
- **Google Cloud:** Workflows — a connector library covering most of the provider's own services.
- **Azure:** Logic Apps — a connector catalogue in the hundreds, which is the single largest retention argument in this Part.

## Why this works
State machines are not the problem; the service integrations are. A workflow that calls twelve provider services directly, with retries and error handling expressed declaratively, has no equivalent because the twelve services are what it calls. So the honest answer is a dated exception: inventory the state machines, price the rewrite properly against the two open landings, and write the ones that stay into the account-closure schedule with a name and a date beside each. That gives Move 122 something concrete to discharge instead of a vague dependency it discovers at the end.

## Before you start

**Access**
- Every state machine listed with its invocation frequency, its criticality and its owner
- The account-closure schedule from Move 122, ready to receive dated entries

**Software**
- The two landings priced honestly: a workflow engine for graph-shaped batch, and a durable execution framework for long-running state
- A rewrite estimate per machine, in days, produced by somebody who has read the definition

**People**
- The owner of each state machine and whoever holds the budget for the rewrite

## The runbook
1. Inventory the state machines by frequency and criticality. Most estates find that a handful run constantly and the rest run monthly, and only the first group justifies a rewrite on cost.
2. Count the provider service integrations in each. This number, more than the size of the definition, predicts the rewrite cost, because each integration becomes code you write and maintain.
3. Price the two landings against the estate. A workflow engine suits graph-shaped batch work; a durable execution framework suits long-running business state. Both are openly licensed, which is why they are the landings.
4. Do not hand-roll a state machine on a queue. It is the obvious shortcut, it works for a fortnight, and then somebody has to reimplement retries, timeouts and idempotency badly.
5. Rewrite the ones that justify it, and leave the rest running with a named owner and a date. The date is the point of this Move.
6. Write the retained machines into the account-closure schedule so Move 122 has a concrete list with dates rather than an open dependency.
7. Review the list quarterly and shorten it, because the retention argument weakens every time one of the twelve services it calls is turned off elsewhere in the programme.

## Operator's notes
- **Swap:** Where a state machine calls only your own services, it converts almost directly and should be moved now rather than dated. The integrations are the whole difficulty.
- **Do it faster:** Delete the state machines that have not run in a year. There are always some, and they are on the list of things blocking account closure.
- **Watch out:** A retained state machine keeps an account alive, and an account that is alive has credentials, permissions and a bill. Move 122 has to know about every one of these.
- **Leftovers:** Workflow services bill per state transition, so a low-frequency machine costs almost nothing and is easy to leave running forever. That is the failure this Move exists to prevent.

## Rollback
Nothing is migrated here that cannot be reverted by re-enabling the original state machine, which is still there. There is no point of no return in this Move at all; it is an inventory, a price and a set of dates. Keep the inventory in source control and re-run it quarterly, so the retained list can be restored, compared and shortened rather than quietly growing.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $290/mo | $180/mo | 38% | 0 min | 2 weeks | — |

## What you can turn off
The state machines that have not run in a year, today. The rest stay against a written date, and Move 122 collects them.
