# AGENTS.md

Working notes for coding agents on **Back to Metal**. Read this before editing anything.

## What this repo is

A technical handbook that is compiled, not laid out by hand. The markdown files in `moves/` are
the single source of truth; a Python toolchain in `book/` turns them into three artefacts:

- `dist/Back-to-Metal.pdf` — the print interior, 8.25x11 trim with bleed
- `dist/Back-to-Metal.epub` — a reflowable EPUB3 for Kindle
- `site/` — a static website with no build step and no external requests

Every number that appears in any output — page numbers, contents, Part totals, cutover sums,
the website filters, the planner, **and the count of Moves itself** — is derived from the Move
files. There are no hand-maintained totals anywhere, and no prose anywhere spells a total out:
`mission.py` takes the count as a parameter and the cover reads `len(moves)`. Change a Move,
rerun the build, and the rest follows.

## The one rule that matters

**Never hand-edit `dist/`, `site/` or `build/`.** They are generated. Change `moves/` or `book/`,
then rerun `make`. A diff that edits generated HTML directly will be overwritten by the next
build and is always the wrong fix.

`build/` is gitignored. `dist/` and `site/` are committed, so regenerate and commit them whenever
the sources change — otherwise the repo ships stale output.

## Build

```bash
make deps       # fonts, playwright, chromium
make verify     # structure — must be clean
make audit      # content — must be clean
make book       # markdown -> HTML -> PDF -> KDP check
make site       # markdown -> static site
make            # verify, audit, book, site
```

Requires Python 3.9 or newer with `playwright` and a Chromium build available to it. The
Makefile prefers `.venv/bin/python3` when it exists, so a project virtualenv works without
activating it. `make clean` removes `build/` and `site/`.

`make verify` and `make audit` are the gate. Both must report zero problems before you commit.

## Pipeline

```
moves/*.md
   |
   parse.py         markdown -> structured Move data
   |
   +-- build.py     -> build/book.html  -- render.py -> dist/*.pdf
   |
   +-- site.py      -> site/
   |
   +-- epub.py      -> dist/*.epub
```

Shared data modules feed **every** output, so edit them once and print, EPUB and web stay in
agreement:

| File | Owns |
|---|---|
| `book/deps.py` | which Moves must be finished before which |
| `book/kit.py` | the reference build, the laptop kit, the ten rules |
| `book/costs.py` | the cost model: AWS list prices, hardware, and the salary line |
| `book/rollback_data.py` | the general rollback and safety page |
| `book/equivalents.py` | AWS to GCP to Azure to what you run instead |
| `book/symptoms.py` | the symptom index — "which Move do I need" |
| `book/mission.py` | why the book exists |
| `book/icons.py` | Part glyphs, the cutover dial, the risk bars, the page-anatomy diagram |
| `book/imprint.py` | title, author, ISBNs, and the economics of selling it |
| `book/style.css` | print stylesheet |
| `book/web/` | site stylesheet and scripts |

The website is one page per question. `index.html` answers *what do I do next* and shows
exactly one Move; `checklist.html` is all the Moves in order with a tick box each;
`roadmap.html` answers *how long*; `plan.html` answers *what if we only do some of it*.
A figure belongs on the page whose question it answers, and nowhere else — which is why
the per-Move downtime, risk, effort and wait are on the Move page and inside the
checklist's opt-in figures strip rather than printed on all 122 rows. On a list, print a
fact only where it changes what the reader does: 110 of 122 Moves have no downtime, so
the twelve that do are worth saying and the 110 are not.

## Move file contract

`moves/NN-slug.md`, numbered contiguously from `01`. `verify.py` enforces all of the following
and fails the build otherwise:

- Exactly one H1: `# NN · Title`. Titles must be unique across the book, **and so must
  the slugs they reduce to** — the website writes one page per slug, so two Moves that
  slug alike silently overwrite each other. `verify.py` checks both; `site.py` asserts
  the second where the damage would happen.
- A meta line matching exactly, `·`-separated:
  `**Layer:** X · **Leaving:** Y · **Risk:** Low|Medium|High · **Cutover:** N min · **Reversible:** Z`
  where `Reversible` is `No`, `Immediately`, or `N days` / `N hours`.
- `Cutover` is user-visible downtime in minutes and is **never above 60** — the dial's cap.
  Past an hour it is not a cutover window, it is an outage, and the Move should be split.
