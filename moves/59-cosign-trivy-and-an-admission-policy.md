# 59 · cosign, Trivy and an admission policy

**Layer:** Platform · **Leaving:** Managed image scanning, managed code signing, tag immutability, scan-on-push gates and cluster-level binary authorisation · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately

> Leaving the managed registry deletes signing, scanning and the admission gate at once, so all three are rebuilt with cosign, Trivy and a break-glass bypass.

## Leaving from
- **AWS:** ECR enhanced scanning with Signer — scan-on-push you can replace with an open scanner more or less directly.
- **Google Cloud:** Artifact Analysis with Binary Authorization — an attestor model that does not map one to one onto a policy rule, so this reader re-derives the policy rather than translating it.
- **Azure:** Microsoft Defender for Containers — again scan-on-push at the registry, with the findings landing in a security portal rather than in the registry.

## Why this works
Moving off the managed registry removes three things at once, and only one of them is obvious. Scanning goes, signing goes, and the admission gate that refused unsigned or vulnerable images goes with them. All three are rebuilt here: signatures and attestations chained to the root of trust from Move 57, scanning in the pipeline and again in the registry so that a base image which rots after the build is still caught, and enforcement at admission. The interesting part is the failure mode. A policy that blocks the fix at three in the morning is a policy that gets deleted at five past, so the bypass is designed, written down and alerted on rather than improvised.

## Before you start

**Access**
- The registry of record from Move 58, holding images the pipeline already pushes
- The root of trust from Move 57, so signatures chain to something rather than to a key in a file

**Software**
- `cosign` for signatures and attestations, pinned, with its key material held by Move 57
- A scanner in the pipeline and in the registry, and an admission controller at a pinned chart version

**People**
- Whoever is on call, because they are the ones who will meet the bypass under pressure

## The runbook
1. Sign images in the pipeline with `cosign`, chained to the root of trust from Move 57, and attach a software bill of materials as an attestation at the same time. Signing without an inventory answers half the question Move 117 will ask.
2. Scan in the pipeline and again in the registry. The first catches what you built; the second catches a base image that developed a vulnerability three weeks after the build, which is the majority of real findings.
3. Install the admission controller at a pinned chart version and run every policy in audit mode first. Read a week of what it would have blocked before blocking anything, because the first run always finds something surprising and important.
4. Turn on enforcement one namespace at a time, starting with the least critical. A cluster-wide switch is how an admission policy takes down a production deploy on its first evening.
5. Design the break-glass bypass explicitly: who can use it, how it is invoked, how long it lasts, and what alert fires when it is used. An undesigned bypass is a deleted policy.
6. Re-derive rather than translate if you are leaving a cluster-level authorisation model. The attestor structure there does not map cleanly onto a policy rule, and a mechanical translation produces a policy that passes tests and permits things it should not.
7. Prove it works from both directions: push a signed, clean image and watch it admit; push an unsigned one and watch it refuse, with a message a developer can act on.

## Operator's notes
- **Swap:** Where an admission controller is too much for the team, registry-side scanning with a hard failure in the pipeline covers most of the ground. You lose the guarantee that only signed images run, and you should say so.
- **Do it faster:** Start with one policy — images must come from your registry — and enforce only that. It is the highest-value rule and it is uncontroversial.
- **Watch out:** Blocking on vulnerability severity alone produces a policy that fails builds for findings nobody can fix. Gate on signature and provenance, and handle vulnerabilities through the patch commitment in Move 117.
- **Leftovers:** The managed scanning subscriptions bill per image or per node and can be turned off once your own scanning is producing findings people act on.

## Rollback
Every part of this is reverted by removing the policies, and the images remain signed and scanned regardless, so nothing is lost by backing out. There is no point of no return here. The real risk is the opposite failure — a policy enforced too widely too early, which is why the audit week and the namespace-by-namespace rollout exist. Keep the policies in source control so a known good set can be restored the moment a bypass is used at three in the morning.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $340/mo | $0/mo | 100% | 0 min | 1 week | — |

## What you can turn off
The managed scanning subscription, once your own findings are being triaged by a person under Move 117.
