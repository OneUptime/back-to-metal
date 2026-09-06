# 82 · The event bus, and the control-plane events that stop arriving

**Layer:** Data · **Leaving:** Managed event buses and provider control-plane events · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 7 days

> Rebuilds custom buses, schema registry, archive and replay on a broker you own, and names the control-plane events that stop arriving with the account.

## Leaving from
- **AWS:** EventBridge — custom buses, cross-account rules, content-based filtering, a schema registry and an event archive with replay.
- **Google Cloud:** Eventarc with Pub/Sub — the same idea assembled from two services, with the filtering expressed differently.
- **Azure:** Event Grid — the same again, with system topics carrying the provider's own resource events.

## Why this works
There are two halves here and only one of them has a replacement. The custom half — your own buses, your own rules, your own schemas — moves onto the substrate from Move 81: rules become subjects, the registry becomes a self-hosted one, and archive and replay become a retained stream rather than a product feature. The other half is the provider's own control-plane events: object-created notifications, database events, resource-lifecycle events, audit routing. Those stop arriving because the resources that emit them are the ones being deleted, and pretending otherwise is how a migration silently loses an automation nobody remembered.

## Before you start

**Access**
- Every rule, bus and subscription exported, including the cross-account ones that nobody in your account can see
- The substrate from Move 81, running and carrying real traffic

**Software**
- A self-hosted schema registry, and a retained stream configured for the archive and replay use
- Bucket notifications on your own object store, which cover the storage half of the control-plane events

**People**
- The owner of each rule, because a rule with no owner is either critical or dead and only they can say which

## The runbook
1. Separate the two halves before doing anything. Custom application events move; provider control-plane events do not, and the second list is the one that needs decisions rather than work.
2. Convert each rule into a subject or topic on the substrate from Move 81, keeping the content-based filtering where the substrate supports it and moving it into the consumer where it does not.
3. Stand up a schema registry you run, and migrate the schemas. A registry is cheap to run and expensive to be without once producers and consumers are versioned independently.
4. Replace archive and replay with a retained stream. This is a capacity decision rather than a feature: retention costs storage, and the retention you choose is the replay window you have.
5. Wire your own object store's bucket notifications for the storage half of the control-plane events. That covers object-created and object-removed, which is most of what people actually used.
6. Use cluster events plus the alerting path from Move 62 for the resource-lifecycle half. It is not the same thing and it covers the same need for anything running on your own hardware.
7. Write down what is genuinely lost, with the automation it fed. An honest list of three lost event types beats an assumption that everything was covered.

## Operator's notes
- **Swap:** For a handful of rules, a direct call from the producer to the consumer is simpler than a bus and removes a system. Buses earn their place when the number of consumers per event is genuinely unknown.
- **Do it faster:** Convert the rules with the most consumers first. They prove the substrate and they are the ones where the bus is actually earning its keep.
- **Watch out:** Cross-account rules are invisible from the receiving side. Ask the other account's owner rather than reading your own configuration, or the rule will be discovered when it stops firing.
- **Leftovers:** Event archives keep billing for their retention after the bus stops receiving. Reduce the retention explicitly rather than waiting for it to lapse.

## Rollback
For seven days both paths exist, so reverting is repointing producers back at the managed bus. Events consumed on the new side are not restored to the old archive, which is why the retained stream is configured before producers move. The point of no return is the deletion of the archive, which is Part VII. Keep the exported rules in source control so the topology can be restored, and keep the lost-events list where Move 119's auditor can read it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $460/mo | $30/mo | 93% | 0 min | 2 weeks | 7 days |

## What you can turn off
Custom buses and their rules after seven days. The provider's system events stop on their own when the resources behind them go.
