# 08 · The way in when the machine will not boot

**Layer:** Iron · **Leaving:** The provider's serial console and boot diagnostics · **Risk:** High · **Cutover:** 0 min · **Reversible:** Until the order is signed

> Treats the management controller as a purchase-order line, tests Redfish on a loan unit, and finds which console features sit behind a licence before delivery.

## Leaving from
- **AWS:** EC2 Serial Console and EC2 Instance Connect — a console you could reach from an API call, with no licence, no firmware and no cable.
- **Google Cloud:** Compute Engine interactive serial console — the same idea, enabled per project or per instance, and free.
- **Azure:** Serial console and boot diagnostics — boot screenshots included, which is the feature people miss most when it stops existing.

## Why this works
Every cloud gave you a way to watch a machine boot and to type at it when the network was not working. That was a product feature, and on your own hardware it is a baseboard management controller: a small computer inside the server with its own processor, its own network port and its own firmware. It is the difference between diagnosing a failed boot from your desk and driving to a building at three in the morning. It is also, on every major vendor, partly behind a licence — and the moment to discover that is before delivery, when it is a line item, rather than after, when it is an emergency purchase at list price.

## Before you start

**Access**
- A loan or evaluation unit of the exact chassis chosen in Move 07, with a management port you can reach
- The vendor's licence matrix for that generation, in writing rather than from a forum post

**Software**
- A Redfish client, or `curl` and the specification, to test the API rather than the web interface
- `ipmitool` for the operations the vendor has not yet moved to Redfish, which is still several of them

**People**
- Whoever writes the purchase order, so the licence lands on it rather than on next quarter's budget

## The runbook
1. Establish which console features are licensed on the exact model quoted. Remote console and virtual media sit behind iDRAC Enterprise on Dell, behind iLO Advanced on HPE, and behind the DCMS key on Supermicro, and the naming changes between generations.
2. Test Redfish against the loan unit rather than the datasheet. Ask it for the system inventory, the power state, the boot source override, the event log and a firmware version, and confirm each returns what the specification says it should. Vendors claim conformance and implement subsets.
3. Test the operations you will actually need under pressure: power cycle, boot to a one-time source, mount an image over virtual media, and read the log after a forced reset. Do them over the network from a laptop, which is how you will do them for real.
4. Confirm that `ipmitool` still works for anything Redfish does not cover, and record which is which. Running both is normal; pretending one is enough is how a runbook stops halfway through.
5. Record the firmware support horizon: how long this controller will receive updates, how those updates are delivered, and whether an update requires a host reboot. That horizon is the number that actually dates the platform, more than the processor does.
6. Put the licence, at the correct part number, on the purchase order for every machine, including the spare. A controller licence bought under pressure costs more and arrives slower than one bought with the server.

## Operator's notes
- **Swap:** Where the vendor's licence is priced absurdly, a serial console server reaching every machine's serial port covers the same ground for boot diagnosis, though not for virtual media. Move 16 buys that hardware anyway.
- **Do it faster:** Ask the vendor for a temporary licence key on the loan unit. Most will issue one for thirty days and it turns this Move from a negotiation into a test.
- **Watch out:** Management controllers are a security boundary and a well-known target. They belong on their own network, they do not belong on the internet, and their default credentials belong changed before the machine leaves the loading bay.
- **Leftovers:** Some vendors bind licences to a service tag. A machine returned under warranty can come back with a controller that has forgotten it was licensed, and re-issuing the key is a support case rather than a click.

## Rollback
Until the order is signed, a controller decision is reversed by editing the quote. After that, adding a licence to twenty machines is a purchase at list price and a per-machine application step, which is annoying rather than fatal. The point of no return is the purchase order in Move 20. Keep every key, its service tag and the vendor's licence matrix in the same place as the bill of materials, so entitlement can be restored quickly when a controller is replaced and arrives blank.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. This is the Move that stops Part II being carried out by driving to a building.
