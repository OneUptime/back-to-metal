# 85 · The data that stays: deep archive and the warehouse

**Layer:** Data · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Keeps deep archive and the warehouse on the provider deliberately, and hardens the one account that holds the archive and the third backup copy.

## Leaving from
- **AWS:** S3 Glacier Deep Archive and Redshift — a one-hundred-and-eighty-day minimum storage term on the deepest tier, which changes the retrieval arithmetic.
- **Google Cloud:** Archive storage and BigQuery — a three-hundred-and-sixty-five-day minimum on the archive class, the longest of the three.
- **Azure:** Archive tier and Synapse — a one-hundred-and-eighty-day minimum, with rehydration priorities that change both the time and the price.

## Why this works
This is an honest no with a runbook attached. Deep archive is cheap to hold and expensive to move, and repatriating it means a one-off egress bill plus a media-refresh obligation you do not want. The managed warehouse means somebody else owns a query engine, a scheduler and a storage tier, and owning those three is a team rather than a Move. So both stay, deliberately, and the work here is different: hardening the one account that will outlive the migration, because it now holds the archive and the third copy of your backups, and it is no longer protected by everything else you were running.

## Before you start

**Access**
- The archive inventory with its storage classes and the minimum-term charges that apply to each
- The warehouse's real query cost, so the decision to keep it is priced rather than assumed

**Software**
- A separate credential set for the retained account, outside the identity path built in Move 55
- Immutability, multi-factor deletion and a budget alarm on the retained account

**People**
- Whoever owns retention policy, because this account is now the long-term record

## The runbook
1. Price the retrieval properly, with early-deletion charges rather than list retrieval rates. The deepest tiers carry a minimum storage term of six months on two clouds and a full year on the third, and deleting early bills the remainder anyway.
2. Decide, and write the decision down: the archive stays, the warehouse stays, and the reason for each is arithmetic rather than inertia. Move 122 needs this in writing so it does not try to close the account.
3. Bring the lake substrate home. Open table formats on the object store from Move 84, with a query engine in front, is the part that does move, and it is where most of the ongoing query cost actually lives.
4. Harden the retained account. Separate credentials outside the identity path from Move 55, immutability on the archive buckets, multi-factor deletion, and a budget alarm that alerts a human rather than a mailbox.
5. Rehearse a retrieval end to end and time it, including the rehydration wait. A retrieval nobody has performed is a retention policy rather than a capability.
6. Put the account into Move 119's evidence pack and Move 120's cost model as a permanent line, so it is never a surprise on a future invoice.

## Operator's notes
- **Swap:** Where the archive is small and cold enough to fit on your own store under immutability, bringing it home is fine and removes an account. Price the one-off egress before deciding.
- **Do it faster:** Split the archive by whether it must be retrievable in hours or in days. The second half can go one tier deeper and is usually most of the volume.
- **Watch out:** A retained account with no active workloads is a security blind spot. It stops appearing in dashboards, its credentials stop being rotated, and its budget alarm is the only thing anybody looks at.
- **Leftovers:** The warehouse's scheduled queries and its ingestion pipelines keep billing whether or not anyone reads the results. Review them before deciding what the warehouse actually costs.

## Rollback
Nothing here is a one-way door: the archive can be repatriated later at the price of the egress bill, and the warehouse can be migrated when someone is willing to own a query engine. The point of no return does not exist in this Move. Keep the retrieval drill timings and the hardening configuration in source control, so the account's intended state can be restored and audited when nobody has looked at it for a year.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,860/mo | $1,860/mo | 0% | 0 min | 1 week | — |

## What you can turn off
Nothing here, by design. What you can turn off is the warehouse's scheduled queries that nobody reads, which is usually a third of its cost.
