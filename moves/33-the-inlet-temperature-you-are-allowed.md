# 33 · The inlet temperature you are allowed

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Commits the inlet temperature at the top of the cabinet inside containment, then fixes the blanking, brush strips and aisle orientation that make it achievable.

## Leaving from
- **AWS:** EC2 host management — thermal behaviour was the provider's problem and surfaced to you, at most, as a retirement notice.
- **Google Cloud:** Compute Engine host maintenance — the same, with live migration hiding thermal events entirely.
- **Azure:** Virtual Machines health events — again somebody else's cooling, and the reason nobody arriving from a cloud owns a temperature probe.

## Why this works
A cooling commitment measured as a room average at the cooling unit's return tells you nothing about the machine at the top of your cabinet, which is where the air is hottest and where the failures start. So the commitment is written at the point that matters: inlet air at the top of the cabinet, inside containment. The envelope itself is well established — the recommended band is eighteen to twenty-seven degrees and mainstream equipment is allowable considerably higher — and in practice the binding constraint is rarely temperature at all. It is the facility's density limit per cabinet, which is a different number and one that is frequently discovered late.

## Before you start

**Access**
- The facility's cooling commitment as drafted, with its measurement point stated
- The density limit per cabinet in kilowatts, which is often lower than the power commitment implies

**Software**
- A temperature probe or a set of them, because a thermal survey done by hand is not a survey
- Blanking panels and brush strips ordered with the cabinet rather than after the first hot spot

**People**
- The facility's engineer, walked around the cabinet with you rather than consulted by email

## The runbook
1. Get the cooling commitment written at your inlet, at the top of the cabinet, inside containment. If the facility will only commit to a room average, understand that you are buying a number that does not describe your equipment.
2. Set the envelope explicitly rather than by folklore. Write down the recommended band you intend to run in and the allowable maximum for your class of equipment, so that a warm day is a known condition rather than an incident.
3. Confirm the density limit per cabinet and check it against Move 31's budget. A hall rated at five kilowatts a cabinet will not take a cabinet designed for eight, whatever the power schedule says you may draw.
4. Fix the airflow discipline before the thermal survey, not after. Consistent hot and cold aisle orientation, blanking panels in every unused rack unit, brush strips on every cable cut-out, and no cabinet drawing its air from the hot aisle.
5. Run a thermal survey with a probe, at the bottom, middle and top of the cabinet, front and rear, at full load. Record the numbers against the commitment.
6. Repeat the survey after Move 36 has racked the cabinet properly and again in the warmest month. A cabinet that is comfortable in February is not evidence of anything.

## Operator's notes
- **Swap:** Where containment is not available, a cabinet with good blanking in a well-run hall is usually acceptable. Where neither is available, reduce the density rather than accepting the temperature.
- **Do it faster:** Buy a handful of small logging probes and leave them in the cabinet permanently. Move 114 will alert on them and you will never have to run a survey again.
- **Watch out:** Running at the top of the allowable envelope saves the facility money and costs you fan power, which you pay for. Warmer is not automatically cheaper once the draw is yours.
- **Leftovers:** Blanking panels are the cheapest thermal improvement available and the one most often left in a box. Fit them all, including the ones for gaps you intend to fill next year.

## Rollback
Every mitigation here is physical and reversible: panels come out, probes move, the aisle orientation is a decision about which way cabinets face. The point of no return is the cabinet's orientation once it is bolted down and cabled, which is an afternoon's work to change on day one and a serious disruption once populated. Keep the survey readings in source control so the commissioned thermal baseline can be restored and compared when a machine starts throttling next summer.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. Getting this wrong shortens the life of everything Move 20 bought.
