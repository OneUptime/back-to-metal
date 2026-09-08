# 04 · The three things you keep renting

**Layer:** Decide · **Leaving:** Nothing — this Move decides what stays rented · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Three capabilities do not come home: the edge, outbound mail and volumetric scrubbing. Naming them now keeps the plan honest.

## Leaving from
- **AWS:** CloudFront and Shield — Shield Advanced bills $3,000 a month on a twelve-month term and attaches only to AWS resources, so it protects a distribution and never a rack.
- **Google Cloud:** Cloud CDN and Cloud Armor — Cloud CDN is a mode on a load balancer backend, so a colocated origin must first become an internet network endpoint group.
- **Azure:** Front Door and its web application firewall — managed rule sets need the Premium tier, and the firewall policy is a resource that outlives its profile.

## Why this works
A plan that pretends everything comes home fails in Stage 5, when somebody notices password resets landing in spam folders and no schedule is left. Three capabilities are bought rather than built, because building them badly is worse than renting them well: a hundred points of presence, a decade of sender reputation, and absorption capacity upstream of your transit. None is expensive next to what it prevents, and all three are worth paying for after the move on the terms you pay now. Deciding here costs two days and removes the largest late surprise.

## Before you start

**Access**
- The three invoice lines for edge, mail and mitigation, and authority to sign

**Software**
- The comparison from Move 03, open for a new permanent line
- The sending domain's current SPF, DKIM and DMARC records

**People**
- Whoever owns the marketing sends, who shares the reputation
- An engineer willing to name the fourth item honestly

## The runbook
1. Price the edge. Take the delivery and egress figures off the invoice from Move 01 and quote three independent vendors against that volume. A content network in front of a rack is the same arrangement as in front of the cloud.
2. Price outbound mail on its own. Transactional sending goes to a provider whose only business is deliverability, and the sending domain's SPF, DKIM and DMARC records point at it. Marketing sends take a separate subdomain.
3. Price mitigation upstream of your transit, the only place it works. Ask the facility and each transit vendor what is included, at what capacity and how it triggers: a hundred-gigabit attack against a ten-gigabit port is decided before it reaches your equipment.
4. Sign all three contracts before the hardware ships, confirming each notice period and minimum term. Mail warm-up takes weeks and cannot begin during an incident.
5. Write the total, about $5,200 a month, into the comparison from Move 03 as a permanent line. Then name the fourth item: whatever the business depends on that nobody here has run, such as a payments integration.

## Operator's notes
- **Swap:** One vendor covering delivery and mitigation halves the contracts, and one outage then takes both.
- **Do it faster:** Ask each vendor for the contract and onboarding checklist in the first message.
- **Watch out:** Facility-included protection is often a null route with a better name. Get in writing what it does to your address.
- **Leftovers:** The cloud edge stays in front of the cloud origin until Move 18 shifts traffic, so two edge bills overlap.

## Rollback
Nothing here touches a running system, so backing out is cancelling inside a notice period. The point of no return arrives later, when the sending domain's records point at the new provider: reputation then accrues on their addresses, and the old standing cannot be restored by changing the records back.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $5,200/mo | $5,200/mo | 0% | 0 min | 2 days | — |

## What you can turn off
Nothing, and that is the point. The cloud's versions switch off in Moves 18 and 20; these three stay on the invoice permanently.
