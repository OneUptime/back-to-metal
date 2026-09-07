# 01 · The bill, and the three lines that are most of it

**Layer:** Decide · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> The invoice records what you were charged, not what you use. Read it to the line, find the three that are most of it, then start the clock on working set.

## Leaving from
- **AWS:** Cost Explorer — hourly and resource-level granularity is a paid opt-in, and that detail is then kept for 14 days.
- **Google Cloud:** Cloud Billing reports — detailed usage cost reaches BigQuery only from the day the export is enabled, and is never backfilled.
- **Azure:** Cost Management — amortised reservation cost appears on an Enterprise Agreement account, not on pay-as-you-go, and exports land in Blob Storage on a schedule.

## Why this works
Three numbers decide everything that follows, and none is on the provider's default dashboard. A bill records what was charged — allocation, commitment, a support percentage — not what the machines were doing. Grouped into compute, state and traffic, two hundred line items collapse into three piles, and three lines usually carry eighty per cent of the spend. The window runs alongside, because the figure a purchase order needs is working set and the hypervisor cannot see it. Two weeks, not thirty days: this is a five-machine decision, and more precision would not change the order.

## Before you start

**Access**
- Billing owner rights in every cloud account, and permission to install an agent on production instances

**Software**
- The provider tools `aws`, `gcloud` and `az`, none older than six months
- A spreadsheet and a time-series store with three weeks of retention

**People**
- Whoever signs the invoice, for half an hour at the end

## The runbook
1. Export one month at line-item granularity from every account, not the summary view. That means the detailed export rather than the console API on all three: the Cost and Usage Report delivered to a bucket, a BigQuery billing export, and `az costmanagement export` per subscription. `aws ce get-cost-and-usage` and the reports page return period totals grouped two ways at most, which is the summary view under another name.
2. Put every line in the spreadsheet, one row each, tagged compute, state or traffic: instances and containers; managed databases, caches and object storage; egress, balancers and the CDN.
3. Sort by amount and rule a line under the third row. Those three are the programme; anything beneath worth under two per cent of the invoice is not discussed again.
4. Reconcile the export against what you believe you run. Enumerate the accounts first — `aws organizations list-accounts`, `gcloud billing projects list` against each billing account, `az account list` — because the forgotten estate is usually in an account nobody named. Lines nobody owns are idle balancers, volumes of dead instances, a staging project that shipped. Expect five to fifteen per cent.
5. Install the memory agent where it is missing and point one time-series store at all three metric APIs. No hypervisor sees inside its guests, so working set arrives only from within the machine.
6. Open the window for a fortnight, and record what resists measurement: burstable credits, page cache against anonymous memory, build minutes that were never an instance.

## Operator's notes
- **Swap:** If finance already breaks the bill down by service, start there and spend the saved day on step four. The categories will be wrong, the totals right.
- **Do it faster:** Pull three invoices rather than one. One month hides a reservation renewal and a support tier that stepped up.
- **Watch out:** Agent metrics are billed differently on each cloud — per unique metric a month on one, per sample ingested on the others — and an agent collecting every counter it finds has produced four-figure surprises on all three. Name the metrics you want.
- **Leftovers:** The agents, export jobs and extra ingestion bill on until somebody removes them. Diary it for the day the hardware order is signed.

## Rollback
Nothing in production changes, so backing out is removing an agent and stopping an export job. There is no point of no return here; the first is the hardware order, signed against these numbers. A sampling window cannot be rerun retrospectively, so stopping at day nine means starting over. If the time-series store is lost, restore it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 2 weeks |

## What you can turn off
Nothing, yet. This Move moves one line upward: a fortnight of custom metrics, the cheapest few hundred dollars in the programme.
