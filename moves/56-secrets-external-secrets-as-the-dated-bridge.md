# 56 · Secrets: External Secrets as the dated bridge

**Layer:** Platform · **Leaving:** — · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> External Secrets Operator syncs the cloud secret stores into the cluster under a written end date, so workloads can land before the root of trust has moved.

## Leaving from
- **AWS:** Secrets Manager and Parameter Store — two services, one billed per secret and per API call, the other largely free at the standard tier.
- **Google Cloud:** Secret Manager — one service, versioned, billed per secret version and per access.
- **Azure:** Key Vault — one service holding secrets, certificates and keys as three first-class object types, which makes the eventual migration in Move 57 carry three shapes rather than one.

## Why this works
Workloads have to land on your cluster months before the root of trust moves, and they need their secrets on the first day. This Move builds a bridge rather than a destination: an operator that reads the cloud secret stores, authenticated by the federated identity from Move 55 rather than by a key in a file, and writes the values into the cluster as secrets. Nothing is chosen as the store of record here; the cloud store stays authoritative until Move 57 replaces it. The one thing that must happen today is writing the end date down, because bridges that have no end date become architecture.

## Before you start

**Access**
- The federated identity from Move 55, working, so the operator authenticates without a static credential
- Read access to the secret stores in every account that still holds one

**Software**
- The External Secrets Operator at a pinned chart version, installed with `helm`
- An inventory of secrets by store, with a note of which are actually read at runtime

**People**
- Whoever will own the eventual migration in Move 57, because the end date is their commitment

## The runbook
1. Install the operator with `helm install` at a pinned chart version, authenticated through the federated identity from Move 55. If it needs a static key to start, something in Move 55 is not finished.
2. Define one store resource per cloud secret service and confirm the operator can read from each. Three services across three clouds is the common case and each has its own authentication shape.
3. Set the refresh interval as a cost decision rather than a preference. Two of the three providers bill per read, and a five-minute refresh across a few thousand secrets is a bill that shows up a month later with no obvious cause.
4. Sync only the secrets that are actually read at runtime. An inventory that lists four hundred secrets usually contains fifty that matter and three hundred and fifty that were created once by a pipeline.
5. Confirm rotation propagates: change a value at the source, and time how long until a pod sees it. That number is what Move 57 will have to match or beat.
6. Write the end date into the exit plan on the day the operator is installed, with a named owner. This is a bridge, and the date is what stops it becoming the design.

## Operator's notes
- **Swap:** For a small estate, a manual copy of a dozen secrets into the cluster is faster and honest, provided it is written down and dated the same way.
- **Do it faster:** Start with one namespace and one store. The shapes are all the same once the first one works, and the first one takes most of the day.
- **Watch out:** Syncing a secret into the cluster puts a plaintext copy in the consensus store unless at-rest encryption from Move 48 is on. It is on, if Move 48 was done, and it is worth confirming rather than assuming.
- **Leftovers:** The cloud secret stores keep billing per secret and per read for as long as this bridge exists, which is another reason for the end date.

## Rollback
Removing the operator stops the synchronisation and leaves the existing cluster secrets in place, so nothing breaks at the moment of removal. There is no point of no return in this Move; the cloud store remains authoritative throughout, which is the entire design. Keep the store and secret definitions in source control so the sync configuration can be restored, and confirm the cloud copies are intact before deleting anything on either side.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $210/mo | $210/mo | 0% | 0 min | 3 days | — |

## What you can turn off
Nothing. This Move deliberately keeps paying the cloud secret bill so that workloads can move before the root of trust does.
