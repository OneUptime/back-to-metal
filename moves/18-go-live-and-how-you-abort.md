# 18 · Go-live, and how you abort

**Layer:** Run · **Leaving:** Weighted DNS and the parallel managed edge · **Risk:** High · **Cutover:** 10 min · **Reversible:** 7 days

> The weight moves in four steps and comes back in one, which is why the time-to-live drops a day early and the old edge stays up a week.

## Leaving from
- **AWS:** Route 53 weighted records — a group weighted entirely to zero answers with every record in it, so drain by raising the survivor.
- **Google Cloud:** Cloud DNS routing policies — a policy cannot coexist with a plain record of the same name and type, so creating one replaces that set.
- **Azure:** Azure DNS and Traffic Manager — weighting lives in the profile, not the zone, so the apex needs an alias record and a second time-to-live.

## Why this works
The edge ramp changes where requests enter; it must not choose between competing copies of writable data. Stateless services already passed Move 14, and the reference database moved in Move 16. Both edges must reach the same authoritative workload and data before their weights can be interchangeable. Lower the time-to-live ahead of the day, check actual client behaviour, and let each soak span a traffic cycle.

Stateful VMs deferred from Move 14 need a separate service window before this edge ramp. Seed their data, rehearse the final transfer and time the return path. The strip's ten minutes covers the reference edge change only. Record each VM's measured downtime separately; if a write stop exceeds an hour, split the migration by independently movable workload or retain that VM until a shorter method is proved. An image export does not acquire a zero-downtime guarantee by appearing earlier in the book.

## Before you start

**Access**
- Write access to the authoritative zone, and a second person who has it too
- The change window agreed with whoever answers the support line
- For a stateful VM, a restored backup and a tested transfer and reverse-transfer plan approved by its data owner

**Software**
- `dig` run from two networks you do not control, and a resolver you have never used
- `argocd` sync windows for Kubernetes, or the VM pipeline's deployment hold
- The application-native replication or backup tooling already tested for each stateful VM

**People**
- One named decider, and the abort criteria they read out rather than argue

## The runbook
1. Lower the record's time-to-live to 60 in the authoritative zone a day ahead, then confirm it with `dig` on several resolvers, not the registrar's view.
2. Write the abort criteria as numbers: error rate above a figure, tail latency above a figure, any data-integrity report at all. Name the decider on it.
3. Tell the clients a record cannot move: mobile builds with a pinned host, batch jobs holding an old address, third parties allowlisting one.
4. For each deferred stateful VM, seed a destination guest while the source remains authoritative, using its tested application-native replication or backup tooling. Restore into isolation, verify record counts or file checksums, and rehearse final transfer and reverse transfer. Book its measured write-stop window separately from the edge change.
5. In that VM's window, stop all source writers and timers; keep destination writers stopped too. Drain replication or transfer the final delta, validate the data, then switch traffic and start only destination writers. Retain the source stopped. If verification misses the deadline before destination writes, abandon the cutover and resume the source. Never split live writes between independent VM disks.
6. Before the edge ramp, verify both edges route to that same authoritative service and data. Keep destination backups running. If the old edge cannot reach the new authority, it is not an available traffic-only rollback; repair that path or retain the existing edge until it can.
7. Open the edge window and freeze releases with an `argocd` sync window or the VM pipeline's deployment hold. A release landing mid-shift cannot be told apart from the shift.
8. Move the weight to one per cent and soak. Then ten, then fifty, then all of it. Confirm actual traffic, errors and latency after each change. The ten minutes in the strip is the final reference step, not the earlier VM windows or the soak.
9. Keep the managed edge configured, resolvable and at zero traffic weight for seven days, with the new edge's weight positive. Verify the return route during the week. Nothing is deleted before that check passes.

## Operator's notes
- **Swap:** Where a contract forbids a freeze, run the ramp in the customer's quiet hours in smaller increments across a fortnight.
- **Do it faster:** Take the one per cent step a week early, on its own. It finds the certificate and header faults while there is time to fix them.
- **Watch out:** Some corporate resolvers and mobile stacks ignore the time-to-live outright and reach the old address for days. Hence the week.
- **Leftovers:** The lowered time-to-live is itself a leftover, multiplying query volume and query billing on a zone nobody reads.

## Rollback
For an edge failure, restore the old edge's traffic weight and confirm requests reach the same authoritative service; cached clients may take longer than one TTL. For a stateful VM, the point of no return for a quick switch back is its first destination write. Stop writers, reverse-transfer those changes or restore and replay them to the source, validate the recovered data, then restart source writers and change traffic. Never boot a stale source as a writable fallback. The managed edge stays available for seven days, but its existence cannot replace that data recovery procedure.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $8,900/mo | $0/mo | 100% | 10 min | 3 days | 1 week |

## What you can turn off
The weighted record and the managed edge behind it, seven days after full weight, and with them the egress line that was most of the $8,900.
