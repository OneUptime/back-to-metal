# 14 · The card, the driver, and the kernel you will run

**Layer:** Iron · **Leaving:** The provider's paravirtual network interface and its single driver · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Per node, at the cost of a card swap and a reboot

> Chooses the network card against the Talos kernel rather than a datasheet, because there is no DKMS and no third place a driver can come from.

## Leaving from
- **AWS:** Elastic Network Adapter — one paravirtual device, one driver, in every kernel you were ever offered, so the question never arose.
- **Google Cloud:** virtio-net and the gVNIC adapter — two devices, both in-tree, and the choice between them was a performance setting rather than a procurement decision.
- **Azure:** the synthetic adapter with accelerated networking — a virtual function appearing beside a synthetic device, with the driver handled by the platform image.

## Why this works
Talos Linux is an immutable, API-driven operating system with no shell and no package manager, and that is the property this book wants. It also means a driver is either compiled into the kernel Talos ships or supplied as an official system extension, and there is no third option: no DKMS, no vendor installer, no compiling on the host. Kernel module signatures are enforced. So the network card is chosen against that kernel, by exact model and firmware requirement rather than by family, before the order goes out — because on the far side of delivery there is no recovery path except a different card.

## Before you start

**Access**
- The Talos release notes and kernel configuration for the version you intend to run in Part III
- The slot budget from Move 07 and the fabric decision from Move 13

**Software**
- The exact model and firmware level of each candidate card, from the vendor rather than from a reseller listing
- A loan machine you can boot Talos on and check that the interface appears

**People**
- Whoever will own the node lifecycle, since a card change later means touching every machine

## The runbook
1. List the candidate cards by exact model, not family. Two cards with the same marketing name can use different silicon and different drivers, and the one you get is the one on the part number.
2. Check each against the Talos kernel: in-tree driver, official system extension, or neither. Neither means it does not go on the list, however good the card is, because there is nowhere for the driver to come from.
3. Check the firmware requirement as carefully as the driver. A card whose driver needs firmware that is not shipped will bind and then fail to bring the link up, which is a much more confusing failure than a missing driver.
4. Boot Talos on a loan machine with the card in it and confirm the interface appears, links at the expected speed, and that the node comes back with the same interface name after a reboot. Ten minutes of this is worth every datasheet.
5. Decide the redundancy honestly. Two ports on one card is one PCIe device and one failure domain; genuine card redundancy is two cards, and it costs a slot. Twenty-five gigabit to the host against hundred gigabit uplinks is the sensible floor today.
6. Refuse SR-IOV and RDMA for the general cluster. They bypass the eBPF datapath that Move 60 enforces east-west policy in, and outside high-performance computing and dedicated storage fabrics they buy nothing you can measure against that cost.

## Operator's notes
- **Swap:** Where an existing card is unsupported and cannot be replaced, the honest answer is a different host operating system for those machines, not a patched Talos. Keep the exception small and write down why it exists.
- **Do it faster:** Buy one card of each candidate before the fleet order. The test is an afternoon and it removes the only failure in this Move that cannot be fixed remotely.
- **Watch out:** Card firmware and switch software have compatibility opinions, particularly around link training and forward error correction at twenty-five gigabit and above. Test the card against the switch you actually bought, on the cable you actually bought.
- **Leftovers:** Cards pulled from the old estate are usually the wrong generation and always the wrong firmware. Treat them as spares for a lab, not for production.

## Rollback
Changing card model after delivery is a per-node operation: drain the node, swap the card, reboot, return it to service. That is a maintenance window per machine rather than a disaster, which is why this Move is Medium risk rather than High. The point of no return is not a moment but a count: past about a dozen machines, swapping every card costs more than the difference between the cards ever will. Keep the tested model, firmware and Talos version recorded together so a known good combination can be restored on a replacement machine.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | — |

## What you can turn off
Nothing yet. The provider's network adapter stays in service until the workloads leave it in Parts IV to VI.
