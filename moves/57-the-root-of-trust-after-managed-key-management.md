# 57 · The root of trust after managed key management

**Layer:** Platform · **Leaving:** Managed key management and cloud HSM services, cloud-backed auto-unseal, envelope encryption in CI, and the cloud secret store as the record · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> The managed key could be neither exfiltrated nor lost, so replacing it means naming the humans, the HSM or the TPMs that hold it now, with a rehearsed recovery.

## Leaving from
- **AWS:** KMS and CloudHSM — a key that could not be exported and could not be lost, scheduled for deletion with a waiting period you could cancel.
- **Google Cloud:** Cloud KMS and Cloud HSM — the same properties and the same cancellable destruction window.
- **Azure:** Key Vault and Managed HSM — the same again, except that with purge protection enabled the old key cannot be destroyed on your timetable at all, which is a constraint Move 122 inherits.

## Why this works
The managed key had two properties that are hard to reproduce together: nobody could take a copy of it, and nobody could lose it. Replacing it means choosing which of those you are willing to work for, and there are three honest custody models. Shares of the key held by named people, which is strong and depends on those people being reachable. A hardware module in the cabinet, which is strong and is a single physical thing in a building. Or a key sealed to the control-plane machines themselves, which is convenient and ties recovery to hardware that can fail. None of the three is best; each has a failure mode, and this Move is about naming yours.

## Before you start

**Access**
- The physical security position from Move 35 and the encryption decisions from Move 48
- The secret inventory from Move 56, including the certificates and keys that one provider holds as separate object types

**Software**
- The chosen secret store, licensed deliberately: an openly licensed fork rather than the source-available original where that matters to you
- A recovery procedure written before the system is depended upon, not after

**People**
- Custodians with named deputies, and a rehearsal in the calendar before anything depends on this

## The runbook
1. Choose the custody model and write down its failure mode in one sentence. Shares held by people fail when the people are unreachable; a module in the cabinet fails when the building does; a key sealed to machines fails when the machines are replaced.
2. Pick the software with the licence read rather than assumed. The widely deployed secret manager moved to a source-available licence; an openly licensed fork exists and is the book's default. For an estate small enough that a share-based ceremony is theatre, file-level encryption with a simple key tool is a legitimate and much simpler answer.
3. Stand it up, seal it, and rehearse the recovery with the custodians before migrating anything. Two days of ceremony rehearsal is the recommended budget and it is the step that gets cut and then regretted.
4. Migrate the secrets from the cloud stores, remembering that one provider holds certificates and keys as first-class objects alongside secrets, so three shapes travel rather than one.
5. End the Move 56 bridge on its written date. Turn off the synchronisation, confirm every workload still starts, and remove the federated read access afterwards rather than before.
6. Plan the destruction of the old keys with the provider difference in mind, only after a full billing cycle has confirmed nothing still reads them. Two providers schedule destruction with a cancellable waiting period; one, with purge protection on, will not let you destroy the key on your schedule at all, and Move 122 has to allow for that.

## Operator's notes
- **Swap:** For fewer than about twenty secrets, file-level encryption committed to source control with a key held in two places is genuinely better than a secret manager nobody has rehearsed recovering.
- **Do it faster:** Rehearse the recovery with the actual custodians, in a room, once. It takes an afternoon and it converts a document into a capability.
- **Watch out:** A secret store that seals itself on restart and can only be opened by people who are asleep is an outage waiting for a power cut. Whatever model you choose, the recovery has to be possible at three in the morning.
- **Leftovers:** The cloud keys stay for thirty days after the migration, because that is the window in which you find the workload nobody knew was using one.

## Rollback
For thirty days the old keys still exist and the bridge can be restarted, so a failed migration is recoverable by repointing workloads at the cloud store. The point of no return is the destruction of the old key material, which is deliberately deferred to Move 38 and Move 122. Rehearse the recovery of the new store before that date, because after it the only way back from a lost key is a restore of data encrypted under a key that no longer exists, which is to say no way back at all.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $640/mo | $40/mo | 94% | 0 min | 2 weeks | — |

## What you can turn off
The cloud key management keys and the secret stores behind them — thirty days after the migration, and after a billing cycle has shown nothing still reading them.
