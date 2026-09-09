# Publishing

Keep this record, `book/imprint.py`, Bowker and KDP in agreement. Prepared files
are not evidence of registration or publication.

## Publication preparation — 2026-09-09

The author authorized Kindle, colour paperback and colour hardcover publication,
using owned Bowker ISBNs, with at least 25% margin and prices rounded upward to
amounts ending in .99. Margin is the share of the list price retained after
Amazon's deduction and printing or delivery cost, excluding tax.

Four worksheets drawn from the existing manuscript bring the interior to an even
76 pages while preserving all Move spreads. The same templates appear in the
EPUB and on the website. The final local build confirms 76 pages.

| Edition | Ink | KDP page band | Prepared US list | Estimated US print cost |
|---|---|---|---|---|
| Paperback | Standard colour, white paper | 72–600 | $11.99 | $4.0552 |
| Hardcover | Premium colour, white paper | 75–550 | $33.99 | $11.73 |
| Kindle | Reflowable EPUB with colour artwork | Not applicable | $8.99 | Delivery based on converted file |

Estimated print margins are 26.2% and 25.5%. Confirm the final costs and royalty
in KDP before submission. The hardcover uses the official Cover Calculator
template downloaded on 2026-09-09 for 8.25 × 11 in, 76 pages, case laminate,
premium colour on white paper. `book/cover.py` records the measured guide geometry;
the generated case cover has a blank spine and reserves KDP's barcode area.

