# 48 · Encryption at rest, and who holds the key

**Layer:** Cluster · **Leaving:** Default encryption at rest on managed volumes · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Encrypts the state and ephemeral partitions and the Ceph OSDs, and settles who holds the key when the only copy of it lives on the cluster it opens.

## Leaving from
- **AWS:** EBS default encryption with a managed key — a setting you had to switch on per account and per region, and the outlier of the three.
- **Google Cloud:** Persistent Disk encryption — every disk encrypted with a provider-managed key whether or not anyone asked, so this reader has a default to replace rather than a setting to port.
- **Azure:** Storage Service Encryption with disk encryption sets — also on by default, with customer-managed keys as the option on top.

## Why this works
Move 35 already established the fact that makes this necessary: facility staff can open your cabinet. Encryption at rest is what makes that fact survivable, and it has to be turned on before there is anything on the devices, because there is no in-place conversion. The Talos state and ephemeral partitions are encrypted with a key provider chosen deliberately — a node identifier for convenience, a hardware module to bind a device to the machine it was installed in, or an external key server — and the Ceph devices are created encrypted in Move 49, because encrypting them afterwards is a rebuild rather than a setting. The cluster's own secret store gets a key with a named custodian.

## Before you start

**Access**
- Machines not yet carrying anything, because this cannot be applied to a populated device
- The physical security position from Move 35, which is what this Move is answering

**Software**
- The chosen key provider configured and tested, including its recovery path
- The cluster encryption configuration, with a named key and a documented rotation procedure

**People**
- A named custodian for each key, with a deputy, recorded somewhere that outlives both of them

## The runbook
1. Choose the key provider deliberately, and write down what each choice means when a machine fails. A node identifier is convenient and offers little protection against a stolen device. A hardware module binds the device to the machine, which is stronger and means a device moved to another chassis will not open. An external key server is strongest and adds a dependency.
2. If you choose an external key server, understand the ordering problem: a state partition sealed by a network service cannot take its network configuration from the configuration stored on that partition. The network has to come up before the partition opens, and that has to be designed rather than discovered.
3. Enable encryption on the state and ephemeral partitions at install time, on every machine, before anything is bound to them.
4. Set the cluster's own at-rest encryption for secrets with a named key, and record the custodian, the deputy and the rotation procedure. This key protects the secrets that every workload depends on.
5. Solve the recursion before it bites: the only copy of a key must not live solely on the cluster that key opens. Put a sealed copy somewhere physical and record who may open it, exactly as Move 40 did for break-glass.
6. Test the recovery path. Take a machine, move its device to another chassis, and confirm the behaviour matches what you chose in step one. This is the test that tells you what your decision actually means.

## Operator's notes
- **Swap:** For an estate where physical access is genuinely controlled and the threat model is honest about it, a node-identifier key is a reasonable choice that keeps recovery simple. Write down the reasoning rather than the conclusion.
- **Do it faster:** Do this as part of the first install rather than as a second pass. Reinstalling twelve machines because encryption was forgotten costs a day that nobody planned.
- **Watch out:** Key rotation for the cluster secret store requires rewriting every secret. It is a documented procedure, it is not automatic, and it should be rehearsed once on the second cluster before it is needed.
- **Leftovers:** The provider's key management keys keep billing per key per month, and they are destroyed in Move 38 rather than here.

## Rollback
There is no in-place decryption, so this Move is irreversible on any machine it has been applied to: reversing it means reinstalling the machine. The point of no return is the first node installed with encryption enabled. That is acceptable precisely because it happens before anything is bound. If a key is lost, the data is not recoverable and the only path is a rebuild and a restore from the backups Move 54 and Move 74 create, which is the reason the sealed copy exists.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | — |

## What you can turn off
Nothing yet. The provider's key management stays until Move 38 destroys the key material deliberately.
