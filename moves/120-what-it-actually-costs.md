# 120 · What it actually costs

**Layer:** Watch · **Leaving:** The provider's cost explorer, billing exports, budgets and cost-advisory service · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Prices the cluster from real invoices, counting power, transit burst, spares, support contracts, audit hours, the rota and the months you paid twice.

## Leaving from
- **AWS:** Cost Explorer with Cost and Usage Reports and Trusted Advisor — a cost model somebody else maintained for you.
- **Google Cloud:** Cloud Billing reports with the Recommender — the same, with recommendations attached.
- **Azure:** Cost Management with Advisor — the same again, and the same absence once the account closes.

## Why this works
Every repatriation comparison you have read omits the same lines, and this Move is where the honest number gets built from real invoices rather than from a model. Power at the committed figure from Move 28, transit at the percentile from Move 93, the spares holding from Move 19, the support subscriptions from Move 112, audit hours from Move 119, the rota from Move 113, and the months where both estates were paid for at once. The last of those is the one that makes a good migration look bad in month six and is always left out. If a cost tool is used, the default on-premises prices in it are placeholders and have to be replaced.

## Before you start

**Access**
- Real invoices for a full quarter, from every supplier, not estimates
- The discounted rate you actually paid on the cloud, not list, so the comparison is fair

**Software**
- A custom pricing file if a cost tool is used, because the defaults are placeholders
- A showback model against scarce capacity rather than against money

**People**
- Somebody from finance to check the invoices with you, because this number will be quoted in board papers

## The runbook
1. Build the cost model from invoices. Every supplier, a full quarter, actual amounts. Estimates in this Move undermine every other number in the book.
2. Replace the default prices in any cost tool. On-premises prices in these tools are placeholders and using them produces a confident wrong answer.
3. Count the lines that get omitted: committed power from Move 28, transit burst at the percentile from Move 93, the spares holding from Move 19, support subscriptions from Move 112, audit hours from Move 119 and the rota from Move 113.
4. Count the double-running months explicitly. Both estates were paid for during Parts V and VI, and that is real money that belongs in the programme's total rather than outside it.
5. Compare against the discounted rate you actually paid rather than list price. A comparison against list flatters the result and will be dismantled by the first person who checks it.
6. Do showback against scarce capacity rather than against money. On a fixed fleet the constraint is cores, memory and storage, and charging teams for those changes behaviour in a way that charging them for currency does not.
7. Write the refresh policy: what is replaced when, staggered so that year five is a cadence rather than a cliff, with the money set aside annually rather than found in a crisis.

## Operator's notes
- **Swap:** Where the estate is small, a spreadsheet updated quarterly beats any tool. The discipline is counting everything, not the software you count it in.
- **Do it faster:** Build it once properly and then update it quarterly. The first build is two weeks and each update is an afternoon.
- **Watch out:** Amortisation choices change the answer substantially. Pick a life, state it, and use the same one on both sides of the comparison.
- **Leftovers:** The provider's billing exports keep writing to a bucket after everything else has gone, and that bucket bills.

## Rollback
A cost model is corrected by correcting it and there is nothing to reverse. The point of no return does not exist here, though the number this Move produces will be quoted for years, which is an argument for building it carefully rather than quickly. Keep every quarterly version in source control so the model at any past date can be restored and compared, which is how you answer the question of whether the programme delivered what it promised.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $74,013/mo | $38,337/mo | 48% | 0 min | 2 weeks | — |

## What you can turn off
The cost-advisory services and, eventually, the billing exports — but not until Move 122 has taken the billing history you will need for the comparison.
