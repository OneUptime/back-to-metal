# 64 · Builds onto your own metal

**Layer:** Platform · **Leaving:** Managed CI build services, their hosted runner pools and self-managed runner autoscaling groups · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> The control plane stays with the forge and only execution moves to ephemeral runners on your nodes, so one label change routes every build back if it goes wrong.

## Leaving from
- **AWS:** CodeBuild — billed per build minute, with private pools already able to run inside your network, so this is close to a pool swap.
- **Google Cloud:** Cloud Build — a free allowance of concurrent builds that a self-hosted pool has to beat on latency rather than on price.
- **Azure:** Azure Pipelines — build stages and deploy stages tangled in one pipeline object, so here and only here this Move and Move 65 are cut together.

## Why this works
Only execution moves. The forge that holds the code, the pull requests and the pipeline definitions stays exactly where it is, and what changes is where the work runs: ephemeral runners on your own machines, registered to a pool, torn down after each job. That split is what makes this Move safe, because the way back is changing one label on a job definition. It is also where the endurance arithmetic from Move 09 gets tested for real, since a build fleet writes more, harder, than anything else in the estate, and a cheap device in a build node will wear out inside a year.

## Before you start

**Access**
- The forge's runner registration flow, and permission to register a self-hosted pool
- The object store from Move 49 for the shared build cache

**Software**
- An ephemeral runner controller at a pinned chart version, so a job never runs on a dirty machine
- A build cache backend on the object store, and a warm layer cache measured before and after

**People**
- Whoever owns the pipeline, because build latency is the thing developers will notice within a day

## The runbook
1. Install the ephemeral runner controller at a pinned version and register one pool. Ephemeral is the requirement rather than the preference: a runner that survives a job carries state into the next one, and that is how a build passes on a machine and fails everywhere else.
2. Measure build wall-clock time before and after, with the cache cold and warm. The managed service had a warm cache you did not have to think about, and reproducing it is most of the value of this Move.
3. Put the layer cache and the package cache on the object store from Move 49, and confirm cache hits rather than assuming them. A cache that is being written and never read is a cost with no benefit.
4. Do the endurance arithmetic against the device class from Move 09. Builds are the hardest write workload you will run, and a build fleet on the wrong drive class is a replacement programme in month nine.
5. Rebuild the isolation the managed builder was quietly selling: rootless building, dedicated and tainted nodes so a build cannot land beside production, and a separate cache namespace per tenant.
6. Route a fraction of jobs to the new pool by label, run both for a week, and compare failure rates as well as times. A pool that is faster and flakier is not faster.
7. Leave the hosted macOS runners bought. There is no answer to them on your own hardware that is worth the trouble.

## Operator's notes
- **Swap:** Where builds are infrequent, keeping them hosted is entirely defensible. This Move earns its place on estates where build minutes are a real line on the invoice.
- **Do it faster:** Move the slowest, most cache-dependent pipeline first. It shows the biggest improvement and it exercises the cache design hardest.
- **Watch out:** Build nodes tainted for builds will still attract system daemons and log shippers. Account for that overhead or the machines will be slower than the arithmetic promised.
- **Leftovers:** The managed build service keeps billing per minute until the last job moves, and the hosted parallel job allowance disappears rather than being refunded.

## Rollback
Changing one label on a job definition sends every build back to the hosted pool, which is why this Move is reversible immediately and why it is safe to try on a Tuesday. There is no point of no return. Keep the pipeline definitions and the runner configuration in source control so a working pool can be restored, and keep the cache buckets until a full week has passed with no fallback, because a cold cache on a rollback is a very slow morning.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,940/mo | $180/mo | 91% | 0 min | 2 weeks | — |

## What you can turn off
The managed build service and its hosted pools, once a week of parallel running shows the same failure rate and better wall-clock times.
