# 44 · Cilium, with kube-proxy off

**Layer:** Cluster · **Leaving:** The cloud-provider CNI plug-in and kube-proxy · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Installs Cilium with kube-proxy replaced, which ends the address accounting behind pod density and turns service resolution into a hash-map lookup.

## Leaving from
- **AWS:** the Amazon VPC CNI — pods took real network addresses from the subnet, so pod density was an address-accounting problem rather than a capacity one.
- **Google Cloud:** GKE Dataplane V2 — already Cilium, so this reader is taking over a control loop rather than changing a datapath.
- **Azure:** Azure CNI Powered by Cilium — also already Cilium, with the same consequence and the same short journey.

## Why this works
Two things change here and they are worth separating. The first is the address model: on one of the three clouds, pods took addresses from the network itself, which is why pod density per machine was governed by how many addresses an instance could hold. On your own fabric, pods get their own range from Move 39 and that accounting disappears. The second is service resolution. Replacing kube-proxy turns a linear walk through a rule chain into a hash-map lookup in the kernel, which stops mattering somewhere in the low thousands of services and then matters a great deal. The pod network is left deliberately flat here, because policy is Move 60.

## Before you start

**Access**
- The cluster from Move 43, healthy, with the API address reachable from every machine
- The pod and service ranges from Move 39, agreed and not overlapping anything

**Software**
- `helm`, and the Cilium chart pinned to an exact chart version rather than to a range
- `cilium` for the connectivity test, and `kubectl` for the verification steps

**People**
- Whoever will own the network datapath, because this is the component that carries every packet

## The runbook
1. Install Cilium with `helm install` at a pinned chart version, with kube-proxy replacement enabled and the API host and port pinned at the virtual address raised in Move 43. Without those two values the agent cannot reach the API once kube-proxy is gone, which is a memorable way to break a cluster.
2. Confirm no kube-proxy rules survive. Check that the rule chains it created are absent rather than merely unused, because a half-removed kube-proxy produces packet behaviour that is extremely hard to reason about.
3. Run the `cilium` connectivity test and read the whole output. It exercises paths you would not think to test and it is the cheapest verification in this Part.
4. Check the connection-tracking table sizing set in Move 41 against real load, and watch for table exhaustion under a load test rather than in production.
5. Leave the pod network flat and unpoliced for now. Introducing policy at the same time as the datapath means that when something is unreachable, there are two candidate causes instead of one. Move 60 does policy.
6. Record the fallback explicitly: for the non-Talos exception from Move 41 on an older kernel, the standard rule-based dataplane of another network plug-in remains available, and it is the answer where the kernel is too old rather than too new.

## Operator's notes
- **Swap:** Where an older kernel rules out kube-proxy replacement, run Cilium with kube-proxy in place first and remove it after the kernel is updated. The two changes do not have to happen together.
- **Do it faster:** Do this on the second cluster from Move 51 first if it exists yet, or on a three-node scratch cluster if it does not. The whole cycle is twenty minutes.
- **Watch out:** Pinning the API host to a name rather than an address reintroduces a name-resolution dependency in the path that brings up name resolution. Pin the address.
- **Leftovers:** The cloud network plug-in and its address reservations stay in the old cluster until Part VII. Nothing here touches them.

## Rollback
Cilium is uninstalled and kube-proxy restored by reverting the machine configuration and reapplying it, which takes minutes on a cluster with no workloads on it. That is the argument for doing it now. The point of no return is Move 47, where the first volume binds and machines stop being disposable. Keep the chart version and every value in source control so a known good datapath configuration can be restored exactly rather than reconstructed from memory.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The old cluster's network plug-in stays until Part VII closes the account.
