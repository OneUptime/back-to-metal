# 17 · The front door

**Layer:** Run · **Leaving:** Managed layer-7 balancers and certificate services · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The new edge goes up beside the one carrying users, with its own address and certificates, proved from a host file entry while real traffic goes elsewhere.

## Leaving from
- **AWS:** Application Load Balancer and ACM — DNS validation records must remain while the certificates need automatic renewal, including the old edge's return window.
- **Google Cloud:** external Application Load Balancer and Certificate Manager — URL map, target proxy and forwarding rule are separate objects, and the reserved address outlives all three.
- **Azure:** Application Gateway and Key Vault certificates — the gateway retrieves certificates through a managed identity; losing access can disable the affected HTTPS listeners.

## Why this works
Build the edge beside the live one. Envoy Gateway routes to Kubernetes services; a pair of proxy guests routes to application VMs. Either uses an address from Move 08 and services tested on your hardware. Keep production DNS unchanged and restrict test access. Export the managed balancer's listener rules and rewrites into versioned proxy configuration or Gateway API objects, then prove their behaviour before shifting traffic. The figures retain the reference Kubernetes edge; price a VM proxy pair separately.

## Before you start

**Access**
- The public address range from Move 08, with one address held back for the gateway
- Write access to the VM configuration repository or the Argo CD repository from Move 13
- DNS challenge credentials restricted to certificate validation records
- An export of every listener rule, redirect, rewrite and health check from the managed balancer

**Software**
- For VMs: a supported reverse proxy and ACME client, plus Keepalived, with exact package versions and configuration pinned in the guest template
- For Kubernetes: `helm`, Envoy Gateway 1.8.4, and `cmctl` for the platform's cert-manager 1.21.1
- `openssl`, to inspect the certificate each listener actually serves

**People**
- Whoever owns the two most valuable transactions, to walk them end to end first

## The runbook
1. For VMs, deploy the pinned proxy template to guests on different physical hosts. For Kubernetes, install Envoy Gateway with `helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.8.4 -n envoy-gateway-system --create-namespace`. Configure at least two data-plane replicas on different hosts, verify the platform's cert-manager and commit the settings for Argo CD.
2. Assign one virtual IP from Move 08. For VM proxies, configure Keepalived to track proxy health and transfer it between guests on the same layer-2 network; permit its peer traffic and address announcements through the host bridges. For Kubernetes, use the cluster network's layer-2 announcement. Power off the physical host serving the address and measure recovery, then test a failed proxy process separately.
3. Use DNS validation before traffic moves. On VMs, schedule the ACME client and deploy renewed certificates to both proxies with a reload hook. On Kubernetes, issue through cert-manager and check `cmctl status certificate`. Rehearse renewal in staging, then inspect production with `openssl s_client`, supplying the destination address, SNI hostname and hostname-verification options. Repeat after failover.
4. Read the balancer export line by line into a table: one row per listener rule, path condition, redirect, header rewrite, sticky-session setting and health check. The rule nobody remembers is the one a customer depends on.
5. Translate each row into proxy configuration or Kubernetes HTTPRoute and any required policy objects, and write requests proving its observed behaviour. Enable backend health checks. Rule precedence differs between implementations: test overlapping matches so a previously shadowed rule cannot start serving unexpectedly.
6. Point a laptop at the new address with a host file entry and walk sign-in, the two most valuable transactions, a large upload and any websocket. Cut nothing over; Move 18 moves the traffic.

## Operator's notes
- **Swap:** For a small rule set, keep the mapping beside the route tests instead of in a separate table.
- **Do it faster:** Keep one low-traffic route as a permanent smoke test for the address, certificate and proxy.
- **Watch out:** Renewal does not guarantee reload. Alert on the certificate each proxy serves, and verify the standby's certificate before failover.
- **Leftovers:** Managed balancer and address charges continue until decommissioning. Keep certificate-validation records and permissions while the old edge remains a return path.

## Rollback
Nothing here serves users, so backing out is removing the test gateway or proxy guests and their address assignment, once no host file entry still points at them. There is no point of no return in this Move, by design. Keep the definitions in the repository so the edge can be restored and retested.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,400/mo | $320/mo | 87% | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The managed balancer, its listener rules and its certificate service can switch off after Move 18's retention window and a verified replacement.
