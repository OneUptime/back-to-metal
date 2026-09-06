# 13 · The switch, and the software running on it

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Buys tier-one merchant-silicon leaves running a supported network operating system, and checks the quoted licence tier for the routing features assumed.

## Leaving from
- **AWS:** VPC route tables and Transit Gateway — routing was a set of API objects and the forwarding plane was invisible.
- **Google Cloud:** VPC routes and Cloud Router — the same, with a managed router that spoke BGP on your behalf without you configuring one.
- **Azure:** Route tables and Virtual WAN — again managed routing, and again nothing you could log into when a path went wrong.

## Why this works
The switch is the one device in this book that a small team should refuse to be clever about. This book buys tier-one merchant-silicon leaves running a vendor network operating system, and the recommendation is Arista EOS on Trident-class hardware, because its routing and EVPN behaviour is documented, supported and dull, and dull is the property you want from the thing every packet crosses. A commercially supported Enterprise SONiC distribution is the reasonable alternative where procurement requires an open operating system. Community SONiC and Cumulus Linux are both real, and both are set aside here — the latter because its current release supports only one silicon vendor, which removes the point of merchant silicon.

## Before you start

**Access**
- The topology and redundancy decision from Move 12, since it changes which features you need licensed
- Loan units of the exact model being quoted, not a similar one from the same family

**Software**
- The vendor's licence matrix for the exact part number, and the release notes for the version you intend to run
- A traffic generator capable of producing the microbursts you measured, rather than a steady stream

**People**
- Somebody in procurement who can get a licensing answer in writing before the order goes in

## The runbook
1. Fix port count and speed against three years of growth from Move 11, not against today. Twenty-five gigabit to the host with hundred gigabit uplinks is the sensible floor, and the spare ports you leave are the cheapest capacity in the estate.
2. Check buffer depth against the microbursts you measured rather than against a rule of thumb. Shallow-buffer leaves are fine for most traffic and are not fine for a storage cluster that synchronises writes across racks.
3. Read the licence tier on the exact part number being quoted. Routing protocols, EVPN, telemetry streaming and even some monitoring features sit behind tiers, the tiers are renamed between generations, and the detail that catches people is that the base tier on a quote is rarely the tier the design assumes.
4. Run the loan units against your own design for a week. Configure the routing you intend to run, pull a cable, pull a power lead, upgrade the operating system, and watch what the fabric does. A switch is bought for its behaviour when something breaks.
5. Confirm the automation path you will actually use — a configuration API, a structured data model, and a way to diff intended against running state. Configuring switches by hand is how a two-switch fabric drifts into two different fabrics.
6. Get the licensing and support answer in writing, including what a hardware replacement looks like and how long the model will be supported. That horizon dates the fabric more surely than its speed does.

## Operator's notes
- **Swap:** For a single-rack estate that will never grow, a pair of well-supported one-rack-unit leaves from any tier-one vendor is sufficient, and the operating system argument matters much less than the support contract.
- **Do it faster:** Ask for the loan units at the same time as the quote. The evaluation and the negotiation then run in parallel rather than in series, which is worth two weeks.
- **Watch out:** The same model number can ship with different silicon in different regions or generations. Confirm the exact silicon on the quote, because the feature set and the buffer behaviour follow it, not the badge.
- **Leftovers:** Evaluation licences expire and take features with them. If a loan unit becomes a production unit, make the licence conversion a purchase-order line rather than a surprise.

## Rollback
Until the order is signed, changing switch vendor costs a fortnight of evaluation and nothing else. The point of no return is that signature: after it, a fabric that cannot do what the design assumed is either a licence purchase at list price or a replacement, and the optics you bought in Move 15 are coded for a vendor. Keep the loan-unit test results, the licence matrix and the running configurations in source control, so a known good configuration can be restored on a switch that has been replaced under warranty.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 weeks | 2 weeks |

## What you can turn off
Nothing yet. This Move buys the thing every packet in Parts III to VI will cross.
