# 18 · Go-live, and how you abort

**Layer:** Run · **Leaving:** Weighted DNS and the parallel managed edge · **Risk:** High · **Cutover:** 10 min · **Reversible:** 7 days

> The weight moves in four steps and comes back in one, which is why the time-to-live drops a day early and the old edge stays up a week.

## Leaving from
- **AWS:** Route 53 weighted records — a group weighted entirely to zero answers with every record in it, so drain by raising the survivor.
- **Google Cloud:** Cloud DNS routing policies — a policy cannot coexist with a plain record of the same name and type, so creating one replaces that set.
- **Azure:** Azure DNS and Traffic Manager — weighting lives in the profile, not the zone, so the apex needs an alias record and a second time-to-live.

## Why this works
Almost all of this Move is preparation, and the preparation is writing things down while nobody is under pressure. The mechanism is one field: a weight on a record, moved four times and movable back once. It is safe because the destination already carries real traffic and already holds the same rows as the source, so nothing is proved here for the first time. The time-to-live decides how long an abort takes, so it drops ahead of the day and is checked rather than assumed. Each soak spans a traffic cycle, because a filling connection table hides in a quiet minute.

## Before you start

**Access**
- Write access to the authoritative zone, and a second person who has it too
- The change window agreed with whoever answers the support line

**Software**
- `dig` run from two networks you do not control, and a resolver you have never used
- `argocd` sync windows, or another way to hold every deployment for the day

**People**
- One named decider, and the abort criteria they read out rather than argue

## The runbook
1. Lower the record's time-to-live to 60 in the authoritative zone a day ahead, then confirm it with `dig` on several resolvers, not the registrar's view.
2. Write the abort criteria as numbers: error rate above a figure, tail latency above a figure, any data-integrity report at all. Name the decider on it.
3. Tell the clients a record cannot move: mobile builds with a pinned host, batch jobs holding an old address, third parties allowlisting one.
4. Open the change window and freeze deploys with an `argocd` sync window over it. A release landing mid-shift cannot be told apart from the shift.
5. Move the weight to one per cent and soak. Then ten, then fifty, then all of it. The ten minutes in the strip is the last step, not the day.
6. Keep the managed edge configured, resolvable and billed at full weight for seven days. Nothing is deleted before the week is out, so the abort stays a field.

## Operator's notes
- **Swap:** Where a contract forbids a freeze, run the ramp in the customer's quiet hours in smaller increments across a fortnight.
- **Do it faster:** Take the one per cent step a week early, on its own. It finds the certificate and header faults while there is time to fix them.
- **Watch out:** Some corporate resolvers and mobile stacks ignore the time-to-live outright and reach the old address for days. Hence the week.
- **Leftovers:** The lowered time-to-live is itself a leftover, multiplying query volume and query billing on a zone nobody reads.

## Rollback
Putting the weight back returns new connections to the managed edge inside one time-to-live, which is why it was lowered first. That is the whole procedure for seven days. The point of no return is not the weight change but switching the managed edge off when the week is out. If the data failed rather than the traffic, no weight helps and the way back is the database restore.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,900/mo | $0/mo | 100% | 10 min | 3 days | 1 week |

## What you can turn off
The weighted record and the managed edge behind it, seven days after full weight, and with them the egress line that was most of the $1,900.
