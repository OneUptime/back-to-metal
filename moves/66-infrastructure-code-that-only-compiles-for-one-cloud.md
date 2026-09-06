# 66 · Infrastructure code that only compiles for one cloud

**Layer:** Platform · **Leaving:** Provider-native stack templates, their programming-language synthesisers and the serverless application frameworks built on them · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Provider-native templates have no target off the cloud that defines them, so the estate they describe is re-expressed once rather than translated stack by stack.

## Leaving from
- **AWS:** CloudFormation with the Cloud Development Kit — the hardest of the three, because the source is a program rather than a document, and the serverless framework sits on top of it.
- **Google Cloud:** Deployment Manager — already past end of support and scheduled for turndown, with Config Connector and a managed service as successors, so this reader is moving regardless.
- **Azure:** ARM templates with Bicep — a template language with a friendlier front end, which makes the source at least readable as a description.

## Why this works
A provider-native template has no target other than the cloud that defines it. There is no compiler flag that emits your cluster. So the honest approach is to re-express the estate once rather than to translate stack by stack, and the split is clean: identity, networking and buckets — the shrinking cloud footprint that stays — are described in the tool chosen in Move 65, while everything describing compute becomes Kubernetes manifests under that same reconciler and is not translated at all. The synthesiser estates are the harder half, because their higher-level constructs have no equivalent to compile into, and this Move decides how much of the function estate in Move 89 can move at all.

## Before you start

**Access**
- Every template, stack and synthesiser project in the estate, listed rather than remembered
- The state backend and repository from Move 65, ready to receive what survives

**Software**
- A stack-by-stack inventory marked as stays, moves to manifests, or is deleted
- The successor tooling for any provider whose native service is being retired underneath you

**People**
- The author of each synthesiser project, because reading somebody else's generated infrastructure is slower than rewriting it

## The runbook
1. Inventory every stack and mark each one. Stays in the cloud, becomes a Kubernetes manifest, or is deleted because nothing has used it in two years. The third category is usually larger than expected.
2. Re-express what stays — identity, networking, buckets — in the tool chosen in Move 65, against the shrinking cloud footprint. This is ordinary work and it goes quickly.
3. Do not translate the compute stacks. A description of an instance group has no meaning here; the workload is described as a manifest and the stack is deleted. Attempting a translation produces something that resembles the old estate and works like neither.
4. Take the synthesiser estates one project at a time, and read what they actually create rather than what they appear to say. A single high-level construct can create a dozen resources, several of which nobody knows about.
5. Where a provider's own template service is being retired, move to its successor only if you are staying on that cloud for that resource. Otherwise move straight to the target and skip the intermediate step entirely.
6. Record which parts of the function estate cannot move because their infrastructure only exists as a synthesiser construct. Move 89 needs that list, and this is the Move that produces it.
7. Delete each old stack only after its resources are managed elsewhere, and confirm the deletion does not remove anything still in use, which is the failure mode that ends this Move badly.

## Operator's notes
- **Swap:** Where a stack describes something genuinely staying on the cloud forever, leave it alone. Rewriting working infrastructure code for its own sake is the least valuable month available.
- **Do it faster:** Start with the stacks that only create identity and networking. They convert almost mechanically and they unblock everything else.
- **Watch out:** Deleting a stack can delete the resources it created, including buckets with data in them. Set the retention behaviour deliberately on every resource before removing any stack.
- **Leftovers:** Orphaned resources left behind by half-deleted stacks are extremely common and Move 120 will find them in the billing data.

## Rollback
Nothing is destroyed while the estate is being re-expressed, because the new description and the old stack can both exist against the same resources for a while. There is no point of no return until a stack is deleted. Keep the original templates in source control after they stop being used, so the previous definition can be restored and compared when a resource turns out to have had a setting nobody carried across.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 4 weeks | — |

## What you can turn off
Old stacks, once their resources are managed elsewhere — and the orphaned resources they left behind, once Move 120 has found them.
