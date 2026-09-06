# 32 · Two feeds, one of which you have tested

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Establishes that a dual-fed cabinet is worth one feed at the derate, puts single-supply equipment behind a transfer switch, and pulls the A feed to prove it.

## Leaving from
- **AWS:** Availability Zones — the redundancy was inside the zone and you never saw it, tested it, or paid for it as a line.
- **Google Cloud:** zones — the same, with the provider's own testing invisible and the failure domains described rather than demonstrated.
- **Azure:** availability zones and fault domains — again resilience as a property of the platform, which is why an untested B feed feels acceptable to people arriving from it.

## Why this works
A cabinet with two feeds looks like twice the power and is not. The usable budget is one feed at the derate, because the whole point is that either feed can carry the load alone, so a pair of 8.6 kilowatt feeds is an 8.6 kilowatt cabinet and each distribution unit runs at around forty per cent in normal operation. That arithmetic is routinely got wrong in the direction that produces an outage. The second half of this Move is the part almost nobody does: pulling the A feed with the cabinet fully loaded and nothing yet depending on it, and measuring what the B feed actually carried and what tripped.

## Before you start

**Access**
- A commissioning window with the cabinet loaded and no production on it
- Permission from the facility to open a breaker on the A feed, agreed in advance

**Software**
- Per-outlet or per-feed metering readings, recorded before and during the test
- A rack transfer switch for the single-supply equipment, ordered with the distribution units

**People**
- A second person on site during the test, because the failure mode is a dark cabinet

## The runbook
1. Recompute the cabinet budget as one feed at the derate rather than the sum of the two. If the plan from Move 31 exceeded that figure, fix it now, before anything is racked against it.
2. Wire every dual-supply machine to both feeds, with one supply on each distribution unit, and record which outlet each cable occupies in the cabinet plan.
3. Deal with the single-supply equipment properly. A console server, a small access switch or an out-of-band unit with one supply goes behind a rack transfer switch fed from both strips, rather than being assigned to a feed and hoped about.
4. Load the cabinet fully and take a baseline reading per feed. This number is the one you will compare against for the rest of the cabinet's life.
5. Pull the A feed. Open the breaker with the cabinet loaded and watch what happens: the reading on B, anything that restarted, anything that did not come back, and whether the transfer switch carried its load without interruption. Record the numbers rather than the impression.
6. Restore the A feed, confirm both strips return to their baseline, and write up what tripped. Every fault this test finds is a fault you would otherwise have found during a real supply failure, at three in the morning, with production on the cabinet.

## Operator's notes
- **Swap:** Where the facility will not permit a live feed test, ask them to schedule it during their own maintenance. Failing that, test at the distribution unit level rather than not at all.
- **Do it faster:** Do this on the day the first cabinet is loaded and before anything is installed on the machines. It is a two-hour test that becomes a three-week negotiation once production depends on the cabinet.
- **Watch out:** Some power supplies draw noticeably more from one feed when the other is absent, so the B feed reading under test can exceed half the normal total by more than expected. That is the number the budget has to survive.
- **Leftovers:** Test readings are evidence. Keep them, because they are what you compare against when a feed reading drifts in year two.

## Rollback
The test is reversed by closing the breaker, and the wiring decisions are reversed by moving cables. Nothing here is permanent. The point of no return is the day production depends on the cabinet, after which this test stops being a commissioning step and becomes a change with a risk assessment. Keep the baseline readings and the cabinet plan in source control so the commissioned state can be restored and compared when something is rewired later.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. This Move spends a day proving that the resilience you are paying for exists.
