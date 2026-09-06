# 58 · The mirror, then Harbor as the registry of record

**Layer:** Platform · **Leaving:** Managed container registries: private and public repositories, geo-replication, lifecycle rules and pull-through cache rules · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> A proxy cache is the cheap half and Harbor becomes the registry of record, the component that stops anything scheduling or recovering when it is down.

## Leaving from
- **AWS:** ECR with pull-through cache rules — an account-level rule with an authorisation token that expires every twelve hours.
- **Google Cloud:** Artifact Registry with remote and virtual repositories — the closest managed equivalent to what you are about to build yourself.
- **Azure:** Container Registry — with geo-replication gated behind the premium tier, which is the line that disappears here.

## Why this works
This Move has a cheap half and an expensive half. The cheap half is a proxy cache in front of the public registries, which removes the rate limits and the outages you do not control, and takes an afternoon. The expensive half is making your own registry the record, because from that moment nothing schedules and nothing recovers while it is down. That is worth doing anyway, and it is worth understanding before you do it. The registry then needs a database and a cache of its own, which is this book's one deliberate exception to keeping databases out of Part IV.

## Before you start

**Access**
- The object store from Move 49 for the layers, and a local volume from Move 47 for the database
- The identity provider from Move 50, so people authenticate the same way here as everywhere

**Software**
- A proxy cache at a pinned version, and `skopeo` for copying pinned digests rather than tags
- Harbor at a pinned chart version, installed with `helm`, with its database and cache configured deliberately

**People**
- Whoever owns the build pipeline, because Move 64 will be pushing here within a fortnight

## The runbook
1. Stand up the proxy cache first, in front of the public registries you actually pull from. Point the cluster at it and confirm pulls succeed. This half is cheap and immediately valuable.
2. Understand what a cache is not. A cache holds what has been pulled; it does not hold what you have never pulled, and the difference only becomes visible during a recovery when nothing is warm. Copy the digests you depend on deliberately with `skopeo`, pinned by digest rather than by tag.
3. Install Harbor with `helm install` at a pinned chart version, with its database on a local volume from Move 47 and its layers in the object store from Move 49. This is the deliberate exception to keeping stateful services out of this Part, and it is made because the registry cannot depend on anything that depends on the registry.
4. Set up projects, robot accounts, quotas and garbage collection before anyone pushes. Retention rules written after a year of images are written against a full disk.
5. Move the pipeline to push here, and mirror from the cloud registry rather than cutting over. Both registries hold the images for thirty days, which is the reversibility window this Move claims.
6. Power the rack off and back on, deliberately, and watch what happens. The registry needs the cluster to run and the cluster needs the registry to start, and the only way to know how that resolves in your estate is to do it once on purpose.

## Operator's notes
- **Swap:** For a small estate, a simple registry with object storage behind it is enough, and it removes the database and cache entirely. You lose projects, quotas and scanning integration, which Move 59 then has to solve differently.
- **Do it faster:** Do the proxy cache today and defer the registry of record by a fortnight. The first half delivers most of the operational benefit on its own.
- **Watch out:** Garbage collection in a registry is a real operation with real risk, and it needs the images that are actually in use to be identifiable. Do not enable aggressive retention before Move 65 makes deployments declarative.
- **Leftovers:** The cloud registry keeps billing for storage and data transfer for thirty days after the switch, and that overlap is deliberate.

## Rollback
For thirty days both registries hold the images, so reverting is repointing the pipeline and the cluster back at the cloud registry. The point of no return is the day the cloud registry's images are deleted in Move 38, after which a restore means rebuilding images from source. Keep the mirror running for the whole window, and verify that a representative image can be pulled from the cloud registry on the last day before it goes.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $780/mo | $60/mo | 92% | 0 min | 2 weeks | — |

## What you can turn off
The managed registry's geo-replication today, and the registry itself after thirty days of the mirror running clean.
