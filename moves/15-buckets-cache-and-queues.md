# 15 · Buckets, cache and queues

**Layer:** Move · **Leaving:** Managed object storage, Redis and queues · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Objects, cache and queues move by copying to a second place, then changing an endpoint. None of them needs writes stopped.

## Leaving from
- **AWS:** S3, ElastiCache and SQS — SQS now carries a megabyte a message, so a large payload may be sitting inline rather than as a pointer into a bucket.
- **Google Cloud:** Cloud Storage, Memorystore and Pub/Sub — Pub/Sub acknowledges per subscription, so two subscriptions deliver everything twice.
- **Azure:** Blob Storage, Azure Cache for Redis and Service Bus — sessions and duplicate detection begin at the Standard tier; Basic has no topics.

## Why this works
The database is the hard migration; this one runs beside it. Objects, cache and queues can each be written to two places at once, so the work is a copy repeated until the delta is boring, then a configuration change. Writes never stop. The risk is not the bytes but the assumptions in the code: an object store that promised more than the standard did, a cache holding sessions nobody labelled as state, a queue whose visibility timeout the consumer extends. Reading source finds those. Watching a transfer does not.

## Before you start

**Access**
- Read access to every bucket and the managed cache, and write on the Ceph gateway (Move 12)
- The queue inventory: visibility timeouts, dead-letter rules and message size ceilings

**Software**
- `rclone` 1.68 or newer, comparing checksums rather than size and time
- Valkey 8.0 with `valkey-cli`, and NATS JetStream 2.10 with the `nats` command line

**People**
- The owner of each key pattern and each queue consumer: both switches are code changes

## The runbook
1. Sort the object estate by size and last access. Hot buckets move; archive stays, because egress on extracting terabytes exceeds years of its storage fee.
2. Copy the hot buckets with `rclone` onto the Ceph gateway, repeating until a pass takes minutes. A multipart entity tag is a digest of digests: it compares only if part sizes match.
3. Change the endpoint, then run a last `rclone` pass for what was written during the swap. Read the client code for listing order, read-after-write on overwrites, part size.
4. Scan the cache key space by pattern. Patterns with no expiry are sessions, counters and locks — state, not cache — and wait for Move 16. The owner confirms; the rest point at Valkey 8.0, checked with `valkey-cli`, and take a cold start in a quiet hour.
5. Stand up NATS JetStream 2.10 beside the old queues. Make consumers idempotent, then have producers write to both for a day, checking each visibility timeout against a long job.
6. Drain the old queues to zero, watch `nats` take the load, then stop the old consumers. Both copies are retained for thirty days; nothing is deleted.

## Operator's notes
- **Swap:** One small bucket read by one service needs no repeated passes. Copy it once, verify it once.
- **Do it faster:** Start the bulk copy the week the cluster comes up. It is bandwidth, not attention, and the last delta takes an hour.
- **Watch out:** Presigned links issued before the endpoint changed resolve to the cloud until expiry; somebody always set one to a year.
- **Leftovers:** Non-current object versions bill on after the live ones go, and cache nodes bill until the last client moves.

## Rollback
Nothing here is deleted, so backing out is three configuration changes: object endpoint, cache endpoint, broker. Objects written to Ceph afterwards are restored by copying the other way. The point of no return is the first message acknowledged only on the new broker.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $12,800/mo | $1,150/mo | 91% | 0 min | 8 days | — |

## What you can turn off
The cache nodes and the managed queues, after thirty days and a clean billing cycle. The object line shrinks rather than going: the archive stays.
