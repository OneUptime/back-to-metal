# 46 · Cluster DNS, and the resolver the network used to be

**Layer:** Cluster · **Leaving:** The managed cluster DNS add-on and the provider's private resolver · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Sizes CoreDNS against the real racks and replaces the provider resolver for everything outside the cluster, with the replica count proved by a load test.

## Leaving from
- **AWS:** the CoreDNS add-on with the Route 53 Resolver — a resolver at the second address in every subnet, which was always just there.
- **Google Cloud:** Cloud DNS for GKE — where cluster name resolution was moved into the managed service, so this reader has no in-cluster deployment to carry across and is standing one up from nothing.
- **Azure:** the CoreDNS add-on with the Azure DNS Private Resolver — the same pattern, reached at a fixed platform address nobody configured.

## Why this works
Two separate things are being replaced and it helps to name them apart. Inside the cluster, name resolution is a deployment you now size, place and upgrade yourself, against the real failure domains labelled in Move 42 rather than against cloud zones. Outside it, every cloud provided a resolver at a fixed address that every machine used without anyone configuring it, and that resolver did split views, conditional forwarding and stub domains. Both have to exist here. The sizing is the part people get wrong, because the default replica count is a starting point that was never right for anybody, and a load test settles it in an hour.

## Before you start

**Access**
- The cluster from Move 44 with its network working, and the failure-domain labels from Move 42
- The current resolver configuration in the cloud: forwarders, private views and stub domains, exported

**Software**
- A name-resolution load generator, so the replica count is measured rather than copied from an article
- `kubectl` to place, scale and observe the deployment

**People**
- Whoever owns the internal name zones, because split views are their design and not yours

## The runbook
1. Deploy the cluster resolver with anti-affinity across the racks and switches labelled in Move 42. Two replicas on one machine is one replica with extra billing.
2. Turn on the node-local cache. It removes most of the load, removes the connection-tracking race that produces intermittent lookup failures on parallel queries, and it is the single highest-value change in this Move.
3. Deal with the search-path amplification. The default search list turns one external lookup into several, and services that resolve external names in a hot path pay for it repeatedly. Set fully qualified names where it matters and measure the difference.
4. Load test the deployment and set the replica count from the result. Include a failure case: kill a replica during the test and confirm the remaining ones absorb it without the error rate moving.
5. Build the site resolver that replaces the provider's fixed address. Forward internal zones to it, define the split views and stub domains you exported, and give it two instances that do not share a machine.
6. Point everything outside the cluster at the new resolver and confirm resolution from a machine, from a pod, and from the office link. Three vantage points, because they take three different paths.

## Operator's notes
- **Swap:** Where an existing internal name service already exists and is well run, keep it and forward to it. Building a second authority for the same zones is how two answers to one question appear.
- **Do it faster:** Copy the exported forwarders and views wholesale and prune afterwards. Reconstructing them from what people remember takes a fortnight and misses two.
- **Watch out:** Forcing upstream lookups over a connection-oriented transport avoids one class of truncation and failure, and costs latency. Decide deliberately rather than inheriting whichever default you land on.
- **Leftovers:** The provider's resolver endpoints and private zones bill per endpoint and per query, and they stay until Part VI has moved the traffic.

## Rollback
Name resolution is reverted by scaling the old path back up and repointing, and with no production traffic on the cluster this is a minutes-long change. The point of no return does not exist in this Move; the danger is entirely that it is done badly and then relied upon. Keep the exported forwarder and view configuration in source control so the provider's resolver behaviour can be restored and compared when something resolves differently in two places.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $190/mo | $0/mo | 100% | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The provider's resolver endpoints stay until the workloads that use them have moved.