- A one-line `> hook`, at most 170 characters.
- H2 sections, exactly these and in this order:
  `Leaving from`, `Why this works`, `Before you start`, `The runbook`, `Operator's notes`,
  `Rollback`, `The numbers`, `What you can turn off`.
- **`Leaving from` is exactly three lines, one per cloud, in this order:**
  ```
  - **AWS:** Service name — what differs there, concretely.
  - **Google Cloud:** Service name — what differs there, concretely.
  - **Azure:** Service name — what differs there, concretely.
  ```
  The separator is an em dash with a space either side. The service name is at most 62
  characters; the half after the dash must be a real technical difference an engineer would
  trip over — a flag that needs a reboot, a tier that cannot do it at all, a quota, a
  different export mechanism, a resource that outlives its parent — and at least four words.
  No two clouds may be given the same service name. If a provider genuinely has no
  equivalent, name what people use there instead.
- 3–9 numbered runbook steps.
- `Operator's notes` contains all four labels: `**Swap:**`, `**Do it faster:**`,
  `**Watch out:**`, `**Leftovers:**`.
- `Rollback` is 30–140 words and **must contain the phrase "point of no return"**.
- If `Reversible` is `No`, the rollback must say so plainly (`irreversible`, `no way back`,
  or `cannot be undone`).
- **If a Move moves persistent state, its rollback must mention restoring it.** This is the one
  failure in this book that would cost somebody something, so it is a build error rather than a
  review comment.
- `The numbers` is a six-cell strip, `| Was | Now | Saved | Cutover | Effort | Wait |`. The
  `Saved` percentage must equal `(Was − Now) / Was` within one point, and the `Cutover` cell must
  equal the meta line exactly.
- **`Wait` is not `Effort`, and conflating them is the mistake that made the first roadmap wrong
  by two quarters.** Effort is somebody's labour; wait is calendar time that has to pass before a
  dependent Move can start — a thirty-day sampling window, a six-to-twelve-week circuit order, an
  RIR queue, a procurement cycle. Nobody is working during it. `roadmap.py` adds wait to the
  critical path and *not* to the person-day budget, and frees the engineer after the labour, so a
  Move that is "four days of work spread across a thirty-day window" no longer lets the next Move
  start on day five. Write `—` when there is none; a range like `6 to 12 weeks` is allowed and the
  scheduler takes the pessimistic end.
- `Reversible` is a short label, at most 52 characters, not a sentence. **`No` is reserved**: it is
  what marks a Move irreversible everywhere else in the build. Anything else is free text, because
  the enum this used to be was too narrow for real content — "Until the order is signed" and "Per
  drive, at the cost of a Ceph rebuild" are better answers than a fixed vocabulary allows.

## Parts are stages

Each Part carries a `stage` number, a `doing` verb and a `done` line in `parse.py`, and both
outputs lead with them. The Part names are nouns from the system diagram — Iron, Site, Cluster —
which is how an architect thinks about an estate and not how somebody halfway through the work
thinks about their week. "Stage 4 · Make it fit to run production" answers *where am I*; "Part IV
· Platform" does not. The website's checklist page is built on them, and its front
page names the stage the Move it is recommending belongs to.

## Three clouds, one runbook

The book covers AWS, Google Cloud and Azure equally. The *job* is the same whichever you are
leaving; only the extraction differs, so only the extraction is written three times. That is
what the `Leaving from` block is for, and it is why the runbook itself is written once and
cloud-neutral, with per-provider specifics called out inside a step where they matter.

Two consequences worth stating, because both are enforced:

- **A Move title may not name one provider's product** unless the name is a genuine
  cross-vendor standard. The S3 API, BGP, OIDC and NUMA qualify; RDS, Lambda, ElastiCache and
  CloudWatch do not. `**Leaving:**` on the meta line is the generic category —
  "Managed PostgreSQL", not "RDS for PostgreSQL".
- **Service names are spelled one way across the whole book**, on all three clouds.
  `audit.py` carries the canonical list and checks every occurrence, not just the first.
  In particular the book writes "Google Cloud" and never "GCP".

## House style

Enforced mechanically — a build failure, not a preference:

