# Releasing

## Cutting a release

1. Bump `version` in `package.json`. Nothing else holds a version — `book/version.py` reads it,
   and it surfaces on the cover foot, in the colophon and in the website footer.
2. Add a `CHANGELOG.md` entry, and move anything sitting under `[Unreleased]` into it.
3. `make verify audit artefacts` — the gates, then the interior, the covers, the Kindle
   edition and the site, in that order. `artefacts` exists because the order matters:
   `site.py` copies the Kindle edition into `site/`, so the EPUB has to be built first or
   the website ships whichever one was committed last.
4. `make releasable` — the release gate. It is not part of `make`, because CI has to stay green
   while work is in progress and this is the one check that must not pass until it should.
5. Commit the regenerated `dist/` and `site/` along with the sources.
6. Merge to the `release` branch and push. **That is the release**: pushing to `release` runs
   `.github/workflows/release.yml`, which does everything below on its own.

`EPUB_ID` in `book/imprint.py` must **not** change. It names the work, not the build: retailers
and libraries key on it, and a new string presents the next version as a different book. The
release gate compares it against the previous tag and fails the release if it has moved.

### What `make releasable` checks

`book/release.py`, and every check is read out of a file in the repository:

- the version is a semantic version and is not `0.0.0` (which is what `version.py` returns when
  it cannot read `package.json` at all);
- `CHANGELOG.md` has a section for that version, and it is not empty;
- nothing is still filed under `[Unreleased]` — anything left there ships without being written
  down as part of anything, which is how a changelog starts lying;
- `EPUB_ID` has not moved since the previous release tag;
- the tag `vX.Y.Z` either does not exist or already points at this commit.

It also writes `build/release-notes.md` from the changelog entry, which is what the GitHub
release is made from. The notes are never typed twice.

## The pipeline

`.github/workflows/release.yml`. Two jobs, and nothing in either that a person could not do
from a laptop with the commands in this file.

**Build and check** runs `make verify`, `make audit`, `make releasable`, then
`make artefacts` in one invocation, then the same committed-site comparison CI
runs — releasing from a drifted commit would publish a site nobody reviewed. What it built is
handed to the second job as an artefact, so the bytes that get published are the bytes that
were checked.

**Publish** deploys `site/` to Firebase, fetches the page it has just published and fails
unless it is serving this version, and then cuts the GitHub release with the interior, the
Kindle edition, the paperback wrap and the Kindle cover attached. The hardback case is not
among them: `cover.py` will not guess its dimensions, so until `HC` is measured there is
nothing to attach. Re-running a release corrects it rather than failing on it.

Two ways to start it:

- **push to `release`** — publishes to the live site and cuts the release;
- **Actions → Release → Run workflow** — pick `preview` for an expiring channel URL that is not
  the custom domain and is not indexed, or `live` for the real thing.

The publish job runs in the `production` environment (or `preview`). Add a protection rule to
that environment in the repository settings if a release should need somebody to approve it
before it goes out.

### The deploy credentials

The workflow needs one repository secret to deploy, and takes either of two. Nothing else in
the pipeline needs a secret — the GitHub release uses the token the workflow is already given.

**`FIREBASE_SERVICE_ACCOUNT`** is the one to use. It holds the whole JSON key of a service
account scoped to the `back-to-metal` project with the **Firebase Hosting Admin** role, so a
leak costs you this project's hosting and nothing else. The Firebase CLI cannot mint one;
`gcloud` does:

```bash
gcloud iam service-accounts create back-to-metal-deploy \
  --project back-to-metal --display-name "Back to Metal release pipeline"

gcloud projects add-iam-policy-binding back-to-metal \
  --member "serviceAccount:back-to-metal-deploy@back-to-metal.iam.gserviceaccount.com" \
  --role roles/firebasehosting.admin

gcloud iam service-accounts keys create key.json \
  --iam-account back-to-metal-deploy@back-to-metal.iam.gserviceaccount.com

gh secret set FIREBASE_SERVICE_ACCOUNT --repo OneUptime/back-to-metal < key.json
rm key.json
```

Delete the local copy the moment it is in the secret; it is a long-lived credential to a
project that publishes under a company domain.

`firebase init hosting:github` mints the same thing through a browser if you would rather not
use `gcloud`, and sets the GitHub secret itself — but it names the secret after the project
(`FIREBASE_SERVICE_ACCOUNT_BACK_TO_METAL`) and offers to write workflow files of its own.
Rename the secret to `FIREBASE_SERVICE_ACCOUNT` and decline the workflows.

**`FIREBASE_TOKEN`** is the fallback, and it is one command:

```bash
firebase login:ci
```

It prints a token; paste that into a repository secret called `FIREBASE_TOKEN`. Understand what
you are pasting: it is a refresh token for **your whole Google account**, not for this project,
and `--token` is marked deprecated in the CLI and will be removed in some future major version.
Use it to get a release out, then move to the service account.

The workflow prefers the service account when both are set, and says in the log which one it
used.

## Publishing the website by hand

The pipeline above is the ordinary way. These are the same commands, for when you are deploying
something that is not a release — or when the pipeline itself is what is broken.

The book has a Firebase project to itself, **`back-to-metal`**, holding one hosting site,
`backtometal`, at `https://backtometal.web.app`. It used to be one site inside the imprint's
own project, sharing it with the imprint's website; it does not any more, so nothing this
repository publishes can reach anything but the book. `.firebaserc` maps the deploy
target `book` to that site, and both the project and the site name are read out of that file by
the workflow rather than written down a second time.

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
firebase hosting:channel:list --site backtometal
```

### The custom domain

`backtometal.oneuptime.com` is served by this site. Adding it is a two-step dance and the
first step has to happen in the Firebase console, because the verification token is issued
there:

1. Firebase console → the `back-to-metal` project → Hosting → the `backtometal` site →
   **Add custom domain** → `backtometal.oneuptime.com`. It issues a TXT record for verification
   and then the records to point at.
2. In Cloudflare, on the `oneuptime.com` zone, add the TXT record, wait for Firebase to verify,
   then point `backtometal` at `backtometal.web.app`. Set the record to **DNS only** (grey
   cloud) — proxying through Cloudflare in front of Firebase's own edge breaks the certificate
   issuance and buys nothing, since Firebase already terminates TLS on a CDN.
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
