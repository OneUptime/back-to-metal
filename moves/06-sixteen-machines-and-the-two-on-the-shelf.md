# 06 · Sixteen machines, and the two on the shelf

**Layer:** Buy · **Leaving:** Elastic node capacity and cluster autoscaling · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Sixteen active nodes and two reserved replacements, bought for the shelf or included in the rental quote, because iron does not autoscale.

## Leaving from
- **AWS:** EC2 Auto Scaling groups — the fleet ceiling is a per-region vCPU quota, raised by support ticket.
- **Google Cloud:** Managed instance groups — the instance template is immutable, so a shape change means a rolling replace.
- **Azure:** Virtual Machine Scale Sets — the platform fault domain count is fixed at creation and cannot be edited.

## Why this works
Fleet size is the quietest thing the bill decides. Three nodes are a quorum and nothing more: lose one and a third of the capacity goes with it. Sixteen and a dead machine costs six per cent, which is the difference between an incident and a note in the channel — and it is why a repatriation at this size is a far easier argument than the same one at a tenth of the bill. Buy enough usable capacity after control-plane reservations, storage overhead and a host failure; gross core count alone does not prove that the workloads fit.

For owned colocation, two spare machines are built, burned in and configured with the active fleet, then unplugged and shelved. Remote hands can put one into service while a failed machine goes through repair or return. The rented route reserves the same two machines as spare capacity in its eighteen-server quote; agree the provider's replacement response and how that capacity is brought into service before ordering.

## Before you start

**Access**
- The per-node sizing from Move 05 and the service inventory from Move 02
- Authority to commit the purchase or rental budget chosen in Move 03

**Software**
- A quote comparison sheet with three vendors or rental providers priced line by line

**People**
- A vendor or provider contact who will quote complete machines and support
- Whoever signs the purchase or rental commitment, with the chosen route agreed before ordering

## The runbook
1. Put the per-node sizing from Move 05 beside the inventory from Move 02. Reserve capacity for host services and one failed physical machine before placing guests or containers. The reference fleet uses sixteen active nodes; the two spares are additional replacement capacity. Recalculate the workload budget for the chosen platform.
2. Write the specification on one page: dual-socket, 32 physical cores, 256 GB of ECC memory with every channel populated, four 3.84 TB mixed-use NVMe drives plus a mirrored boot pair, redundant power supplies, two 25 GbE ports, and a controller speaking Redfish. For Proxmox hosts, require hardware virtualisation and verify IOMMU support if assigning devices to guests.
3. Send that page to three vendors for colocation, or three dedicated-host providers for rented metal. Record complete capacity, support and delivery terms in the quote comparison sheet. For a purchase, mark which components may be refurbished and quote new drives and power supplies; for rental, confirm support for the selected host operating system, virtualisation and remote management.
4. Include two identical spare nodes alongside the sixteen active ones. For owned colocation, burn them in with the fleet, then unplug and shelve them for remote hands. For rented metal, reserve two servers and document activation while the provider repairs a fault. Include all eighteen in the price; exclude spares from running capacity, quorum and storage replicas.
5. Confirm the route chosen in Move 03 against the hardware and facility quotes or the rental quote before making a binding commitment. For owned colocation, have the capital approver sign the hardware purchase order and record the ship date. For rented metal, order the quoted fleet under the agreed support and notice terms; the provider supplies the facility, so no hardware purchase or separate cage order is needed.

## Operator's notes
- **Swap:** Lease the eighteen machines over three years. The total is higher, but the monthly line resembles the cloud bill it replaces.
- **Do it faster:** Ask for a configuration the vendor stocks. Wanting 288 GB because the model said 240 turns a two-week delivery into an eight-week build.
- **Watch out:** Rails, power leads, 25 GbE optics and the support contract are quoted separately. A bill of materials listing only servers is short by thousands.
- **Leftovers:** A spare helps only if it stays current. Firmware, Proxmox and Talos versions drift. Update each spare on an isolated maintenance network, then return it to reserve; unplug owned spares. Enrol one in production only when replacing a failed host.

## Rollback
Before an order is accepted, both routes can be reversed by leaving the quote unsigned. The point of no return is the binding commitment: configured hardware may be non-returnable, while a rented fleet can carry minimum-term and notice charges. Check those terms before signing. An owned fleet can be resold at its then-current value; a rental ends under the provider's cancellation terms.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 4 weeks |

## What you can turn off
Nothing for months. The cloud instances and managed clusters carry production until Move 18 shifts the traffic; this Move commits the selected purchase or rental budget.
