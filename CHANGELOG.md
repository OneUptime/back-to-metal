# Changelog

All notable changes to this book are recorded here. The version lives in `package.json` and
nothing else; `book/version.py` reads it.

## [Unreleased]

### Added

- **A fourth gate, `book/agree.py` and `make agree`.** The same figures are
  published by three different renderers into a website, a printed interior and
  a README, and the saving can honestly be divided by two denominators — the
  bare cloud bill, or that bill with the cloud's own operations time in it.
  Both are true; only one can be the headline. It has been divided by the wrong
  one **three times, in three files** — `costs.py`'s self-test printing 79 per
  cent against the site's 56, `readme.py` printing 50 against 36, and
  `build.py` one edit away from the same — and every one was caught by somebody
  reading two outputs side by side, which is not a method. This reads the built
  artefacts rather than the model (the model agreeing with itself was never in
  doubt; the failure was a caller doing its own arithmetic on the way to the
  page), pulls eight figures out of each, and fails if they disagree. Confirmed
  against the bug: reinstating `readme.py`'s bare-bill denominator makes it
  fail with `the headline percentage: DISAGREE - 36 in index.html; 50 in
  README.md`.

## [5.0.0] - 2026-09-08

The reference estate is $10,000 a month, not $24,000. Every figure in the book
is a slice of that bill, so every figure moved; the fleet is three machines and
a spare rather than five and a spare; and the exercise surfaced two errors and
one question the book had never answered.

### Changed — the estate

- **`BILL_MONTH` is $10,000.** It is not one constant: eleven Moves state a
  "Was" and they sum to the bill, which is what makes the arithmetic
  checkable. All eleven were re-derived line by line rather than multiplied,
  because the lines do not scale together — a managed control plane is $73 at
  any size, a load balancer and a Multi-AZ database have floors, and egress and
  object storage scale with traffic and data. The Was column sums to $10,003.
- **The reference build is 3 nodes + 1 spare**, 96 cores and 768 GB, down from
  5 + 1. Move 06 is retitled and says the honest thing about it: three is a
  quorum and losing one costs a **third** of the capacity rather than a fifth.
  At twice the bill you buy five and a dead machine costs twenty per cent. The
  smaller fleet is the floor, not the comfortable answer.
- **New headline: $4,967 a month, $59,604 a year, 36 per cent** of the loaded
  bill, 63 per cent of the infrastructure line.

### Fixed

- **The ops hours were absolute constants and had to scale with the estate.**
  Holding 60 and 80 while the bill fell 58 per cent left the same person
  running half the services, and it was the difference between the book
  clearing its own decision rule and failing it: at 60/80 owned lands 29.1 per
  cent under cloud, and Move 03 requires a third. They are 40 and 55 — the
  cloud figure falls by a third rather than a half because somebody still
  upgrades the cluster and rotates the credentials whatever its size, and the
  delta falls from 20 to 15 because it is driven by the machines and there are
  four of them now.
- **`readme.py` printed 50 per cent where the site printed 36**, because it
  divided the saving by the bare bill while the site divides by the bill with
  the cloud's own operations time added. Third occurrence of the same
  two-denominators bug; it now uses the loaded framing like everything else.
- **The "when to stay" threshold contradicted the new reference estate.** It
  said the saving stops being worth the distraction below about ten thousand a
  month, which is exactly where this edition now sits. The real break-even is
  about **nine thousand** — the quarter rack costs $1,400 whether it holds
  three machines or thirty, so the saving falls faster than the bill — and the
  item says that, with the arithmetic, rather than a round number.

### Added

- **Why there is no hypervisor.** The book went from EC2 to Kubernetes on the
  metal without once mentioning Proxmox or KVM, which is the first question
  anyone arriving from EC2 asks. Move 11 answers it — you are not moving
  virtual machines, and a hypervisor under a container platform is a second
  control plane bought for a problem this estate does not have — with a Swap
  naming the three cases where it is the right call.
- **The rent-versus-own comparison no longer picks a winner.** The margin was
  $249 a month, one per cent, and it flips on two inputs the model marks as not
  re-verified. Sweeping both across their defensible ranges puts owning ahead
  in three of four combinations. The book now says the two are level at this
  size, names the numbers that decide it, and tells the reader to break the tie
  with their own quote.
- **Why owning is booked as dearer at all**, written down rather than implied:
  every first-hand account says the delta is nought, the only non-zero estimate
  is an outside ten to twenty hours, and the book takes twenty. It is the book
  declining the most favourable reading of its own evidence, not a finding that
  a rack is harder work than an invoice. The same note explains why the cloud's
  own hours are booked generously: the dollar saving cancels them, so a larger
  cloud figure only makes the headline percentage smaller.

## [4.1.1] - 2026-09-08

The printed interior had content hanging off three pages, and the check that
should have stopped it was printing a warning and building the book anyway.

### Fixed

- **`render.py` reported overflowing pages and did not fail on them.** It
  computed the list, printed it, and wrote the PDF regardless — so 4.0.0 and
  4.1.0 both shipped a cost page with **165px of the five-year table hanging
  off the bottom**, and the only evidence was a line of output nobody read. A
  check that reports and does not gate is a check that has already failed. It
  raises now, and `make book` stops.
- **Three pages were running off**, all of them introduced by the last two
  releases: the cost page (165px), the new case-for-leaving page (50px) and
  Move 13's setup page (6px). The five-year comparison now has a page of its
  own, the case for leaving is a two-page spread with the costs facing the
  gains, and Move 13's operator note is shorter. Zero overflowing pages, and
  the body-to-footer slack is back to a healthy 4.5mm minimum from 0.
- **The case for leaving is in the printed book at all**, which it was not.
  4.0.0 added it to the website and stopped there, so the question the book
  now answers on its front page went unanswered in the artefact people pay
  for. It is a spread: the five gains with their disproofs on the recto, the
  four costs and the four reasons to stay on the verso — so a reader has to
  turn past the costs to reach the Moves.

### Changed

