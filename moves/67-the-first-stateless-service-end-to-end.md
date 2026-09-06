# 67 · The first stateless service, end to end

**Layer:** Platform · **Leaving:** One stateless service: its workload identity role, its load-balancer target group and its managed log group · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> One service goes from inventory to production traffic with every step written down, because the next eighty follow it and the rollback is one weighted DNS record.

## Leaving from
- **AWS:** an EKS Deployment behind an Application Load Balancer — with an IAM role for the pod and a CloudWatch log group behind it.
- **Google Cloud:** a GKE Deployment behind a load balancer — with a service account and a Cloud Logging sink doing the same two jobs.
- **Azure:** an AKS Deployment behind Application Gateway — with a managed identity and a Log Analytics workspace behind it.

## Why this works
This is the Move where everything built in Parts III and IV is used at once, on one real service, with every step written down — because the next eighty services follow this path and the difference between a good runbook and a vague one is measured in months. The traffic comes through the load balancer still running in the cloud, across the interconnect from Move 53, onto the routable pod addresses from Move 45. None of Part VI exists yet and none of it is needed. The rollback is one weighted record in the cloud's name service, which is why this can be done on a Tuesday afternoon.

## Before you start

**Access**
- A service whose owner is willing, whose dependencies are known, and which is not the most important thing you run
- The cloud load balancer in front of it, with the ability to add a second target and weight it

**Software**
- Manifests and chart values, config and secrets from Move 56, image and signature from Moves 58 and 59
- Dashboards and log pipeline from Moves 62 and 63, already collecting from the new cluster

**People**
- The service's owner, in the room, because the handover is the point and not the deployment

## The runbook
1. Map the dependencies before writing anything. What it calls, what calls it, what data it touches, and what it assumes about its environment. This map is the template for every service that follows.
2. Run the compatibility audit. The new cluster is on a newer Kubernetes minor than the managed one, so deprecated resource versions, removed flags and changed defaults all need checking against the manifests rather than discovered at admission.
3. Assemble the whole package: manifests, chart values, configuration and secrets, a signed image, an identity from Move 55 and a network policy from Move 60. Write down each step as you do it; this document is the deliverable.
4. Deploy with no traffic and let it run for a day. Watch its dashboards, read its logs, and confirm both are as usable as the ones it had before.
5. Add the new cluster as a second target behind the existing cloud load balancer, weighted at a small percentage, and watch error rates and latency at the same resolution as the old target.
6. Increase the weight in steps over a few days rather than in one change, and stop at any step where the two targets do not behave the same.
7. Hand the namespace over as a product: quotas, roles, a dashboard, a way to deploy and a way to roll back. A service that has moved but that its team cannot operate has not moved.

## Operator's notes
- **Swap:** Where no service is small enough to be a good first candidate, build a trivial one that does something real — an internal tool, a status endpoint — and move that first. The point is the path, not the service.
- **Do it faster:** Do the second service the week after the first, with the same person, following the document. That is the run that turns a narrative into a runbook.
- **Watch out:** The appliances that stay rented — a managed identity gateway, a third-party service behind a private link — are dependencies too, and they need to be reachable from the new cluster before the first request arrives.
- **Leftovers:** The old target group, task definition and log group stay until the weight has been at one hundred per cent for a fortnight.

## Rollback
Set the weight back to zero on the cloud load balancer and the traffic returns instantly to where it was, with the old deployment still running and still warm. There is no point of no return in this Move at all, which is what makes it the right place to spend two weeks. Keep the runbook, the manifests and the dependency map in source control so the exact configuration can be restored, and leave the old deployment in place for a fortnight rather than tidying it up on the day.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $640/mo | $0/mo | 100% | 0 min | 2 weeks | — |

## What you can turn off
The old service's compute and its log group, a fortnight after the weight reaches one hundred per cent and stays there.