- **No exclamation marks** in prose. Fenced code and inline spans are exempt.
- **Banned:** seamless, effortless, blazing, game-changer, leverage, unlock, revolutionary,
  painless, silver bullet, best-in-class, cutting-edge, turnkey, synergy, **simply**,
  "easy as", "no time at all", "in a nutshell".

  *Simply* is banned outright and deliberately: if a step is simple it does not need saying, and
  if it is not, the word is a lie told to somebody about to move a production database.

And these are conventions `audit.py` enforces:

- Every tool a runbook invokes must be declared in `Before you start`, and everything declared
  there should get used. Same rule as an ingredient list.
- A destructive step (`rm -rf`, `DROP`, `terraform destroy`, `--force`, a delete) must carry a
  guard in the same step: a backup, a verification, a precondition, or a reference to the rollback.
- Anything installed must pin a version. A runbook that does not reproduce is not a runbook.
- Service names on all three clouds are spelled one way across the whole book; `audit.py`
  carries the list and checks every occurrence.
- Risk and cutover must agree: over 15 minutes of downtime is not Low risk, and a Move you
  cannot undo is High by definition. There is deliberately **no** rule against "High risk,
  reversible immediately" — that is not a contradiction but the best kind of Move. Turning
  off kube-proxy breaks every service in the cluster if it goes wrong and is undone by
  reverting one flag. Risk is blast radius; reversibility is the way back; they are
  independent.
- If a Move costs *more* after the change, the hook or `Why this works` has to say so.
- No sentence copy-pasted between Moves; `audit.py` flags repeated prose and repeated hooks.
- Plain, declarative voice. Describe what happens to the system and why, not how good it feels.

## The dependency invariant

`book/deps.py` maps each Move to the Moves that must be finished first. **Every dependency must
be a lower-numbered Move.** That is what makes the book readable front to back — a reader who has
reached Move 40 has, by construction, met every prerequisite of Move 40 — and it makes a cycle
impossible to express. `audit.py` fails the build on a forward or missing dependency.

Because of it, book order is already a valid execution order, which is why the website's planner
can "sort" a selection rather than topologically searching it.

Keep the map minimal and true. If Move B would work without Move A, they are not related, however
much they rhyme.

## The design

The visual language is a technical datasheet crossed with an operations checklist, not an
editorial one. That is a decision with consequences you should not undo casually:

- **Two families, both variable.** Archivo carries every word — condensed and heavy for
  display, normal for text — and JetBrains Mono carries every number, label and identifier.
  There is no serif anywhere. Use the `standard` cut of Archivo, not `wght`: the display
  voice is built on the width axis, which the `wght` cut does not carry.
- **Hairline rules, never boxes.** No rounded corners, no shadows, no tinted cards, no pills.
  A panel is a rule and some space.
- **Colour is a signal.** One colour per Part, used in the fore-edge tab, a rule, and a
  numeral. Never as a decorative fill.
- **The fore-edge tab** steps down the page by Part index, so the closed book shows a band
  per Part. It must not carry a CSS `transform`: a transform makes Chromium emit a
  transparency group and `kdpcheck.py` will fail the build.
- **The cutover is a gauge, not a dial**, and step numbers are mono ordinals in a ruled
  gutter, not discs.

## Print geometry

The book is typeset for Amazon KDP at **8.25in x 11in trim**, the only size in KDP's catalogue
that is both a standard hardcover trim and reachable as a paperback. One interior serves both
print editions.

**The page box carries bleed.** `.page` is `8.375in x 11.25in` — trim plus 0.125in on the top,
bottom and outer edge. The gutter never carries bleed.

**Margins are mirrored, and the side comes from the page index.** `build.py` stamps
`data-side="recto|verso"` when it numbers the pages; the CSS keys the mirrored `.inner` padding
and the folio off that attribute. Never derive the side from `:nth-of-type()` — divider and blank
insertions make the DOM index wrong.

**Pagination invariants, asserted in `build.py`.** A facing pair in a bound book is
(even verso, odd recto), so every Move's setup page must be even and its runbook page the next
one, or the two-page spread the whole design rests on is split across a page turn. The build
asserts this for every Move, that each Move's contents entry matches where its setup page lands,
and that the total page count is even — KDP appends an uncontrolled blank otherwise. Front matter
runs to 18 pages so the first Part divider opens on a recto.

