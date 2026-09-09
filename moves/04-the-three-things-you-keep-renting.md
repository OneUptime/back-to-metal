# 04 · The three things you keep renting

**Layer:** Decide · **Leaving:** Nothing — this Move decides what stays rented · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Until a contract is signed

> Three capabilities do not come home: the edge, outbound mail and volumetric scrubbing. Naming them now keeps the plan honest.

## Leaving from
- **AWS:** CloudFront and Shield — Shield Advanced starts at $3,000 a month on a twelve-month term; a protected distribution can front a rack, but does not protect direct rack traffic.
- **Google Cloud:** Cloud CDN and Cloud Armor — Cloud CDN is a mode on a load balancer backend, so a colocated origin must first become an internet network endpoint group.
- **Azure:** Front Door and its web application firewall — Standard supports custom rules only; Premium includes managed rule sets, and the firewall policy is a separate resource.

## Why this works
A plan that pretends everything comes home can fail when password resets stop arriving or an attack fills the transit link. Keep three capabilities in the budget: distributed content delivery, outbound mail delivery and volumetric protection upstream of the rack. Existing providers may already serve the new origin; a hardware migration does not itself require changing them. Check coverage, capacity and terms now, and carry the quoted cost into the decision. Two days is the reference planning effort, not a promise about onboarding time.

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
1. Price the edge. Take delivery and egress figures from Move 01 and compare the existing vendor with alternatives at that volume. Confirm external-origin support, origin authentication and the rack's transit charges on cache misses.
2. Price outbound mail on its own. Keep the current sending provider if it meets the requirements. Check SPF authorises its senders, DKIM signs correctly and the authenticated domain aligns with DMARC; marketing sends use a separate subdomain. Plan a staged migration only if the provider changes.
3. Price mitigation upstream of your transit, the only place it works. Ask the facility and each transit vendor what is included, at what capacity and how it triggers: a hundred-gigabit attack against a ten-gigabit port is decided before it reaches your equipment.
4. Confirm all three contracts before the hardware ships, including notice periods, minimum terms and activation dates. New dedicated sending IPs can need weeks of warm-up; agree the plan before shifting mail, and keep the working sender available during it.
5. Write the quoted total into the comparison from Move 03 as a permanent line; the reference allows $5,200 a month. Then name any additional retained service the business depends on, such as a payments integration.

## Operator's notes
- **Swap:** One vendor can cover delivery and mitigation, reducing contracts while putting both services behind the same provider.
- **Do it faster:** Ask each vendor for the contract and onboarding checklist in the first message.
- **Watch out:** Facility-included protection is often a null route with a better name. Get in writing what it does to your address.
- **Leftovers:** Keep the current edge serving the cloud origin until Move 18. Changing vendors can create overlapping bills; keeping the same edge avoids a second delivery contract.

## Rollback
Planning is reversible; the contractual point of no return is accepting a binding term, with cancellation charges governed by that agreement. If mail later moves, retain the old sender, authentication records and suppression lists until delivery is proved. Returning means restoring routing and valid authentication, then checking bounces and complaints. Domain reputation follows the domain; a new provider's IP reputation is a separate consideration.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $5,200/mo | $5,200/mo | 0% | 0 min | 2 days | — |

## What you can turn off
Nothing yet. Retire superseded providers only after their replacements work; any existing edge or mail service kept in the plan stays on the invoice.
