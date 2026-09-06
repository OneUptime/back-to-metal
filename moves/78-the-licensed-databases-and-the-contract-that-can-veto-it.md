# 78 · The licensed databases, and the contract that can veto it

**Layer:** Data · **Leaving:** Managed licensed database engines · **Risk:** High · **Cutover:** 30 min · **Reversible:** No

> Prices core-based licensing, mobility rules and partitioning policy on hardware you own, because the contract can veto the migration before any data moves.

## Leaving from
- **AWS:** RDS for Oracle and RDS for SQL Server — licence-included or bring-your-own, with the cloud counting cores differently from the way your own hardware will be counted.
- **Google Cloud:** Cloud SQL for SQL Server and Bare Metal Solution for Oracle — the second existing precisely because the licensing made the first impossible.
- **Azure:** SQL Managed Instance and Oracle Database at Azure — again the licensing shaping the product rather than the technology.

## Why this works
The arithmetic here is not the one readers expect, and it can go either way. One major vendor's core factor table applies to hardware you own and does not apply in an authorised cloud, so the same silicon frequently needs half as many processor licences on your own metal. Against that, the same vendor recognises only a named list of partitioning technologies as hard, general-purpose virtualisation is not on it, and a small guest on a large uncapped host is licensed for the whole host. The other major vendor carries a per-processor core minimum and a reassignment rule that decides whether the hypervisor tier from Move 70 may move a guest at all. The technical work is the small half.

## Before you start

**Access**
- Your actual licence agreements, read rather than remembered, including any support-assurance terms
- The core counts and partitioning capability of the machines from Move 04

**Software**
- A licence position model for both the current estate and the target, side by side
- The technical path: a backup and restore, or a replica onto the hypervisor tier from Move 70

**People**
- Counsel and a licensing specialist, because a wrong position here is discovered in an audit rather than in a test

## The runbook
1. Model the licence position for the target before anything else. Core factor, per-processor minimums, and whether your partitioning approach is recognised. This is three of the four weeks and it is the part that decides whether the Move happens.
2. Check the mobility rule. One vendor restricts how often a licence may be reassigned between physical machines unless a support-assurance agreement is in place, and that rule governs whether live migration in Move 70 is permitted for these guests.
3. Get the position in writing from the vendor or a reseller with authority, on the specific configuration. A verbal reassurance about core factors is not a defence.
4. Pin the guests if the licensing requires it. Where general-purpose virtualisation is not recognised as hard partitioning, the guest is licensed against the whole host, and the answer is a dedicated host with a matching core count rather than a clever configuration.
5. Do the technical work: a backup and restore, or an availability replica onto the hypervisor tier from Move 70, plus Windows nodes for the workloads that stay on Windows. Thirty minutes of cutover per database and it is the easy part.
6. Run the Move 72 gate in whatever form the engine supports, and keep the source available until the licence position has survived one audit cycle.
7. Accept the honest outcome. Sometimes this estate does not move, and that conclusion, written down with its arithmetic, is a successful result for this Move.

## Operator's notes
- **Swap:** Where the licence makes ownership impossible, one provider sells dedicated hardware in its own facility specifically for this engine. It is not repatriation and it is frequently the right answer.
- **Do it faster:** Model the licence position before doing any technical work at all. It takes a fortnight and it can end the Move before anyone builds anything.
- **Watch out:** Licence terms change between contract versions. A position that was true at your last renewal may not hold for a new deployment, and the vendor's audit team reads the current terms.
- **Leftovers:** Licence-included managed instances stop charging when deleted; bring-your-own licences you have already bought may or may not transfer, and that is worth more than the hardware.

## Rollback
This Move is irreversible in the way that matters: a licence position taken on your own hardware cannot be undone by moving back, because the migration itself may have triggered a reassignment the agreement counts. There is no way back from a licence audit. The point of no return is the day the workload starts on your hardware under your own licences. Keep the source database and its backups so the data can be restored, and keep the written licence position permanently, because it is the evidence.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $9,400/mo | $4,100/mo | 56% | 30 min | 4 weeks | 4 weeks |

## What you can turn off
The managed licensed instances, once the licence position is confirmed in writing and the data has been verified on the far side.
