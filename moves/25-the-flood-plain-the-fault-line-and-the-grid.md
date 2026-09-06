# 25 · The flood plain, the fault line and the grid

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Checks the address rather than the brochure: flood history, seismic category, the substation behind each feed, and the fibre routes drawn on a map.

## Leaving from
- **AWS:** Availability Zone selection — you chose a letter, and the physical risk behind it was assessed by somebody else and never shown to you.
- **Google Cloud:** zone selection — the same, with the provider publishing rather less about the physical estate than its competitors.
- **Azure:** availability zone numbers — again a number standing in for a building, and again no way to ask where the fibre enters.

## Why this works
Everything in the facility contract is negotiable except where the building is. A site on a flood plain, on a single substation, or with two fibre entries that leave through the same duct cannot be repaired by better contract terms, and none of those facts appear in a brochure. So the address is checked before the contract is read: the national flood map and the building's own history, the seismic design category and whether cabinets need bracing that must be ordered with them, the substation feeding each supply, and the fibre routes drawn on an actual map. This is also where the two distances that matter get measured.

## Before you start

**Access**
- The exact address and, ideally, the as-built utility drawings, which facilities are reluctant to send
- A site visit booked, because some of these questions are answered by looking at a wall

**Software**
- The national flood map and the applicable seismic hazard data for the address
- A route-tracing tool or a carrier who will draw the fibre path for you rather than describing it as diverse

**People**
- Somebody who has done this before, or a consultant for one day, because the questions are unfamiliar and the answers are consequential

## The runbook
1. Check the flood position at the address rather than the postcode: the published flood map, the building's own history, and what is in the basement. Plant in a basement on a flood plain is a specific and recurring way that a well-run facility fails.
2. Establish the seismic design category and whether the cabinets need bracing or anchoring. If they do, it is ordered with the cabinets rather than discovered on the installation day.
3. Trace the electrical supply back to the substation. Ask which substation feeds each of the two supplies, and get the answer in writing. Two feeds from one substation are one feed with two cables, and this is the single most common misrepresentation in the industry.
4. Get the fibre entries drawn on a map. Diverse entry means two physically separate routes leaving the building in different directions, not two ducts in the same trench. Ask where they converge, because they almost always converge somewhere.
5. Measure the two distances that matter. Road time for a person carrying a spare part, honestly, at the worst time of day. And fibre distance to your users and to the cloud region you are leaving, at roughly one millisecond of round trip per hundred kilometres of glass, measured along the real path rather than the straight line.
6. Score the site and write it down. A site that fails on flood, on substation diversity or on fibre diversity is refused here, before anybody has spent time negotiating a schedule for it.

## Operator's notes
- **Swap:** Where a site is otherwise ideal but has a single substation, ask what the generator arrangement is and how often it is tested under load. A well-maintained generator estate can be a better answer than a second substation nobody checks.
- **Do it faster:** Ask three questions on the first phone call: which substations feed you, where does the fibre enter, and has the building ever flooded. Two of the four candidates will usually remove themselves.
- **Watch out:** Facilities will describe a route as diverse when it is diverse for the first two hundred metres. The question to ask is where the two routes are closest to each other, not whether they are separate.
- **Leftovers:** The latency measurements taken here are the baseline for Move 53 and Move 103. Record them properly rather than reading them off a screen once.

## Rollback
Refusing a site costs nothing except the time spent assessing it, and that time is the cheapest in the whole Part. There is no point of no return here; the nearest one is Move 28, where power is committed to a specific building. Every finding in this Move should be dated and kept, because facilities change hands, and the substation answer that was true in March is worth re-checking at renewal. Keep the assessments in source control so an earlier survey can be restored and compared.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing. This Move spends four days to avoid signing a three-year term against a building on a flood plain.
