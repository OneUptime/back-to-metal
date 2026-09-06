# 88 · Document and wide-column stores: the hardest exit

**Layer:** Data · **Leaving:** Managed document, key-value and wide-column stores · **Risk:** High · **Cutover:** 30 min · **Reversible:** 30 days

> Decides per store whether the table moves to Cassandra, collapses into Postgres, or stays on the bill below a stated monthly threshold.

## Leaving from
- **AWS:** DynamoDB — export to object storage and import back round-trips the items and builds secondary indexes from a specification, but only into a new table, and carries no expiry, stream, capacity or tag configuration.
- **Google Cloud:** Firestore and Bigtable — the document store exports in a format importable only back into itself and carrying no index definitions; the wide-column store exits through its compatibility interface.
- **Azure:** Cosmos DB — multiple APIs, each with its own export path and its own set of things that do not travel.

## Why this works
This is the hardest exit in the book and the honest answer is a decision procedure with a threshold rather than a slogan. Three outcomes are legitimate: the table moves to a wide-column database you run, the table collapses into the relational database you already operate, or the table stays on the bill because it is below a monthly figure where migrating it costs more than paying for it for three years. The export limitations are real and specific, and the harder problem is not the data at all — it is that on-demand capacity meant nobody ever had to know the workload shape you must now size hardware against.

## Before you start

**Access**
- Export permissions, and the throughput data that tells you what shape the workload actually is
- A stated monthly threshold below which a store stays, agreed with whoever owns the budget

**Software**
- A repository interface in front of every store that stays, so the decision can be revisited without a rewrite
- The destination chosen deliberately: the permissively licensed wide-column database rather than the source-available alternative

**People**
- The owner of each store, because collapsing into a relational schema is a data-model decision

## The runbook
1. Measure the workload shape first: read and write rates, item sizes, access patterns and how much of the traffic is a single hot partition. On-demand capacity hid all of this and hardware sizing needs all of it.
2. Apply the threshold. Below an agreed monthly figure, the store stays and a repository interface goes in front of it, so the decision can be revisited later without touching application code. Record which stores fall this side of the line.
3. For stores that move, read the export limitations rather than assuming a round trip. One export can only create a new table and carries no expiry, stream, capacity or tag configuration; another is importable only back into its own service and carries no index definitions; the wide-column case exits through a compatibility interface.
4. Rebuild everything the export does not carry: secondary indexes, expiry settings, stream configuration and capacity settings. Each is a separate step and each is silently absent otherwise.
5. Choose the landing deliberately. Where a wide-column store is genuinely required, the destination is the permissively licensed project rather than the alternative, which since a recent release ships only under a source-available licence with a capacity-limited free tier.
6. Where the data model is really relational — and it frequently is — collapse it into the database you already run. Fewer systems is worth more than a faithful reproduction of a data model nobody chose deliberately.
7. Dual-write, compare, then cut over with a thirty-minute window and keep the source for thirty days.

## Operator's notes
- **Swap:** Keeping a store on the bill is a legitimate outcome and should be written down as a decision with its threshold, not as an unfinished task.
- **Do it faster:** Do the threshold arithmetic before any technical work. It frequently removes two thirds of the stores from the programme in an afternoon.
- **Watch out:** A single hot partition that the managed service absorbed invisibly becomes a hot node on your own hardware. Find it in the measurement step or find it in production.
- **Leftovers:** Streams, expiry jobs and on-demand backups on the source all keep billing after the table stops being read.

## Rollback
For thirty days the source table still exists and still holds the data, so reverting is repointing the repository interface. Anything written on the new side in the interim must be restored to the source by replaying it, which is why the dual-write runs for the whole window rather than only until the cutover. The point of no return is the deletion of the source table in Move 38, against a signed approval.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,620/mo | $740/mo | 84% | 30 min | 6 weeks | 30 days |

## What you can turn off
The tables that moved, their streams and their on-demand backups, thirty days after the dual-write stops. The ones below the threshold stay, deliberately.
