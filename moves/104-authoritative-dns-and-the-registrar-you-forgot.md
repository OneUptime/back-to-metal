# 104 · Authoritative DNS, and the registrar you forgot

**Layer:** Edge · **Leaving:** Managed authoritative DNS and provider-integrated registrars · **Risk:** High · **Cutover:** 0 min · **Reversible:** 7 days

> Moves the zone to a managed anycast provider and dual-serves for the parent TLD's NS TTL, because the recovery path needs DNS too.

## Leaving from
- **AWS:** Route 53 with its own registrar — the provider is also the registrar, so both have to be considered together.
- **Google Cloud:** Cloud DNS — the provider exited domain registration and handed its customers to a third party, so the registrar is already somewhere else.
- **Azure:** Azure DNS with App Service domains — a partner registrar fronted under the provider's own name, which is the case people forget entirely.

## Why this works
Name resolution is the one service that has to work when everything else does not, which is why this Move moves the zone to a managed anycast provider rather than to nameservers you run. Running your own is refused here, and deliberately: a recovery path that depends on your own infrastructure resolving your own names has a circular dependency in exactly the situation you built it for. The transition is a dual-serving window at least as long as the parent zone's nameserver lifetime, during which every edit is applied to both sides — a discipline that is simple to state and easy to break.

## Before you start

**Access**
- Administrative access to the registrar, which is frequently held by one person who left
- A zone export from the current provider, including the records created by automation

**Software**
- A managed anycast DNS provider, with the zone imported and verified record by record
- The cluster's record publisher repointed, so automation keeps writing to the right place

**People**
- Whoever holds the registrar account, because changing nameservers happens there and nowhere else

## The runbook
1. Find the registrar before anything else. One provider is its own registrar, one exited registration and handed customers to a third party, and one fronts a partner under its own name. Establish which you have and who can log in.
2. Export the zone and import it, then compare record by record rather than by count. Records created by automation are the ones that go missing.
3. Deal with the apex record. A name at the zone apex cannot be a normal alias, so providers implement flattening differently, and the behaviour you rely on may not exist on the other side.
4. Reproduce or retire the routing features. Latency and geography routing keyed to cloud regions is keyed to regions that will not exist much longer, and health-check-driven failover has to be rebuilt against endpoints you now own.
5. Repoint the cluster's record publisher at the new provider so automation keeps working, and confirm it can create and delete records.
6. Add the new nameservers at the registrar and dual-serve for at least the parent zone's nameserver lifetime, which is typically a day or two. Every edit during the window is applied to both sides, without exception.
7. Move the certificate challenge delegation from Move 97 with the zone, or issuance stops working the moment the old provider is removed.

## Operator's notes
- **Swap:** Two managed anycast providers serving the same zone is a genuinely good permanent arrangement for anyone whose availability requirement justifies it, and it costs very little.
- **Do it faster:** Import the zone and dual-serve weeks before you need to, then take your time verifying. Nothing forces the removal of the old provider on a schedule.
- **Watch out:** An edit applied to one side during the dual-serving window produces answers that differ depending on which nameserver a resolver picked, which is the hardest class of fault to diagnose because it is intermittent by design.
- **Leftovers:** The old hosted zone bills per zone and per million queries, and queries continue for a long time after the nameservers change.

## Rollback
For seven days both providers serve the zone, so reverting is removing the new nameservers at the registrar. The point of no return is the deletion of the old hosted zone, after which the record set exists only in your export — so keep that export in source control and confirm it can be restored into a new zone before deleting anything. The registration itself stays where it is; this Move does not move it.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $180/mo | $30/mo | 83% | 0 min | 1 week | 7 days |

## What you can turn off
The old hosted zone, seven days after the nameservers changed and the query count there has fallen to nothing.
