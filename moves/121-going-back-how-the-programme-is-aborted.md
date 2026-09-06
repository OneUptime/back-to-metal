# 121 · Going back: how the programme is aborted

**Layer:** Watch · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Writes the abort plan while going back is still cheap: what returns, what the surrendered commitments cost to restart, and who is allowed to make the call.

## Leaving from
- **AWS:** Savings Plans and Reserved Instances — surrendered on the way out and repriced at current rates on the way back.
- **Google Cloud:** Committed Use Discounts — the same, with the commitment tied to a project or organisation you may have closed.
- **Azure:** reservations and savings plans — the same again, and the one where a closed subscription complicates the restart most.

## Why this works
Somewhere around month nine a board asks what happens if this does not work, and the answer should already be written. It is answerable now, because Move 120 knows the real number and Moves 52, 74 and 115 have proved the restores. The abort plan says what would actually return, what it costs to restart the discounts that were surrendered, which managed services no longer exist in the version you left, who is allowed to make the call, and what would trigger it. It also names the genuine point of no return, which is not a technical step at all.

## Before you start

**Access**
- The cost model from Move 120, so the comparison is against a real number rather than a fear
- The notice dates from Move 30 and the disposal plan from Move 38

**Software**
- Each Move's own rollback paragraph, collected into one ordered document
- A current list of which managed services still exist in the form you left them in

**People**
- A named decision owner with the authority to stop the programme, and their deputy

## The runbook
1. Collect every Move's rollback into one ordered document. The abort inherits each Move's own cutover window in reverse rather than adding one of its own, which is why the individual paragraphs matter.
2. Price the restart. Reserved capacity and committed spend surrendered on the way out are repriced at current rates on the way back, and current rates are not the rates you left.
3. Check what still exists. Managed services change, are retired and are renamed; a service you left eighteen months ago may not be available in the form your code expects.
4. Name the decision owner and the deputy. An abort decision with no owner is an abort decision that gets made too late by a committee.
5. Write the trigger criteria in advance and in numbers, the same way Move 103 wrote its abort criteria. What would have to be true for this to be the right call.
6. Name the real point of no return, which is commercial rather than technical: the notice served on the facility in Move 30 and the hardware disposal in Move 38. Everything before those is recoverable at a price.
7. Print the egress and switching-charge position with its source and a review date, because it is regulated, it is dated, and it moves.

## Operator's notes
- **Swap:** Where the programme is genuinely in trouble, a partial abort is usually the right answer: keep the platform and return one workload. The plan should support that rather than treating this as all or nothing.
- **Do it faster:** Write it at the first programme gate rather than at the ninth month. It takes a week and it is the document that keeps a nervous board calm.
- **Watch out:** The way back depends on the interconnect from Move 53 and the cloud accounts staying open. Move 122 must not close them before this plan is retired.
- **Leftovers:** The old estate's configuration, launch templates and node groups are the way back, and they cost almost nothing to leave in place. Leave them.

## Rollback
This is the rollback, and it is irreversible in the sense that the decisions it describes cannot be taken twice: notice served on a facility cannot be recalled, and hardware disposed of under Move 38 cannot be restored. The point of no return for the whole programme is those two events, not any technical cutover. Review this document at every programme gate, and keep each version, so the board can see how the answer changed as the evidence did.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing. This Move exists to keep options open, and every option it protects costs a little to keep.
