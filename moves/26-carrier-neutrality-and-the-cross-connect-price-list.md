# 26 · Carrier neutrality and the cross-connect price list

**Layer:** Site · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Counts the carriers that will sell at your volume and prices every cross-connect you will need across three years against the facility's own list.

## Leaving from
- **AWS:** Direct Connect — a port you ordered through a console, with the physical cross-connect ordered separately and forgotten about.
- **Google Cloud:** Cloud Interconnect — the same shape, with a dedicated and a partner variant, and the partner one hiding the physical layer completely.
- **Azure:** ExpressRoute — again a logical circuit, and again a cross-connect underneath it that somebody had to order in a building.

## Why this works
Carrier neutral is a marketing term that means the facility will let other people's fibre into the building. What matters is narrower: which carriers have live fibre in the meet-me room today, and which of those will sell to a customer of your size. The second list is always much shorter than the first. Underneath that sits a price list nobody quotes in the headline number — a cross-connect is commonly fifty to three hundred and fifty dollars a month each, plus installation, recurring forever, and outside the cabinet price. You will need more of them than you think.

## Before you start

**Access**
- The carrier list for the specific building, not the operator's national list
- The facility's cross-connect price list, in writing, including installation and disconnection charges

**Software**
- A three-year plan of every cross-connect the estate will need, drawn as a list rather than remembered
- The cloud provider's own documentation on how their authorisation and assignment paperwork expires

**People**
- Whoever will negotiate the facility contract in Move 30, because cross-connects belong in that negotiation

## The runbook
1. Ask for the list of carriers with live fibre in the meet-me room. Then ask each of them, separately, whether they will sell at your committed volume. This is the list that matters and it is usually three or four names rather than thirty.
2. Count every cross-connect you will need over three years: two transit providers, a peering fabric port, the private interconnect back to the cloud you are leaving, and one per additional cabinet. Missing any of these turns a monthly number into a surprise.
3. Price them against the facility's own list, with installation and disconnection charges included. Ask specifically whether the price is per connection or per pair, because the two conventions differ by a factor of two.
4. Negotiate the cross-connect cost inside the facility agreement rather than afterwards. It is the line facilities are most willing to move, and once the contract is signed it is the line they are least willing to move.
5. Time the cloud on-ramp paperwork properly. The authorisation letter and connecting facility assignment that a cloud provider issues expires after ninety days if the cross-connect has not been completed, so it is ordered when the cabinet is ready and not when the contract is signed.
6. Record which carrier terminates in which position, because Move 37 will need it and Move 93 will order transit against it.

## Operator's notes
- **Swap:** Where a building has few carriers, a wavelength or dark fibre to a nearby carrier hotel can restore the choice. It costs more per month and it is better than being captive to one provider.
- **Do it faster:** Ask the facility for a copy of a recent, redacted cross-connect invoice. It answers the per-connection question and several others in one document.
- **Watch out:** Some facilities charge to disconnect as well as to install, and some require notice. Both belong in the exit runbook that Move 30 writes.
- **Leftovers:** The cloud interconnect on the far side keeps billing until Part VI has moved the traffic and Part VII closes the account. Do not cancel it early to save a few hundred dollars.

## Rollback
Nothing is committed until the facility contract is signed in Move 30 and the first cross-connect is ordered. Cancelling an ordered cross-connect before installation is usually free and after it is usually a disconnection fee. The point of no return, such as it is, is the installation itself, and it is small money. Keep the carrier list, the price list and the cross-connect plan in source control so the original commercial position can be restored when a renewal quotes different numbers.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | 2 to 4 weeks |

## What you can turn off
Nothing yet. The cloud interconnect stays until Part VI has moved the traffic across it.
