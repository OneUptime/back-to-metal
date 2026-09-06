# 28 · Committed kilowatts, metered kilowatts and the derate

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Reads the power schedule rather than the price, and fixes the billing model, the committed figure and the continuous-load derate in writing.

## Leaving from
- **AWS:** per-hour instance pricing — power was inside the rate, invisible, and never something you committed to in advance.
- **Google Cloud:** per-second billing with sustained use discounts — the same invisibility, with the discount applied after the fact rather than committed up front.
- **Azure:** per-hour pricing with reservations — again power inside the rate, and again no schedule to read.

## Why this works
The headline price of a cabinet is not the number that governs your bill. The power schedule is. There are three billing models in common use — a flat charge against a committed figure, metered consumption with a committed floor, and a hybrid with an overage rate — and they behave completely differently when you grow. Underneath that sits the derate: the eighty per cent continuous-load convention is an artefact of one country's wiring code and has no direct equivalent in others, so one facility may sell against the full breaker rating where another will not. The only number that matters is the one the contract says you may draw continuously.

## Before you start

**Access**
- The per-cabinet draw from Move 20 at expected and at peak load
- The facility's power schedule as a document, not as a paragraph in a proposal

**Software**
- The three billing models written out with your own numbers substituted into each
- A note of what happens at the commitment boundary in each model: alarm, invoice, or breaker

**People**
- Counsel to read the schedule with you, because the words that matter here are contractual rather than technical

## The runbook
1. Identify which billing model the schedule uses before discussing price. A flat charge against a commitment and a metered charge with a floor produce very different bills for the same estate, and the difference grows with you.
2. Establish what the facility does when you exceed the commitment. Some alarm and call you, some invoice at an overage rate, and some trip the breaker. Get the answer in writing, because the third one is an outage caused by a contract term.
3. Fix the derate in the contract. Ask directly what you are permitted to draw continuously per feed, as a number in kilowatts, and have it written into the schedule rather than inferred from a breaker rating.
4. Set the committed figure for the first cabinet from Move 20, with honest headroom. Committing too low makes growth an amendment; committing too high pays for power you never draw, and most schedules have no mechanism to reduce a commitment.
5. Negotiate a written right to increase power mid-term, with a stated notice period and a stated price. This is worth more than a discount on the initial rate and it is routinely omitted.
6. Get the metering point identified. Power measured at the cabinet and power measured at the distribution board are different numbers, and only one of them is yours.

## Operator's notes
- **Swap:** Where the facility will only sell a flat commitment, size it against the year-two estate rather than the year-one one, and negotiate the increase right anyway. Paying for a little unused power is cheaper than an amendment under time pressure.
- **Do it faster:** Ask for a worked example invoice at your committed figure and at one hundred and twenty per cent of it. It settles the model question in an afternoon.
- **Watch out:** Power and cooling are frequently sold as one number and metered as two. Check whether cooling is included, charged as a factor on power, or billed separately against a facility efficiency figure that can change.
- **Leftovers:** Cloud commitments continue in parallel through the whole programme. You will pay both for a period, and Move 20 has already budgeted for it.

## Rollback
This Move is irreversible in the way that matters: a signed power commitment is a monthly charge for the term, and most schedules have no mechanism to reduce it. The point of no return is the signature on the schedule, not the day the machines arrive. What is still reversible is where the machines go, since Move 22 kept a rented-metal option alive. Keep the schedule, the worked examples and the negotiation record in source control so the agreed position can be restored when the facility's billing disagrees with it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | 4 to 8 weeks |

## What you can turn off
Nothing yet. This Move adds a monthly bill that runs in parallel with the cloud one until Part VI.
