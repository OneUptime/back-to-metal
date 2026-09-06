# 74 · Point-in-time recovery with pgBackRest

**Layer:** Data · **Leaving:** Managed automated backups and snapshots · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Rebuilds point-in-time recovery with pgBackRest, because every claim of reversibility later in the book rests on a restore that has actually been run.

## Leaving from
- **AWS:** RDS automated backups and snapshots — a retention window and a restore-to-time button that you never had to operate yourself.
- **Google Cloud:** Cloud SQL automated backups and point-in-time recovery — the same, with the write-ahead log retention configured separately.
- **Azure:** Flexible Server backups with geo-redundant options — the same again, with the redundancy sold as a tier.

## Why this works
Every claim of reversibility in this book, and every rollback paragraph in Part V, rests on a restore that has actually been run. The managed service gave you that for a monthly charge and you never had to think about the repository, the archive path or the recovery objective. Owning it means all three become explicit. The repository goes on the object store from Move 49, in a different failure domain and a different credential domain, under immutability — and because immutability on that store has to be set when a bucket is created rather than added later, the bucket is made correctly before the first backup rather than hardened afterwards.

## Before you start

**Access**
- The object store from Move 54, with its durability, off-site copy and restore drill already proved
- A second credential domain for the repository, so one compromised credential cannot reach both copies

**Software**
- `pgbackrest` at a pinned version, configured with asynchronous archiving rather than the default
- A scratch cluster to restore into, because a restore that has never been performed is a hope

**People**
- Whoever owns the recovery objective, so the number this Move produces is the number they expected

## The runbook
1. Create the repository bucket with immutability enabled at creation. On the object store you now own, this cannot be added afterwards on most releases, and a repository that can be deleted by the credential that writes it is not a backup.
2. Configure `pgbackrest` with a full and differential schedule and asynchronous write-ahead log archiving. Synchronous archiving on a busy database becomes the bottleneck and then becomes an incident.
3. State the recovery point objective honestly. The archive timeout bounds it only on a quiet database; a busy one is bounded by how fast segments fill plus how long the push takes, and that is the case that matters.
4. Put the repository in a different failure domain and a different credential domain from the cluster. A repository the cluster can delete with its own identity is a copy, not a backup.
5. Take a full backup and then restore it to a point in time into a scratch cluster. Time the restore. That number is the recovery time objective, and it is usually longer than anyone assumed.
6. Run the Move 72 gate against the restored copy. A restore that completes and produces different data has not succeeded; it has failed quietly, which is worse.
7. Put the restore drill on a schedule and treat a failed drill as an incident, because a repository nobody has restored from is exactly as useful as no repository at all.

## Operator's notes
- **Swap:** For a small database, a nightly dump to the object store plus write-ahead log archiving is simpler and adequate. It gives a worse recovery point and it is a great deal better than nothing.
- **Do it faster:** Restore into the second cluster from Move 51 rather than building a scratch environment. It exists for exactly this.
- **Watch out:** A backup that has been running successfully for weeks can still be unrestorable if the archive has a gap. Verify the archive continuously rather than checking that the backup job exited zero.
- **Leftovers:** Managed automated backups keep billing for their retention window after the instance is deleted, which is a line that surprises people in Part VII.

## Rollback
Nothing in this Move changes the running database, so it is reversible immediately and has no point of no return. What it changes is what the rest of the book is allowed to claim: no Move after this one may describe itself as reversible unless a restore from this repository has been performed and verified. Keep the repository configuration and the timed drill results in source control, so the recovery objective is a published number rather than an assumption.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $620/mo | $70/mo | 89% | 0 min | 2 weeks | — |

## What you can turn off
Managed automated backups, once a restore from your own repository has been performed, verified by the gate and timed.
