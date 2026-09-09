# 09 · Racking day

**Layer:** Build · **Leaving:** The provider's serial console and boot diagnostics · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Prove remote console access to the whole batch, then shelve the spares. Rails, power and labels are the work; recovery from outside the building is the proof.

## Leaving from
- **AWS:** EC2 Serial Console — requires account access and a supported instance type; it exposes a serial port, not a controller that mounts your recovery ISO.
- **Google Cloud:** Compute Engine serial console — switched on by the `serial-port-enable` metadata key, and an organisation policy can forbid it estate-wide.
- **Azure:** Boot diagnostics and Serial Console — portal-created VMs default to managed boot diagnostics; interactive console access needs its own permissions and can be disabled subscription-wide.

## Why this works
The physical work is ordered so nothing has to be undone: rails across the active positions before a chassis is lifted, weight low, power split so one distribution unit cannot take the estate. None of that is the point. The Move exists for the baseboard management controller in each node — a small computer with its own processor, port and firmware, and the whole of the console the cloud gave you. Proved from outside the building, it turns two years of faults into an afternoon at a keyboard rather than a drive to the facility.

## Before you start

**Access**
- A booked day on site for two named people
- An out-of-band line that is live and independent of the uplinks

**Software**
- `ipmitool` and a Redfish client on a laptop outside the building
- A memory tester, a drive exerciser and one firmware bundle for the whole batch

**People**
- Two people for the lift; a chassis at head height is not a one-person job

## The runbook
1. Fit the active fleet's rail pairs before any chassis goes in, checked against the cabinet's depth. Rack bottom-up, heaviest low, two people on each lift. Test the spares temporarily; their permanent home is the shelf.
2. A-side power from one distribution unit, B-side from the other, so a node's supplies never share a strip. Verify each feed can carry the full rack load, then pull one feed per node and confirm it stays up.
3. Cable data in one colour and management in another, both ends labelled before anything is plugged in. Label the position, not the machine.
4. Give each controller a static address on the isolated management network, serial-over-LAN on, and a unique password stored outside the cluster. Disable unused shared-NIC access. Check power status through `ipmitool` and Redfish, recording which functions and licences each controller provides.
5. Leave the building. From a laptop elsewhere, over the out-of-band line, watch a node POST, enter firmware setup, mount an image over virtual media and power-cycle it. Until that works from outside, nothing here is built.
6. Run the memory tester and the drive exerciser overnight on all eighteen nodes, level them all to one firmware bundle, and before leaving site take front and rear photographs, the port map and a file naming each active rack position and each spare. Unplug and shelve the spares after acceptance; they remain outside every production cluster.

## Operator's notes
- **Swap:** Quote remote hands for racking and cabling to a drawing. Keep controller access and acceptance tests with your platform owner.
- **Do it faster:** Address and password the controllers on a bench the week before, so the day itself is cabling and testing.
- **Watch out:** Controllers can share a host NIC when configured that way. Prove guest and internet traffic cannot reach them, even during a host reboot.
- **Leftovers:** Cardboard, the spare's rail kit, and the temporary address scope that hands out addresses for months.

## Rollback
Nothing here carries data: a mistake is undone by unracking a machine the same afternoon. The point of no return is the day this cabinet takes production traffic, after which moving a cable is a change window. Firmware is the exception — a downgrade is sometimes refused, so record the shipped version per serial and keep the vendor's image so a working level can be restored.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 6 days | — |

## What you can turn off
Nothing yet. The active fleet draws power in one building while the whole cloud bill runs in another.
