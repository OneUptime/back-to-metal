# 02 · What you actually run

**Layer:** Decide · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> The estate feels infinite because nobody has written it down. Give every workload a row and an owner, then keep its resources underneath it.

## Leaving from
- **AWS:** Resource Explorer — indexes per Region behind one aggregator and searches one account until the organisation-wide view is on, so the second account stays invisible.
- **Google Cloud:** Cloud Asset Inventory — the caller needs `cloudasset.assets.searchAllResources` at the organisation scope; a project-level grant says nothing about the siblings on the same invoice.
- **Azure:** Resource Graph — reads only subscriptions the caller can already see, and pages at 1,000 rows, so an unpaged query returns a truncated estate that looks complete.

## Why this works
Leaving the cloud is hard to price until somebody can say what has to move. A bill does not reveal service boundaries, dependencies or who owns a workload. Make a short service summary backed by the complete resource list; the spend alone cannot tell you how many rows there will be. Every later Move then has something finite to count against. The inventory itself changes no running system. Its risks are omission and mistaken ownership, so reconcile the provider APIs with billing, configuration and the people who operate the services.

## Before you start

**Access**
- Read-only access to every cloud account, project and subscription, including the forgotten ones
- The billing export from Move 01, at resource granularity rather than by service

**Software**
- The provider's asset CLI — `aws`, `gcloud` or `az` — and one shared document with a row per resource

**People**
- The engineer who would notice each service stopping, named on every row

## The runbook
1. Pull the machine-readable list at every account's full scope: `aws resource-explorer-2 list-resources`, `gcloud asset search-all-resources` or `az graph query`. Check indexed regions and supported resource types. Follow every continuation token; Resource Explorer's separate `search` operation stops at 1,000 total matches. Keep one row per resource.
2. Check scheduled jobs, queues, DNS records and third-party webhooks against that list. Inventories include supported cloud resources, but guest-level schedulers and external services need application configuration and their owners to find them.
3. Reconcile against the billing export from Move 01 both ways. A bill line with no row is unowned; a row with no bill line is free, or in an account nobody has opened.
4. Hunt what hides: snapshots whose disk is gone, volumes attached to nothing, load balancers with no target, staging at full size overnight, the accounts opened for a proof of concept in 2022.
5. Label each workload VM, container or managed service. For each VM record its operating system, CPU architecture, boot mode, attached disks, licences and metadata credentials; mark which disks contain persistent state. A VM stays a VM on Proxmox VE in Move 11. Moving an application into containers is a separate project, not an unstated prerequisite.
6. Sort every row into one of four piles — moves as-is, moves with work, stays rented, gets deleted. Before deleting, confirm ownership, dependencies and retention needs, inspect at least thirty days of metrics and preserve a tested backup of required state. Record a destination and data-transfer method for every row that moves; check image-export restrictions before choosing that route.

## Operator's notes
- **Swap:** Where accounts are few and tags honest, the provider's tag report is a quicker first pass. Untagged resources still have to be found by hand.
- **Do it faster:** Reconcile before assigning owners. The bill sorts rows by cost, which is the order worth arguing about.
- **Watch out:** A contractor's cloud resources appear if the type and account are covered; software inside a VM generally does not. Compare the resource list with deployment configuration and guest-level services.
- **Leftovers:** A snapshot outlives the volume it came from and bills long after the rest of its account has gone. So does a retained log group.

## Rollback
Nothing here touches a running system, so backing out is discarding a document nobody acted on. The point of no return is the fourth pile: once a resource on it is deleted, getting it back means a restore from whatever snapshot survives, and for a log group there may be none. Keep the inventory in version control.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
The fourth pile, once owners, dependencies, backups and retention checks agree: orphaned volumes, unneeded snapshots, idle load balancers and proof-of-concept resources. Keep required recovery copies even when their original disks are gone.
