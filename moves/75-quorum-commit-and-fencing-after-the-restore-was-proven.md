# 75 · Quorum commit and fencing, after the restore was proven

**Layer:** Data · **Leaving:** Managed multi-zone database failover · **Risk:** High · **Cutover:** 2 min · **Reversible:** Immediately

> Replaces the managed failover checkbox with quorum commit, and says plainly that only fencing gives safety.

## Leaving from
- **AWS:** RDS Multi-AZ — a checkbox that doubled the price and handled failover without ever telling you how.
- **Google Cloud:** Cloud SQL high availability — the same checkbox with the same opacity and the same doubling.
- **Azure:** Flexible Server zone-redundant high availability — the same again, with the zone mapping being per-subscription and therefore worth checking.

## Why this works
The managed checkbox did two different things and never distinguished them: it kept a second copy current, and it decided when to promote it. Quorum commit gives you the first — a write is not acknowledged until enough replicas hold it — and it is durability, not consensus. It cannot by itself stop a partitioned old primary from continuing to accept writes. That is what fencing does, and it is the part almost everyone omits, which is why it is named in this Move's title. This runs only after Move 74 has proven a restore, because building automatic failover before the recovery path works inverts the principle the previous Move exists to establish.

## Before you start

**Access**
- A proven restore from Move 74, timed and verified, because that is the gate on this Move
- The failure-domain labels from Move 42, so the replicas are placed across real racks

**Software**
- The operator's quorum configuration, written explicitly rather than left at a default
- A fencing mechanism configured and tested, not merely available

**People**
- Somebody from the on-call rota watching the deliberate failover, because this is the behaviour they will meet at night

## The runbook
1. Confirm Move 74's restore has been performed and timed. This is a gate: automatic failover in front of an unproven recovery path is a mechanism for turning one bad night into two.
2. Place the members across the failure domains labelled in Move 42. Three replicas on three machines that share a switch is one failure domain with extra replication traffic.
3. Configure quorum commit explicitly, naming how many replicas must acknowledge, and set the commit behaviour honestly. A configuration that acknowledges before any replica has the data is faster and is not what you think you bought.
4. Configure fencing and test it. Quorum commit is durability; fencing is what stops a partitioned old primary from accepting writes that will be lost. Without it, the configuration is safe against machine loss and unsafe against network partition, which is the more common failure.
5. Kill the primary deliberately, during business hours, with people watching. Measure the promotion time, watch the application reconnect, and confirm the old primary does not accept a single write after it is fenced.
6. Write down what the two minutes consist of — detection, promotion, reconnection — so that the number is understood rather than quoted.
7. Do not attempt quorum across sites. Move 24 already declined the second site, and Move 115 settles the recovery question against a measured rebuild time instead.

## Operator's notes
- **Swap:** Where two minutes of unavailability is genuinely unacceptable, the answer is connection-level retry and a queue in front, not a cleverer failover. Applications that survive a failover are applications that expected one.
- **Do it faster:** Test the failover on the second cluster first, several times, including the partition case. It is the only way to see the fencing work.
- **Watch out:** Synchronous replication to a replica that is slow makes every write slow. Quorum with more replicas than required is what stops one degraded machine from becoming a performance incident.
- **Leftovers:** The managed high-availability tier can be turned off on the source, halving that bill immediately, once Move 73 has cut over and the week has passed.

## Rollback
The configuration is reverted to a single primary in a minute, so this Move is reversible immediately, and the data is untouched because nothing here moves it. There is no point of no return, and if a promotion does go wrong the way back is the proven restore from Move 74 rather than anything in this Move. The real risk is the opposite: enabling automatic promotion without fencing, which is safe until the first partition and then loses writes. Keep the configuration and the failover drill results in source control, and re-run the drill after every upgrade in Move 108, because failover behaviour is exactly the kind of thing a minor version changes quietly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,090/mo | $0/mo | 100% | 2 min | 1 week | — |

## What you can turn off
The managed high-availability tier on the source instance, which is usually half its cost, once the cutover week from Move 73 has passed.
