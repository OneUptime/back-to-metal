# 71 · The Postgres pre-flight

**Layer:** Data · **Leaving:** Managed PostgreSQL · **Risk:** Medium · **Cutover:** 15 min · **Reversible:** Immediately

> Audits roles, extensions, replica identity and collation weeks before any cutover, because these failures are silent until the far side is already serving reads.

## Leaving from
- **AWS:** RDS and Aurora for PostgreSQL — provider-only extensions and a role graph built under a superuser you never had.
- **Google Cloud:** Cloud SQL for PostgreSQL — its own provider-only extensions and a flag set that has to be enabled before logical decoding works.
- **Azure:** Database for PostgreSQL Flexible Server — an allowlist parameter that governs which extensions may load at all.

## Why this works
Every failure this Move looks for is silent. A missing role does not fail at migration time; it fails when an application connects. A provider-only extension does not fail until a query uses it. A table with no primary key replicates its inserts and silently discards its updates. And a collation difference between the source and the destination does not fail at all — it produces text indexes that are subtly, permanently wrong. All four are cheap to find weeks ahead and expensive to find on the far side of a cutover, which is why this Move is separate from Move 73 and happens long before it.

## Before you start

**Access**
- Read access to the catalogues on the managed instance, and a maintenance window for one parameter change
- The second cluster from Move 51 to rehearse the audit against

**Software**
- `psql` at a version at least as new as the server, and `pg_dump` for the globals-only role export
- A written comparison of the collation provider and version on both sides

**People**
- Whoever owns the application, to schedule the reboot the one production change requires

## The runbook
1. Export the role graph with a globals-only dump and read it. Managed instances build roles under a superuser you never had, so the graph frequently contains grants that cannot be reproduced literally and have to be re-expressed.
2. Inventory the extensions and mark the provider-only ones. Each cloud has its own — an object-store integration extension, a machine-learning integration, a storage extension behind an allowlist — and each is either replaced, dropped or blocks the migration. Decide which, in writing, now.
3. Find every table with no primary key or no replica identity. Logical replication carries inserts for these and silently discards updates and deletes, which produces a destination that diverges quietly and passes a row count.
4. Compare the collation provider and version on both sides. A text index built under one collation and used under another can return wrong results, and this is the failure that is hardest to detect and worst to discover late.
5. Rehearse the whole audit against a restored copy on the second cluster from Move 51, so the findings are proved rather than theorised.
6. Make the one production change: enable logical decoding. It is a static parameter on all three providers and it requires a reboot. On a single-instance deployment that reboot is routinely longer than five minutes; on a multi-zone one it is a failover. Schedule it weeks ahead of anything anyone has described as zero-downtime.

## Operator's notes
- **Swap:** Where an extension has no equivalent and the application depends on it, the honest answer may be that this database moves last, or moves as a dump and restore with a longer window.
- **Do it faster:** Run the audit as a set of queries checked into source control rather than as a session. It will be run again for every database in the estate.
- **Watch out:** The reboot is the whole cutover figure in this Move, and it is the step people schedule casually because the rest of the Move is read-only.
- **Leftovers:** Logical decoding retains write-ahead log for any slot that exists. A slot created during the audit and forgotten will fill the source's disk, which is an outage on the system you are still depending on.

## Rollback
The audit changes nothing and the parameter change is reverted by another parameter change and another reboot, so this Move is reversible immediately at the cost of one more window. The point of no return does not exist here; it is in Move 73. Keep the audit output in source control, because it is the baseline the verification in Move 72 will be compared against, and because a restore of the source later needs to be checked against the same findings.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 15 min | 2 weeks | — |

## What you can turn off
Nothing. This Move only adds a parameter and a list of things to fix before Move 73 can safely run.
