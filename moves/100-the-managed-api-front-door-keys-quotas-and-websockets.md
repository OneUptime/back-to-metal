# 100 · The managed API front door: keys, quotas and WebSockets

**Layer:** Edge · **Leaving:** Managed API gateways · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Rebuilds the managed API front door as keys, quotas, validation and throttling on the gateway, and gives long-lived sockets an answer of their own.

## Leaving from
- **AWS:** API Gateway — a connect-and-disconnect route model for sockets with a server-initiated callback API that has no standard equivalent and has to be rebuilt as a service you run.
- **Google Cloud:** API Gateway and Apigee — no socket support in the lighter product at all, which pushes that traffic to the full platform.
- **Azure:** API Management — which proxies sockets through, making this the easiest of the three for that half.

## Why this works
A managed API front door was doing more than proxying, and the extra is what this Move rebuilds: usage plans with per-consumer quotas, keys and their rotation, request and schema validation, throttling, and the authoriser functions that fronted code migrated in Move 89. On the gateway from Move 98, key authentication and global rate limiting are policy resources, and the rate limiting needs a small service and a small cache of its own on the storage from Move 49. The genuinely divergent part is long-lived sockets, where the three providers do three different things and one of them has no equivalent at all.

## Before you start

**Access**
- The usage plans, keys and quotas exported, and a list of every consumer holding a key
- The gateway and routes from Moves 98 and 99, already carrying test traffic

**Software**
- Key authentication and rate-limiting policies on the gateway, with the rate-limit service and its cache deployed
- Request and schema validation moved to the gateway or explicitly to the application

**People**
- Whoever can contact every external consumer, because keys you cannot reissue set this Move's timeline

## The runbook
1. Inventory the consumers and their keys first. Keys you can reissue on your own schedule are a week's work; keys held by external customers are a quarter, and that is what sets the timeline.
2. Rebuild usage plans as rate-limiting policy with per-consumer quotas. Deploy the rate-limit service and its small cache on the storage from Move 49 rather than treating them as an afterthought.
3. Rebuild key authentication as a security policy on the route, and design the rotation before issuing the first key. A key with no rotation path is a key you will be living with in five years.
4. Move request and schema validation deliberately. Either it happens at the gateway or it happens in the application, and the failure mode of assuming the other one is doing it is an unvalidated payload reaching your code.
5. Handle sockets according to which provider you are leaving. Where the managed gateway proxied them, the gateway here does too. Where the model was connect-and-disconnect routes with a server-initiated callback, that callback has no standard equivalent and is rebuilt as a service you run, which is a real piece of engineering rather than a configuration change.
6. Run both front doors for thirty days with consumers migrating on their own schedule.
7. Alert on quota rejections from day one, because a misconfigured quota looks to a customer like an outage and to you like nothing at all.

## Operator's notes
- **Swap:** Where the front door was doing nothing but proxying, delete it and route directly. A surprising number of managed gateways are an expensive layer with no policy in them.
- **Do it faster:** Start the consumer contact on the first day of the Part. The engineering is three weeks and the customers are a quarter.
- **Watch out:** Quota accounting resets differently between implementations — per calendar period against per rolling window — and a consumer at the edge of their plan will notice.
- **Leftovers:** The managed gateway bills per million requests plus its own caching tier, and the caching tier is billed per hour whether or not it is hit.

## Rollback
For thirty days both front doors work and a consumer is moved back by reissuing them the old key and endpoint. The point of no return is the deletion of the managed gateway with its keys, since the keys themselves cannot be restored afterwards and every consumer would have to be reissued at once. Keep the exported usage plans and the key inventory in source control so the configuration can be restored onto a rebuilt gateway if the migration is aborted.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,480/mo | $80/mo | 95% | 0 min | 3 weeks | 30 days |

## What you can turn off
The managed gateway and its caching tier, thirty days after the last consumer moved and their old key stopped being used.
