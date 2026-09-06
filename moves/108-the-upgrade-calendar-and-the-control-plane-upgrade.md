# 108 · The upgrade calendar and the control-plane upgrade

**Layer:** Watch · **Leaving:** Managed control-plane upgrades, purchasable extended support for end-of-life Kubernetes minors, and a managed add-on lifecycle · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Upstream maintains a minor for about fourteen months and the extra year sold by the hour is gone, so the treadmill becomes a dated calendar with a named owner.

## Leaving from
- **AWS:** EKS extended support — a year beyond upstream, billed at a higher hourly rate, which is the option that disappears here.
- **Google Cloud:** GKE release channels with extended support — the same idea sold as a channel rather than as a surcharge.
- **Azure:** AKS long-term support — the same again, with its own eligibility rules and its own end dates.

## Why this works
Upstream maintains a minor release for roughly fourteen months, and the extra year every provider sold you by the hour does not exist on your own cluster. That is not a crisis; it is a calendar. What replaces the managed lifecycle is a written schedule with a named owner, a rehearsal on the second cluster before every step, and — the larger half — an ownership matrix for the forty-odd charts, operators and drivers that each move on their own cadence. On this host operating system the image and the Kubernetes version move on separate commands, which is a feature: two smaller changes rather than one large one.

## Before you start

**Access**
- The second cluster from Move 51, matching production's versions, for every rehearsal
- A verified snapshot from Move 52's procedure before each step, not merely a scheduled one

**Software**
- A written calendar with dates and a named owner, published where the team will see it
- The ownership matrix: every chart, operator and driver, its current version, its cadence and its owner

**People**
- One named owner for the calendar, because a shared responsibility for upgrades is nobody's

## The runbook
1. Write the calendar first, with real dates derived from upstream's support window rather than from when it feels convenient. Publish it and name its owner.
2. Build the ownership matrix. Forty-odd components on independent cadences is normal and it is the part that actually consumes time; without the matrix, an upgrade stalls on a chart nobody knows the owner of.
3. Take and verify a snapshot before every step, using the procedure proved in Move 52. Verified means restored somewhere, not merely written.
4. State the version skew rules per component and check them before each step. The control plane, the kubelets and the client tools have separate tolerances and exceeding one produces failures that do not name the cause.
5. Check for removed APIs and for your own admission webhooks. A webhook configured to fail closed during a control-plane upgrade can block the upgrade itself, and that is a memorable afternoon.
6. Upgrade sequentially, never skipping a minor, rehearsing each step on the second cluster first. On this host operating system the image and the Kubernetes version are separate commands, so take them separately.
7. Record how long each step took, because that number is the input to next quarter's calendar.

## Operator's notes
- **Swap:** Where the estate genuinely cannot upgrade on schedule, a support subscription from Move 112 buys advice rather than time. Nothing buys back an unmaintained minor.
- **Do it faster:** Upgrade the second cluster a fortnight ahead of production, always. It converts an upgrade into a rehearsal that has already been performed.
- **Watch out:** Add-ons that were managed for you are now yours, and they have their own end-of-support dates that do not align with the cluster's. The matrix is what stops that being a surprise.
- **Leftovers:** Extended support surcharges on the old cluster stop when it does, and until then they are a real and growing line.

## Rollback
A control-plane upgrade is not reversible: there is no way back from a completed minor upgrade except restoring the snapshot taken before it, which loses everything written since. The point of no return is the first control-plane component upgraded. That is why the snapshot is verified rather than assumed and why every step is rehearsed on the second cluster first. Restoring is a real procedure from Move 52 with a measured time, not a theoretical option.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $210/mo | $0/mo | 100% | 0 min | 1 week | — |

## What you can turn off
Extended support surcharges on the old cluster, once it is gone. On your own cluster there is nothing to buy and nothing to cancel.
