# 20 · The bill of materials

**Layer:** Iron · **Leaving:** Committed-spend discounts on rented compute · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Assembles every Iron decision into a document a supplier can quote against, and sets the three-year cost frame the rest of the book is judged against.

## Leaving from
- **AWS:** Savings Plans and Reserved Instances — a one or three-year commitment whose renewal date is the real deadline for this programme.
- **Google Cloud:** Committed Use Discounts — the same commitment shape, per project or across an organisation, with the same renewal cliff.
- **Azure:** Reservations and savings plans — the same again, and the one where the licensing benefit is usually tangled into the commitment.

## Why this works
Everything in Part I has been a decision. This Move turns them into a document a supplier can quote against, which is a different artefact: part numbers, quantities, unit prices, lead times, firmware baselines, per-rack draw, the rack-unit budget, the spares, the acceptance terms from Move 18, and an explicit exclusion list for the cabinet, the power distribution and the cross-connects, which belong to Part II. It also fixes the date. The renewal of your committed-spend discount is the deadline that actually governs this programme, because that is the moment the cloud bill either falls off a cliff or is re-committed for another three years.

## Before you start

**Access**
- Authority to commit capital, and the finance calendar it has to fit inside
- The renewal date and terms of every committed-spend agreement across all three providers

**Software**
- Every decision from Moves 01 to 19 in one document, with the reasoning attached rather than summarised
- A three-year cost model that includes people, because a comparison that omits salary is the reason repatriations get approved and then regretted

**People**
- Finance and procurement in the same room as whoever signs the order, once rather than four times

## The runbook
1. Assemble the document. Part numbers and quantities, unit prices, lead times per line, firmware baselines, the per-rack draw from Move 07, the rack-unit budget from Move 11, the spares from Move 19 and the acceptance terms from Move 18 written in as a condition of payment.
2. State the exclusions explicitly. The cabinet, the power distribution units, the cross-connects and the facility itself are Part II and are not on this document. An exclusion list prevents the two most common surprises, which are buying a cabinet twice and buying none at all.
3. Set an order sequence rather than a single date. Memory and optics have the longest lead times and a switch without transceivers is a paperweight, so the sequence is memory first, then switches and optics, then chassis, then spares.
4. Build the three-year frame with both numbers in it. For the reference estate in this book, the same core count on rented compute is about $56,500 a month before storage or egress, and the owned infrastructure is about $12,100 a month all in. Add the salary honestly — the platform needs more of it than the cloud did — and the total-against-total comparison is closer to half rather than four-fifths. Publish both, and let nobody quote only the first.
5. Name the renewal date of the commitment you are choosing not to renew, and work backwards from it. That date, not the delivery date, is what the programme plan hangs on.
6. Sign it, and tell everyone the number. From this moment the programme has a budget, a delivery window and a deadline, and Part II can be negotiated against a real draw instead of an estimate.

## Operator's notes
- **Swap:** Renting dedicated machines by the month gets most of the saving with none of the capital, the lead time or the loading bay. It is the honest answer for a team that wants the economics without the facility, and it costs roughly half the saving.
- **Do it faster:** Ask for a quote on the whole document rather than line by line. Suppliers discount the bundle and it removes a fortnight of correspondence.
- **Watch out:** A committed-spend discount usually cannot be cancelled and sometimes cannot be transferred. Check whether yours can be sold on the marketplace before assuming the remaining term is a sunk cost.
- **Leftovers:** The cloud commitment keeps billing until its term ends whether or not anything runs on it. Plan the migration to finish near that date, not long before it.

## Rollback
This Move is irreversible: a signed purchase order is money committed and, past the supplier's return window from Move 17, hardware you own. The point of no return is the signature itself, which is why the whole of Part I exists to make it a well-evidenced one. What remains reversible is the programme, not the purchase — Move 121 describes how to abort and keep running on the cloud, and Move 20's hardware retains resale value. Keep every quote, model and decision in source control so the case can be restored and re-examined afterwards.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $74,013/mo | $38,337/mo | 48% | 0 min | 1 week | 8 to 16 weeks |

## What you can turn off
Nothing yet, and this is the point. The cloud bill does not move until Part V and Part VI have carried the workloads across; everything before then is spending twice.
