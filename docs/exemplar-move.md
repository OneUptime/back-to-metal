<!-- EXEMPLAR. Not part of the book: this file is the reference for voice, shape
     and density when writing a Move. The contract it satisfies is documented in
     AGENTS.md; verify.py and audit.py enforce it. Numbered 02 here only because
     it was written that way; it is not in moves/, and the book's real Move 02 is
     a different job entirely. -->

# 02 · Managed Postgres, brought home

**Layer:** Move · **Leaving:** Managed PostgreSQL · **Risk:** High · **Cutover:** 15 min · **Reversible:** 7 days

> Fifteen minutes of stopped writes, at the end of a week in which the new cluster was caught up, backed up, and restored once on purpose.

## Leaving from
- **AWS:** RDS for PostgreSQL — the default parameter group cannot be edited, so `rds.logical_replication` needs a custom group and a reboot.
- **Google Cloud:** Cloud SQL for PostgreSQL — `cloudsql.logical_decoding` requires a restart; retained write-ahead log can fill storage or trigger a billed increase when automatic growth is enabled.
- **Azure:** Database for PostgreSQL flexible server — `CREATE EXTENSION` fails until the name is in the `azure.extensions` allowlist, and extensions requiring `shared_preload_libraries` also need a server restart.

## Why this works
Logical replication carries table data while the managed source keeps serving. This example targets CloudNativePG on Kubernetes, with a primary and two standbys on different physical hosts. The initial copy and a restore from an independent backup happen before the maintenance window. Fifteen minutes is a rehearsed reference allowance for the final write stop and validation, not a guarantee based on database size. Existing PostgreSQL VMs can use their own tested replication and backup plan instead.

## Before you start

**Access**
- Logical decoding enabled on the managed instance, with the reboot taken
- Credentials for an object-backup repository and an independent off-site copy, separate from the cluster's
- A Kubernetes database platform, local NVMe and physical-host replica separation

**Software**
- CloudNativePG 1.30.0, with a pinned PostgreSQL image on the source's supported major version and a rehearsed failover
- Barman Cloud plugin 0.15.0 and cert-manager 1.21.1; the plugin requires CloudNativePG 1.26 or later
- `psql` and `pg_dump` no older than the managed server

**People**
- The application owner, present for the window when writes stop

## The runbook
1. List extensions, roles, large objects and table replica identities with `psql`. Recreate required roles and grants; provider-only extensions or unsupported objects block the Move until a tested alternative exists. Freeze schema changes and rehearse returning destination writes to the managed instance.
2. Apply `pg_dump --schema-only` to a CloudNativePG cluster with one primary and two standbys on separate hosts. Preserve primary keys and replica-identity indexes. Confirm every updated or deleted source table has a suitable replica identity; the schema dump does not copy cluster-wide roles.
3. Create the publication and subscription, keeping application writes off the destination. Monitor `pg_stat_subscription`, table synchronization and retained source WAL continuously. Require every table to finish its initial copy and application queries to pass before booking cutover.
4. Configure the Barman Cloud plugin's ObjectStore and cluster plugin settings for continuous archiving and scheduled full backups. Keep an independent off-site copy with its keys. Check WAL arrival and archive failures; backups confined to the rack do not survive its loss.
5. Restore from the off-site copy into isolation and replay to a recorded timestamp. Disable subscriptions and outbound jobs there; compare with checks recorded for that recovery point, not a changing production database. Measure recovery and confirm the recovered application works before allowing destination writes.
6. Open the window. Stop all source writers and wait for in-flight transactions. Record a final published transaction and confirm the subscriber applies it after every table is synchronized. Compare final data, transfer any separately handled objects and set destination sequences from source values. Abort to the source if checks exceed the rehearsed deadline.
7. Disable the forward subscription, fence source writers and switch every connection string. Start writes only on the destination, then verify VM and container clients, errors and query latency. Keep destination backups running and preserve the tested return procedure throughout the seven days.

## Operator's notes
- **Swap:** A reverse subscription can shorten rollback only if the managed service permits it and its replication loop prevention and sequence repair have been rehearsed. Keeping the old instance alone does not keep its data current.
- **Do it faster:** Tune `max_sync_workers_per_subscription` within the source's slot and destination's worker budgets. Initial table copies already support parallelism; splitting related tables across subscriptions loses their shared transaction boundary.
- **Watch out:** Replication carries rows only. Sequences, large objects, schema changes and tuned parameters stay behind, and a sequence left at one collides on the first insert.
- **Leftovers:** A disabled subscription still retains source WAL. Once rollback no longer needs it, remove the subscription and verify slot cleanup; normal subscription removal drops its slot, but a detached or orphaned slot needs separate cleanup.

## Rollback
Until destination writes resume, return connection strings to the source and release its write pause. The point of no return for that quick return is the first destination commit. After it, stop writers again and use the rehearsed reverse replication or restore-and-replay procedure to carry those commits back; verify data and sequence positions before reopening the source. A source backup predating cutover cannot recover newer writes. Retain the managed instance and its backups for seven days, and take destination backups throughout that period.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,180/mo | $410/mo | 90% | 15 min | 6 days | — |

## What you can turn off
The managed instance and read replicas after seven days, verified destination recovery and the required snapshot retention. Confirm the resulting charges disappear on the next invoice; an active instance cannot produce that evidence first.
