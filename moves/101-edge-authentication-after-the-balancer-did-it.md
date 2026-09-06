# 101 · Edge authentication after the balancer did it

**Layer:** Edge · **Leaving:** Load-balancer authentication, managed user directories and client VPN · **Risk:** High · **Cutover:** 5 min · **Reversible:** 7 days

> Rebuilds the authentication the balancer was performing, before internal tools that never had a login of their own become publicly reachable.

## Leaving from
- **AWS:** Application Load Balancer authentication — with Cognito behind it and Client VPN beside it, the balancer signed an identity header the application trusted.
- **Google Cloud:** Identity-Aware Proxy — the same pattern, with its own header name and its own signature scheme.
- **Azure:** App Service authentication with Entra ID — again the same, with a third header name, and a point-to-site VPN beside it.

## Why this works
A number of internal tools have no login of their own, because the balancer in front of them did the authenticating and passed a signed header the application trusted. Move those tools without rebuilding that, and they become publicly reachable with no authentication at all — which is the most dangerous single failure available in this Part. So this Move rebuilds it: an authentication proxy behind the gateway's external authorisation filter, against the identity provider from Move 50, with the cookie domain and the session store chosen deliberately rather than defaulted, and the downstream code updated for a header with a different name.

## Before you start

**Access**
- The identity provider from Move 50, with an application registration for the proxy
- A list of every service currently relying on a balancer-injected identity header

**Software**
- An authentication proxy wired to the gateway's external authorisation filter, at a pinned version
- A session store and a cookie domain chosen deliberately, because the defaults are wrong for a multi-service estate

**People**
- The owner of every internal tool, because their users will all be signed out at once

## The runbook
1. List every service that trusts an injected identity header. The dangerous ones are the tools nobody thinks of as applications: a dashboard, an admin panel, a metrics interface.
2. Deploy the authentication proxy and wire it to the gateway's external authorisation filter, against the identity provider from Move 50.
3. Choose the cookie domain deliberately. A cookie scoped too broadly is a session shared between services that should not share one; scoped too narrowly and users sign in repeatedly. Neither default is right.
4. Choose the session store deliberately too. An in-memory store means every proxy restart signs everybody out, which is fine for a tool and unacceptable for anything customer-facing.
5. Update the downstream code for the new header name and signature. Each provider injected a differently named header and applications parsed it directly; that parsing has to change in every one.
6. Retire the client VPN once the internal tools are behind this, which removes a per-hour endpoint charge and a client nobody enjoyed.
7. Cut over in a single change and accept that live sessions are invalidated. Five minutes of everybody signing in again, nothing down, and it is visible enough to warn people about in advance.

## Operator's notes
- **Swap:** Where an application already has its own login, do not put a proxy in front of it. Two authentication layers is a support burden and a source of confusing failures.
- **Do it faster:** Move the least-used internal tool first and use it as the pattern. It will find the cookie domain problem for you at no cost.
- **Watch out:** An application that trusts a header will trust that header from anyone if the proxy is bypassed. Network policy from Move 60 must ensure the only path to the application is through the gateway.
- **Leftovers:** The managed user directory bills per monthly active user, and the client VPN bills per endpoint-hour plus per connection-hour, both until deleted.

## Rollback
For seven days the balancer-based authentication still exists and a service is moved back by repointing its route. The point of no return is the deletion of the managed user directory, because the accounts in it cannot be restored afterwards and any user identity that lived only there is gone. Export the directory before deleting it, and confirm the export can be read, not merely that it completed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $720/mo | $30/mo | 96% | 5 min | 2 weeks | 7 days |

## What you can turn off
The client VPN endpoints today, and the managed user directory after seven days and a verified export.
