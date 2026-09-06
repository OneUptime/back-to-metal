# 40 · The management VLAN, and the way in at 03:00

**Layer:** Cluster · **Leaving:** Cloud serial console and agent-based remote shell · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Builds the management VLAN, rotates the BMC credentials off the sticker, and drills the break-glass path before Move 50 can lock everyone out at once.

## Leaving from
- **AWS:** EC2 Serial Console with Session Manager — a console and a shell, both reached through the provider's control plane rather than your network.
- **Google Cloud:** the serial console with Identity-Aware Proxy — the same, except that serial access is a permission an organisation policy commonly disables, so many readers never used it.
- **Azure:** Serial Console with Bastion and Run Command — the same again, with three separate services covering what is here one VLAN and one jump host.

## Why this works
Every remote path you had went through somebody else's control plane, which meant it kept working when your own network did not. Reproducing that property is the whole content of this Move: a management network with no default route, reachable only through a jump host, carrying the management controllers bought in Move 08 and the console server bought in Move 16. The second half is break-glass — a path that works when the API server, the identity provider and internal name resolution are all down at the same time — and it is drilled here, because Move 50 puts identity in front of the cluster and can otherwise lock everyone out at once.

## Before you start

**Access**
- The management range from Move 39 and the out-of-band hardware from Move 16, installed
- The default controller credentials from the build, which are about to be replaced

**Software**
- A credential store that the break-glass path does not depend on, and a sealed copy of the emergency credentials
- `ipmitool` and a Redfish client for the smoke test, one per vendor if you have mixed hardware

**People**
- Two people who will drill the break-glass path, because a path one person knows is not a path

## The runbook
1. Build the management VLAN with no default route. Nothing on it reaches the internet and nothing on the internet reaches it; the only way in is the jump host, and the only way out is the out-of-band uplink from Move 16.
2. Rotate every controller credential off the sticker, and record the firmware baseline for each machine at the same time. Default credentials on a management controller are the single most exploited weakness in a private estate.
3. Run a Redfish smoke test per vendor: inventory, power state, boot override, and one virtual media mount. Confirm `ipmitool` covers whatever Redfish does not, and write down which tool does which.
4. Build the jump host outside the cluster's failure domain. It does not run on the cluster, it does not authenticate against the cluster's identity provider, and it does not resolve names using the cluster's name service.
5. Seal the break-glass credentials somewhere physical and auditable, and record who may open them and what happens afterwards. Rotation after use is part of the procedure, not an afterthought.
6. Drill it. Disable the identity provider for an hour, on purpose, in daylight, and have two people reach a machine console and recover it. Move 50 is gated on this drill having been done, and the drill is the reason it is gated.

## Operator's notes
- **Swap:** Where a cellular router is the out-of-band uplink, test it with the primary link down rather than assuming. Some cellular services fail closed on a captive portal that nobody notices until it matters.
- **Do it faster:** Do the credential rotation as part of the acceptance testing in Move 18, before the machines are racked. It is much faster with a keyboard in front of the machine.
- **Watch out:** A jump host that authenticates against the same identity provider as everything else is not a break-glass path. Its whole value is being independent, and that independence has to be deliberate.
- **Leftovers:** The cloud bastion, session manager and serial console stay in place until Part VII. They are how you reach the old estate while it still carries production.

## Rollback
Everything here is configuration and is reversed by reverting it. There is no point of no return in this Move, which is exactly why the drill happens now rather than after Move 50 has put identity in front of the API. If the break-glass credentials are lost, the controller passwords can be restored through a physical reset at the machine, which is the reason the whole path is worth documenting. Keep the procedure in source control and the credentials nowhere near it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 days | — |

## What you can turn off
Nothing yet. The provider's console and shell services remain the way into the old estate.
