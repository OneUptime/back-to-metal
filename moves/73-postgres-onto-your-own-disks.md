# 73 · Postgres onto your own disks

**Layer:** Data · **Leaving:** Managed PostgreSQL · **Risk:** High · **Cutover:** 20 min · **Reversible:** 7 days

> Moves Postgres onto CloudNativePG by logical replication, with writes stopped at PgBouncer for the sequence advance and the verification gate.

## Leaving from
- **AWS:** RDS for PostgreSQL — replicates from the writer endpoint, with the logical decoding parameter already enabled in Move 71.
- **Google Cloud:** Cloud SQL for PostgreSQL — the same, with an additional role grant required before a publication can be created.
- **Azure:** Database for PostgreSQL Flexible Server — the same again; the older single-server product has no logical decoding at all and has to be dumped and restored.

## Why this works
Logical replication moves the data while both databases are live, so the downtime is not the copy — it is the few minutes it takes to stop writing to one side, advance the sequences, run the gate and start writing to the other. This is also the first production data to land on your own hardware, which means it lands on the local volumes from Move 47, under the encryption from Move 48, from the registry in Move 58, inside the policy from Move 60 and on the dashboards from Move 62. None of that existed by accident; the whole of Parts III and IV was ordered so that this Move would have somewhere safe to land.

## Before you start

**Access**
- The logical decoding parameter enabled and the audit findings from Move 71 resolved rather than noted
- The link from Move 53, sized for catch-up rather than for steady state

**Software**
- CloudNativePG at a pinned version, already rehearsed and failed over on the second cluster
- PgBouncer in front of the application, so writes can be paused without restarting anything

**People**
- The application owner present for the window, because the pause at PgBouncer is visible to users

## The runbook
1. Rehearse the whole thing twice on the second cluster from Move 51 before touching production. Three weeks is the budget for this Move and two rehearsals are most of it.
2. Copy the schema only, apply it to the CloudNativePG cluster on the destination, and defer the indexes on large tables. They slow the initial copy and are faster to build afterwards.
3. Create the publication and the subscription and watch the catch-up in the subscription statistics. Set the write-ahead log retention limit on the source as a safety valve, so a stalled subscriber cannot fill the source's disk and take down the database you are still depending on.
4. Build the reverse subscription back to the managed instance before the cutover, and leave it running. This is what makes the Move reversible for a week rather than only until the first write.
5. Build the deferred indexes, then run the Move 72 gate and resolve every mismatch that is not on the benign list.
6. Open the window. Pause writes at PgBouncer, wait for lag to reach zero, advance every sequence with a margin, run the gate one final time, and resume against the new primary. Twenty minutes is the honest figure and most of it is the gate.
7. Watch error rates and latency for an hour, then leave the managed instance running with its automated backups on for seven days.

## Operator's notes
- **Swap:** Under about fifty gigabytes with a tolerant window, a dump and restore is simpler and finishes inside an hour. Logical replication earns its complexity above roughly that size.
- **Do it faster:** Run the initial copy from a read replica rather than the primary. It costs one extra instance for a day and takes the load off the database serving traffic.
- **Watch out:** Logical replication does not carry sequences, large objects or schema changes. A migration that forgets the sequences works perfectly until the first insert collides, which is usually about ninety seconds later.
- **Leftovers:** The publication and subscription persist until dropped. Drop them deliberately after the week, or the source keeps retaining write-ahead log for a subscriber nobody is reading.

## Rollback
Until writes are resumed on the new side, backing out is releasing the pause and doing nothing else. After that, the reverse subscription is what makes the week real: repoint PgBouncer, let the reverse stream drain, and the managed instance is authoritative again. The point of no return is the day the source is deleted, which is Move 38 and not this Move. Keep the managed instance and its automated backups for seven days so a restore to a known good point stays available.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,180/mo | $410/mo | 90% | 20 min | 3 weeks | 7 days |

## What you can turn off
The managed instance, its read replicas and its snapshots — after seven days, after Move 75 has high availability working, and after a billing cycle has shown the line gone.
