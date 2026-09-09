# 03 · The number that decides it

**Layer:** Decide · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Three columns, the same operations team and five years of costs. Put colocation and rented metal beside the cloud bill and choose the margin worth moving for.

## Leaving from
- **AWS:** AWS Pricing Calculator — two tools now carry that name, and only the one inside the billing console can see the Savings Plans your account already holds.
- **Google Cloud:** Google Cloud Pricing Calculator — the only discount it models is a committed-use one you pick from a dropdown, and its default machine series earns no sustained-use discount at all.
- **Azure:** Azure Pricing Calculator — signing in and selecting the Enterprise Agreement licensing programme rewrites every price on the page, so an anonymous quote is retail and not yours.

## Why this works
Moves 01 and 02 produced a grouped bill and an inventory that accounts for it. This Move compares three ways to run that estate: the cloud, rented dedicated servers and owned hardware in colocation. Both metal options can keep the existing operations team while reducing the infrastructure bill; renting also keeps the hardware purchase off the opening budget. Put support, retained services and one-time migration work into the comparison, then apply a margin chosen before the figures. Two days of analysis gives the team a decision it can fund and defend.

## Before you start

**Access**
- Three recent invoices at the rate you actually paid, not list
- Quotes for sixteen active machines, two spares and a full rack, plus an equivalent dedicated-server rental

**Software**
- One spreadsheet, three columns: cloud, rented metal and colocation

**People**
- The existing cloud operations lead, to map the team's work onto the new platform

## The runbook
1. Write the decision rule in the spreadsheet before any figure goes in: a metal option must land at least a third under the current cloud cost to justify this programme. Apply the same margin to rented metal and colocation.
2. Fill the cloud column from the three invoices at the rate you actually paid, discounts in and tax out across all columns. One monthly number, checkable against Move 01.
3. Fill the colocation column from hardware and facility quotes: sixteen machines and two spares over sixty months, rack, power, transit, cross-connects and remote hands. Quote equivalent rented metal with traffic and hardware support. For VMs, add the chosen Proxmox support subscription, guest OS and application licences, and off-site VM backup capacity to each applicable column. The published figures describe the container reference estate; price your VM mix separately.
4. Carry the existing operations salary into all three columns. This reference model budgets the same 160 hours a month for each: cloud ops transitions to platform ops, with physical work assigned to the facility's remote hands or the rental provider under the support contract. Validate that assumption with the pilot and the people doing the work. Price setup, training and migration once in the project budget; any measured recurring difference belongs in the monthly line.
5. Add the services that stay rented. Move 04 identifies the edge, outbound mail and scrubbing; later Moves retain archived object storage, a registry, a queue and an off-site backup copy. Their cost is already in the cloud invoice and must remain in both metal columns.
6. Total the three columns and apply the rule. If either metal option clears it, compare the five-year totals and the monthly cash requirement. If neither clears, keep the sheet and revisit it when the estate or quotes change.
7. Choose how to fund the move. Colocation buys the fleet and carries its value forward; rented metal pays monthly and keeps that capital available. Put the actual purchase quote, one-time migration effort and overlap with the cloud bill in front of whoever signs. Move 07 settles the facility and rental terms.

## Operator's notes
- **Swap:** Price the three largest lines only; that lands within about ten per cent in an afternoon.
- **Do it faster:** Use one sheet with the same capacity, support and retained-service assumptions in every column; compare it with the cloud rate you actually pay.
- **Watch out:** Equal recurring hours assumes an existing production team, a standardised platform and contracted physical support. For VMs, include hypervisor updates, guest OS patching and restore drills when validating that assumption. Vary hours, rental rates and hardware life in the sheet; setup and migration are one-time work.
- **Leftovers:** The committed-spend agreement bills to the end of its term, and that renewal date is the deadline.

## Rollback
Nothing is ordered and nothing signed, so this Move reverses by changing a cell. The point of no return is the order in Move 06 and the contract in Move 07. Keep dated versions of the sheet, so earlier assumptions can be restored when somebody asks how the decision was reached.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. This Move produces a number and, with it, permission to act or to stop.
