# 89 · The serverless estate in four piles

**Layer:** Data · **Leaving:** Managed function-as-a-service and its schedulers · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Triages the function estate into cron, provider-event glue, HTTP handlers that should have been Deployments, and the load-bearing few that need real design.

## Leaving from
- **AWS:** Lambda with EventBridge Scheduler — the largest of the three estates in practice, and the one with the most provider-event glue in it.
- **Google Cloud:** Cloud Functions with Cloud Scheduler — which land on a serverless layer over Kubernetes rather than being rewritten.
- **Azure:** Azure Functions with Timer triggers — an open-source runtime that runs in a container, so this estate has a lift path the other two do not.

## Why this works
A few hundred functions sounds like a migration and is mostly a triage. Four piles: things that run on a schedule, which become cron jobs; glue reacting to provider events, which Move 82 already answered or declared lost; HTTP handlers that should always have been ordinary services, which become deployments; and the load-bearing few that genuinely need per-message scaling. Only the fourth pile needs design, and it needs it here rather than earlier because scale-from-zero on a fixed fleet is a different problem from scale-from-zero on an autoscaler, and Move 69 is where the fleet became fixed.

## Before you start

**Access**
- An inventory of every function with its trigger, its invocation rate and its owner
- The event substrate from Moves 81 and 82, carrying the triggers that survived

**Software**
- An event-driven autoscaler at a pinned version for the per-message pile
- A measured cold-start figure on your own fleet: poll interval plus image pull plus process start

**People**
- The owner of each function, because a third of the estate is usually deletable and only they can say so

## The runbook
1. Triage first and spend a week on it. Four piles, every function in exactly one, with its owner named. This week determines the size of the other five.
2. Convert the scheduled pile to cron jobs. This is mechanical, it is usually a third of the estate, and it finishes in days.
3. Convert the HTTP pile to ordinary deployments. Most of these were services all along and were written as functions because that was the platform, not because the shape fitted.
4. Check the second pile against Move 82. The glue reacting to provider control-plane events either has a replacement there or was written down as lost, and either way it is not new work here.
5. Design the fourth pile properly with the event-driven autoscaler, and measure the scale-from-zero figure honestly on your own fleet: poll interval, image pull and process start. It is slower than the managed platform and knowing the number is what lets somebody decide whether that matters.
6. State what is lost rather than hiding it: per-invocation isolation, automatic retry with a dead-letter destination, and the wall-clock execution limit that quietly forced every handler to be safe to replay. That last one is the property most likely to be missed.
7. Run both for thirty days with the new side handling a share of the traffic, then stop the old.

## Operator's notes
- **Swap:** Where a function estate is small and genuinely bursty, keeping it rented is defensible and belongs on the Move 116 list of things you deliberately keep.
- **Do it faster:** Delete first. Most estates have functions that have not been invoked in a year, and deleting them is faster than migrating them.
- **Watch out:** The execution time limit enforced replay-safety. Once it is gone, a handler that runs for an hour and half-completes is a new class of failure, and the code was never written to survive it.
- **Leftovers:** Function versions, aliases and their logs keep billing after invocations stop, and log retention in particular runs for months.

## Rollback
For thirty days both paths exist and traffic can be shifted back by changing the trigger, with the function versions still deployed. Anything the new side wrote in the interim has to be restored or reconciled by hand, which is why the shift is gradual rather than a switch. The point of no return is the deletion of the function versions, which is Part VII. Keep the triage document, because it is what Move 122 will check against.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,720/mo | $90/mo | 95% | 0 min | 6 weeks | 30 days |

## What you can turn off
Function versions, aliases and their schedulers after thirty days, and their log retention once it has been set down deliberately.
