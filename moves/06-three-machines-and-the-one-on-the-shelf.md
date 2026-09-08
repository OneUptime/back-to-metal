# 06 · Three machines, and the one on the shelf

**Layer:** Buy · **Leaving:** Elastic node capacity and cluster autoscaling · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Three nodes are a quorum, and losing one costs a third of the capacity. The fourth is bought with them and never plugged in, because iron does not autoscale

## Leaving from
- **AWS:** EC2 Auto Scaling groups — the fleet ceiling is a per-region vCPU quota, raised by support ticket.
- **Google Cloud:** Managed instance groups — the instance template is immutable, so a shape change means a rolling replace.
- **Azure:** Virtual Machine Scale Sets — the platform fault domain count is fixed at creation and cannot be edited.

## Why this works
Three is the smallest fleet that is a cluster at all, and at this size the book is honest that it is the floor rather than the comfortable answer. Three nodes give a control plane its quorum; lose one and a third of the capacity goes with it, and the two survivors carry a load you have to have sized them for deliberately. That is the trade a $10,000 estate makes: at twice the bill you buy five and a dead machine costs twenty per cent instead of thirty-three. Size the workload so two can hold it, or accept that a failure is a degraded afternoon rather than a shrug.

The fourth machine is what makes that survivable, and it is not in the rack. It is built, burned in, configured identically and then unplugged, because the replacement path you left behind was an API call and the one ahead is a return authorisation and three weeks. Those weeks cost more than the machine that prevents them, and at three nodes they cost more again.

## Before you start

**Access**
- The per-node sizing from Move 05 and the service inventory from Move 02
- Authority to raise a purchase order in the tens of thousands

**Software**
- A quote comparison sheet with three vendors priced line by line

**People**
- A vendor account manager who will price a configured node, not a parts list
- Whoever signs capital expenditure, warned four weeks ahead

## The runbook
1. Put the per-node sizing from Move 05 beside the service inventory from Move 02, add one whole machine of failure headroom, and divide by what a node holds. The reference estate lands on five.
2. Write the specification on one page: dual-socket, 32 physical cores, 256 GB of ECC memory with every channel populated, four 3.84 TB mixed-use NVMe drives plus a mirrored boot pair, redundant power supplies, two 25 GbE ports, and a controller speaking Redfish.
3. Send that page to three vendors, marking line by line what may be refurbished: chassis and processors two generations old run Kubernetes as well as new ones at half the price, while drives and power supplies wear and are bought new. Take each quote into the comparison sheet, ship date beside price.
4. Add the sixth node, identical to the other five: burned in with the rest, then pulled and shelved. It is the only capacity on site that does not arrive by courier.
5. Raise the purchase order, have the person who signs capital expenditure sign it, and put the ship date in the calendar. Moves 07 and 08 run against that date.

## Operator's notes
- **Swap:** Lease the six machines over three years. The total is higher, but the monthly line resembles the cloud bill it replaces.
- **Do it faster:** Ask for a configuration the vendor stocks. Wanting 288 GB because the model said 240 turns a two-week delivery into an eight-week build.
- **Watch out:** Rails, power leads, 25 GbE optics and the support contract are quoted separately. A bill of materials listing only servers is short by thousands.
- **Leftovers:** A spare helps only if it stays current. Firmware and the Talos version drift within a quarter, so the shelf machine boots and updates with the rest.

## Rollback
Everything before the purchase order is a document, and an unaccepted quote expires harmlessly. The point of no return is the signature: configured servers are built to order and rarely returnable. Afterwards they still hold about half their value second-hand.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 days | 4 weeks |

## What you can turn off
Nothing for months. The EC2 Auto Scaling groups carry production until Move 18 shifts the traffic; this Move only commits money.
