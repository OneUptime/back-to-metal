# 17 · The front door

**Layer:** Run · **Leaving:** Managed layer-7 balancers and certificate services · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The new edge goes up beside the one carrying users, with its own address and certificates, proved from a host file entry while real traffic goes elsewhere.

## Leaving from
- **AWS:** Application Load Balancer and ACM — the validation record must stay in the zone forever, because every renewal re-checks it.
- **Google Cloud:** external Application Load Balancer and Certificate Manager — URL map, target proxy and forwarding rule are separate objects, and the reserved address outlives all three.
- **Azure:** Application Gateway and Key Vault certificates — the gateway reads its certificate through a managed identity, and withdrawing that grant fails the gateway.

## Why this works
An edge cannot be half-tested once it is live, so this one is built beside the live one. Envoy Gateway takes an address from the range ordered in Move 08, terminates its own certificates, and routes to the services Move 14 and Move 16 already put on your hardware. No user arrives, because no DNS record points at it. That exposes the hard part cheaply: the listener rules and rewrites accumulated in the managed balancer over three years, which nobody has a full list of. As Gateway API objects they can be read and diffed.

## Before you start

**Access**
- The public address range from Move 08, with one address held back for the gateway
- Write access to the repository from Move 13, the one Argo CD reconciles
- An export of every listener rule, redirect, rewrite and health check from the managed balancer

**Software**
- `helm`, with a pinned chart version for each of the two installs below
- `cmctl` and `openssl`, to check issuance and to read what a listener actually serves

**People**
- Whoever owns the two most valuable transactions, to walk them end to end first

## The runbook
1. Install both controllers with `helm` at fixed versions — `helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.4.2`, and cert-manager at `v1.17.2`. Commit the values to the repository so Argo CD owns them.
2. Bind the gateway to one address from the Move 08 range as a virtual IP in layer-2 mode. Cut power to the node holding it and time the recovery: on one rack that is neighbour cache expiry, not anycast, and ten to thirty seconds is honest.
3. Issue certificates through cert-manager, confirm with `cmctl status certificate`, then read what the listener serves using `openssl s_client -connect`. Prove renewal in a scratch cluster by winding its clock past the threshold, not by waiting until day eighty-nine.
4. Read the balancer export line by line into a table: one row per listener rule, path condition, redirect, header rewrite, sticky-session setting and health check. The rule nobody remembers is the one a customer depends on.
5. Translate each row into an HTTPRoute in the repository and write one request that proves it. Priority ordering and specificity ordering disagree, so a rule shadowed for two years comes back to life once translated faithfully.
6. Point a laptop at the new address with a host file entry and walk sign-in, the two most valuable transactions, a large upload and any websocket. Cut nothing over; Move 18 moves the traffic.

## Operator's notes
- **Swap:** Under a dozen rules, skip the table and write the routes directly. It earns its keep around thirty.
- **Do it faster:** Stand the gateway up against one low-traffic service and keep that route as a permanent smoke test. It exercises address, certificate and route before the table exists.
- **Watch out:** A renewed certificate and a reloaded one are different events. Envoy takes a new secret in seconds; a legacy proxy behind it may not. cert-manager renews at day sixty of a ninety-day certificate, so the stale copy stays valid for another thirty and the symptom arrives on day ninety.
- **Leftovers:** The managed balancer charges per hour and per capacity unit until Move 18, and its validation records must stay in the zone or its certificates stop renewing.

## Rollback
Nothing here serves users, so backing out is removing the gateway objects and the address assignment, once no host file entry still points at them. There is no point of no return in this Move, by design. Keep the definitions in the repository so the edge can be restored in an afternoon.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $780/mo | $90/mo | 88% | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The managed balancer, its listener rules and its certificate service switch off in Move 18, where the $780 line stops.
