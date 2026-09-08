# 16 · Postgres, the one that matters

**Layer:** Move · **Leaving:** Managed PostgreSQL · **Risk:** High · **Cutover:** 15 min · **Reversible:** 7 days

> Fifteen minutes of stopped writes, at the end of a week in which the new cluster was caught up, backed up, and restored once on purpose.

## Leaving from
- **AWS:** RDS for PostgreSQL — the default parameter group cannot be edited, so `rds.logical_replication` needs a custom group and a reboot.
- **Google Cloud:** Cloud SQL for PostgreSQL — storage auto-grows to hold retained write-ahead log and never shrinks, so it bills at the high-water mark.
- **Azure:** Database for PostgreSQL flexible server — `CREATE EXTENSION` fails until the name is in the `azure.extensions` allowlist, and anything wanting shared memory needs `shared_preload_libraries` too, which does need a restart.

## Why this works
Nothing here is new except the data. The local NVMe and the object gateway the backups go to both came up in Move 12, that gateway has carried the application's own buckets since Move 15, and the application has run on the cluster since Move 14. CloudNativePG supplies the part nobody wants to write: a primary, two standbys, and an operator that promotes one without a human awake at three in the morning. The copy is a stream, not a dump, so the new cluster is caught up and dull for days before anyone books a window. The rehearsed restore is what makes the fifteen minutes safe.

## Before you start

**Access**
- Logical decoding enabled on the managed instance, with the reboot taken
- Credentials for a bucket on the object gateway from Move 12, separate from the cluster's

**Software**
- CloudNativePG 1.25 or newer, failed over by hand at least once already
- The Barman Cloud plugin for CloudNativePG, pinned, because the operator writes `archive_command` itself and will not take one from you
- `psql` and `pg_dump` no older than the managed server

**People**
- The application owner, present for the window when writes stop

## The runbook
1. List the extensions and roles on the managed instance with `psql`. What exists only on the provider's fork is replaced, re-expressed, or blocks the Move.
2. Copy the schema with `pg_dump --schema-only` onto a CloudNativePG cluster of one primary and two standbys on local NVMe, deferring the biggest indexes.
3. Create the logical replication publication and subscription and let it run for days. Read `pg_stat_subscription` each morning: a stalled subscriber fills the source's disk.
4. Declare the object store as the cluster's backup destination so the Barman Cloud plugin drives it, turn on continuous archiving, watch the first write-ahead log segments arrive in the bucket, and only then take the full backup.
5. Restore that backup into a scratch cluster, replay to a chosen timestamp, and count rows against production. Time it. The cutover waits until this passes.
6. Open the window. Stop writes at the application, wait for lag to reach zero, advance every sequence, promote, repoint, start writes.

## Operator's notes
- **Swap:** Leave the managed instance subscribed to the new cluster for the week, replicating backwards. One more week of the old bill turns rollback into a repoint.
- **Do it faster:** Split the publication into several subscriptions grouped by table size, so the initial copy runs in parallel, not table by table.
- **Watch out:** Replication carries rows only. Sequences, large objects, schema changes and tuned parameters stay behind, and a sequence left at one collides on the first insert.
- **Leftovers:** The replication slot on the source outlives its subscription and retains write-ahead log for a reader that has gone.

## Rollback
Until writes resume, backing out is releasing the pause. The point of no return is the first commit on the new cluster: after that the two have diverged, and going back means replaying those writes or losing them. The managed instance stays up with its backups on for seven days, a copy that can still be restored to a timestamp.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $19,500/mo | $0/mo | 100% | 15 min | 6 days | — |

## What you can turn off
The managed instance, its read replicas and their snapshots, after the seven days and once an invoice shows the line gone.
