# 72 · The verification gate

**Layer:** Data · **Leaving:** Managed database-migration validation · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the chunked hash-and-checksum comparison that every later data cutover has to pass before anyone is allowed to proceed.

## Leaving from
- **AWS:** Database Migration Service data validation — a validation task that stops working the day the account does.
- **Google Cloud:** Database Migration Service verification — the same, tied to the same lifetime.
- **Azure:** Database Migration Service assessment — the same again, and the same reason to own this rather than rent it.

## Why this works
Every cutover in Part V ends with somebody deciding whether the two sides agree. That decision should be a measurement rather than a judgement, and it should be the same measurement every time so that it can be trusted without re-reading it. What this Move builds is a deterministic aggregate over every table on both sides — a hash over the primary key and a checksum over the columns, chunked by key range so that it runs concurrently and can be restarted — plus an assertion that replication lag is zero. It is deliberately a gate and not a repair tool: it answers go or no-go and nothing else.

## Before you start

**Access**
- A physical replica on the source side to run against, so the comparison costs read load on a machine nothing is serving from
- The destination database from Move 73's rehearsal, or the second cluster from Move 51

**Software**
- `psql` for the aggregates, and somewhere to store per-chunk results so a run can resume
- A written rule for which mismatches are benign and which mean stop

**People**
- Whoever will make the go decision on cutover night, because they have to trust this before they rely on it

## The runbook
1. Write the aggregate as a hash over the primary key combined with a checksum over the remaining columns, computed per chunk of the key range. Deterministic ordering matters; an aggregate that depends on row order will disagree for no reason.
2. Chunk by primary key range so the comparison runs concurrently and restarts from where it stopped. On a large table a single unchunked query is both slow and unrestartable, which is how verification gets skipped.
3. Run it against a physical replica rather than the primary. The blast radius is then read load on a machine nothing serves from, which is what makes it safe to run as often as you like.
4. Assert replication lag is zero before comparing. A comparison taken while the stream is behind reports differences that are not differences, and the resulting arguments waste an hour of a maintenance window.
5. Write down which mismatches are benign — a sequence ahead by design, a monitoring table that writes on both sides — and which mean stop. Do this in advance and in daylight, not at two in the morning.
6. Run it against the rehearsal from Move 73 and confirm it detects a difference you introduce on purpose. A gate that has never said no is a gate nobody has tested.

## Operator's notes
- **Swap:** For small tables a straight row-by-row comparison is simpler and just as good. The chunked aggregate earns its complexity above a few million rows.
- **Do it faster:** Run it continuously during the catch-up phase rather than only at the end. Differences found a week early are cheap; the same differences found in the window are not.
- **Watch out:** Floating-point columns and timestamps with time zones are the two types most likely to produce spurious mismatches through formatting rather than value. Normalise them explicitly in the aggregate.
- **Leftovers:** The managed validation task keeps billing while its migration task exists. It is turned off with the rest of the migration service in Part VII.

## Rollback
This Move only reads, so there is nothing to reverse and no point of no return anywhere in it. That is what makes it the right thing to build before any data moves. Keep the queries and the benign-mismatch rules in source control, so the same gate is applied to every database in Part V and so that a previous run can be restored and compared when somebody questions a result.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $180/mo | $0/mo | 100% | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The managed validation tooling goes with the migration service in Part VII.
