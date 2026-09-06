# 79 · Redis: which half of it is actually a cache

**Layer:** Data · **Leaving:** Managed Redis, Valkey and Memcached · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Classifies the key space before moving anything, sends the genuinely ephemeral half to Valkey and hands the durable half to the next Move.

## Leaving from
- **AWS:** ElastiCache for Redis, Valkey and Memcached — three engines, one service, and a default eviction policy that is not the stock one.
- **Google Cloud:** Memorystore — the same idea with its own defaults, and its own cluster mode behaviour.
- **Azure:** Azure Cache for Redis — the same again, with tiers that change which features exist.

## Why this works
Most Redis is not a cache. It holds sessions, rate-limit counters, distributed locks and a job queue, and every one of those is durable state wearing a cache's clothing. Moving all of it as though it were ephemeral is how a migration loses everybody's shopping basket. So this Move classifies the key space first, by pattern and by time-to-live distribution, and only the half that is genuinely disposable moves here. The other half — sessions, locks, queues — is handed to Move 81, which treats it as the durable state it is.

## Before you start

**Access**
- Read access to the managed instance for a full key-space scan, run in a way that does not block it
- The eviction policy currently configured, which is not the stock default on any of the three

**Software**
- A scanning script that classifies by key pattern and records the time-to-live distribution per pattern
- `valkey-cli` for the destination checks, at a version matching what you will run

**People**
- The owner of each key pattern, because only they can say whether losing those keys is acceptable

## The runbook
1. Scan the key space incrementally rather than listing it, and classify by pattern. Every estate has between five and twenty real patterns and a long tail of one-offs.
2. Record the time-to-live distribution per pattern. Keys with no expiry are almost never a cache, and that single check finds the durable half faster than any conversation.
3. Get an owner to confirm, per pattern, whether losing those keys during a cutover is acceptable. Where the answer is no, the pattern goes to Move 81.
4. Note the two behaviour changes that are silent at the boundary. Cluster mode routes by key hash, so commands touching multiple keys that worked against a single node will be refused; and the managed eviction default differs from the stock one, so a cache that never evicted may start evicting, or the reverse.
5. Stand up the destination on the openly licensed fork, and say why: the original project is now under a set of licences of which only one is approved as open source, and the fork is under a permissive licence with multi-vendor governance.
6. Move the ephemeral half by pointing the application at the new endpoint and letting the cache fill. There is nothing to copy, which is what makes this Move three days rather than three weeks.
7. Land the memcached estate on stock memcached at the same time; it belongs with the caching layer and it converts trivially.

## Operator's notes
- **Swap:** Where a cache is small and its miss cost is low, moving it with no warm-up is fine. Where a cold cache means a stampede on the database, warm it before switching or switch during a quiet hour.
- **Do it faster:** Do the classification once and keep it. It is the input to Move 81 and it is the document that stops the same argument being had twice.
- **Watch out:** A client library configured for cluster mode against a single node, or the reverse, fails in ways that look like a network problem. Confirm the topology the client expects matches what you built.
- **Leftovers:** The managed cache keeps billing per node-hour until the last client moves, and reserved nodes keep billing past that.

## Rollback
Pointing the application back at the managed endpoint returns everything to where it was, and because only disposable keys moved, nothing needs to be restored. There is no point of no return in this Move. Keep the classification in source control, and keep the managed instance running until Move 81 has dealt with the durable half, because the two halves frequently share a client configuration.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,180/mo | $60/mo | 95% | 0 min | 1 week | — |

## What you can turn off
The cache nodes serving the ephemeral half, once the new endpoint has been serving for a week — but not the instance itself until Move 81 is done.
