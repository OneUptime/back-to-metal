# 15 · Buckets, cache and queues

**Layer:** Move · **Leaving:** Managed object storage, Redis and queues · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Copying bytes is the easy part. A live move also needs an ordered record of changes, retryable publishing and consumers that recognise the same job twice.

## Leaving from
- **AWS:** S3, ElastiCache and SQS — SQS now carries a megabyte a message, so a large payload may be sitting inline rather than as a pointer into a bucket.
- **Google Cloud:** Cloud Storage, Memorystore and Pub/Sub — acknowledgements belong to a subscription; a second matching subscription receives its own copy, not a share of the first one's work.
- **Azure:** Blob Storage, Azure Cache for Redis and Service Bus — sessions and duplicate detection begin at the Standard tier; Basic has no topics.

## Why this works
Objects, disposable cache and queues can move while the application runs, but copying and changing endpoints alone cannot guarantee it. The zero-minute reference requires ordered object-change replay and durable queue publishing with shared deduplication. If the application cannot supply those, retain the service or rehearse a separate write-stop window. Sessions and locks remain state even when they expire. The owner must account for them before this Move is complete.

## Before you start

**Access**
- Read access to every bucket and the managed cache, and write on the Ceph gateway (Move 12)
- The queue inventory: ordering, visibility timeouts, dead-letter rules, retention and message size ceilings

**Software**
- `rclone` 1.75.1, including `rclone check --download` where the stores share no usable checksum
- Valkey 8.0.11 with `valkey-cli`, and NATS JetStream 2.12.15 with the `nats` command line

**People**
- The owner of each key pattern and each queue consumer: both switches are code changes

## The runbook
1. Sort the object estate by size and last access. Compare retrieval and transfer costs with continued storage before retaining an archive. Inventory versions, retention locks, metadata and access policies; copying current objects does not migrate those contracts.
2. Before copying, capture every object change in a durable application journal, including overwrites and deletions with version ordering. Keep the source authoritative. Bulk-copy with `rclone` to Ceph, then replay the journal in order; verify content with a common checksum or `rclone check --download`. A multipart or encrypted object's entity tag is not a portable content checksum.
3. Test client listing, overwrites and multipart operations. Rehearse the writer handoff and reverse replay. Once caught up, route every writer through the journal to Ceph, then switch reads. Fence old writers, including signed uploads. Keep journalling through the return window; a final blind source-to-destination copy could overwrite new data.
4. Classify cache keys with their owner, regardless of expiry. Only values safely rebuilt from the authoritative database take a cold start on Valkey 8.0.11, checked with `valkey-cli`. Retain sessions, counters and locks until a separate state-transfer or expiry-and-reissue plan passes; Move 16's PostgreSQL replication does not move them.
5. Stand up NATS JetStream 2.12.15 beside the old queues. Use a durable outbox to retry each publish until both brokers acknowledge it, with one stable job identifier. Deduplicate effects in the shared authoritative datastore. Test ordering, payload limits, dead-letter handling and acknowledgement extensions on long jobs; broker-local deduplication cannot cover two brokers.
6. Switch producers to JetStream, finish old publish retries, and drain visible, delayed and in-flight work before stopping old consumers. Watch delivery with `nats`. Retain payloads and processing records independently for thirty days: SQS retention is at most fourteen days, and acknowledged messages are not a backup.

## Operator's notes
- **Swap:** An immutable bucket needs no change journal: copy it once and verify it before switching readers.
- **Do it faster:** Begin the bulk transfer as soon as the change journal is reliable; measure its duration from bytes and available bandwidth.
- **Watch out:** Signed links still target their original provider. S3 Signature Version 4 URLs last at most seven days, often less with temporary credentials; audit actual expiry and revoke old upload paths before handing off writers.
- **Leftovers:** Non-current object versions bill on after the live ones go, and cache nodes bill until the last client moves.

## Rollback
For objects, fence writers, restore new objects and replay ordered changes from the journal back to the source, verify them, then switch endpoints. Rebuild disposable cache from its authority; never re-enable a stale session or lock store. For queues, stop dispatch, restore unprocessed payloads from the retained outbox and reconcile processing records before resuming the old broker. An acknowledged job may already have changed the database or charged a customer. The point of no return for a configuration-only return is the first write or job processed only at the destination; thirty days of retained evidence supports recovery, not automatic reversal of effects.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $12,800/mo | $1,150/mo | 91% | 0 min | 8 days | — |

## What you can turn off
The cache nodes and managed queues, after all stateful key patterns have a home and the thirty-day return window ends; confirm their charges disappear on the next invoice. Any retained archive continues to bill and must leave before Move 20 closes its account.