- **The paperback is printable.** At 72 pages the interior clears KDP's
  72–600 standard-colour band, which it missed by four at 68. It now needs
  only a list price: $11.13 or more to clear the margin. The hardcover is
  three pages short of its own 75-page minimum. `PUBLISHING.md` carries both.

## [4.1.0] - 2026-09-08

The overhaul the last three editions were painting over. 4.0.0 changed the
colour and the content; this changes the shape.

### Changed — the layout

- **The ledger grid.** Measured at 1440 before it existed: the content box was
  1056px and every paragraph in it ended at 527px, with a two-pixel rule drawn
  straight across the rest — a rule whose whole job is to measure the column,
  measuring twice what was under it. Five hundred pixels of dead column beside
  every paragraph on the site, on every page, which is why three editions of
  new paint kept looking like the old one. There are two tracks now: the
  ACCOUNT carries the argument, the AMOUNTS carry what the argument is about —
  figures, the stage key, cross-references, and the marginalia that used to
  interrupt the prose. They sum to the content box exactly (544 + 96 + 416 =
  1056), so `--page` does not change and every full-width object keeps the
  width it had. A section with nothing for the margin says `.solo` and
  collapses: a page of pure argument is allowed to be one column, a ruled-off
  empty gutter is not. Verified at 1440, 1080 and 390 with no horizontal
  scroll at any of them.
- **The front page opens with the balance, not a stat strip.** Four equal
  figures at one size in one colour, on a page whose argument is one figure —
  three of them were context and the fourth was the claim. It is a ledger now,
  read down as a subtraction: the bill struck through, the three lines that
  replace it, the total, and the saving at the only type size on the site that
  large. It adds up, because the parts are the rounded parts and the total is
  their sum.
- **A real type scale.** There were `--t-body` 17, `--t-item` 17 and
  `--t-item-lg` 19 — three names within two pixels, which is not a hierarchy.
  A census found 12px used 97 times, 15px 84 times, 17px 65 times, and nothing
  at all between 28px and the masthead. Five prose steps now, four for
  amounts, and Archivo's width axis used as a real third dimension: a row
  title at `wdth 92` beside a hook at 100 is a different kind of statement,
  which is hierarchy that costs neither size nor weight.

### Changed — the argument

- **The case for leaving leads with the stake**, not with a list. What the
  saving is in things a company actually spends: two engineers, or a year of
  runway, or the difference between raising again and not.
- **We say what we did, in the first person.** 730 days at 99.993 per cent,
  19 per cent lower latency on identical software, two hardware interventions
  in twenty-four months, nobody hired. It is our own fleet and our own
  measurement rather than an independent audit, and the section says so —
  which is the point. It is the one thing on the site nobody else could write.
- **Every claim carries the test that would disprove it.** A page that tells
  the reader how to prove it wrong is not selling them anything, and this
  audience believes a falsifiable claim and distrusts a confident one. Most of
  the tests point at a Move.
- **"Startup" is "company" throughout**, including the subtitle and the cover.
  The book is sized for an estate, not for a funding stage.
- **The mark is on it.** OneUptime's logo, vendored and recoloured for a dark
  ground, in the footer where a publisher signs its name. Its green is
  `#7ED957` — byte-identical to the accent this edition chose independently,
  on contrast and collision grounds, before anybody looked at the logo.

### Fixed

- The comparison table stopped adding up the moment the cloud column gained
  its people row: it printed $24,000 under a column whose visible rows came to
  $29,491. Every column is the sum of its own rows again.

## [4.0.0] - 2026-09-08

The arithmetic was wrong in the book's own favour's opposite direction, the
accent was the same colour as one of the five Stages, and the one question
every reader arrives with had no answer anywhere. Headline figures moved, so
this is a major version.

### Fixed — the cost model

- **Half an extra engineer was a guess sitting in the load-bearing position.**
  It was 0.5 FTE, $7,917 a month, fifty-nine per cent of the whole owned
  column — about eighty-seven engineer-hours a month of incremental work on
  six machines, for ever. Nothing published supports it at this fleet size.
  The independent estimate of the delta is ten to twenty operations hours a
  month for a stack self-hosting its database, cluster and cache; this book
  now takes **twenty**, the top of that range. 37signals report a delta of
  **zero** at a hundred times the fleet — "the same people who were operating
  HEY and Basecamp and the other apps in the cloud are now operating them on
  our own hardware" — and Ahrefs the same at 850 machines.
- **The interest is declared.** There is a measured figure close to this stack
  — about fourteen engineer-hours a month — and it was published by the
  company that publishes this book. It is corroboration and it is not
  independent, and a book that quietly cited its own publisher to move its own
  headline in its own favour would deserve everything it got. It is named in
  `costs.py`, named in the prose on the cost page, and the twenty hours stand
  on the independent figure without it.
- **The evidence against is in the file too.** Vendors selling managed
  Kubernetes put self-hosting at half an engineer to two. The rebuttal is not
  that they are biased — everyone here is — but that their itemised effort is
  SETUP, which this book already prices once as the person-days in the
  roadmap. Counting it again monthly charges the reader twice.
- **The cloud's own people cost was written as "already in the bill".** It is
  not: a cloud invoice bills for machines, not for whoever upgrades the
  managed cluster, rotates the credentials, argues with the bill and carries
  the pager. Both columns carry their own hours now, and Move 03 tells the
  reader to write both down. The saving is a delta and is unchanged by this;
  the percentage is not, and the old denominator was a bill with the salary
  taken out of it beside a column with the salary left in.
- **Renting looked cheaper than owning over five years, which is not
  possible.** Two errors cancelling: the rented machine was priced at $420 a
  month — $25,200 over sixty months for a box that costs $13,000 — and the
  model still came out ahead because the rented column also dropped the cage.
  The rent is $650, and `rent_vs_own_5yr()` now shows the arithmetic rather
  than asserting it: six machines cost $78,000 to buy and $234,000 to rent,
  three times the purchase price. Renting is correctly dearer on
  infrastructure. What it buys is no capital, no lead time, no cage and no
  contract.
