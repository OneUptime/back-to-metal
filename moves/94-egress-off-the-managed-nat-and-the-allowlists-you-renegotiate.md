# 94 · Egress off the managed NAT, and the allowlists you renegotiate

**Layer:** Edge · **Leaving:** Managed NAT gateways and provider-assigned egress addresses · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Sends pods out through node addresses, gives fixed-source workloads an explicit SNAT hop, and renegotiates every partner allowlist before the first packet moves.

## Leaving from
- **AWS:** NAT Gateway — pre-allocates translation ports per instance, so exhaustion is a limit you can compute in advance.
- **Google Cloud:** Cloud NAT — a shared pool where one noisy workload can exhaust translation capacity for everything else behind it.
- **Azure:** NAT Gateway with public IP prefixes — a similar pooled model, with the same failure shape and the same need to reserve ports explicitly.

## Why this works
Most pods do not need a fixed source address and can leave through the address of the machine they are on, which is simpler and free. A minority do need one, because a partner's firewall has their address written into it, and those get an explicit translation hop with a stable address. The hard part of this Move is not the networking at all. It is that every partner, webhook endpoint and payment gateway with your current address in an allowlist has to be renegotiated onto a hostname or a new range, and each of those sits on somebody else's change calendar.

## Before you start

**Access**
- The allowlist inventory started in Move 39, with a named contact for every entry
- Public address space from Move 91 and, for the egress-heavy workloads, the second family from Move 92

**Software**
- An egress gateway or a dedicated translation hop, configured with a stable address
- Port budget arithmetic per workload, so exhaustion is computed rather than experienced

**People**
- Whoever owns each partner relationship, because this is their change request, not yours

## The runbook
1. Start the allowlist renegotiation first and treat it as the critical path. Assume a quarter for the long tail; some partners take six weeks to change a firewall rule and some require a contract amendment.
2. Ask every partner for a hostname rather than an address wherever they will accept one. It is the change that stops this Move recurring the next time anything moves.
3. Classify the workloads. Those that do not need a fixed source leave through node addresses, which is most of them and costs nothing.
4. Give the fixed-source workloads an explicit translation hop with a stable address from Move 91. This is a deliberate, small set rather than a default for everything.
5. Do the port arithmetic. Translation state is per source address and port, and a workload opening thousands of short-lived connections exhausts a pool. One provider pre-allocates per instance so the limit is computable; another shares a pool so a noisy neighbour exhausts it for everyone.
6. Where a workload is genuinely egress-heavy, give it public addresses in the second family from Move 92 instead of translating it at all. That removes the state entirely.
7. Expect established connections to reset when an assignment moves, because translation state does not migrate. That is the user-visible cost of this Move rather than a downtime window, and it is worth telling people about in advance.

## Operator's notes
- **Swap:** Where a single partner refuses to move off an address allowlist, keep one small cloud footprint with that address and route only that traffic through it. It is ugly and it is cheaper than losing the integration.
- **Do it faster:** Send the allowlist change requests on the day you start this Part, not when the engineering is ready. The engineering takes two weeks and the partners take a quarter.
- **Watch out:** Webhook senders often verify the source address as well as the signature. A webhook that stops arriving silently is the classic symptom, and nobody notices until a reconciliation runs.
- **Leftovers:** The managed translation gateway bills per hour and per gigabyte, and both continue until the last workload has moved.

## Rollback
For thirty days the managed path still exists and a workload is moved back by changing its egress policy, so this is reversible per workload rather than all at once. The point of no return is the release of the provider-assigned addresses, which cannot be reclaimed once released and which is deliberately deferred to Part VII. Keep the allowlist inventory current, because it is the document a restore of the old egress path depends on.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,340/mo | $0/mo | 100% | 0 min | 2 weeks | 30 days |

## What you can turn off
The managed translation gateways, thirty days after the last workload moved and every partner has confirmed the new source.
