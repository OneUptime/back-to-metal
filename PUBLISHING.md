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
in KDP before submission. The hardcover needs an official Cover Calculator
template for 8.25 × 11 in, 76 pages, case laminate, premium colour on white paper.
`HC` remains unset until those dimensions have been read; its cover is not generated.

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
| ISBNs | Not allocated or registered in this attempt |
| Print preparation | 76-page interior; hardcover template and KDP previews pending |
| Amazon ASINs | Not published |
| EPUB identifier | `urn:uuid:f021e81e-4b5f-4ecc-bc23-402193edac60` — never change |
| KDP Select | Do not enroll: the ebook is openly available elsewhere |
| DRM | Do not apply; the text is CC BY 4.0 |

No Bowker record or KDP draft has been created in this attempt. Chrome account
access failed with “Codex auth token is unavailable”; reconnection is pending.

The prepared files passed `make verify audit artefacts pricing releasable`:
41 tests, zero content findings, print geometry and embedded-font checks,
rendered typography and safe-area checks, website checks and agreement across
all editions. EPUBCheck 5.3.0 reported zero errors or warnings. The regenerated
cover and affected interior pages, including all four worksheets, were visually
reviewed. These local checks do not replace KDP's ingestion and previews.

Amazon Kindle Previewer 3.107 was obtained from KDP's official download and its
Apple signature was verified. Its command-line startup produced no conversion
output in this environment, so Kindle conversion is not marked as validated.
Use KDP's online previewer after browser access is restored.

On 2026-09-09 the author confirmed that the original manuscript and artwork were
not AI-generated; AI helped with editing. Worksheets reformat existing manuscript
excerpts. Answer the current KDP disclosure form using this provenance.

## ISBNs

The repository previously recorded these unused numbers in HackerBay, Inc.'s
owned block. Their current availability has not been checked in Bowker.

| Format | Candidate number | Status |
|---|---|---|
| Paperback | 978-1-950600-03-8 | Unverified inventory; not allocated |
| Hardcover | 978-1-950600-04-5 | Unverified inventory; not allocated |

The block's first two numbers were recorded as assigned to *The 20-Minute Table*.
Check the actual inventory before assigning either candidate. Kindle needs no ISBN.
After registration, record the account, filing date, exact metadata, publication
date, format, page count and price here, then set `imprint.ISBN`.

## Metadata to file

| Field | Value |
|---|---|
| Title | Back to Metal |
| Subtitle | How a company leaves the cloud, one move at a time |
| Author | Nawaz Dhandala |
| Publisher | HackerBay — verify the owned Bowker imprint spelling |
| Language | English |
| Edition | First edition |
| Copyright | 2026, Nawaz Dhandala |
| Licence | CC BY 4.0 (text), MIT (software) |
| Rights | Author-owned copyright; not public-domain content |
| Audience | Adult technical nonfiction |
| Publication date | Set during actual submission; not filed yet |

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

Select the closest available KDP categories to cloud computing, distributed
systems and Linux. No categories have been filed yet.

Prepared search phrases:

- cloud repatriation
- leaving AWS
- Kubernetes bare metal
- self hosted infrastructure
- cloud exit strategy
- cloud cost comparison
- colocation planning

## Before submitting

1. Restore the Chrome connection and inspect both accounts for existing records.
2. Register one owned ISBN per print format and update this record and `imprint.py`.
3. Read the official hardcover template dimensions into `cover.py`.
4. Regenerate all editions and the website; run `make amazon` and the agreement gates.
5. Run EPUBCheck on the final EPUB and inspect KDP's ebook and print previews.
6. Verify each marketplace's royalty, tax handling and .99 price. Automatic currency
   conversion may violate either the margin or the Kindle-to-print price relationship.
7. Submit all formats, record the actual statuses and add ASIN links once live.