- **Move 14 was charged twice for the same five weeks.** `wait_days` is
  defined as calendar time in which nobody works, and 3.0.1 booked the
  stateless rollout cadence as Wait *on top of* the ten days of effort spread
  across it. Thirty weeks end to end, not thirty-four.

### Added

- **"Why leave at all", the first section on the front page.** The book had no
  such section for three editions and the omission was deliberate — the front
  matter says the argument has been had. That was fair to the reader who had
  already decided and unfair to the one who had not. Five gains, every
  measurable one computed from the same model the cost page uses; four costs,
  written at the same length by the same hand; and four reasons to **stay
  exactly where you are**, which is the list that lets the rest be believed.
- **Five years, three ways.** Cloud against rented metal against colocation
  over the life of one generation of machines, with the capital on the line
  where it actually happens rather than buried in an amortisation figure. Both
  metal options save about a million dollars, and they land within a few
  thousand of each other — the whole of that difference being the residual,
  because after sixty months you still hold a working fleet.
- **Staging moves first, in Move 13.** Nothing told the reader to move the
  non-production estate before production, which is the sequencing decision
  the whole stage rests on. Staging is a real workload with real people who
  complain within the hour, and the only one whose bad afternoon appears on no
  invoice and wakes nobody. With a warning that staging still pointed at
  production data stores has not moved, it has been relocated.

### Changed — the design

- **The accent is green, and not only because blue was asked about.** The old
  `#79C8F2` sat a CIE distance of **12** from Stage 3's Build blue — about the
  point at which two colours stop being distinguishable — so the site had six
  colours doing five jobs and two of them were the same colour. `#7ED957` is
  **50** from its nearest neighbour, 125 degrees of hue away, 10.94:1 on the
  page and 9.78:1 on the hover fill. Paper gets `#2E6B18` at 6.5:1.
- **Two rules now keep money and interaction apart**, and they are structural
  because the problem is: under the commonest colour deficiency the accent and
  the money ochre sit at almost the same luminance, and no hue fixes that with
  blue off the table. So the accent is never a quantity, the money colour is
  never interactive, every money figure carries a `$` in a tabular column and
  every accent carries a shape. Colour is the second signal in both cases.
- **The masthead is brushed steel, not blue.** The largest object on the site
  was Cloud Blue, on a book about leaving the cloud.
- **The five Stage colours were respaced.** Chosen one at a time, they read
  together as five greys — which is the whole job of a Stage colour. The
  nearest pair in the palette is now 50 apart where about 10 is the threshold.
- Anchors no longer land under the sticky header: `--anchor` is measured from
  the real header height at runtime, because a guess is wrong the moment the
  nav wraps, which it does at six items and on every phone.

### Fixed — consistency

- Four places still said "half an engineer" after the model stopped believing
  it, and Move 03's rhetoric — the salary being "more than twice the whole of
  the hardware, the space and the link" — had silently inverted. All rewritten.
- `costs.py`'s self-test printed a different headline from the site, because
  it was still using the delta framing. Both now put the salary on both sides.

### Fixed

- **The book is four pages too short to print, and nothing said so.** KDP will
  not manufacture outside its page-count bands whatever the price works out at:
  a standard-colour paperback needs 72 pages and this interior is 68, and a
  hardcover needs 75. Both bands were written as a comment beside `INK` in
  `imprint.py` and nothing ever read them, so `pricing.py` cheerfully computed
  a margin for an edition that cannot be made — which is a submission rejected
  after the covers have been drawn. They are data now, and checked before any
  margin is. `PUBLISHING.md` carries the three ways out and what each costs.
- **The hardcover printing rate is no longer unset.** $5.65 fixed plus $0.080 a
  page, premium colour, large trim, read off KDP's own table — it is a property
  of the trim and the ink rather than of this title, so it carries. It only
  becomes usable if the interior reaches 75 pages.

## [3.0.1] - 2026-09-07

3.0.0 shipped with the roadmap on the front page invisible, and twenty-one
other defects an adversarial review found and reproduced. This fixes them, and
adds the gate that would have caught the first one.

### Fixed

- **The roadmap was invisible for the whole of 3.0.0.** The one drawing of the
  20 Moves across 34 weeks rendered as a blank 153px band under its own
  heading, above a caption describing a chart that was not there, for every
  reader whose scripting worked — and only appeared for readers whose scripting
  was broken. Its hidden state was a `clip-path` on the `<svg>` itself, and an
  IntersectionObserver measures its target **after** the target's own clip, so
  the observer saw an intersection rectangle of 0×0 and `isIntersecting: false`
  wherever the chart actually was on screen. It was never seen to arrive, so it
  was never revealed. The wipe now lives on a `<g>` inside the SVG; the
  observer watches the SVG, which is never clipped.
- **A new gate, `book/webcheck.py`, and `make webcheck`.** It drives the built
  site in a real browser, scrolls each of the seven page types the way a reader
  would, and fails if anything the build hid is still invisible at the end —
  plus the reduced-motion and app.js-blocked paths, and horizontal overflow at
  390px. Every check that ran before 3.0.0 passed: the markup was right, the
  CSS parsed, the links resolved, the contrast was fine, the element was in the
  document at its final position. It simply was not on the screen. This is now
  the third gate, in `make all`, in `make artefacts` and in CI. Confirmed
  against the bug: reinstating the 3.0.0 clip makes it fail with
  `index.html: svg.rm is still invisible after the whole page has been scrolled`.
- **The owned column did not add up.** $3,235 + $7,917 + $2,310 was printed
  under a total of $13,461. Every figure is rounded to the dollar, so the total
  has to be the sum of the rounded parts and not the rounded sum — on a page
  whose argument is that other people's comparisons are sloppy, the first sum a
  sceptic tries was a dollar out. Rounded once now, in one place, with the year
  and the percentage derived from it: $13,462 owned, $10,538 saved, 44 per cent.
