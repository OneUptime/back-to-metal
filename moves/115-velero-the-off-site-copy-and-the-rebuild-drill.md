# 115 · Velero, the off-site copy and the rebuild drill

**Layer:** Watch · **Leaving:** Managed backup, snapshot lifecycle policies, cross-region copy and managed fault injection · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Backs up cluster state with Velero and volumes with CSI snapshots to another credential domain, and publishes an RTO measured by an actual rebuild.

## Leaving from
- **AWS:** Backup with cross-region copy and Fault Injection Service — a policy engine and a game-day tool, both of which stop with the account.
- **Google Cloud:** Backup for GKE with cross-region storage — the only one of the three that sold a cluster-workload backup product.
- **Azure:** Backup for AKS with geo-redundant vaults — which exists and is frequently overlooked, so this reader may have more to replace than they expect.

## Why this works
Two things need backing up and they are different: the cluster's own state, which is a set of objects, and the volumes, which are data. Velero handles the first and snapshots handle the second, and both go to the object store from Move 49 under the durability terms Move 54 established. The rule that makes them backups rather than copies is where the second copy sits: a different building, a different credential domain and, where it matters, a different jurisdiction, under immutability. Database backups stay with the repository from Move 74. And the whole thing ends with a measured rebuild, because an untested recovery time is a guess.

## Before you start

**Access**
- The object store from Move 49, made durable by Move 54, with an off-site target in a second credential domain
- Two drill days a year in the calendar, funded and defended

**Software**
- `velero` at a pinned version for cluster state, and volume snapshots configured through the storage driver
- Immutability on the off-site target, so a compromised credential cannot delete both copies

**People**
- Whoever will run the game day, and whoever will act on what it finds

## The runbook
1. Back up cluster state with `velero` on a schedule, and confirm what it captures and what it does not. Objects are captured; the data behind a volume is captured only if snapshots are configured.
2. Configure volume snapshots through the storage driver and confirm one can be restored into a new claim before trusting the schedule.
3. Send the off-site copy to a different building, a different credential domain and, where regulation requires it, a different jurisdiction, under immutability. A copy the cluster can delete with its own identity is not an off-site copy.
4. Leave the database backups where they are. The repository from Move 74 is purpose-built for point-in-time recovery and this Move does not duplicate it.
5. Schedule a game day twice a year to replace whatever fault-injection service the provider offered. Break something real, on purpose, in daylight, with people watching.
6. Do the rebuild drill: from the repository in Move 65 and these backups, rebuild a working cluster and restore a service into it. Measure the wall-clock time.
7. Publish that number as the recovery time objective, and use it to settle the second-site question that Move 24 deferred. If the measured rebuild is faster than the business can tolerate, the deferral was correct; if it is not, the trigger for a second site has been met.

## Operator's notes
- **Swap:** Where a full rebuild drill is too disruptive, rebuild into the second cluster from Move 51 instead. It measures the same thing at a fraction of the risk.
- **Do it faster:** Automate the rebuild as a script rather than a document, and run it every game day. A script that has been executed is worth more than a runbook that has been read.
- **Watch out:** A backup of cluster objects without the volume data restores an estate that starts and has nothing in it, which is a specific and demoralising kind of failure. Test both together.
- **Leftovers:** Managed backup vaults keep billing for their retention after the resources are gone, and vault lock can prevent deletion entirely until the retention expires.

## Rollback
Nothing here changes the running estate, so it is reversible by removing the schedules. There is no point of no return. The purpose of this Move is the opposite of risk: it is what makes every rollback paragraph elsewhere in the book true, because a restore that has been performed and timed is the only kind that counts. Treat a failed drill as an incident, with a postmortem, rather than as an inconvenience to be repeated later.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,480/mo | $120/mo | 92% | 0 min | 2 weeks | — |

## What you can turn off
Managed backup vaults, snapshot lifecycle policies and cross-region copy, once a rebuild has been performed from your own backups and timed.
