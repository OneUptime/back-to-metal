# 61 · East-west encryption, and an identity per workload

**Layer:** Platform · **Leaving:** Managed service mesh add-ons and the in-mesh mTLS they provided by default · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Gives every workload a cryptographic name and encrypts pod-to-pod traffic, which is the destination Move 55 named and what an auditor asks for before data lands.

## Leaving from
- **AWS:** App Mesh — retired, so this population is migrating regardless of anything in this book.
- **Google Cloud:** Anthos Service Mesh and Cloud Service Mesh — Istio underneath, which makes this a control-plane swap rather than a rewrite.
- **Azure:** the Open Service Mesh add-on — also retired, which leaves this reader in the same position as the first.

## Why this works
There are two different things people mean by encrypting east-west traffic, and conflating them is why this Move takes either a week or three. The floor is node-to-node encryption, which is close to one flag, protects traffic on the wire between machines, and costs measurable throughput that this Move measures rather than guesses. The thing an auditor usually means is different: a cryptographic identity per workload, so that a service can prove which service it is, and mutual authentication between named services. That is the destination Move 55 pointed at, and it is worth reaching before Part V puts real data on the network.

## Before you start

**Access**
- The namespace policy from Move 60 in place, because encryption without policy protects the wire and not the access
- A load test that can measure throughput before and after, honestly

**Software**
- Node-to-node encryption available in the network plug-in already installed in Move 44
- If per-workload identity is in scope, a mesh chosen with its licence read rather than assumed

**People**
- Whoever will answer the auditor's question in Move 119, so that what is built matches what will be asked

## The runbook
1. Decide which of the two things you are doing, and write it down. Node-to-node encryption is a week. Per-workload mutual authentication is three, and it changes how services are named.
2. Turn on node-to-node encryption in the network plug-in and measure throughput before and after with a real load test. The cost is measurable and it is better to know the number than to discover it during an incident.
3. Confirm the encryption is actually applied by capturing traffic between two machines and looking at it. A flag that is set and not working is the failure mode here, and it is silent.
4. If per-workload identity is in scope, choose the mesh with the licence read. One popular option now requires a paid subscription for stable builds above a modest organisation size, leaving only edge releases freely available; the book's default is the mesh that runs without sidecars in its lighter mode.
5. Roll the mesh out per namespace and give each service a name that means something. The identity is the point; the encryption is a consequence.
6. Prove it from the auditor's direction: show that service A can prove it is service A, that service B refuses an unauthenticated caller, and that both facts are logged somewhere durable.

## Operator's notes
- **Swap:** For most estates, node-to-node encryption plus the policy from Move 60 is a defensible position, and per-workload identity can wait for a specific requirement. Say which one you have.
- **Do it faster:** Do the encryption now and the identity later. They are independent and the first one is a genuine improvement on its own.
- **Watch out:** A mesh adds a component to every request path. Whatever is chosen must be something the team can debug at three in the morning, and that is a stronger constraint than any feature comparison.
- **Leftovers:** Two of the three managed mesh add-ons are retired or retiring, so there is often nothing left to turn off — the bill went away before you did.

## Rollback
Node-to-node encryption is a flag and is reverted in minutes with a brief interruption to cross-machine traffic. A mesh is removed per namespace and the services keep working, because the mesh sits beside them rather than inside them. There is no point of no return. Keep the throughput measurements, taken before and after, so that a later performance question can be answered with data rather than suspicion, and so the previous configuration can be restored knowingly.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $290/mo | $0/mo | 100% | 0 min | 3 weeks | — |

## What you can turn off
The managed mesh add-on, where it still exists. On two of the three clouds it has already been retired for you.
