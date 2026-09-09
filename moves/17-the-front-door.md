# 17 · The front door

**Layer:** Run · **Leaving:** Managed layer-7 balancers and certificate services · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The new edge goes up beside the one carrying users, with its own address and certificates, proved from a host file entry while real traffic goes elsewhere.

## Leaving from
- **AWS:** Application Load Balancer and ACM — the validation record must stay in the zone forever, because every renewal re-checks it.
- **Google Cloud:** external Application Load Balancer and Certificate Manager — URL map, target proxy and forwarding rule are separate objects, and the reserved address outlives all three.
- **Azure:** Application Gateway and Key Vault certificates — the gateway reads its certificate through a managed identity, and withdrawing that grant fails the gateway.

## Why this works
An edge cannot be half-tested once it is live, so this one is built beside the live one. For Kubernetes, Envoy Gateway terminates TLS and routes to services. For a VM estate, a pair of proxy guests routes directly to application guests; Kubernetes is unnecessary. Either edge takes an address from Move 08 and reaches the services already tested on your hardware. No user arrives, because no DNS record points at it. That exposes the hard part cheaply: the listener rules and rewrites accumulated in the managed balancer over three years, which nobody has a full list of. Store those rules in versioned proxy configuration or Gateway API objects. The figures below retain the reference Kubernetes edge; price the VM pair separately.

## Before you start

**Access**
- The public address range from Move 08, with one address held back for the gateway
- Write access to the VM configuration repository or the Argo CD repository from Move 13
- DNS challenge credentials restricted to certificate validation records
- An export of every listener rule, redirect, rewrite and health check from the managed balancer

**Software**
- For VMs: a supported reverse proxy and ACME client, plus Keepalived, with exact package versions and configuration pinned in the guest template
- For Kubernetes: `helm` and `cmctl`, with the controller chart versions pinned below
- `openssl`, to inspect the certificate each listener actually serves

**People**
- Whoever owns the two most valuable transactions, to walk them end to end first

## The runbook
1. For VMs, deploy the pinned proxy template to a pair of guests, with placement rules keeping them on different physical hosts. Reuse your team's supported proxy where available. For Kubernetes, install Envoy Gateway with `helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.4.2` and cert-manager at `v1.17.2`; commit values for Argo CD.
2. Assign one virtual IP from Move 08. For VM proxies, configure Keepalived to track proxy health and transfer it between guests on the same layer-2 network; permit its peer traffic and address announcements through the host bridges. For Kubernetes, use the cluster network's layer-2 announcement. Power off the physical host serving the address and measure recovery, then test a failed proxy process separately.
3. Use DNS validation so issuance works before traffic moves. On VMs, schedule the pinned ACME client and securely deploy renewed certificates to both proxies with a reload hook. On Kubernetes, issue through cert-manager and check `cmctl status certificate`. Rehearse renewal against the ACME staging service, then check production certificates with `openssl s_client -connect`, including each proxy after failover.
4. Read the balancer export line by line into a table: one row per listener rule, path condition, redirect, header rewrite, sticky-session setting and health check. The rule nobody remembers is the one a customer depends on.
5. Translate each row into the VM proxy configuration or a Kubernetes HTTPRoute, and write one request that proves it. Point VM backends at the application guests and enable health checks. Priority ordering and specificity ordering disagree, so a rule shadowed for two years comes back to life once translated faithfully.
6. Point a laptop at the new address with a host file entry and walk sign-in, the two most valuable transactions, a large upload and any websocket. Cut nothing over; Move 18 moves the traffic.

## Operator's notes
- **Swap:** Under a dozen rules, skip the table and write the routes directly. It earns its keep around thirty.
- **Do it faster:** Stand the gateway up against one low-traffic service and keep that route as a permanent smoke test. It exercises address, certificate and route before the table exists.
- **Watch out:** A renewed certificate and a reloaded one are different events. Alert on the expiry of the certificate actually served by each proxy, and verify that the standby has the new certificate before it takes the virtual IP.
- **Leftovers:** The managed balancer charges per hour and per capacity unit until Move 18, and its validation records must stay in the zone or its certificates stop renewing.

## Rollback
Nothing here serves users, so backing out is removing the test gateway or proxy guests and their address assignment, once no host file entry still points at them. There is no point of no return in this Move, by design. Keep the definitions in the repository so the edge can be restored in an afternoon.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,400/mo | $320/mo | 87% | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The managed balancer, its listener rules and its certificate service can switch off after Move 18's retention window and a verified replacement.
