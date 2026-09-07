# 14 · The first service, end to end

**Layer:** Move · **Leaving:** Managed container compute · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The cheapest stateless service goes first, running on your hardware against the cloud database across the link, with a DNS weight as the way back

## Leaving from
- **AWS:** ECS on Fargate — task credentials come from the metadata endpoint at 169.254.170.2, which does not exist on your nodes.
- **Google Cloud:** Cloud Run — between requests the CPU is throttled to almost nothing unless it is always allocated, so idle timers stop firing.
- **Azure:** Container Apps — the outbound address belongs to the environment, not the app, so rebuilding it changes what partners must allowlist.

## Why this works
The first service to leave is chosen for how little it matters, because its job is to produce evidence rather than savings. Its database stays in the cloud, so the only new variables are the platform, the network path and the identity model. The link adds latency, and the number measured here decides which later services can live with a database on the far side of it and which must move in the same window as their data. The exit is a weighted DNS record: one value, one cache expiry. Nothing else returns as much for as little exposure.

## Before you start

**Access**
- Write access to the Argo CD repository holding the cluster's application manifests
- Permission to edit the weighted DNS records for the service's hostname

**Software**
- `kubectl` and `argocd`, both already pointed at the new cluster
- `dig` for confirming what public resolvers return during the ramp

**People**
- The service owner, told which week the ramp runs and what would stop it
- Whoever maintains egress allowlists on partner systems, warned in advance

## The runbook
1. Choose the cheapest stateless service, not the most interesting one. The right candidate is one whose failure is a shrug and whose owner will not escalate over a slow hour.
2. Commit its manifests to the Argo CD repository and let `argocd` sync them. Keep the connection string on the cloud database, swap anything reading instance metadata for a real credential, and tell the partners who filter on egress addresses.
3. With no live traffic, drive synthetic requests at the new copy and compare latency percentiles against the cloud copy. Write the added milliseconds down.
4. Ramp the weighted record: one per cent, ten, fifty, all of it. Hold each step a business day, confirm the split with `dig`, and stop on any rise in error rate or the ninety-ninth percentile.
5. Soak a week at full weight, watching node disk with `kubectl`: scratch files that were ephemeral on the managed runtime still are, but now they fill a machine you own.
6. Then repeat across the stateless estate, two services a week. After the third, nobody asks for a plan.

## Operator's notes
- **Swap:** If the service sits behind a proxy you already control, shift weight there rather than in DNS; the abort is then immediate, not TTL-bound.
- **Do it faster:** Ramp on a Tuesday morning with the owner beside you. Two people reading one graph is most of what the first one is for.
- **Watch out:** A mean response time stays flat while one pod in four times out. Alert on percentiles and status codes, not averages.
- **Leftovers:** The old record sits at zero weight and the allowlists carry both ranges. Both are free and both get forgotten, so date each.

## Rollback
Every step before the ramp is additive: two copies exist and the cloud copy carries the traffic. Backing out is setting the weighted record to zero and waiting one TTL. There is no point of no return here — no state has moved, so there is nothing to restore. The exception is a partner's allowlist entry: leave the old address in place for the week.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $6,800/mo | $0/mo | 100% | 0 min | 5 days | 1 week |

## What you can turn off
The managed container service, its task revisions and its log retention, once the ramp has held at full weight for a week.
