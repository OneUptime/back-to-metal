"""Publication details for the printed editions, and the economics of selling them.

The copyright page omits any field left empty rather than printing a placeholder,
so the book is always correct to print even while something here is unset. Several
fields below ARE unset on purpose - see the ISBN and Amazon notes.

The pricing figures below use the cited public large-trim rate tables.
`make pricing` checks page eligibility and margins; confirm the actual title
configuration in KDP's calculator before setting a price.
"""

import re

TITLE = 'Back to Metal'
SUBTITLE = 'How a company leaves the cloud, one move at a time'
AUTHOR = 'Nawaz Dhandala'
PUBLISHER = 'HackerBay, Inc.'
PUBLISHER_SITE = 'HackerBay.io'
YEAR = 2026
EDITION = 'First edition'
SITE = 'backtometal.oneuptime.com'
REPO = 'github.com/OneUptime/back-to-metal'

# Everything the title touches, derived from it. The title used to be spelled out
# in the two build scripts, four filenames and the website's masthead, which is
# exactly the drift the rest of this repository refuses to allow. Rename the book
# here and the artefacts, the download links and the wordmark all follow.
SLUG = re.sub(r'[^A-Za-z0-9]+', '-', TITLE).strip('-')
PDF_NAME = SLUG + '.pdf'
EPUB_NAME = SLUG + '.epub'

# The wordmark, broken where a designer would break it. The flagged line is the
# one set in the accent colour, on the cover, the title page and the masthead.
WORDMARK = [('Back to', False), ('Metal', True)]

# The imprint line. OneUptime is the author's company and the book recommends it,
# so this and DISCLOSURE below travel together: a reader who sees the byline can
# always find the interest declared. Printed on the cover, the title page, the
# back cover and the website.
BYLINE = 'By the makers of OneUptime'
ONEUPTIME_SITE = 'oneuptime.com'


def wordmark_html(sep='<br>', accent='em'):
    """The title as display markup, with the accented line wrapped."""
    return sep.join(f'<{accent}>{t}</{accent}>' if hot else t for t, hot in WORDMARK)

# --- identifiers -----------------------------------------------------------
# Set an ISBN only after its record exists in the owned Bowker account; builds
# never allocate one. The copyright page omits entries still left empty.
#
# Paperback 978-1-950600-03-8 was submitted on 2026-09-09 under HackerBay, Inc.
# Bowker's dashboard shows Back to Metal / Paperback / Pending. Hardcover
# 978-1-950600-04-5 was submitted the same day and its form confirmed a successful
# save; its dashboard was verified as Back to Metal / Hardback / Pending. These
# are submitted records, not confirmation of completed Bowker processing or KDP
# publication.
# In the same block, -00-7 belongs to incomplete Simplified JavaScript metadata;
# -01-4 and -02-1 belong to The 20-Minute Table.
# The exact filing and observed status are recorded in PUBLISHING.md.
ISBN = {
    'paperback': '978-1-950600-03-8',
    'hardback': '978-1-950600-04-5',
}

# The Kindle edition's publication identifier, for the EPUB's dc:identifier.
#
# Minted once, for this work, and never again. dc:identifier names the WORK, not
# the build: it has to stay byte-for-byte identical across every release, because
# retailers and libraries key on it and a new string presents the next version as
# a different book. So it is a literal here rather than something derived from
# the version or generated at build time - either would give every build a new
# identity and break reproducibility along with it.
#
# A random (version 4) UUID in URN form, which is what EPUB 3 asks for when no
# ISBN applies - and none does, since the Kindle edition has no ISBN.
EPUB_ID = 'urn:uuid:f021e81e-4b5f-4ecc-bc23-402193edac60'

# Set once the editions are live. Until then the website links to the repository
# instead of to a product page that does not exist.
AMAZON = {
    'paperback': None,
    'hardback': None,
    'kindle': None,
}
AMAZON_DP = 'https://www.amazon.com/dp/'


def amazon_url(edition):
    """The product page, or None while the edition is unpublished."""
    asin = AMAZON.get(edition)
    return AMAZON_DP + asin if asin else None


def on_amazon():
    return any(AMAZON.values())


# --- Kindle economics ------------------------------------------------------
# KDP charges a delivery fee per megabyte against the 70% royalty option, so file
# weight comes straight off the margin. This book is text and vector, so it is
# small; the figure matters far less here than on an illustrated title.
KINDLE_LIST_USD = 8.99          # also at least 20% below the paperback list
KINDLE_ROYALTY_RATE = 0.70
KDP_70_BAND = (2.99, 12.99)     # US
KDP_DELIVERY_PER_MB = 0.15      # USD, charged on the CONVERTED file size, which is
                                # NOT the EPUB size - measured once on a sibling
                                # title, a 4.23 MB EPUB converted to 4.56 MB, so
                                # an estimate taken from the EPUB runs light.
MIN_KINDLE_MARGIN = 0.25        # royalty after delivery, as a share of list price

