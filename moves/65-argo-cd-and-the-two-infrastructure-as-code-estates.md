# 65 · Argo CD, and the two infrastructure-as-code estates

**Layer:** Platform · **Leaving:** Managed deployment services, pipeline deploy stages, source-repository connections and cloud-hosted remote state backends · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Argo CD reconciles the cluster from Git while the shrinking cloud estate stays described in its own modules, with one owner and one review path across both.

## Leaving from
- **AWS:** CodeDeploy and CodePipeline with an S3 state backend — a deploy service, a pipeline, and a state file with a lock table.
- **Google Cloud:** Cloud Deploy with a Cloud Storage state backend — the same shape, with delivery pipelines as first-class objects.
- **Azure:** Azure Pipelines release stages — the same again, with a Blob Storage state backend, and the one where build and deploy are the same pipeline object.

## Why this works
There are two estates here and they never merge. The cluster is reconciled from a repository by a controller that runs inside it, and everything about the cluster is described that way. The shrinking cloud footprint — the accounts, the identities, the buckets that stay — is described in its own modules with its own state. What matters is that both have one owner and one review path, so that a change to either is proposed, reviewed and recorded the same way. The other thing that matters is the bootstrap: the controller that deploys the platform cannot itself depend on the platform it deploys.

## Before you start

**Access**
- A repository the cluster can read, with a deploy credential that does not depend on the cluster
- The root of trust from Move 57, because the controller needs secrets before the platform exists

**Software**
- Argo CD at a pinned chart version, with an application-of-applications structure prepared rather than improvised
- The state backend moved deliberately, with the licence of the tool decided before the state file moves

**People**
- One owner for both estates, because two owners with two review paths is how they diverge

## The runbook
1. Choose the reconciler and say why. This book uses Argo CD, for its interface and its explicit synchronisation model, and the alternative is a perfectly good project that suits teams who prefer a smaller footprint. Do not run both.
2. Structure the repository as an application of applications, so that the whole platform can be recreated by pointing a fresh controller at one path. Test that by doing it on the second cluster from Move 51.
3. Solve the bootstrap explicitly. The controller needs its own credentials before the secret platform it deploys is running, so those come from the root of trust in Move 57 or from a sealed file, and the answer is written down rather than assumed.
4. Move the state backend for the cloud estate. Take the licence decision at the same time: the widely used tool moved to a source-available licence at version 1.6 and an openly licensed fork exists, and this is the moment to choose rather than after the state file has moved.
5. Fix the deprecated locking arrangement if you have one. A separate lock table is a superseded pattern and native state locking replaces it; migrate to the current shape rather than carrying the old one across.
6. Write the recovery as an ordered procedure: from an empty cluster and a repository, in what order does the platform come back. Move 115 drills it for real, and this Move is where the order is decided.
7. Run both delivery paths for thirty days. The managed deploy service stays configured and unused, which is the reversibility this Move claims.

## Operator's notes
- **Swap:** For a small estate, a pipeline that applies manifests directly is simpler and honest. What it loses is drift detection, which is most of the value once more than one person is deploying.
- **Do it faster:** Onboard the platform components first and the applications second. The platform is where the ordering problems live and they are better found without a product team waiting.
- **Watch out:** A reconciler with cluster-wide write access is the most powerful credential in the estate. Its access is scoped, its repository is protected, and Move 118 audits what it did.
- **Leftovers:** The managed deploy service, its pipelines and its source-repository connections keep billing until they are removed, and the connections in particular hold credentials that Move 122 must revoke.

## Rollback
For thirty days the managed deploy path stays configured, so a failed adoption is reverted by using it again. The point of no return is deleting those pipelines, which is a Part VII activity. Because everything is in a repository, a bad state is corrected by reverting a commit and letting the controller reconcile, and a lost cluster is restored by pointing a fresh controller at the same path — which is the property that makes this Move worth its three weeks.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $410/mo | $0/mo | 100% | 0 min | 3 weeks | 30 days |

## What you can turn off
The managed deploy service and its pipelines, thirty days after the reconciler has been the only thing deploying.
