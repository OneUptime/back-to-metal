# Releasing

## Cutting a release

1. Bump `version` in `package.json`. Nothing else holds a version — `book/version.py` reads it,
   and it surfaces on the cover foot, in the colophon and in the website footer.
2. Add a `CHANGELOG.md` entry.
3. `make` — verify, audit, book, site. All clean.
4. Commit the regenerated `dist/` and `site/` along with the sources.
5. Merge to the `release` branch.

`EPUB_ID` in `book/imprint.py` must **not** change. It names the work, not the build: retailers
and libraries key on it, and a new string presents the next version as a different book.

## Publishing the website

The site lives in the **hackerbay-press** Firebase project, on a hosting site of its own
(`back-to-metal`), so it does not share a release history with anything else in that project.
`.firebaserc` maps the deploy target `book` to it.

**Preview first.** A channel deploy publishes to a temporary URL that expires, is not the
custom domain, and is not indexed. Use it for anything you would not want a stranger to read:

```bash
make site
firebase hosting:channel:deploy draft --only book --expires 30d
```

**Then promote.** Only when the content is real:

```bash
make site
firebase deploy --only hosting:book
```

Check what is currently public before and after:

```bash
firebase hosting:channel:list --site back-to-metal
```

### The custom domain

`backtometal.oneuptime.com` is served by this site. Adding it is a two-step dance and the
first step has to happen in the Firebase console, because the verification token is issued
there:

1. Firebase console → Hosting → the `back-to-metal` site → **Add custom domain** →
   `backtometal.oneuptime.com`. It issues a TXT record for verification and then two A records.
2. In Cloudflare, on the `oneuptime.com` zone, add the TXT record, wait for Firebase to verify,
   then add the two A records it gives you. Set those records to **DNS only** (grey cloud) —
   proxying through Cloudflare in front of Firebase's own edge breaks the certificate issuance
   and buys nothing, since Firebase already terminates TLS on a CDN.
3. Firebase issues the certificate. That takes minutes to a few hours.

Do not point the domain at the site until the site holds the real book. A custom domain is
indexed, and `oneuptime.com` is a company domain rather than a scratch one.

`firebase.json` serves `site/` as the public root, with HTML sent `no-cache` and assets cached
for an hour. Rebuild before deploying; do not deploy a `site/` that is out of date with `moves/`.

The site is a plain static directory — the fonts are embedded in the stylesheet and nothing is
fetched at runtime — so it drops onto any other static host unchanged.

## Before the first Amazon submission

These are the human steps the build deliberately will not take for you.

1. **Settle the page count.** Everything below depends on it, and it changes whenever a Move does.
2. **Measure the hardback case.** Open KDP's Cover Calculator at 8.25x11, the real page count,
   hardcover case laminate, premium colour, white paper. Fill `HC` at the top of `book/cover.py`
   with the sheet, panel, spine, turn-in and hinge it returns. Check
   `2*panel_w + spine + 2*wrap == sheet_w` before trusting it. `make covers` prints these
   instructions with your page count already in them.
3. **Read the print costs.** Open KDP's Printing Cost & Royalty Calculator for the same
   configuration and put the hardback figure in `imprint.HARDBACK_PRINT_COST_USD`. The per-page
   rates already in `INK` were verified for this trim on 2026-08-31 for a sibling title;
   re-read them.
4. **Set the list prices.** `make pricing` reports the minimum each edition needs to clear the
   25% target margin, and fails if a configured price misses it.
5. **Allocate and register the ISBNs.** The next free numbers in HackerBay's block are noted in
   `book/imprint.py`. Registering means entering real publication metadata at Bowker under a real
   account — do it by hand, then record what was filed in `PUBLISHING.md` and put the numbers in
   `imprint.ISBN`. The two records have to go on agreeing with each other.
6. `make amazon`. It runs verify, audit, the interior, both wraps, the Kindle edition and the
   margin gate, and refuses to finish if the hardback case is unmeasured or the economics do not
   work.
7. Run Adobe epubcheck and Kindle Previewer 3 against `dist/Back-to-Metal.epub`. The built-in
   `epubcheck.py` catches what breaks a Kindle conversion, but it is not a substitute.
8. Once the editions are live, put the ASINs in `imprint.AMAZON`. The website links to the
   product pages only when they exist, so nothing needs disabling until then.

## Ink and paper are permanent

A title cannot be moved between premium colour, standard colour and black-and-white after it is
published. The interior is type, rules and flat colour with no photographs, so `INK_CHOICE` is
`standard colour` — roughly half the per-page cost of premium, and the book loses nothing.
Hardcover is premium colour only; KDP does not offer standard colour for it.
