# 20 · Closing the account

**Layer:** Run · **Leaving:** The provider organisation, its audit trail and its support plan · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> The estate moved a month ago. The account did not: a dormant organisation still bills, still holds credentials, and still lets someone start an instance in it.

## Leaving from
- **AWS:** AWS Organizations and the management account — the management account can close members centrally, but a closed account's ninety-day reopening period does not cancel its commitments.
- **Google Cloud:** organisation and its projects — project deletion is scheduled rather than immediate, and a lien refuses the request outright.
- **Azure:** subscriptions and the Entra tenant — tenant deletion also checks Microsoft 365 and other connected services; leaving Azure compute does not make their shared identity disposable.

## Why this works
A migration that stops at cutover can leave live credentials, forgotten bills and an audit trail nobody has exported. Observe a full monthly job cycle before destructive cleanup: the job on the twenty-eighth still needs its bucket. Planned recovery copies keep billing during that wait. Close only after retention obligations, commitments and shared services are accounted for. The strip's zero is the completed reference outcome; an unexpired contract or retained archive still has a cost.

## Before you start

**Access**
- Provider closure authority and independent recovery logins, controlled by two named people
- The registrar login, often held by one person who has since left

**Software**
- `aws`, `gcloud` or `az` signed in with an identity that can read billing
- `rclone` 1.75.1 to copy exported audit trails and billing history somewhere you own

**People**
- Whoever answers the auditor, because the attestations you inherited become yours to produce
- The finance owner who has to see the invoice reach zero and say so

## The runbook
1. Take the final invoice apart with `aws`, `gcloud` or `az`. Expect address translation gateways nothing routes through, CloudWatch log groups still ingesting, snapshots on a retention policy nobody reviews, a support plan priced against spend that has gone, and two subscriptions from a proof of concept three years ago.
2. Have the auditor confirm the required period, then export audit trails, billing history and compliance evidence through their provider services. Copy the exports with `rclone` and test them without cloud credentials. Re-encrypt retained data under independently controlled keys where necessary; copying ciphertext does not free it from a provider-managed key.
3. Revisit the archive you decided in Move 15 to leave behind. Data parked in an account you are closing is not archived anywhere. Move it out, or agree in writing to delete it once someone has confirmed nothing still reads from it.
4. Transfer provider-managed domain registrations, preserving DNS service and renewal access, then restore the transfer lock. Move authoritative zones too before closing their projects or accounts; changing registrar alone does not move DNS hosting. Verify mail, certificate validation and the replacement platform's sign-in path.
5. Quiesce remaining workloads and disable automation that restarts them. Deallocate Azure VMs rather than only shutting down guests. Reduce or cancel support under its terms and observe one full monthly job cycle with no unexplained usage. Keep snapshots, volumes and their keys throughout the wait; finance records their expected residual charges.
6. With exports restored, retention satisfied and owners' approval recorded, remove remaining workload resources and unused credentials. Schedule key destruction only after proving no retained data needs them. Keep closure administrators until the last request. Close member accounts, projects and subscriptions before their parent, preserving any tenant still used for identity or office services.

## Operator's notes
- **Swap:** Where one thing genuinely has to stay — an archive whose egress you will not pay — move it into a small account of its own and close everything around it.
- **Do it faster:** Inventory key dependencies during the observation month. Schedule destruction only after independent recovery passes: a key pending deletion can already be unavailable for decryption, even while deletion remains cancellable.
- **Watch out:** Committed spend does not end when usage does. A Savings Plans commitment keeps billing against the organisation after every resource inside it has gone.
- **Leftovers:** Check marketplace contracts, support cancellation terms and final invoices separately. Account closure is not proof that contractual charges or data-retention duties ended.

## Rollback
During observation, retained resources and keys allow a tested return. Destructive cleanup is irreversible once required data or keys disappear: that is the point of no return, potentially before account closure. AWS offers a ninety-day reopening period subject to its conditions; Azure describes thirty to ninety days of data retention after cancellation. Google permits project restoration for thirty days, but some services can delete data sooner. None is a universal restore guarantee. Treat closure requests as final and rely on independent, already-restored copies for records you must retain.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $3,200/mo | $0/mo | 100% | 0 min | 4 days | 1 month |

## What you can turn off
The unused account or project and its remaining services, after the observation month and verified export. Preserve required archives and shared identity, settle commitments, and reconcile the final invoices before calling its cost zero.
