# 113 · The rota

**Layer:** Watch · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the rota from the engineers who can actually be called, because one week in four needs a bench that leave and resignation do not empty.

## Leaving from
- **AWS:** the shared responsibility model — the provider carried the hardware layer and its on-call for it, invisibly and permanently.
- **Google Cloud:** its shared responsibility documentation — the same split, described in a whitepaper you never had to staff against.
- **Azure:** its shared responsibility guidance — the same again, and the reason the hardware rota is a new line in the budget.

## Why this works
A rota is arithmetic before it is a policy. One week in four needs four people who can genuinely be called; one in three needs three and burns them out; one in two is not a rota, it is two people waiting to resign. Whether the team is large enough at all was settled back in Move 22, against each landing option, at the point where the reader could still act on the answer. What happens here is building it, funding it and writing the handover practice — and being honest that the alert volume will include signals the managed monitor never surfaced, because nobody was ever paged about an inlet temperature before.

## Before you start

**Access**
- The staffing conclusion from Move 22, and the budget it implied
- The alert inventory from Move 114, so the rota is designed against real volume rather than hope

**Software**
- A rota schedule with escalation, published where everyone can see who is on
- A handover practice: what is written down, when, and by whom

**People**
- Enough engineers that one week in four is achievable with someone on leave

## The runbook
1. Do the arithmetic and publish it. Depth of four is the minimum for a sustainable weekly rota, and depth of three works only with an explicit plan for leave and an accepted risk during it.
2. Settle compensation and rest. Standby that materially constrains someone's free time counts as working time under several jurisdictions' rules, and rest entitlements after a disturbed night are a legal obligation rather than a courtesy.
3. Estimate the alert volume honestly. Power distribution, inlet temperature, fans, memory errors and disks are all new sources that the managed monitor never surfaced, and they arrive at night by their nature.
4. Set the escalation path with names rather than roles, and a second name behind each. A rota that escalates to a role nobody occupies at three in the morning escalates to nobody.
5. Write the handover practice down: what the outgoing person records, what the incoming person reads, and where it lives. This single practice decides whether year two is calm.
6. Rehearse a handover during a real incident review rather than only in theory, and adjust the template based on what was actually missing.
7. Price it and give the number to Move 120, because a rota is a standing cost and the comparison in that Move is dishonest without it.

## Operator's notes
- **Swap:** Where the team is genuinely too small, the honest answers are the rented-metal option from Move 22 or a managed service partner, not a rota of two people. Both are cheaper than losing them.
- **Do it faster:** Start the rota before go-live, on the non-production estate, so that the first real page is not the first page anybody has received.
- **Watch out:** Alert fatigue is the failure mode, and it arrives about six weeks in. Move 114's tuning is not optional; it is what keeps the rota staffed.
- **Leftovers:** The rented paging service, if you keep one, bills per user per month, and it is one of the lines Move 114 examines.

## Rollback
A rota is changed by changing it, and there is nothing here to reverse technically. The point of no return does not exist; what does exist is a human cost that is slow to appear and slow to recover from, which is why the depth arithmetic is done honestly rather than optimistically. Keep the rota, the compensation policy and the handover template in source control so the agreed practice can be restored when it drifts.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing. This Move adds a standing cost, and pretending otherwise is how the comparison in Move 120 goes wrong.
