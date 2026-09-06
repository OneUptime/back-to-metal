# 86 · The batch estate: who schedules the jobs

**Layer:** Data · **Leaving:** Managed workflow orchestration and managed Spark · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 30 days

> Moves the DAGs and the Spark jobs onto schedulers you run, because the lake substrate came home and nothing yet writes to it on a schedule.

## Leaving from
- **AWS:** Managed Workflows for Apache Airflow with EMR — the same open-source scheduler on both sides, so the work is the hooks rather than the graphs.
- **Google Cloud:** Cloud Composer with Dataproc — the same again, with the same consequence.
- **Azure:** Data Factory with Synapse Spark — a low-code designer with no open-source equivalent, so this estate is a rewrite priced as one rather than a migration.

## Why this works
The scheduler repatriates well on two of the three clouds because it is literally the same software on both sides, which means the graphs themselves are not the work. The work is everything around them: the provider-specific hooks and operators embedded in the tasks, the metadata database, the executor, and the secrets backend. Each of those has a clean landing — a database cluster of its own, the cluster executor on the fixed fleet from Move 69, and the secrets path from Move 56. The third cloud is genuinely different, because a designer-based pipeline has nothing to port, and calling that a migration rather than a rewrite is how the estimate goes wrong by a factor of three.

## Before you start

**Access**
- The scheduler's metadata database, exported, and the graphs in source control rather than only in the console
- The lake substrate from Move 85 and the object store from Move 84

**Software**
- The scheduler at a pinned version with the cluster executor, and its metadata on a database cluster of its own
- The Spark operator reading and writing the object store, at a pinned version

**People**
- The owner of every pipeline, because provider-specific operators are code changes in their repositories

## The runbook
1. Inventory the tasks by the operators they use. Anything using a provider-specific hook or operator is a code change; anything using a generic one moves untouched. That split is the whole estimate.
2. Stand up the scheduler at a pinned version with its metadata on its own database cluster, and the cluster executor pointed at the fixed fleet from Move 69. Batch runs at the lower priority tier defined there, which is the point of having tiers.
3. Move the secrets backend to Move 56's path rather than carrying the provider's. A scheduler holding credentials in its own database is a finding waiting for Move 118.
4. Rewrite the provider-specific operators. This is ordinary work and it goes at a predictable rate once the first few are done.
5. Land the Spark jobs on the operator, reading and writing the object store from Move 84. Sizing is now yours: executor count, memory and shuffle space are a capacity decision rather than a cluster type.
6. Where the source was a designer rather than code, price a rewrite and schedule it as one. Do not attempt to translate a visual pipeline into a graph automatically.
7. Run both schedulers for thirty days with the new one writing to a separate output path, and compare results before switching consumers.

## Operator's notes
- **Swap:** For a handful of jobs, cluster cron jobs are simpler than a scheduler and remove a component. A scheduler earns its place when dependencies between jobs are real.
- **Do it faster:** Move the graphs that use only generic operators first. They are usually half the estate and they move in a day.
- **Watch out:** The metadata database grows and is rarely pruned. Import a cleaned copy rather than a full one, or the first thing your new scheduler does is inherit five years of task instances.
- **Leftovers:** The managed scheduler bills per environment-hour whether or not anything runs, and the managed Spark service bills per cluster. Both keep running through the dual period.

## Rollback
For thirty days the managed scheduler still has the graphs and can be re-enabled, and because the new side writes to a separate output path nothing has been overwritten. Reverting is disabling the new schedules and re-enabling the old ones. The point of no return is deleting the managed environment, which is Part VII. Keep the exported metadata so a scheduler can be restored with its history rather than starting blank.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,410/mo | $290/mo | 91% | 0 min | 4 weeks | 30 days |

## What you can turn off
The managed scheduler environment and the managed Spark clusters, thirty days after both sides produced the same outputs.
