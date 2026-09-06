# 99 · Balancer rules and proxy annotations into HTTPRoute

**Layer:** Edge · **Leaving:** Managed balancer listener rules and ingress-controller annotations · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Translates every listener rule and controller annotation into HTTPRoute by hand, with a test case per rule, because only some have a standard equivalent.

## Leaving from
- **AWS:** Application Load Balancer listener rules — priority-ordered conditions with weighted target groups underneath them.
- **Google Cloud:** URL maps — a different structure for the same job, with its own ordering semantics.
- **Azure:** Application Gateway routing rules — the same again, expressed through path maps and backend settings.

## Why this works
Routing rules look mechanical and are not, because the ordering semantics differ between implementations and because a large share of real behaviour lives in annotations that have no standard equivalent at all. A conversion tool produces a useful first draft and a misleading final answer. So the deliverable here is not a set of resources; it is a table with one row per rule, its translation, a test case, and — for anything unmapped — a named owner and a decision. Nothing is cut over, which is why a Move that takes three weeks is Low risk.

## Before you start

**Access**
- Every listener rule and every annotation exported, from every balancer and every ingress resource
- The gateway from Move 98, ready to accept routes

**Software**
- A conversion tool used for the first draft only, with its output reviewed line by line
- A test harness that can assert a request lands on the right backend with the right transformations

**People**
- An owner named for every annotation that has no equivalent, because each is a decision rather than a translation

## The runbook
1. Export everything first: host and path conditions, priorities, header and query matching, redirects, rewrites, weights, session affinity and every annotation on every ingress resource.
2. Translate the mechanical parts. Host and path matching, header and query matching, redirects and rewrites, and weighted target groups into backend references with weights.
3. Handle ordering explicitly. Priority-ordered rules and specificity-ordered matching are not the same thing, and two rules that overlapped harmlessly under one model can shadow each other under the other.
4. Deal with affinity and slow start deliberately. These are common, they matter to real applications, and their support differs by implementation, so each one is either configured, replaced or dropped with the owner's agreement.
5. List the annotations with no equivalent and give each a named owner and a decision. This list is the honest output of the Move and it is what stops a surprise during Move 103.
6. Write a test case per rule. A request that should land on backend A, one that should be redirected, one that should be rewritten. Run them against the gateway from Move 98 with backends still in the cloud.
7. Budget about a day per twenty rules. A mid-sized estate is three weeks and it does not compress.

## Operator's notes
- **Swap:** Where a rule exists only to work around something the application should do itself, delete it and change the application. Migrations are the only time anyone is allowed to do this.
- **Do it faster:** Run the conversion tool first and then review, rather than writing from scratch. The draft is worth an hour of typing and no more trust than that.
- **Watch out:** A rule that has been shadowed by another for years is dead, and translating it faithfully makes it live again. Test what the current balancer actually does, not what its configuration says.
- **Leftovers:** The old listener rules stay until Move 103 shifts traffic, and they remain the rollback for the whole Part.

## Rollback
Nothing is serving through these routes, so the rollback is deleting them. There is no point of no return in this Move. The route table and the test cases are the durable output, and they should be in source control so that the mapping can be restored and re-checked when a rule behaves differently in Move 103 than it did in testing.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 weeks | — |

## What you can turn off
Nothing. Both edges are configured and only one is serving.
