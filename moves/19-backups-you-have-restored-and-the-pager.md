# 19 · Backups you have restored, and the pager

**Layer:** Run · **Leaving:** Managed backup, alarms and a rented paging service · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Velero, a continuous database archive and a copy somewhere you are not leaving — then the drill that turns a guessed recovery time into a measured one.

## Leaving from
- **AWS:** AWS Backup and CloudWatch alarms — a vault under compliance-mode lock cannot be shortened or removed until its retention expires.
- **Google Cloud:** Backup and DR Service and Cloud Monitoring — a backup vault's enforced retention makes a backup indelible until it expires, by you or by Google, so the copy outlives the decision to leave.
- **Azure:** Azure Backup and Azure Monitor alerts — a Recovery Services vault protects only resources in its own region, and soft delete holds removed items for fourteen days.

## Why this works
Two failures end a company here: the data cannot be got back, and nobody was woken. Schedules are cheap and worthless until somebody has rebuilt from them, so the deliverable is the drill — an estate reconstructed from the repository and the object store while production carries on untouched, with a stopwatch running. That figure is the recovery time objective, and it is usually several times the number in the plan. Monitoring runs on your platform; the alerting runs outside it, because a failed cluster cannot report its own failure. The existing cloud operations rota transitions with the services. Physical faults go to the contracted remote hands team or rental provider; your engineers retain software recovery and incident command within the same recurring-hours budget, validated during the pilot.

## Before you start

**Access**
- An account at an object storage provider unrelated to the cloud you are closing, with object lock
- Five days of one engineer's time for the rebuild drill, on a date nobody may move

**Software**
- `velero` 1.15 and the Barman Cloud plugin from Move 16, both pinned in the repository from Move 13
- `rclone` 1.68 for the copy out to the third provider
- Prometheus and Loki with a series budget agreed before the first scrape

**People**
- The existing operations rota, a named second escalation contact and a rule about what waits until morning
- The facility or rental provider's physical-support escalation and approved intervention runbooks

## The runbook
1. Schedule `velero` nightly for cluster objects, and let the Barman Cloud plugin archive the database from Move 16 continuously, both into the Ceph object gateway built in Move 12.
2. Copy that store out with `rclone` to a provider that is neither the rack nor the account being closed, with object lock on and append-only credentials, so one identity cannot reach both copies.
3. Do the drill. On the spare machine from Move 06, from the Git repository and those backups alone, build a cluster, restore the database and bring one service up, with nothing touching the original. Time it: that number is the recovery time objective, and the plan that disagrees is wrong.
4. Stand Prometheus and Loki up on your own nodes against the series budget, with drop rules at scrape time. A monitoring bill that outgrows the estate it watches is a cloud habit that follows you home.
5. Put the alerting where the cluster cannot take it down. OneUptime runs the probes, the rota, the escalation and the status page from outside; the author of this book founded OneUptime, and the copyright page says so. Add a dead-man's-switch heartbeat.
6. Transition the existing cloud rota to the new platform. Route physical faults to remote hands or the rental provider under the support contract; keep software recovery with the operations team. Test both escalation paths, name a backup contact, record what waits until morning and measure the hours against Move 03's budget.

## Operator's notes
- **Swap:** If the drill on the spare machine is disruptive, rent a dedicated server by the month and rebuild into that instead.
- **Do it faster:** Make the drill a script, not a document. The second run then takes an afternoon rather than a week.
- **Watch out:** Cluster objects without volume data restore an estate that starts cleanly and holds nothing. Count rows before calling the drill a pass.
- **Leftovers:** Backup vaults bill after the resources they protected are gone, and one under a retention lock stays until it expires.

## Rollback
Nothing here alters what serves traffic, so backing out is removing two schedules and leaving the managed alarms enabled. The point of no return is the day the provider's vaults age out: after that the only copy of last month is the one you wrote. Keep them until a restore from your own has been timed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,800/mo | $1,400/mo | 71% | 0 min | 5 days | — |

## What you can turn off
Managed backup vaults, their cross-region copies, the alarms and their ingestion, and the rented pager seats — once a restore of your own has been timed and one real page has woken somebody.