**Never write `rgba()`, `opacity`, or an eight-digit hex.** KDP requires a flattened interior.
Every alpha in this book is one known colour over one known backdrop, so it is pre-composited at
build time with `flatten.mix(fg, bg, alpha)`. Flattening downstream with Ghostscript instead would
rasterise those regions and turn an all-vector book into a mixed one. `make kdp` fails the build
on any transparency group, soft mask, sub-1 alpha operator, wrong page box or odd page count.

**Vertical justification.** `render.py` binary-searches one parameter per page that expands or
tightens leading, panel padding and — on the densest pages — body size, until content sits 4.5 mm
above the footer. **Every lever's baseline `b` must match what `style.css` actually sets.** The
first `apply()` writes all levers at once, so a baseline that disagrees makes the page jump
before the search has done anything. If you change a spacing value in the stylesheet, change it
in `render.py` too. Long prerequisite lists switch to a two-column panel automatically. If you add a
Move with an unusually long runbook, **check the PDF**, not just that the build exited zero: the
justifier will do something to make it fit, and you want to confirm the something is reasonable.

## The recommendation the book has an interest in

Part VII recommends OneUptime for alerting, on-call, incidents and status pages. The author
founded it. CONTRIBUTING.md already requires a contributor who works on a project they are
adding to say so, and that rule cannot apply to everybody except the author, so
`imprint.DISCLOSURE` states the interest and is printed on the copyright page, in the
colophon, in the EPUB and on the website's about page. `imprint.BYLINE` carries the imprint
line on the cover, the title page and the back cover.

If you change the recommendation, change the disclosure with it. If you remove the
recommendation, remove the disclosure. They travel together, and a byline without a
declared interest is the one thing here that would cost the book its credibility.

## The unset fields, and why

Several things in `book/imprint.py` are `None` on purpose. The copyright page omits an empty
field rather than printing a placeholder, so the book is always correct to print as it stands.

- **ISBNs.** Registering one means entering real publication metadata under a real Bowker
  account. That stays a human step and never happens from a build. The next free numbers in
  HackerBay's block are noted in the file; fill them in only once the records exist.
- **List prices and the hardback print cost.** `make pricing` computes the minimum each edition
  needs to clear its target margin and fails if a configured price misses it, so a submission
  bundle cannot be prepared with economics that do not work. It stays out of CI, because an
  unmade business decision should not turn the build red.
- **The hardback case dimensions (`HC` in `cover.py`).** KDP publishes no hardcover formula and
  defers to its own Cover Calculator; the case is materially larger than the paperback wrap in
  both axes. `make covers` prints the exact numbers to feed the calculator and skips the case;
  `make amazon` refuses to finish without it. Do not compute the case from the paperback wrap.

The AWS and KDP figures in `costs.py` and `imprint.py` are dated observations, not quotations.
`imprint.py` says which were verified, when, and against what.

## Adding or changing a Move

`docs/exemplar-move.md` is the reference for voice, shape and density. It is a complete Move
that satisfies the whole contract, kept outside `moves/` so it is not part of the book. Read it
before writing one.

1. Copy `docs/exemplar-move.md`, or an existing file in `moves/`, as the template — the
   contract above is unforgiving.
2. Number it next in sequence; keep numbering contiguous, and keep the Parts in contiguous blocks.
3. Add its prerequisites to `book/deps.py`, all of them lower-numbered than the Move itself.
4. `make verify && make audit` — both clean.
5. `make` to regenerate, then eyeball the affected spread in `dist/Back-to-Metal.pdf`.
6. Commit the sources **and** the regenerated `dist/` and `site/`.

Renumbering existing Moves is expensive: it changes filenames, the dependency map, the symptom
index and every cross-reference. Prefer appending within a Part.

## Versioning and releases

`package.json` holds the version and nothing else does. `book/version.py` reads it, and it
surfaces in the book cover foot, the colophon and the website footer. Never hardcode a version
anywhere else — in particular, `EPUB_ID` must stay byte-identical across releases, because
retailers key on it and a new string presents the next version as a different book.

## Continuous integration

`.github/workflows/ci.yml` runs `make verify`, `make audit`, then a full book and site build on
every push and pull request. It also fails if the committed `site/` does not match what the
sources generate — that check is what stops a Move change landing without its regenerated output.
The PDF is excluded from that comparison because Chromium stamps a creation date into it, so it
is not byte-reproducible. The HTML is.
