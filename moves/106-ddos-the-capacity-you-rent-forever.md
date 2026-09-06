# 106 · DDoS: the capacity you rent forever

**Layer:** Edge · **Leaving:** Managed DDoS protection subscriptions · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Rents mitigation capacity, because a volumetric attack saturates transit upstream of every device you own.

## Leaving from
- **AWS:** Shield Advanced — an annual commitment with a response team attached.
- **Google Cloud:** Cloud Armor with its managed protection tier — the same shape, sold as a subscription.
- **Azure:** DDoS Protection — the same again, priced per protected plan with an annual term.

## Why this works
A volumetric attack does not reach your firewall. It saturates your transit, upstream of every device you own, which means no equipment you buy can mitigate it. The capacity to absorb it is the product, and it is rented. This Move therefore prices four options with time-to-mitigate against each, kills origin secrecy as a strategy, and reaches a keep-paying verdict. The reason it is irreversible is commercial rather than technical: announcements and tunnels can be withdrawn in an afternoon, but diversion authority is a signed contract with a minimum term and a notice period.

## Before you start

**Access**
- The address space and network number from Move 91, since prefix-level protection uses both
- The transit contracts from Move 93, because inline scrubbing may be available there

**Software**
- An origin access list, refreshed as vendor ranges change, replacing origin secrecy entirely
- A diversion mechanism configured and tested, whether tunnelled or announced

**People**
- Whoever can authorise diversion at three in the morning, with a deputy and a telephone number

## The runbook
1. Price the four options with time-to-mitigate against each: transit with inline scrubbing, a scrubbing provider reached over a tunnel or a private interconnect with on-demand diversion, always-on proxying behind the network from Move 105, and prefix-level protection using your own address space and routing.
2. Kill origin secrecy as a strategy. It fails to the first certificate transparency log entry, the first misconfigured subdomain and the first email header. Replace it with an origin access list that only accepts the mitigation vendor's ranges, and a process to refresh those ranges when they change.
3. Choose the diversion mechanism and test it during business hours. A diversion that has never been performed takes an hour longer than it should, and the hour is during an attack.
4. Establish who can authorise diversion out of hours, with a deputy, a telephone number and an agreed form of words. Vendors will not divert on the word of somebody they cannot identify.
5. Read the commitment terms. All three cloud subscriptions are annual, and what replaces them has the same shape, so the exit cost is a notice period rather than a switch.
6. Set the detection thresholds and rehearse the runbook once, end to end, including the return to normal routing afterwards, which is the half people forget.
7. Put the recurring cost in Move 116's list of things you deliberately keep, and in Move 120's model as a permanent line.

## Operator's notes
- **Swap:** For a small estate already behind an always-on proxying network from Move 105, that may be the whole answer and no separate subscription is needed. Confirm what the proxy's own terms cover.
- **Do it faster:** Get the tunnels or the announcements configured and tested before you need them. Configuring a diversion path during an attack is not a plan.
- **Watch out:** Prefix-level protection depends on your announcements being accepted, which depends on the routing records from Move 91 being correct. Validate them before relying on this path.
- **Leftovers:** The provider subscription runs to the end of its annual term whether or not anything is behind it, which is a line Move 120 has to carry.

## Rollback
The technical parts are reversible in an afternoon, but this Move is irreversible in the way that counts: diversion authority is a signed contract with a minimum term and a notice period, so leaving costs the remainder of the term. The point of no return is that signature. Nothing here holds data, so there is nothing to restore; what has to be kept is the origin access list, which is the thing that must be current before an attack rather than during one.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,000/mo | $2,400/mo | 20% | 0 min | 1 week | 4 weeks |

## What you can turn off
The provider subscription at the end of its annual term, and nothing before it. This is a cost you keep paying, deliberately.
