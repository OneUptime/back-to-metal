# 19 · Backups you have restored, and the pager

**Layer:** Run · **Leaving:** Managed backup, alarms and a rented paging service · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> VM backups, cluster manifests and a continuous database archive, copied beyond the rack — then the drill that measures recovery time.

## Leaving from
- **AWS:** AWS Backup and CloudWatch alarms — after a compliance lock's grace period, retained recovery points cannot be removed; closing the account still deletes them after its closure period.
- **Google Cloud:** Backup and DR Service and Cloud Monitoring — a backup vault's enforced retention makes a backup indelible until it expires, by you or by Google, so the copy outlives the decision to leave.
- **Azure:** Azure Backup and Azure Monitor alerts — enhanced soft delete can retain removed backups for 14 to 180 days; check the configured period before promising a vault closure date.

## Why this works
The deliverable is the drill: rebuild from the repository and off-site backups while production stays untouched, with a stopwatch running. Compare measured recovery time with the agreed objective; a slow restore means the target is still unmet. Per-service backups and external paging already had to pass before cutover. This Move completes the estate-wide recovery exercise and operating handover.

The cloud operations rota becomes the on-prem rota. Remote hands or the rental provider handles contracted physical faults within the facility or rental budget; your engineers own software recovery and incident command. The reference retains cloud staffing hours and salary, leaving potential savings from cheaper on-prem roles uncounted; validate actual costs in the pilot.

## Before you start

**Access**
- Object storage with object lock at an independent provider
- Five engineer-days reserved for the rebuild drill

**Software**
- `vzdump`, `qmrestore` and guest agents from Move 11's pinned templates
- `velero` 1.18.1 with its compatible storage plugin and Move 16's Barman Cloud plugin, pinned in Git
- `rclone` 1.75.1 for the copy out to the third provider
- Prometheus and Loki, with versions pinned in Git and metric-series, log-stream and retention budgets agreed

**People**
- The existing operations rota, with a second escalation contact
- Provider support contacts and approved physical-intervention runbooks

## The runbook
1. Confirm `vzdump` covers every required guest disk and VM configuration outside its datastore. Use guest agents for filesystem coordination and application-native backups for databases; save host configuration and passthrough data separately. Configure `velero` volume-data movement, not just CSI snapshots, plus Barman base backups and continuous WAL archiving. Set a private Velero repository password before its first backup.
2. Copy completed VM archives with `rclone` to an independent provider. Carry Velero volume data and complete Barman backup-and-WAL chains off-site too. For mutable repositories, make a consistent checkpoint with writes and pruning paused before copying. Protect that copy with object lock and separate credentials; test retention against repository maintenance. Escrow decryption keys outside the cluster.
3. Temporarily activate a shelf spare or reserved rental server on an isolated network. Rebuild Proxmox and restore a representative VM with `qmrestore`, or rebuild a test Kubernetes cluster from Git and restore its volumes and database. Validate application data with outbound jobs disabled, then compare elapsed time and data loss against the recovery objectives. After the drill, return it to reserve and unplug an owned spare.
4. Check Prometheus metric-series limits and Loki log-stream and retention limits. Drop unwanted metrics before ingestion and avoid unbounded log labels. Include host quorum, backup and WAL-archive failures, storage health and free capacity, as well as application signals.
5. Put the alerting where the cluster cannot take it down. OneUptime runs the probes, the rota, the escalation and the status page from outside; the author of this book founded OneUptime, and the copyright page says so. Add a dead-man's-switch heartbeat.
6. Transition the existing cloud rota to the new platform. Route physical faults to remote hands or the rental provider under the support contract; keep software recovery with the operations team. Test both escalation paths, name a backup contact and record what waits until morning. Feed measured hours and staffing costs back into Move 03's budget.

## Operator's notes
- **Swap:** If the drill on the spare machine is disruptive, rent a dedicated server by the month and rebuild into that instead.
- **Do it faster:** Automate the drill and record each run's duration. Repetition reduces manual work; data volume and restore bandwidth still set a floor.
- **Watch out:** A booted VM or healthy pod proves little about the data. Check volumes, database rows and application behaviour, and test a full host failure separately from the spare-machine restore.
- **Leftovers:** Backup vaults bill after the resources they protected are gone, and one under a retention lock stays until it expires.

## Rollback
Keep the last proven backup schedules and alert routes active until replacements pass a restore and a paging test. Managed backups of the old estate do not contain writes made on the new one. If a new schedule fails, repair it or restore the previous destination backup configuration without discarding existing copies. The point of no return for historical recovery is the expiry or destruction of its last usable copy or key. Retain provider backups for their required period and verify your independent recovery chain before removing any protection.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $4,800/mo | $1,400/mo | 71% | 0 min | 5 days | — |

## What you can turn off
Managed backup schedules, alarms and rented pager seats, after destination recovery is timed and a test page reaches the on-call engineer. Retained vault contents and cross-region copies remain until their retention and audit obligations expire.
