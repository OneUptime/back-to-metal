# 52 · The etcd restore drill

**Layer:** Cluster · **Leaving:** Managed control-plane backup and restore · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Destroys a quorum on purpose on the second cluster and restores it from a snapshot, so the recovery time is a measured number rather than an assumption.

## Leaving from
- **AWS:** EKS control-plane recovery — the consensus store was never exposed, and recovery meant recreating a cluster.
- **Google Cloud:** GKE control-plane recovery with Backup for GKE — the only one of the three selling a backup product for cluster workloads, and it does not restore the consensus store either.
- **Azure:** AKS control-plane recovery — the same as the first, with the same answer: recreate the cluster.

## Why this works
None of the three managed offerings ever let you touch the consensus store, so there is nothing to migrate here. What there is instead is a number you do not have: how long it takes you to get a cluster back after losing quorum. That number is only obtainable by doing it, and the second cluster from Move 51 exists precisely so that it can be done without a conversation. The finding is the wall-clock time, published, along with the discovery of which pieces you did not have to hand — usually the certificate authority material, and usually at the worst moment.

## Before you start

**Access**
- The second cluster from Move 51, with nothing on it anyone cares about
- The object store from Move 49, holding a snapshot that was taken rather than assumed

**Software**
- `etcdctl` and `talosctl`, both pinned, and the snapshot verification step actually run
- A stopwatch, and somewhere to publish the number afterwards

**People**
- Two people, one driving and one writing down what is missing, because the gaps are the output

## The runbook
1. Take a snapshot and verify it. A snapshot that has not been verified is a file, and the verification step takes seconds.
2. Confirm where the off-site copies live: the snapshot, the machine configurations and the certificate authority material. All three are needed and only the first is usually thought about. They go to the object store from Move 49, whose own durability is Move 54's problem.
3. Destroy the quorum on the second cluster deliberately, having first confirmed nothing on it matters. Stop two of the three members and leave the cluster genuinely unable to elect.
4. Restore through a single-member bootstrap with a new cluster identity, then bring the other two members back and confirm they join. Start the stopwatch at step three and do not stop it until the cluster is serving requests.
5. Repoint the kubelets and confirm the workloads come back. A restored control plane with machines that cannot reach it is a half-finished restore.
6. Publish the wall-clock number and the list of things you had to look up. Both go into the runbook, and the second list is the more valuable of the two.
7. While you are here, run a defragmentation and check the backend size against its quota. A consensus store that hits its quota goes read-only, which presents as a cluster that will not accept any change at all.

## Operator's notes
- **Swap:** Where the second cluster does not exist yet, a three-machine scratch cluster is enough for this drill. What it cannot rehearse is the scale of the restore, which matters less than the procedure.
- **Do it faster:** Script the restore rather than documenting it. A script that has been run is worth more than a document that has been read.
- **Watch out:** Restoring a snapshot creates a new cluster identity. Members from the old cluster will refuse to join, and that refusal looks like a networking fault to anyone who does not know.
- **Leftovers:** The managed control-plane backup product on one of the three clouds keeps billing until Part VII, and it never covered this anyway.

## Rollback
There is nothing to reverse: the drill happens on a cluster built to be destroyed. The point of no return does not exist here, and that is the entire value of the exercise — it converts an unknown into a measured number at no risk. Repeat it quarterly, and repeat it after every upgrade in Move 108, because a restore procedure that worked on the previous version is not evidence about this one.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The managed backup product, where you bought one, stays until Part VII.
