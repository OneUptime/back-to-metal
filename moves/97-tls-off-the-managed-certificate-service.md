# 97 · TLS off the managed certificate service

**Layer:** Edge · **Leaving:** Managed certificate services and managed private certificate authorities · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Issues and renews every certificate from cert-manager through a delegated challenge zone, and rebuilds the internal hierarchy the managed private CA was holding.

## Leaving from
- **AWS:** Certificate Manager and Private CA — public certificates are exportable for a per-name fee, and only when issued as exportable in the first place.
- **Google Cloud:** Certificate Manager and Certificate Authority Service — where the private key of a managed public certificate is not handed over.
- **Azure:** App Service Certificates and Key Vault — where a certificate's key can be exported, which changes the custody argument for this reader.

## Why this works
The case for leaving has to be made accurately, because the folklore is out of date: two of the three providers will now give you a public certificate's private key, one of them for a fee and only when the certificate was issued as exportable. So the argument is not that you are locked out of your own keys. It is renewal automation you control, cost, and the private hierarchy — which is the larger half of this Move. What replaces the managed service is automated issuance through a challenge delegated to a throwaway zone, plus an offline root and an issuing authority for everything internal.

## Before you start

**Access**
- A delegated zone dedicated to challenge records, so the issuance credential is scoped to nothing else
- The root of trust from Move 57, which is where the internal authority's key material lives

**Software**
- `cmctl` and the issuer configuration, with issuance rate limits understood as an availability dependency
- An offline root and an issuing authority for the internal hierarchy

**People**
- Whoever owns the domain, because delegating a zone is a change on their side

## The runbook
1. Delegate a dedicated zone for challenge records and scope the issuance credential to it alone. A credential that can edit your production zone in order to prove domain control is a much larger grant than the job needs.
2. Configure automated issuance for public names and confirm a renewal end to end, not just an issuance. The renewal is the part that fails silently ninety days later.
3. Treat issuance rate limits as an availability dependency. A cluster rebuild that requests two hundred certificates at once will hit them, and the failure arrives during a recovery.
4. Set expiry alerting as a fraction of remaining lifetime rather than as a fixed number of days, because the maximum lifetime of a public certificate is on a published downward schedule and a fixed threshold will stop making sense.
5. Build the internal hierarchy: an offline root, kept offline and sealed with the custody model from Move 57, and an online issuing authority for workload and service certificates. Most of this Move's two weeks is here.
6. Distribute the internal root to everything that has to trust it, and write down what that list is. A root nobody trusts is an outage waiting for the first internal call.
7. Name the case for keeping a managed private authority: where a regulator requires keys in a validated key store, buying that is the right answer and it belongs on Move 116's list of things you deliberately keep.

## Operator's notes
- **Swap:** Where only a handful of public certificates exist, issuing them by hand and diarising renewals is workable and terrible. Automate the renewal even for three certificates; the failure mode is an outage on a Sunday.
- **Do it faster:** Do the public half first. It is a day and it removes the dependency on the managed service for anything new.
- **Watch out:** A certificate that renews correctly but is not reloaded by the process using it expires while a valid one sits on disk. Test the reload, not the renewal.
- **Leftovers:** The managed private authority bills a substantial monthly fee per authority plus a per-certificate charge, and both stop only when the authority is deleted, which has its own waiting period.

## Rollback
For thirty days the managed service still holds valid certificates, so reverting is repointing the listener at them. The point of no return is the deletion of the managed private authority, which has its own deletion window and after which certificates it issued cannot be reissued from it. Keep the internal root sealed and backed up in two places, because losing it means every internal certificate has to be reissued and every trust store updated.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $520/mo | $0/mo | 100% | 0 min | 2 weeks | 30 days |

## What you can turn off
The managed private certificate authority after thirty days, and the public certificates once every listener has been serving from your own issuance for a full renewal cycle.
