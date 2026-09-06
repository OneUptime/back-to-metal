# 55 · Workload identity without the cloud's

**Layer:** Platform · **Leaving:** Cloud IAM workload identity: cluster OIDC federation, pod-identity agents and instance metadata credentials · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Publishes the cluster's own service-account issuer and federates it with each cloud's IAM, so pods on your metal hold the roles they held before, with no static key.

## Leaving from
- **AWS:** IAM roles for service accounts — an estate already on the newer pod-identity agent has to convert back to this shape first, because that agent exists only inside the managed cluster.
- **Google Cloud:** workload identity federation — the one that genuinely differs, because the provider accepts an uploaded key set, so your issuer need not be reachable from the internet at all.
- **Azure:** federated credentials on a managed identity — capped at twenty per identity, which forces a naming scheme before the first one is created.

## Why this works
Your workloads currently get cloud credentials because the managed cluster's identity issuer is trusted by the cloud's identity service. Your own cluster can be trusted the same way: publish the discovery document and the signing keys at a stable address, tell the API server to issue tokens naming that address, and register it as a federated identity provider in each cloud that still holds resources you need. The result is that a pod running on your metal holds exactly the role it held before, with no static key anywhere. This has to work during the migration, because for months the workloads are here and the data is still there.

## Before you start

**Access**
- Permission to create an identity provider in each cloud account that still holds resources
- A stable, durable place to publish the discovery document and key set, outside the cluster

**Software**
- The API server issuer setting, applied through the machine configuration from Move 41
- An inventory of every role each workload currently assumes, which is the bulk of the work

**People**
- Whoever owns cloud identity policy, because federating a new issuer is a decision they should make knowingly

## The runbook
1. Build the per-role inventory first. Every workload, every role it assumes, and what that role can do. This is four days of the five and it is the part that finds the roles nobody remembers granting.
2. Publish the discovery document and the signing key set at a stable address that does not depend on the cluster being up. An object bucket with a fixed name is the usual answer; the address is effectively permanent, so choose it carefully.
3. Set the issuer on the API server through the machine configuration and confirm a freshly issued token names it. Applying this changes every token in the cluster, so do it before workloads arrive.
4. Register the issuer in each cloud. The audience value differs per provider and getting it wrong produces an authentication error that says nothing useful, so take it from the provider's own documentation rather than from a copied example.
5. Convert any estate on a newer agent-based identity mechanism back to the federated shape first. That agent only exists inside the managed cluster and there is nothing to carry across.
6. Write down the signing-key rotation order — publish the new key, wait for caches, start signing with it, retire the old one — and the revocation path for a role that has to be withdrawn in a hurry. Both are needed before anything depends on this.

## Operator's notes
- **Swap:** Where a workload needs one cloud credential and nothing else, a short-lived static credential with a rotation job is defensible for a few weeks. Write the end date down when you create it.
- **Do it faster:** Do the inventory with the cloud's own access analyser rather than by reading policy documents. It finds roles that are granted and never used, which are the ones to delete rather than federate.
- **Watch out:** The provider that caps federated credentials per identity will let you create the twenty-first and fail, at the worst moment. Decide the naming scheme and the identity granularity before creating the first.
- **Leftovers:** The old cluster's identity provider stays registered until Part VII. Removing it early breaks the way back.

## Rollback
The issuer setting is reverted through the machine configuration and the federated providers are deleted in each cloud, both in minutes. There is no point of no return here, and the risk is confined to the moment the issuer changes, which invalidates existing tokens. Keep the issuer address, the key set and the federation configuration in source control so a working identity path can be restored quickly, and keep the previous signing key until every consumer has stopped using it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 5 days | — |

## What you can turn off
Nothing yet. The cloud roles stay exactly as they are, and this Move is what lets your own machines keep using them.
