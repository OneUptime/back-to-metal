# 13 · Images, secrets and one-command deploys

**Layer:** Move · **Leaving:** Managed registries, secret stores and hosted CI runners · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Three pieces of plumbing, then staging moves onto them: the first real workload on hardware you own, and the only one whose bad afternoon costs you nothing.

## Leaving from
- **AWS:** ECR and Secrets Manager — the registry token expires every twelve hours, and a secret you remove holds its name for thirty days unless you ask for the seven-day minimum.
- **Google Cloud:** Artifact Registry and Secret Manager — values are immutable, so every rotation leaves a billable version until destroyed.
- **Azure:** Container Registry and Key Vault — soft-delete cannot be switched off, and purge protection, once on, holds the name ninety days.

## Why this works
Nothing real has moved yet, so this is the moment for plumbing. A registry you own makes a build that cannot reach its base image a problem you fix, not an outage you watch. Cluster state in a repository, reconciled by Argo CD, makes every Move that follows a commit, and a commit can be reverted. Secrets encrypted there, under a key held outside the cluster, mean a cluster rebuilt from bare metal gets its credentials back. Runners come last because they hold most of the $640: hosted minutes bill by the minute, and a spiky build queue pays for waiting.

Then staging goes, and it goes before anything a customer touches. This is the sequencing decision the whole stage rests on. Staging is a real workload — real images, real secrets, real deploys, real people who will tell you within the hour when it is wrong — and it is the only real workload whose bad afternoon appears on no invoice, breaches no agreement and wakes nobody. Every class of problem the platform has, it has under staging first: a storage class that does not bind, a network policy nobody wrote down, a base image that only existed in a cache, a deploy that works once and not twice. You would rather find those with your own engineers complaining in a channel than with Move 14's production service in front of users. It is also the honest rehearsal for the ones after it, because a staging estate is usually the same shapes as production at a tenth of the size.

## Before you start

**Access**
- A Git repository the cluster can read, with a deploy key held outside it
- An account on the registry you push to today, so the cache can pull private images

**Software**
- Argo CD 3.0 and Harbor 2.12, both installed with `helm` at pinned chart versions
- `sops` and `age` for encrypting secrets, with the private key kept off the cluster
- A runner controller for your forge, ephemeral rather than long-lived

**People**
- One engineer who owns the repository layout; two owners produce two conventions

## The runbook
1. Stand the registry up as a cache. `helm install` Harbor at chart version 1.16.2 on the Ceph object store from Move 12, proxying the registry you use today. Repoint pulls and confirm workloads still start.
2. Make it where images are pushed. Move the pipeline's push target across and mirror ninety days of tags, so both registries hold the same images while yours is on trial.
3. Put the cluster in the repository. `helm install` Argo CD at chart version 8.1.3, as an application of applications, so one path rebuilds namespaces, deployments, network policy and Move 12's storage classes. Bootstrap credentials come from outside the cluster.
4. Encrypt every secret into the same repository with `sops`, under an `age` key kept in a password manager and one offline copy. A rebuilt cluster is seeded with that key by hand; the key never lives inside the thing being rebuilt.
5. Delete a non-production namespace and let the reconciler put it back. Do this only after step four, and check the workload returns with its secrets attached.
6. Install the ephemeral runner controller at chart version 0.12.1 and route builds to it by label. Then the acceptance test: an engineer changes one line and the image builds, lands in your registry and deploys with nobody at a console.
7. Move the whole non-production estate — staging, review environments, whatever the branch builds deploy to — and leave it there. Point its DNS at the new cluster, let its data stay wherever it is for now, and tell the engineers who use it that it has moved and where to complain. Then use it: for a fortnight, every branch deploys here and nowhere else. The bugs this finds are the bugs Move 14 would otherwise find in front of users, and the cost of finding them here is somebody saying the preview is slow.

## Operator's notes
- **Swap:** A plain registry over the same object store drops the database and cache Harbor needs, and with them projects, quotas and scanning.
- **Do it faster:** Do the cache in an afternoon and leave the registry of record a fortnight; most of the benefit arrives with the first half.
- **Watch out:** The registry has to run for the cluster to start, and the cluster for the registry to serve. Power the rack down and up once, deliberately, before an outage asks it.
- **Watch out:** Staging that still talks to production data stores has not moved, it has been relocated. Point it at its own copies before step seven.
- **Leftovers:** The cloud registry bills storage and egress until its images go, a Move 20 decision, and hosted runner minutes continue for anything still routed at them.

## Rollback
All of this is a repository: a bad change is a revert, and the reconciler catches up. Pulls point back at the cloud registry, builds back at hosted runners by one label. The point of no return is the day the cloud registry's images go, because a restore then means rebuilding from source, not pulling a tag. Keep the cloud secret store populated until a rebuilt cluster has decrypted its own secrets unaided.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,600/mo | $260/mo | 90% | 0 min | 5 days | 2 weeks |

## What you can turn off
The hosted runner minutes, once a week of builds has passed on your own nodes with no fallback. The non-production estate's cloud compute, once the fortnight in step seven is done and nobody has asked to go back. The cloud registry and its secret store stay funded until Move 20.
