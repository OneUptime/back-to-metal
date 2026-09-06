# 83 · Kafka off the managed broker

**Layer:** Data · **Leaving:** Managed Kafka · **Risk:** High · **Cutover:** 0 min · **Reversible:** 7 days

> Deletes the Kafka clusters that were never Kafka, then mirrors the rest onto Strimzi with a written per-topic decision to replay or to skip.

## Leaving from
- **AWS:** MSK — an identity-backed authentication mechanism on every client, so every client configuration changes.
- **Google Cloud:** Managed Service for Apache Kafka — a standard authentication profile, which is the closest of the three to what you will run.
- **Azure:** Event Hubs with its Kafka endpoint — a protocol endpoint on a product that is not Kafka underneath and does not support log compaction, which frequently decides the answer for this reader.

## Why this works
A large share of managed Kafka clusters are not doing anything Kafka is for. So this Move opens with a test rather than a migration: partition count, retention, real throughput, whether anybody replays, and whether ordering is load-bearing. Clusters that fail that test become a queue on the substrate from Move 81 and are deleted, which is the cheapest outcome available. For what genuinely stays Kafka, the landing is the operator on the current architecture without the old coordination service, and the mirroring tool carries the topics — with one honest caveat that governs everything else.

## Before you start

**Access**
- Topic-level metrics: partitions, retention, throughput and consumer group lag over a representative fortnight
- The link from Move 53, sized for the mirroring throughput rather than the steady state

**Software**
- The Kafka operator at a pinned version, on the current coordination architecture rather than the removed one
- The mirroring tool configured per topic, with a written decision to replay or to skip for each

**People**
- The owner of every consumer group, because offsets are the part that does not travel cleanly

## The runbook
1. Run the test first. Partitions, retention, throughput, replay, ordering. Write the answer per cluster and delete the ones that were never Kafka, moving them to the substrate from Move 81.
2. Stand up the destination under its operator at a pinned version, on the current coordination architecture. The separate coordination service was removed from Kafka in the 4.0 release and there is no reason to reproduce it.
3. State the caveat before configuring anything: consumer offsets are cluster-local and the mirroring tool's translation of them is approximate. Consumers are made idempotent before a single topic is mirrored, and transactional producers do not survive the boundary at all.
4. Decide per topic whether history is replayed or skipped. A topic used as a queue does not need its history; a topic used as a log does, and mirroring a month of it is a schedule item rather than a footnote.
5. Change every client's authentication configuration. This differs on each cloud — an identity-backed mechanism on one, a standard profile on another, and a protocol endpoint on the third — and it is a change to every producer and consumer.
6. Mirror, then move consumers group by group, watching lag on both sides. Producers move last for a log-shaped topic and first for a queue-shaped one, which is the opposite of Move 81 and worth stating explicitly.
7. Keep the source for seven days with the mirror still running in case a consumer group was missed.

## Operator's notes
- **Swap:** Where the source is a protocol endpoint on a product that is not Kafka, log compaction does not exist there, so any compacted topic must be rebuilt rather than mirrored. That usually decides the whole migration for that reader.
- **Do it faster:** Move the queue-shaped topics first with no history. They are quick, they build confidence, and they shrink the cluster you have to mirror.
- **Watch out:** Partition counts are not freely changeable after the fact for keyed topics, because changing them changes which partition a key lands in. Choose the destination partition count deliberately.
- **Leftovers:** The managed cluster bills per broker-hour and per gigabyte of storage, and storage keeps billing for the retention period after production stops.

## Rollback
For seven days the mirror runs and the source retains its data, so a consumer group can be pointed back and will find its messages. Offsets will not be exact, which is why idempotent consumers are a prerequisite rather than a recommendation. The point of no return is the expiry of the source's retention, after which the history exists only on your side. Verify a replay from the new cluster before that date rather than assuming the mirrored data is complete, because after it the only way to restore a topic is from whatever produced it in the first place.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,180/mo | $240/mo | 92% | 0 min | 3 weeks | 7 days |

## What you can turn off
The managed brokers and their storage, seven days after the last consumer group moved and a replay from your own cluster has been verified.