- **The README headlined a $20,123 monthly saving** where the book computes
  $10,538 — the same repository committing the exact error its cost page calls
  the reason repatriations get approved and then regretted. Both numbers appear
  now, each under the name of what it is: line savings across the Moves, and
  the saving with everything counted. Its prose said "around 70 person-days"
  six lines above its own generated table saying 79.
- **Keyboard focus landed on rows still at opacity 0.** The reveal holds back
  anything in the bottom eight per cent of the window, which is right for
  scrolling and wrong for the Tab key: a reader tabbing down the checklist
  reached rows they could not see, with an invisible focus ring, and the next
  Space ticked a Move that gave no visible feedback. Anything focus lands
  inside is now shown at once, with a `:focus-within` backstop in CSS written
  out of the same list that does the hiding, so the two cannot drift.
- **Pressing Back showed a checklist that contradicted itself** — the row
  struck through and counted, its tick box visibly empty. A restored page is
  not re-executed; it repaints on `pageshow` now.
- **Ticking a Move while the summary was on screen left the summary wrong.** A
  count-up animation in flight kept writing an old number over the new one for
  the rest of its run. Runs are cancellable now, and a frame that finds the
  element has been written to by anything else stops.
- **A missing corpus script painted "0 Moves left" and "$0 still on the
  table"** above twenty unticked boxes — the opposite of the truth, and the
  central claim of the book. `paintSummary` now has the guard `paintNext`
  already had.
- **Unticked tick boxes were drawn at 1.90:1** against the page — below the 3:1
  floor for a control boundary, so the checklist read as a plain list of titles
  and the one thing the page exists to do was invisible until hovered. They are
  `--ink4` now, at 5.53:1.
- **The printed cost chart's key overprinted itself.** Labels sat under the
  start of the segments they named, which works at two segments and collided at
  three into "INFRASTRUC☒RRIED TIME". It is a measured legend row now, so the
  three colours are always named — dropping the colliding label would have
  dropped the salary, which is the argument.
- **On a phone:** the twenty-Move strip gave each link an 11.8px target with
  3px between them, under half the 24px floor, and its ordinals ran together
  into unbroken runs of digits — it scrolls now, with real targets and room for
  each number; a ticked runbook step drew a bright Stage-coloured line straight
  through its own body text, because the fill was hidden with the track left
  behind; and the cost chart's saving figure was left out of the font bump and
  rendered at about 6px — the two numbers that are the whole argument of the
  page.
- **The twenty printed as twenty hairlines**, backgrounds being dropped in
  print by default, under a caption describing a chart of bars.
- **The website printed the rented column with no caveat** while the printed
  interior of the same edition warned about it — the free, linked, most-read
  artefact was the one stating an unsourceable figure as fact.
- **Move 07's Swap note compared a whole rented column against an
  infrastructure-only line**, so a reader with a real quote at the top of the
  book's own range saw double the cost where the note promised level. It
  compares like with like now.
- Smaller: `site.py`'s comment about the Move table still said its rows sum to
  less than the headline while the prose below said more; `bar()`'s docstring
  still said the header is not sticky, two editions after it became sticky; and
  the override keeping the two charts from double-animating was wrapped in
  `:where()`, so it lost on source order to the rule `site.py` appends.

## [3.0.0] - 2026-09-07

A fact-check and a redesign. The fact-check moved a headline the book prints on
its cover, so this is a major version rather than a minor one: the saving is
44 per cent, not 54, and the programme is 79 person-days across 34 weeks, not
74 across 29. Nothing about the argument changed. What changed is that the
arithmetic behind it is now right, and the two figures that could not be
verified say so out loud instead of being quoted as though they had been.

### Fixed

- **The saving was overstated by $2,310 a month, and this is the important
  one.** Move 04 concludes that three things never come home — the content
  delivery network, outbound mail deliverability and volumetric scrubbing at
  the edge — and tells the reader in as many words to write them into the
  comparison as a permanent line. The comparison had no row for them. Nor for
  the residue five later Moves leave behind: archived object storage, a
  registry, a queue, an off-site backup copy. All of it is inside the $24,000
  on the left and all of it is still there on the right, so the model counted
  it once and paid it twice. Owning is **$13,461** a month, not $11,151; the
  saving is **$10,539 and 44 per cent**, not $12,849 and 54. The figure is
  derived rather than typed — it is the Now column of the Move files, which
  the cost page already printed in a table footer three sections below the
  comparison that omitted it. Move 03 gains a runbook step for it, because
  Move 03 is where the owned column gets built and it listed hardware, space,
  transit, cross-connect, hands and salary with no slot for the one line
  Move 04 tells you to add.
- **Three AWS list prices were wrong**, each re-checked against
  `pricing.us-east-1.amazonaws.com` offer files rather than a pricing page.
  RDS PostgreSQL `db.r7g.2xlarge` was $1.0368 an hour and labelled Multi-AZ;
  Multi-AZ is **$1.913** and Single-AZ is $0.956, so the figure was a Multi-AZ
  label on something under the Single-AZ price — a 46 per cent understatement
  on the line this book leans on hardest. ElastiCache `cache.r7g.large` was
  $0.2016 and is **$0.219** (Valkey is $0.1752 for the same machine, which is
  now in the comment because a fifth off is worth knowing). Egress was a flat
  $0.09 a gigabyte, which is the first tier only: it is tiered at 0.09, 0.085,
  0.07 and 0.05, so the flat sum overstated 100 TB by **$1,229 and 15 per
  cent**. The function walks the bands now and applies the 100 GB free
  allowance, which changes nothing at this size and is the same class of error
  in the other direction.
- **A managed Kubernetes control plane is $73 a month, not $220.** Ten cents
  an hour at all three providers, times 730. `costs.py` had held that ten cents
  in a constant nothing had referenced since it was written, while Move 11 said
  $220 in its prose and in its numbers strip. There is a function now, so the
  two cannot disagree again.
- **Move 14 was under-booked, and it is the only estimate here that went up.**
  Its runbook says to repeat across the stateless estate at two services a
  week; its strip booked five days and one week, for one service, while
  claiming the whole $6,800 of managed container compute. Ten days and five
  weeks is what the Move as written actually costs. Its "what you can turn
  off" no longer invites somebody to kill the managed runtime after the first
  service's soak.
