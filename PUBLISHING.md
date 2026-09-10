# Publishing

As of **2026-09-10**, KDP's Bookshelf shows **Kindle Live**, **paperback Draft**
after a margin rejection, and **hardcover In review**. The hardcover cannot
currently be edited while Amazon's review is in progress.

| Edition | KDP setup identifier | ISBN / ASIN | Last submitted US list price | Current status |
|---|---|---|---:|---|
| Kindle | `AZTAAK7S3HZ0G` | ASIN [B0HJB4M8NZ](https://www.amazon.com/dp/B0HJB4M8NZ) | $8.99 | Live |
| Paperback | `YHJP6H3BSP1` | ISBN 978-1-950600-03-8 | $11.99 | Draft; correction pending resubmission |
| Hardcover | `YHJP6H3BSP1`, linked hardcover setup | ISBN 978-1-950600-04-5 | $33.99 | In review; edits unavailable |

All three formats were initially submitted successfully on **2026-09-09** using
version **6.4.7**. At 17:56 UTC that day, each appeared as In review and no ASINs
were displayed. This remains retail edition **1**. Version **6.4.8** is being
prepared for the print-margin correction; no replacement submission is yet
confirmed. The live Kindle and the hardcover under review still refer to the
initial uploads until a later update is explicitly recorded.

## Paperback margin correction — 2026-09-10

KDP rejected the paperback because content on **PDF pages 36–39** was outside
the permitted margins. The earlier automated safe-area check excluded page
furniture, so it did not inspect the text in the fore-edge tabs. Passing that
check and approving the online preview did not establish that every text label
was inside KDP's safe area.

The source correction removes **all 40 Move-page edge-tab labels**, retaining
colour-only tabs and adding an automated margin check for all page text. The
rebuilt interior remains **76 pages**, preserving the existing facing spreads. This shared
interior correction also applies to hardcover; its submitted file cannot
currently be replaced while the format remains In review.

| Correction milestone | Status |
|---|---|
| Source layout correction and all-text margin check | Complete locally; zero text-margin violations across all 76 PDF pages |
| Version 6.4.8 release and exact asset hashes | Pending |
| Website agreement with the corrected release | Pending verification |
| Corrected paperback KDP upload and preview | Pending |
| Paperback prices and royalties after replacement | Pending confirmation against the September 9 observations below |
| Paperback resubmission and resulting status | Not yet confirmed |
| Hardcover replacement | Awaiting an editable KDP status |

The local build passed 48 tests and `make verify audit artefacts pricing
releasable amazon`. Browser measurement placed every text fragment at least
12.7 mm from the PDF edge. An independent scan of the generated PDF found no
violations of that stricter floor; its smallest glyph clearances were 15.499 mm
at the gutter, 15.999 mm outside, 13.358 mm at the top and 12.927 mm at the
bottom. Pages 36–39 were rendered and visually inspected after correction.

Record the released commit, exact asset sizes and SHA-256 hashes, final
margin-check results, KDP preview approval and actual resubmission confirmation
before marking this correction complete. Preserve the initial submission,
pricing and Bowker observations below as dated history.

## Initial release and website agreement — 2026-09-09

[Version 6.4.7](https://github.com/OneUptime/back-to-metal/releases/tag/v6.4.7)
was released from commit `bd4ffa27c3504f8e7bb13db17ec39634d6a5c746` after
[PR #6](https://github.com/OneUptime/back-to-metal/pull/6) merged. PR CI, main CI
and production release workflow `34380110575` passed. The September 9 KDP
submissions used these exact public release assets:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `Back-to-Metal.epub` | 200,902 | `f47de6e0da9ef9963dabfb760d123b664cb860c18b4bdfdcaf733faba9408db3` |
| `Back-to-Metal.pdf` | 3,606,789 | `a70330ba56002217a5637bbbca451561f4234ec64361e11da43faa4a5e9f8b25` |
| `cover-hardback.pdf` | 220,778 | `258693339f2f936994e8fce0f0530a208e63ffbe2e42d73db69ab8f0706accdf` |
| `cover-kindle.jpg` | 151,132 | `fccff7001cc1842d0174d3e42d9fba93a6dff3dbd2b471e4c6858a8dd1923b66` |
| `cover-paperback.pdf` | 220,722 | `553165ecdc79f76500d3c41217bf7a772772aaf9c16e573cac67c65061888ab2` |

The release passed 43 tests, `make verify audit artefacts pricing releasable
amazon`, the print geometry, embedded-font, flattening, typography and safe-area
checks, and agreement checks across editions. EPUBCheck 5.3.0 reported zero
findings. The public files were downloaded and independently checked against
their release sizes and hashes. Both print covers were visually inspected;
the hardcover was also checked against the official Cover Calculator guides.

The PDF and EPUB downloads on both
[backtometal.oneuptime.com](https://backtometal.oneuptime.com) and
[backtometal.web.app](https://backtometal.web.app) were byte-identical to the
corresponding release assets, with and without cache-busting parameters. The
five top-level website pages and sampled Move pages displayed version 6.4.7.

The interior has an even 76 pages. Four worksheets drawn from existing
manuscript material preserve the facing Move spreads and also appear in the
EPUB and website. Version 6.4.7 corrects literal HTML markup around “open source”
in the EPUB introduction. The EPUB identifier remains
`urn:uuid:f021e81e-4b5f-4ecc-bc23-402193edac60` and must never change.

## Metadata and settings submitted on 2026-09-09

| Field | Value |
|---|---|
| Title | Back to Metal |
| Subtitle | How a company leaves the cloud, one move at a time |
| Author | Nawaz Dhandala |
| Publisher | HackerBay, Inc. |
| Language | English |
| Copyright year | 2026 |
| Edition number | 1 |
| Rights | Author-owned copyright; worldwide publishing rights |
| Content rating | No sexually explicit content |
| Text licence | Creative Commons Attribution 4.0; not public-domain content |
| Software licence | MIT |
| Release choice | Available for sale upon publication; no preorder |
| AI-generated content | No |
| Kindle ISBN | None |
| KDP Select | Not enrolled; the ebook remains openly available elsewhere |
| Kindle DRM | Not applied |
| Kindle image accessibility declaration | Unknown; cover-image accessibility could not be confirmed |

On 2026-09-09 the author confirmed that the original manuscript and artwork were
not AI-generated; AI helped with editing. Worksheets reformat existing
manuscript excerpts. The no-AI-generated-content answers follow that provenance.

| Print setting | Paperback | Hardcover |
|---|---|---|
| Owned ISBN | 978-1-950600-03-8 | 978-1-950600-04-5 |
| Ink and paper | Standard colour, white paper | Premium colour, white paper |
| Trim | 8.25 × 11 in, custom entry | 8.25 × 11 in, KDP preset |
| Interior | Same 76-page bleed PDF | Same 76-page bleed PDF |
| Bleed | Top, bottom and outer edge | Top, bottom and outer edge |
| Cover | Matte paperback wrap | Matte case laminate |
| Barcode | KDP adds it in the reserved area | KDP adds it in the reserved area |
| Spine text | None | None |

The hardcover cover uses the official KDP Cover Calculator template downloaded
on 2026-09-09 for this trim, page count, binding, ink and paper. Its geometry is
recorded in `book/cover.py`. The interior trim is not the physical case size.

## Prices and margin observed on 2026-09-09

The author requested at least 25% margin, rounded upward to prices ending in
.99, or whole-currency amounts ending in 99 where KDP requires integers.
Margin is the share of list price retained after Amazon's deduction and
printing or delivery costs, excluding tax. The September 9 prices were saved
and displayed royalties checked before the initial submissions. Every observed
royalty exceeded 25% of its corresponding list price. These are dated KDP
observations; recheck the paperback after uploading the corrected interior.

Print prices exclude tax; Amazon's added tax can change the storefront ending.
Kindle fields include local tax where applicable. The saved Kindle prices use
a conservative check against numeric print list prices for the required 20%
discount under the
[70% royalty option](https://kdp.amazon.com/en_US/help/topic/G200634500).
The free edition remains available. Amazon can price-match it, including to
zero, so list-price margin is not guaranteed on every Kindle transaction.

### Kindle prices confirmed at submission — 2026-09-09

The table records KDP's displayed royalties for the final **6.4.7 conversion**,
confirmed immediately before submission. Its converted size was **0.24 MB**, with
a **$0.04 US delivery charge**. All 13 prices and royalties persisted unchanged
after the final replacement upload.

| Marketplace | Currency | Saved list price | Displayed royalty |
|---|---|---:|---:|
| Amazon.com | USD | 8.99 | 6.26 |
| Amazon.in | INR | 599 | 178 |
| Amazon.co.uk | GBP | 6.99 | 4.88 |
| Amazon.de | EUR | 7.99 | 5.21 |
| Amazon.fr | EUR | 7.99 | 5.28 |
| Amazon.es | EUR | 7.99 | 5.36 |
| Amazon.it | EUR | 7.99 | 4.56 |
| Amazon.nl | EUR | 7.99 | 5.11 |
| Amazon.co.jp | JPY | 1199 | 382 |
| Amazon.com.br | BRL | 31.99 | 11.20 |
| Amazon.ca | CAD | 11.99 | 8.36 |
| Amazon.com.mx | MXN | 152.99 | 53.55 |
| Amazon.com.au | AUD | 12.99 | 8.24 |

KDP required whole rupees, so the Indian price is INR599. Worldwide rights and
the 70% royalty option are selected. India, Japan, Brazil and Mexico receive
35% without KDP Select. Every observed royalty exceeds 25% of its displayed
list price.

### Paperback prices confirmed at submission — 2026-09-09

All final prices, costs and royalties persisted after the 6.4.7 replacement.
Worldwide rights are selected, royalties are 60% in all supported marketplaces,
and Expanded Distribution is disabled.

| Currency | Saved list price | Printing cost | Displayed royalty |
|---|---:|---:|---:|
| USD | 11.99 | 4.06 | 3.14 |
| CAD | 14.99 | 5.21 | 3.78 |
| JPY | 1599 | 548 | 411 |
| GBP | 8.99 | 2.90 | 2.49 |
| EUR | 9.99 | 3.41 | 2.58 |
| PLN | 45.99 | 15.97 | 11.62 |
| SEK | 110.99 | 36.42 | 30.17 |

The EUR entries cover Belgium, Germany, Spain, France, Ireland, Italy and the
Netherlands. Every observed royalty exceeds 25% of the tax-exclusive list price.
Standard-colour paperback is unavailable in Australia. Expanded Distribution
must remain disabled at these prices because its royalty rate is 40%.

### Hardcover prices confirmed at submission — 2026-09-09

These are the final KDP values, with 60% royalties in every displayed market.
Worldwide rights are selected.

| Marketplace / currency | List price | Printing cost | Displayed royalty |
|---|---:|---:|---:|
| United States / USD | 33.99 | 11.73 | 8.66 |
| Canada / USD, based on Amazon.com | 33.99 | 11.73 | 8.66 |
| United Kingdom / GBP | 24.99 | 8.71 | 6.28 |
| Euro marketplaces / EUR | 28.99 | 10.12 | 7.27 |
| Poland / PLN | 135.99 | 47.39 | 34.20 |
| Sweden / SEK | 322.99 | 113.01 | 80.78 |

The EUR entries cover Belgium, Germany, Spain, France, Ireland, Italy and the
Netherlands. KDP explicitly displayed the Canadian row in USD based on
Amazon.com, rather than as a CAD price. Hardcover distribution to Canada and
Australia uses Amazon.com; no local printing-cost table was available. Japanese
hardcover distribution was not available. The lowest displayed hardcover
margin is Sweden at approximately 25.01%.

Rates were checked on 2026-09-09 against KDP's
[paperback printing costs](https://kdp.amazon.com/en_US/help/topic/G201834340),
[hardcover printing costs](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H)
and [print royalties](https://kdp.amazon.com/en_US/help/topic/G201834330).
The 8.25 × 11 in format uses large-trim rates.

## Bowker filings — 2026-09-09

Both records were submitted successfully in the **HackerBay, Inc.** account.
Both dashboard entries were observed as **Pending** with the correct title
and format. The hardcover's saved registration was independently checked.
Pending describes Bowker processing; it does not establish a live Amazon title.

| Field | Paperback | Hardcover |
|---|---|---|
| ISBN | 978-1-950600-03-8 | 978-1-950600-04-5 |
| Format | Print — Paperback | Print — Hardback |
| Dashboard entry | Back to Metal / Paperback / Pending | Back to Metal / Hardback / Pending |
| Pages | 76 | 76 |
| Filed dimensions | Length 11 in, width 8.25 in; depth and weight blank | Dimensions and weight blank |
| Planned publication date | September 9, 2026 | September 9, 2026 |
| Publication status | Forthcoming | Forthcoming |
| US retail price | $11.99 | $33.99 |
| Front-cover image | Existing Kindle cover uploaded successfully | Same Kindle cover uploaded successfully |

Both filings carry the shared title, subtitle, author and publisher above,
English language, copyright year 2026, genre **COMPUTERS**, audience
**Scholarly & Professional**, and the same description and short author bio.
The publisher spelling is fixed by the Bowker account. Planned publication
dates and Forthcoming status are metadata, not proof of release on that date.

The hardcover record was cloned from the paperback into an ISBN verified unused
before registration. Other numbers in the block were left unchanged:
**978-1-950600-00-7** is the existing incomplete *Simplified JavaScript* record;
**978-1-950600-01-4** and **978-1-950600-02-1** belong to *The 20-Minute Table*.
Kindle has no ISBN. The ISBNs in `imprint.ISBN` match these submitted filings.

## KDP description submitted on 2026-09-09

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

## Categories and keywords submitted on 2026-09-09

Bowker's genre is COMPUTERS. The KDP categories are:

- Kindle: Computers & Technology → Networking & Communications → Cloud Computing;
  Computer Science → Systems Analysis & Design; Operating Systems → Linux.
- Paperback and hardcover: Computers & Technology → Networking & Cloud Computing
  → Cloud Computing; Operating Systems → Linux → Networking & System
  Administration and Servers.

The seven saved search phrases are:

- cloud repatriation
- leaving AWS
- Kubernetes bare metal
- self hosted infrastructure
- cloud exit strategy
- cloud cost comparison
- colocation planning

## Initial KDP preview evidence — 2026-09-09

The final 6.4.7 Kindle files completed processing and the manuscript check.
KDP's online preview showed “open source” correctly emphasized in the
introduction, with no literal HTML tags. Navigation was checked. The recovery
worksheet was inspected at tablet location 1292 and phone location 1291, with
clean layouts. No issues were listed. The separate spelling/image quality scan
was still running and is not recorded as completed. KDP accepted the submission
after these checks.

The initial paperback preview, `PSFWSJN70PA`, confirmed 76 pages and was approved.
The cover displayed version 6.4.7, with the paperback ISBN barcode inside its
reserved area. The cover and Move 05 spread at pages 34–35 appeared clean. The later rejection
identified pages 36–39; the initial checks did not detect the edge-tab text
margin issue.

The initial hardcover preview, `6K4GF7AFMWQ`, confirmed 76 pages and was approved.
The cover displayed version 6.4.7, with the hardcover ISBN barcode inside its
reserved area. The cover, PostgreSQL spread at pages 60–61 and worksheets at
pages 72–73 were clean.
