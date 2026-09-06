# 112 · The support contracts you buy for open source

**Layer:** Watch · **Leaving:** Paid cloud support plans priced against spend · **Risk:** Low · **Cutover:** 0 min · **Reversible:** 365 days

> Prices support subscriptions for the host OS, Ceph, Postgres and the switch OS, because the answer at 03:00 on a corruption bug is not always someone you employ.

## Leaving from
- **AWS:** Business and Enterprise Support — priced as a percentage of spend, so the saving here is largest where the bill was largest.
- **Google Cloud:** Standard and Enhanced Support — the same percentage-of-spend model with its own thresholds.
- **Azure:** Standard and Professional Direct — flat-rate tiers, so a small estate saves almost nothing by cancelling.

## Why this works
Cancelling the cloud support plan is a real saving on two of the three clouds, because it was priced as a share of a bill that is about to shrink. What replaces it is not nothing. There are four components where a subscription genuinely earns its money — the host operating system, the storage cluster, the database and its operator, and the switch operating system — and what such a contract buys is a named escalation path and a fix in a release, not an engineer on site. Knowing that distinction is what stops the subscription being either skipped or over-bought.

## Before you start

**Access**
- The current support plan's price and what it actually covers, read rather than remembered
- A list of the components you would not want to debug alone at three in the morning

**Software**
- Quotes from vendors for each candidate subscription, on the versions you actually run
- The escalation path each one offers, in writing, with a response commitment attached

**People**
- Whoever holds the budget, because these are annual commitments rather than monthly ones

## The runbook
1. Price what you are cancelling. On two of the three clouds support was a percentage of spend, so the saving falls with the bill and is largest at the start; on the third it was a flat tier and cancelling saves very little.
2. Shortlist the components that warrant a subscription. The host operating system from its vendor, the storage cluster from a company that employs its maintainers, the database and its operator from a database company, and the switch operating system from whoever sold it.
3. Read what each contract buys. A named escalation path and a fix in a future release is the realistic answer. An engineer at your site is not, and a subscription bought expecting one will disappoint.
4. Check the versions covered. A subscription that only supports versions you are not running is a subscription you cannot use, and this is the most common mismatch.
5. Get quotes early. Procurement here is a quarter, mostly spent waiting, so start it when Part VII starts rather than when the cloud plan lapses.
6. Note the commitment shape. Most of these are annual and cancellable only at renewal, which is what the reversibility figure records, and that is a reason to buy fewer of them rather than more.
7. Test each escalation path once with a real, low-severity question. A path nobody has used is a path with an unknown response time.

## Operator's notes
- **Swap:** Where the team genuinely has deep expertise in a component, skip its subscription and put the money into the rota from Move 113. Support contracts and headcount are the same budget.
- **Do it faster:** Buy the storage subscription first. It is the component where an unsolved problem is most likely to be a data problem.
- **Watch out:** A support subscription is not a substitute for the restore drills in Moves 52, 74 and 115. Vendors help you diagnose; they do not restore your data.
- **Leftovers:** The cloud support plan is billed monthly and cancels on notice, so it can be dropped as soon as the estate that justified it has moved.

## Rollback
Subscriptions are annual and cancellable only at renewal, so leaving one costs the remainder of a year. The point of no return, such as it is, is the purchase order. Cancelling the cloud plan is reversible at any time by re-subscribing, which is worth knowing before Part VII closes the account entirely. Keep the escalation paths and contract terms in source control with the runbooks, so the right number can be found at three in the morning rather than searched for. No vendor on this list will restore your data for you; the drills in Moves 52, 74 and 115 do that.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,100/mo | $1,600/mo | 61% | 0 min | 1 week | 4 weeks |

## What you can turn off
The cloud support plan, once the estate it covered has moved. What you buy instead is smaller and it is not nothing.