- **Six claims about the three clouds were stale**, each replaced after the
  vendor's current documentation was fetched and read. The Google calculator
  does not silently apply sustained-use discounts (Move 03). Azure boot
  diagnostics has not needed a storage account of yours for years (Move 09). A
  GKE maintenance exclusion caps at 90 days, not 180 (Move 11).
  `azure.extensions` is dynamic, and the restart belongs to
  `shared_preload_libraries` (Move 16). Backup and DR's appliance requirement
  no longer holds for the console-native path, and a backup vault's enforced
  retention is the better gotcha anyway (Move 19). Azure DDoS Protection is
  layer 3 and 4 only, so the row claiming to replace AWS Shield *and* WAF has
  to name the WAF (the equivalence table).
- **The on-ramp is $3,430, not $1,840.** A 64 GB kit now costs more than the
  refurbished machine it goes into. It was three weekends and the price of a
  laptop; it is three weekends and the price of two.
- Smaller, all verified in the repository: `deps.py` said twenty-eight edges
  while its own `__main__` printed thirty-one; a comment said Move 07 would
  read as minus $1,250 where the file says $1,400; the comment above the Move
  table said its rows sum to less than the headline when they sum to more, and
  the sentence explaining the gap named half of it; Move 07 said the $1,400
  buys "the space, the power" when power is charged per node on draw and the
  fourth line is transit; the rack comment said a 3 kW commitment while Move
  07 said 4, and Move 07 is right; `DEDICATED`'s comment said "at five
  machines" where every caller passes six.

### Changed

- **Two numbers are now labelled as not re-priced, rather than quoted as
  though they had been.** The monthly rent of a dedicated machine could not be
  settled: the cheapest European provider lists a 48-core / 128 GB / 7.68 TB
  box near $371 and the reference spec is double that memory and double that
  disk, while a three-provider survey put the class near $1,100 on a citation
  whose cheapest entry was a desktop part wearing a server's name. At $420
  renting is well under owning; near $1,100 it is level. The book will not
  pick between those on a number nobody could source, so the figure stands as
  last observed, `costs.py` says so at the constant, and the prose around it
  no longer draws a conclusion that needs it to be exact — Move 07 now tells
  the reader to get a quote, and says the spread between providers is a factor
  of two or three and wide enough to decide the question on its own. The
  hardware capital cost carries the same note for the same reason: it sits on
  the memory and NVMe market that moved the on-ramp node from $420 to $950.
- **What the fact-check did NOT change, having tried to.** The hypothesis put
  to the researchers was that colocation was priced too high and the saving
  therefore understated. A quarter rack at $650, transit at $450, a
  cross-connect at $150 and hands at $150 all came back inside the published
  bands, and the finding that argued otherwise was refuted on verification. So
  were the challenges to the $190 per kW power rate, the five-year
  amortisation, the $190,000 loaded engineer and the half an engineer of
  ongoing time. Those numbers stand exactly as written. Of sixty-five verdicts
  returned, forty-four findings did not survive being argued with.

### Changed — the website

- **It has depth, colour and motion, and it had none of the three.** The ground
  drops to `#0C0F11` so raised surfaces have somewhere to be raised from;
  anything that lifts wears one inset hairline of white at 5.5 per cent, which
  is a machined edge rather than a drop shadow used as decoration. Two fixed
  layers sit behind the page: a bloom above the masthead with a hairline grid
  masked away below the first screenful, and three octaves of noise at three
  per cent, which is the only thing that stops a near-black gradient banding.
- **Colour does two jobs now instead of one.** It still marks a Stage. It also
  marks money — the saved column, the salaried-time bar, the delta on the
  chart — because the argument of this book is arithmetic and the arithmetic
  should be findable on the page.
- **New on the front page: the twenty.** One bar a Move, as tall as that Move's
  own effort figure, in its Stage's colour, every one of them a link. It is the
  contents page and the shape of the work in one object, and the shape is the
  argument — the heavy days are in the middle, not at the start.
- **New on the cost page: the datum.** Today's bill drawn as a dashed rule the
  height of the chart, with every row below it carrying a measured gap to that
  rule, labelled with what the gap is worth. Three bars of different lengths
  ask the reader to do the subtraction; a bar, a gap and a figure in the gap
  have already done it. The bars carry three segments now, the third being the
  line that never comes home.
- **The header is sticky, and it was deliberately not.** Twenty-five pages in a
  fixed order, and the header carries the one thing that knows where you are in
  them; a reader four screens down a Move page had to go back to the top to use
  it. It halves its padding once the masthead is behind it, and on a phone it
  folds the nav row away entirely — 36px of chrome instead of 96.
- **Prose never moves and is never hidden.** Only structure arrives: headings,
  figure strips, rows, tables, charts, controls. A Move page does not arrive at
  all, because it is worked rather than read, and a runbook step that fades in
  as somebody scrolls to it is a step arguing with the person running it.
- **The reveal has a dead man's handle.** The head of every page sets the class
  that allows anything to be hidden and immediately arms a two-second timer to
  remove it; `app.js` clears that timer as its first act. With the script
  blocked, missing, or throwing, the timer fires and the reader gets the whole
  page. Verified four ways, including a reload halfway down a document — which
  had left every element above the fold at opacity 0, because an observer only
  ever reports what is on screen and those had already gone past it.
- **The reveal list lives in one place.** It used to be a selector list in
  `style.css` and a string in `app.js`, and a selector added to one and not the
  other left an element invisible for the life of the edition. `site.py` owns it
  and writes both.
- Contrast was audited on every page type at 1440 and 390: **no pair below
  4.5:1**, including against the hover fill, which is the pair that actually
  occurs and the one the old palette never checked. The money colour had no
  paper value and printed at 1.84:1 on white; it has one now, at 5.5:1.

## [2.1.1] - 2026-09-07

