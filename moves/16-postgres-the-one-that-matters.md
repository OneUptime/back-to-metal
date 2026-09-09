# 16 · Postgres, the one that matters

**Layer:** Move · **Leaving:** Managed PostgreSQL · **Risk:** High · **Cutover:** 15 min · **Reversible:** 7 days

> Fifteen minutes of stopped writes, at the end of a week in which the new cluster was caught up, backed up, and restored once on purpose.

## Leaving from
- **AWS:** RDS for PostgreSQL — the default parameter group cannot be edited, so `rds.logical_replication` needs a custom group and a reboot.
- **Google Cloud:** Cloud SQL for PostgreSQL — storage auto-grows to hold retained write-ahead log and never shrinks, so it bills at the high-water mark.
- **Azure:** Database for PostgreSQL flexible server — `CREATE EXTENSION` fails until the name is in the `azure.extensions` allowlist, and anything wanting shared memory needs `shared_preload_libraries` too, which does need a restart.

## Why this works
The application already runs on your hardware from Move 14, in a VM or a container. This Move migrates its managed PostgreSQL service to CloudNativePG on Kubernetes, using Move 12's local NVMe and object gateway. The primary and standbys must occupy different physical hosts even when their Kubernetes nodes are guests. The initial copy runs before the maintenance window; a rehearsed restore and final replication catch-up make the fifteen-minute reference possible.

A VM-only estate may keep its managed database under Move 04. An existing PostgreSQL VM does not need converting to CloudNativePG to leave the cloud: keep its VM deployment and use a separately rehearsed database replication, failover and backup plan at Move 18. The operator-specific steps below apply only when the inventory selects the Kubernetes database route.

## Before you start

**Access**
- Logical decoding enabled on the managed instance, with the reboot taken
- Credentials for a bucket on the object gateway from Move 12, separate from the cluster's
- The Kubernetes database platform from Moves 11 and 12, including physical-host replica separation

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
6. Open the window. Stop every writer, including jobs inside VMs. Wait for replication lag to reach zero, compare the final data, advance sequences and switch every application connection string. Start writes only on the destination, then verify both VM and container clients use it.

## Operator's notes
- **Swap:** A reverse subscription can shorten rollback only if the managed service permits it and its replication loop prevention and sequence repair have been rehearsed. Keeping the old instance alone does not keep its data current.
- **Do it faster:** Split the publication into several subscriptions grouped by table size, so the initial copy runs in parallel, not table by table.
- **Watch out:** Replication carries rows only. Sequences, large objects, schema changes and tuned parameters stay behind, and a sequence left at one collides on the first insert.
- **Leftovers:** The replication slot on the source outlives its subscription and retains write-ahead log for a reader that has gone.

## Rollback
Until destination writes resume, return connection strings to the source and release its write pause. The point of no return for that quick return is the first destination commit. After it, stop writers again and use the rehearsed reverse replication or restore-and-replay procedure to carry those commits back; verify data and sequence positions before reopening the source. A source backup predating cutover cannot recover newer writes. Retain the managed instance and its backups for seven days, and take destination backups throughout that period.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $19,500/mo | $0/mo | 100% | 15 min | 12 days | — |

## What you can turn off
The managed instance, its read replicas and their snapshots, after the seven days and once an invoice shows the line gone.
