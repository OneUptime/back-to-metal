# 03 · The number that decides it

**Layer:** Decide · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Two columns, five years of amortisation and one salary line. If owned is not a third under rented, the answer is to stop, and stopping here is cheap.

## Leaving from
- **AWS:** AWS Pricing Calculator — two tools now carry that name, and only the one inside the billing console can see the Savings Plans your account already holds.
- **Google Cloud:** Google Cloud Pricing Calculator — the only discount it models is a committed-use one you pick from a dropdown, and its default machine series earns no sustained-use discount at all.
- **Azure:** Azure Pricing Calculator — signing in and selecting the Enterprise Agreement licensing programme rewrites every price on the page, so an anonymous quote is retail and not yours.

## Why this works
Moves 01 and 02 produced a grouped bill and an inventory that accounts for it. This Move sets the two candidate estates beside each other. The arithmetic is not hard; the discipline is refusing to leave anything out of the owned column, because an omitted line is what somebody finds in month five with two platforms running. The rule goes in before the numbers, so they cannot be argued into the answer somebody wanted. Nothing has been bought and no traffic has moved; two days of somebody's time is the whole exposure.

## Before you start

**Access**
- Three recent invoices at the rate you actually paid, not list
- A written quote for the sixteen machines and one for a full rack

**Software**
- One spreadsheet, two columns: owned on the left, rented on the right

**People**
- Whoever carries the pager, because the salary line here is theirs

## The runbook
1. Write the decision rule before any figure goes in: owned must land at least a third under rented, or the programme stops here. A thinner margin sits inside your own forecasting error.
2. Fill the rented column from the three invoices at the rate you actually paid, discounts in and tax out on both sides. One monthly number, checkable against Move 01.
3. Fill the owned column from the hardware quote and the facility quote: sixteen machines and two spares over sixty months, the full rack, committed power, transit, the cross-connects, remote hands.
4. Add the salary line to BOTH columns, because both columns have one. The cloud estate already costs somebody sixty hours a month — the managed cluster upgrades itself on somebody's Tuesday, the credentials rotate, the bill gets argued with, the pager gets carried — and a cloud invoice bills for none of it. Owning adds about twenty hours a month on top of that, not a second person. Write both down. A column with the salary on one side only is not a comparison, whichever side it is missing from.
5. Add the line that does not come home. Move 04 settles which capabilities you keep renting — the edge, outbound mail, scrubbing — and there is a residue besides: archived object storage nobody will pay the egress to extract, a registry, a queue, an off-site backup copy. It is inside the rented column already, so it has to be inside the owned column too. Leaving it out is the same error as leaving out the salary, and it is worth about a tenth of the bill.
6. Total both columns and apply the rule. If owned is not a third under rented, stop and keep the spreadsheet. Stopping costs three Moves and a week, against a programme abandoned in month five with two estates billing.
7. If it clears, put the capital question to the founder who signs. About $248,000 leaves the bank before anything serves a request — eighteen machines and a pair of switches, and on eighteen months of runway that is a fair refusal; renting dedicated machines by the month is the way round it, in Move 07.

## Operator's notes
- **Swap:** Price the three largest lines only; that lands within about ten per cent in an afternoon.
- **Do it faster:** Use one calculator, not three. The comparison is owned against what you pay now, not a cheaper landlord.
- **Watch out:** The ops-hours line moves the answer further than anything else in the sheet, and it is the one people guess at. Amortisation over seven years instead of five shifts the total by about three per cent; doubling the hours you think owning will take shifts it by ten times that. Put your own number in before you argue with the conclusion.
- **Leftovers:** The committed-spend agreement bills to the end of its term, and that renewal date is the deadline.

## Rollback
Nothing is ordered and nothing signed, so this Move reverses by changing a cell. The point of no return is the order in Move 06 and the contract in Move 07. Keep dated versions of the sheet, so earlier assumptions can be restored when somebody asks how the decision was reached.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. This Move produces a number and, with it, permission to act or to stop.