### Fixed
- **The about page printed the PDF and EPUB file sizes,** which made `site/` fail
  its own reproducibility check and turned the release build red on a commit that
  had changed nothing. Both artefacts carry a build timestamp, so both are excluded
  from that check by name — and a size read off their bytes and written into an
  HTML page walked straight past the exclusion. The cards now carry the trim size
  and the Move count, which are derived from the sources like everything else.

## [2.1.0] - 2026-09-07

### Changed
- **The website is dark, and only dark.** It used to carry two palettes and follow
  the reader's system setting. One theme is one set of numbers to hold at contrast,
  and it is the theme the cover, the wordmark and the favicon were already drawn in.
  Every Stage colour now resolves to the hex `parse.LAYERS` chose for a near-black
  ground rather than the one chosen for paper, so the signals read at 5.4:1 or better
  instead of the 2.2:1 the paper hexes measured there.
- **Paper is still paper.** The printed interior is unchanged, and the site's own
  print stylesheet puts the light palette and the paper Stage colours back, so
  Ctrl-P gives a readable page rather than a flooded one.

## [2.0.0] - 2026-09-07

**The startup edition.** The book is rewritten from 122 Moves to 20, and the website from
sixteen page types to five. It is the same argument at a size somebody can act on.

The previous edition was correct and unusable. Computed from its own Move files it was 975
person-days of labour and a critical path of 160 weeks — 242 weeks with three engineers, 201
with six. Four and a half years is not a plan; it is a reason to do nothing. A startup with
two or three engineers and a $24,000 monthly bill has no way in to a document like that, and
the document is what the reader was actually blocked on.

### Changed
- **Twenty Moves, in five stages of four.** Decide, Buy, Build, Move, Run. Around 70
  person-days of labour and about half a year end to end for two engineers, and most of the
  calendar is hardware lead time rather than work. Every figure is computed from the Move
  files as before; none is typed.
- **Stages are verbs, not layers.** The seven Parts named after the system diagram — Iron,
  Site, Cluster, Platform, Data, Edge, Watch — are gone. An architect thinks in layers;
  somebody halfway through the work thinks about their week. "Stage 3 · Build" answers
  *where am I* without a diagram.
- **The reference build is one site, five machines and a spare,** at 32 cores and 256 GB a
  node. It was two sites and twelve. Two sites doubles the hardware, doubles the operational
  surface and is the most common reason a repatriation runs out of energy; one site with
  proven off-site backups is the honest answer at this size.
- **The cost model is a startup's.** A $24,000 monthly bill against $11,151 owned, of which
  $7,917 is the salary line. Half an engineer of ongoing work, not one and a half — five
  machines in one cage is not a platform team, and a book that asks a startup to hire two
  people to save $3,000 of hardware is asking it to lose money.
- **Move 07 says plainly that renting dedicated machines by the month is often the right
  answer,** and that at five machines it costs about the same as owning, because a quarter
  rack's fixed costs do not amortise over a small fleet. You own hardware when the fleet is
  big enough to carry the room.
- **Move 03 gives the reader permission to stop.** If the owned column does not come in a
  third under the rented one, three Moves and a week of work is the whole cost of finding
  out — against a programme abandoned in month five with two platforms live.
- **Ten rules became seven.** What survived being written for a company with two engineers.

### Removed
- **The website is five pages plus one per Move,** down from nine top-level pages, seven
  stage pages and 244 Move pages. About 50 files, down from 267.
- **The left rail, the sticky chrome, the spine, the jump box and the dependency planner.**
  All of them were instruments for somebody running a four-year programme. With twenty
  Moves in a fixed order, the order is the plan, and the checklist replaces the planner
  outright.
- **The roadmap, plan, symptoms, rollback, kit and replaces pages,** folded into the five
  that remain. The stage pages go with them: a stage is four Moves, and four Moves do not
  need an address of their own.
- **`docs/manifest.json` and `docs/manifest-critique.md`** — 273 KB of specification for the
  122 Moves that no longer exist. A repository carrying a detailed plan that contradicts its
  own contents is worse than one carrying none; both are in the history.

### Added
- **One "next" link, in the header of every page** — the lowest-numbered Move you have not
  ticked. The build renders Move 01 into it, which is correct for every reader on a first
  visit, so the answer is right before any script runs. That single line is the whole
  "what do I do next" experience, and it replaced a page.
- **A cost page that shows its working:** the three-way comparison, the salary line called
  out, where the money goes Move by Move, and what replaces what.

## [1.3.0] - 2026-09-07

The website rebuilt as an instrument rather than a document. No Move changed; the 122
Moves, the schedule and the arithmetic are the same. This is presentation, navigation and
one factual correction.

### Added
- **A chrome on every page.** A 48px bar carrying the wordmark, a breadcrumb saying where
  you are, previous and next on a Move, a box that takes a Move number, how far you have
  got, and a menu of every page. It replaced a 265px masthead that was reprinted on all
  130 pages — a book cover glued to the top of every page of the book it wraps, and 39%
  of a phone's viewport before a word of content. The masthead now appears once, on the
  front page, where a cover belongs.
- **A way to name a Move.** There was none: no search, no jump, and the only routes to an
  arbitrary Move were to scroll a 7,600px checklist or hit a bar on the schedule drawing.
  The chrome now takes `87` or a title, `/` focuses it, and every Move has a numeric
  address — `m/87.html` — that resolves with no script and from a `file://` URL, so a
  Move is something you can say out loud in a datacentre.
- **The progress spine.** Seven segments under the chrome, one per stage, each as wide as
  that stage has Moves and filled in that stage's own colour as they are ticked. It is
  the printed book's fore-edge tab laid flat, it is a rule and some space, and it gives
  the 122 Move pages the progress readout they have never had.
- **A page per stage,** at `s/<stage>.html`. The book's own organising unit had no
  address, so the rail, the front page's starting points and every cross-reference
  pointed at a fragment of one very long document. Each carries the stage's figures, its
  lead times and its Moves, against the same ticks the checklist reads.
- **A page for the symptom index,** which was reachable only by scrolling the front page.
- **Keyboard navigation:** `/` for the jump box, `1`–`7` for a stage, arrows to turn the
  page on a Move. Stated once, in the footer.
