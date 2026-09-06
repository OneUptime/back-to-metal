# 27 · What a tier rating promises, and what it does not

**Layer:** Site · **Leaving:** — · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** Immediately

> Separates tier topology from tier certification and from the similarly numbered parallel schemes, and retires the availability percentages quoted beside them.

## Leaving from
- **AWS:** the shared responsibility model and its compliance reports — the building's resilience arrived as an attestation you inherited rather than assessed.
- **Google Cloud:** its compliance reports manager — the same inheritance, with the physical estate described and never inspected.
- **Azure:** the Service Trust Portal — again somebody else's audit, and again the reason nobody arriving from a cloud has read a tier standard.

## Why this works
A sales deck runs three different things together. Tier topology describes redundancy and whether the facility can be maintained without being switched off, and nothing else. Tier certification is a separate exercise and comes in three distinct forms — one for the design documents, one for the constructed building, and one for how it is operated — of which only the second tells you the building was built the way it was drawn. And there are parallel schemes with confusingly similar numbering that are different standards with different scopes. Knowing which of these a facility actually holds is the difference between a tour and an assessment.

## Before you start

**Access**
- Whatever certificates the facility claims, requested as documents rather than logos on a website
- A tour booked, with the plant rooms included rather than the reception and the hall

**Software**
- A written question list, prepared beforehand, because the useful questions do not occur to you on the day
- The relevant standard's scope statement, read once, so you know what the certificate covers

**People**
- Somebody technical on the tour who will look at the plant, not only at the racks

## The runbook
1. Ask which certificate the facility holds and for which of the three forms. A design certificate and a constructed-facility certificate are different documents, and only the second says the building matches the drawings.
2. Ask for the certificate itself with its date and scope. Certificates apply to a specific building and sometimes to a specific phase of it, and a group-level claim is not a certificate for the hall you will occupy.
3. Note which scheme it is. The parallel schemes number their levels the same way and mean different things, and a facility rated under one will happily be described as though it were rated under another.
4. Retire the availability percentages. The figures still quoted beside each tier were removed from the standard in 2009 and never constituted a guarantee of anything. If a percentage appears in a proposal, ask what contractual commitment stands behind it, and Move 29 will tell you the answer is a capped credit.
5. Use the tour, and the question list, to ask what the topology means in practice: can the uninterruptible supply be maintained without dropping load, can a cooling unit be taken out in July, when was the generator last run under load, and for how long.
6. Write down what the facility actually holds, what it actually claims, and the gap between them. That gap is a negotiating position for Move 28 and Move 29.

## Operator's notes
- **Swap:** An uncertified facility with an excellent operations record and open answers can be a better bet than a certified one that will not let you into the plant room. The certificate is evidence, not the thing itself.
- **Do it faster:** Ask two questions on the phone before booking a tour: which certificate, and for which building. That removes half the shortlist without leaving your desk.
- **Watch out:** Concurrently maintainable and fault tolerant are precise terms with different meanings, and they are used interchangeably in marketing. The distinction is whether the facility survives a failure or only a planned maintenance.
- **Leftovers:** The question list from this Move is reused at every renewal and at every new site. Keep it.

## Rollback
Nothing is committed here, so this Move is undone by filing the notes. The point of no return is Move 28, which commits power in a specific building; everything before that is assessment. If a facility later turns out to have been misdescribed, these notes are the record, so keep them dated and in source control where an earlier version can be restored and compared against what the facility says at renewal.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 2 days | — |

## What you can turn off
Nothing. This Move costs two days and changes what you are willing to sign in Move 28.
