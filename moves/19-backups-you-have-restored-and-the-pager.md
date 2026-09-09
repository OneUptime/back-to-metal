# 19 · Backups you have restored, and the pager

**Layer:** Run · **Leaving:** Managed backup, alarms and a rented paging service · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> VM backups, cluster manifests and a continuous database archive, copied beyond the rack — then the drill that measures recovery time.

## Leaving from
- **AWS:** AWS Backup and CloudWatch alarms — a vault under compliance-mode lock cannot be shortened or removed until its retention expires.
- **Google Cloud:** Backup and DR Service and Cloud Monitoring — a backup vault's enforced retention makes a backup indelible until it expires, by you or by Google, so the copy outlives the decision to leave.
- **Azure:** Azure Backup and Azure Monitor alerts — a Recovery Services vault protects only resources in its own region, and soft delete holds removed items for fourteen days.

## Why this works
The deliverable is the drill: rebuild from the repository and off-site backups while production stays untouched, with a stopwatch running. Compare measured recovery time with the agreed objective; a slow restore means the target is still unmet. Monitoring runs on your platform; alerting runs outside it, because a failed cluster cannot report its own failure.

The existing cloud operations rota transitions with the services. Physical faults go to the contracted remote hands team or rental provider; your engineers retain software recovery and incident command within the same recurring-hours budget, validated during the pilot.

## Before you start

**Access**
- Object storage with object lock at an independent provider
- Five engineer-days reserved for the rebuild drill

**Software**
- `vzdump`, `qmrestore` and guest agents from Move 11's pinned templates
- `velero` 1.15 and Move 16's Barman Cloud plugin, pinned in Git
- `rclone` 1.68 for the copy out to the third provider
- Prometheus and Loki with a series budget agreed before the first scrape

**People**
- The existing operations rota, with a second escalation contact
- Provider support contacts and approved physical-intervention runbooks

## The runbook
1. Schedule `vzdump` for Proxmox guests to archive-file storage outside their datastore, including every required virtual disk and VM configuration. Use the guest agent to coordinate filesystems and application-native backups for database consistency. Save host configuration and recovery credentials separately; passthrough devices need their own data backups. For Kubernetes, schedule `velero` for objects and volume data, and continuous database archiving through the Barman Cloud plugin.
2. Copy completed VM backup archives and Kubernetes backup data out with `rclone` to a provider that is neither the rack nor the account being closed. Use object lock and separate credentials; the source cluster cannot remove retained copies. Verify that decryption keys survive its loss.
3. Temporarily activate a shelf spare or reserved rental server on an isolated network. Rebuild Proxmox and restore a representative VM with `qmrestore`, or rebuild a test Kubernetes cluster from Git and restore its volumes and database. Validate application data with outbound jobs disabled, then compare elapsed time and data loss against the recovery objectives. After the drill, return it to reserve and unplug an owned spare.
4. Stand Prometheus and Loki up on the active nodes against the series budget, with drop rules at scrape time. Include Proxmox host quorum, VM backup failures, storage health and free capacity, as well as application signals.
5. Put the alerting where the cluster cannot take it down. OneUptime runs the probes, the rota, the escalation and the status page from outside; the author of this book founded OneUptime, and the copyright page says so. Add a dead-man's-switch heartbeat.
6. Transition the existing cloud rota to the new platform. Route physical faults to remote hands or the rental provider under the support contract; keep software recovery with the operations team. Test both escalation paths, name a backup contact, record what waits until morning and measure the hours against Move 03's budget.

## Operator's notes
- **Swap:** If the drill on the spare machine is disruptive, rent a dedicated server by the month and rebuild into that instead.
- **Do it faster:** Make the drill a script, not a document. The second run then takes an afternoon rather than a week.
- **Watch out:** A booted VM or healthy pod proves little about the data. Check volumes, database rows and application behaviour, and test a full host failure separately from the spare-machine restore.
- **Leftovers:** Backup vaults bill after the resources they protected are gone, and one under a retention lock stays until it expires.

## Rollback
Nothing here alters what serves traffic, so backing out is disabling the new backup schedules and leaving the managed alarms enabled. The point of no return is the day the provider's vaults age out: after that the only copy of last month is the one you wrote. Keep them until a restore from your own has been timed.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,800/mo | $1,400/mo | 71% | 0 min | 5 days | — |

## What you can turn off
Managed backup vaults, their cross-region copies, the alarms and their ingestion, and the rented pager seats — once a restore of your own has been timed and one real page has woken somebody.
