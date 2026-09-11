# Publishing

As of **2026-09-11 at 06:27 UTC**, the corrected version
**6.4.8 hardcover has been resubmitted successfully**. KDP confirmed
“Your hardcover has been submitted,” and the Bookshelf shows **In review**,
modified September 11. The corrected paperback remains **In review** from its
September 10 resubmission. The Kindle edition remains **Live**.

| Edition | KDP setup identifier | ISBN / ASIN | Last submitted US list price | Current status |
|---|---|---|---:|---|
| Kindle | `AZTAAK7S3HZ0G` | ASIN [B0HJB4M8NZ](https://www.amazon.com/dp/B0HJB4M8NZ) | $8.99 | Live; initial 6.4.7 upload |
| Paperback | `YHJP6H3BSP1` | ISBN 978-1-950600-03-8 | $11.99 | In review; corrected 6.4.8 resubmitted September 10 |
| Hardcover | `YHJP6H3BSP1`, linked hardcover setup | ISBN 978-1-950600-04-5 | $33.99 | In review; corrected 6.4.8 resubmitted September 11 |

All three formats were initially submitted successfully on **2026-09-09** using
version **6.4.7**. At 17:56 UTC that day, each appeared as In review and no ASINs
were displayed. This remains retail edition **1**. Kindle still uses the
initial 6.4.7 upload; the paperback and hardcover correction records below
identify their later 6.4.8 submissions.

## Hardcover margin correction — 2026-09-11

The author reported the same margin rejection for the hardcover. On September
11, KDP showed the hardcover as **Draft**, making its content editable. The
existing hardcover setup and ISBN were retained. Its interior and cover were
replaced with the exact public version **6.4.8** release files, which already
contain the shared margin correction described in the paperback record below.
No manuscript rebuild or new retail edition was needed.

### Corrected files uploaded to KDP

Both files were downloaded from the published 6.4.8 release and their sizes and
SHA-256 hashes matched GitHub's release metadata before upload. These hashes
identify the actual files in the **September 11 hardcover resubmission**.

| Uploaded asset | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| `Back-to-Metal.pdf` | Hardcover interior | 3,604,928 | `3d8c896880415b7aff565682a8de48e18611d411f0f5dc413e683053ace424ff` |
| `cover-hardback.pdf` | Hardcover cover | 221,334 | `6fb3a20a45ef9fcbbe385bc97c57666d2fee79a71d3feddfae473949d629809c` |

### File validation

The interior has **76 pages** with one consistent **603.12 × 810 pt** bleed page
box. The PDF check confirms embedded fonts and a flattened interior. An
independent scan of all **27,646 word boxes** found no text inside the 12.7 mm
PDF-edge safety floor. Minimum gutter/outside/top/bottom clearances were
**15.499 / 15.999 / 13.358 / 12.927 mm**. Pages **36–39** were rendered and
visually checked again: the fore-edge tabs contain colour only, and the text
and footers remain clear of the page edges.

The hardcover cover is one page, **1327.91992 × 894 pt**. Its dimensions differ
from the official KDP template geometry recorded in `book/cover.py` by less
than **0.031 mm**, within the build's geometry tolerance. Visual inspection
confirmed version **6.4.8**, the correct author and imprint, a blank spine and
an unobstructed **2 × 1.2 in** barcode reservation. KDP adds the barcode. Interior
copyright page 4 identifies **HackerBay, Inc.** and hardcover ISBN
**978-1-950600-04-5**.

At **06:22 UTC on September 11**, the PDF linked from the generated About page
was downloaded from [the public website](https://backtometal.oneuptime.com/Back-to-Metal.pdf).
It returned HTTP 200 and matched the hardcover interior upload byte for byte:
**3,604,928 bytes**, SHA-256 as recorded above.

### KDP preview, prices and resubmission

KDP preview **`6K4GF7AFMWQ`** confirmed **76 pages** and listed no issues.
It was approved at approximately **06:26 UTC** after checking the version
**6.4.8** cover and hardcover ISBN barcode **9781950600045**, with no overlap
in the reserved area. The previously rejected pages **36–39** showed
colour-only edge tabs and text inside the safety guides. The PostgreSQL spread
on pages **60–61** and worksheets on pages **72–73** were also inspected.

The saved settings remained **premium colour on white paper**, **8.25 × 11 in**,
**bleed**, and a **matte** hardcover. The owned ISBN **978-1-950600-04-5** and
publisher **HackerBay, Inc.** were retained. KDP adds the barcode; no
AI-generated content was declared, consistent with the author's provenance
statement. Worldwide rights remained selected.

All **12 hardcover marketplace rows**, including list prices, printing costs
and displayed royalties, exactly matched the **September 9 hardcover table**
preserved below. The Canadian row remained in **USD based on Amazon.com**.
The lowest displayed margin was Sweden: **SEK80.78 / SEK322.99 = 25.0101%**,
meeting the author's 25% target. The US list price remained **$33.99**.

At **06:27 UTC on September 11, 2026**, KDP confirmed
**“Your hardcover has been submitted.”** The subsequent Bookshelf state was
**In review**, with a September 11 modification date. This records successful
resubmission for Amazon's review; it does not establish that the corrected
hardcover is available for sale.

At that check, the corrected paperback remained **In review** from September
10, and Kindle ASIN **B0HJB4M8NZ** remained **Live** on the initial 6.4.7 upload.

## Paperback margin correction — 2026-09-10

KDP rejected the paperback because content on **PDF pages 36–39** was outside
the permitted margins. The earlier automated safe-area check excluded page
furniture, so it did not inspect the text in the fore-edge tabs. Passing that
check and approving the online preview did not establish that every text label
was inside KDP's safe area. An independent scan of the exact 6.4.7 public PDF
used for the initial submission found the same problem on all **40 Move pages**:
the only offending text was the stage labels in the edge tabs.

The source correction removes all 40 Move-page edge-tab labels while retaining
the colour bands. Footer text has also been moved farther from the PDF edge.
The new automated margin check measures every rendered text fragment, including
page furniture outside the main text area, transformed SVG labels and preserved
spaces. It checks both mirrored sides and the top and bottom edges, with a
conservative **12.7 mm (0.5 in) PDF-edge floor**. On edges carrying 3.175 mm
(0.125 in) bleed, that leaves 9.525 mm (0.375 in) inside the finished trim.
Thicker books also receive the larger KDP gutter minimum for their page count.

The rebuilt interior remains **76 pages**, preserving the existing facing
spreads. This shared interior correction also applies to hardcover. On September
10, the hardcover remained In review and its submitted file could not be replaced;
its later correction is recorded in the September 11 section above.

### Corrected files uploaded to KDP

The following **validated local version 6.4.8 files** were uploaded to the
existing paperback draft while GitHub CI/release was queued. Their exact sizes
and hashes identify the files in the **September 10 paperback resubmission**.
KDP's corrected preview was approved and submission succeeded at 11:54 UTC.

| Uploaded asset | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| `Back-to-Metal.pdf` | Paperback interior | 4,028,461 | `b1c72fd01fdfeed2e6b113d7f68f67d61f278d807c02abd55addb0d95fb22cee` |
| `cover-paperback.pdf` | Paperback cover | 257,789 | `9d8ab28e3f879e6320e3b2df9d51d8a4eff6766f0faba727a4a6024513eaa02b` |

These uploads use the corrected version 6.4.8 sources. The public release
assets are recorded separately below: PDF bytes can differ between Chromium
environments and because of timestamps even when source version, content and
geometry agree. The uploaded-file hashes above identify the actual KDP submission.

### Completed local validation

The local build passed **48 tests** and `make verify audit artefacts pricing
releasable amazon`. All eight browser print checks passed, including the new
regressions for fore-edge text outside the main text area, top/bottom page
furniture, both mirrored sides, rotated SVG text, preserved spaces and increased
gutter requirements for thicker books.

Browser measurement placed all **4,614 rendered text fragments** at least
12.7 mm from the PDF edge. A separate Poppler scan of the uploaded interior
checked all **76 pages and 27,646 PDF word boxes**, independently of the HTML
margin gate. It found zero text-margin or page-geometry failures at the same
stricter floor. Its minimum text-box clearances were:

| PDF edge | Minimum clearance |
|---|---:|
| Gutter | 15.499 mm |
| Outside | 15.999 mm |
| Top | 13.358 mm |
| Bottom | 12.927 mm |

All 76 pages were visually reviewed in contact sheets, with the rejected pages
36–39 inspected at larger size. No clipping, layout anomalies or unexpected
blank pages were found. Blank pages 22, 32, 42, 52 and 62 are intentional versos
before stage dividers; every Move still occupies its even/odd facing pair.
Worksheets on pages 72–75 and the colophon on page 76 were also checked.

The uploaded paperback cover was checked for version **6.4.8**, readable front
and back copy, its blank spine and the reserved barcode area. Its raster was
identical to the previously inspected version 6.4.8 cover. The 76-page standard
colour wrap is calculated as 16.921152 × 11.25 in with a 0.171152 in spine; the
rendered PDF is 1218 × 810 pt. Its width differs by 0.323 pt from the calculated
width, within the build's 0.5 pt geometry tolerance.

The generated About page now links to the confirmed live Kindle ASIN from
`imprint.amazon_url('kindle')`. It retains the EPUB download and omits the store
link when the ASIN is unset. Website checks passed on all seven representative
pages: no hidden content, screen/print contrast failures or sideways scrolling.
Live deployment verification is recorded in the release section below.

### Corrected KDP preview, prices and resubmission

KDP preview **`PSFWSJN70PA`** confirmed **76 pages** and listed no issues. It was
approved after checking the cover's version **6.4.8** and paperback ISBN barcode,
the originally rejected spreads on pages **36–39**, the PostgreSQL spread on
pages **60–61**, and the worksheets on pages **72–73**. No text remained in the
edge tabs; body text and the revised page furniture stayed inside the preview's
safety guides.

All **13 paperback marketplace rows**, including their list prices, printing
costs and displayed royalties, were checked after the replacement and exactly
matched the **September 9 paperback table** preserved below. Worldwide rights
remained selected and Expanded Distribution remained disabled. The lowest
observed margin was Canada: **CAD3.78 / CAD14.99 = 25.2168%**, satisfying the
author's 25% target. The US list price remained **$11.99**.

At **11:54 UTC on September 10, 2026**, KDP confirmed **“Your paperback has been
submitted.”** The subsequent Bookshelf state was **In review**, with a September
10 modification date. This establishes successful resubmission for Amazon's
review; it does not yet establish that the corrected paperback is available
for sale.

At the same September 10 check, Kindle ASIN **B0HJB4M8NZ** remained **Live** on
the original version 6.4.7 upload. The hardcover remained **In review** with its
September 9 modification date, and its editing controls were unavailable. No
replacement hardcover upload or resubmission had been performed at that time.

### Paperback correction status — 2026-09-10

| Correction milestone | Status |
|---|---|
| Source layout correction and all-text margin check | Complete; 76-page PDF passed independent geometry and text-box checks |
| Whole-manuscript and paperback-cover visual review | Complete; no issues found |
| Corrected paperback interior and cover upload | Complete; exact uploaded-file hashes recorded above |
| Corrected KDP preview | Approved; `PSFWSJN70PA`, 76 pages, no issues listed |
| Paperback prices and royalties after replacement | All 13 rows match September 9; minimum displayed margin 25.2168% |
| Paperback resubmission and resulting status | Confirmed at 11:54 UTC September 10; Bookshelf In review |
| Version 6.4.8 release and public asset hashes | Published and independently verified; evidence below |
| Live website agreement with the corrected release | Verified on both hosts, including canonical and cache-busted downloads |
| Hardcover replacement | Unavailable at the September 10 check; completed September 11 as recorded above |

The hardcover became editable after its later rejection. Its corrected-file
upload, preview and resubmission are recorded in the September 11 section above.

## Release 6.4.8 — verified 2026-09-10 at 12:33 UTC

[Version 6.4.8](https://github.com/OneUptime/back-to-metal/releases/tag/v6.4.8) was published at 12:32:37 UTC from `ba9b1f237843a1e7fe0700c8acd18df0d631cb2e`, the merge of [PR #8](https://github.com/OneUptime/back-to-metal/pull/8). [PR CI](https://github.com/OneUptime/back-to-metal/actions/runs/34472825323) and [main CI](https://github.com/OneUptime/back-to-metal/actions/runs/34473523398) passed.

The [Release build](https://github.com/OneUptime/back-to-metal/actions/runs/34474322538/job/102861337608) passed at 12:29:24 UTC. Its Publish job remained queued with no runner or executed steps, so it was cancelled at 12:31:26 UTC before direct publication with existing Firebase authentication. The exact checked `release-bundle` artifact (`10151899969`, ZIP SHA-256 `d15976dbbe1de175d665e70422ee73639eda0c321c6c838d3e000f3898b36242`) supplied all website files, release notes and edition files. Firebase CLI 15.29.0 deployed that bundle to the configured `backtometal` site; no content was rebuilt. The workflow therefore records a successful build and a cancelled Publish job, rather than a successful workflow deployment.

Every public asset was downloaded afresh and matched GitHub's published size and SHA-256, as well as the corresponding checked bundle bytes. The tag resolves to the merge commit above.

| Public release file | Bytes | SHA-256 |
|---|---:|---|
| `Back-to-Metal.pdf` | 3,604,928 | `3d8c896880415b7aff565682a8de48e18611d411f0f5dc413e683053ace424ff` |
| `Back-to-Metal.epub` | 200,957 | `ea17dffea587ecb86ea1ddd0b58bdc45f002c33aaaca03b8af79cdfc5c0d1f15` |
| `cover-paperback.pdf` | 221,279 | `fbc1dce6ead73be350b2efea7847049ea2c1f6472fd65b9b3f035ab99c1789ae` |
| `cover-hardback.pdf` | 221,334 | `6fb3a20a45ef9fcbbe385bc97c57666d2fee79a71d3feddfae473949d629809c` |
| `cover-kindle.jpg` | 151,186 | `2a63403323c404e3c33fa35090177bf46ce3aa5ec861c6e29871bb674b791eea` |

The released interior has 76 pages and 27,646 word boxes. Independent PDF checks found zero page-geometry or text-margin problems: minimum gutter/outer/top/bottom text clearances were 15.499 / 15.999 / 13.358 / 12.927 mm, all above the 12.7 mm floor. Fonts are embedded and the interior is flattened. Rendered pages 36–39 and both print covers retain the corrected layout with no clipping; the Kindle cover also passed visual review.

The September 10 paperback resubmission used the local files recorded above, whose bytes differ from this public release. A per-page comparison confirmed the same content in all 76 interior pages and the paperback cover, allowing PDF text emission and line-wrap differences; both versions passed their margin and visual checks. At the September 10 release check, the live Kindle edition and hardcover under review still used their initial 6.4.7 submissions. The September 11 hardcover resubmission uses the exact public 6.4.8 interior and hardcover cover identified in its correction record.

Both [the custom domain](https://backtometal.oneuptime.com/) and [Firebase Hosting](https://backtometal.web.app/) passed the final checks: all eight canonical/cache-busted PDF and EPUB downloads matched the release bytes, all sixteen page checks visibly showed v6.4.8, and both About pages displayed exactly one Kindle purchase link to [ASIN B0HJB4M8NZ](https://www.amazon.com/dp/B0HJB4M8NZ). No stale-cache, page-identity or link discrepancies were found.

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
observations; the paperback values were confirmed again after the September 10
correction. The hardcover values were confirmed again after the September 11
correction, as recorded above.

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
