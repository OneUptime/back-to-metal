# 01 · The bill, and the three lines that are most of it

**Layer:** Decide · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> The invoice records what you were charged, not what you use. Read it to the line, find the three that are most of it, then start the clock on working set.

## Leaving from
- **AWS:** Cost Explorer — hourly detail is a paid opt-in with a 14-day window; resource-level daily detail is a separate setting.
- **Google Cloud:** Cloud Billing reports — a new BigQuery export in the US or EU multi-region backfills the current and previous month; regional datasets start when enabled.
- **Azure:** Cost Management — amortised exports support Enterprise Agreement and Microsoft Customer Agreement accounts, but management-group exports omit amortisation and commitment purchases.

## Why this works
The bill and the workload measurements answer different questions. A bill records what was charged — allocation, commitment, a support percentage — not what the machines were doing. Group compute, state and traffic, keep shared charges visible, and rank the workloads inside them. Start guest memory measurements alongside the billing work: allocated RAM is not working set. A fortnight is the reference window; extend it or replay measured peaks if month-end jobs, seasonal demand or rare batches would otherwise be absent from the hardware order.

## Before you start

**Access**
- Billing export rights in every cloud account, organisation account-list access, and permission to install an agent on production instances

**Software**
- The provider tools `aws`, `gcloud` and `az`, with their tested versions recorded
- The chosen memory agent, with its tested version and collection configuration pinned
- A spreadsheet and a time-series store with three weeks of retention

**People**
- Whoever signs the invoice, for half an hour at the end

## The runbook
1. Export a full month's detailed cost from every account: AWS Data Exports CUR 2.0 with resource IDs, Google Cloud's detailed BigQuery export, and `az costmanagement export` at supported subscription scopes. Record missing history; a new export may not contain last month. Keep the invoice beside it for credits, support and purchases that an export can omit.
2. Preserve the raw rows, then aggregate the month by resource or workload in the spreadsheet. Tag compute, state or traffic: instances and containers; databases, caches and object storage; egress, balancers and the CDN. Keep support and unallocated commitments in a shared-cost row; reconcile the grand total to the invoice.
3. Sort the aggregated workloads by amount and mark the largest three as the first candidates. Keep the rest in the inventory: a cheap identity service or queue can still block an expensive migration.
4. Reconcile the export against what you believe you run. Enumerate the accounts first — `aws organizations list-accounts`, `gcloud billing projects list` against each billing account, `az account list` — and check permissions cover the whole estate. Investigate unowned lines rather than treating them as proven waste.
5. Install the pinned memory agent where it is missing and collect CPU and guest memory in one time-series store. Confirm units, sampling intervals and working-set definitions before combining the three clouds' metrics.
6. Open the window for a fortnight, and record what resists measurement: burstable credits, page cache against anonymous memory, build minutes that were never an instance. Extend the window or test omitted peaks before Move 05 approves capacity.

## Operator's notes
- **Swap:** If finance already breaks the bill down by service, start there and spend the saved time on step four. Reconcile its categories and totals before relying on them.
- **Do it faster:** Pull three invoices rather than one. One month hides a reservation renewal and a support tier that stepped up.
- **Watch out:** Metric charges depend on the collection path: custom time series, ingested bytes, samples and API reads can each be billable. Name the metrics and labels you need, then price that collection before enabling it across the fleet.
- **Leftovers:** The agents, export jobs and extra ingestion bill on until somebody removes them. Diary it for the day the hardware order is signed.

## Rollback
The billing queries do not change workloads; an agent rollout does, so test its overhead and retain the prior configuration. Backing out removes the added agent and stops the export job. There is no point of no return here; the hardware order comes later. Preserve collected samples, mark any gaps and extend the window when needed. If the time-series store is lost, restore it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 2 weeks |

## What you can turn off
Nothing, yet. This Move may add a temporary metrics charge; calculate it from the chosen collection path and remove it when the measurements are complete.
