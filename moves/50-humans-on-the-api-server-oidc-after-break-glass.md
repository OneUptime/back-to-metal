# 50 · Humans on the API server: OIDC, after break-glass

**Layer:** Cluster · **Leaving:** Cloud IAM authentication to the managed cluster · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Points the API server at the identity provider you already run, maps groups to RBAC, and deletes the static admin kubeconfig from every laptop.

## Leaving from
- **AWS:** IAM with the authentication ConfigMap or access entries — a mapping from cloud principals to cluster identities that disappears with the account.
- **Google Cloud:** Cloud IAM with the authentication plug-in — the same, and it also disappears when the project does.
- **Azure:** Microsoft Entra ID with Azure role-based access — the shortest path of the three, because that directory is a general-purpose identity provider you keep.

## Why this works
Authentication to your old cluster was a property of the cloud account, and it goes away when the account does. What replaces it is the identity provider the organisation already runs and intends to keep, with groups mapped to cluster roles and credentials that expire. The important part of this Move is its ordering: it runs after the break-glass path in Move 40 has been drilled, and it blocks go-live. Without that ordering, Parts III to VII get operated from a copied administrator credential on somebody's laptop, which then becomes permanent, and the audit in Move 119 finds it.

## Before you start

**Access**
- The identity provider's configuration, and permission to register a new client against it
- The drilled break-glass path from Move 40, because this Move can otherwise lock everyone out at once

**Software**
- The API server configuration for the identity provider, applied through the machine configuration
- `kubectl` with an authentication plug-in that fetches short-lived credentials rather than storing long ones

**People**
- Whoever owns groups in the directory, because the mapping is theirs to maintain, not yours

## The runbook
1. Confirm the break-glass drill from Move 40 has actually been done, by two people, within the last month. This is a gate rather than a suggestion.
2. Register the cluster with the identity provider and configure the API server through the machine configuration. Get the claim names right first time by testing against a scratch cluster, because a wrong claim name looks exactly like a permissions problem.
3. Map directory groups to cluster roles. Keep the mapping small and boring: one group with administrative rights, one per team with namespace rights, and nothing bespoke per person.
4. Switch everyone to short-lived credentials through the authentication plug-in, and confirm that a credential actually expires by waiting for it to.
5. Delete the static administrator credential from every laptop, and rotate it. This is the whole point of the Move and it is the step most often deferred until it is forgotten.
6. Send the access log somewhere that survives the cluster. A record of who did what that lives only on the thing they did it to is not a record.

## Operator's notes
- **Swap:** Where no identity provider exists yet, this Move waits. Building one specifically for the cluster is a much larger project than it appears and it will be the wrong one.
- **Do it faster:** Test the whole flow on the second cluster from Move 51. The failure modes are confusing and they are much cheaper to meet there.
- **Watch out:** Group membership changes in the directory do not propagate until the credential is renewed. A removed engineer keeps access until their token expires, which is an argument for short lifetimes rather than long ones.
- **Leftovers:** The cloud identity mappings stay on the old cluster until Part VII. Do not remove them while that cluster is still carrying production.

## Rollback
The API server configuration is reverted through the machine configuration and reapplied, and the static credential can be regenerated, so this is fully reversible within minutes. The point of no return does not exist here, which is exactly why the break-glass gate matters: the risk is not permanence but simultaneity, since a mistake locks out everybody at once. Keep the configuration and group mapping in source control so a working state can be restored without guesswork at the moment nobody can log in.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet, though the static administrator credentials on laptops go today, and that is a real reduction in risk.
