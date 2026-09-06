# 42 · Netboot, node identity and failure-domain labels

**Layer:** Cluster · **Leaving:** Golden machine images, launch templates and the instance metadata service · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Netboots nodes from a per-MAC record that also carries node identity and the rack, PDU and switch labels every later spread constraint reads.

## Leaving from
- **AWS:** AMIs, launch templates and the instance metadata service — an image, a template and an identity endpoint that every workload assumed was there.
- **Google Cloud:** machine images, instance templates and the metadata server — the same three, with the metadata server also serving identity tokens.
- **Azure:** managed images and the instance metadata service — again the same idea, and again nothing to replace them with unless you build it.

## Why this works
A managed node arrived complete: an image, a template that configured it, and a metadata service that told it who it was. On your own hardware all three have to exist somewhere, and the cheapest place to put them is one record per network address. Address assignment points the machine at a boot chain, the boot chain hands it a machine configuration, and the same record carries the labels that everything later depends on: which rack, which power feed, which switch. Without those labels an inherited spread constraint is a rule that matches everything and therefore protects nothing.

## Before you start

**Access**
- The as-built from Move 37, which is where the rack, feed and switch facts come from
- The provisioning range from Move 39, and address assignment you control on it

**Software**
- A boot chain: address assignment with a next-server pointer, a chain loader and a place to serve machine configurations
- The Talos boot assets for your pinned version, built or fetched from the upstream image service

**People**
- Whoever will add the next machine, because this is the process they will follow and it should be written for them

## The runbook
1. Choose the provisioning components with the support position stated rather than implied. The Talos boot assets and the upstream image service are maintained by the project; one common provisioning server is minimally maintained; one is an early-stage project; and the vendor's own management product is licensed under terms that require a commercial licence for production use. Pick deliberately and record why.
2. Build the boot chain: address assignment with a next-server pointer, a chain loader, and machine configurations served per hardware address. Set the firmware boot order so that a machine which has been power-cycled comes back the same way every time.
3. Put node identity in the same record. No metadata service is issuing it any more, so the record that boots the machine is also the record that names it.
4. Carry the failure-domain labels in that record too: rack, power feed and switch, taken from the as-built rather than typed from memory. Every spread constraint and anti-affinity rule later in the book reads these labels.
5. Check inherited zone rules against reality. A rule that spread pods across cloud zones will match nothing here unless the labels exist, and it will fail open rather than failing loudly. This is worth checking hardest for readers leaving Azure, where zone numbers are mapped per subscription and the same number means different buildings to different subscriptions.
6. Time it with a stopwatch, from power button to a node reporting Ready. Then do it again on a machine that has already been in service, because that is the path Move 109 will use for every upgrade.

## Operator's notes
- **Swap:** For a small fleet, machine configurations on removable media work and remove the boot server entirely. It stops being reasonable somewhere around a dozen machines.
- **Do it faster:** Keep the per-machine record to the minimum that differs — address, identity, labels — and put everything shared in one patch applied to all of them.
- **Watch out:** Firmware boot order is the quiet failure. A machine that boots from a stale local disk instead of the network comes back as a version you retired, and it will pass every health check.
- **Leftovers:** Image build pipelines, launch templates and their versions stay in the cloud accounts until Part VII. They are the way back if the programme is aborted.

## Rollback
A machine is reprovisioned from nothing in minutes, so this Move is reversed by changing a record and rebooting. The point of no return is Move 47, after which a machine holds a bound volume and cannot be rebuilt casually. Keep the per-machine records and the boot configuration in source control so a known good provisioning state can be restored, and so that the fleet can be rebuilt from the repository rather than from a server nobody backed up.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 weeks | — |

## What you can turn off
Nothing yet. The managed node groups keep carrying production until Part IV.
