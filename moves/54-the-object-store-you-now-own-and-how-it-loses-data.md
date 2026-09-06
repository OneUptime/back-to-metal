# 54 · The object store you now own, and how it loses data

**Layer:** Cluster · **Leaving:** Managed object-storage durability, versioning and object lock · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> States the replication factor, the off-site copy and the restore drill for the store that now holds backup repositories, log chunks and registry layers.

## Leaving from
- **AWS:** S3 with cross-region replication and Object Lock — durability quoted in elevens, replication as a bucket setting, and immutability as a mode.
- **Google Cloud:** Cloud Storage with dual-region buckets and bucket lock — the only one selling a single bucket name spanning two regions, so this reader loses a geographic property rather than a feature.
- **Azure:** Blob Storage with geo-redundant storage — the same durability story, with immutability policies and a different redundancy vocabulary.

## Why this works
The object store built in Move 49 has quietly become the durability floor under everything: the database backup repositories from Move 74, the log chunks from Move 63, the cluster backups from Move 115 and the registry layers from Move 58. None of those is a backup until this Move is done, because a backup that lives in the same failure domain as the thing it protects is a copy rather than a backup. So this Move fixes the protection scheme, the failure domain it spreads across, versioning, immutability, an off-site copy in a second credential domain, and a restore drill with a published number.

## Before you start

**Access**
- The object gateway from Move 49, and the link from Move 53 for the off-site copy
- A second credential domain for the off-site target, so one compromised credential cannot reach both copies

**Software**
- The pool protection scheme decided before any data is written, because it cannot be changed in place afterwards
- `rclone` or `mc` for the off-site copy, pinned, with a schedule and an alert on failure

**People**
- Whoever owns the recovery objectives from Move 24, because this Move is what makes those objectives real

## The runbook
1. Fix the data pool's protection scheme now: replication for latency-sensitive pools, erasure coding for large cold ones. This cannot be changed in place once the pool holds data, so it is decided before the first object is written.
2. Set the failure domain the pool spreads across to the rack labels from Move 42, and verify by asking the cluster where the copies of a test object actually are rather than assuming.
3. Turn on versioning where the workload benefits from it, and set object immutability where a retention requirement exists. Note that on some releases immutability can only be enabled when a bucket is created, so it is a creation-time decision rather than a later one.
4. Build the off-site copy over the link from Move 53, into a second credential domain. Schedule it, alert on failure, and check the alert works by breaking the copy deliberately once.
5. Run a restore drill: take a backup repository, delete it from the primary store, and restore it from the off-site copy. Time it and publish the number.
6. Write the failure modes down in plain language, because everyone downstream now depends on this store: what happens when a machine is lost, when a rack is lost, when the pool passes its fullness threshold, and when the off-site copy has been silently failing for a week.

## Operator's notes
- **Swap:** Where an off-site copy in your own second location does not exist yet, a small amount of cloud object storage is a perfectly good target and costs very little for backups. Keeping it is not a failure of the programme.
- **Do it faster:** Do the restore drill on the smallest real repository you have rather than the largest. The procedure is what you are testing, and it transfers.
- **Watch out:** A cheap off-site copy in the same credential domain as the primary is not protection against the failure that matters most, which is a credential doing something destructive everywhere at once.
- **Leftovers:** Cross-region replication and versioning in the cloud keep billing throughout the migration. They are removed in Move 38, deliberately and last.

## Rollback
The protection scheme is irreversible once the pool holds data, so there is no way back from that decision except a new pool and a copy. The point of no return is the first object written into a pool created with the wrong scheme. Everything else here — versioning, the off-site copy, the schedule — is reversible. Keep the pool configuration and the drill results in source control so the tested state can be restored and compared when the store behaves differently a year from now.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,310/mo | $180/mo | 92% | 0 min | 2 weeks | — |

## What you can turn off
Nothing yet. Cross-region replication and immutability policies stay until Move 38 removes them against a signed approval.
