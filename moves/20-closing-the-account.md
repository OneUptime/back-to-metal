# 20 · Closing the account

**Layer:** Run · **Leaving:** The provider organisation, its audit trail and its support plan · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> The estate moved a month ago. The account did not: a dormant organisation still bills, still holds credentials, and still lets someone start an instance in it.

## Leaving from
- **AWS:** the management account and its support plan — closing a member account takes the management account, but making one standalone first needs its own contact details, payment method and support plan.
- **Google Cloud:** organisation and its projects — project deletion is scheduled rather than immediate, and a lien refuses the request outright.
- **Azure:** subscriptions and the Entra tenant — the tenant refuses deletion while any subscription or application registration still exists.

## Why this works
A migration that stops at the traffic cutover leaves about $1,240 a month and a quieter second problem: live credentials, an audit surface someone will still ask about, and enough idle capacity to make drifting back the cheapest decision in the room. Nothing here is deleted until a full billing month has passed with the line at zero and no ticket filed. The failures that follow a migration are monthly rather than daily — the job that runs on the twenty-eighth and cannot find its bucket. Switching off and closing down stay four weeks apart, with everything irreversible on the far side of that gap.

## Before you start

**Access**
- Root credentials for the management account, held by two named people
- The registrar login, often held by one person who has since left

**Software**
- `aws`, `gcloud` or `az` signed in with an identity that can read billing
- `rclone` 1.68 or newer to copy the audit trail and billing history somewhere you own

**People**
- Whoever answers the auditor, because the attestations you inherited become yours to produce
- The finance owner who has to see the invoice reach zero and say so

## The runbook
1. Take the final invoice apart with `aws`, `gcloud` or `az`. Expect address translation gateways nothing routes through, CloudWatch log groups still ingesting, snapshots on a retention policy nobody reviews, a support plan priced against spend that has gone, and two subscriptions from a proof of concept three years ago.
2. Extract what cannot be recovered later: the audit trail for the period your auditor requires, the billing history, and the compliance attestations you inherited. Copy them out with `rclone`, then open one of each and check it reads.
3. Revisit the archive you decided in Move 15 to leave behind. Data parked in an account you are closing is not archived anywhere. Move it out, or agree in writing to delete it once someone has confirmed nothing still reads from it.
4. Move the domain before anything touches identity. Where the registrar sits with the provider — Route 53 is its own, and Azure fronts a partner under its own name — transfer it away, then put the lock back on.
5. Turn everything off and remove nothing. Stop the instances, drop the support plan to the free tier, keep the snapshots, and wait one full billing month with the compute lines at zero and no ticket filed. The snapshots and the volumes under the stopped instances go on billing, and are meant to: that residue is what keeps the month reversible.
6. Close it from the leaves inward. Federation and human users first, then access keys and roles, then the keys in Secrets Manager or Key Vault, because those decrypt archives you may still hold. Member accounts and subscriptions next; the organisation itself last.

## Operator's notes
- **Swap:** Where one thing genuinely has to stay — an archive whose egress you will not pay — move it into a small account of its own and close everything around it.
- **Do it faster:** Begin the key management waiting periods on the first day of the wait, not the last. Seven to thirty days is the AWS range; Google's can be set as long as a hundred and twenty, and a Key Vault holds keys for a retention period fixed when the vault was created. Nothing else waits on any of them.
- **Watch out:** Committed spend does not end when usage does. A Savings Plans commitment keeps billing against the organisation after every resource inside it has gone.
- **Leftovers:** Billing exports, budget alerts and marketplace subscriptions outlive what they were attached to. So does the support plan, which renews on its own anniversary rather than yours.

## Rollback
Until the closure request this is ordinary work: an account switched off can be switched back on in an afternoon, which is why the wait is four weeks and not four days. The point of no return is the request itself. AWS will reopen a closed account for ninety days, a cancelled Azure subscription keeps its data for thirty to ninety, and a Google project stays scheduled for deletion for thirty — so a restore of anything left inside is possible for thirty days on all three and impossible after ninety. Use the wait to confirm the audit trail and billing history read correctly from your own copies.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $1,240/mo | $0/mo | 100% | 0 min | 3 days | 4 weeks |

## What you can turn off
The account itself, and with it the support plan, the idle gateways, the log ingestion and the snapshot retention still billing a month after the last user request left. What is left is a platform rather than a project.
