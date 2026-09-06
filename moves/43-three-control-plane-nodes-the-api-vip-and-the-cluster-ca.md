# 43 · Three control-plane nodes, the API VIP and the cluster CA

**Layer:** Cluster · **Leaving:** The managed Kubernetes control plane and its cluster-creation tooling · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Places three etcd members across separate power feeds and switches, raises the API VIP, and takes ownership of the cluster CA the provider used to rotate.

## Leaving from
- **AWS:** the EKS managed control plane — a per-hour charge, an endpoint, and a certificate authority somebody else rotated on your behalf.
- **Google Cloud:** the GKE managed control plane — the same, with control-plane upgrades applied on a release channel you chose.
- **Azure:** the AKS managed control plane — the same again, with the availability guarantee sold as a paid tier, so a reader on the free tier has no commitment to lose.

## Why this works
The control plane is three machines and a consensus store, and the consensus store is the part that decides whether you have a cluster. etcd is an fsync benchmark wearing a database's clothing: its write path is a durability promise on every commit, so it goes on the power-loss-protected devices specified in Move 09 and it never goes on replicated network storage. The three members are placed across the power feeds, switches and racks labelled in Move 42, so that losing one of anything loses one member and not two. The API address is raised by the operating system's own virtual-address support rather than by adding another component to the critical path.

## Before you start

**Access**
- Three machines provisioned by Move 42, on separate feeds, switches and racks
- The power-loss-protected devices from Move 09, confirmed present in each of them

**Software**
- `talosctl` and `kubectl`, both pinned to the cluster version you are building
- `etcdctl` for the health checks, and a way to measure fsync latency on each control-plane device

**People**
- Whoever will hold the certificate authority material, because that custody starts today

## The runbook
1. Confirm the placement before installing anything. Three control-plane machines on three feeds, three switches and, where you have them, three racks. Three members in one cabinet is one failure domain wearing a quorum's clothing.
2. Measure fsync latency on each control-plane device and record it. This is the number that predicts leadership stability under load, and a device that fails here fails the cluster later rather than now.
3. Bring up the three members and raise the API address using the operating system's own virtual-address support. Adding a separate load balancer in front of the API introduces a component that has to be up for the cluster to be reachable.
4. Take ownership of the certificate authority hierarchy. Record where the key material lives, who can use it, how kubelet certificates rotate, and when every certificate in the cluster expires. The at-rest encryption key is a separate concern and belongs to Move 48.
5. Build the annual expiry inventory now, while the numbers are in front of you. A certificate that expires unnoticed is the classic way a healthy cluster stops working on a Sunday.
6. Kill a control-plane member deliberately and watch the cluster stay up, then bring it back and confirm it rejoins. Do it again with the machine that currently holds leadership. This drill costs an hour and it is the difference between believing you have three members and knowing it.

## Operator's notes
- **Swap:** Five members are worth it for an estate expected to pass a few hundred nodes, and are unnecessary below that. Five members write to five devices on every commit, which is not free.
- **Do it faster:** Build the cluster twice from the same configuration before you trust it. The second build takes twenty minutes and proves the first was not luck.
- **Watch out:** Placing the consensus store on replicated network storage looks reasonable and destroys performance and availability together. It goes on local, protected devices, always.
- **Leftovers:** The managed cluster keeps running and keeps charging until Part VII. It is the way back for the whole of Parts IV, V and VI.

## Rollback
Until workloads arrive, this cluster can be deleted and rebuilt in an afternoon, which is the argument for building it long before anything needs it. The point of no return is Move 47, where the first volume binds. Keep the certificate authority material somewhere sealed and backed up, and rehearse the consensus restore in Move 52 before trusting any of it; a control plane that cannot be restored from its own backup is three machines and a hope.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $73/mo | $0/mo | 100% | 0 min | 2 weeks | — |

## What you can turn off
Nothing yet, although the per-hour control-plane charge on the old cluster is the first line of the cloud bill that will go to zero in Part VII.
