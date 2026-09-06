# 107 · Email: inbound comes home, outbound does not

**Layer:** Edge · **Leaving:** Managed inbound email receiving and its object-store pipelines · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 7 days

> Brings inbound mail home to a receiver you run and keeps outbound on a relay, because sender reputation cannot be rebuilt on demand.

## Leaving from
- **AWS:** SES inbound receiving with its rule sets — the only first-party inbound receiving of the three, writing to a bucket or invoking a function.
- **Google Cloud:** no first-party inbound receiving — so these readers are leaving a third party rather than their cloud.
- **Azure:** Communication Services email — outbound only, so again the inbound half is somebody else's product.

## Why this works
The two halves of email have opposite answers. Inbound is a service you can run: a receiver, a spam pipeline, and storage of what arrives, and it is not difficult. Outbound is not, because sending mail that reaches inboxes depends on a sender reputation that takes months to build and can be destroyed in a day, and on alignment records, reverse name records, list-unsubscribe handling and a failure mode that is invisible — your mail is accepted and filed in a spam folder, and nothing tells you. So this Move brings inbound home and refuses the outbound half explicitly, which closes the Part on a deliberate no.

## Before you start

**Access**
- The zone from Move 104, because every record this Move touches lives there
- The current inbound rules exported, including the ones that invoke code

**Software**
- A receiver you run with a real spam pipeline in front of it, not a bare mail server
- Storage of received mail on the object store from Move 49, under Move 54's durability terms

**People**
- The owner of every transactional sender and every mail-to-webhook integration, named individually

## The runbook
1. List the senders that will be affected, individually. Standards-compliant senders retry for four to five days and will survive any cutover; transactional senders and mail-to-webhook integrations frequently give up in minutes and report a bounce, and those are the ones that need warning.
2. Stand up the receiver with a genuine spam pipeline in front of it. A bare mail server on the internet receives mostly abuse, and filtering is the product rather than an add-on.
3. Store received mail on the object store from Move 49, under the durability terms Move 54 established. Mail is data and it inherits the same rules as everything else.
4. Reproduce the rules that invoked code. Where an inbound rule triggered a function, that becomes a service or a job on the substrate from Move 81, and it is ordinary work.
5. Cut the mail exchanger record over with both destinations live and equal preference, so mail arrives at either while the change propagates. For compliant senders this is lossless.
6. Watch both destinations for a week and confirm the old one goes quiet before removing it.
7. Refuse the outbound half in writing, with the reasons: alignment, reverse name records, warmed reputation, one-click unsubscribe handling and an invisible failure mode. Keep the relay bought and put it on Move 116's list.

## Operator's notes
- **Swap:** Where inbound volume is trivial, a hosted mailbox provider with forwarding is simpler than running a receiver and costs almost nothing.
- **Do it faster:** Run both destinations at equal preference for a fortnight rather than cutting. There is no cost to the overlap and it removes the timing risk entirely.
- **Watch out:** A mail-to-webhook integration that reports a bounce to a customer looks like your outage even though it is their retry policy. Warn those senders individually before the record changes.
- **Leftovers:** The managed receiving rules and the object-store pipeline behind them bill per message received and per bucket write, and both stop when the rules are deleted.

## Rollback
For seven days both destinations are live, so reverting is removing the new record and leaving the old one. Nothing is lost for compliant senders because they retry. The point of no return is deleting the managed receiving rules, after which mail addressed under them is rejected rather than queued — so keep them until the new destination has been the only one receiving for a full week, and confirm the stored mail can be restored and read before removing anything.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $260/mo | $40/mo | 85% | 0 min | 2 weeks | 4 weeks |

## What you can turn off
The managed inbound receiving rules and their pipelines, a week after the new destination is the only one receiving. The outbound relay stays bought.
