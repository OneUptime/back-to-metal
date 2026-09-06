# 68 · The container service that was not Kubernetes

**Layer:** Platform · **Leaving:** Managed container runtimes that are not Kubernetes: task-definition services, request-billed serverless containers and their built-in service discovery · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> A task definition is not a Deployment, so the sidecar model, the exec path, the per-task network interface and scale-to-zero billing are each converted separately.

## Leaving from
- **AWS:** ECS with Fargate — a task definition with its own service discovery, exec access, placement constraints and a network interface per task, which is a security boundary you lose.
- **Google Cloud:** Cloud Run — request-billed, with a concurrency model, revision traffic splitting and scale to zero that have no default equivalent on a fixed fleet.
- **Azure:** Container Apps — already KEDA, Dapr and Envoy over Kubernetes underneath, so it converts the most directly of the three.

## Why this works
These three are not one thing and converting them as though they were is why this Move exists separately. A task definition becomes a Deployment, a Service and a network policy, and loses its per-task network boundary, which has to be re-expressed as policy rather than assumed away. A request-billed container has a concurrency model and a scale-to-zero behaviour that a fixed fleet does not reproduce for free. And one of the three is already Kubernetes underneath, so it converts almost mechanically. The honest note is about billing: a workload that cost nothing while idle now occupies capacity you bought.

## Before you start

**Access**
- The task or service definitions exported, including the placement rules nobody remembers writing
- Traffic profiles per service, because the ones that are genuinely bursty may not move at all

**Software**
- Manifests derived from each definition, with the sidecars converted rather than dropped
- An autoscaler configuration for the request-billed services, since concurrency was doing that job before

**People**
- The owner of each service, to say whether idle cost or peak latency is the thing that matters to them

## The runbook
1. Sort the estate by runtime first. Three different services with three different conversion paths, and treating them as one is how a migration produces a fleet of half-converted workloads.
2. Convert task definitions into a Deployment, a Service and a network policy. Take the sidecars seriously: a logging or proxy sidecar in the old definition has an equivalent here, and dropping it silently removes a function somebody depends on.
3. Re-express the per-task network boundary as policy. Each task had its own interface and its own firewall membership; here that becomes a label selector in Move 60's policy set, and it must be written rather than assumed.
4. Replace the exec path. Debugging access to a running task was a platform feature; here it is a role, a policy and an audit trail, and it should be granted deliberately.
5. For the request-billed services, map concurrency onto replicas and requests, and add an autoscaler that responds to the same signal the platform used. Revision traffic splitting becomes two deployments and a weight.
6. Be honest about the ones that should not move. A service that runs for four minutes a day and costs nothing while idle now occupies reserved capacity, and the right answer may be that it stays rented until Move 89 gives it a scale-from-zero design.
7. Run both for a week per service, with traffic split, and compare cost as well as latency.

## Operator's notes
- **Swap:** Where a service is already on the platform that is Kubernetes underneath, convert it first. It is the fastest win and it builds the pattern for the harder two.
- **Do it faster:** Convert the definitions with a script and then read every output by hand. The mechanical part is quick and the review is where the sidecars and the placement rules are caught.
- **Watch out:** Scale to zero is a billing property, not a design one. A service that has never handled a cold start on a fixed fleet may have a first-request latency nobody has measured.
- **Leftovers:** The old service definitions, their service-discovery namespaces and their per-task interfaces stay until Part VII, and the discovery namespaces in particular are easy to forget.

## Rollback
Each service is reverted by shifting its traffic weight back, with the old task still defined and still able to run, so this is reversible per service and within minutes. There is no point of no return. Keep the exported definitions in source control so the original placement rules and sidecars can be restored and compared when a converted service behaves differently under load.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,260/mo | $0/mo | 100% | 0 min | 2 weeks | — |

## What you can turn off
The task definitions, service-discovery namespaces and request-billed revisions, once a week of split traffic shows the same behaviour on both sides.
