# 80 · Brokered messaging: JMS, durable subscriptions, your broker

**Layer:** Data · **Leaving:** Managed message brokers · **Risk:** High · **Cutover:** 10 min · **Reversible:** 7 days

> Rebuilds JMS semantics on a broker you run, because durable subscriptions, message selectors and transacted sessions are what neither a stream nor a table replaces.

## Leaving from
- **AWS:** Amazon MQ for ActiveMQ and RabbitMQ — the same brokers you are landing on, which makes this the most direct exit of the three.
- **Google Cloud:** no first-party managed broker — so these readers are already self-hosting or buying from a marketplace vendor, and have the shortest path.
- **Azure:** Service Bus — JMS 2.0 over AMQP only on the premium tier, with the lower tier restricted to an older profile and a reduced feature set.

## Why this works
A broker is not a stream and it is not a table, and the difference is the set of guarantees the application was written against: durable topic subscriptions that accumulate while a consumer is away, message selectors that filter server-side, transacted sessions that commit a receive and a send together. None of those survives a translation into a log-based system without rewriting the application, so this Move rebuilds them on a broker you run. Which broker follows from what is load-bearing: a message-queue broker where the estate is protocol-driven, and the enterprise messaging broker where the older messaging semantics genuinely matter.

## Before you start

**Access**
- The broker configuration exported: queues, topics, subscriptions, selectors and dead-letter settings
- A list of durable subscribers and who owns each, because they cannot be double-consumed

**Software**
- The chosen broker under its cluster operator, at a pinned version, with quorum queues rather than mirrored ones
- The shovel or federation mechanism configured, so the drain is gradual rather than a repoint

**People**
- The owner of every durable subscriber, present for the quiescence window

## The runbook
1. Establish which semantics are actually load-bearing. Durable topic subscriptions, selectors and transacted sessions each decide which broker you land on, and most estates use fewer of them than the configuration suggests.
2. Stand up the destination under its operator at a pinned version, with quorum queues in place of the older mirrored ones. The mirrored form is superseded and behaves worse under partition, so it is not carried across.
3. Recreate the topology: queues, topics, durable subscriptions, selectors, dead-letter destinations and their retry counts. Export first and diff afterwards, because a subscription that is silently missing produces messages that vanish.
4. Set up the shovel or federation link between old and new so that messages drain across rather than being cut over in one step. This is what turns a big-bang repoint into something you can pause.
5. Move producers first and let consumers drain the old broker. In-flight messages are never migrated by hand; they are consumed where they are.
6. Quiesce the durable subscribers for the window. This is the ten minutes: a durable subscription cannot be double-consumed the way a queue can, so its consumer stops on one side before it starts on the other.
7. Keep the source broker for seven days with its topology intact, so a subscriber that turns out to have been missed has somewhere to go back to.

## Operator's notes
- **Swap:** Where the estate is entirely queues with no durable topics or selectors, Move 81's substrate is simpler and cheaper, and this Move can be skipped entirely.
- **Do it faster:** Move one queue family at a time, with the shovel running, rather than the whole broker. Each family is an afternoon and the risk is contained.
- **Watch out:** Message ordering guarantees differ between brokers and between queue types on the same broker. An application that depends on ordering needs the guarantee checked rather than assumed.
- **Leftovers:** The managed broker bills per instance-hour and per storage, and a broker with no consumers still bills. Delete it deliberately after the week.

## Rollback
For seven days the source broker still has its topology, so reverting is repointing producers back and letting the new side drain. Messages already consumed on the new side are not restored to the old one, which is why producers move before consumers rather than after. The point of no return is the deletion of the source broker with its durable subscriptions, which is Part VII. Keep the exported topology so it can be restored onto a rebuilt broker if the migration is aborted.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,640/mo | $120/mo | 93% | 10 min | 2 weeks | 7 days |

## What you can turn off
The managed broker instances and their storage, seven days after the last durable subscriber has moved and stayed moved.
