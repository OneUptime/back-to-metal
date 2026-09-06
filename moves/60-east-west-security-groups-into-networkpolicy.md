# 60 · East-west: security groups into NetworkPolicy

**Layer:** Platform · **Leaving:** Instance-level firewalls: security groups and their group-to-group references, VPC firewall rules and network ACLs · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> The pod network is flat until you say otherwise, so the existing firewall rules become the policy set, rolled out per namespace in audit mode before default-deny.

## Leaving from
- **AWS:** security groups with group-to-group references — a construct with no equivalent here, so every rule is re-expressed as a label selector rather than translated.
- **Google Cloud:** VPC firewall rules with network tags — closer, because tags behave more like labels, and the dataplane was already Cilium-derived.
- **Azure:** network security groups with application security groups — the same shape as the first, with the same re-expression required.

## Why this works
Move 44 left the pod network deliberately flat, which means that today anything can talk to anything. That is fine while nothing real is running and unacceptable the moment Part V arrives, so this is the Move that closes it. The policy set is derived from the firewall rules you already have rather than invented from a diagram, because the existing rules encode a decade of decisions nobody remembers making. The rollout is per namespace and in audit mode first, with flow logs answering what actually talks to what, and only then default-deny. North-south policy is Part VI.

## Before you start

**Access**
- The exported firewall rules from every cloud account, including the ones attached to things nobody claims
- The cluster with its network observability enabled, so flows can be read rather than guessed

**Software**
- Flow logging turned on, with somewhere to query it that is not the terminal you are standing in
- The policy resources chosen deliberately: the portable upstream shape, or the richer vendor one with its portability cost stated

**People**
- One owner per namespace, because a default-deny rollout needs somebody who can say what that namespace legitimately talks to

## The runbook
1. Export the existing firewall rules and turn them into an inventory rather than a policy. Most of the three weeks this Move takes is here, and none of it is writing configuration.
2. Re-express group-to-group references as label selectors. Two of the three clouds have no equivalent construct, so this is a rewrite, and a mechanical translation produces rules that are both too broad and subtly wrong.
3. Turn on flow logging and watch a full week, including a deploy, a batch window and a weekend. What actually talks to what is never quite what the diagram says.
4. Roll out per namespace in audit mode. Read the would-be denials and fix the policy rather than the workload, until a week passes with nothing surprising in the log.
5. Handle name resolution and outbound traffic explicitly and first, because they are what break and they break quietly. A default-deny policy that forgets name resolution produces an application that fails in ways nobody attributes to the network.
6. Switch to default-deny one namespace at a time, least critical first, with the previous policy one command away.
7. Decide the resource shape deliberately. The upstream policy resource is portable and limited; the vendor's own is more expressive and ties you to this network plug-in. Write down which you chose and what it costs.

## Operator's notes
- **Swap:** Where a namespace is genuinely too tangled to police, leave it flat and say so in writing, with a date. An honest exception beats a policy full of allow-everything rules.
- **Do it faster:** Start with the namespaces that have one or two dependencies. They take an hour each and they build the pattern the difficult ones will follow.
- **Watch out:** Policies are additive and there is no explicit deny, so a permissive rule somewhere else in the namespace silently defeats a restrictive one. Review the whole namespace rather than the rule you just wrote.
- **Leftovers:** The cloud security groups keep protecting the old estate and stay until Part VII. Do not tidy them while anything still runs there.

## Rollback
Policies are deleted and the network returns to flat within seconds, which makes this one of the safest High-risk Moves in the book. There is no point of no return. The danger is entirely in the direction of doing it late, after Part V has put data behind an unpoliced network. Keep every policy in source control so a working set can be restored instantly, and keep the audit-mode logs so a denial can be explained rather than argued about.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 weeks | — |

## What you can turn off
Nothing yet. The cloud firewall rules protect the old estate for as long as it carries production.
