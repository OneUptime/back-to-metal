# 02 · What you actually run

**Layer:** Decide · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> The estate feels infinite because nobody has written it down. On one page it is forty rows, and every row has a name against it.

## Leaving from
- **AWS:** Resource Explorer — indexes per Region behind one aggregator and searches one account until the organisation-wide view is on, so the second account stays invisible.
- **Google Cloud:** Cloud Asset Inventory — the caller needs `cloudasset.assets.searchAllResources` at the organisation scope; a project-level grant says nothing about the siblings on the same invoice.
- **Azure:** Resource Graph — reads only subscriptions the caller can already see, and pages at 1,000 rows, so an unpaged query returns a truncated estate that looks complete.

## Why this works
Leaving the cloud feels impossible because nobody can say what would have to move. The estate lives in three or four heads, so the total is always imagined larger than it is. A company spending $10,000 a month usually runs half a dozen services, one Postgres, one cache, a couple of buckets and a handful of scheduled jobs. That fits on a page, and every later Move then has something finite to count against. Nothing changes here: this Move reads, and writes down what it read. The risk is being wrong about what runs, and the bill settles that.

## Before you start

**Access**
- Read-only access to every cloud account, project and subscription, including the forgotten ones
- The billing export from Move 01, at resource granularity rather than by service

**Software**
- The provider's asset CLI — `aws`, `gcloud` or `az` — and one shared document with a row per resource

**People**
- The engineer who would notice each service stopping, named on every row

## The runbook
1. Pull the machine-readable list, one account at a time: `aws resource-explorer-2 search`, `gcloud asset search-all-resources` or `az graph query`. Paste it into one document, a row per resource.
2. Add what those APIs never return: scheduled jobs, queues, third-party services with a webhook into production, and the DNS records pointing at any of it.
3. Reconcile against the billing export from Move 01 both ways. A bill line with no row is unowned; a row with no bill line is free, or in an account nobody has opened.
4. Hunt what hides: snapshots whose disk is gone, volumes attached to nothing, load balancers with no target, staging at full size overnight, the accounts opened for a proof of concept in 2022.
5. Sort every row into one of four piles — moves as-is, moves with work, stays rented, gets deleted. The fourth is the biggest; confirm each row with its owner and check thirty days of metrics first.

## Operator's notes
- **Swap:** Where accounts are few and tags honest, the provider's tag report is a quicker first pass. Untagged resources still have to be found by hand.
- **Do it faster:** Reconcile before assigning owners. The bill sorts rows by cost, which is the order worth arguing about.
- **Watch out:** These inventories list what the provider created. What a third party stood up against your account — an agent, a contractor's sandbox — appears nowhere else.
- **Leftovers:** A snapshot outlives the volume it came from and bills long after the rest of its account has gone. So does a retained log group.

## Rollback
Nothing here touches a running system, so backing out is discarding a document nobody acted on. The point of no return is the fourth pile: once a resource on it is deleted, getting it back means a restore from whatever snapshot survives, and for a log group there may be none. Keep the inventory in version control.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
The fourth pile, once its owners confirm: orphaned volumes, snapshots of vanished disks, idle load balancers and the proof-of-concept accounts. The cheapest saving in the book.
