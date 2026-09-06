# 91 · Your own ASN, a /24 and the address space you already have

**Layer:** Edge · **Leaving:** Provider-assigned public IP addresses and bring-your-own-IP programmes · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Takes an ASN and provider-independent address space, and registers the IRR and RPKI objects that decide whether anyone will accept the prefix.

## Leaving from
- **AWS:** Elastic IP addresses and the bring-your-own-IP programme — which requires a route origin authorisation naming the provider's own network as the origin.
- **Google Cloud:** external addresses and bring-your-own-IP — the same requirement, expressed through its own onboarding flow.
- **Azure:** public IP addresses and custom IP prefixes — the same again, and the same trap when you publish your own authorisation too early.

## Why this works
Addresses you rent are addresses that end when the account does. Provider-independent space is yours, and taking it has three parts: membership of the registry for your region, an autonomous system number, and the address space itself. None of that is difficult and all of it is slow, which is why this Move opens the Part and why Move 39 told you to start it months ago. The part that is easy to get wrong is the routing security records, because a route origin authorisation naming your own network, published while a provider is still announcing the prefix on your behalf, invalidates the announcement carrying your production traffic.

## Before you start

**Access**
- Registry membership under way, started in Move 39, with the legal entity documentation ready
- Any existing address space you already hold, and evidence of the right to use it

**Software**
- The registry's portal for route objects and origin authorisations, and a validator to check what you publish
- A written plan for the transition period during which a provider still announces the prefix

**People**
- Whoever can sign registry agreements, and whoever will be listed as the technical contact for the next decade

## The runbook
1. Complete the registry membership and take an autonomous system number. This is paperwork against a wait measured in weeks, and nothing else in this Part can start without it.
2. Get the address space. An address allocation for a member is a fixed size and an assignment to an end user is a different, smaller one; the sizes are documented and worth reading rather than assuming. For legacy address space, the waiting list has a real eligibility condition — in one region only a member that has never held an allocation may join a queue currently measured in years — so the transfer market is usually the realistic path.
3. Publish route objects in the routing registry so that upstreams will build filters that accept your prefix. A prefix with no route object is a prefix most transit providers will drop.
4. Publish route origin authorisations, and choose the maximum length deliberately. Too tight and you cannot announce more specific prefixes during an attack; too loose and you have authorised a hijack.
5. Handle the transition carefully. While a provider is still announcing your prefix under its bring-your-own-IP programme, the authorisation must name that provider's network as the origin. Publishing your own too early invalidates the live announcement, which is an outage on production traffic caused by a routing record.
6. Validate what you published from outside your own network, using a public validator, before relying on any of it.
7. Announce nothing yet. This Move is registration only; the announcements are Move 95 and Move 96.

## Operator's notes
- **Swap:** For a small estate, addresses from your transit provider are perfectly workable and cost nothing in paperwork. What you lose is the ability to change transit provider without renumbering, which is the whole argument for this Move.
- **Do it faster:** Start the registry membership on the day you read Move 39. Everything here is queue time and the queue does not care how urgent you are.
- **Watch out:** The technical contact on a registry record is a person who will be emailed about outages for years. Use a role address that survives them leaving.
- **Leftovers:** Provider-assigned addresses stay assigned and stay billing until Part VII, and releasing one early means it is gone for good.

## Rollback
Nothing is announced and nothing is serving, so this Move is reversed by withdrawing registry objects, and membership can be relinquished. There is no point of no return here. The one genuinely dangerous action is publishing an origin authorisation that contradicts a live announcement, and that is reversed by restoring the previous record — which propagates in minutes but not instantly, so it is checked before publication rather than after.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | 6 to 12 weeks |

## What you can turn off
Nothing yet. Provider addresses carry every user you have until Move 103.
