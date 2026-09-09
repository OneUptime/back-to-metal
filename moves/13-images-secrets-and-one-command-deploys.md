# 13 · Images, secrets and one-command deploys

**Layer:** Move · **Leaving:** Managed registries, secret stores and hosted CI runners · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Registry, secrets and deployments are proved together in staging, before customers depend on the new platform.

## Leaving from
- **AWS:** ECR and Secrets Manager — registry tokens last twelve hours; scheduled secret deletion has a seven-to-thirty-day recovery window, with thirty days the default.
- **Google Cloud:** Artifact Registry and Secret Manager — values are immutable, so every rotation leaves a billable version until destroyed.
- **Azure:** Container Registry and Key Vault — soft-delete cannot be switched off once enabled; purge protection holds deleted names for the configured seven-to-ninety-day retention period.

## Why this works
Containers use Harbor and Argo CD; VMs keep versioned templates and existing deployment tools. Either route must recover credentials using a key held outside the platform. VM-only estates can retain their artifact store and runners.

Staging exercises production's templates, images, secrets and deployment path against its own data. A fortnight of branch deployments, plus a rebuild and restore, tests recovery before Move 14 introduces customer traffic.

## Before you start

**Access**
- A deployment repository, with its deploy key held outside the platform
- Registry or VM artifact access and CI credentials

**Software**
- For containers: `helm`, Argo CD and Harbor at the pinned versions below
- For GitHub Actions: Actions Runner Controller and isolated build infrastructure
- For VMs: versioned deployment and runner tooling
- `sops` and `age`, with the private key held externally

**People**
- One engineer responsible for the deployment and recovery conventions

## The runbook
1. For containers, use `helm install` to deploy Harbor 2.15.2 at chart version 1.19.2, storing image blobs on Move 12's Ceph object gateway. Back its database separately. Configure a proxy project only where the upstream adapter supports it; test private-image authentication before repointing pulls. VM-only estates can retain their artifact store.
2. Create a separate normal Harbor project for pushes; a proxy-cache project cannot accept them. Move the push target, mirror retained releases and verify image digests. Keep the cloud registry current during the trial so either deployment path can use the same release.
3. For Kubernetes, `helm install` Argo CD 3.5.2 at chart version 10.8.4 and configure applications with automated sync and self-healing, including namespace creation. For VMs, record template checksums, resource settings and the pinned deployment recipe in Git. Bootstrap credentials stay outside the platform.
4. Encrypt every secret into the repository with `sops`, under an `age` key kept in a password manager and one offline copy. Feed decrypted secrets through the existing VM deployment tool or the Kubernetes bootstrap path. Limit the bootstrap key to that process; never bake it into a template or image.
5. After backing up staging data, rebuild a disposable VM from its template and deployment recipe, or delete a non-production namespace and let the reconciler recreate it. Check that the workload and its secrets return; restore the staging data and verify its contents.
6. For GitHub Actions, install both Actions Runner Controller and its runner scale-set chart at version 0.14.2 on isolated build infrastructure. Set the repository URL, credential-secret reference and runner image digest; route jobs by scale-set name. Other CI services and VM deployments can retain existing runners. Test a commit through build and deployment.
7. Move staging and review environments to their assigned guests or namespaces, update DNS, and use them for a fortnight of branch deployments. Their data may remain in the cloud, but only in staging's own stores. Reboot a guest or redeploy a container for each route in use; neither passes until its configuration survives.

## Operator's notes
- **Swap:** A plain registry over the same object store drops the database and cache Harbor needs, and with them projects, quotas and scanning.
- **Do it faster:** Prove the image pull path first, then switch pushes after the restore test passes.
- **Watch out:** Keep bootstrap images independent of Harbor and prove recovery from a full rack restart with test workloads. Staging must use its own data copies before step seven; a registry cache does not break every dependency loop.
- **Leftovers:** The cloud registry bills storage and egress until its images go, a Move 20 decision, and hosted runner minutes continue for anything still routed at them.

## Rollback
Revert the deployment recipe and route builds back to the existing runners. Restore staging data before returning a workload that has accepted writes; a Git revert cannot recover those writes. The point of no return is removing the old artifacts and credentials before their replacements have passed a rebuild. Keep the cloud registry, VM artifacts and secret store available until the corresponding guest or cluster has recovered from its recorded configuration.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,600/mo | $260/mo | 90% | 0 min | 7 days | 2 weeks |

## What you can turn off
The hosted runner minutes, once a week of builds has passed on your own nodes with no fallback. The non-production estate's cloud compute, once the fortnight in step seven is done and nobody has asked to go back. The cloud registry and its secret store stay funded until Move 20.
