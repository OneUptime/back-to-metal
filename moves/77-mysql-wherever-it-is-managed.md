# 77 · MySQL, wherever it is managed

**Layer:** Data · **Leaving:** Managed MySQL · **Risk:** High · **Cutover:** 20 min · **Reversible:** 7 days

> Moves MySQL on GTIDs rather than replication slots, cut over behind read_only, a GTID position check and the verification gate.

## Leaving from
- **AWS:** RDS for MySQL and Aurora MySQL — the latter carrying a rewind feature whose replacement on your own hardware is an ordinary physical backup plus binary logs.
- **Google Cloud:** Cloud SQL for MySQL — the same shape, with its own external replica flow and its own parameter names.
- **Azure:** Database for MySQL Flexible Server — again the same, with the parameter change requiring a restart as it does everywhere.

## Why this works
MySQL replicates by global transaction identifiers rather than by replication slots, which changes the shape of the cutover: what you check before switching is a position rather than a lag, and what makes the switch safe is putting the source into a read-only state so that no write can land after the position was taken. The transfer itself is a parallel dump and load followed by positioned replication. What is not available is the physical backup tool everybody reaches for first, because it needs access to the data directory and no managed provider gives you that — where a provider mentions it at all, it is a way in rather than a way out.

## Before you start

**Access**
- Row-based binary logging with full row images enabled, which costs a restart on every managed variant
- The link from Move 53 and the gate from Move 72

**Software**
- A parallel dump and load tool for the initial copy, pinned, and `mysql` for the position checks
- A written comparison of the source's mode settings against the version you are landing on

**People**
- The application owner for the read-only window, because it is visible as failed writes rather than as slowness

## The runbook
1. Enable row-based binary logging with full row images. This is a prerequisite and it costs a restart on every managed variant, so it is scheduled well before the cutover in the same way Move 71 schedules its reboot.
2. Audit the drift nobody logged. Mode settings that differ from upstream, and columns using the three-byte character set that have been silently truncating four-byte characters for years. The second one is a data problem, not a migration problem, and it is found here or never.
3. Take the initial copy with a parallel dump and load, recording the position it corresponds to. A copy without a recorded position cannot be followed by replication and has to be taken again.
4. Start positioned replication from that point and watch it catch up. The check that matters is the executed transaction set on both sides, not a lag figure in seconds.
5. Run the Move 72 gate against the destination while replication is live, and resolve every mismatch not on the benign list.
6. Cut over: set the source read-only, confirm the positions match exactly, run the gate once more, and repoint the application. Twenty minutes, most of it the final gate run.
7. Land on a long-term-support release or the openly licensed alternative distribution, under an operator, and keep the source for seven days.

## Operator's notes
- **Swap:** Where the provider's own migration service is available and the database is small, it is a reasonable path for the initial copy. Do not let it own the cutover decision; the gate does that.
- **Do it faster:** Run the parallel dump from a read replica rather than the primary, with enough threads to saturate the link from Move 53 rather than the default.
- **Watch out:** The character set problem is the one that ruins a migration retrospectively. Fix the columns before the copy, not after, because after the copy the truncation has already been carried across.
- **Leftovers:** Binary log retention on the source continues to consume storage after the cutover. Reduce it deliberately once the seven days have passed.

## Rollback
Until the source is taken out of read-only and the application is repointed, backing out is a single setting. For the week afterwards, replication is reversed by streaming from the new primary back to the source, and the source's own backups remain available for a restore to a known good point. The point of no return is the deletion of the source, which is Move 38. Keep the recorded positions, because a rollback without them is a full recopy.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,760/mo | $310/mo | 89% | 20 min | 3 weeks | 7 days |

## What you can turn off
The managed instance, its read replicas and its binary log retention — after seven days, and after the gate has been run once more against the source before it goes.