Rates checked on 2026-09-09 against KDP's public tables:
[paperback printing](https://kdp.amazon.com/en_US/help/topic/G201834340),
[hardcover printing](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H), and
[print royalties](https://kdp.amazon.com/en_US/help/topic/G201834330).
This book's trim counts as large trim.

Kindle is priced at least 20% below both print editions, as required by the
[70% royalty option](https://kdp.amazon.com/en_US/help/topic/G200634500).
Check KDP's converted delivery size and account eligibility before submission.
The free online edition remains available. Amazon can price-match it, including
to zero, so the list-price margin is not guaranteed on every Kindle transaction.
Do not enable paperback Expanded Distribution at these prices: its royalty is 40%.

## Prepared marketplace prices

These exclude tax and need a final check in KDP. US-style decimal currencies use
.99; whole-yen prices end in 99. Tax added by Amazon can change the storefront ending.

| Currency | Paperback | Hardcover |
|---|---:|---:|
| USD | 11.99 | 33.99 |
| GBP | 8.99 | 24.99 |
| EUR | 9.99 | 28.99 |
| CAD | 14.99 | Check distribution via Amazon.com |
| PLN | 45.99 | 135.99 |
| SEK | 110.99 | 322.99 |
| JPY | 1599 | Not available |

Standard-colour paperback is unavailable in Australia. Hardcover distribution to
Canada and Australia uses Amazon.com; no local printing-cost table was available.
Do not assume automatic Kindle currency conversion respects the print discount.
With these print prices, .99-ending Kindle prices must not exceed GBP6.99,
EUR7.99 or CAD11.99 to meet the 20% requirement; check other markets individually.

## Status

| Field | Status |
|---|---|
| Editions | Paperback, hardcover, Kindle |
| Print trim | 8.25 × 11 in; bleed on top, bottom and outer edge |
| Cover finish | Matte; hardcover case laminate |
| Paperback ISBN | 978-1-950600-03-8 — submitted to Bowker; dashboard status Pending |
| Hardcover ISBN | 978-1-950600-04-5 — submitted successfully; Bowker processing and dashboard verification pending |
| Bowker publisher | HackerBay, Inc. — exact account and fixed publisher-field spelling |
| Print preparation | Final 6.4.6 files validated locally; KDP uploads and previews pending |
| KDP Kindle draft | AZTAAK7S3HZ0G — details complete; content settings saved |
| KDP paperback draft | YHJP6H3BSP1 — details saved; print setup pending |
| Amazon ASINs | Not published |
| EPUB identifier | `urn:uuid:f021e81e-4b5f-4ecc-bc23-402193edac60` — never change |
| KDP Select | Do not enroll: the ebook is openly available elsewhere |
| DRM | Do not apply; the text is CC BY 4.0 |

Direct computer access to Chrome is working. On 2026-09-09, both print records
were submitted successfully in the **HackerBay, Inc.** Bowker account. The paperback
dashboard shows **Back to Metal / Paperback / Pending**. The hardcover form confirmed
a successful save; its dashboard status remains to be verified. These are submitted
ISBN filings, not completed Bowker validation or Amazon publication. No KDP submission
or ASIN has been confirmed in this record; KDP setup is ongoing.

The final 6.4.6 files, including the filed ISBNs and exact publisher spelling, passed
`make verify audit artefacts pricing releasable amazon`:
41 tests, zero content findings, print geometry and embedded-font checks,
rendered typography and safe-area checks, website checks and agreement across
all editions. EPUBCheck 5.3.0 reported zero errors or warnings. The regenerated
cover and affected interior pages, including all four worksheets, were visually
reviewed. The hardcover was also overlaid against the official template guides.
These local checks do not replace KDP's ingestion and previews.

The saved Kindle draft has the matching title, subtitle, author, first-edition
number, description and seven keywords. It records author-owned rights, no
sexually explicit content, no AI-generated content, no DRM, and publisher
HackerBay, Inc. No ISBN is assigned to Kindle. The linked paperback inherited
the matching title, author, description and keywords; its edition number is 1.
Amazon requested a fresh sign-in when opening the paperback content page after
saving its details. Neither format has been submitted for publication.

Amazon Kindle Previewer 3.107 was obtained from KDP's official download and its
Apple signature was verified. Its command-line startup produced no conversion
output in this environment, so Kindle conversion is not marked as validated.
Use KDP's online previewer during title setup before submission.

On 2026-09-09 the author confirmed that the original manuscript and artwork were
not AI-generated; AI helped with editing. Worksheets reformat existing manuscript
excerpts. Answer the current KDP disclosure form using this provenance.

## ISBNs

The live Bowker inventory was inspected on 2026-09-09 in the **HackerBay, Inc.**
account. The publisher field uses that exact spelling and is fixed; the imprint
dropdown has no custom entries.

| ISBN | Title / intended format | Observed status |
|---|---|---|
| 978-1-950600-00-7 | Simplified JavaScript | Existing incomplete record |
| 978-1-950600-01-4 | The 20-Minute Table | Already assigned to that title |
| 978-1-950600-02-1 | The 20-Minute Table | Already assigned to that title |
| 978-1-950600-03-8 | Back to Metal — Paperback | Submitted successfully; Pending |
| 978-1-950600-04-5 | Back to Metal — Hardback | Submitted successfully; dashboard verification pending |

The earlier inventory history incorrectly described the block's first two
numbers as belonging to *The 20-Minute Table*: that title uses **01-4 and 02-1**,
while **00-7** belongs to *Simplified JavaScript*. Kindle needs no ISBN.
Both print entries in `imprint.ISBN` now hold their submitted numbers. The hardcover
number was verified unused before the paperback record was cloned into it.

## Paperback metadata filed with Bowker — 2026-09-09

| Field | Value |
|---|---|
| Title | Back to Metal |
| Subtitle | How a company leaves the cloud, one move at a time |
| Contributor | Nawaz Dhandala — Author |
| Publisher | HackerBay, Inc. |
| Language | English |
| Copyright year | 2026 |
| Format | Print — Paperback |
| Pages | 76 |
| Dimensions | Inches; Length 11, Width 8.25; depth and weight left blank |
| Genre | COMPUTERS |
| Audience | Scholarly & Professional |
| Planned publication date | September 9, 2026 |
| Publication status | Forthcoming |
| US retail price | $11.99 |
| Front-cover image | Existing `dist/cover-kindle.jpg`, uploaded successfully |
| Dashboard result | Back to Metal / Paperback / Pending |

The planned publication date and Forthcoming status were filed metadata, not
evidence that an edition was released that day. The publication remains the
first edition, with author-owned copyright, CC BY 4.0 text and MIT software;
it is not public-domain content. These rights and edition statements remain
the metadata basis for the KDP setup.

## Hardcover metadata filed with Bowker — 2026-09-09

The paperback record was cloned into the verified unused ISBN
**978-1-950600-04-5**. Bowker confirmed
`Congratulations! Your form is complete and has been saved successfully!`
after submission. The record is submitted and awaiting Bowker processing;
the dashboard status has not yet been verified.

| Field | Value |
|---|---|
| Title | Back to Metal |
| Subtitle | How a company leaves the cloud, one move at a time |
| Description and short author bio | Same as the paperback filing, retained through Clone |
| Contributor | Nawaz Dhandala — Author |
| Publisher | HackerBay, Inc. |
| Language | English, explicitly set |
| Copyright year | 2026, explicitly set |
| Format | Print — Hardback |
| Pages | 76, explicitly set |
| Dimensions and weight | Left blank; the physical hardcover case has not been measured |
| Genre | COMPUTERS |
| Audience | Scholarly & Professional |
| Planned publication date | September 9, 2026 |
| Publication status | Forthcoming |
| US retail price | $33.99 |
| Front-cover image | Same `dist/cover-kindle.jpg`, uploaded with success confirmation |
| Submission result | Form saved successfully; dashboard verification pending |

The 8.25 × 11 in interior trim is not a filed hardcover case dimension. The
planned publication date and Forthcoming status do not establish a live edition.

## Description prepared for KDP

Back to Metal is a practical handbook for deciding whether to leave the cloud,
then moving workloads onto hardware you control. It covers AWS, Google Cloud and
Azure, with a common runbook and the extraction details that differ by provider.

Follow the stages Decide, Buy, Build, Move and Run. Compare costs, plan capacity,
choose colocation or rented hardware, build a platform for virtual machines or
Kubernetes, migrate state, rehearse recovery and establish ongoing operations.
Each Move states its prerequisites, risk, planned downtime, effort and rollback
limits. The figures are worked examples to replace with measurements from your
own systems.

Written by Nawaz Dhandala, founder of OneUptime. The book discloses that interest
where it recommends OneUptime. The text is licensed under Creative Commons
Attribution 4.0.

## Categories and keywords

Bowker's submitted genre is COMPUTERS. The saved KDP categories are:

- Kindle: Computers & Technology → Networking & Communications → Cloud Computing;
  Computer Science → Systems Analysis & Design; Operating Systems → Linux.
- Paperback: Computers & Technology → Networking & Cloud Computing → Cloud Computing;
  Operating Systems → Linux → Networking & System Administration and Servers.

Prepared search phrases:

- cloud repatriation
- leaving AWS
- Kubernetes bare metal
- self hosted infrastructure
- cloud exit strategy
- cloud cost comparison
- colocation planning

## Remaining submission work

1. Confirm the hardcover record's actual dashboard status and any Bowker processing updates.
2. Keep this record and `imprint.py` aligned with the filed metadata; inspect KDP
   for existing drafts before creating another.
3. Resume the saved KDP drafts after the fresh Amazon sign-in; create the linked hardcover.
4. Upload the validated 6.4.6 files with standard-colour paperback and premium-colour hardcover settings.
5. Inspect KDP's ebook and print previews.
6. Verify each marketplace's royalty, tax handling and .99 price. Automatic currency
   conversion may violate either the margin or the Kindle-to-print price relationship.
7. Submit all formats, record the actual statuses and add ASIN links once live.
