# 03 · The estate nobody sizes

**Layer:** Iron · **Leaving:** Non-production capacity that costs nothing when it is switched off, and hosted CI runners · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Sizes dev, staging and CI from the same month of samples, because on hardware you own idle non-production costs exactly what busy non-production costs.

## Leaving from
- **AWS:** CodeBuild and non-production accounts — build minutes are billed per minute of a build container and never appear in an instance inventory at all.
- **Google Cloud:** Cloud Build and non-production projects — the same absence, plus a free tier that hides the real volume until you export the billing data.
- **Azure:** Azure Pipelines with Microsoft-hosted agents — billed per parallel job rather than per minute, so the invoice tells you concurrency and not consumption.

## Why this works
Non-production is invisible in a cloud cost model because it is cheap when nobody is using it: scale it to zero at seven in the evening and the bill agrees. On a machine you own, that saving does not exist. The machine draws power whether or not a test is running, and the capital was spent whether or not anyone deploys on a Friday. So non-production has to be sized like production, from measurement, and it usually comes to between a third and the whole of production again. Build capacity is worse, because hosted runners never appeared as instances anywhere, and the only honest record of them is billed minutes.

## Before you start

**Access**
- Billing exports for every non-production account and project, including the sandbox nobody claims
- The build service's usage report for the same month, in minutes rather than in currency

**Software**
- The same time-series store as Move 01, with the non-production accounts already flowing into it
- A list of every pipeline and its trigger, so concurrency can be reasoned about rather than guessed

**People**
- Whoever runs the delivery pipeline, to say what queue time is currently tolerated

## The runbook
1. Inventory the non-production estate the same way you inventoried production, and reconcile it against the billing export. Everything on the invoice and not in the inventory is either a test environment somebody forgot or a resource that has been idle for a year.
2. Take the same p95 and p99 from the window, per environment. Staging usually turns out to be production-shaped and dev turns out to be much smaller than its instance sizes suggest.
3. Convert build minutes into concurrent build capacity. Take the busiest hour of the busiest weekday in the window, divide the minutes by sixty, and add the queue depth you are willing to accept. This is the number of build executors you need, and it is normally between four and twelve for a team of thirty.
4. Add the storage that comes with it — artefacts, layer caches, package proxies — measured, not estimated. Build caches are the fastest-growing thing in most estates and they behave nothing like application storage.
5. Decide the sharing question now: does non-production run on the same machines as production with resource limits and priority, or on its own smaller ones? Both are defensible; only one of them is in the machine count, and Move 11 needs the answer.
6. Write the decision down with its consequence stated plainly. Sharing saves capital and puts your test suite one bad manifest away from production. Separating costs money and makes the blast radius a conversation you never have to have.

## Operator's notes
- **Swap:** If the sharing question cannot be settled in the time available, size for separate machines. Merging two clusters later is a weekend; splitting a shared one after production is on it is a quarter.
- **Do it faster:** Build executors are the one place where a small number of fast cores beats a large number of slow ones. Size them against wall-clock build time and stop optimising.
- **Watch out:** Free tiers hide volume. A pipeline that looks like four hundred minutes a month on the invoice can be four thousand, with the difference absorbed by an included allowance that will not exist on your own hardware.
- **Leftovers:** The idle environments this Move surfaces can be deleted today, on the cloud, before anything moves. That is usually the first saving in the whole programme.

## Rollback
The output is a number and a decision, and both are revised by revising them. The point of no return is Move 20: once the machine count includes a separate non-production tier, unpicking that means either returning hardware inside a vendor window or living with capacity you did not want. Until then the cost of being wrong is an hour of arithmetic. Keep the environment inventory under source control so an earlier version can be restored and compared when somebody argues the estate was smaller than this.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
The environments this Move finds and nobody claims. Delete them in the cloud, this week, and watch a full billing cycle before you count the saving.
