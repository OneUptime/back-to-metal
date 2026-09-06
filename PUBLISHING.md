# Publishing

What has been filed, and where. This file and `book/imprint.py` have to go on agreeing with each
other and with the records at Bowker and KDP, so change them together — and by hand, never from a
build.

## Status

| | |
|---|---|
| Editions planned | paperback, hardcover, Kindle |
| Trim | 8.25 x 11 in, bleed on three edges |
| Interior ink | standard colour (paperback), premium colour (hardcover — KDP offers no alternative) |
| ISBNs | **not yet allocated or registered** |
| Amazon ASINs | **not yet published** |
| EPUB identifier | `urn:uuid:f021e81e-4b5f-4ecc-bc23-402193edac60` — minted once, never to change |

## ISBNs

Nothing is registered. The next two free numbers in HackerBay, Inc.'s own Bowker block (prefix
978-1-950600) are:

| Format | Number | Status |
|---|---|---|
| Paperback | 978-1-950600-03-8 | free, not allocated |
| Hardcover | 978-1-950600-04-5 | free, not allocated |

Check digits computed; the block's first two numbers went to *The 20-Minute Table*. Using
HackerBay's own block rather than a free Amazon ISBN keeps the publisher of record yours, and
means the book could be printed somewhere else later without new numbers.

When these are registered, record here: the date, the account, the exact title and subtitle
filed, the contributor name, the publication date, the format, the page count and the price. Then
put the numbers in `imprint.ISBN`.

## Metadata to file

| Field | Value |
|---|---|
| Title | Back to Metal |
| Subtitle | Leaving the cloud with Kubernetes |
| Author | Nawaz Dhandala |
| Publisher | HackerBay |
| Language | English |
| Edition | First edition |
| Copyright | 2026, Nawaz Dhandala |
| Licence | CC BY 4.0 (text), MIT (software) |

The licence is worth stating in the description: a CC BY book on Amazon is unusual enough that
readers ask, and the copyright page says it too.

## Categories and keywords

Not yet chosen. Candidates worth testing:

- Computers > Networking > Cloud Computing
- Computers > Systems Architecture > Distributed Systems
- Computers > Operating Systems > Linux
- Business > Industries > Computers & Technology

Keywords should carry the words people actually search: *cloud repatriation*, *leaving AWS*,
*Kubernetes bare metal*, *self-hosted infrastructure*, *cloud exit*, *cloud costs*, *colocation*.

## The free-book question

The whole text is CC BY 4.0 and the site publishes it in full, alongside the PDF and the EPUB.
That is deliberate and it does not have to be resolved before publishing: the paid editions sell
on being an object and on being ordered, not on being the only copy.
