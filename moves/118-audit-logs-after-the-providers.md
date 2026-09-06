# 118 · Audit logs after the provider's

**Layer:** Watch · **Leaving:** The provider's control-plane audit trail, its configuration-compliance rules and its posture-management service · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Writes the audit policy by hand and ships it to an append-only store in another credential domain, because Kubernetes audit logging is off by default.

## Leaving from
- **AWS:** CloudTrail with Config and Security Hub — the management-event trail could not be switched off and was retained for you.
- **Google Cloud:** Cloud Audit Logs with Security Command Center — admin activity logs retained without charge, and the rest a resource you paid for.
- **Azure:** Activity Log with Policy and Defender for Cloud — the same split again, with its own retention defaults.

## Why this works
Two of the three providers retained a control-plane audit trail whether or not you asked, which means most readers have never had to think about audit logging existing. On your own cluster it is off by default, the policy is written by hand, and each level of detail has a storage cost you are choosing. It also has a structural weakness the provider's did not: the log is written by the thing being audited. That is why the destination is an append-only store in a separate credential domain, and why the preventive and detective controls from Moves 59 and 65 matter alongside it.

## Before you start

**Access**
- A destination in a separate credential domain, under immutability, that the cluster cannot delete from
- The reconciler from Move 65, because drift detection against the repository is half the control

**Software**
- A hand-written audit policy, with each level's storage cost estimated before it is enabled
- Scheduled benchmark runs against the cluster, so configuration compliance is measured rather than assumed

**People**
- Whoever will answer the auditor in Move 119, so the evidence collected is the evidence they need

## The runbook
1. Write the audit policy by hand, rule by rule. Full request and response bodies for sensitive resources, metadata only for the noisy ones, and nothing at all for the health checks that would otherwise dominate the volume.
2. Estimate the storage before enabling it. Audit logging at a high level on a busy cluster produces a surprising volume, and the estimate is what stops the first month's bill being the reason it gets turned off.
3. Ship it to an append-only store in a separate credential domain, under immutability. The cluster writes the log about itself, so the destination has to be somewhere the cluster's own identity cannot delete from.
4. Set retention deliberately and budget it. Retention that nobody chose is retention that either costs too much or is too short when it is asked for.
5. Rebuild the continuous control monitoring the provider's configuration service was doing: scheduled benchmark runs against the cluster and its nodes, on a schedule, with the results stored.
6. Name the two halves of control explicitly. The admission policy from Move 59 is the preventive control; drift detection against the repository from Move 65 is the detective one. An auditor will ask which is which.
7. Test the trail by doing something notable and finding it in the store afterwards, from the auditor's side rather than from the cluster's.

## Operator's notes
- **Swap:** Where the volume is genuinely unaffordable, log metadata for everything and bodies only for secret and role changes. That covers most of what is ever asked for.
- **Do it faster:** Start from the upstream example policy and prune. Writing one from nothing takes a day and produces the same result.
- **Watch out:** An audit log that is never read is not a control. Sample it monthly, and put one query in front of a human, or the first time anybody looks at it will be during an incident.
- **Leftovers:** The provider's trail, configuration rules and posture service bill per event and per rule evaluation, and the trail in particular keeps billing after everything else has gone.

## Rollback
The policy is reverted through the machine configuration and the shipping is stopped by removing it, so this is reversible in minutes. There is no point of no return. What cannot be recovered is a period during which auditing was off, which is why it is enabled early rather than before an audit. Keep the policy in source control so the exact configuration in force at any past date can be restored and evidenced.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $940/mo | $90/mo | 90% | 0 min | 1 week | — |

## What you can turn off
The provider's configuration rules and posture service once your own benchmarks are running. The trail itself goes with the account in Move 122.
