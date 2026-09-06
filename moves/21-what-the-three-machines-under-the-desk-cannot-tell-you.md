# 21 · What the three machines under the desk cannot tell you

**Layer:** Site · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Writes down on one page what a three-machine desk cluster proved and what it did not, and attaches each remaining gap by name to the Move that closes it.

## Leaving from
- **AWS:** the free tier and a personal account — where most people first ran a cluster, and where nothing about physical failure was ever visible.
- **Google Cloud:** the free tier and a personal project — the same, with a generous allowance that made experimenting feel like operating.
- **Azure:** a free account and a personal subscription — again a place to learn the software and never the hardware underneath it.

## Why this works
The on-ramp in this book's front matter is three refurbished small machines, a managed switch and about eighteen hundred dollars. It is an excellent thing to have done and it proves a great deal: the software estate installs, the cluster forms, the storage layer works, the deployment pipeline reaches it. It also convinces people that the migration is de-risked, which it is not, because nothing about that desk cluster resembles the parts of the estate that fail at three in the morning. This Move writes the gap list down on one page and attaches each item to the Move that closes it, which turns a warning into a map.

## Before you start

**Access**
- The desk cluster, left running at full load for a week rather than benchmarked for ten minutes
- Somewhere to publish one page that the whole team will actually read

**Software**
- A thermal and power meter at the wall, so the numbers on the page are measured rather than asserted
- The wear and error counters from each device in the desk cluster, read rather than assumed

**People**
- Whoever is sponsoring this programme, because this page is what stops the plan being sized off a desk

## The runbook
1. Leave the desk cluster at genuine load for a week and read what happens. Sustained thermals, fan behaviour, the power draw at the wall, and whether anything throttles. A ten-minute benchmark tells you none of this.
2. Read the wear and error counters off every device in it. A year of real writes against a consumer part is the number nobody has, and the desk cluster is the cheapest place to start collecting it.
3. Write the gap list. A fabric wider than one switch, dual power supplies fed from two sources, out-of-band access from another city, drive endurance measured against a year of writes, and the four-week wait for a replacement part are all things the desk cluster cannot show you.
4. Attach each gap to the Move that closes it, by number. The fabric is Moves 12 and 13, the supplies are Move 07 and Move 32, out-of-band is Moves 16 and 40, endurance is Move 09, and the wait for a part is Move 19.
5. State plainly which of the gaps are the reason for Part II. The facility exists to supply power that does not fail, cooling that does not stop and physical access that is controlled, and none of those are things a desk can offer.
6. Publish the page to everyone working on the programme and put a date on it. It gets revisited once, after the first rack is built in Move 36, to see which gaps turned out to matter.

## Operator's notes
- **Swap:** If there is no desk cluster, build one. Eighteen hundred dollars and a weekend is the cheapest possible way to discover that the software estate does not do what you assumed.
- **Do it faster:** The gap list is short and mostly the same for everyone. Start from the six items above and add your own rather than beginning with a blank page.
- **Watch out:** The most seductive false conclusion here is about storage. A replicated storage cluster on three consumer devices works beautifully for a week and tells you nothing about how it behaves after a year of writes and a device failure during recovery.
- **Leftovers:** The desk cluster stays useful for the whole programme as a place to break things. Do not dismantle it when the real hardware arrives.

## Rollback
A page of writing is undone by rewriting it, so there is nothing to reverse here. The point of no return is elsewhere entirely: it is Move 20, which has already been signed by the time most readers reach this page, and Move 28, which commits to a facility. This Move exists to make sure neither of those was signed on the strength of a desk. Keep the page in source control so the original gap list can be restored and compared against what actually went wrong.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing. The desk cluster earns its electricity for the rest of the programme.
