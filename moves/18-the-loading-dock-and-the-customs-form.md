# 18 · The loading dock and the customs form

**Layer:** Site · **Leaving:** Managed service · **Risk:** High · **Cutover:** 20 min · **Reversible:** Immediately

> Synthetic placeholder for the Site Part, number 18, used only to design the page layouts at realistic length.

## Leaving from
- **AWS:** RDS for PostgreSQL — set the `rds.logical_replication` parameter to 1 and reboot; Aurora needs the same flag but replicates from the writer endpoint only.
- **Google Cloud:** Cloud SQL for PostgreSQL — set the `cloudsql.logical_decoding` flag, which also reboots, and grant the `cloudsqlexternalsync` role before creating a publication.
- **Azure:** Database for PostgreSQL Flexible Server — set `wal_level` to `logical` in server parameters; Single Server has no logical decoding at all and has to be dumped and restored instead.

## Why this works
Every managed PostgreSQL is PostgreSQL with a control plane bolted on, and the PostgreSQL underneath speaks the same replication protocol as any other instance. A publication on the source and a subscription on the destination move the data continuously while the application keeps writing, which turns a migration into a wait. What remains at cutover is draining the last transactions, promoting the new primary and pointing the application at it. The twelve minutes are not the copy; they are the verification you should refuse to skip.

## Before you start

**Access**
- Superuser or the provider's nearest equivalent on the source, with logical decoding already enabled and the reboot taken
- A maintenance window agreed with whoever owns the application

**Software**
- CloudNativePG 1.25 or newer, installed and running a test cluster you have already failed over
- `psql` and `pg_dump` at a version at least as new as the server
- `pgbackrest` 2.54 or newer, writing to a repository in a third location

**Hardware**
- Local NVMe on at least three nodes, with a storage class that pins a volume to its node
- Enough disk for the database plus fifty per cent, measured rather than estimated

## The runbook
1. Take a `pgbackrest` backup of the destination's empty cluster and restore it into a scratch namespace. A backup nobody restored is not a backup, and this is the cheapest moment to find that out.
2. Copy the schema only, with `pg_dump --schema-only`, and apply it to the destination. Create every table but no indexes on large tables yet; they slow the initial sync and are faster to build afterwards.
3. Create a publication on the source for all tables, and a subscription on the destination. Watch `pg_stat_subscription` until the initial copy finishes and the lag settles under a second.
4. Build the deferred indexes on the destination, then compare row counts table by table and checksum a sample of the largest three. Do not proceed on a count that disagrees, however small the difference looks.
5. Open the maintenance window. Stop the application's writers, wait for replication lag to reach zero, and confirm it with `pg_current_wal_lsn` on both sides.
6. Advance every sequence on the destination past its source value. A migration that forgets the sequences works perfectly until the first insert collides, which is usually about ninety seconds later.
7. Repoint the application's connection string at the destination and start the writers. Watch error rates and query latency for ten minutes before you call it done.
8. Leave the managed instance running, and leave its automated backups on, for the full thirty days.

## Operator's notes
- **Swap:** For a database under 50 GB with a tolerant maintenance window, `pg_dump` and restore is simpler and finishes inside an hour. Logical replication earns its complexity above roughly that size.
- **Do it faster:** Run the initial sync from a read replica rather than the primary. It costs an extra instance for a day and takes the load off the database serving traffic.
- **Watch out:** Logical replication does not carry sequences, large objects, or DDL. Every one of those has ended a cutover that otherwise went perfectly.
- **Leftovers:** The publication and subscription stay in place until you drop them. Drop them deliberately after the thirty days, or the source keeps retaining write-ahead log for a subscriber nobody is reading.

## Rollback
Until step seven the source is still the primary and still authoritative, so backing out is stopping the subscription and doing nothing else. The point of no return is the first write that lands on the destination: from that moment the two databases have diverged and returning means replicating backwards, not switching back. If you must return after that, stop the writers, set up the reverse subscription from destination to source, wait for it to drain, and repoint. Keep the managed instance and its automated backups for thirty days so a restore to a known good point stays possible.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $5,170/mo | $100/mo | 98% | 20 min | 8 days | — |

## What you can turn off
The managed instance, its read replicas and its snapshots — after thirty days, and after a full billing cycle has shown the line gone.
