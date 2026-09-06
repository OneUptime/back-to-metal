# 119 · The auditor's checklist, and the contracts nobody read

**Layer:** Watch · **Leaving:** Inherited compliance attestations, the provider's audit-evidence portal and its committed-spend agreement · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Rebuilds the evidence pack from the facility's report, the asset register and the sanitisation certificates, because physical controls stop being inherited.

## Leaving from
- **AWS:** Artifact — a portal where compliance reports were downloaded and inherited without further thought.
- **Google Cloud:** Compliance Reports Manager — the same, with the same effect on how nobody learned what the reports covered.
- **Azure:** the Service Trust Portal — the same again, and the same set of controls that quietly stop being somebody else's.

## Why this works
A large part of your compliance posture was inherited from a provider and evidenced by a report you downloaded. Moving into a facility changes who owns which controls, and the ones that stop being inherited are physical: access, environmental, media handling and disposal. So the evidence pack is rebuilt from what you now have — the facility's own report and, critically, the complementary controls it expects you to operate — plus the sanitisation certificates from Move 38, the asset register from Move 110 and the trail from Move 118. The legal half is the part that blocks migrations hardest and is started a quarter early.

## Before you start

**Access**
- The facility's own audit report, including its complementary user entity controls section
- Every customer contract, data-processing agreement and security questionnaire that names a provider

**Software**
- An evidence pack assembled as documents rather than as links into consoles you are closing
- The committed-spend agreement read for what happens when spending stops

**People**
- Counsel, the auditor and whoever owns customer contracts, all engaged a quarter before the audit window

## The runbook
1. Read the facility's report properly, including the complementary controls section. That section lists what the facility assumes you are doing, and every item in it is now yours to evidence.
2. List the controls that stop being inherited: physical access, environmental, media handling and media disposal. Map each to evidence you actually hold.
3. Assemble the evidence: sanitisation certificates and chain of custody from Move 38, the asset register from Move 110, the audit trail from Move 118, the access list from Move 35 and the acceptance results from Move 18.
4. Start the legal work a quarter early, because it lives in other people's calendars. Sub-processor notices, data-processing agreements that name the old provider explicitly, and customer security questionnaires whose answers were written against cloud controls.
5. Read the committed-spend agreement for what happens when spending stops. On all three providers the commitment does not shrink because you stopped using the service, so the remaining term is a cost regardless.
6. Rewrite the questionnaire answers before a customer asks. An answer that says a control is inherited from a provider you have left is a false statement in a contractual document.
7. Rehearse the audit conversation once with somebody playing the auditor. It finds the missing evidence while there is still time to produce it.

## Operator's notes
- **Swap:** Where an attestation genuinely cannot be reproduced in time, a scoped exception agreed with the auditor in advance is far better than discovering the gap during the audit.
- **Do it faster:** Collect evidence continuously rather than in a scramble. Every Move in this book that says keep this in source control is feeding this pack.
- **Watch out:** A data-processing agreement naming a specific provider is a contractual commitment, not a description. Changing where the data lives may require customer notice or consent.
- **Leftovers:** The committed-spend agreement runs to its end date whether or not anything runs on it, and Move 120 has to carry that as a real line.

## Rollback
This Move is irreversible in the sense that matters: statements made to auditors and customers cannot be unmade, and a commitment surrendered or a notice served cannot be recalled. The point of no return is the first formal notice to a customer or a regulator. Keep every version of the evidence pack, so the state of the controls at any past date can be restored and shown, which is what an auditor is actually asking for.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 3 weeks | 8 to 12 weeks |

## What you can turn off
Nothing. This Move adds work that the provider was doing invisibly, and it is the work that keeps the contracts valid.
