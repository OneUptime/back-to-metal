# 76 · The proprietary Postgres engines: the exit is a stream

**Layer:** Data · **Leaving:** Proprietary managed PostgreSQL-compatible engines · **Risk:** High · **Cutover:** 20 min · **Reversible:** 7 days

> Leaves the proprietary PostgreSQL engines by logical replication, which is the only door, and settles what replaces fast cloning and near-instant crash recovery.

## Leaving from
- **AWS:** Aurora PostgreSQL — a decoupled storage layer that gives near-instant crash recovery and fast cloning, neither of which comes with you.
- **Google Cloud:** AlloyDB — the same shape, with a columnar engine on top that has no landing-side equivalent at all.
- **Azure:** Cosmos DB for PostgreSQL — distributed by an extension that is openly licensed, so this reader can self-host the same distribution rather than facing a closed engine.

## Why this works
These engines are PostgreSQL at the protocol and a different system underneath, and that difference is the whole content of this Move. There is no file-level backup you can take away, no base backup that restores anywhere but the same engine, and no snapshot that means anything outside it. Logical replication is the only door. That makes the migration bounded by two things: how fast the initial copy runs, and how long the source will hold a replication slot open while it does. Everything else here is deciding what replaces the features that do not travel, before anyone touches production.

## Before you start

**Access**
- Logical decoding enabled per Move 71, on the writer endpoint rather than a reader
- A measured initial copy rate from a rehearsal, because that is what sets the schedule

**Software**
- The same CloudNativePG destination and the same gate from Move 72 as Move 73 used
- A written list of features in use that have no equivalent, with a decision beside each

**People**
- Whoever uses fast cloning, usually the delivery team, because their workflow changes

## The runbook
1. List the engine-specific features actually in use and decide each one before the migration starts. Fast cloning for per-branch test databases, restore granularity finer than a backup repository gives, near-instant crash recovery, and scale to zero on the serverless variants. Each is consciously replaced or consciously dropped.
2. Replace fast cloning explicitly. On your own hardware the equivalent is a restore from the repository built in Move 74 into the second cluster, which is slower and adequate, or a filesystem-level snapshot where the storage supports it.
3. Follow Move 73's runbook for the stream itself: schema first, deferred indexes, publication and subscription, catch-up watched, reverse subscription built before the cutover.
4. Watch the slot rather than the lag on these engines. The constraint is how long the source will hold the replication slot open while the initial copy runs, and a slot that is dropped mid-copy means starting again.
5. Run the Move 72 gate, then cut over with writes paused, sequences advanced and the gate run once more. Twenty minutes, and the same shape as Move 73.
6. For the distributed variant on one cloud, decide between a rewrite and self-hosting the same openly licensed distribution extension. That is a genuine choice rather than a workaround, and it is usually the better answer.
7. Keep the source running for seven days with the reverse stream in place, exactly as in Move 73.

## Operator's notes
- **Swap:** Where the columnar engine is load-bearing, the honest landing is a separate analytical store rather than an attempt to reproduce it in PostgreSQL. Move 85 has the substrate.
- **Do it faster:** Measure the copy rate on a rehearsal against a full-sized dataset. Every schedule in this Move derives from that one number and estimating it is how the window overruns.
- **Watch out:** Near-instant crash recovery is a property you are giving up. On your own hardware, recovery time after an unclean stop is proportional to the work in flight, and Move 75's failover figure reflects that.
- **Leftovers:** The engine's storage is billed separately from its compute on some variants and continues after the instance stops. Check both lines before declaring the saving.

## Rollback
The reverse subscription makes the week real: repoint the connection, let the reverse stream drain, and the managed engine is authoritative again. Until writes resume on the new side, backing out is releasing the pause. The point of no return is the deletion of the source, which is Move 38. Keep the source and its automated backups for seven days so a restore to a known good point remains possible, and confirm the reverse stream is actually flowing rather than merely configured.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $6,240/mo | $580/mo | 91% | 20 min | 3 weeks | 7 days |

## What you can turn off
The proprietary engine's instances and its storage line — after seven days, and after checking that the storage line is billed separately and has actually stopped.
