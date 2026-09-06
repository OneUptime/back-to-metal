# 51 · The second cluster, and what it shares

**Layer:** Cluster · **Leaving:** The second managed cluster and its per-branch ephemeral variants · **Risk:** Low · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the non-production cluster the drills and rehearsals in this book assume, and states plainly what it shares with production and what it must not.

## Leaving from
- **AWS:** a second EKS cluster — a per-hour control-plane charge and a node group, duplicated for staging.
- **Google Cloud:** a GKE Autopilot cluster — the one that genuinely differs, because it removed node management from staging entirely and a self-hosted second cluster puts that cost straight back.
- **Azure:** a second AKS cluster — the same as the first, usually on the free control-plane tier.

## Why this works
Most of the drills in this book need somewhere to fail. The restore drill in Move 52, the upgrade rehearsal in Move 108, the verification gate in Move 72 and every per-branch clone all need a cluster that can be broken without a conversation. That cluster was sized back in Move 03 and is built here from the same boot assets as production, so that what it proves is transferable. What it shares is the interesting question, and the answers are deliberate: its own certificate authority and its own storage pool, but the same identity provider and, from Move 58, the same registry of record.

## Before you start

**Access**
- The machines allocated for non-production in Move 03, provisioned by Move 42
- The identity provider configuration from Move 50, ready to serve a second cluster

**Software**
- The same pinned versions as production, because a rehearsal on different versions rehearses the wrong thing
- Separate storage pool configuration, so a mistake in staging cannot consume production capacity

**People**
- Whoever will run the drills, since this cluster exists mainly for them

## The runbook
1. Build it from the same boot assets and the same pinned versions as production. A staging cluster that drifts is a staging cluster that stops predicting anything.
2. Give it its own certificate authority. Sharing one means a credential minted for staging is valid against production, which is the kind of mistake that is found during an incident review.
3. Give it its own storage pool. Sharing devices means a runaway test can fill the pool that production writes to.
4. Share the identity provider from Move 50 deliberately. One place to grant and revoke access is worth more than the isolation of a second directory, and the roles can still differ per cluster.
5. Share the registry of record from Move 58 once it exists. A second registry is how staging starts running images that production has never seen, which defeats the purpose of having staging.
6. State plainly, in writing and in the runbook, that this is not a disaster-recovery site. It has no copy of production data, it is not sized for production load, and describing it as a fallback is how a bad night becomes a worse one.

## Operator's notes
- **Swap:** Where hardware is tight, a smaller cluster of three machines still supports every drill in this book. What it cannot do is rehearse capacity behaviour, and that limitation should be written down.
- **Do it faster:** Build it before production, not after. Every mistake you are going to make is cheaper here, and the production build then takes a day instead of a fortnight.
- **Watch out:** Staging clusters accumulate exceptions — a version pinned back, a policy disabled for a demonstration — until they no longer resemble production. Reconcile the two on a schedule.
- **Leftovers:** The second managed cluster keeps its own control-plane charge and its own node group until Part VII. Autopilot readers should note that this line disappears entirely rather than shrinking.

## Rollback
This cluster is deleted and rebuilt from the same configuration in an afternoon, which is what makes it useful. There is no point of no return here at all; it holds no production data by construction and it is meant to be destroyed regularly. Keep its configuration in source control next to production's, and diff them periodically, so the rehearsal cluster can be restored to a state that genuinely matches what it is rehearsing for.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $890/mo | $0/mo | 100% | 0 min | 1 week | — |

## What you can turn off
Nothing yet, though the per-branch ephemeral clusters can move here as soon as the pipeline in Move 64 reaches it.
