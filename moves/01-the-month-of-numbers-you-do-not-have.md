# 01 · The month of numbers you do not have

**Layer:** Iron · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Installs a memory-reporting agent in all three clouds and opens a thirty-day sampling window, because none of them reports guest working set without one.

## Leaving from
- **AWS:** CloudWatch — the hypervisor publishes CPU, network and disk and says nothing about memory; the CloudWatch agent has to be installed and handed a configuration that names the memory metrics you want.
- **Google Cloud:** Cloud Monitoring and the Ops Agent — the only one of the three that reports memory in its default configuration, so the work here is confirming coverage rather than writing configuration.
- **Azure:** Azure Monitor — memory arrives only through the Azure Monitor agent behind a data collection rule, an object you create per subscription and then associate with every machine you care about.

## Why this works
You cannot buy a machine against a number you have never measured. The figure a purchase order needs is working set — the memory a process is actually touching — and no cloud reports it, because the hypervisor cannot see inside the guest. What the console shows you instead is allocation, which is the number you were billed for and not the number you need. Thirty days is the shortest window that contains a month end, a full weekly cycle and at least one deploy of every service, and it is the reason this is the first Move in the book: every purchasing decision in Part I waits on it, so the clock starts before anything else does.

## Before you start

**Access**
- Read access to the billing export in every cloud account you run in, including the ones nobody has opened this year
- Permission to install an agent on production instances, and a change window if that needs one

**Software**
- A Prometheus or equivalent time-series store with at least forty days of retention, so the window survives its own analysis
- The three provider command-line tools, `aws`, `gcloud` and `az`, none older than six months
- `kubectl` against every managed cluster, with rights to read the metrics API

**People**
- Whoever owns each application, to say which workloads are allowed to be slow and which are not

## The runbook
1. Install the memory agent everywhere it is missing. On AWS that is the CloudWatch agent with a configuration block naming `mem_used_percent` and `mem_available`; on Azure it is the Azure Monitor agent plus a data collection rule associated with each machine; on Google Cloud confirm the Ops Agent is running and reporting rather than assuming it.
2. Point your own time-series store at all three metric APIs and let it pull, rather than reading each console separately. One store means one query language at the end of the month instead of three.
3. Add per-container working set and per-node IOPS from the managed clusters you already run, using `kubectl` against the metrics API. Container memory is what sizes a node; node memory is what sizes a machine.
4. Export a full month of billing data per account and reconcile it against the running inventory. Anything on the invoice that is not in the inventory is the part of the estate nobody remembers, and it is usually five to fifteen per cent.
5. Write down what cannot be measured at all: burstable credit balances, page cache against anonymous memory, and the build minutes that never appeared as an instance. An honest gap list is worth more than an invented figure.
6. Leave it running for thirty days. Do not analyse it at day seven and do not shorten the window because the quarter is ending; a month with no month end in it is not a month.

## Operator's notes
- **Swap:** If an agent rollout to production needs a change advisory board that meets fortnightly, start with a representative fifth of the fleet and widen. A partial month of real data beats a full month you never got approval for.
- **Do it faster:** The agent configuration is three files. Ship them through whatever configuration tool already reaches those machines rather than building a new path for one job.
- **Watch out:** The agents themselves cost money — custom metrics are billed per metric per month on all three, and a careless configuration collecting every counter on every host has surprised people with a four-figure line. Name the metrics you want.
- **Leftovers:** The data collection rules, agent configurations and the extra metric ingestion stay billing until you remove them. Diary the removal for the day the purchase order is signed.

## Rollback
Nothing here changes how anything runs, so backing out is uninstalling three agents and deleting a data collection rule. The point of no return does not exist in this Move; it exists in Move 20, which spends money against these numbers. The only real cost of abandoning it is the calendar: stop at day twelve and you have twelve days of data, and starting again means waiting another thirty. If the time-series store is lost, restore it from its own snapshot rather than re-running the window, because the window cannot be re-run retrospectively.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | 30 days |

## What you can turn off
Nothing yet. This Move only adds cost — a few hundred dollars of agent metrics for a month — and it is the cheapest money in the programme.
