# 13 · Images, secrets and one-command deploys

**Layer:** Move · **Leaving:** Managed registries, secret stores and hosted CI runners · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Three pieces of plumbing, then staging moves onto them: the first real workload on hardware you own, and the only one whose bad afternoon costs you nothing.

## Leaving from
- **AWS:** ECR and Secrets Manager — the registry token expires every twelve hours, and a secret you remove holds its name for thirty days unless you ask for the seven-day minimum.
- **Google Cloud:** Artifact Registry and Secret Manager — values are immutable, so every rotation leaves a billable version until destroyed.
- **Azure:** Container Registry and Key Vault — soft-delete cannot be switched off, and purge protection, once on, holds the name ninety days.

## Why this works
Nothing real has moved yet, so this is the moment for plumbing. Container workloads use a registry and Kubernetes manifests reconciled by Argo CD. VM workloads keep versioned OS templates and their existing application deployment recipes in Git; the hypervisor does not replace that tooling. Secrets encrypted under a key held outside the platform let either kind of workload recover its credentials. The detailed registry and runner steps below are the container reference. A VM-only estate can retain its existing artifact store and runner service while proving the same deployment and recovery checks.

Staging goes before customers do. Exercise the same VM templates or container images, secret delivery and deployment path production will use, against staging's own data. A guest that loses its configuration on reboot and a pod whose volume will not bind both belong here. Keep staging on the new platform for a fortnight of real branch deployments before Move 14 introduces production traffic.

## Before you start

**Access**
- A Git repository the deployment tooling can read, with a deploy key held outside the platform
- Access to the existing image registry or VM artifact store and the Proxmox templates

**Software**
- For containers: Argo CD 3.0 and Harbor 2.12, installed with `helm` at pinned chart versions, and an ephemeral runner controller
- For VMs: the existing versioned application deployment and runner tooling
- `sops` and `age` for encrypting secrets, with the private key kept outside the platform

**People**
- One engineer who owns the repository layout; two owners produce two conventions

## The runbook
1. For container workloads, stand the registry up as a cache. `helm install` Harbor at chart version 1.16.2 on the Ceph object store from Move 12, proxying the registry you use today. Repoint pulls and confirm workloads still start. A VM-only estate skips the registry steps and retains its artifact store.
2. Make it where images are pushed. Move the pipeline's push target across and mirror ninety days of tags, so both registries hold the same images while yours is on trial.
3. For Kubernetes, `helm install` Argo CD at chart version 8.1.3 so the repository rebuilds namespaces, deployments, network policy and storage classes. For VMs, record template checksums, guest resource settings and the pinned application deployment recipe there instead. Bootstrap credentials stay outside the platform.
4. Encrypt every secret into the repository with `sops`, under an `age` key kept in a password manager and one offline copy. Feed decrypted secrets through the existing VM deployment tool or the Kubernetes bootstrap path. Limit the bootstrap key to that process; never bake it into a template or image.
5. After backing up staging data, rebuild a disposable VM from its template and deployment recipe, or delete a non-production namespace and let the reconciler recreate it. Check that the workload and its secrets return; restore the staging data and verify its contents.
6. For Kubernetes runners, install the ephemeral controller at chart version 0.12.1 and route builds to it by label. VM deployments can keep their current runners. Test both routes by changing one line: the pipeline must build the pinned artifact and deploy to the intended guest or namespace without manual repair.
7. Move staging and review environments to their assigned guests or namespaces, update DNS, and use them for a fortnight of branch deployments. Their data may remain in the cloud, but only in staging's own stores. Reboot a guest or redeploy a container for each route in use; neither passes until its configuration survives.

## Operator's notes
- **Swap:** A plain registry over the same object store drops the database and cache Harbor needs, and with them projects, quotas and scanning.
- **Do it faster:** Do the cache in an afternoon and leave the registry of record a fortnight; most of the benefit arrives with the first half.
- **Watch out:** The registry has to run for the cluster to start, and the cluster for the registry to serve. Power the rack down and up once, deliberately, before an outage asks it.
- **Watch out:** Staging that still talks to production data stores has not moved, it has been relocated. Point it at its own copies before step seven.
- **Leftovers:** The cloud registry bills storage and egress until its images go, a Move 20 decision, and hosted runner minutes continue for anything still routed at them.

## Rollback
Revert the deployment recipe and route builds back to the existing runners. Restore staging data before returning a workload that has accepted writes; a Git revert cannot recover those writes. The point of no return is removing the old artifacts and credentials before their replacements have passed a rebuild. Keep the cloud registry, VM artifacts and secret store available until the corresponding guest or cluster has recovered from its recorded configuration.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,600/mo | $260/mo | 90% | 0 min | 7 days | 2 weeks |

## What you can turn off
The hosted runner minutes, once a week of builds has passed on your own nodes with no fallback. The non-production estate's cloud compute, once the fortnight in step seven is done and nobody has asked to go back. The cloud registry and its secret store stay funded until Move 20.