- **Persistence where the work happens.** A Move page can tick its own runbook steps, its
  own pre-flight boxes and the Move itself; the kit page remembers its 46 procurement
  boxes. The page a reader spends most of their time on was the only one that wrote
  nothing, and a half-run runbook did not survive a reload.
- **The checklist can be filtered** by stage and by what is not done, remembers which
  stages you folded, and asks before clearing every tick.
- **A link gate in the build.** Every internal link and every fragment must resolve to a
  file and an id that exist, or the build fails.

### Changed
- **The rail is the primary navigation and is on every page** rather than two, and the
  stage you are in opens into its own Moves, so any Move is one click from any other Move
  beside it. Its second zone carries every page on the site with the current one marked —
  which is where Kit, What replaces what and About stop being reachable only from a 10px
  strip at the bottom of a seven-screen scroll.
- **Below 900px the rail becomes a seven-cell stage strip** across the top. It used to be
  `display:none`, which left the checklist as 11,364px of blind scroll on a phone with no
  landmark of any kind. Chrome on a phone falls from 330px to 92px.
- **A Move page leads with the runbook.** The first step used to begin 1,093px down the
  page, and "Before you start" rendered 2,548px *below* the runbook it is a prerequisite
  for. The order is now the order you work in: what you need, then the steps, then the
  rollback, then a rule and everything that is read rather than run. The runbook gets the
  only display-size heading and a rule down the ordinal gutter that fills as you tick.
- **A spec cell whose value is an em dash is not printed.** Sixty-five Moves were
  rendering three blank cells to say nothing three times.
- **A design system, where there were 33 spacing literals and 33 type sizes.** Nine
  spacing steps, nine type sizes, one label recipe in place of 42, three breakpoints in
  place of seven, and a container: prose ran to 274 characters a line at 2560px because
  nothing on the site had a maximum width.
- **The planner works from a `file://` URL.** It fetched its data, which is blocked there,
  so the page the navigation calls "Plan yours" was a grey apology in exactly the medium
  this book says it has to work in. The payload is inlined, as the front page's already
  was. Its rows are sentence case, its selected state is visible at last, and it says
  plainly that it needs JavaScript instead of printing an instruction nobody can obey.
- **The schedule answers first.** "242 working weeks — about 5.3 years with 3 engineers"
  is set at the size of an answer and follows the control; the drawing's week ruler is
  spaced from the room it has rather than a fixed step, which had put 61 three-digit
  labels into 1,060 units of drawing.
- **The roadmap has a table as well as a drawing**, because 29 of the bars are too narrow
  to carry their own number and a drawing is not reachable by keyboard.
- **The lookup table stacks on a phone.** 41% of it was visible, and the column carrying
  the answer — what you run instead — was not.

### Fixed
- **The seven Part colours were unreadable in the dark theme.** One hex per Part was
  inlined into the markup and used in both themes, so every Part signal — a numeral, a
  section rule, a rail tab, a bar on the schedule — landed between 2.2:1 and 3.6:1 on the
  dark ground, below the floor for a graphic and nowhere near what a numeral set in it
  needs. `parse.LAYERS` now carries both hexes, the markup carries `data-part` instead of
  a colour, and the stylesheet picks. Every rendered text pair on the site now passes
  WCAG AA in both themes; `--ink4`, which carried most of the site's labels, was 2.58:1.
- **The rollback page said three Moves cannot be undone. Thirteen can not.** The number
  was spelled out in prose in a repository whose rule is that no total is. It is now
  passed in and counted, so the print edition, the EPUB and the website cannot disagree
  with each other or with the Moves.
- The crew picker on the schedule page had a focus rule that could never match, so the
  one keyboard control on the page was invisible when focused.
- The rail never marked the current stage on the checklist — the one page where position
  is the whole question — and its links threw a reader out of the Move they were reading.
- Filtering the checklist after folding it showed a closed summary bar and a count of
  rows that were not on screen.
- The step ordinals were ARIA toggle buttons in the markup, so with no script every Move
  page offered 797 buttons that could not be pressed. They are upgraded by script now.
- The front page rendered its seven starting points twice with no script.
- The figures a stage page renders had no control that could reveal them.
- `<` is escaped in the inlined payload, so a Move title could not close the script
  element it sits in.
- Dead weight removed: a 58 KB asset nothing loaded, five unused imports — one of which
  ran the whole print builder as a side effect — and every CSS rule that matched no
  markup, including the stylesheet of a search bar removed two releases ago.

## [1.2.0] - 2026-09-07

Nothing about the book changed; `site/` is byte-identical to 1.1.0. This is how the book
gets published.

### Added
- **A release pipeline.** Pushing to the `release` branch runs the gates, builds the book,
  the covers, the Kindle edition and the site, publishes the site to Firebase Hosting,
  fetches the page it has just published and fails unless it is serving that version, then
  cuts a GitHub release with the editions attached. Running it by hand from the Actions tab
  offers a preview channel that publishes to an expiring URL and cuts nothing.
- **`make releasable`**, the gate the pipeline adds on top of `verify` and `audit`: a bumped
  version, a written changelog entry, nothing left under `[Unreleased]`, a tag that is free
  or already on this content, and an EPUB identifier that has not moved since the previous
  release. It writes the GitHub release notes out of the changelog, so they are never typed
  twice. It is deliberately not part of `make`, because CI has to stay green while work is
  in progress and this is the one check that must not pass until it should.
- **`make artefacts`**, which builds everything a release publishes in the order it has to
  be built. `site.py` copies the Kindle edition into `site/`, so the EPUB has to exist
  first — which `make book site covers epub` would not have done, and which no gate would
  have caught, because the committed-site check has to exclude the EPUB.
- The pipeline takes either a scoped service account or a CI token, because the Firebase
  CLI can only produce the second and asking for a credential the CLI cannot mint is a
  poor first run.