# --- print economics -------------------------------------------------------
# KDP pays 50% below $9.99 and 60% from $9.99 on Amazon.com, minus print cost.
# Verified 2026-09-09: https://kdp.amazon.com/en_US/help/topic/G201834330
# On a colour book the page
# count sets the floor under the price.
#
# Public Amazon.com large-trim rates and page bands checked 2026-09-09:
# https://kdp.amazon.com/en_US/help/topic/G201834340 (paperback)
# https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H (hardcover)
# https://kdp.amazon.com/en_US/help/topic/G201834180 (trim/page eligibility)
# Premium colour has a fixed-price 24-40-page band before the per-page band.
# Confirm the actual title configuration in KDP before setting list prices.
#
# 8.25x11 is a LARGE trim (over 6.12in wide or over 9in tall), the more expensive
# per-page band. Ink and paper are locked permanently once a title is published:
# a book cannot be moved between premium colour, standard colour and
# black-and-white later.
PRINT_ROYALTY_RATE = 0.60
PRINT_LOWER_ROYALTY_RATE = 0.50
PRINT_60_MIN_USD = 9.99
MIN_PRINT_MARGIN = 0.25

# fixed cost, per-page cost - USD, Amazon.com, large trim
INK = {
    'premium colour':  (1.00, 0.0800),
    'standard colour': (1.00, 0.0402),
}

# KDP will not print outside these page-count bands, regardless of price.
# pricing.py checks eligibility against the built interior before its margins.
# (min pages, max pages), Amazon.com, large trim.
INK_PAGES = {
    'premium colour':  (24, 828),
    'standard colour': (72, 600),
}
HARDBACK_PAGES = (75, 550)
PREMIUM_SHORT_MAX_PAGES = 40
PREMIUM_SHORT_COST_USD = 4.20
# The interior is type, rules and flat colour - no photographs anywhere - so
# premium colour buys this book nothing it can use.
INK_CHOICE = 'standard colour'

# Hardcover is PREMIUM COLOUR ONLY. KDP's calculator rejects standard colour for
# hardcover, so the hardback cannot be made cheaper the way the paperback can.
HARDBACK_INK = 'premium colour'

# Publication prices prepared 2026-09-09 from the public KDP rates above, rounded
# up to .99 and checked by pricing.py against the built page count. Confirm the
# same costs in the live title setup before submission; PUBLISHING.md records
# whether that check and the submission have happened.
LIST_USD = {
    'paperback': 11.99,
    'hardback': 33.99,
}

# Hardcover, premium colour, large trim: $5.65 fixed plus $0.080 a page, read
# off KDP's own Hardcover Printing Cost table. It is a rate for the trim and the
# ink rather than for this title; pricing.py also checks the page-count band.
HARDBACK_FIXED_USD = 5.65
HARDBACK_PER_PAGE_USD = 0.080
HARDBACK_PRINT_COST_USD = None      # calculator override; otherwise use the rates above

# The content is CC BY 4.0, so the copyright page says that rather than the
# "all rights reserved" boilerplate, which would contradict the LICENSE files.
LICENCE = (
    'The text of this book, including every Move, is licensed under the Creative '
    'Commons Attribution 4.0 International licence. You may share and adapt it, '
    'including commercially, provided you give credit. The software that typesets '
    'this book is licensed separately under the MIT licence. Both are at ' + REPO + '.'
)

MORAL_RIGHTS = (
    'The right of ' + AUTHOR + ' to be identified as the author of this work has been '
    'asserted in accordance with the Copyright, Designs and Patents Act 1988.'
)

DISCLAIMER = (
    'Every runbook in this book changes production infrastructure, and several of '
    'them move data that cannot be recreated. Read the Rollback section before the '
    'first step of any Move, take a backup you have restored at least once, and '
    'rehearse against a copy. Prices, service names and product behaviour are those '
    'the author observed while writing and will drift; the figures in each Move are '
    'illustrative of the shape of a saving, not a quotation. Nothing here is legal, '
    'financial, security or compliance advice. You remain responsible for your own '
    'systems, your own data and your own obligations to the people whose data it is.'
)

# The book recommends a tool its author has an interest in. CONTRIBUTING.md
# demands that a contributor who works on a project they are adding says so, and
# that rule cannot apply to everybody except the author. Printed on the copyright
# page, in the colophon, and on the website's about page.
DISCLOSURE = (
    'Disclosure: the author founded OneUptime, which this book recommends for '
    'alerting, on-call, incidents and status pages. It is recommended because it is '
    'Apache-2.0 licensed, self-hostable, and does in one place what that Move would '
    'otherwise ask you to assemble from four separate tools. The alternatives named '
    'beside it are real ones, and a reader who prefers them loses nothing else in '
    'this book.'
)

TYPE_NOTE = (
    'Set in Archivo, drawn by Omnibus-Type, and JetBrains Mono, drawn by Philipp Nurullin and Konstantin Bulenkov. Both are licensed under the SIL Open Font License.'
)
