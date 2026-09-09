# 06 · Sixteen machines, and the two on the shelf

**Layer:** Buy · **Leaving:** Elastic node capacity and cluster autoscaling · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Sixteen nodes, so losing one costs six per cent and not a third. Two are bought with them and never plugged in, because iron does not autoscale

## Leaving from
- **AWS:** EC2 Auto Scaling groups — the fleet ceiling is a per-region vCPU quota, raised by support ticket.
- **Google Cloud:** Managed instance groups — the instance template is immutable, so a shape change means a rolling replace.
- **Azure:** Virtual Machine Scale Sets — the platform fault domain count is fixed at creation and cannot be edited.

## Why this works
Fleet size is the quietest thing the bill decides. Three nodes are a quorum and nothing more: lose one and a third of the capacity goes with it. Sixteen and a dead machine costs six per cent, which is the difference between an incident and a note in the channel — and it is why a repatriation at this size is a far easier argument than the same one at a tenth of the bill. Buy the headroom the arithmetic already bought you: 512 cores against the four hundred or so the estate actually needs.

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
1. Put the per-node sizing from Move 05 beside the service inventory from Move 02 and divide by what a node holds, leaving capacity for an active node to fail. The reference estate uses sixteen active nodes; the two spare machines are additional replacement capacity.
2. Write the specification on one page: dual-socket, 32 physical cores, 256 GB of ECC memory with every channel populated, four 3.84 TB mixed-use NVMe drives plus a mirrored boot pair, redundant power supplies, two 25 GbE ports, and a controller speaking Redfish.
3. Send that page to three vendors for colocation, or three dedicated-host providers for rented metal. Record complete capacity, support and delivery terms in the quote comparison sheet. For a purchase, mark which components may be refurbished and quote new drives and power supplies; for rental, confirm that the provider supports your operating-system image and remote management.
4. Include two identical spare nodes alongside the sixteen active ones. On the owned route, burn them in with the fleet and leave them on the shelf for remote hands. On the rented route, reserve two servers for replacement capacity and document how the team activates them while the provider repairs a fault. Keep all eighteen machines in the cost comparison.
5. Confirm the route chosen in Move 03 against the hardware and facility quotes or the rental quote before making a binding commitment. For owned colocation, have the capital approver sign the hardware purchase order and record the ship date. For rented metal, order the quoted fleet under the agreed support and notice terms; the provider supplies the facility, so no hardware purchase or separate cage order is needed.

## Operator's notes
- **Swap:** Lease the eighteen machines over three years. The total is higher, but the monthly line resembles the cloud bill it replaces.
- **Do it faster:** Ask for a configuration the vendor stocks. Wanting 288 GB because the model said 240 turns a two-week delivery into an eight-week build.
- **Watch out:** Rails, power leads, 25 GbE optics and the support contract are quoted separately. A bill of materials listing only servers is short by thousands.
- **Leftovers:** A spare helps only if it stays current. Firmware and the Talos version drift within a quarter, so the shelf machine boots and updates with the rest.

## Rollback
Before an order is accepted, both routes can be reversed by leaving the quote unsigned. The point of no return is the binding commitment: configured hardware may be non-returnable, while a rented fleet can carry minimum-term and notice charges. Check those terms before signing. An owned fleet can be resold at its then-current value; a rental ends under the provider's cancellation terms.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 4 weeks |

## What you can turn off
Nothing for months. The EC2 Auto Scaling groups carry production until Move 18 shifts the traffic; this Move commits the selected purchase or rental budget.