### Changed
- **The book has a Firebase project to itself.** It was one hosting site inside the
  imprint's project, sharing it with the imprint's own website — a shared blast radius for
  no benefit. It is now `back-to-metal`, one project, one site, and
  `backtometal.oneuptime.com` points at it. `.firebaserc` is the only place either name is
  written; the workflow reads both out of it.

## [1.1.0] - 2026-09-07

The website, laid out so it can be used rather than read. No Move changed; the book,
the PDF and the EPUB are the same 122 Moves. This is all presentation.

### Changed
- **The front page answers one question.** It used to be the whole checklist — seven
  stages, every Move, and five or six figures on every row, all of it on screen before
  the reader had decided anything. It now shows the single Move to do next: its number,
  its title, its hook, the five figures that decide whether it can start today, and a
  button to open it or tick it off. The build renders that answer, so it is correct with
  no JavaScript; script only substitutes a later Move once there is a tick to substitute
  it from.
- **The 122 rows moved to `checklist.html`,** which is the page you work down. A row is a
  tick box, a number and a title, and the title is the link. The six figures that used to
  sit on every row are still rendered on every row and hidden until asked for, because a
  column that reads `0 min` on 110 rows out of 122 is not information.
- **A row carries one flag, and only where the fact changes what you do:** `no way back`
  on the 13 Moves that cannot be undone, `NN min down` on the 12 that take the site off
  the air. The other 109 rows say nothing.
- **Each stage names the Moves with a lead time**, because nobody is working during a
  wait and a Move ordered late holds up everything behind it.
- **The symptom index moved to the front page,** which is where somebody who arrived with
  a problem rather than a programme will look. It was below the schedule drawing.
- **The masthead carries five figures instead of eight** and the navigation five links
  instead of ten. Person-days and weeks-at-three now live only on the roadmap page, which
  is the page that question belongs to; the reference pages and the downloads moved to
  the footer.
- **The rail appears only where the reader is inside the sequence** — the checklist and a
  Move — and its links point at the checklist.
- The "how to use this" box is gone, along with the only bordered tinted panel on the
  site. The page does the three things it described instead of describing them.

### Fixed
- The planner did nothing at all: `plan.html` never emitted the `.picker` root that
  `plan.js` requires, so every click was ignored.
- An author `display` rule outranked the user agent's `[hidden]`, so the planner's summary
  showed while it was still empty.

## [1.0.0] - 2026-09-06

The book itself. All **122 Moves** are written, across seven Parts, each one a complete
runbook rather than a placeholder: three named cloud services with the one thing that
genuinely differs on each, why the approach works, grouped prerequisites, a numbered
runbook, four operator's notes, a rollback that names its point of no return, a six-cell
numbers strip and a list of what can then be switched off.

### Added
- Part I, Iron (01-20): measurement, derating a vCPU, cores against licensing, memory,
  chassis and draw, management controllers, drives, capacity, the fabric, cards, cabling,
  out-of-band, suppliers, acceptance testing, spares, and the bill of materials.
- Part II, Site (21-38): what a desk cluster cannot prove, the four landing options,
  the on-premises room, the second site, the address, cross-connects, tier ratings,
  the power schedule, service credits, the exit, the cabinet, feeds, cooling, importing,
  access, the first rack, the as-built, and decommissioning.
- Part III, Cluster (39-54): addressing and the three clocks, the management VLAN, Talos,
  netboot, the control plane, Cilium, BGP, cluster DNS, local NVMe, encryption at rest,
  Ceph under Rook, OIDC, the second cluster, the restore drill, the links, and the object store.
- Part IV, Platform (55-70): workload identity, secrets, the root of trust, the registry,
  signing and admission, east-west policy and encryption, metrics, logs and traces, builds,
  Argo CD, provider-native templates, the first stateless service, the non-Kubernetes
  container services, the fixed fleet, and the workloads that stay virtual machines.
- Part V, Data (71-90): the Postgres pre-flight, the verification gate, Postgres, pgBackRest,
  quorum commit and fencing, the proprietary engines, MySQL, the licensed databases, Redis,
  brokers, queues, the event bus, Kafka, application buckets, the archive that stays, batch,
  search, document stores, the serverless estate, and orchestrated workflows.
- Part VI, Edge (91-107): your own ASN, dual-stack, transit, egress, the first VIP, BGP VIPs,
  TLS, Envoy Gateway, route translation, the API front door, edge authentication, the shadow
  edge, go-live, authoritative DNS, CDN, DDoS, and email.
- Part VII, Watch (108-122): the upgrade calendar, the fleet roll, the inventory, the 03:00
  disk, support contracts, the rota, alerting, backups and the rebuild drill, capacity
  planning, patch SLAs, audit logs, the auditor, what it costs, aborting, and the last account.
- A `Wait` column in every numbers strip, so the roadmap separates somebody's labour from
  calendar time that simply has to pass, and stops under-forecasting the programme.
- A plain "How to use this" block and one card per stage on the front page.

### Changed
- The symptom index and the equivalence table now point at the real Moves.
- `verify.py` accepts three-digit Move numbers; the website, the planner and the roadmap
  sort Move numbers numerically rather than as strings.


### Added
- The toolchain: `parse.py`, `verify.py`, `audit.py`, `build.py`, `render.py`, `site.py`,
  `epub.py`, `cover.py`, `kdpcheck.py`, `epubcheck.py`, `pricing.py`.
- The two gates. `verify.py` enforces the Move file contract, the cost arithmetic and the house
  style; `audit.py` enforces undeclared tools, unused prerequisites, unguarded destructive steps,
  unpinned installs, drifted AWS service names, the dependency invariant and repeated prose.
- Shared data modules: `deps.py`, `kit.py`, `costs.py`, `rollback_data.py`, `equivalents.py`,
  `symptoms.py`, `mission.py`, `imprint.py`.
- The website, including the migration planner: pick the Moves you need and it closes the
  dependency set, orders it, and totals the downtime, the effort and the saving.
- Print geometry for KDP at 8.25x11 with bleed, mirrored margins, spread invariants asserted at
  build time, and a vertical-justification pass in headless Chromium.
