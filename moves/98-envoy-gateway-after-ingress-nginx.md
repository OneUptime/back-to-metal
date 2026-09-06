# 98 · Envoy Gateway, after ingress-nginx

**Layer:** Edge · **Leaving:** Managed layer-7 load balancers and in-cluster ingress controllers · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Installs a Gateway API controller on an address of its own, so the layer-7 edge exists and is testable before a single route moves.

## Leaving from
- **AWS:** Application Load Balancer with the load balancer controller — an appliance managed for you and configured from the cluster.
- **Google Cloud:** the external application load balancer — the same shape driven by an ingress controller, and implemented in the network rather than as an appliance.
- **Azure:** Application Gateway with its ingress controller — the same again, with its own annotation vocabulary.

## Why this works
This Move builds the edge and moves nothing through it. A gateway controller, a gateway class, a gateway and its listeners, with certificates from Move 97 and an address from Move 95 or Move 96, fronting backends that are still running in the provider account across the link from Move 53. That last detail is what makes it low risk: the new edge can be exercised against real backends before any user is involved. Readers arriving from the in-cluster controller rather than a managed balancer have a deadline as well, because that project has been retired and no longer receives security fixes.

## Before you start

**Access**
- An address from Move 95 or Move 96, and certificates issued by Move 97
- The link from Move 53, so backends still in the cloud are reachable from the new gateway

**Software**
- The gateway controller at a pinned chart version, installed with `helm`
- A gateway class, a gateway and listeners defined as resources rather than configured by hand

**People**
- Whoever owns the routes that will move in Move 99, so the structure suits them

## The runbook
1. Install the controller with `helm install` at a pinned chart version. The book names one implementation rather than surveying three, because a small team should run one edge and know it well.
2. Define the gateway class, the gateway and its listeners. Terminate the certificates from Move 97 on the listener and confirm the chain is served correctly from outside.
3. Bind the gateway to the address from Move 95 or Move 96. This is where the two halves of the Part meet, and it is worth confirming the address is reachable before adding any route.
4. Point one throwaway route at a backend still running in the provider account, across the link from Move 53. It proves the whole path — address, certificate, gateway, link, backend — without touching production.
5. Establish the delegation model: who may create a route, in which namespace, against which listener. Getting this right now avoids re-organising every route later.
6. Note the deadline if you are leaving the in-cluster controller rather than a managed balancer. That project is retired and no longer receives security fixes, which makes this urgent rather than merely worthwhile.
7. Cut nothing over. Route translation is Move 99 and traffic is Move 103.

## Operator's notes
- **Swap:** Where an estate is already on a well-run alternative gateway implementation, keep it. The value here is the resource model, not the specific proxy.
- **Do it faster:** Stand it up on the second cluster from Move 51 first. It takes an hour and it removes every surprise from the production install.
- **Watch out:** Listener and certificate mismatches produce a gateway that reports ready and serves the wrong certificate. Check what is served from outside rather than what the resource says.
- **Leftovers:** The managed balancer keeps billing per hour and per capacity unit until Move 103, and the retired in-cluster controller keeps running until its routes move.

## Rollback
Nothing is serving production, so this Move is undone by deleting the gateway resources. There is no point of no return. That is precisely the design: the edge exists, is tested and is boring long before Move 103 asks it to carry users. Keep the gateway and listener definitions in source control so a working edge can be restored quickly, and keep the throwaway route as a permanent smoke test.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing. Both edges are running and both are paid for until Move 103.
