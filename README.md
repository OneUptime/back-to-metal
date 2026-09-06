# Back to Metal

**Leaving the cloud with Kubernetes**, by the makers of
[OneUptime](https://oneuptime.com), published three ways: a printable
book, a reflowable EPUB, and a static website you can host anywhere.

The reason cloud repatriations fail is rarely the technology. It is that they are attempted as
one decision, executed as one project, and abandoned somewhere in the middle with two platforms
running and nobody able to say whether it is going well.

This book is the opposite shape. It is a sequence of **Moves**. Each is one job with a stated
cutover in minutes of user-visible downtime, a stated risk, and a rollback that names its point
of no return. Each can be done on a Tuesday and undone on a Wednesday, and you can stop after
any of them and still be somewhere coherent.

📕 **[dist/Back-to-Metal.pdf](dist/Back-to-Metal.pdf)** &nbsp;·&nbsp;
📖 **[dist/Back-to-Metal.epub](dist/Back-to-Metal.epub)** &nbsp;·&nbsp;
🌐 **[site/](site/)** — open `site/index.html`

## Three clouds, one runbook

Every Move covers **AWS, Google Cloud and Azure**. The job is the same whichever you are
leaving; only the extraction differs, so only the extraction is written three times. Each Move
opens with three lines naming the real product on each provider and the one thing that is
genuinely different there — a flag that needs a reboot, a tier that cannot do it at all, a
resource that outlives its parent. The runbook itself is written once.

## It is honest about what not to move

Several Moves conclude that you should keep paying somebody else. A global content network,
scrubbing capacity at the edge and outbound mail deliverability are businesses other people run
better than you will, and each is cheap next to what it replaces. A book that claims everything
can be repatriated is selling something.

## The dependency invariant

Every Move's prerequisites are **lower-numbered Moves**. A reader who has reached Move 40 has,
by construction, met every prerequisite of Move 40. That is not a stylistic choice — the build
refuses to compile a book where it does not hold, and it is what lets the website's planner
order a migration by sorting rather than searching.

## Layout

```
moves/       the Move files, numbered from 01 — the source of truth
book/        the typesetter and the site generator
  parse.py       markdown -> structured Move data
  verify.py      structure: the contract, the arithmetic, the house style
  audit.py       content: undeclared tools, unguarded destructive steps,
                 unpinned installs, drifted service names, repeated prose
  build.py       Move data -> a self-contained book.html
  render.py      html -> PDF via headless Chromium, vertically justified
  site.py        Move data -> a static website in site/
  epub.py        Move data -> a reflowable EPUB3
  cover.py       the paperback wrap, the Kindle cover, the hardback case
  deps.py        which Moves must be finished before which
  kit.py         the reference build, the laptop kit, the ten rules
  costs.py       the cost model, with the salary line in it
  equivalents.py AWS to Google Cloud to Azure to what you run instead
  rollback_data.py  the safety page every Move's rollback derives from
  symptoms.py    the symptom index — "which Move do I need"
  icons.py       Part glyphs, the cutover gauge, the risk bars, the page anatomy
  style.css      the print stylesheet
  web/           the site's stylesheet and scripts
dist/        the built PDF, EPUB and covers
site/        the built website
build/       intermediate HTML (gitignored)
```

## Building

```bash
make deps       # fonts, playwright, chromium
make verify     # structure — must be clean
make audit      # content — must be clean
make book       # markdown -> HTML -> PDF -> KDP compliance check
make site       # markdown -> static website
make            # all of it, and the tables in this README
```

Python 3.9 or newer with `playwright` and a Chromium build available to it. The Makefile prefers
`.venv/bin/python3` when it exists, so `python3 -m venv .venv && make deps` works without
activating anything.

`verify.py` and `audit.py` are the gate and both must come back clean. `verify.py` checks the
shape of every Move: the sections, the three-cloud block, the cost arithmetic, and that no Move
moving persistent state ships without saying how the state comes back. `audit.py` goes after the
things that are actually wrong in infrastructure writing — a runbook calling a tool the
prerequisites never mentioned, a destructive command with nothing standing behind it, software
installed without a version, a service spelled four ways, prose copy-pasted between Moves.

## The website

`site/` is self-contained — the fonts are embedded in the stylesheet and nothing is fetched at
runtime — so it drops onto any static host unchanged. It carries a **migration planner**: tick
the Moves you need and it closes the dependency set, orders it, and totals the downtime, the
effort and the saving. The plan lives in the address bar, so it is a link you can send to
whoever has to approve it.

## Contributing

The most valuable contribution is a **correction**. If you ran a runbook and it did not work as
written, that is worth an issue on its own. [CONTRIBUTING.md](CONTRIBUTING.md) covers the
workflow; [AGENTS.md](AGENTS.md) documents the Move contract, the house style the build
enforces, and what not to hand-edit.

## Licence

Two licences, because this repository is two things:

- **The software** — the toolchain in `book/`, the print stylesheet, the site's stylesheet and
  scripts — is [MIT](LICENSE).
- **The content** — the Moves, the written text of the book — is
  [CC BY 4.0](LICENSE-CONTENT).

So you may share and adapt any of it, for any purpose including commercially, as long as you
give credit.

<!-- generated: everything below this line is written by book/readme.py -->
