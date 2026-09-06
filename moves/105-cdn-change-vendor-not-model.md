# 105 · CDN: change vendor, not model

**Layer:** Edge · **Leaving:** Provider-bundled CDN, edge functions and managed web application firewall · **Risk:** High · **Cutover:** 0 min · **Reversible:** 7 days

> Changes CDN vendor rather than insourcing one, because the points of presence stay rented either way and only the invoice changes.

## Leaving from
- **AWS:** CloudFront with Lambda@Edge and the managed firewall — edge compute that is a rewrite rather than a migration.
- **Google Cloud:** Cloud CDN with Cloud Armor — the same bundle, with the firewall rules expressed differently.
- **Azure:** Azure Front Door — where a previous CDN tier has already been retired and its customers moved once, which is the argument against treating any of this as permanent.

## Why this works
There is no version of this where you own the points of presence. A content network is a few hundred locations you rent, and repatriating it means building a few hundred locations, which nobody in this book's audience is doing. So this is a keep-renting verdict with a vendor change attached, and the vendor change is worth making because it decouples the edge from the cloud account you are closing. What makes it a High-risk Move is not the switch; it is the semantics that differ between vendors in ways that can serve one authenticated user's page to another.

## Before you start

**Access**
- The current cache configuration exported: cache keys, header handling, TTLs and behaviours per path
- Signed link and cookie configuration, which does not port between vendors

**Software**
- A new vendor with origin shielding configured, so a cache miss storm does not reach your origin directly
- The firewall running in detection-only mode, with the trusted-hop count set explicitly

**People**
- The owner of any edge compute, because it is a rewrite rather than a configuration move

## The runbook
1. Export the cache configuration and read it for the semantics rather than the values. Cache key composition and header variation are where a subtle difference serves the wrong user's content, and that is the worst failure available in this Part.
2. Configure origin shielding at the new vendor. Without it, a cache flush or a cold start sends every point of presence to your origin at once, and your origin is now a rack rather than a fleet.
3. Rebuild signed links and signed cookies. These do not port between vendors and the format differs, so this is a code change in whatever generates them.
4. Treat edge compute as a rewrite and price it as one. The runtimes differ, the limits differ, and a mechanical port produces something that runs and behaves differently under load.
5. Decide where the firewall sits, and run it in detection-only mode for a fortnight before enforcing anything. A firewall enforcing on day one blocks a legitimate customer within a week.
6. Set the trusted-hop count explicitly so the client address is taken from the right position in the forwarded header. Taking it from anywhere a client can set is how a rate limiter is defeated and how an audit log becomes fiction.
7. Cut over one hostname at a time with the old vendor still configured, and keep it for seven days.

## Operator's notes
- **Swap:** Where the content is small and mostly dynamic, no content network at all is a legitimate answer and removes a vendor. Measure the cache hit ratio before assuming one is needed.
- **Do it faster:** Move the static asset hostnames first. They are low risk, they are most of the volume, and they prove the configuration.
- **Watch out:** A cache key that omits a header the application varies on will serve the wrong response to somebody. Test with authenticated requests specifically, not only with anonymous ones.
- **Leftovers:** The bundled network bills per gigabyte and per request, and the firewall bills per rule and per million requests, both until the last hostname moves.

## Rollback
For seven days both vendors are configured and a hostname is moved back by changing one record. The point of no return is the deletion of the old distribution and its firewall rules, which is Part VII. Keep the exported cache configuration and firewall rules in source control so the previous behaviour can be restored and compared when a cache-related fault appears weeks later.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,180/mo | $1,900/mo | 40% | 0 min | 2 weeks | 7 days |

## What you can turn off
The bundled distribution and its firewall rules, seven days after the last hostname moved. The vendor bill does not go away; it changes name.
