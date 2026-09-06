# 23 · The room in your own building

**Layer:** Site · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Sets out the narrow case for a room in a building you occupy, then prices the suppression, detection, consent and insurance most estimates leave out.

## Leaving from
- **AWS:** Outposts — the closest the provider came to putting its estate in your building, and it came with the building requirements attached.
- **Google Cloud:** Google Distributed Cloud — the same idea, with the same implication that a room has to meet a specification before hardware can go in it.
- **Azure:** Azure Stack HCI and Azure Local — again a supported on-premises footprint, and again the room, the power and the cooling were yours to provide.

## Why this works
There is a real case for a room in a building you occupy, and it is narrow. It needs four things at once: you own the building or hold a long lease on it, there is a second electrical supply from a different substation, the plant room has the structural and cooling capacity for the load, and somebody's job title contains the word facilities. Where all four hold, the economics can be excellent. Where any one of them does not, the missing pieces are expensive, slow and regulated, and the honest conclusion for most companies is no. That conclusion should come from the arithmetic rather than from the tone of this page.

## Before you start

**Access**
- The lease or title, read for what it says about plant, alterations and hours of access
- The building's electrical single-line diagram, and the substation each supply comes from

**Software**
- A cooling load calculation from the per-rack draw in Move 20, done by somebody qualified
- The applicable detection and suppression standards for your jurisdiction, obtained rather than paraphrased

**People**
- A facilities manager, a mechanical and electrical consultant, and an insurance broker, all engaged before any number is published

## The runbook
1. Test the four conditions before pricing anything. Ownership or a long lease, a genuinely separate second supply, plant capacity for the cooling, and a facilities owner for the room. A no on any of them ends the exercise cheaply, which is the point of running it first.
2. Price the fire strategy properly. Detection designed to the applicable standard, clean-agent or water-mist suppression, the annual test and the maintenance contract behind it. This is the line most estimates omit entirely and it is rarely small.
3. Price the electrical works: distribution, the uninterruptible supply and its batteries, and the generator if there is one. A generator brings planning consent and fuel storage approval with it, and both have lead times measured in months rather than weeks.
4. Get an insurance schedule from an underwriter who has seen the actual design. Cover for the equipment, for business interruption and for the building is priced against the fire strategy, and an underwriter's questions will find gaps the design review missed.
5. Add maintenance contracts for every system: cooling, suppression, the uninterruptible supply and the generator. These recur annually for the life of the room and belong in the monthly comparison from Move 22, not in the capital line.
6. Publish the total against the colocation quotation from Move 22, over the same three years, with staff time in both. Let the arithmetic reach the conclusion, and record it either way so the question is not reopened every quarter.

## Operator's notes
- **Swap:** A room in your own building is a much better idea for the second site than the first. Low stakes, real learning, and the failure mode is a restore rather than an outage.
- **Do it faster:** Ask a colocation provider for a tour and take the facilities manager. An hour in a real hall answers more design questions than a week of drawings.
- **Watch out:** Cooling is the constraint that surprises people. A room that is comfortable with four kilowatts of equipment is a different building problem at twenty, and the plant that solves it may not fit where you assumed.
- **Leftovers:** Where the answer is no, the work is not wasted: the cooling load, the draw and the fire requirements are all inputs to the colocation conversation in Move 28.

## Rollback
Nothing is committed until works are ordered or a contract is signed, so this Move is reversed by filing the study and choosing something else. The point of no return is the first irreversible building work — a penetration, a plant order, a consent application — after which the money is spent whether or not the room is finished. Keep the study, the quotations and the underwriter's questions in source control so the case can be restored and re-examined when somebody proposes the room again in two years.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing. This Move is a study, and its most common output is a decision not to spend.
