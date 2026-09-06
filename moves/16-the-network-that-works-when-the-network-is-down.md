# 16 · The network that works when the network is down

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Buys the out-of-band estate as hardware in its own right, on its own uplink and power, because the management controller rides the network you are fixing.

## Leaving from
- **AWS:** EC2 Instance Connect Endpoint — a control path that reached an instance without touching your own network at all.
- **Google Cloud:** Identity-Aware Proxy TCP forwarding — the same property, reached through the provider's front door rather than yours.
- **Azure:** Azure Bastion — a managed jump host that stayed reachable when everything you had built was not.

## Why this works
Every cloud gave you a control path that did not depend on your network working. On your own hardware that path has to be bought, and it is the cheapest line on the bill of materials and the one most often struck out on the grounds that the management controller from Move 08 covers it. It does not. The controller is reached over a network, and the fault you most need it for is the production switch pair itself. What is needed is a small management switch, a serial console server with ports for every switch and enough machines to matter, and an uplink and power that do not traverse the production fabric.

## Before you start

**Access**
- The switch and machine counts from Moves 11 and 13, to size the port count
- The facility's position on a second uplink, which is a Part II conversation you can start now

**Software**
- A console server that speaks SSH and logs sessions, not one that needs a Java applet
- A cellular or fixed uplink option priced, even if the decision is deferred

**People**
- Whoever will be woken up, since this is the equipment that decides whether they can help from home

## The runbook
1. Count the serial ports you need: every switch, every power distribution unit that has one, and enough machines that a console is available where the management controller is not. Add a quarter for growth and buy the next size up.
2. Buy a management switch that is not part of the production fabric, and a console server that logs every session to somewhere off the device. The log is what tells you what the last person did at three in the morning.
3. Give the out-of-band estate its own uplink. A small business broadband line or a cellular router is enough, and its whole purpose is that it does not share a fate with the transit you buy in Part VI.
4. Give it its own power. A separate small uninterruptible supply for the management switch and console server, so that the thing you use to diagnose a power fault is not on the circuit that failed.
5. Price the whole set. It is normally under two per cent of the hardware bill, and stating that percentage is usually enough to keep it on the purchase order.
6. Record what this equipment is for, in one paragraph, on the bill of materials. Six months later somebody will ask why there is a second switch, and the paragraph is what the engineer woken at three in the morning will be glad of.

## Operator's notes
- **Swap:** Where the facility offers a managed out-of-band service with its own uplink, taking it is reasonable and cheaper than building one. Read what it depends on before believing it is independent.
- **Do it faster:** Buy the console server with more ports than you need. Adding a second one later means a second address, a second credential set and a second thing to forget.
- **Watch out:** An out-of-band network that reaches the internet directly is an out-of-band network that will be scanned. It gets its own firewall and its own authentication in Move 40, and it is never left open in the meantime.
- **Leftovers:** The cloud bastion and instance-connect endpoints keep billing quietly. They stay until Part VII, because they are how you reach the old estate while it still matters.

## Rollback
Nothing here is committed to anything: the equipment is small, cheap and independent, and taking it out is unplugging it. The point of no return does not exist in this Move, which is why leaving it out is such a common and such an expensive decision — the cost of including it is small and known, and the cost of omitting it is a drive to a building. Keep the console server configuration exported so it can be restored onto a replacement unit without rebuilding the port map by hand.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing yet. The provider's bastion and console endpoints are still the way into the old estate.
