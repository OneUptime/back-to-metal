# 122 · The last account

**Layer:** Watch · **Leaving:** The provider's organisation and identity centre, audit trail, key management, registry, marketplace subscriptions and support plan · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Extracts the reports, the history and the key material, discharges the dated exceptions, then closes all but what four earlier Moves deliberately kept.

## Leaving from
- **AWS:** Organizations with IAM Identity Center — an organisation closes only with its management account, and a closed account is recoverable for about ninety days.
- **Google Cloud:** the organisation with Cloud Identity — a deleted project is recoverable for about thirty days, which is the shortest window and therefore the one this Move quotes.
- **Azure:** the tenant with Entra ID — a cancelled subscription is recoverable for about ninety days, with its own reactivation process.

## Why this works
This is the last Move and it is mostly extraction and waiting. What has to come out before anything closes: the compliance reports, the billing history that Move 120's comparison depends on, the audit trail from Move 118 and the key material. What trips people is the mechanics — key deletion has a waiting period, the audit trail keeps billing after everything else has gone, reserved capacity cannot be cancelled, and an organisation closes only with its management account. And what stays open is deliberate rather than accidental: four earlier Moves each kept something, and each said so in writing.

## Before you start

**Access**
- The management account or root project, because the organisation cannot be closed from anywhere else
- Every account and subscription enumerated, including the ones nobody has opened this year

**Software**
- An extraction list: compliance reports, billing history, audit trail and key material, with a destination for each
- The retained list from Moves 85, 88, 90 and 116, consolidated with dates and owners

**People**
- Whoever signed the committed-spend agreement, since that spend does not end when the usage does

## The runbook
1. Extract before closing anything: compliance reports for the audit in Move 119, the full billing history for the model in Move 120, the audit trail from Move 118, and any key material still needed to read archived data.
2. Consolidate the retained list. The archive from Move 85, the store held below its threshold in Move 88, the workflows dated in Move 90 and the tested overflow from Move 116. Each stays, each has an owner and each has a review date.
3. Resolve the egress credit conflict. The free-egress-on-exit programmes are time-boxed and at least one requires actually leaving, which conflicts with the footprint Move 116 keeps. Decide which is worth more, with the numbers, before closing anything.
4. Order the identity removal correctly. The federated identity provider registered in Move 55 is removed after the workloads that used it, not before, or the last workloads lose their access on the way out.
5. Work through the mechanics that delay closure: key deletion waiting periods, an audit trail that keeps billing, a committed-spend agreement and reserved capacity that cannot be cancelled, and marketplace subscriptions with their own terms.
6. Close accounts and subscriptions from the leaves inward, and close the organisation last, from its management account.
7. Wait out the recovery windows before declaring it finished. They differ by provider and the shortest is about thirty days, which is what this Move's reversibility figure records.

## Operator's notes
- **Swap:** Where a single retained resource is keeping a large account alive, moving it to a small separate account first makes the closure much simpler and cheaper.
- **Do it faster:** Start the key deletion waiting periods first, in parallel with everything else. They are the longest pole and nothing depends on them.
- **Watch out:** Closing an account does not cancel a committed-spend agreement. It continues to bill against the organisation, and Move 119 should already have established what that costs.
- **Leftovers:** Billing exports, audit trails and marketplace subscriptions all survive the deletion of what they were attached to. Each needs closing individually.

## Rollback
For about thirty days a closed account or a deleted project can be recovered, which is the window this Move quotes because it is the shortest of the three. After that, the extraction you took is all that remains, so verify that every extracted artefact can be restored and read before the window expires rather than after. The point of no return is the end of the shortest recovery window, and it is the last one in the book.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,180/mo | $1,900/mo | 13% | 0 min | 2 weeks | 30 days |

## What you can turn off
Everything except the four retained items, and those are written down with owners and review dates rather than forgotten.
