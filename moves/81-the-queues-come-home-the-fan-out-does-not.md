# 81 · The queues come home, the fan-out does not

**Layer:** Data · **Leaving:** Managed queues and topic fan-out · **Risk:** High · **Cutover:** 0 min · **Reversible:** 14 days

> Brings managed queues and internal topic fan-out home to NATS JetStream or Postgres by drain-and-switch, and keeps renting mobile push and SMS.

## Leaving from
- **AWS:** SQS and SNS — separate queue and topic products, with a visibility timeout and a redrive policy that are load-bearing and undocumented in most codebases.
- **Google Cloud:** Pub/Sub — one subscription model with acknowledgement deadlines, so the semantics map differently rather than directly.
- **Azure:** Storage queues and Service Bus queues — two products with different durability, and applications that frequently use both without anyone noticing.

## Why this works
The semantics are the migration. Visibility timeout and its extension, at-least-once delivery, the retention ceiling, message grouping and the redrive policy are all load-bearing in real applications and documented in almost none of them, and the three clouds do not agree on any of them. So the audit comes first. After that the mechanics are simple: producers switch to the new substrate and consumers drain the old queue until it is empty. In-flight messages are never migrated, which is exactly why the reversibility window is the source queue's own retention period rather than a number this book chose.

## Before you start

**Access**
- Every queue and topic listed with its settings, including the redrive policies nobody configured deliberately
- The durable half of the key space handed over by Move 79

**Software**
- The chosen substrate: a permissively licensed streaming server for high volume, or the database for low
- Consumers made idempotent, because at-least-once means at-least-once on both sides

**People**
- The owner of each producer and each consumer, because the switch is a code change on both

## The runbook
1. Audit the semantics per queue: visibility timeout and whether the consumer extends it, retention, ordering or grouping, and the redrive policy. Write down which of these the application actually depends on rather than which are configured.
2. Pick the substrate per workload. High-volume, high-fan-out work goes to the streaming server; low-volume work goes into the database you already run, which is a queue with transactions and one fewer system to operate.
3. Take the durable half of the key space from Move 79 — sessions, locks, counters, the job queue — and place each one deliberately. A job queue in a cache was always a queue in the wrong place.
4. Make every consumer idempotent before anything moves. Both sides deliver at least once and a migration doubles the opportunities to prove it.
5. Switch producers to the new substrate and leave consumers running against both. The old queue drains and then stays empty, which is the signal that the switch is complete.
6. Keep mobile push and SMS bought. Repatriating those means becoming a messaging provider badly, and the certification and deliverability work is a business rather than a migration.
7. Wait out the source's retention period before deleting anything, because that period is the reversibility window this Move claims.

## Operator's notes
- **Swap:** For a queue doing fewer than a few messages a second, a table in the database with a locking select is genuinely the right answer and removes a whole system from the estate.
- **Do it faster:** Move the queues with a single producer and a single consumer first. They are an hour each and they build the pattern.
- **Watch out:** A dead-letter queue on the old side will keep receiving failures from consumers that have not moved. Check it is empty before deleting anything, because it is where the messages you lost are sitting.
- **Leftovers:** Queue services bill per request, so a queue nobody uses costs almost nothing and is easy to forget. Move 120 will find them in the billing data.

## Rollback
For the length of the source's retention, producers are switched back and consumers drain the new substrate instead. Messages already consumed are not restored to the old queue, so the order — producers first, consumers last — is what makes the rollback clean. The point of no return is the expiry of that retention window, after which an unconsumed message on the old side is gone. Verify the dead-letter queues on both sides are empty before calling the Move finished.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $840/mo | $50/mo | 94% | 0 min | 2 weeks | 14 days |

## What you can turn off
The queue and topic resources, once both dead-letter queues are empty and the source retention window has passed. Push and SMS stay bought.
